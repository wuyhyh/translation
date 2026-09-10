from __future__ import annotations

import html
import json
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple

from .chunker import PAGE_MARKER_RE, load_page_records, make_chunks
from .progress import ACTIVE_STATUSES, ProgressStore
from .repair import _code_blocks, _format_pages, split_pages
from .util import atomic_write_text, utc_now


IMAGE_RE = re.compile(r"!\[[^]]*\]\(([^)]+)\)")
URL_RE = re.compile(r"https?://[A-Za-z0-9:/?&%#._~+=-]+")
PATH_RE = re.compile(
    r"(?:[A-Za-z]:\\(?:[A-Za-z0-9_.-]+\\)*[A-Za-z0-9_.-]*[A-Za-z0-9_-]"
    r"|\.{1,2}/(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+"
    r"|(?<![A-Za-z0-9])/(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+"
    r"|(?<![A-Za-z0-9])/(?:boot|dev|etc|home|mnt|opt|proc|root|run|srv|sys|tmp|usr|var)(?![A-Za-z0-9_.-])"
    r"|(?:(?:Core|Drivers|Middlewares|USB_Device_Library|portable)/)(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+"
    r"|(?<![A-Za-z0-9_])[A-Za-z0-9_-]+\.(?:c|h|cpp|hpp|s|asm|ld|sh|exe|linux|zip|yaml|json|md|txt)(?![A-Za-z0-9_]))"
)
HEX_RE = re.compile(r"\b0x[0-9A-Fa-f]+\b")
REGISTER_RE = re.compile(r"(?<![A-Za-z0-9_])(?:R(?:1[0-5]|[0-9])|SP|LR|PC|xPSR|MSP|PSP|PRIMASK|BASEPRI|FAULTMASK|CONTROL|[A-Z]{2,12}\d?_[A-Z0-9_]+)(?![A-Za-z0-9_])")
MACRO_RE = re.compile(r"(?<![A-Za-z0-9_])[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+(?![A-Za-z0-9_])")
FUNCTION_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:(?:HAL|LL)_[A-Za-z0-9_]+|[A-Za-z_][A-Za-z0-9_]*_[A-Za-z0-9_]+"
    r"|[a-z]+[A-Z][A-Za-z0-9_]*|(?:printf|sprintf|snprintf|malloc|calloc|realloc|free|memcpy|memset))(?=\s*\()"
)
IDENTIFIER_EQUIVALENTS = {
    ("1d323e27d9522c68", "portable/GCC/ARM_CMO"): "portable/GCC/ARM_CM0",
    ("1d323e27d9522c68", "portmarco.h"): "portmacro.h",
    ("1d323e27d9522c68", "ARM_CMO"): "ARM_CM0",
    ("c0e024d8bbe95fb7", "UART_IRQ_Hanler"): "UART_IRQ_Handler",
}
LEAK_PATTERNS = re.compile(
    r"SOURCE MARKDOWN|Mandatory rules:|You are a professional translator|<think>|</think>|reasoning_content|Terminology \(English",
    re.I,
)


@dataclass
class AuditCheck:
    name: str
    passed: bool
    summary: str
    details: List[str]


def recover_missing_sources(progress: ProgressStore, work_dir: Path) -> List[str]:
    recovered = []
    snapshot = progress.snapshot()
    missing = {
        chunk_id: item for chunk_id, item in snapshot.get("chunks", {}).items()
        if item.get("status") in ACTIVE_STATUSES
        and not (item.get("source_file") and Path(str(item.get("source_file"))).is_file())
    }
    pages = sorted({int(page) for item in missing.values() for page in item.get("pages") or []})
    candidates = {}
    if pages:
        records = load_page_records(work_dir, pages=pages)
        for target_min, target_max in ((4000, 7000), (4800, 8000), (7200, 12000)):
            candidates.update({
                chunk.chunk_id: chunk
                for chunk in make_chunks(records, target_min=target_min, target_max=target_max)
            })
    for chunk_id, item in missing.items():
        match = candidates.get(chunk_id)
        if not match:
            continue
        path = work_dir / "chunks" / f"{chunk_id}.md"
        atomic_write_text(path, match.text)
        progress.set_status(chunk_id, str(item["status"]), source_file=str(path))
        recovered.append(chunk_id)
    return recovered


def _tokens(text: str, pattern: re.Pattern) -> Set[str]:
    return set(pattern.findall(text))


def _identifier_text(text: str) -> str:
    """Remove structures checked elsewhere and repair obvious PDF line-wrap artifacts."""
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = IMAGE_RE.sub("", text)
    text = re.sub(r"\bfunction(?=(?:HAL|LL)_)", "", text)
    text = re.sub(r"(?<=[A-Z_])-\s+(?=[A-Za-z0-9_])", "", text)
    return text


def _identifier_tokens(text: str, pattern: re.Pattern) -> Set[str]:
    values = _tokens(_identifier_text(text), pattern)
    if pattern is PATH_RE or pattern is URL_RE:
        return {value.rstrip(".,;:") for value in values}
    return values


def _hex_tokens(text: str) -> Set[str]:
    values = re.findall(r"\b0x[0-9A-Fa-f]+(?:\s+[0-9A-Fa-f]{2,8})*\b", _identifier_text(text))
    return {re.sub(r"\s+", "", value) for value in values}


def _function_source_tokens(text: str) -> Set[str]:
    return _identifier_tokens(text, FUNCTION_RE)


def _identifier_words(text: str) -> Set[str]:
    return set(re.findall(r"(?<![A-Za-z0-9_])[A-Za-z_][A-Za-z0-9_]*(?![A-Za-z0-9_])", _identifier_text(text)))


def _equivalent_identifier_present(chunk_id: str, token: str, translated: str) -> bool:
    replacement = IDENTIFIER_EQUIVALENTS.get((chunk_id, token))
    if not replacement:
        return False
    return bool(re.search(
        rf"(?<![A-Za-z0-9_]){re.escape(replacement)}(?![A-Za-z0-9_])",
        _identifier_text(translated),
    ))


def _long_english_paragraphs(text: str) -> List[str]:
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = IMAGE_RE.sub("", text)
    text = URL_RE.sub("", text)
    text = re.sub(r"`[^`\n]+`", "", text)
    findings = []
    for paragraph in re.split(r"\n\s*\n", text):
        words = re.findall(r"\b[A-Za-z]{2,}\b", paragraph)
        visible = re.sub(r"\s", "", paragraph)
        ascii_letters = len(re.findall(r"[A-Za-z]", visible))
        if len(words) >= 35 and visible and ascii_letters / len(visible) >= 0.65:
            findings.append(re.sub(r"\s+", " ", paragraph).strip()[:240])
    return findings


def _paragraph_occurrences(text: str) -> Dict[str, List[int]]:
    occurrences: Dict[str, List[int]] = defaultdict(list)
    for page, body in split_pages(text):
        body = re.sub(r"```[\s\S]*?```", "", body)
        for paragraph in re.split(r"\n\s*\n", body):
            normalized = re.sub(r"\s+", " ", paragraph).strip()
            if len(normalized) >= 160:
                occurrences[normalized].append(page)
    return occurrences


def _duplicate_paragraphs(source: str, translated: str) -> List[str]:
    source_repeats = Counter(
        tuple(pages) for pages in _paragraph_occurrences(source).values() if len(pages) > 1
    )
    findings = []
    for paragraph, pages in _paragraph_occurrences(translated).items():
        if len(pages) <= 1:
            continue
        key = tuple(pages)
        if source_repeats[key]:
            source_repeats[key] -= 1
        else:
            findings.append(paragraph[:180])
    return findings


def _translation_weight(text: str) -> int:
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = IMAGE_RE.sub("", text)
    text = PAGE_MARKER_RE.sub("", text)
    return len(re.findall(r"[A-Za-z]", text)) + 3 * len(re.findall(r"[\u3400-\u9fff]", text))


def _source_weight(text: str) -> int:
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = IMAGE_RE.sub("", text)
    text = PAGE_MARKER_RE.sub("", text)
    return len(re.findall(r"[A-Za-z]", text))


CODE_BLOCK_RE = re.compile(r"```[^\n]*\n[\s\S]*?```")


def restore_exact_code_blocks(progress: ProgressStore) -> Dict[str, object]:
    """Deterministically restore fenced blocks from source without model calls."""
    changed: List[str] = []
    unresolved: List[str] = []
    for chunk_id, item in progress.snapshot().get("chunks", {}).items():
        if item.get("status") != "completed":
            continue
        source_path = Path(str(item.get("source_file") or ""))
        output_path = Path(str(item.get("output_file") or ""))
        if not source_path.is_file() or not output_path.is_file():
            continue
        source = source_path.read_text(encoding="utf-8")
        translated = output_path.read_text(encoding="utf-8")
        source_blocks = list(CODE_BLOCK_RE.finditer(source))
        output_blocks = list(CODE_BLOCK_RE.finditer(translated))
        if [match.group(0) for match in source_blocks] == [match.group(0) for match in output_blocks]:
            continue
        if len(source_blocks) != len(output_blocks):
            unresolved.append(chunk_id)
            continue
        pieces: List[str] = []
        position = 0
        for source_match, output_match in zip(source_blocks, output_blocks):
            pieces.append(translated[position:output_match.start()])
            pieces.append(source_match.group(0))
            position = output_match.end()
        pieces.append(translated[position:])
        atomic_write_text(output_path, "".join(pieces))
        progress.set_status(
            chunk_id, "completed", code_blocks_restored=len(source_blocks),
            code_integrity_repaired_at=utc_now(),
        )
        changed.append(chunk_id)
    return {"changed": changed, "changed_count": len(changed), "unresolved": unresolved}


def audit_project(
    progress: ProgressStore, work_dir: Path, output_dir: Path,
    total_pages: int, destination: Path,
) -> Dict[str, object]:
    data = progress.snapshot()
    active = {key: item for key, item in data.get("chunks", {}).items() if item.get("status") in ACTIVE_STATUSES}
    checks: List[AuditCheck] = []
    missing_sources = []
    missing_outputs = []
    final_failed = []
    marker_issues = []
    heading_issues = []
    image_issues = []
    fence_issues = []
    code_issues = []
    identifier_issues = []
    leak_issues = []
    duplicate_issues = []
    truncation_issues = []
    english_issues = []
    anomaly_markers = []

    for chunk_id, item in active.items():
        source_path = Path(str(item.get("source_file") or ""))
        output_path = Path(str(item.get("output_file") or ""))
        if not source_path.is_file():
            missing_sources.append(chunk_id)
            continue
        if item.get("status") != "completed" or not output_path.is_file():
            if item.get("status") == "failed":
                final_failed.append(chunk_id)
            if not output_path.is_file():
                missing_outputs.append(chunk_id)
            continue
        source = source_path.read_text(encoding="utf-8")
        translated = output_path.read_text(encoding="utf-8")
        if PAGE_MARKER_RE.findall(source) != PAGE_MARKER_RE.findall(translated):
            marker_issues.append(chunk_id)
        source_headings = re.findall(r"^(#{1,6})\s", source, re.M)
        output_headings = re.findall(r"^(#{1,6})\s", translated, re.M)
        if source_headings != output_headings:
            heading_issues.append(chunk_id)
        source_images = IMAGE_RE.findall(source)
        output_images = IMAGE_RE.findall(translated)
        missing_image_files = [ref for ref in source_images if not (output_dir / ref).resolve().is_file()]
        if source_images != output_images or missing_image_files:
            image_issues.append(f"{chunk_id}: refs={source_images != output_images}, missing={missing_image_files}")
        if source.count("```") % 2 or translated.count("```") % 2 or source.count("```") != translated.count("```"):
            fence_issues.append(chunk_id)
        if _code_blocks(source) != _code_blocks(translated):
            code_issues.append(chunk_id)
        for label, pattern in (
            ("URL", URL_RE), ("path", PATH_RE), ("hex", HEX_RE),
            ("register", REGISTER_RE), ("macro", MACRO_RE), ("function", FUNCTION_RE),
        ):
            if label == "hex":
                missing = sorted(_hex_tokens(source) - _hex_tokens(translated))
            elif label == "function":
                missing = sorted(_function_source_tokens(source) - _identifier_words(translated))
            else:
                missing = sorted(_identifier_tokens(source, pattern) - _identifier_tokens(translated, pattern))
            missing = [
                token for token in missing
                if not _equivalent_identifier_present(chunk_id, token, translated)
            ]
            if missing:
                identifier_issues.append(f"{chunk_id} {label}: {', '.join(missing[:20])}")
        if item.get("reasoning_present") or LEAK_PATTERNS.search(translated):
            leak_issues.append(chunk_id)
        duplicates = _duplicate_paragraphs(source, translated)
        if duplicates:
            duplicate_issues.append(f"{chunk_id}: {duplicates[0]}")
        source_visible = _source_weight(source)
        output_visible = _translation_weight(translated)
        if str(item.get("finish_reason", "")).lower() in {"length", "max_tokens"} or (source_visible > 200 and output_visible < source_visible * 0.28):
            truncation_issues.append(chunk_id)
        if not re.search(r"reference|bibliograph|index|contents", str(item.get("chapter_title", "")), re.I):
            for finding in _long_english_paragraphs(translated):
                english_issues.append(f"{chunk_id}: {finding}")
        anomaly_markers.extend(
            f"{chunk_id}: {marker}" for marker in re.findall(r"\[原文提取异常，第\d+页\]", source)
        )

    registered = progress.registered_pages()
    missing_pages = sorted(set(range(1, total_pages + 1)) - registered)
    manifest = json.loads((work_dir / "manifest.json").read_text(encoding="utf-8"))
    blank_pages = sorted(
        int(page) for page, item in manifest.get("pages", {}).items()
        if int(item.get("characters", 0)) < 20
    )
    checks.extend([
        AuditCheck("All source chunks have successful translations", not missing_sources and not missing_outputs, f"sources={len(active) - len(missing_sources)}/{len(active)}, outputs={len(active) - len(missing_outputs)}/{len(active)}", missing_sources + missing_outputs),
        AuditCheck("Final failed count is zero", not final_failed, f"failed={len(final_failed)}", final_failed),
        AuditCheck("Physical page coverage", not missing_pages and registered == set(range(1, total_pages + 1)), f"covered={len(registered)}/{total_pages}; explicit blank/anomaly pages={len(blank_pages)}", [f"missing pages: {_format_pages(missing_pages)}"] if missing_pages else []),
        AuditCheck("Page marker order", not marker_issues, f"issues={len(marker_issues)}", marker_issues),
        AuditCheck("Markdown heading count and levels", not heading_issues, f"issues={len(heading_issues)}", heading_issues),
        AuditCheck("Image references and files", not image_issues, f"issues={len(image_issues)}", image_issues),
        AuditCheck("Code fences paired", not fence_issues, f"issues={len(fence_issues)}", fence_issues),
        AuditCheck("Code block contents exact", not code_issues, f"issues={len(code_issues)}", code_issues),
        AuditCheck("Technical identifiers preserved", not identifier_issues, f"issues={len(identifier_issues)}", identifier_issues),
        AuditCheck("No reasoning or prompt leakage", not leak_issues, f"issues={len(leak_issues)}", leak_issues),
        AuditCheck("No abnormal duplicate paragraphs", not duplicate_issues, f"issues={len(duplicate_issues)}", duplicate_issues),
        AuditCheck("No obvious truncation", not truncation_issues, f"issues={len(truncation_issues)}", truncation_issues),
        AuditCheck("Extraction anomaly markers inventoried", True, f"markers={len(anomaly_markers)}", anomaly_markers),
        AuditCheck("No long untranslated English body", not english_issues, f"issues={len(english_issues)}", english_issues),
    ])
    passed = all(check.passed for check in checks)
    lines = [
        "# Translation integrity audit", "",
        f"- Generated: {utc_now()}", f"- Overall: **{'PASS' if passed else 'FAIL'}**",
        f"- Active chunks: {len(active)}", f"- Physical pages: {total_pages}", "",
        "| Check | Result | Summary |", "|---|---|---|",
    ]
    for check in checks:
        lines.append(f"| {check.name} | {'PASS' if check.passed else 'FAIL'} | {check.summary} |")
    lines.extend(["", "## Details", ""])
    for check in checks:
        lines.append(f"### {check.name}")
        lines.append("")
        if check.details:
            lines.extend(f"- {detail}" for detail in check.details)
        else:
            lines.append("- No issues found.")
        lines.append("")
    atomic_write_text(destination, "\n".join(lines).rstrip() + "\n")
    return {
        "passed": passed, "checks": [
            {"name": check.name, "passed": check.passed, "summary": check.summary}
            for check in checks
        ], "report": str(destination), "blank_pages": blank_pages,
    }


def _page_map(progress: ProgressStore, use_source: bool) -> Dict[int, str]:
    data = progress.snapshot()
    rows = sorted(
        (
            int(item.get("chapter_number", 0)), min(item.get("pages") or [10**9]),
            int(item.get("sequence", 0)), chunk_id, item,
        )
        for chunk_id, item in data.get("chunks", {}).items() if item.get("status") == "completed"
    )
    pages: Dict[int, List[str]] = defaultdict(list)
    key = "source_file" if use_source else "output_file"
    for _, _, _, _, item in rows:
        path = Path(str(item.get(key) or ""))
        if not path.is_file():
            continue
        for page, body in split_pages(path.read_text(encoding="utf-8")):
            if body.strip():
                pages[page].append(body.strip())
    return {page: "\n\n".join(parts) for page, parts in pages.items()}


def _focus_items(source: str) -> str:
    numbers = sorted(set(re.findall(r"\b(?:0x[0-9A-Fa-f]+|\d+(?:\.\d+)?(?:%|kHz|MHz|GHz|ms|us|ns|V|mA)?)\b", source)))
    negatives = sorted(set(re.findall(r"\b(?:not|no|never|unless|without|disable[ds]?|cannot)\b", source, re.I)))
    conditions = sorted(set(re.findall(r"\b(?:if|when|unless|otherwise|only if|as long as)\b", source, re.I)))
    identifiers = sorted(_tokens(source, REGISTER_RE) | _tokens(source, MACRO_RE) | _tokens(source, FUNCTION_RE))
    return "; ".join([
        "numbers=" + ", ".join(numbers[:25]), "negation=" + ", ".join(negatives[:15]),
        "conditions=" + ", ".join(conditions[:15]), "identifiers=" + ", ".join(identifiers[:35]),
    ])


def generate_semantic_samples(
    progress: ProgressStore, work_dir: Path, repaired_pages: Iterable[int],
    destination: Path, seed: int = 20260909,
) -> Dict[str, object]:
    manifest = json.loads((work_dir / "manifest.json").read_text(encoding="utf-8"))
    source_pages = _page_map(progress, True)
    translated_pages = _page_map(progress, False)
    rng = random.Random(seed)
    selected: Set[int] = set(int(page) for page in repaired_pages)
    per_chapter: Dict[int, List[int]] = defaultdict(list)
    for page_text, item in manifest.get("pages", {}).items():
        page = int(page_text)
        chapter = int(item.get("chapter", {}).get("number", 0))
        body = source_pages.get(page, "")
        if 1 <= chapter <= 28 and len(body) >= 300 and "[原文提取异常" not in body:
            per_chapter[chapter].append(page)
    for chapter in range(1, 29):
        candidates = per_chapter.get(chapter, [])
        if candidates:
            selected.update(rng.sample(candidates, min(2, len(candidates))))
    priority_terms = ("interrupt", "DMA", "clock tree", "Flash", "bootloader", "FreeRTOS", "SEGGER")
    priority_pages = []
    for term in priority_terms:
        candidates = [page for page, body in source_pages.items() if term.lower() in body.lower()]
        if candidates:
            choice = rng.choice(sorted(candidates))
            selected.add(choice)
            priority_pages.append(choice)
    rows = []
    for page in sorted(selected):
        source = source_pages.get(page, "")
        translated = translated_pages.get(page, "")
        chapter_data = manifest.get("pages", {}).get(str(page), {}).get("chapter", {})
        rows.append((page, chapter_data, source, translated))
    lines = [
        "# Semantic review samples", "",
        "This is a deterministic sampling artifact for human review. It does not ask the translation model to judge its own correctness.",
        f"Seed: `{seed}`. Samples: **{len(rows)}**. Repaired pages included: **{len(set(repaired_pages))}**.",
        f"Priority pages: `{', '.join(map(str, sorted(set(priority_pages))))}`.", "",
    ]
    for page, chapter, source, translated in rows:
        title = str(chapter.get("title", "Front Matter"))
        number = int(chapter.get("number", 0))
        lines.extend([
            f"## PDF page {page} — Chapter {number}: {title}", "",
            f"Focus: `{html.escape(_focus_items(source))}`", "",
            "<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>",
            f"<td><pre>{html.escape(source)}</pre></td>",
            f"<td><pre>{html.escape(translated)}</pre></td>",
            "</tr></tbody></table>", "",
        ])
    destination.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(destination, "\n".join(lines).rstrip() + "\n")
    return {"samples": len(rows), "pages": [row[0] for row in rows], "report": str(destination)}
