import pytest
from book_system.models import Book, InvalidBookDataError


def test_book_init():
  b = Book(1, "1984", "George Orwell", 1949, 328)
  assert b.title == "1984"
  assert b.pages == 328


def test_invalid_title():
  with pytest.raises(InvalidBookDataError, match="Title cannot be empty"):
    Book(1, "   ", "Author", 2020, 100)


def test_invalid_author():
  with pytest.raises(InvalidBookDataError, match="Author cannot be empty"):
    Book(1, "Title", "", 2020, 100)


def test_custom_exception_properties():
  with pytest.raises(InvalidBookDataError) as exc:
    Book(1, "", "Author", 2020, 100)

  assert isinstance(exc.value, InvalidBookDataError)
  assert issubclass(InvalidBookDataError, Exception)


def test_book_eq():
  b1 = Book(1, "Title", "Author", 2020, 100)
  b2 = Book(1, "Title", "Author", 2020, 100)
  assert b1 == b2


def test_book_neq():
  b1 = Book(1, "T1", "Author", 2020, 100)
  b2 = Book(2, "T2", "Author", 2020, 100)
  assert b1 != b2


def test_immutability():
  b = Book(1, "1984", "George Orwell", 1949, 328)
  with pytest.raises(AttributeError):
    b.title = "New"


@pytest.mark.parametrize(
    "y",
    [
        pytest.param(999, id="old"),
        pytest.param(2027, id="future"),
        pytest.param(-1, id="neg"),
    ],
)
def test_invalid_year(y):
  with pytest.raises(InvalidBookDataError):
    Book(1, "Title", "Author", y, 100)


@pytest.mark.parametrize(
    "y",
    [
        pytest.param(1000, id="min"),
        pytest.param(2026, id="max"),
    ],
)
def test_valid_year(y):
  b = Book(1, "Title", "Author", y, 100)
  assert b.year == y


@pytest.mark.parametrize(
    "p",
    [
        pytest.param(0, id="zero"),
        pytest.param(-10, id="neg"),
    ],
)
def test_invalid_pages(p):
  with pytest.raises(InvalidBookDataError):
    Book(1, "Title", "Author", 2020, p)


def test_pages_approx():
  b = Book(1, "Title", "Author", 2020, 100)
  assert b.pages == pytest.approx(100)