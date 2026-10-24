import os

def get_allowed_year_range() -> tuple[int, int]:
    min_year = int(os.getenv("MIN_BOOK_YEAR", "1000"))
    max_year = int(os.getenv("MAX_BOOK_YEAR", "2026"))
    return min_year, max_year