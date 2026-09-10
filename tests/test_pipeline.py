from pathlib import Path

from book_translator.pipeline import (
    _deduplicate_page_markers, _normalize_glossary_first_uses, merge_markdown,
)


def test_glossary_first_use_is_global_and_skips_code():
    terms = {"register": "寄存器"}
    seen = set()
    first = _normalize_glossary_first_uses("寄存器和寄存器\n```c\n// 寄存器\n```", terms, seen)
    second = _normalize_glossary_first_uses("另一个寄存器", terms, seen)
    assert first.startswith("寄存器（register）和寄存器")
    assert "// 寄存器" in first
    assert second == "另一个寄存器"


def test_existing_decoration_is_moved_to_first_use():
    terms = {"microcontroller": "微控制器"}
    output = _normalize_glossary_first_uses(
        "微控制器。后面的微控制器（microcontroller）。", terms, set()
    )
    assert output == "微控制器（microcontroller）。后面的微控制器。"


def test_final_chapter_has_one_marker_per_page():
    text = "<!-- page: 4 -->\nA\n<!-- page: 4 -->\nB\n<!-- page: 5 -->\nC"
    output = _deduplicate_page_markers(text)
    assert output.count("<!-- page: 4 -->") == 1
    assert output.count("<!-- page: 5 -->") == 1


def test_page_markers_are_canonicalized_without_losing_split_page_body():
    text = (
        "<!-- page:616 -->\nprevious\n"
        "<!--page: 617-->\nfirst half\n"
        "<!-- page: 617 -->\nsecond half\n"
        "<!-- page:618 -->\nnext"
    )
    output = _deduplicate_page_markers(text)
    assert output.count("<!-- page: 617 -->") == 1
    assert "<!--page: 617-->" not in output
    assert "<!-- page:618 -->" not in output
    assert output.count("<!-- page:") == 3
    assert output.index("first half") < output.index("second half")
    assert output.index("second half") < output.index("<!-- page: 618 -->")


def test_merge_normalizes_and_deduplicates_markers_across_chapters(tmp_path: Path):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "01-one.md").write_text(
        "<!-- page: 1 -->\none\n<!-- page:2 -->\ntwo-a\n", encoding="utf-8",
    )
    (output_dir / "02-two.md").write_text(
        "<!--page: 2-->\ntwo-b\n<!-- page:3 -->\nthree\n", encoding="utf-8",
    )
    destination = output_dir / "all-translated.md"
    merge_markdown(output_dir, destination)
    merged = destination.read_text(encoding="utf-8")
    assert all(
        marker in merged
        for marker in ("<!-- page: 1 -->", "<!-- page: 2 -->", "<!-- page: 3 -->")
    )
    assert merged.count("<!-- page:") == 3
    assert "two-a" in merged and "two-b" in merged
