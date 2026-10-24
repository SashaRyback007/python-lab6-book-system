import json
import pytest
from book_system.exporters import export_to_json, import_from_csv
from book_system.models import Book
from book_system.services import CatalogService


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
def test_csv_import_pipeline(tmp_path):
  p = tmp_path / "data.csv"
  p.write_text(
      "id,title,author,year,pages\n1,Kobzar,Taras Shevchenko,1840,228\n",
      encoding="utf-8",
  )
  books = import_from_csv(p)
  srv = CatalogService(InMemoryBookRepository())
  for b in books:
    srv.add_book(b)

  assert len(srv.search_by_author("Taras Shevchenko")) == 1


@pytest.mark.integration
def test_export_pipeline(tmp_path):
  srv = CatalogService(InMemoryBookRepository())
  srv.add_book(Book(1, "Dune", "Frank Herbert", 1965, 412))

  out = tmp_path / "out.json"
  export_to_json(srv.search_by_title("Dune"), out)

  assert out.exists()
  res = json.loads(out.read_text(encoding="utf-8"))
  assert res[0]["title"] == "Dune"


@pytest.mark.integration
def test_full_pipeline(tmp_path):
  inp = tmp_path / "in.csv"
  inp.write_text(
      "id,title,author,year,pages\n1,Fahrenheit 451,Ray"
      " Bradbury,1953,256\n2,Dune,Frank Herbert,1965,412\n",
      encoding="utf-8",
  )

  srv = CatalogService(InMemoryBookRepository())
  for b in import_from_csv(inp):
    srv.add_book(b)

  out = tmp_path / "res.json"
  export_to_json(srv.search_by_title("Dune"), out)
  assert out.exists()