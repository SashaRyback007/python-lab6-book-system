from book_system.config import get_allowed_year_range

def test_get_allowed_year_range_custom(monkeypatch):
    monkeypatch.setenv("MIN_BOOK_YEAR", "1500")
    monkeypatch.setenv("MAX_BOOK_YEAR", "2020")

    min_y, max_y = get_allowed_year_range()
    assert min_y == 1500
    assert max_y == 2020

def test_get_allowed_year_range_default(monkeypatch):
    monkeypatch.delenv("MIN_BOOK_YEAR", raising=False)
    monkeypatch.delenv("MAX_BOOK_YEAR", raising=False)

    min_y, max_y = get_allowed_year_range()
    assert min_y == 1000
    assert max_y == 2026