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
        # create tables
        await conn.run_sync(SQLModel.metadata.create_all)

        # seed some initial data (idempotent)
        await conn.exec_driver_sql(
            """
            INSERT OR IGNORE INTO author (id, first_name, last_name, biography) VALUES
                      (1, 'J.R.R.', 'Tolkien', 'Author of The Hobbit and The Lord of the Rings.'),
                      (2, 'George', 'Orwell', 'Author of 1984 and Animal Farm.');
            """
        )

        await conn.exec_driver_sql(
            """
            INSERT OR IGNORE INTO book (
                      id, title, author_id, isbn, price, published_date, description, stock_quantity, cover_image_url
                    ) VALUES
                      (1001, 'The Hobbit', 1, '978-0-618-00221-0', 15.99, '1937-09-21', 'A fantasy novel by J.R.R. Tolkien.', 50, NULL),
                      (1002, '1984', 2, '978-0-452-28423-4', 12.50, '1949-06-08', 'A dystopian social science fiction novel and cautionary tale.', 40, NULL);
            """
        )


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


# Type hinting for the session dependency, which FastAPI
# can leverage to inject the session object into the endpoint.
SessionDep = Annotated[AsyncSession, Depends(get_session)]
