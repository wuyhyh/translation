from __future__ import annotations

import html
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from .chunker import Chunk, PAGE_MARKER_RE, split_markdown_units
from .progress import ProgressStore
from .translator import BackendResponse, create_backend, glossary_prompt, load_glossary, resolve_backend, _validate_translation
from .util import atomic_write_text, utc_now


REPAIR_SYSTEM_PROMPT = """Translate the supplied English technical-book Markdown into accurate, natural Simplified Chinese.
Return only the translation. Do not add explanations or summaries.
Tokens such as __KEEP_000001__ are immutable placeholders: preserve every token exactly once and in the original order.
Do not emit thinking, reasoning, a preface, or an outer code fence.
"""


PROTECTED_RE = re.compile(
    r"```[\s\S]*?```"
    r"|!\[[^\]]*\]\([^\)]+\)"
    r"|`[^`\n]+`"
    r"|https?://[^\s<>\])]+"
    r"|(?:[A-Za-z]:\\[^\s<>|]+|(?:\.{0,2}/)?(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+)"
    r"|\b0x[0-9A-Fa-f]+\b"
    r"|\b(?:R(?:1[0-5]|[0-9])|SP|LR|PC|xPSR|MSP|PSP|PRIMASK|BASEPRI|FAULTMASK|CONTROL)\b"
    r"|\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b"
    r"|\b(?:HAL|LL)_[A-Za-z0-9_]+\b"
    r"|\b[A-Za-z_][A-Za-z0-9_]*(?=\()"
    r"|(?<![A-Za-z0-9_])\d+(?:\.\d+)*(?:[A-Za-z%]+)?"
    r"|(?:\.\s*){4,}"
    r"|^(?:#{1,6}|\s*(?:[-*+]|\d+\.)|\s*>)[ \t]+",
    re.M,
)
PLACEHOLDER_RE = re.compile(r"__KEEP_\d{6}__")


@dataclass
class RepairSummary:
    before_completed: int
    before_failed: int
    repaired: int
    remaining_failed: int
    repaired_pages: List[int]
    requests: int
    retries: int
    input_tokens: int
    output_tokens: int
    reasoning_present: bool
    backend: str
    actual_model: str


def queue_repaired_chunks(progress: ProgressStore) -> List[str]:
    """Queue only chunks previously produced by the failed-block repair path."""
    queued: List[str] = []
    for chunk_id, item in progress.snapshot().get("chunks", {}).items():
        if item.get("status") == "completed" and item.get("repaired"):
            progress.set_status(
                chunk_id, "failed",
                error="完整性复核：使用强化占位符与逐单元完整性校验重新修复",
                repair_revalidation_queued_at=utc_now(),
            )
            queued.append(chunk_id)
    return queued


def split_pages(source: str) -> List[Tuple[int, str]]:
    matches = list(PAGE_MARKER_RE.finditer(source))
    if not matches:
        raise ValueError("源块不包含物理页码标记")
    pages = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        pages.append((int(match.group(1)), source[match.end():end].strip()))
    return pages


def protect_text(text: str) -> Tuple[str, Dict[str, str]]:
    mapping: Dict[str, str] = {}

    def replace(match: re.Match) -> str:
        token = f"__KEEP_{len(mapping):06d}__"
        mapping[token] = match.group(0)
        return token

    return PROTECTED_RE.sub(replace, text), mapping


def restore_text(text: str, mapping: Dict[str, str]) -> str:
    found = PLACEHOLDER_RE.findall(text)
    expected = list(mapping)
    if found != expected:
        raise ValueError(f"占位符丢失、重复或顺序改变: expected={expected}, output={found}")
    for token, original in mapping.items():
        text = text.replace(token, original)
    return text


def _has_translatable_text(protected: str) -> bool:
    without_tokens = PLACEHOLDER_RE.sub("", protected)
    without_anomaly = re.sub(r"\[原文提取异常，第\d+页\]", "", without_tokens)
    return bool(re.search(r"[A-Za-z]{2,}", without_anomaly))


def _request(
    backend: object, model: str, glossary: str, protected: str,
    max_retries: int, on_attempt, validator=None,
) -> Tuple[str, List[BackendResponse], int]:
    responses: List[BackendResponse] = []
    last_error: Optional[Exception] = None
    for retry in range(max_retries + 1):
        on_attempt(retry)
        try:
            response = backend.chat(model, [
                {"role": "system", "content": REPAIR_SYSTEM_PROMPT},
                {"role": "user", "content": glossary + "\n\nTEXT:\n" + protected},
            ], 0.1)
            responses.append(response)
            if response.reasoning_present:
                raise RuntimeError("修复请求仍产生 reasoning")
            if response.finish_reason.lower() in {"length", "max_tokens"}:
                raise RuntimeError("修复请求被 length 截断")
            if validator is not None:
                validator(response.content.strip())
            return response.content.strip(), responses, retry
        except Exception as exc:
            last_error = exc
            if retry < max_retries:
                time.sleep(min(2 ** retry, 8))
    raise RuntimeError(str(last_error) if last_error else "修复请求失败")


def _translate_protected(
    text: str, backend: object, model: str, glossary: str,
    max_retries: int, on_attempt,
) -> Tuple[str, List[BackendResponse], int]:
    protected, mapping = protect_text(text)
    if not _has_translatable_text(protected):
        return text, [], 0
    def validate(candidate: str) -> None:
        restore_text(candidate, mapping)
        _validate_semantic_completeness(protected, candidate)

    translated, responses, retries = _request(
        backend, model, glossary, protected, max_retries, on_attempt, validate,
    )
    return restore_text(translated, mapping), responses, retries


def _validate_semantic_completeness(source: str, translated: str) -> None:
    """Reject obvious omissions while allowing Chinese to be much more compact."""
    source = PLACEHOLDER_RE.sub("", source)
    translated = PLACEHOLDER_RE.sub("", translated)
    source_letters = len(re.findall(r"[A-Za-z]", source))
    if source_letters < 20:
        return
    output_ascii = len(re.findall(r"[A-Za-z]", translated))
    output_cjk = len(re.findall(r"[\u3400-\u9fff]", translated))
    weighted_output = output_ascii + output_cjk * 3
    if weighted_output < max(8, source_letters * 0.28):
        raise ValueError(
            f"候选译文明显不完整: source_letters={source_letters}, "
            f"weighted_output={weighted_output}"
        )


def _translate_fragmented(
    text: str, backend: object, model: str, glossary: str,
    max_retries: int, on_attempt,
) -> Tuple[str, List[BackendResponse], int]:
    """Translate only gaps between protected spans; protected text never reaches the model."""
    output: List[str] = []
    responses: List[BackendResponse] = []
    retries = 0
    position = 0
    for match in PROTECTED_RE.finditer(text):
        gap = text[position:match.start()]
        if _has_translatable_text(gap):
            leading = re.match(r"\s*", gap).group(0)
            trailing = re.search(r"\s*$", gap).group(0)
            core_end = len(gap) - len(trailing) if trailing else len(gap)
            core = gap[len(leading):core_end]
            translated, gap_responses, gap_retries = _request(
                backend, model, glossary, core, max_retries, on_attempt,
                lambda candidate, original=core: _validate_semantic_completeness(original, candidate),
            )
            output.append(leading + translated + trailing)
            responses.extend(gap_responses)
            retries += gap_retries
        else:
            output.append(gap)
        output.append(match.group(0))
        position = match.end()
    tail = text[position:]
    if _has_translatable_text(tail):
        leading = re.match(r"\s*", tail).group(0)
        trailing = re.search(r"\s*$", tail).group(0)
        core_end = len(tail) - len(trailing) if trailing else len(tail)
        core = tail[len(leading):core_end]
        translated, tail_responses, tail_retries = _request(
            backend, model, glossary, core, max_retries, on_attempt,
            lambda candidate, original=core: _validate_semantic_completeness(original, candidate),
        )
        output.append(leading + translated + trailing)
        responses.extend(tail_responses)
        retries += tail_retries
    else:
        output.append(tail)
    return "".join(output), responses, retries


def _translate_page(
    page_number: int, body: str, backend: object, model: str, glossary: str,
    max_retries: int, on_attempt,
) -> Tuple[str, List[BackendResponse], int, bool]:
    marker = f"<!-- page: {page_number} -->"
    if not body.strip():
        return marker, [], 0, False
    candidate = ""
    try:
        if len(body) > 2500:
            raise ValueError("页面过长，直接使用安全小单元")
        translated, responses, retries = _translate_protected(
            body, backend, model, glossary, max_retries, on_attempt,
        )
        candidate = marker + "\n\n" + translated.strip()
        _validate_translation(marker + "\n\n" + body, candidate)
        _validate_exact_code(marker + "\n\n" + body, candidate)
        return candidate, responses, retries, False
    except Exception:
        outputs: List[str] = []
        all_responses: List[BackendResponse] = []
        total_retries = 0
        for unit in _safe_repair_units(body):
            try:
                translated, responses, retries = _translate_protected(
                    unit, backend, model, glossary, max_retries, on_attempt,
                )
            except Exception:
                translated, responses, retries = _translate_fragmented(
                    unit, backend, model, glossary, max_retries, on_attempt,
                )
            outputs.append(translated.strip())
            all_responses.extend(responses)
            total_retries += retries
        candidate = marker + "\n\n" + "\n\n".join(outputs)
        _validate_translation(marker + "\n\n" + body, candidate)
        _validate_exact_code(marker + "\n\n" + body, candidate)
        return candidate, all_responses, total_retries, True


def _safe_repair_units(text: str, maximum: int = 900) -> List[str]:
    """Split long prose/TOC paragraphs, never fenced code, images, or tables."""
    result: List[str] = []
    for unit in split_markdown_units(text):
        if len(unit) <= maximum or unit.startswith("```") or unit.startswith("![") or unit.lstrip().startswith("|"):
            result.append(unit)
            continue
        # PDF extraction often collapses a whole table-of-contents page into one
        # paragraph. Split before numbered TOC entries first, then apply a bounded
        # whitespace split. No source character is discarded.
        toc_parts = re.split(r"(?=\s+\d{1,2}(?:\.\d+){1,4}\s+[A-Z])", unit)
        pending = [part for part in toc_parts if part]
        if len(pending) == 1:
            pending = [unit]
        for part in pending:
            _append_bounded_unit(result, part, maximum)
    return result


def _append_bounded_unit(result: List[str], unit: str, maximum: int) -> None:
    remaining = unit
    while len(remaining) > maximum:
        split_at = remaining.rfind(" ", 0, maximum + 1)
        if split_at < maximum // 2:
            split_at = remaining.find(" ", maximum)
        if split_at < 0:
            break
        result.append(remaining[:split_at].rstrip())
        remaining = remaining[split_at:].lstrip()
    if remaining:
        result.append(remaining)


def _code_blocks(text: str) -> List[str]:
    return re.findall(r"```[^\n]*\n[\s\S]*?```", text)


def _validate_exact_code(source: str, translated: str) -> None:
    if _code_blocks(source) != _code_blocks(translated):
        raise ValueError("代码块内容被改动")


def write_failed_report(
    progress: ProgressStore, destination: Path,
    error_log: Path = Path("logs/requests-errors.jsonl"),
) -> Dict[str, int]:
    data = progress.snapshot()
    failed = []
    for chunk_id, item in data.get("chunks", {}).items():
        if item.get("status") == "failed":
            failed.append((min(item.get("pages") or [10**9]), chunk_id, item))
    failed.sort()
    historical_chunks = set()
    historical_rows = 0
    if error_log.exists():
        for raw in error_log.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                continue
            chunk_id = row.get("chunk_id")
            if chunk_id and data.get("chunks", {}).get(chunk_id, {}).get("status") == "completed":
                historical_chunks.add(str(chunk_id))
                historical_rows += 1
    lines = [
        "# Final failed blocks", "",
        "This report uses the final status in `work/progress.json`; historical log errors are not treated as final failures.", "",
        f"Final failed blocks: **{len(failed)}**", "",
        f"Historical error rows belonging to chunks that later completed: **{historical_rows}** across **{len(historical_chunks)}** chunks.",
        "These historical errors are excluded from the table below.", "",
        "| chunk_id | PDF pages | Final error | Source file | Attempts |", "|---|---:|---|---|---:|",
    ]
    for _, chunk_id, item in failed:
        pages = _format_pages(item.get("pages") or [])
        error = str(item.get("error") or "").replace("|", "\\|").replace("\n", " ")
        source = str(item.get("source_file") or "")
        attempts = int(item.get("attempts", 0) or 0)
        lines.append(f"| `{chunk_id}` | {pages} | {error} | `{source}` | {attempts} |")
    destination.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(destination, "\n".join(lines) + "\n")
    return {"failed": len(failed), "historical_completed_chunks": len(historical_chunks), "historical_error_rows": historical_rows}


def _format_pages(pages: Iterable[int]) -> str:
    values = sorted(set(int(page) for page in pages))
    if not values:
        return ""
    groups = []
    start = previous = values[0]
    for page in values[1:]:
        if page == previous + 1:
            previous = page
            continue
        groups.append(str(start) if start == previous else f"{start}-{previous}")
        start = previous = page
    groups.append(str(start) if start == previous else f"{start}-{previous}")
    return ", ".join(groups)


def _manual_review(path: Path, chunk: Chunk, source: str, candidate: str, error: Exception) -> None:
    content = (
        f"# Manual review: {chunk.chunk_id}\n\n"
        f"- Pages: {_format_pages(chunk.pages)}\n- Error: `{html.escape(str(error))}`\n\n"
        "## Source\n\n```markdown\n" + source + "\n```\n\n"
        "## Candidate translation\n\n```markdown\n" + candidate + "\n```\n"
    )
    atomic_write_text(path, content)


def repair_failed_chunks(
    progress: ProgressStore, base_url: str, api_key: str, model: str,
    glossary_path: Path, reports_dir: Path, timeout: float = 600,
    backend_name: str = "ollama", max_retries: int = 3,
) -> RepairSummary:
    snapshot = progress.snapshot()
    before_completed = sum(item.get("status") == "completed" for item in snapshot["chunks"].values())
    repair_ids = {
        chunk_id for chunk_id, item in snapshot["chunks"].items()
        if item.get("status") == "failed"
        or (item.get("status") == "pending" and item.get("repair_started_at"))
    }
    failed_chunks = [
        chunk for chunk in progress.load_chunks({"failed", "pending"})
        if chunk.chunk_id in repair_ids
    ]
    before_failed = sum(item.get("status") == "failed" for item in snapshot["chunks"].values())
    glossary = glossary_prompt(load_glossary(glossary_path))
    backend, probes = resolve_backend(backend_name, base_url, api_key, model, timeout, 1)
    repaired = requests = retries = input_tokens = output_tokens = 0
    reasoning_present = False
    repaired_pages = set()
    actual_model = model
    try:
        for chunk in failed_chunks:
            source = chunk.text
            candidate = ""
            progress.set_status(chunk.chunk_id, "running", repair_started_at=utc_now(), error=None)
            chunk_responses: List[BackendResponse] = []
            chunk_retries = 0

            def on_attempt(retry: int) -> None:
                progress.increment(chunk.chunk_id, "attempts")
                progress.increment(chunk.chunk_id, "repair_attempts")
                if retry:
                    progress.increment(chunk.chunk_id, "retries")
                    progress.increment(chunk.chunk_id, "repair_retries")

            try:
                page_outputs = []
                used_fine = False
                for page_number, body in split_pages(source):
                    page_output, responses, page_retries, fine = _translate_page(
                        page_number, body, backend, model, glossary, max_retries, on_attempt,
                    )
                    page_outputs.append(page_output)
                    chunk_responses.extend(responses)
                    chunk_retries += page_retries
                    used_fine |= fine
                candidate = "\n\n".join(page_outputs).strip() + "\n"
                _validate_translation(source, candidate)
                _validate_exact_code(source, candidate)
                output_path = Path(str(progress.snapshot()["chunks"][chunk.chunk_id]["output_file"]))
                atomic_write_text(output_path, candidate)
                chunk_input = sum(item.input_tokens for item in chunk_responses)
                chunk_output = sum(item.output_tokens for item in chunk_responses)
                chunk_reasoning = any(item.reasoning_present for item in chunk_responses)
                if chunk_responses:
                    actual_model = chunk_responses[-1].model
                progress.set_actual_model(actual_model, str(getattr(backend, "name", backend_name)))
                progress.set_status(
                    chunk.chunk_id, "completed", error=None, repaired=True,
                    repair_strategy="page-then-paragraph" if used_fine else "page",
                    repair_finished_at=utc_now(), input_tokens=chunk_input,
                    output_tokens=chunk_output, reasoning_present=chunk_reasoning,
                )
                repaired += 1
                repaired_pages.update(chunk.pages)
                requests += len(chunk_responses)
                retries += chunk_retries
                input_tokens += chunk_input
                output_tokens += chunk_output
                reasoning_present |= chunk_reasoning
                manual_path = reports_dir / "manual-review" / f"{chunk.chunk_id}.md"
                if manual_path.exists():
                    resolved_path = reports_dir / "manual-review" / "resolved" / manual_path.name
                    resolved_path.parent.mkdir(parents=True, exist_ok=True)
                    manual_path.replace(resolved_path)
            except Exception as exc:
                progress.set_status(chunk.chunk_id, "failed", error=str(exc)[:500], repair_finished_at=utc_now())
                _manual_review(reports_dir / "manual-review" / f"{chunk.chunk_id}.md", chunk, source, candidate, exc)
    finally:
        backend.close()
    remaining = len(progress.ids_with_status({"failed"}))
    return RepairSummary(
        before_completed, before_failed, repaired, remaining, sorted(repaired_pages),
        requests, retries, input_tokens, output_tokens, reasoning_present,
        str(getattr(backend, "name", backend_name)), actual_model,
    )
