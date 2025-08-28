import pytest
import pytest_asyncio
from datetime import datetime, timezone
from decimal import Decimal

from sqlmodel import SQLModel, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database.models import Author, Book, Order, OrderItem, User
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
    # Delete child tables first to avoid FK constraint violations.
    # OrderItem table is named "orderitem" by SQLModel (class name lowercased),
    # and it references order and book; order references user; book references author.
    # "order" and "user" are quoted because they are reserved/special identifiers.
    await session.execute(text("DELETE FROM orderitem"))
    await session.execute(text('DELETE FROM "order"'))
    await session.execute(text('DELETE FROM "user"'))
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
        assert (
            b.author.first_name == "J.R.R." or b.author.first_name == "J.R.R."
        )  # simple sanity

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


# ---------- Helpers for get_monthly_bestsellers tests ----------


async def _seed_bestsellers_data(session: AsyncSession, year: int, month: int):
    """
    Seed data for bestseller tests:
    - 3 books (200, 201, 202)
    - Multiple 'completed' orders within target month, giving:
        book 200 -> 5 units (top)
        book 201 -> 1 unit
        book 202 -> 0 units
    - A cancelled order within the month that should be ignored
    - A completed order in the next month that should be ignored
    """
    await _clear_tables(session)

    def dt(y: int, m: int, d: int) -> datetime:
        return datetime(y, m, d, 12, 0, 0)

    # Compute next month for out-of-range data
    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)

    user = User(
        id=2,
        first_name="Buyer",
        last_name="Two",
        email="buyer2@example.com",
        password_hash="hash",
        created_at=datetime.now(timezone.utc),
    )
    b200 = Book(
        id=200,
        title="Top Seller",
        author_id=1,
        isbn="isbn-200",
        price=Decimal("15.00"),
        published_date=datetime.now(timezone.utc),
        stock_quantity=100,
    )
    b201 = Book(
        id=201,
        title="Second Seller",
        author_id=1,
        isbn="isbn-201",
        price=Decimal("20.00"),
        published_date=datetime.now(timezone.utc),
        stock_quantity=100,
    )
    b202 = Book(
        id=202,
        title="No Sales",
        author_id=1,
        isbn="isbn-202",
        price=Decimal("8.00"),
        published_date=datetime.now(timezone.utc),
        stock_quantity=100,
    )

    # Completed orders inside the month
    o1 = Order(
        id=2000,
        user_id=2,
        order_date=dt(year, month, 15),
        total_price=Decimal("75.00"),
        status="Completed",
    )
    o2 = Order(
        id=2001,
        user_id=2,
        order_date=dt(year, month, 20),
        total_price=Decimal("30.00"),
        status="Completed",
    )

    # Cancelled order in month (ignored)
    o3 = Order(
        id=2002,
        user_id=2,
        order_date=dt(year, month, 10),
        total_price=Decimal("100.00"),
        status="Cancelled",
    )

    # Completed order in next month (ignored)
    o4 = Order(
        id=2003,
        user_id=2,
        order_date=dt(next_year, next_month, 5),
        total_price=Decimal("200.00"),
        status="Completed",
    )

    oi1 = OrderItem(
        id=6000,
        order_id=2000,
        book_id=200,
        quantity=3,
        price_at_purchase=Decimal("15.00"),
    )
    oi2 = OrderItem(
        id=6001,
        order_id=2001,
        book_id=200,
        quantity=2,
        price_at_purchase=Decimal("15.00"),
    )
    oi3 = OrderItem(
        id=6002,
        order_id=2000,
        book_id=201,
        quantity=1,
        price_at_purchase=Decimal("20.00"),
    )
    # Items on cancelled order (ignored)
    oi4 = OrderItem(
        id=6003,
        order_id=2002,
        book_id=201,
        quantity=5,
        price_at_purchase=Decimal("20.00"),
    )
    # Items in next month (ignored)
    oi5 = OrderItem(
        id=6004,
        order_id=2003,
        book_id=201,
        quantity=10,
        price_at_purchase=Decimal("20.00"),
    )

    session.add_all([user, b200, b201, b202, o1, o2, o3, o4, oi1, oi2, oi3, oi4, oi5])
    await session.commit()


async def _seed_completed_no_items(session: AsyncSession, year: int, month: int):
    """Seed a 'completed' order within the month but without any items."""
    await _clear_tables(session)
    user = User(
        id=3,
        first_name="Buyer",
        last_name="Three",
        email="buyer3@example.com",
        password_hash="hash",
        created_at=datetime.now(timezone.utc),
    )
    book = Book(
        id=300,
        title="Lonely Book",
        author_id=1,
        isbn="isbn-300",
        price=Decimal("5.00"),
        published_date=datetime.now(timezone.utc),
        stock_quantity=100,
    )
    o = Order(
        id=3000,
        user_id=3,
        order_date=datetime(year, month, 12, 10, 0, 0),
        total_price=Decimal("0.00"),
        status="completed",
    )
    session.add_all([user, book, o])
    await session.commit()


# ---------- Tests for get_monthly_bestsellers ----------


@pytest.mark.asyncio
async def test_get_monthly_bestsellers_positive_ordering_and_limit(
    session: AsyncSession,
):
    now = datetime.now(timezone.utc)
    year, month = now.year, now.month
    await _seed_bestsellers_data(session, year, month)

    svc = BooksService(session)
    result = await svc.get_monthly_bestsellers(year=year, month=month, limit=2)

    assert isinstance(result, list)
    # Expect only top 2 books
    assert len(result) == 2

    # Top seller should be book 200 with 5 units
    top_book, top_units = result[0]
    assert top_book.id == 200
    assert top_units == 5

    # Second should be book 201 with 1 unit
    second_book, second_units = result[1]
    assert second_book.id == 201
    assert second_units == 1


@pytest.mark.asyncio
async def test_get_monthly_bestsellers_negative_no_results(session: AsyncSession):
    now = datetime.now(timezone.utc)
    year, month = now.year, now.month

    # Seed only orders outside the requested month or with non-completed status
    await _clear_tables(session)

    # Create a user and a completed order in the previous month to ensure no matches
    prev_year, prev_month = (year - 1, 12) if month == 1 else (year, month - 1)
    user = User(
        id=4,
        first_name="Buyer",
        last_name="Four",
        email="buyer4@example.com",
        password_hash="hash",
        created_at=datetime.now(timezone.utc),
    )
    book = Book(
        id=400,
        title="Other Month Book",
        author_id=1,
        isbn="isbn-400",
        price=Decimal("10.00"),
        published_date=datetime.now(timezone.utc),
        stock_quantity=100,
    )
    o_prev = Order(
        id=4000,
        user_id=4,
        order_date=datetime(prev_year, prev_month, 10, 9, 0, 0),
        total_price=Decimal("10.00"),
        status="completed",
    )
    oi_prev = OrderItem(
        id=7000,
        order_id=4000,
        book_id=400,
        quantity=2,
        price_at_purchase=Decimal("10.00"),
    )
    # Non-completed order inside the month
    o_non_completed = Order(
        id=4001,
        user_id=4,
        order_date=datetime(year, month, 11, 9, 0, 0),
        total_price=Decimal("10.00"),
        status="New",
    )
    session.add_all([user, book, o_prev, oi_prev, o_non_completed])
    await session.commit()

    svc = BooksService(session)
    result = await svc.get_monthly_bestsellers(year=year, month=month, limit=10)

    assert result == []


@pytest.mark.asyncio
async def test_get_monthly_bestsellers_degenerate_limit_zero_and_no_items(
    session: AsyncSession,
):
    now = datetime.now(timezone.utc)
    year, month = now.year, now.month

    # Case A: limit = 0 yields empty list even when data exists
    await _seed_bestsellers_data(session, year, month)
    svc = BooksService(session)
    result_limit_zero = await svc.get_monthly_bestsellers(
        year=year, month=month, limit=0
    )
    assert result_limit_zero == []

    # Case B: completed order without items yields empty aggregation
    await _seed_completed_no_items(session, year, month)
    result_no_items = await svc.get_monthly_bestsellers(
        year=year, month=month, limit=10
    )
    assert result_no_items == []
