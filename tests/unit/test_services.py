import pytest
from unittest.mock import Mock, AsyncMock
from book_system.models import Book
from book_system.services import CatalogService
from book_system.repositories import BookRepository, AsyncExternalCatalog

def test_empty_catalog_search_and_stats():
    repo = Mock(spec=BookRepository)
    repo.get_all.return_value = []
    service = CatalogService(repo)

    assert service.get_largest_book() is None
    assert service.get_average_pages() == pytest.approx(0.0)

def test_search_by_title(book_list):
    repo = Mock(spec=BookRepository)
    repo.get_all.return_value = book_list
    service = CatalogService(repo)

    results = service.search_by_title("kobzar")
    assert len(results) == 1
    assert results[0].title == "Kobzar"

def test_search_by_author(book_list):
    repo = Mock(spec=BookRepository)
    repo.find_by_author.return_value = [book_list[0], book_list[2]]
    service = CatalogService(repo)

    results = service.search_by_author("Taras Shevchenko")
    assert len(results) == 2
    repo.find_by_author.assert_called_once_with("Taras Shevchenko")

def test_filter_by_year(book_list):
    repo = Mock(spec=BookRepository)
    repo.get_all.return_value = book_list
    service = CatalogService(repo)

    results = service.filter_by_year(1798)
    assert len(results) == 1
    assert results[0].title == "Eneida"

def test_get_largest_book(book_list):
    repo = Mock(spec=BookRepository)
    repo.get_all.return_value = book_list
    service = CatalogService(repo)

    largest = service.get_largest_book()
    assert largest is not None
    assert largest.title == "Eneida"
    assert largest.pages == 350

def test_get_average_pages(book_list):
    repo = Mock(spec=BookRepository)
    repo.get_all.return_value = book_list
    service = CatalogService(repo)

    # (228 + 350 + 180) / 3 = 252.6666...
    avg = service.get_average_pages()
    assert avg == pytest.approx(252.6666, rel=1e-3)
def test_mock_return_value_explicit():
    repo = Mock(spec=BookRepository)
    repo.get_all.return_value = []
    service = CatalogService(repo)
    assert service.get_largest_book() is None

def test_mock_side_effect_explicit():
    repo = Mock(spec=BookRepository)
    repo.find_by_author.side_effect = RuntimeError("DB connection error")
    service = CatalogService(repo)
    with pytest.raises(RuntimeError, match="DB connection error"):
        service.search_by_author("Taras Shevchenko")
        
@pytest.mark.asyncio
async def test_async_sync_remote_book_success():
    repo = Mock(spec=BookRepository)
    ext_catalog = AsyncMock(spec=AsyncExternalCatalog)
    ext_catalog.fetch_remote_book.return_value = {
        "id": 10,
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965,
        "pages": 412
    }

    service = CatalogService(repo, external_catalog=ext_catalog)
    book = await service.sync_remote_book("123456789")

    assert book.title == "Dune"
    ext_catalog.fetch_remote_book.assert_awaited_once_with("123456789")
    repo.add.assert_called_once_with(book)

@pytest.mark.asyncio
async def test_async_sync_remote_book_failure_side_effect():
    repo = Mock(spec=BookRepository)
    ext_catalog = AsyncMock(spec=AsyncExternalCatalog)
    ext_catalog.fetch_remote_book.side_effect = ConnectionError("Network down")

    service = CatalogService(repo, external_catalog=ext_catalog)

    with pytest.raises(ConnectionError, match="Network down"):
        await service.sync_remote_book("123456789")
    
    repo.add.assert_not_called()