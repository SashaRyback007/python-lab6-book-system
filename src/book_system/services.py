import asyncio
from typing import List, Optional
from book_system.models import Book
from book_system.repositories import BookRepository


class CatalogService:

  def __init__(
      self,
      repository: BookRepository,
      external_catalog: Optional[object] = None,
  ):
    self.repository = repository
    self.external_catalog = external_catalog

  def add_book(self, book: Book) -> None:
    if hasattr(self.repository, "add"):
      self.repository.add(book)

  def search_by_title(self, title: str) -> List[Book]:
    if not title or not title.strip():
      return []
    t = title.strip().lower()
    books = self.repository.get_all()
    return [b for b in books if t in b.title.lower()]

  def search_by_author(self, author: str) -> List[Book]:
    if not author or not author.strip():
      return []
    if hasattr(self.repository, "find_by_author"):
      res = self.repository.find_by_author(author)
      if res is not None:
        return res
    a = author.strip().lower()
    books = self.repository.get_all()
    return [b for b in books if a in b.author.lower()]

  def filter_by_year(self, year: int) -> List[Book]:
    books = self.repository.get_all()
    return [b for b in books if b.year == int(year)]

  def get_largest_book(self) -> Optional[Book]:
    books = self.repository.get_all()
    if not books:
      return None
    return max(books, key=lambda b: b.pages)

  def get_average_pages(self) -> float:
    books = self.repository.get_all()
    if not books:
      return 0.0
    return sum(b.pages for b in books) / len(books)

  async def sync_remote_book(self, book_id: int) -> Optional[Book]:
    if self.external_catalog is None:
      raise RuntimeError("External catalog service not configured")

    fetch_fn = getattr(
        self.external_catalog,
        "fetch_remote_book",
        getattr(self.external_catalog, "fetch_book", None),
    )

    if fetch_fn is None:
      raise RuntimeError("External catalog service not configured")

    if asyncio.iscoroutinefunction(fetch_fn):
      result = await fetch_fn(book_id)
    else:
      result = fetch_fn(book_id)

    if not result:
      return None

    if isinstance(result, dict):
      book = Book(
          int(result.get("id", book_id)),
          str(result.get("title", "")),
          str(result.get("author", "")),
          int(result.get("year", 2000)),
          int(result.get("pages", 100)),
      )
    else:
      book = result

    self.add_book(book)
    return book