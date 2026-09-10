import threading
import time
from pathlib import Path

from book_translator.chunker import Chunk
from book_translator.progress import ProgressStore
from book_translator.translator import BackendResponse, translate_chunks


class FakeBackend:
    name = "fake"

    def __init__(self):
        self.active = 0
        self.maximum_active = 0
        self.lock = threading.Lock()

    def chat(self, model, messages, temperature):
        with self.lock:
            self.active += 1
            self.maximum_active = max(self.maximum_active, self.active)
        time.sleep(0.01)
        source = messages[-1]["content"].split("SOURCE MARKDOWN:\n", 1)[1]
        with self.lock:
            self.active -= 1
        return BackendResponse(source, model, 10, 8, False, 0, "stop", self.name)

    def close(self):
        pass


def test_bounded_concurrent_translation_and_atomic_progress(tmp_path: Path):
    glossary = tmp_path / "glossary.yaml"
    glossary.write_text("terms: {}\n", encoding="utf-8")
    chunks = [
        Chunk(str(i), str(i), f"<!-- page: {i + 1} -->\n\nText {i}\n", [i + 1], 1, "Intro", "01-intro.md", i)
        for i in range(8)
    ]
    progress = ProgressStore(tmp_path / "progress.json")
    progress.register(chunks, tmp_path / "translated", tmp_path / "chunks")
    backend = FakeBackend()
    result = translate_chunks(
        chunks, progress, "http://unused", "key", "model", glossary,
        tmp_path / "errors.jsonl", workers=4, backend=backend,
    )
    assert result.completed == 8
    assert result.failed == 0
    assert backend.maximum_active == 4
    assert len(progress.completed_pages()) == 8
    assert all((tmp_path / "translated" / f"{i}.md").exists() for i in range(8))


def test_completed_chunk_is_not_requested_again(tmp_path: Path):
    glossary = tmp_path / "glossary.yaml"
    glossary.write_text("terms: {}\n", encoding="utf-8")
    chunk = Chunk("done", "done", "<!-- page: 1 -->\n\nText\n", [1], 1, "Intro", "01-intro.md", 0)
    progress = ProgressStore(tmp_path / "progress.json")
    progress.register([chunk], tmp_path / "translated", tmp_path / "chunks")
    (tmp_path / "translated").mkdir()
    (tmp_path / "translated" / "done.md").write_text(chunk.text, encoding="utf-8")
    progress.set_status("done", "completed")
    backend = FakeBackend()
    result = translate_chunks(
        [chunk], progress, "http://unused", "key", "model", glossary,
        tmp_path / "errors.jsonl", workers=1, backend=backend,
    )
    assert result.completed == 0
    assert backend.maximum_active == 0
