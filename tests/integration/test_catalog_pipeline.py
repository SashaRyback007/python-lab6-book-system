import pytest
import json
from book_system.services import CatalogService
from book_system.exporters import import_from_csv, export_to_json
from book_system.models import Book, InvalidBookDataError

class InMemoryBookRepository:
    def __init__(self):
        self._books: list[Book] = []

    def add(self, book: Book) -> None:
        self._books.append(book)

    def get_all(self) -> list[Book]:
        return list(self._books)

    def find_by_author(self, author: str) -> list[Book]:
        return [b for b in self._books if b.author == author]

@pytest.mark.integration
def test_csv_import_to_repository_pipeline(tmp_path):
    """Integration Test 1: Import CSV -> Populate Repository."""
    csv_file = tmp_path / "books.csv"
    csv_file.write_text(
        "id,title,author,year,pages\n"
        "1,Kobzar,Taras Shevchenko,1840,228\n",
        encoding="utf-8"
    )
    books = import_from_csv(csv_file)
    repo = InMemoryBookRepository()
    service = CatalogService(repo)
    for b in books:
        service.add_book(b)
    
    assert len(service.search_by_author("Taras Shevchenko")) == 1

@pytest.mark.integration
def test_service_search_and_export_pipeline(tmp_path):
    """Integration Test 2: Repository -> Search -> Export JSON."""
    repo = InMemoryBookRepository()
    service = CatalogService(repo)
    service.add_book(Book(1, "Dune", "Frank Herbert", 1965, 412))
    
    results = service.search_by_title("Dune")
    json_file = tmp_path / "output.json"
    export_to_json(results, json_file)

    assert json_file.exists()
    data = json.loads(json_file.read_text(encoding="utf-8"))
    assert data[0]["title"] == "Dune"

@pytest.mark.integration
def test_full_csv_import_search_export_flow(tmp_path):
    """Integration Test 3: Full End-to-End Pipeline."""
    csv_file = tmp_path / "import_books.csv"
    csv_file.write_text(
        "id,title,author,year,pages\n"
        "1,Fahrenheit 451,Ray Bradbury,1953,256\n"
        "2,Dune,Frank Herbert,1965,412\n",
        encoding="utf-8"
    )

    imported_books = import_from_csv(csv_file)
    repo = InMemoryBookRepository()
    service = CatalogService(repo)
    for b in imported_books:
        service.add_book(b)

    search_res = service.search_by_title("Dune")
    json_file = tmp_path / "exported.json"
    export_to_json(search_res, json_file)

    assert json_file.exists()