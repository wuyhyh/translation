from pathlib import Path

from book_translator.audit import (
    FUNCTION_RE, MACRO_RE, PATH_RE, REGISTER_RE, _equivalent_identifier_present,
    _function_source_tokens, _identifier_tokens, audit_project,
    restore_exact_code_blocks,
)
from book_translator.chunker import Chunk
from book_translator.progress import ProgressStore


def test_audit_detects_exact_complete_project(tmp_path: Path):
    work = tmp_path / "work"
    output = tmp_path / "output"
    images = tmp_path / "images"
    images.mkdir()
    source = "<!-- page: 1 -->\n\n# Title\n\n```c\nHAL_Init();\n```\n"
    translated = "<!-- page: 1 -->\n\n# 标题\n\n```c\nHAL_Init();\n```\n"
    chunk = Chunk("one", "hash", source, [1], 1, "Intro", "01-intro.md", 0)
    progress = ProgressStore(work / "progress.json")
    progress.register([chunk], work / "translated", work / "chunks")
    Path(progress.data["chunks"]["one"]["output_file"]).parent.mkdir(parents=True)
    Path(progress.data["chunks"]["one"]["output_file"]).write_text(translated, encoding="utf-8")
    progress.set_status("one", "completed", reasoning_present=False, finish_reason="stop")
    (work / "manifest.json").write_text(
        '{"pages":{"1":{"characters":10,"chapter":{"number":1,"title":"Intro"}}}}', encoding="utf-8"
    )
    result = audit_project(progress, work, output, 1, tmp_path / "audit.md")
    assert result["passed"] is True
    assert (tmp_path / "audit.md").exists()


def test_audit_rejects_changed_code(tmp_path: Path):
    work = tmp_path / "work"
    output = tmp_path / "output"
    source = "<!-- page: 1 -->\n\n```c\nvalue = 1;\n```\n"
    chunk = Chunk("one", "hash", source, [1], 1, "Intro", "01-intro.md", 0)
    progress = ProgressStore(work / "progress.json")
    progress.register([chunk], work / "translated", work / "chunks")
    path = Path(progress.data["chunks"]["one"]["output_file"])
    path.parent.mkdir(parents=True)
    path.write_text("<!-- page: 1 -->\n\n```c\nvalue = 2;\n```\n", encoding="utf-8")
    progress.set_status("one", "completed")
    (work / "manifest.json").write_text(
        '{"pages":{"1":{"characters":10,"chapter":{"number":1,"title":"Intro"}}}}', encoding="utf-8"
    )
    result = audit_project(progress, work, output, 1, tmp_path / "audit.md")
    code_check = next(item for item in result["checks"] if item["name"] == "Code block contents exact")
    assert code_check["passed"] is False


def test_restore_code_blocks_uses_source_without_touching_prose(tmp_path: Path):
    work = tmp_path / "work"
    source = "<!-- page: 1 -->\n\nText\n\n```c\nvalue = 1; // comment\n```\n"
    translated = "<!-- page: 1 -->\n\n正文\n\n```c\nvalue = 2; // 注释\n```\n"
    chunk = Chunk("one", "hash", source, [1], 1, "Intro", "01-intro.md", 0)
    progress = ProgressStore(work / "progress.json")
    progress.register([chunk], work / "translated", work / "chunks")
    path = Path(progress.data["chunks"]["one"]["output_file"])
    path.parent.mkdir(parents=True)
    path.write_text(translated, encoding="utf-8")
    progress.set_status("one", "completed")
    result = restore_exact_code_blocks(progress)
    assert result["changed"] == ["one"]
    restored = path.read_text(encoding="utf-8")
    assert "正文" in restored
    assert "value = 1; // comment" in restored
    assert "value = 2" not in restored


def test_source_repeated_paragraph_on_same_pages_is_not_false_positive(tmp_path: Path):
    work = tmp_path / "work"
    output = tmp_path / "output"
    repeated_source = "Repeated source paragraph " * 12
    repeated_output = "重复的译文段落" * 30
    source = f"<!-- page: 1 -->\n\n{repeated_source}\n\n<!-- page: 2 -->\n\n{repeated_source}\n"
    translated = f"<!-- page: 1 -->\n\n{repeated_output}\n\n<!-- page: 2 -->\n\n{repeated_output}\n"
    chunk = Chunk("one", "hash", source, [1, 2], 1, "Intro", "01-intro.md", 0)
    progress = ProgressStore(work / "progress.json")
    progress.register([chunk], work / "translated", work / "chunks")
    path = Path(progress.data["chunks"]["one"]["output_file"])
    path.parent.mkdir(parents=True)
    path.write_text(translated, encoding="utf-8")
    progress.set_status("one", "completed")
    (work / "manifest.json").write_text(
        '{"pages":{"1":{"characters":10,"chapter":{"number":1}},"2":{"characters":10,"chapter":{"number":1}}}}',
        encoding="utf-8",
    )
    result = audit_project(progress, work, output, 2, tmp_path / "audit.md")
    duplicate = next(item for item in result["checks"] if item["name"] == "No abnormal duplicate paragraphs")
    assert duplicate["passed"] is True


def test_identifier_boundaries_work_next_to_chinese_and_superscripts():
    translated = "¹²HAL_ADC 模块调用 aes_enc_dec() 函数。"
    assert "HAL_ADC" in _identifier_tokens(translated, REGISTER_RE)
    assert "HAL_ADC" in _identifier_tokens(translated, MACRO_RE)
    assert "aes_enc_dec" in _function_source_tokens(translated)


def test_path_detection_excludes_operator_slashes_but_keeps_real_paths():
    text = (
        "printf()/scanf(), 1$/pc, D+/D- lines, VOUT/VREF, POR/Power Down; "
        "C:\\ST\\STM32CubeIDE； /dev/ttyUSB0 and Core/Src/main.c"
    )
    paths = _identifier_tokens(text, PATH_RE)
    assert paths == {"C:\\ST\\STM32CubeIDE", "/dev/ttyUSB0", "Core/Src/main.c"}


def test_identifier_equivalents_are_chunk_and_token_specific():
    translated = "portable/GCC/ARM_CM0 contains portmacro.h; UART_IRQ_Handler() runs."
    assert _equivalent_identifier_present(
        "1d323e27d9522c68", "portable/GCC/ARM_CMO", translated,
    )
    assert _equivalent_identifier_present(
        "1d323e27d9522c68", "portmarco.h", translated,
    )
    assert _equivalent_identifier_present(
        "c0e024d8bbe95fb7", "UART_IRQ_Hanler", translated,
    )
    assert not _equivalent_identifier_present("another-chunk", "ARM_CMO", translated)
