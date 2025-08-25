from typing import List, Annotated

from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Author, Book
from app.database.session import SessionDep


class AuthorsService:
    """Encapsulate DB operations for authors."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> List[Author]:
        """Return all authors."""
        result = await self._session.execute(select(Author))
        return result.scalars().all()

    async def get_by_id(self, author_id: int) -> Author | None:
        """Return an author by id or None if not found."""
        return await self._session.get(Author, author_id)

    async def get_books_for_author(self, author_id: int) -> List[Book]:
        """Return books written by the specified author."""
        stmt = select(Book).where(Book.author_id == author_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()


async def get_authors_service(session: SessionDep) -> AuthorsService:
    """
    Dependency factory for AuthorsService.

    Usage in routes:
      svc: AuthorsService = Depends(get_authors_service)
    """
    return AuthorsService(session)


# Typing helper for route parameters:
AuthorsServiceDep = Annotated[AuthorsService, Depends(get_authors_service)]
