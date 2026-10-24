from typing import Optional
from book_system.models import Book
from book_system.repositories import BookRepository, AsyncExternalCatalog

class CatalogService:
    def __init__(self, repository: BookRepository, external_catalog: Optional[AsyncExternalCatalog] = None) -> None:
        self.repo = repository
        self.external_catalog = external_catalog

    def add_book(self, book: Book) -> None:
        self.repo.add(book)

    def search_by_title(self, query: str) -> list[Book]:
        return [b for b in self.repo.get_all() if query.lower() in b.title.lower()]

    def search_by_author(self, author: str) -> list[Book]:
        return self.repo.find_by_author(author)

    def filter_by_year(self, year: int) -> list[Book]:
        return [b for b in self.repo.get_all() if b.year == year]

    def get_largest_book(self) -> Optional[Book]:
        books = self.repo.get_all()
        if not books:
            return None
        return max(books, key=lambda b: b.pages)

    def get_average_pages(self) -> float:
        books = self.repo.get_all()
        if not books:
            return 0.0
        return sum(b.pages for b in books) / len(books)

    async def sync_remote_book(self, isbn: str) -> Book:
        if not self.external_catalog:
            raise RuntimeError("External catalog service not configured")
        data = await self.external_catalog.fetch_remote_book(isbn)
        book = Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            pages=data["pages"]
        )
        self.repo.add(book)
        return book