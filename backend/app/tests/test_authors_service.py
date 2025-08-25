import pytest
import pytest_asyncio
from datetime import datetime
from decimal import Decimal

from sqlmodel import SQLModel, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database.models import Author, Book
from app.services.authors import AuthorsService

# Use an in-memory SQLite DB for tests
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="module")
async def async_engine():
    engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, future=True)
    # create tables once for the module
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
        # ensure the session is clean for next test
        await session.rollback()


async def _clear_tables(session: AsyncSession):
    """Delete rows from tables used by these tests (children first)."""
    await session.execute(text("DELETE FROM book"))
    await session.execute(text("DELETE FROM author"))
    await session.commit()


async def _seed_authors_and_books(session: AsyncSession):
    """Clear tables then insert a couple of authors and books for testing."""
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
        title="Unrelated Book",
        author_id=999,  # author that does not exist in authors table
        isbn="isbn-999",
        price=Decimal("5.00"),
        published_date=datetime.utcnow(),
        stock_quantity=1,
    )

    session.add_all([a1, a2, b1, b2, b3])
    await session.commit()
    await session.refresh(a1)
    await session.refresh(a2)


@pytest.mark.asyncio
async def test_get_all_and_get_by_id(session: AsyncSession):
    # Arrange
    await _seed_authors_and_books(session)
    svc = AuthorsService(session)

    # Act
    all_authors = await svc.get_all()
    author1 = await svc.get_by_id(1)
    author2 = await svc.get_by_id(2)

    # Assert
    assert isinstance(all_authors, list)
    assert len(all_authors) >= 2
    assert author1 is not None
    assert author1.first_name == "J.R.R."
    assert author2 is not None
    assert author2.last_name == "Orwell"


@pytest.mark.asyncio
async def test_get_by_id_not_found(session: AsyncSession):
    svc = AuthorsService(session)

    result = await svc.get_by_id(999999)
    assert result is None


@pytest.mark.asyncio
async def test_get_books_for_author_positive_and_degenerate(session: AsyncSession):
    # Arrange: seed authors and books
    await _seed_authors_and_books(session)
    svc = AuthorsService(session)

    # Positive: author 1 (Tolkien) has The Hobbit
    books_a1 = await svc.get_books_for_author(1)
    assert isinstance(books_a1, list)
    assert len(books_a1) == 1
    assert books_a1[0].title == "The Hobbit"
    assert books_a1[0].author_id == 1

    # Positive: author 2 (Orwell) has 1984
    books_a2 = await svc.get_books_for_author(2)
    assert len(books_a2) == 1
    assert books_a2[0].title == "1984"

    # Degenerate: existing author with no books
    # Create an author with no books
    await _clear_tables(session)
    author_lonely = Author(id=10, first_name="Lonely", last_name="Author")
    session.add(author_lonely)
    await session.commit()
    books_lonely = await svc.get_books_for_author(10)
    assert books_lonely == []

    # Non-existent author id returns empty list (service queries books table)
    books_none = await svc.get_books_for_author(999999)
    assert books_none == []
