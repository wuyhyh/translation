from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Dict, Iterable, List

from .chunker import load_page_records, make_chunks
from .extractor import extract_pdf
from .progress import ProgressStore
from .translator import create_backend, resolve_backend, translate_chunks
from .util import atomic_write_json, utc_now


def _valid(result: Dict[str, object]) -> bool:
    return bool(
        result.get("complete")
        and not result.get("reasoning_present")
        and int(result.get("failed_chunks", 0)) == 0
        and result.get("markdown_complete")
    )


def _run_configuration(
    records, pages: List[int], workers: int, chunk_size: int, backend_name: str,
    base_url: str, api_key: str, model: str, glossary_path: Path,
    root: Path, timeout: float,
) -> Dict[str, object]:
    config_root = root / f"workers-{workers}-chars-{chunk_size}"
    chunks = make_chunks(records, target_min=max(4000, int(chunk_size * 0.6)), target_max=chunk_size)
    progress = ProgressStore(config_root / "progress.json")
    progress.register(chunks, config_root / "translated", config_root / "chunks", retire_replaced=False)
    backend = create_backend(backend_name, base_url, api_key, timeout, workers)
    try:
        summary = translate_chunks(
            chunks, progress, base_url, api_key, model, glossary_path,
            config_root / "errors.jsonl", timeout=timeout, temperature=0.1,
            max_retries=3, workers=workers, backend_name=backend_name,
            chunk_max=chunk_size, total_pages=None, progress_every=0, backend=backend,
        )
    finally:
        backend.close()
    source_headings = sum(chunk.text.count("\n#") + int(chunk.text.startswith("#")) for chunk in chunks)
    source_fences = sum(chunk.text.count("```") for chunk in chunks)
    source_images = sum(chunk.text.count("![") for chunk in chunks)
    snapshot = progress.snapshot()
    output_headings = output_fences = output_images = 0
    for item in snapshot["chunks"].values():
        path = Path(str(item["output_file"]))
        if item.get("status") == "completed" and path.exists():
            text = path.read_text(encoding="utf-8")
            output_headings += text.count("\n#") + int(text.startswith("#"))
            output_fences += text.count("```")
            output_images += text.count("![")
    markdown_complete = (
        source_headings == output_headings
        and source_fences == output_fences
        and source_images == output_images
    )
    page_count = len(pages)
    completed_results = [item for item in summary.chunk_results if item.success]
    return {
        "workers": workers, "chunk_size": chunk_size, "pages": pages,
        "page_count": page_count, "chunk_count": len(chunks),
        "total_seconds": summary.wall_seconds,
        "average_seconds_per_page": round(summary.wall_seconds / page_count, 3),
        "average_seconds_per_chunk": round(
            sum(item.elapsed_seconds for item in completed_results) / len(completed_results), 3
        ) if completed_results else None,
        "throughput_pages_per_minute": round(page_count / summary.wall_seconds * 60, 3),
        "input_tokens": summary.input_tokens, "output_tokens": summary.output_tokens,
        "failed_chunks": summary.failed, "retry_count": summary.retries,
        "request_count": summary.requests, "auto_splits": summary.splits,
        "reasoning_present": summary.reasoning_present,
        "complete": summary.completed == len(chunks) and summary.failed == 0,
        "markdown_complete": markdown_complete,
        "headings": {"source": source_headings, "output": output_headings},
        "code_fences": {"source": source_fences, "output": output_fences},
        "image_references": {"source": source_images, "output": output_images},
        "actual_model": summary.actual_model, "backend": summary.backend,
    }


def _choose_size(results: List[Dict[str, object]]) -> int:
    valid = [item for item in results if _valid(item)]
    if not valid:
        raise RuntimeError("块尺寸基准全部失败")
    by_size = {int(item["chunk_size"]): item for item in valid}
    if 12000 in by_size and 8000 in by_size:
        if float(by_size[12000]["throughput_pages_per_minute"]) > float(by_size[8000]["throughput_pages_per_minute"]) * 1.02:
            return 12000
        return 8000
    return int(max(valid, key=lambda item: float(item["throughput_pages_per_minute"]))["chunk_size"])


def _choose_workers(results: List[Dict[str, object]]) -> int:
    valid = {int(item["workers"]): item for item in results if _valid(item)}
    if not valid:
        raise RuntimeError("并发基准全部失败")
    candidates = dict(valid)
    if 2 in valid and 4 in valid:
        rate2 = float(valid[2]["throughput_pages_per_minute"])
        rate4 = float(valid[4]["throughput_pages_per_minute"])
        if rate4 < rate2 * 1.10:
            candidates.pop(4, None)
    return int(max(candidates, key=lambda value: float(candidates[value]["throughput_pages_per_minute"])))


def run_benchmark(
    pdf_path: Path, pages: Iterable[int], base_url: str, api_key: str, model: str,
    glossary_path: Path, results_path: Path, timeout: float = 600,
    requested_backend: str = "auto",
) -> Dict[str, object]:
    pages = sorted(set(int(page) for page in pages))
    if not (10 <= len(pages) <= 20):
        raise ValueError("基准页数必须在 10～20 之间")
    probe_backend, probes = resolve_backend(requested_backend, base_url, api_key, model, timeout, 1)
    selected_backend = str(probe_backend.name)
    probe_backend.close()
    results: List[Dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="pdf-translation-benchmark-") as temp_name:
        root = Path(temp_name)
        extraction = root / "extraction" / "work"
        extract_pdf(pdf_path, extraction, pages=pages, force=True)
        records = load_page_records(extraction, pages=pages)

        size_results = []
        for size in (8000, 12000):
            item = _run_configuration(
                records, pages, 1, size, selected_backend, base_url, api_key,
                model, glossary_path, root, timeout,
            )
            results.append(item)
            size_results.append(item)
        selected_size = _choose_size(size_results)

        concurrency_results = [item for item in results if item["workers"] == 1 and item["chunk_size"] == selected_size]
        for workers in (2, 4):
            item = _run_configuration(
                records, pages, workers, selected_size, selected_backend, base_url,
                api_key, model, glossary_path, root, timeout,
            )
            results.append(item)
            concurrency_results.append(item)
        selected_workers = _choose_workers(concurrency_results)

    selected = next(
        item for item in results
        if item["workers"] == selected_workers and item["chunk_size"] == selected_size
    )
    estimated_910_seconds = 910 / float(selected["throughput_pages_per_minute"]) * 60
    report = {
        "created_at": utc_now(), "pdf": str(pdf_path.resolve()), "pages": pages,
        "requested_model": model, "backend_probes": probes,
        "selected_backend": selected_backend, "results": results,
        "recommendation": {
            "workers": selected_workers, "chunk_size": selected_size,
            "backend": selected_backend,
            "throughput_pages_per_minute": selected["throughput_pages_per_minute"],
            "estimated_910_seconds": round(estimated_910_seconds, 1),
        },
    }
    atomic_write_json(results_path, report)
    return report
