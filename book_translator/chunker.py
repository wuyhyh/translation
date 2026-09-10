from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from .util import sha256_text


PAGE_MARKER_RE = re.compile(r"<!--\s*page:\s*(\d+)\s*-->")


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_hash: str
    text: str
    pages: List[int]
    chapter_number: int
    chapter_title: str
    chapter_file: str
    sequence: int = 0


def split_markdown_units(markdown: str) -> List[str]:
    """Split only at blank lines, keeping fenced code blocks atomic."""
    units: List[str] = []
    current: List[str] = []
    in_fence = False
    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not line.strip() and not in_fence:
            if current:
                units.append("\n".join(current).strip())
                current = []
        else:
            current.append(line)
    if current:
        units.append("\n".join(current).strip())
    return [unit for unit in units if unit]


def _page_numbers(text: str) -> List[int]:
    return [int(value) for value in PAGE_MARKER_RE.findall(text)]


def make_chunks(page_records: Sequence[Dict[str, object]], target_min: int = 4000, target_max: int = 7000) -> List[Chunk]:
    if target_min <= 0 or target_max < target_min:
        raise ValueError("分块长度参数无效")
    chunks: List[Chunk] = []
    grouped: Dict[str, List[Dict[str, object]]] = {}
    for record in page_records:
        chapter_file = str(record["chapter"]["filename"])
        grouped.setdefault(chapter_file, []).append(record)

    for chapter_file, records in grouped.items():
        records.sort(key=lambda item: int(item["page_number"]))
        chapter = records[0]["chapter"]
        units: List[str] = []
        for record in records:
            text = Path(str(record["file"])).read_text(encoding="utf-8")
            units.extend(split_markdown_units(text))
        current: List[str] = []
        current_len = 0
        active_page_marker = ""
        for unit in units:
            marker_match = PAGE_MARKER_RE.fullmatch(unit.strip())
            if marker_match:
                active_page_marker = unit.strip()
            projected = current_len + (2 if current else 0) + len(unit)
            heading_boundary = unit.startswith("#") and current_len >= target_min
            size_boundary = current and projected > target_max
            if heading_boundary or size_boundary:
                chunks.append(_build_chunk(current, chapter, len(chunks)))
                current, current_len = [], 0
                # A page may span multiple chunks. Every request must still carry
                # the physical page marker for the source that follows.
                if active_page_marker and not marker_match:
                    current.append(active_page_marker)
                    current_len = len(active_page_marker)
            current.append(unit)
            current_len += (2 if len(current) > 1 else 0) + len(unit)
        if current:
            chunks.append(_build_chunk(current, chapter, len(chunks)))
    return chunks


def _build_chunk(units: Iterable[str], chapter: Dict[str, object], sequence: int = 0) -> Chunk:
    text = "\n\n".join(units).strip() + "\n"
    digest = sha256_text(text)
    pages = sorted(set(_page_numbers(text)))
    return Chunk(
        chunk_id=digest[:16],
        source_hash=digest,
        text=text,
        pages=pages,
        chapter_number=int(chapter["number"]),
        chapter_title=str(chapter["title"]),
        chapter_file=str(chapter["filename"]),
        sequence=sequence,
    )


def split_chunk_text(text: str, maximum: int) -> List[tuple[str, bool]]:
    """Safely split an oversized request at Markdown unit boundaries.

    The boolean says that a page marker was injected for request integrity and
    must be removed before child outputs are joined.
    """
    if len(text) <= maximum:
        return [(text, False)]
    units = split_markdown_units(text)
    if len(units) < 2:
        raise ValueError("单个段落、代码块或表格超过可用上下文，无法安全切分")
    groups: List[List[str]] = []
    current: List[str] = []
    current_len = 0
    active_marker = ""
    injected_flags: List[bool] = []
    current_injected = False
    for unit in units:
        marker = PAGE_MARKER_RE.fullmatch(unit.strip())
        if marker:
            active_marker = unit.strip()
        projected = current_len + (2 if current else 0) + len(unit)
        if current and projected > maximum:
            groups.append(current)
            injected_flags.append(current_injected)
            current = []
            current_len = 0
            current_injected = bool(active_marker and not marker)
            if current_injected:
                current.append(active_marker)
                current_len = len(active_marker)
        current.append(unit)
        current_len += (2 if len(current) > 1 else 0) + len(unit)
    if current:
        groups.append(current)
        injected_flags.append(current_injected)
    return [("\n\n".join(group).strip() + "\n", injected_flags[index]) for index, group in enumerate(groups)]


def load_page_records(work_dir: Path, pages: Iterable[int] | None = None, chapter: str | None = None) -> List[Dict[str, object]]:
    manifest_path = work_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError("未找到 work/manifest.json，请先执行 extract")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    wanted_pages = set(pages) if pages is not None else None
    records: List[Dict[str, object]] = []
    chapter_query = chapter.strip().lower() if chapter else None
    for key, value in manifest.get("pages", {}).items():
        page_number = int(key)
        if wanted_pages is not None and page_number not in wanted_pages:
            continue
        chapter_data = value["chapter"]
        if chapter_query is not None:
            candidates = {
                str(chapter_data["number"]).lower(),
                str(chapter_data["title"]).lower(),
                str(chapter_data["filename"]).lower(),
                Path(str(chapter_data["filename"])).stem.lower(),
            }
            if chapter_query not in candidates and not any(chapter_query in item for item in candidates):
                continue
        records.append({**value, "page_number": page_number})
    records.sort(key=lambda item: int(item["page_number"]))
    if not records:
        target = f"章节 {chapter!r}" if chapter else "指定页码"
        raise ValueError(f"提取结果中没有{target}；请先提取对应页")
    if wanted_pages is not None:
        missing = wanted_pages - {int(record["page_number"]) for record in records}
        if missing:
            raise ValueError(f"这些页尚未提取: {sorted(missing)}")
    return records
