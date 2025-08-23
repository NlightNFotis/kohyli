from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import SQLModel

engine = create_async_engine(
    url="sqlite+aiosqlite:///./kohyli.db",
    # FOTIS: echo commands for now for debugging purposes
    echo=True,
    # We need to disable the check_same_thread flag for SQLite,
    # as otherwise we will get an error when running multiple threads.
    connect_args={"check_same_thread": False},
)


async def create_tables():
    from .models import Book, User, Author, Review, Order, OrderItem

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


# Type hinting for the session dependency, which FastAPI
# can leverage to inject the session object into the endpoint.
SessionDep = Annotated[AsyncSession, Depends(get_session)]
