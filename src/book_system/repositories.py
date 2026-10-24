from abc import ABC, abstractmethod
from typing import List, Optional
from book_system.models import Book


class BookRepository(ABC):

  @abstractmethod
  def get_all(self) -> List[Book]: ...

  @abstractmethod
  def find_by_author(self, author: str) -> List[Book]: ...

  @abstractmethod
  def add(self, book: Book) -> None: ...


class InMemoryBookRepository(BookRepository):

  def __init__(self):
    self._books: List[Book] = []

  def get_all(self) -> List[Book]:
    return list(self._books)

  def find_by_author(self, author: str) -> List[Book]:
    return [
        b for b in self._books if author.lower() in b.author.lower()
    ]

  def add(self, book: Book) -> None:
    self._books.append(book)


class ExternalCatalog(ABC):

  @abstractmethod
  def fetch_remote_book(self, book_id: int) -> Optional[Book]: ...


class AsyncExternalCatalog(ABC):

  @abstractmethod
  async def fetch_remote_book(self, book_id: int) -> Optional[Book]: ...