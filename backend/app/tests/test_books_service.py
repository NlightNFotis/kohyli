import pytest
import pytest_asyncio
from datetime import datetime
from decimal import Decimal

from sqlmodel import SQLModel, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database.models import Author, Book
from app.services.books import BooksService

# In-memory SQLite for tests
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="module")
async def async_engine():
    engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(async_engine):
    """Provide a fresh AsyncSession for each test."""
    async_session_maker = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_maker() as session:
        yield session
        await session.rollback()


async def _clear_tables(session: AsyncSession):
    """Remove rows from tables used by these tests (children first)."""
    await session.execute(text("DELETE FROM book"))
    await session.execute(text("DELETE FROM author"))
    await session.commit()


async def _seed_authors_and_books(session: AsyncSession):
    """Clear tables then insert sample authors and books."""
    await _clear_tables(session)

    a1 = Author(
        id=1, first_name="J.R.R.", last_name="Tolkien", biography="Fantasy author"
    )
    a2 = Author(
        id=2, first_name="George", last_name="Orwell", biography="Dystopian author"
    )

    b1 = Book(
        id=1001,
        title="The Hobbit",
        author_id=1,
        isbn="978-0-618-00221-0",
        price=Decimal("15.99"),
        published_date=datetime.utcnow(),
        stock_quantity=50,
    )
    b2 = Book(
        id=1002,
        title="1984",
        author_id=2,
        isbn="978-0-452-28423-4",
        price=Decimal("12.50"),
        published_date=datetime.utcnow(),
        stock_quantity=40,
    )
    b3 = Book(
        id=1003,
        title="Another Tolkien",
        author_id=1,
        isbn="isbn-1003",
        price=Decimal("8.00"),
        published_date=datetime.utcnow(),
        stock_quantity=5,
    )

    session.add_all([a1, a2, b1, b2, b3])
    await session.commit()
    await session.refresh(b1)
    await session.refresh(b2)
    await session.refresh(b3)


@pytest.mark.asyncio
async def test_get_all_and_get_by_id(session: AsyncSession):
    # Arrange
    await _seed_authors_and_books(session)
    svc = BooksService(session)

    # Act
    all_books = await svc.get_all()
    book = await svc.get_by_id(1001)

    # Assert
    assert isinstance(all_books, list)
    assert len(all_books) >= 3
    assert book is not None
    assert book.title == "The Hobbit"
    assert book.author_id == 1

    # New: author should be loaded on the returned Book objects
    # (BooksService now uses selectinload(Book.author))
    for b in all_books:
        assert getattr(b, "author", None) is not None
        assert b.author.id is not None
        assert b.author.first_name is not None
        assert b.author.last_name is not None

    # and the single book retrieved by id should have its author populated
    assert book.author is not None
    assert book.author.first_name == "J.R.R."
    assert book.author.last_name == "Tolkien"



@pytest.mark.asyncio
async def test_get_by_id_not_found(session: AsyncSession):
    svc = BooksService(session)
    result = await svc.get_by_id(999999)
    assert result is None


@pytest.mark.asyncio
async def test_get_by_author_positive_and_degenerate(session: AsyncSession):
    # Arrange
    await _seed_authors_and_books(session)
    svc = BooksService(session)

    # Positive: author 1 has two books
    books_a1 = await svc.get_by_author(1)
    assert isinstance(books_a1, list)
    assert len(books_a1) == 2
    titles = {b.title for b in books_a1}
    assert "The Hobbit" in titles
    assert "Another Tolkien" in titles

    # New: ensure each returned book includes its author and that the FK matches
    for b in books_a1:
        assert b.author is not None
        assert b.author.id == 1
        assert b.author.first_name == "J.R.R." or b.author.first_name == "J.R.R."  # simple sanity

    # Positive: author 2 has one book
    books_a2 = await svc.get_by_author(2)
    assert len(books_a2) == 1
    assert books_a2[0].title == "1984"
    assert books_a2[0].author is not None
    assert books_a2[0].author.id == 2
    assert books_a2[0].author.last_name == "Orwell"

    # Degenerate: existing author with no books
    await _clear_tables(session)
    lonely = Author(id=10, first_name="Lonely", last_name="Author")
    session.add(lonely)
    await session.commit()

    books_lonely = await svc.get_by_author(10)
    assert books_lonely == []

    # Non-existent author returns empty list (service queries books table)
    books_none = await svc.get_by_author(999999)
    assert books_none == []

