"""Integration test for order creation with email confirmation."""

import asyncio
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database.models import User, Book, Author
from app.services.orders import OrdersService
from app.api.schemas.orders import OrderElement

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


@pytest.mark.asyncio
async def test_order_creation_enqueues_email(session: AsyncSession):
    """Test that creating an order enqueues an email confirmation task."""
    # Arrange - Create test data
    author = Author(
        id=1,
        first_name="F. Scott",
        last_name="Fitzgerald",
        biography="American novelist",
    )
    session.add(author)

    user = User(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password_hash="hashed_password",
        created_at=datetime.utcnow(),
    )
    session.add(user)

    book = Book(
        id=100,
        title="The Great Gatsby",
        author_id=1,
        isbn="978-0-7432-7356-5",
        price=Decimal("15.99"),
        published_date=datetime.utcnow(),
        stock_quantity=10,
        description="A classic American novel",
    )
    session.add(book)
    await session.commit()

    # Mock the email enqueue function
    with patch("app.services.orders.enqueue_order_confirmation_email") as mock_enqueue:
        mock_enqueue.return_value = AsyncMock()

        # Act - Create an order
        orders_service = OrdersService(session)
        order_elements = [OrderElement(book_id=100, quantity=2)]
        order = await orders_service.create(user_id=1, elements=order_elements)

        # Assert - Order was created
        assert order is not None
        assert order.user_id == 1
        assert order.total_price == Decimal("31.98")  # 2 * 15.99
        assert order.status == "Created"

        # Assert - Email was enqueued with correct parameters
        mock_enqueue.assert_called_once()
        call_args = mock_enqueue.call_args[1]  # Get keyword arguments
        assert call_args["user_email"] == "john.doe@example.com"
        assert call_args["user_name"] == "John Doe"
        assert call_args["order_id"] == order.id
        assert call_args["total_price"] == str(order.total_price)
        assert len(call_args["items"]) == 1
        assert call_args["items"][0]["title"] == "The Great Gatsby"
        assert call_args["items"][0]["quantity"] == 2
        assert call_args["items"][0]["price_at_purchase"] == "15.99"

        # Verify stock was decremented
        await session.refresh(book)
        assert book.stock_quantity == 8  # 10 - 2
