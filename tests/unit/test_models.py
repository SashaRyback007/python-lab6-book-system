import pytest
from book_system.models import Book, InvalidBookDataError

def test_valid_book_creation():
    book = Book(1, "1984", "George Orwell", 1949, 328)
    assert book.title == "1984"
    assert book.pages == 328

def test_empty_title_raises_exception():
    with pytest.raises(InvalidBookDataError, match="Title cannot be empty"):
        Book(1, "   ", "Author", 2020, 100)

def test_empty_author_raises_exception():
    with pytest.raises(InvalidBookDataError, match="Author cannot be empty"):
        Book(1, "Title", "", 2020, 100)

def test_custom_exception_inheritance():
    """Явна перевірка custom exception."""
    with pytest.raises(InvalidBookDataError) as exc_info:
        Book(1, "", "Author", 2020, 100)
    
    assert isinstance(exc_info.value, Exception)
    assert "Title cannot be empty" in str(exc_info.value)
    
@pytest.mark.parametrize("invalid_year", [999, 2027, -1], ids=["too_old", "future", "negative"])
def test_invalid_year_boundary(invalid_year):
    with pytest.raises(InvalidBookDataError, match="Year must be between"):
        Book(1, "Title", "Author", invalid_year, 100)

@pytest.mark.parametrize("valid_year", [1000, 2026], ids=["min_boundary", "max_boundary"])
def test_valid_year_boundary(valid_year):
    book = Book(1, "Title", "Author", valid_year, 100)
    assert book.year == valid_year

@pytest.mark.parametrize("invalid_pages", [0, -10], ids=["zero", "negative"])
def test_invalid_pages_boundary(invalid_pages):
    with pytest.raises(InvalidBookDataError, match="Pages must be positive"):
        Book(1, "Title", "Author", 2020, invalid_pages)