import asyncio
from datetime import datetime
from decimal import Decimal

import pytest
import pytest_asyncio
from sqlmodel import SQLModel, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database.models import User, Book, Order, OrderItem
from app.services.orders import OrdersService


# Use a true in-memory SQLite database for tests (aiosqlite-based driver)
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="module")
async def async_engine():
    engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, future=True)
    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(async_engine):
    """Provide a fresh AsyncSession for each test (transaction-scoped)."""
    async_session_maker = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_maker() as session:
        yield session
        # rollback any leftover changes to keep tests isolated
        await session.rollback()


async def _clear_tables(session: AsyncSession):
    """Remove all rows from tables used by tests to guarantee a clean slate."""
    # Order of deletes matters because of FK constraints: children first.
    await session.execute(text("DELETE FROM orderitem"))
    await session.execute(text("DELETE FROM 'order'"))
    await session.execute(text("DELETE FROM book"))
    await session.execute(text("DELETE FROM 'user'"))
    await session.commit()


async def _seed_minimal(session: AsyncSession):
    """Clear tables, then insert minimal dataset: one user, two books, two orders (one with items)."""
    await _clear_tables(session)

    user = User(
        id=1,
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password_hash="hash",
        created_at=datetime.utcnow(),
    )
    book1 = Book(
        id=100,
        title="Book 1",
        author_id=1,
        isbn="isbn-100",
        price=Decimal("9.99"),
        published_date=datetime.utcnow(),
        stock_quantity=10,
    )
    book2 = Book(
        id=101,
        title="Book 2",
        author_id=1,
        isbn="isbn-101",
        price=Decimal("12.50"),
        published_date=datetime.utcnow(),
        stock_quantity=5,
    )
    # Order 1: has items
    order1 = Order(
        id=1000,
        user_id=1,
        order_date=datetime.utcnow(),
        total_price=Decimal("9.99"),
        status="New",
    )
    item1 = OrderItem(
        id=5000,
        order_id=1000,
        book_id=100,
        quantity=1,
        price_at_purchase=Decimal("9.99"),
    )
    # Order 2: no items (degenerate)
    order2 = Order(
        id=1001,
        user_id=1,
        order_date=datetime.utcnow(),
        total_price=Decimal("0.00"),
        status="New",
    )

    session.add_all([user, book1, book2, order1, item1, order2])
    await session.commit()
    # refresh to ensure relationships load correctly later if needed
    await session.refresh(order1)
    await session.refresh(order2)


@pytest.mark.asyncio
async def test_get_all_and_get_by_user_and_by_id(session: AsyncSession):
    # Arrange
    await _seed_minimal(session)
    svc = OrdersService(session)

    # Act
    all_orders = await svc.get_all()
    user_orders = await svc.get_by_user(1)
    order_by_id = await svc.get_by_id(1000)

    # Assert
    assert isinstance(all_orders, list)
    assert len(all_orders) >= 2  # both seeded orders present
    assert len(user_orders) >= 2
    assert order_by_id is not None
    assert order_by_id.id == 1000
    assert order_by_id.user_id == 1


@pytest.mark.asyncio
async def test_get_by_id_not_found(session: AsyncSession):
    svc = OrdersService(session)

    result = await svc.get_by_id(999999)
    assert result is None


@pytest.mark.asyncio
async def test_cancel_order_success_and_not_found(session: AsyncSession):
    # Arrange - ensure seed exists
    await _seed_minimal(session)
    svc = OrdersService(session)

    # Cancel existing order
    cancelled = await svc.cancel(1000)
    assert cancelled is not None
    assert cancelled.status == "Cancelled"

    # Cancel non-existent order returns None
    none_cancel = await svc.cancel(999999)
    assert none_cancel is None


@pytest.mark.asyncio
async def test_get_items_positive_and_degenerate(session: AsyncSession):
    # Arrange: seed once
    await _seed_minimal(session)
    svc = OrdersService(session)

    # Order 1000 has one item
    items = await svc.get_items(1000)
    assert items is not None
    assert isinstance(items, list)
    assert len(items) == 1
    assert items[0].book_id == 100

    # Order 1001 has no items (degenerate)
    items_empty = await svc.get_items(1001)
    assert items_empty == []  # relationship returns empty list for no items

    # Non-existent order returns None
    items_none = await svc.get_items(999999)
    assert items_none is None


@pytest.mark.asyncio
async def test_create_not_implemented(session: AsyncSession):
    svc = OrdersService(session)
    with pytest.raises(NotImplementedError):
        await svc.create(1)
