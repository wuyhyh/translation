import pytest

from book_translator.util import parse_page_ranges, slugify


def test_parse_page_ranges():
    assert parse_page_ranges("3-5, 8,5", 10) == [3, 4, 5, 8]


def test_parse_page_ranges_rejects_invalid():
    with pytest.raises(ValueError):
        parse_page_ranges("8-3", 10)
    with pytest.raises(ValueError):
        parse_page_ranges("11", 10)


def test_slugify_is_portable():
    assert slugify("Get In Touch With STM32CubeIDE!") == "get-in-touch-with-stm32cubeide"

