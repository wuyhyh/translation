from __future__ import annotations

import re
import statistics
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import fitz

from .util import atomic_write_json, atomic_write_text, slugify, utc_now


ANOMALY_TEMPLATE = "[原文提取异常，第{page}页]"


@dataclass(frozen=True)
class Chapter:
    number: int
    title: str
    start_page: int
    filename: str


def _sample_indices(page_count: int, maximum: int = 24) -> List[int]:
    if page_count <= maximum:
        return list(range(page_count))
    return sorted({round(i * (page_count - 1) / (maximum - 1)) for i in range(maximum)})


def inspect_pdf(pdf_path: Path) -> Dict[str, object]:
    """Classify a PDF using text from pages spread throughout the document."""
    with fitz.open(pdf_path) as doc:
        counts = [len(doc[index].get_text("text").strip()) for index in _sample_indices(doc.page_count)]
        readable = sum(count >= 80 for count in counts)
        ratio = readable / len(counts) if counts else 0.0
        median = statistics.median(counts) if counts else 0
        text_pdf = ratio >= 0.5 and median >= 80
        return {
            "pdf": str(pdf_path),
            "page_count": doc.page_count,
            "sampled_pages": len(counts),
            "readable_sample_pages": readable,
            "readable_ratio": round(ratio, 3),
            "median_text_characters": int(median),
            "pdf_type": "text" if text_pdf else "scanned",
            "needs_ocr": not text_pdf,
        }


def _chapter_filename(number: int, title: str) -> str:
    clean_title = re.sub(r"^\s*\d+[.:]?\s*", "", title).strip()
    return f"{number:02d}-{slugify(clean_title)}.md"


def chapters_from_toc(doc: fitz.Document) -> List[Chapter]:
    chapters: List[Chapter] = []
    seen = set()
    in_numbered_part = False
    inferred_number = 0
    for level, title, page in doc.get_toc(simple=True):
        if level == 1:
            # This book's bookmarks omit chapter numbers. Its numbered chapters
            # are level-2 children of level-1 Roman-numeral Part entries.
            in_numbered_part = bool(re.match(r"^\s*[IVXLCDM]+\s+\S", title, re.I))
        match = re.match(r"^\s*(\d+)[.:]?\s+(.+?)\s*$", title)
        if match:
            number = int(match.group(1))
            clean = match.group(2).strip()
        elif in_numbered_part and level == 2:
            inferred_number += 1
            number = inferred_number
            clean = title.strip()
        else:
            continue
        if number in seen or not (1 <= number <= 999):
            continue
        chapters.append(Chapter(number, clean, int(page), _chapter_filename(number, clean)))
        seen.add(number)
    chapters.sort(key=lambda chapter: chapter.start_page)
    return chapters


def chapter_for_page(page_number: int, chapters: Sequence[Chapter]) -> Dict[str, object]:
    selected: Optional[Chapter] = None
    for chapter in chapters:
        if chapter.start_page <= page_number:
            selected = chapter
        else:
            break
    if selected is None:
        return {"number": 0, "title": "Front Matter", "filename": "00-front-matter.md"}
    return asdict(selected)


def _body_font_size(page_dict: Dict[str, object]) -> float:
    weighted: List[float] = []
    for block in page_dict.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "").strip()
                if text:
                    weighted.extend([float(span.get("size", 10.0))] * min(len(text), 80))
    return statistics.median(weighted) if weighted else 10.0


def _text_block_to_markdown(block: Dict[str, object], body_size: float) -> str:
    lines: List[str] = []
    sizes: List[float] = []
    mono_chars = 0
    total_chars = 0
    for line in block.get("lines", []):
        spans = line.get("spans", [])
        line_text = "".join(str(span.get("text", "")) for span in spans).rstrip()
        if line_text.strip():
            lines.append(line_text.strip())
        for span in spans:
            if span.get("text", "").strip():
                span_text = str(span.get("text", ""))
                total_chars += len(span_text)
                if re.search(r"anonymous|mono|courier|consol", str(span.get("font", "")), re.I):
                    mono_chars += len(span_text)
                sizes.append(float(span.get("size", body_size)))
    if not lines:
        return ""
    raw = "\n".join(lines)
    is_code = total_chars >= 3 and (mono_chars / total_chars > 0.45 or _looks_like_code(lines))
    if is_code:
        return f"```text\n{raw}\n```"

    text = _join_wrapped_lines(lines)
    number_match = re.match(r"^(\d+(?:\.\d+){0,5})\s+\S", text)
    max_size = max(sizes) if sizes else body_size
    if number_match:
        level = min(number_match.group(1).count(".") + 1, 6)
        return f"{'#' * level} {text}"
    if max_size >= body_size * 1.6:
        return f"# {text}"
    if max_size >= body_size * 1.3:
        return f"## {text}"
    if max_size >= body_size * 1.15 and len(text) < 180:
        return f"### {text}"
    return text


def _looks_like_code(lines: Sequence[str]) -> bool:
    if len(lines) < 2:
        return False
    joined = "\n".join(lines)
    signals = sum(token in joined for token in ("#include", ";", "{", "}", "->", "//", "/*", " */", "();"))
    return signals >= 2


def _join_wrapped_lines(lines: Sequence[str]) -> str:
    if any(line.lstrip().startswith(("•", "●")) for line in lines):
        bullets: List[str] = []
        current = ""
        for line in lines:
            clean = re.sub(r"\s+", " ", line).strip()
            if clean.startswith(("•", "●")):
                if current:
                    bullets.append("- " + current)
                current = clean[1:].strip()
            elif current:
                current += " " + clean
            else:
                current = clean
        if current:
            bullets.append("- " + current)
        return "\n".join(bullets)
    result = ""
    for line in lines:
        clean = re.sub(r"\s+", " ", line).strip()
        if not result:
            result = clean
        elif result.endswith("-") and clean and clean[0].islower():
            result = result[:-1] + clean
        else:
            result += " " + clean
    return result


def _page_markdown(page: fitz.Page, page_number: int, images_dir: Path) -> Tuple[str, List[str], int]:
    page_dict = page.get_text("dict", sort=True)
    body_size = _body_font_size(page_dict)
    parts = [f"<!-- page: {page_number} -->"]
    images: List[str] = []
    image_no = 0
    text_characters = 0
    for block in page_dict.get("blocks", []):
        if block.get("type") == 0:
            markdown = _text_block_to_markdown(block, body_size)
            if markdown:
                bbox = block.get("bbox", (0, 0, 0, 0))
                plain = re.sub(r"\s+", " ", markdown.lstrip("# ")).strip()
                is_running_header = float(bbox[1]) < 75 and bool(
                    re.search(r"\s(?:\d+|[ivxlcdm]+)$", plain, re.I)
                )
                if is_running_header:
                    continue
                if markdown.startswith("```") and parts[-1].startswith("```"):
                    previous = parts.pop().splitlines()
                    current = markdown.splitlines()
                    language = previous[0]
                    markdown = language + "\n" + "\n".join(previous[1:-1] + current[1:-1]) + "\n```"
                parts.append(markdown)
                text_characters += len(re.sub(r"\s", "", markdown))
        elif block.get("type") == 1 and block.get("image"):
            image_no += 1
            ext = str(block.get("ext") or "png").lower()
            if not re.fullmatch(r"[a-z0-9]+", ext):
                ext = "png"
            filename = f"page-{page_number:04d}-image-{image_no:02d}.{ext}"
            image_path = images_dir / filename
            image_path.parent.mkdir(parents=True, exist_ok=True)
            image_path.write_bytes(block["image"])
            relative = f"../images/{filename}"
            parts.append(f"![Image from PDF page {page_number}]({relative})")
            images.append(filename)
    if text_characters < 20:
        parts.append(ANOMALY_TEMPLATE.format(page=page_number))
    return "\n\n".join(parts).rstrip() + "\n", images, text_characters


def extract_pdf(pdf_path: Path, work_dir: Path, pages: Optional[Iterable[int]] = None, force: bool = False) -> Dict[str, object]:
    inspection = inspect_pdf(pdf_path)
    if inspection["needs_ocr"]:
        raise RuntimeError(
            "PDF 判定为扫描型：可读文本页比例 "
            f"{inspection['readable_ratio']:.1%}，中位文本字符数 {inspection['median_text_characters']}。需要先执行 OCR。"
        )

    pages_dir = work_dir / "pages"
    # Keep assets beside output/ so chapter links such as ../images/... work.
    images_dir = work_dir.parent / "images"
    pages_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    with fitz.open(pdf_path) as doc:
        selected = list(pages) if pages is not None else list(range(1, doc.page_count + 1))
        if any(page < 1 or page > doc.page_count for page in selected):
            raise ValueError(f"页码必须在 1..{doc.page_count} 范围内")
        chapters = chapters_from_toc(doc)
        manifest_path = work_dir / "manifest.json"
        if manifest_path.exists():
            import json
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        else:
            manifest = {"version": 1, "pdf": str(pdf_path.resolve()), "pages": {}}
        manifest.update({
            "updated_at": utc_now(),
            "inspection": inspection,
            "chapters": [asdict(chapter) for chapter in chapters],
        })
        for page_number in selected:
            output_path = pages_dir / f"page-{page_number:04d}.md"
            if output_path.exists() and not force and str(page_number) in manifest.get("pages", {}):
                continue
            markdown, images, char_count = _page_markdown(doc[page_number - 1], page_number, images_dir)
            atomic_write_text(output_path, markdown)
            manifest.setdefault("pages", {})[str(page_number)] = {
                "file": str(output_path),
                "characters": char_count,
                "images": images,
                "chapter": chapter_for_page(page_number, chapters),
            }
        atomic_write_json(manifest_path, manifest)
    return manifest
