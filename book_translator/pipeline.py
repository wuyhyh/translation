from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
from typing import Dict, Iterable, List, Set

import yaml

from .chunker import Chunk
from .progress import ProgressStore
from .util import atomic_write_text


def _normalize_glossary_first_uses(text: str, terms: Dict[str, str], seen: Set[str]) -> str:
    """Apply first-use terminology outside fenced code blocks."""
    sections = re.split(r"(```[\s\S]*?```)", text)
    for source, target in terms.items():
        source = str(source)
        target = str(target)
        decorated = re.compile(
            re.escape(target) + r"\s*[（(]\s*" + re.escape(source) + r"\s*[）)]",
            re.I,
        )
        for index in range(0, len(sections), 2):
            sections[index] = decorated.sub(target, sections[index])
        if source in seen:
            continue
        for index in range(0, len(sections), 2):
            if target in sections[index]:
                sections[index] = sections[index].replace(target, f"{target}（{source}）", 1)
                seen.add(source)
                break
    return "".join(sections)


def _deduplicate_page_markers(text: str) -> str:
    seen: Set[str] = set()

    def keep_first(match: re.Match) -> str:
        page = match.group(1)
        if page in seen:
            return ""
        seen.add(page)
        # Model output may preserve the marker semantically while changing its
        # whitespace (for example ``<!-- page:219 -->``). Emit one canonical
        # spelling so downstream completeness checks are unambiguous.
        return f"<!-- page: {page} -->"

    text = re.sub(r"<!--\s*page:\s*(\d+)\s*-->", keep_first, text)
    return re.sub(r"\n{3,}", "\n\n", text)


def rebuild_chapter_files(progress: ProgressStore, output_dir: Path, glossary_path: Path | None = None) -> List[Path]:
    grouped = defaultdict(list)
    for chunk_id, item in progress.data.get("chunks", {}).items():
        if item.get("status") == "completed" and Path(str(item["output_file"])).exists():
            grouped[str(item["chapter_file"])].append((
                min(item.get("pages") or [10**9]), int(item.get("sequence", 0)), chunk_id, item,
            ))
    terms: Dict[str, str] = {}
    if glossary_path and glossary_path.exists():
        glossary = yaml.safe_load(glossary_path.read_text(encoding="utf-8")) or {}
        terms = {str(key): str(value) for key, value in glossary.get("terms", {}).items()}
    seen: Set[str] = set()
    written: List[Path] = []
    ordered_groups = sorted(
        grouped.items(),
        key=lambda row: min(int(item[3].get("chapter_number", 10**9)) for item in row[1]),
    )
    for filename, items in ordered_groups:
        items.sort(key=lambda row: (row[0], row[1]))
        content = []
        for _, _, _, item in items:
            content.append(Path(str(item["output_file"])).read_text(encoding="utf-8").strip())
        chapter_text = "\n\n".join(content).rstrip() + "\n"
        chapter_text = _deduplicate_page_markers(chapter_text)
        chapter_text = _normalize_glossary_first_uses(chapter_text, terms, seen)
        path = output_dir / filename
        atomic_write_text(path, chapter_text)
        written.append(path)
    return sorted(written)


def merge_markdown(output_dir: Path, destination: Path) -> List[Path]:
    files = sorted(path for path in output_dir.glob("[0-9][0-9]-*.md") if path.resolve() != destination.resolve())
    if not files:
        raise FileNotFoundError(f"在 {output_dir} 中没有章节 Markdown")
    combined = []
    for path in files:
        combined.append(f"<!-- source-file: {path.name} -->\n\n{path.read_text(encoding='utf-8').strip()}")
    # Enforce the invariant once more across chapter boundaries. This makes the
    # final artifact independent of when individual chapter files were built.
    merged_text = _deduplicate_page_markers("\n\n".join(combined) + "\n")
    atomic_write_text(destination, merged_text)
    return files
