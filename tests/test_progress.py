from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from book_translator.chunker import Chunk
from book_translator.progress import ProgressStore
from book_translator.status import progress_status


def test_running_chunk_is_reset_on_restart(tmp_path: Path):
    path = tmp_path / "progress.json"
    store = ProgressStore(path)
    store.data["chunks"]["abc"] = {"status": "running"}
    store.save()
    restarted = ProgressStore(path)
    assert restarted.data["chunks"]["abc"]["status"] == "pending"


def test_concurrent_progress_writes_remain_valid_json(tmp_path: Path):
    path = tmp_path / "progress.json"
    store = ProgressStore(path)
    chunks = [
        Chunk(str(i), str(i), f"<!-- page: {i + 1} -->\ntext", [i + 1], 1, "Intro", "01-intro.md", i)
        for i in range(12)
    ]
    store.register(chunks, tmp_path / "translated", tmp_path / "chunks")
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda chunk: store.set_status(chunk.chunk_id, "completed"), chunks))
    restarted = ProgressStore(path)
    assert len(restarted.completed_pages()) == 12


def test_status_uses_benchmark_eta_before_full_run(tmp_path: Path):
    progress = ProgressStore(tmp_path / "progress.json")
    benchmark = tmp_path / "benchmark.json"
    benchmark.write_text('{"recommendation":{"throughput_pages_per_minute":10}}', encoding="utf-8")
    status = progress_status(progress, 100, benchmark)
    assert status["rate_source"] == "benchmark"
    assert status["estimated_remaining_seconds"] == 600.0
