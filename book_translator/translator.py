from __future__ import annotations

import json
import re
import threading
import time
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

import httpx
import yaml
from openai import OpenAI

from .chunker import Chunk, PAGE_MARKER_RE, split_chunk_text
from .progress import ProgressStore
from .util import atomic_write_text, utc_now


SYSTEM_PROMPT = """You are a professional translator of embedded-systems technical books. Translate the supplied English Markdown into accurate, natural Simplified Chinese.

Mandatory rules:
1. Preserve Markdown heading levels and every exact <!-- page: X --> marker.
2. Preserve fenced code blocks, commands, function names, variable names, macros, register names, file paths, and URLs. In code blocks translate comments only; do not alter any other code.
3. On the first occurrence of an important technical term, use Chinese (English); afterwards use the same Chinese term consistently. Follow the supplied glossary exactly.
4. Preserve image Markdown and its path; translate alt text only if useful.
5. Do not add explanations, summaries, facts, headings, or commentary absent from the source.
6. Preserve any [原文提取异常，第X页] marker exactly.
7. Return only the translated Markdown, without a preface or surrounding fence.
"""


class LengthTruncatedError(RuntimeError):
    pass


@dataclass
class BackendResponse:
    content: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_present: bool = False
    reasoning_characters: int = 0
    finish_reason: str = "stop"
    backend: str = ""
    requests: int = 1
    splits: int = 0


@dataclass
class ChunkResult:
    chunk_id: str
    success: bool
    pages: List[int]
    elapsed_seconds: float
    attempts: int = 0
    retries: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    requests: int = 0
    splits: int = 0
    reasoning_present: bool = False
    finish_reason: str = ""
    error: Optional[str] = None


@dataclass
class TranslationSummary:
    completed: int = 0
    failed: int = 0
    retries: int = 0
    attempts: int = 0
    requests: int = 0
    splits: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_present: bool = False
    wall_seconds: float = 0.0
    chunk_results: List[ChunkResult] = field(default_factory=list)
    backend: str = ""
    actual_model: str = ""

    def as_dict(self) -> Dict[str, object]:
        return asdict(self)


def load_glossary(path: Path) -> Dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(f"术语表不存在: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data.get("terms", {}), dict):
        raise ValueError("glossary.yaml 的 terms 必须是映射")
    return data


def glossary_prompt(data: Dict[str, object]) -> str:
    lines = ["Terminology (English => Simplified Chinese):"]
    for source, target in data.get("terms", {}).items():
        lines.append(f"- {source} => {target}")
    protected = data.get("protected_terms", [])
    if protected:
        lines.append("Keep these tokens unchanged: " + ", ".join(map(str, protected)))
    return "\n".join(lines)


def _reasoning_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


class OpenAIBackend:
    name = "openai"

    def __init__(self, base_url: str, api_key: str, timeout: float, workers: int):
        limits = httpx.Limits(max_connections=max(2, workers * 2), max_keepalive_connections=max(2, workers))
        self.http = httpx.Client(timeout=httpx.Timeout(timeout), limits=limits)
        self.client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout, max_retries=0, http_client=self.http)

    def chat(self, model: str, messages: List[Dict[str, str]], temperature: float) -> BackendResponse:
        response = self.client.chat.completions.create(
            model=model, temperature=temperature, messages=messages,
            extra_body={"think": False, "keep_alive": -1},
        )
        choice = response.choices[0]
        message = choice.message
        extras = getattr(message, "model_extra", None) or {}
        reasoning = _reasoning_value(getattr(message, "reasoning", None))
        reasoning += _reasoning_value(getattr(message, "reasoning_content", None))
        reasoning += _reasoning_value(extras.get("reasoning"))
        reasoning += _reasoning_value(extras.get("reasoning_content"))
        usage = response.usage
        return BackendResponse(
            content=message.content or "", model=response.model,
            input_tokens=int(getattr(usage, "prompt_tokens", 0) or 0),
            output_tokens=int(getattr(usage, "completion_tokens", 0) or 0),
            reasoning_present=bool(reasoning.strip()), reasoning_characters=len(reasoning),
            finish_reason=str(choice.finish_reason or ""), backend=self.name,
        )

    def list_models(self) -> List[str]:
        return [item.id for item in self.client.models.list().data]

    def close(self) -> None:
        self.client.close()


class OllamaBackend:
    name = "ollama"

    def __init__(self, base_url: str, timeout: float, workers: int):
        root = re.sub(r"/v1/?$", "", base_url.rstrip("/"))
        self.url = root + "/api/chat"
        limits = httpx.Limits(max_connections=max(2, workers * 2), max_keepalive_connections=max(2, workers))
        self.client = httpx.Client(timeout=httpx.Timeout(timeout), limits=limits)

    def chat(self, model: str, messages: List[Dict[str, str]], temperature: float) -> BackendResponse:
        response = self.client.post(self.url, json={
            "model": model, "messages": messages, "think": False,
            "keep_alive": -1, "stream": False,
            "options": {"temperature": temperature, "num_ctx": 16384},
        })
        response.raise_for_status()
        data = response.json()
        message = data.get("message") or {}
        reasoning = _reasoning_value(message.get("thinking")) + _reasoning_value(message.get("reasoning"))
        return BackendResponse(
            content=str(message.get("content") or ""), model=str(data.get("model") or model),
            input_tokens=int(data.get("prompt_eval_count") or 0),
            output_tokens=int(data.get("eval_count") or 0),
            reasoning_present=bool(reasoning.strip()), reasoning_characters=len(reasoning),
            finish_reason=str(data.get("done_reason") or ("stop" if data.get("done") else "")),
            backend=self.name,
        )

    def close(self) -> None:
        self.client.close()


def create_backend(name: str, base_url: str, api_key: str, timeout: float, workers: int):
    if name == "openai":
        return OpenAIBackend(base_url, api_key, timeout, workers)
    if name == "ollama":
        return OllamaBackend(base_url, timeout, workers)
    raise ValueError(f"未知后端: {name}")


def resolve_backend(
    requested: str, base_url: str, api_key: str, model: str, timeout: float, workers: int,
) -> Tuple[object, List[Dict[str, object]]]:
    probe_message = [{"role": "user", "content": "Reply with exactly: OK"}]
    names = [requested] if requested != "auto" else ["openai", "ollama"]
    probes: List[Dict[str, object]] = []
    last_error: Optional[Exception] = None
    for name in names:
        backend = create_backend(name, base_url, api_key, timeout, workers)
        started = time.monotonic()
        try:
            result = backend.chat(model, probe_message, 0.1)
            probe = {
                "backend": name, "ok": bool(result.content.strip()),
                "actual_model": result.model, "reasoning_present": result.reasoning_present,
                "reasoning_characters": result.reasoning_characters,
                "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
                "elapsed_seconds": round(time.monotonic() - started, 3),
            }
            probes.append(probe)
            if result.content.strip() and not result.reasoning_present:
                return backend, probes
            backend.close()
        except Exception as exc:
            last_error = exc
            probes.append({
                "backend": name, "ok": False, "reasoning_present": None,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "error_type": type(exc).__name__, "error": str(exc)[:500],
            })
            backend.close()
    if last_error:
        raise RuntimeError(f"无可用翻译后端: {last_error}")
    raise RuntimeError("后端仍产生 reasoning，无法安全用于翻译")


def check_api(
    base_url: str, api_key: str, model: str, timeout: float,
    log_path: Optional[Path] = None, backend_name: str = "auto",
) -> Dict[str, object]:
    started = time.monotonic()
    try:
        backend, probes = resolve_backend(backend_name, base_url, api_key, model, timeout, 1)
        actual = str(probes[-1].get("actual_model") or model)
        selected = str(probes[-1]["backend"])
        listed_models: List[str] = []
        if isinstance(backend, OpenAIBackend):
            try:
                listed_models = backend.list_models()
            except Exception as exc:
                _log_operation_error(log_path, "list-models", model, base_url, exc)
        backend.close()
        return {
            "ok": True, "requested_model": model, "actual_model": actual,
            "selected_backend": selected, "thinking_disabled": True,
            "probes": probes, "listed_models": listed_models,
            "elapsed_seconds": round(time.monotonic() - started, 3),
        }
    except Exception as exc:
        _log_operation_error(log_path, "check-api", model, base_url, exc)
        raise


def _log_operation_error(log_path: Optional[Path], operation: str, model: str, base_url: str, exc: Exception) -> None:
    if not log_path:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": utc_now(), "operation": operation, "requested_model": model,
        "base_url": base_url, "error_type": type(exc).__name__, "error": str(exc)[:1000],
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _validate_translation(source: str, translated: str) -> None:
    if len(translated.strip()) < 20:
        raise ValueError("模型返回内容过短")
    source_pages = PAGE_MARKER_RE.findall(source)
    output_pages = PAGE_MARKER_RE.findall(translated)
    if source_pages != output_pages:
        raise ValueError(f"页码标记不一致: source={source_pages}, output={output_pages}")
    if source.count("```") != translated.count("```"):
        raise ValueError("代码块围栏数量不一致")
    source_headings = re.findall(r"^(#{1,6})\s", source, re.M)
    output_headings = re.findall(r"^(#{1,6})\s", translated, re.M)
    if source_headings != output_headings:
        raise ValueError("标题数量或层级不一致")
    source_images = re.findall(r"!\[[^]]*\]\(([^)]+)\)", source)
    output_images = re.findall(r"!\[[^]]*\]\(([^)]+)\)", translated)
    if source_images != output_images:
        raise ValueError("图片引用不一致")
    for marker in re.findall(r"\[原文提取异常，第\d+页\]", source):
        if marker not in translated:
            raise ValueError("译文丢失了原文提取异常标记")


_LOG_LOCK = threading.Lock()


def _log_error(log_path: Path, chunk: Chunk, attempt: int, elapsed: float, exc: Exception) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    status_code = getattr(exc, "status_code", None)
    if status_code is None and isinstance(exc, httpx.HTTPStatusError):
        status_code = exc.response.status_code
    record = {
        "timestamp": utc_now(), "chunk_id": chunk.chunk_id, "hash": chunk.source_hash,
        "pages": chunk.pages, "attempt": attempt, "elapsed_seconds": round(elapsed, 3),
        "status_code": status_code, "error_type": type(exc).__name__, "error": str(exc)[:1000],
    }
    with _LOG_LOCK, log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _messages(glossary: str, source: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": glossary + "\n\nSOURCE MARKDOWN:\n" + source},
    ]


def _combine_responses(responses: List[BackendResponse], content: str) -> BackendResponse:
    last = responses[-1]
    return BackendResponse(
        content=content, model=last.model,
        input_tokens=sum(item.input_tokens for item in responses),
        output_tokens=sum(item.output_tokens for item in responses),
        reasoning_present=any(item.reasoning_present for item in responses),
        reasoning_characters=sum(item.reasoning_characters for item in responses),
        finish_reason=last.finish_reason, backend=last.backend,
        requests=sum(item.requests for item in responses),
        splits=sum(item.splits for item in responses),
    )


def _translate_with_auto_split(
    backend: object, model: str, glossary: str, source: str,
    temperature: float, current_max: int,
) -> BackendResponse:
    response = backend.chat(model, _messages(glossary, source), temperature)
    if response.reasoning_present:
        raise RuntimeError(f"后端 {response.backend} 仍返回 reasoning")
    if response.finish_reason.lower() not in {"length", "max_tokens"}:
        translated = response.content.strip() + "\n"
        _validate_translation(source, translated)
        response.content = translated
        return response
    if len(source) <= 2500:
        raise LengthTruncatedError("小块仍因 length 截断")
    next_max = max(2000, min(current_max // 2, int(len(source) * 0.6)))
    pieces = split_chunk_text(source, next_max)
    responses = [response]
    outputs: List[str] = []
    for piece, marker_injected in pieces:
        child = _translate_with_auto_split(backend, model, glossary, piece, temperature, next_max)
        child.splits += 1
        translated = child.content.strip()
        if marker_injected:
            translated = re.sub(r"^\s*<!--\s*page:\s*\d+\s*-->\s*", "", translated, count=1)
        outputs.append(translated)
        responses.append(child)
    combined = "\n\n".join(outputs).strip() + "\n"
    _validate_translation(source, combined)
    return _combine_responses(responses, combined)


def _translate_one(
    chunk: Chunk, progress: ProgressStore, backend: object, model: str, glossary: str,
    log_path: Path, temperature: float, max_retries: int, chunk_max: int,
    stop_event: threading.Event,
) -> ChunkResult:
    started = time.monotonic()
    progress.set_status(chunk.chunk_id, "running", error=None)
    last_error: Optional[Exception] = None
    for retry in range(max_retries + 1):
        if stop_event.is_set():
            progress.set_status(chunk.chunk_id, "pending", error="interrupted")
            return ChunkResult(chunk.chunk_id, False, chunk.pages, time.monotonic() - started, error="interrupted")
        attempt = progress.increment(chunk.chunk_id, "attempts")
        if retry:
            progress.increment(chunk.chunk_id, "retries")
        try:
            response = _translate_with_auto_split(backend, model, glossary, chunk.text, temperature, chunk_max)
            elapsed = time.monotonic() - started
            output_path = Path(str(progress.snapshot()["chunks"][chunk.chunk_id]["output_file"]))
            atomic_write_text(output_path, response.content)
            progress.set_actual_model(response.model, response.backend)
            progress.set_status(
                chunk.chunk_id, "completed", elapsed_seconds=round(elapsed, 3), error=None,
                input_tokens=response.input_tokens, output_tokens=response.output_tokens,
                reasoning_present=response.reasoning_present, finish_reason=response.finish_reason,
                requests=response.requests, splits=response.splits,
            )
            return ChunkResult(
                chunk.chunk_id, True, chunk.pages, elapsed, attempts=retry + 1, retries=retry,
                input_tokens=response.input_tokens, output_tokens=response.output_tokens,
                requests=response.requests, splits=response.splits,
                reasoning_present=response.reasoning_present, finish_reason=response.finish_reason,
            )
        except Exception as exc:
            last_error = exc
            _log_error(log_path, chunk, attempt, time.monotonic() - started, exc)
            if retry < max_retries and not stop_event.is_set():
                progress.set_status(chunk.chunk_id, "retrying", error=str(exc)[:500])
                stop_event.wait(min(2 ** retry, 30))
    elapsed = time.monotonic() - started
    progress.set_status(chunk.chunk_id, "failed", elapsed_seconds=round(elapsed, 3), error=str(last_error)[:500])
    return ChunkResult(
        chunk.chunk_id, False, chunk.pages, elapsed, attempts=max_retries + 1,
        retries=max_retries, error=str(last_error)[:500] if last_error else "unknown error",
    )


def _format_progress(completed: int, total: int, rate: float, summary: TranslationSummary) -> str:
    percent = (completed / total * 100) if total else 0.0
    remaining = max(0, total - completed)
    eta = datetime.now() + timedelta(seconds=(remaining / rate if rate > 0 else 0))
    return (
        f"[progress] {completed}/{total} pages ({percent:.1f}%), "
        f"recent {rate * 60:.2f} pages/min, ETA {eta:%Y-%m-%d %H:%M}, "
        f"success={summary.completed} failed={summary.failed} retries={summary.retries}"
    )


def translate_chunks(
    chunks: Iterable[Chunk], progress: ProgressStore, base_url: str, api_key: str, model: str,
    glossary_path: Path, log_path: Path, timeout: float = 600, temperature: float = 0.1,
    max_retries: int = 3, workers: int = 1, backend_name: str = "auto",
    chunk_max: int = 8000, total_pages: Optional[int] = None,
    progress_every: int = 0, backend: Optional[object] = None,
) -> TranslationSummary:
    if workers not in {1, 2, 4}:
        raise ValueError("--workers 只支持 1、2、4")
    chunks = sorted(chunks, key=lambda item: (item.chapter_number, min(item.pages or [10**9]), item.sequence))
    state = progress.snapshot().get("chunks", {})
    chunks = [
        chunk for chunk in chunks
        if state.get(chunk.chunk_id, {}).get("status") in {"pending", "failed"}
    ]
    if not chunks:
        snapshot = progress.snapshot()
        return TranslationSummary(
            backend=str(snapshot.get("backend") or backend_name),
            actual_model=str(snapshot.get("actual_model") or model),
        )
    glossary = glossary_prompt(load_glossary(glossary_path))
    owned_backend = backend is None
    probes: List[Dict[str, object]] = []
    if backend is None:
        backend, probes = resolve_backend(backend_name, base_url, api_key, model, timeout, workers)
    summary = TranslationSummary(backend=str(getattr(backend, "name", backend_name)))
    stop_event = threading.Event()
    started = time.monotonic()
    tracked_pages = set(range(1, total_pages + 1)) if total_pages else {page for chunk in chunks for page in chunk.pages}
    initial_pages = len(progress.completed_pages() & tracked_pages)
    last_report_pages = initial_pages
    last_report_time = started
    progress.set_current_run({
        "started_at": utc_now(), "workers": workers, "backend": summary.backend,
        "chunk_max": chunk_max, "initial_completed_pages": initial_pages,
        "total_pages": total_pages or len(tracked_pages), "probes": probes,
    })

    iterator = iter(chunks)
    futures: Dict[Future, Chunk] = {}
    executor = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="translator")

    def submit_one() -> bool:
        try:
            chunk = next(iterator)
        except StopIteration:
            return False
        future = executor.submit(
            _translate_one, chunk, progress, backend, model, glossary, log_path,
            temperature, max_retries, chunk_max, stop_event,
        )
        futures[future] = chunk
        return True

    try:
        for _ in range(min(len(chunks), workers * 2)):
            submit_one()
        while futures:
            done, _ = wait(futures, return_when=FIRST_COMPLETED)
            for future in done:
                futures.pop(future)
                result = future.result()
                summary.chunk_results.append(result)
                summary.completed += int(result.success)
                summary.failed += int(not result.success)
                summary.retries += result.retries
                summary.attempts += result.attempts
                summary.requests += result.requests
                summary.splits += result.splits
                summary.input_tokens += result.input_tokens
                summary.output_tokens += result.output_tokens
                summary.reasoning_present |= result.reasoning_present
                now = time.monotonic()
                completed_pages = len(progress.completed_pages() & tracked_pages)
                if progress_every and completed_pages - last_report_pages >= progress_every:
                    rate = (completed_pages - last_report_pages) / max(now - last_report_time, 0.001)
                    print(_format_progress(completed_pages, len(tracked_pages), rate, summary), flush=True)
                    last_report_pages, last_report_time = completed_pages, now
                submit_one()
    except KeyboardInterrupt:
        stop_event.set()
        for future in futures:
            future.cancel()
        raise
    finally:
        executor.shutdown(wait=True, cancel_futures=True)
        if owned_backend:
            backend.close()

    summary.wall_seconds = round(time.monotonic() - started, 3)
    snapshot = progress.snapshot()
    summary.actual_model = str(snapshot.get("actual_model") or model)
    final_pages = len(progress.completed_pages() & tracked_pages)
    progress.add_run({
        "started_at": snapshot.get("current_run", {}).get("started_at", utc_now()),
        "finished_at": utc_now(), "workers": workers, "backend": summary.backend,
        "chunk_max": chunk_max, "initial_completed_pages": initial_pages,
        "final_completed_pages": final_pages, "pages_completed": max(0, final_pages - initial_pages),
        "wall_seconds": summary.wall_seconds, "completed_chunks": summary.completed,
        "failed_chunks": summary.failed, "retries": summary.retries,
        "input_tokens": summary.input_tokens, "output_tokens": summary.output_tokens,
    })
    return summary
