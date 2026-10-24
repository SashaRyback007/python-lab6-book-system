from unittest.mock import create_autospec
import pytest
from book_system.models import Book
from book_system.repositories import BookRepository


@pytest.fixture
def sample_book():
  return Book(1, "Kobzar", "Taras Shevchenko", 1840, 228)


@pytest.fixture
def sample_book_1():
  return Book(1, "Kobzar", "Taras Shevchenko", 1840, 228)


@pytest.fixture
def sample_book_2():
  return Book(2, "Eneida", "Ivan Kotlyarevsky", 1798, 350)


@pytest.fixture
def sample_book_3():
  return Book(3, "Dune", "Frank Herbert", 1965, 180)


@pytest.fixture
def book_list(sample_book_1, sample_book_2, sample_book_3):
  return [sample_book_1, sample_book_2, sample_book_3]


@pytest.fixture
def book_factory():
  def _make(
      b_id=1, title="Test", author="Author", year=2020, pages=200
  ):
    return Book(b_id, title, author, year, pages)

  return _make


@pytest.fixture
def mock_repo():
  return create_autospec(BookRepository, instance=True)