from pathlib import Path

from book_translator.chunker import make_chunks, split_chunk_text, split_markdown_units


def test_code_fence_is_atomic():
    text = "Intro\n\n```c\nint main(void) {\n  return 0;\n}\n```\n\nEnd"
    units = split_markdown_units(text)
    assert len(units) == 3
    assert "int main" in units[1]
    assert units[1].startswith("```c") and units[1].endswith("```")


def test_chunks_keep_page_markers_and_paragraphs(tmp_path: Path):
    page = tmp_path / "page-0001.md"
    paragraph = "A" * 2600
    page.write_text(f"<!-- page: 1 -->\n\n{paragraph}\n\n{paragraph}\n\n{paragraph}\n", encoding="utf-8")
    records = [{
        "page_number": 1,
        "file": str(page),
        "chapter": {"number": 1, "title": "Intro", "filename": "01-intro.md"},
    }]
    chunks = make_chunks(records, target_min=4000, target_max=7000)
    assert len(chunks) == 2
    assert chunks[0].text.count(paragraph) == 2
    assert chunks[1].text.count(paragraph) == 1
    assert chunks[0].pages == [1]
    assert chunks[1].pages == [1]


def test_emergency_split_keeps_units_and_marks_injected_page():
    paragraph = "A" * 2500
    source = f"<!-- page: 7 -->\n\n{paragraph}\n\n{paragraph}\n\n{paragraph}\n"
    pieces = split_chunk_text(source, 4000)
    assert len(pieces) == 3
    assert pieces[0][1] is False
    assert pieces[1][1] is True
    assert all(piece.count(paragraph) == 1 for piece, _ in pieces)
    assert all("<!-- page: 7 -->" in piece for piece, _ in pieces)
