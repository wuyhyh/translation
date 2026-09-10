from __future__ import annotations

import json
import threading
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set

from .chunker import Chunk
from .util import atomic_write_json, atomic_write_text, utc_now


ACTIVE_STATUSES = {"pending", "running", "completed", "failed"}


class ProgressStore:
    """Thread-safe, atomically persisted chunk state."""

    def __init__(self, path: Path):
        self.path = path
        self._lock = threading.RLock()
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8"))
        else:
            self.data = {
                "version": 2, "created_at": utc_now(), "updated_at": utc_now(),
                "actual_model": None, "chunks": {}, "runs": [],
            }
        self.data["version"] = max(2, int(self.data.get("version", 1)))
        self.data.setdefault("runs", [])
        self.data.setdefault("chunks", {})
        for item in self.data["chunks"].values():
            if item.get("status") in {"running", "retrying"}:
                output = Path(str(item.get("output_file", "")))
                item["status"] = "completed" if output.is_file() else "pending"
        self.save()

    def register(
        self, chunks: Iterable[Chunk], translated_dir: Path,
        source_dir: Optional[Path] = None, retire_replaced: bool = True,
    ) -> None:
        chunks = list(chunks)
        source_dir = source_dir or translated_dir.parent / "chunks"
        new_ids = {chunk.chunk_id for chunk in chunks}
        scope_by_chapter: Dict[str, set] = {}
        for chunk in chunks:
            scope_by_chapter.setdefault(chunk.chapter_file, set()).update(chunk.pages)
        with self._lock:
            if retire_replaced:
                for old_id, old in self.data["chunks"].items():
                    scope = scope_by_chapter.get(str(old.get("chapter_file")))
                    old_pages = set(old.get("pages") or [])
                    if old_id not in new_ids and scope and old_pages and old_pages.issubset(scope):
                        old["status"] = "obsolete"
                        old["updated_at"] = utc_now()
            for chunk in chunks:
                output = translated_dir / f"{chunk.chunk_id}.md"
                source = source_dir / f"{chunk.chunk_id}.md"
                atomic_write_text(source, chunk.text)
                previous = self.data["chunks"].get(chunk.chunk_id)
                if previous and previous.get("hash") == chunk.source_hash and previous.get("status") == "completed" and output.exists():
                    previous.setdefault("source_file", str(source))
                    previous.setdefault("sequence", chunk.sequence)
                    continue
                self.data["chunks"][chunk.chunk_id] = {
                    "hash": chunk.source_hash, "status": "pending",
                    "retries": int(previous.get("retries", 0)) if previous else 0,
                    "attempts": int(previous.get("attempts", 0)) if previous else 0,
                    "pages": chunk.pages, "chapter_number": chunk.chapter_number,
                    "chapter_title": chunk.chapter_title, "chapter_file": chunk.chapter_file,
                    "sequence": chunk.sequence, "source_file": str(source),
                    "output_file": str(output), "elapsed_seconds": None,
                    "input_tokens": 0, "output_tokens": 0,
                    "reasoning_present": False, "error": None, "updated_at": utc_now(),
                }
            self.save()

    def set_status(self, chunk_id: str, status: str, **updates: object) -> None:
        with self._lock:
            item = self.data["chunks"][chunk_id]
            item.update(updates)
            item["status"] = status
            item["updated_at"] = utc_now()
            self.save()

    def increment(self, chunk_id: str, field: str, amount: int = 1) -> int:
        with self._lock:
            item = self.data["chunks"][chunk_id]
            item[field] = int(item.get(field, 0)) + amount
            item["updated_at"] = utc_now()
            self.save()
            return int(item[field])

    def set_actual_model(self, model: str, backend: Optional[str] = None) -> None:
        with self._lock:
            self.data["actual_model"] = model
            if backend:
                self.data["backend"] = backend
            self.save()

    def ids_with_status(self, statuses: Set[str]) -> List[str]:
        with self._lock:
            rows = [
                (int(item.get("chapter_number", 10**9)), min(item.get("pages") or [10**9]), int(item.get("sequence", 0)), key)
                for key, item in self.data["chunks"].items() if item.get("status") in statuses
            ]
        return [row[-1] for row in sorted(rows)]

    def pending_ids(self) -> List[str]:
        return self.ids_with_status({"pending", "failed"})

    def load_chunks(self, statuses: Set[str]) -> List[Chunk]:
        result: List[Chunk] = []
        for chunk_id in self.ids_with_status(statuses):
            with self._lock:
                item = dict(self.data["chunks"][chunk_id])
            source_file = item.get("source_file")
            if not source_file or not Path(str(source_file)).exists():
                raise FileNotFoundError(f"块 {chunk_id} 缺少持久化原文，请重新执行对应 translate 或 translate-all")
            result.append(Chunk(
                chunk_id=chunk_id, source_hash=str(item["hash"]),
                text=Path(str(source_file)).read_text(encoding="utf-8"),
                pages=[int(page) for page in item.get("pages", [])],
                chapter_number=int(item.get("chapter_number", 0)),
                chapter_title=str(item.get("chapter_title", "")),
                chapter_file=str(item.get("chapter_file", "00-front-matter.md")),
                sequence=int(item.get("sequence", 0)),
            ))
        return result

    def completed_pages(self) -> Set[int]:
        states: Dict[int, List[str]] = defaultdict(list)
        with self._lock:
            for item in self.data["chunks"].values():
                if item.get("status") not in ACTIVE_STATUSES:
                    continue
                for page in item.get("pages") or []:
                    states[int(page)].append(str(item.get("status")))
        return {page for page, values in states.items() if values and all(value == "completed" for value in values)}

    def registered_pages(self) -> Set[int]:
        pages: Set[int] = set()
        with self._lock:
            for item in self.data["chunks"].values():
                if item.get("status") in ACTIVE_STATUSES:
                    pages.update(int(page) for page in item.get("pages") or [])
        return pages

    def reset_failed(self) -> int:
        count = 0
        with self._lock:
            for item in self.data["chunks"].values():
                if item.get("status") == "failed":
                    item["status"], item["error"] = "pending", None
                    item["updated_at"] = utc_now()
                    count += 1
            self.save()
        return count

    def add_run(self, run: Dict[str, object]) -> None:
        with self._lock:
            self.data.setdefault("runs", []).append(run)
            self.data["runs"] = self.data["runs"][-50:]
            self.data.pop("current_run", None)
            self.save()

    def set_current_run(self, value: Optional[Dict[str, object]]) -> None:
        with self._lock:
            if value is None:
                self.data.pop("current_run", None)
            else:
                self.data["current_run"] = value
            self.save()

    def snapshot(self) -> Dict[str, object]:
        with self._lock:
            return json.loads(json.dumps(self.data))

    def save(self) -> None:
        with self._lock:
            self.data["updated_at"] = utc_now()
            atomic_write_json(self.path, self.data)
