import csv
import json
from pathlib import Path
from book_system.models import Book, InvalidBookDataError

def export_to_json(books: list[Book], path: Path) -> None:
    data = [
        {
            "id": b.book_id,
            "title": b.title,
            "author": b.author,
            "year": b.year,
            "pages": b.pages
        }
        for b in books
    ]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def import_from_csv(path: Path) -> list[Book]:
    books = []
    content = path.read_text(encoding="utf-8").splitlines()
    reader = csv.DictReader(content)
    for row in reader:
        try:
            book = Book(
                book_id=int(row["id"]),
                title=row["title"],
                author=row["author"],
                year=int(row["year"]),
                pages=int(row["pages"])
            )
            books.append(book)
        except (KeyError, ValueError) as e:
            raise InvalidBookDataError(f"Malformed CSV record: {row}") from e
    return books