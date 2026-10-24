import pytest
from book_system.models import Book
from book_system.services import CatalogService

@pytest.fixture
def sample_book_1() -> Book:
    return Book(book_id=1, title="Kobzar", author="Taras Shevchenko", year=1840, pages=228)

@pytest.fixture
def sample_book_2() -> Book:
    return Book(book_id=2, title="Eneida", author="Ivan Kotliarevsky", year=1798, pages=350)

@pytest.fixture
def sample_book_3() -> Book:
    return Book(book_id=3, title="Gaydamaky", author="Taras Shevchenko", year=1841, pages=180)

@pytest.fixture
def book_list(sample_book_1, sample_book_2, sample_book_3) -> list[Book]:
    return [sample_book_1, sample_book_2, sample_book_3]