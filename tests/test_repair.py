import pytest

from book_translator.repair import (
    PROTECTED_RE, _safe_repair_units, _validate_semantic_completeness,
    protect_text, queue_repaired_chunks, restore_text, split_pages,
)
from book_translator.chunker import Chunk
from book_translator.progress import ProgressStore


def test_repair_protects_structure_code_images_and_identifiers():
    source = (
        "## Configure HAL_UART_Init() at https://example.com/a\n\n"
        "![diagram](../images/page-0001-image-01.png)\n\n"
        "```c\nRCC->CR = 0x01;\n```"
    )
    protected, mapping = protect_text(source)
    assert "## " not in protected
    assert "https://example.com/a" not in protected
    assert "HAL_UART_Init" not in protected
    assert "![diagram]" not in protected
    assert "RCC->CR" not in protected
    assert restore_text(protected, mapping) == source


def test_placeholder_loss_is_rejected():
    protected, mapping = protect_text("Call HAL_Init() and use 0x10")
    with pytest.raises(ValueError):
        restore_text(protected.replace(next(iter(mapping)), ""), mapping)


def test_page_markers_are_split_out_for_programmatic_restore():
    pages = split_pages("<!-- page: 4 -->\n\nAlpha\n\n<!-- page: 5 -->\n\nBeta")
    assert pages == [(4, "Alpha"), (5, "Beta")]


def test_protected_spans_can_be_anchored_without_model_round_trip():
    source = "## Call HAL_Init() using 0x10"
    spans = [match.group(0) for match in PROTECTED_RE.finditer(source)]
    assert spans == ["## ", "HAL_Init", "0x10"]


def test_long_prose_splits_but_code_does_not():
    paragraph = "word " * 1000
    code = "```c\n" + ("x++;\n" * 500) + "```"
    units = _safe_repair_units(paragraph + "\n\n" + code, maximum=1000)
    assert len(units) > 2
    assert units[-1] == code
    assert all(len(unit) <= 1000 for unit in units[:-1])


def test_numbers_and_toc_leaders_are_protected():
    source = "10.2 Clock Tree . . . . . . . . 257"
    protected, mapping = protect_text(source)
    assert "10.2" not in protected
    assert "257" not in protected
    assert ". . . ." not in protected
    assert restore_text(protected, mapping) == source


def test_obvious_semantic_omission_is_rejected():
    source = "This technical paragraph contains enough meaningful English text to require a complete translated result."
    with pytest.raises(ValueError, match="明显不完整"):
        _validate_semantic_completeness(source, "短")


def test_requeue_only_prior_repair_outputs(tmp_path):
    work = tmp_path / "work"
    chunks = [
        Chunk("regular", "a", "<!-- page: 1 -->\n\nA", [1], 1, "One", "01-one.md", 0),
        Chunk("repaired", "b", "<!-- page: 2 -->\n\nB", [2], 1, "One", "01-one.md", 1),
    ]
    progress = ProgressStore(work / "progress.json")
    progress.register(chunks, work / "translated", work / "chunks")
    for chunk_id in ("regular", "repaired"):
        output = work / "translated" / f"{chunk_id}.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(chunks[0 if chunk_id == "regular" else 1].text, encoding="utf-8")
        progress.set_status(chunk_id, "completed", repaired=chunk_id == "repaired")
    assert queue_repaired_chunks(progress) == ["repaired"]
    assert progress.snapshot()["chunks"]["regular"]["status"] == "completed"
    assert progress.snapshot()["chunks"]["repaired"]["status"] == "failed"
