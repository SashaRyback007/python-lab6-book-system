from book_system.models import Book
from book_system.repositories import InMemoryBookRepository


def test_in_memory_repository_full():
  repo = InMemoryBookRepository()
  book = Book(1, "Title", "Author", 2020, 100)

  repo.add(book)
  assert repo.get_all() == [book]
  assert repo.find_by_author("author") == [book]
  assert repo.find_by_author("nonexistent") == []