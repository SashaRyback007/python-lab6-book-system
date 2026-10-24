import pytest
import json
from book_system.services import CatalogService
from book_system.exporters import import_from_csv, export_to_json
from book_system.models import Book

class InMemoryBookRepository:
    """Fake repository для інтеграційного тесту."""
    def __init__(self):
        self._books: list[Book] = []

    def add(self, book: Book) -> None:
        self._books.append(book)

    def get_all(self) -> list[Book]:
        return list(self._books)

    def find_by_author(self, author: str) -> list[Book]:
        return [b for b in self._books if b.author == author]

@pytest.mark.integration
def test_csv_import_search_export_pipeline(tmp_path):
    # 1. Створення тимчасового CSV
    csv_file = tmp_path / "import_books.csv"
    csv_file.write_text(
        "id,title,author,year,pages\n"
        "1,Fahrenheit 451,Ray Bradbury,1953,256\n"
        "2,Dune,Frank Herbert,1965,412\n",
        encoding="utf-8"
    )

    # 2. Імпорт книг
    imported_books = import_from_csv(csv_file)
    assert len(imported_books) == 2

    # 3. Додавання в сервіс із Fake Repository
    repo = InMemoryBookRepository()
    service = CatalogService(repo)
    for b in imported_books:
        service.add_book(b)

    # 4. Пошук і розрахунки
    search_res = service.search_by_title("Dune")
    assert len(search_res) == 1

    avg_pages = service.get_average_pages()
    assert avg_pages == pytest.approx(334.0)

    # 5. Експорт знайдених результатів у JSON
    json_file = tmp_path / "exported.json"
    export_to_json(search_res, json_file)

    assert json_file.exists()
    data = json.loads(json_file.read_text(encoding="utf-8"))
    assert data[0]["title"] == "Dune"