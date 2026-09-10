from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Dict

from .progress import ACTIVE_STATUSES, ProgressStore


def progress_status(
    progress: ProgressStore, total_pages: int,
    benchmark_path: Path = Path("benchmarks/latest.json"),
) -> Dict[str, object]:
    data = progress.snapshot()
    active = [item for item in data.get("chunks", {}).values() if item.get("status") in ACTIVE_STATUSES]
    counts = Counter(str(item.get("status")) for item in active)
    completed_pages = len(progress.completed_pages() & set(range(1, total_pages + 1)))
    rates = []
    for run in data.get("runs", [])[-10:]:
        pages = int(run.get("pages_completed", 0) or 0)
        seconds = float(run.get("wall_seconds", 0) or 0)
        if pages > 0 and seconds > 0:
            rates.append((pages, seconds))
    pages_per_second = sum(row[0] for row in rates) / sum(row[1] for row in rates) if rates else 0.0
    rate_source = "completed-runs" if pages_per_second else None
    current = data.get("current_run") or {}
    if not pages_per_second and current.get("started_at"):
        try:
            started = datetime.fromisoformat(str(current["started_at"]))
            elapsed = (datetime.now(timezone.utc) - started).total_seconds()
            gained = completed_pages - int(current.get("initial_completed_pages", 0))
            if gained > 0 and elapsed > 0:
                pages_per_second = gained / elapsed
                rate_source = "current-run"
        except (TypeError, ValueError):
            pass
    if not pages_per_second and benchmark_path.exists():
        try:
            benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
            pages_per_second = float(benchmark["recommendation"]["throughput_pages_per_minute"]) / 60
            rate_source = "benchmark"
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            pass
    remaining = max(0, total_pages - completed_pages)
    remaining_seconds = remaining / pages_per_second if pages_per_second else None
    eta = None
    if remaining_seconds is not None:
        eta = (datetime.now(timezone.utc) + timedelta(seconds=remaining_seconds)).isoformat(timespec="seconds")
    return {
        "completed_pages": completed_pages,
        "total_pages": total_pages,
        "percent": round(completed_pages / total_pages * 100, 2) if total_pages else 0.0,
        "completed_chunks": counts.get("completed", 0),
        "pending_chunks": counts.get("pending", 0),
        "running_chunks": counts.get("running", 0) + counts.get("retrying", 0),
        "failed_chunks": counts.get("failed", 0),
        "retry_count": sum(int(item.get("retries", 0) or 0) for item in active),
        "recent_pages_per_minute": round(pages_per_second * 60, 3) if pages_per_second else None,
        "rate_source": rate_source,
        "estimated_remaining_seconds": round(remaining_seconds, 1) if remaining_seconds is not None else None,
        "estimated_completion_utc": eta,
        "actual_model": data.get("actual_model"),
        "backend": data.get("backend"),
        "current_run": data.get("current_run"),
    }
