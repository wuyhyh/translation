from book_translator.benchmark import _choose_size, _choose_workers


def result(workers, size, rate, valid=True):
    return {
        "workers": workers, "chunk_size": size,
        "throughput_pages_per_minute": rate,
        "complete": valid, "reasoning_present": False,
        "failed_chunks": 0, "markdown_complete": valid,
    }


def test_size_prefers_8000_without_material_gain():
    assert _choose_size([result(1, 8000, 8.4), result(1, 12000, 8.5)]) == 8000
    assert _choose_size([result(1, 8000, 8.4), result(1, 12000, 9.0)]) == 12000


def test_workers_rejects_less_than_ten_percent_gain_from_four():
    values = [result(1, 8000, 8.0), result(2, 8000, 8.4), result(4, 8000, 9.0)]
    assert _choose_workers(values) == 2


def test_workers_can_choose_one_for_serial_server():
    values = [result(1, 8000, 8.45), result(2, 8000, 8.36), result(4, 8000, 8.50)]
    assert _choose_workers(values) == 1
