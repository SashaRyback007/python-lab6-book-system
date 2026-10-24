from dataclasses import dataclass
from typing import Optional

class InvalidBookDataError(Exception):
    """Кастомний виняток для невалідної книги."""
    pass

@dataclass(frozen=True, slots=True)
class Book:
    book_id: int
    title: str
    author: str
    year: int
    pages: int

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise InvalidBookDataError("Title cannot be empty")
        if not self.author.strip():
            raise InvalidBookDataError("Author cannot be empty")
        if not (1000 <= self.year <= 2026):
            raise InvalidBookDataError(f"Year must be between 1000 and 2026, got {self.year}")
        if self.pages <= 0:
            raise InvalidBookDataError(f"Pages must be positive, got {self.pages}")