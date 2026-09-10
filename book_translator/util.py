from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, List


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def atomic_write_json(path: Path, data: Any) -> None:
    atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def slugify(text: str, fallback: str = "chapter") -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or fallback


def parse_page_ranges(spec: str, page_count: int | None = None) -> List[int]:
    """Parse 1-based ranges such as '3-5,8,10-11'."""
    pages = set()
    for raw_part in spec.split(","):
        part = raw_part.strip()
        if not part:
            continue
        if "-" in part:
            bits = part.split("-", 1)
            if not all(bit.strip().isdigit() for bit in bits):
                raise ValueError(f"无效页码范围: {part}")
            start, end = (int(bit) for bit in bits)
            if start > end:
                raise ValueError(f"页码范围起点大于终点: {part}")
            pages.update(range(start, end + 1))
        elif part.isdigit():
            pages.add(int(part))
        else:
            raise ValueError(f"无效页码: {part}")
    if not pages:
        raise ValueError("页码不能为空")
    if min(pages) < 1 or (page_count is not None and max(pages) > page_count):
        raise ValueError(f"页码必须在 1..{page_count or '最后一页'} 范围内")
    return sorted(pages)


def contiguous_ranges(values: Iterable[int]) -> str:
    values = sorted(set(values))
    if not values:
        return ""
    groups = []
    start = prev = values[0]
    for value in values[1:]:
        if value == prev + 1:
            prev = value
            continue
        groups.append(str(start) if start == prev else f"{start}-{prev}")
        start = prev = value
    groups.append(str(start) if start == prev else f"{start}-{prev}")
    return ",".join(groups)
