from book_translator.extractor import chapters_from_toc


class FakeDocument:
    def get_toc(self, simple=True):
        return [
            [1, "Preface", 2],
            [2, "Who Is This For?", 3],
            [1, "I Introduction", 10],
            [2, "Introduction to Widgets", 11],
            [3, "Widget Basics", 12],
            [2, "Using the Toolchain", 20],
            [1, "II Advanced Topics", 30],
            [2, "Interrupts", 31],
        ]


def test_infers_numbered_chapters_from_part_bookmarks():
    chapters = chapters_from_toc(FakeDocument())
    assert [chapter.number for chapter in chapters] == [1, 2, 3]
    assert chapters[0].filename == "01-introduction-to-widgets.md"
    assert chapters[2].start_page == 31
