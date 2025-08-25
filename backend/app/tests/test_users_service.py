import pytest
import pytest_asyncio
from datetime import datetime
from decimal import Decimal

from sqlmodel import SQLModel, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.api.schemas.users import UserCreate
from app.database.models import User, Order
from app.services.users import UsersService

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
    """Delete rows from tables used by these tests (children first)."""
    # order -> depends on user via foreign key
    await session.execute(text("DELETE FROM 'order'"))
    await session.execute(text("DELETE FROM 'user'"))
    await session.commit()


async def _seed_users_and_orders(session: AsyncSession):
    """Clear tables then insert sample users and orders."""
    await _clear_tables(session)

    u1 = User(
        id=1,
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        password_hash="hash1",
        created_at=datetime.now(),
    )
    u2 = User(
        id=2,
        first_name="Bob",
        last_name="Jones",
        email="bob@example.com",
        password_hash="hash2",
        created_at=datetime.now(),
    )

    o1 = Order(
        id=2001,
        user_id=1,
        order_date=datetime.now(),
        total_price=Decimal("20.00"),
        status="New",
    )
    o2 = Order(
        id=2002,
        user_id=1,
        order_date=datetime.now(),
        total_price=Decimal("5.00"),
        status="Shipped",
    )
    o3 = Order(
        id=2003,
        user_id=2,
        order_date=datetime.now(),
        total_price=Decimal("12.00"),
        status="New",
    )

    session.add_all([u1, u2, o1, o2, o3])
    await session.commit()
    await session.refresh(u1)
    await session.refresh(u2)


@pytest.mark.asyncio
async def test_get_all_and_get_by_id(session: AsyncSession):
    # Arrange
    await _seed_users_and_orders(session)
    svc = UsersService(session)

    # Act
    all_users = await svc.get_all()
    user1 = await svc.get_by_id(1)
    user2 = await svc.get_by_id(2)

    # Assert
    assert isinstance(all_users, list)
    assert len(all_users) >= 2
    assert user1 is not None
    assert user1.email == "alice@example.com"
    assert user2 is not None
    assert user2.first_name == "Bob"


@pytest.mark.asyncio
async def test_get_by_id_not_found(session: AsyncSession):
    svc = UsersService(session)
    result = await svc.get_by_id(999999)
    assert result is None


@pytest.mark.asyncio
async def test_create_user_success(session: AsyncSession):
    # Arrange
    await _clear_tables(session)
    svc = UsersService(session)
    new_user_data = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="somehash"
    )

    # Act
    created_user = await svc.create(new_user_data)

    # Assert
    assert created_user is not None
    assert created_user.id is not None
    assert created_user.first_name == "John"
    assert created_user.email == "john@example.com"
    assert created_user.created_at is not None


@pytest.mark.asyncio
async def test_create_user_duplicate_email(session: AsyncSession):
    # Arrange
    await _seed_users_and_orders(session)
    svc = UsersService(session)
    duplicate_user = UserCreate(
        first_name="Another",
        last_name="User",
        email="alice@example.com",  # Already exists
        password="hash"
    )

    # Act & Assert
    with pytest.raises(IntegrityError):
        await svc.create(duplicate_user)


@pytest.mark.asyncio
async def test_create_user_invalid_data(session: AsyncSession):
    # Arrange
    await _clear_tables(session)
    svc = UsersService(session)

    # Act & Assert
    with pytest.raises(ValueError):
        invalid_user = UserCreate(
            first_name="",  # Empty first name
            last_name="Test",
            email="invalid",  # Invalid email
            password=""  # Empty password
        )

        await svc.create(invalid_user)


@pytest.mark.asyncio
async def test_get_by_email_positive_and_not_found(session: AsyncSession):
    # Arrange
    await _seed_users_and_orders(session)
    svc = UsersService(session)

    # Positive
    u = await svc.get_by_email("alice@example.com")
    assert u is not None
    assert u.id == 1
    assert u.first_name == "Alice"

    # Not found
    none_u = await svc.get_by_email("noone@example.com")
    assert none_u is None


@pytest.mark.asyncio
async def test_get_orders_for_user_positive_and_degenerate(session: AsyncSession):
    # Arrange
    await _seed_users_and_orders(session)
    svc = UsersService(session)

    # Positive: user 1 has two orders
    orders_u1 = await svc.get_orders_for_user(1)
    assert isinstance(orders_u1, list)
    assert len(orders_u1) == 2
    ids = {o.id for o in orders_u1}
    assert 2001 in ids and 2002 in ids

    # Degenerate: existing user with no orders
    # create a user with no orders
    await _clear_tables(session)
    lonely = User(
        id=10,
        first_name="Lonely",
        last_name="User",
        email="lonely@example.com",
        password_hash="hash",
        created_at=datetime.now(),
    )
    session.add(lonely)
    await session.commit()

    orders_lonely = await svc.get_orders_for_user(10)
    assert orders_lonely == []

    # Non-existent user id: service queries orders table and should return empty list
    orders_none = await svc.get_orders_for_user(999999)
    assert orders_none == []

