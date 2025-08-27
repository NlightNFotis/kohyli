from typing import List, Annotated

from fastapi import Depends
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Book
from app.database.session import SessionDep


class BooksService:
    """Encapsulate DB operations for books."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> List[Book]:
        """Return all books."""
        stmt = select(Book).options(selectinload(Book.author))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, book_id: int) -> Book | None:
        """Return a book by id or None if not found."""
        stmt = select(Book).options(selectinload(Book.author)).where(Book.id == book_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    # FOTIS: This is a mirror of books_service.get_books_for_author. We
    # should probably delete one of the two, but let's keep this around
    # for now.
    async def get_by_author(self, author_id: int) -> List[Book]:
        """Return books for a specific author."""
        stmt = select(Book).options(selectinload(Book.author)).where(Book.author_id == author_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()


async def get_books_service(session: SessionDep) -> BooksService:
    """Dependency factory that returns a BooksService bound to the provided session."""
    return BooksService(session)


# Typing helper for route parameter annotations:
BooksServiceDep = Annotated[BooksService, Depends(get_books_service)]
