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


def test_custom_exception_attributes_and_type():
    """Явна перевірка custom exception та його type/value (п. 6 та п. 19 методички)."""
    with pytest.raises(InvalidBookDataError) as exc_info:
        Book(1, "", "Author", 2020, 100)

    assert isinstance(exc_info.value, InvalidBookDataError)
    assert issubclass(InvalidBookDataError, Exception)
    assert "Title cannot be empty" in str(exc_info.value)


def test_book_equality():
    b1 = Book(1, "Title", "Author", 2020, 100)
    b2 = Book(1, "Title", "Author", 2020, 100)
    assert b1 == b2


def test_book_inequality():
    b1 = Book(1, "Title 1", "Author", 2020, 100)
    b2 = Book(2, "Title 2", "Author", 2020, 100)
    assert b1 != b2


def test_book_immutability():
    book = Book(1, "1984", "George Orwell", 1949, 328)
    with pytest.raises(AttributeError):
        book.title = "New Title"


# Використання pytest.param із параграфа 23 методички
@pytest.mark.parametrize(
    "invalid_year",
    [
        pytest.param(999, id="too_old"),
        pytest.param(2027, id="future"),
        pytest.param(-1, id="negative"),
    ],
)
def test_invalid_year_boundary(invalid_year):
    with pytest.raises(InvalidBookDataError, match="Year must be between"):
        Book(1, "Title", "Author", invalid_year, 100)


@pytest.mark.parametrize(
    "valid_year",
    [
        pytest.param(1000, id="min_boundary"),
        pytest.param(2026, id="max_boundary"),
    ],
)
def test_valid_year_boundary(valid_year):
    book = Book(1, "Title", "Author", valid_year, 100)
    assert book.year == valid_year


@pytest.mark.parametrize(
    "invalid_pages",
    [
        pytest.param(0, id="zero_pages"),
        pytest.param(-10, id="negative_pages"),
    ],
)
def test_invalid_pages_boundary(invalid_pages):
    with pytest.raises(InvalidBookDataError, match="Pages must be positive"):
        Book(1, "Title", "Author", 2020, invalid_pages)


def test_valid_pages_approx():
    """Використання pytest.approx (п. 7 методички)."""
    book = Book(1, "Title", "Author", 2020, 100)
    assert book.pages == pytest.approx(100)