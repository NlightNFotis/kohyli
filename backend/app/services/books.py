from datetime import datetime, timezone
from typing import List, Annotated, Tuple, Optional

from fastapi import Depends
from sqlalchemy import func, desc
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Book, Order, OrderItem
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

    async def get_monthly_bestsellers(
        self, year: Optional[int] = None, month: Optional[int] = None, limit: int = 10
    ) -> List[Tuple[Book, int]]:
        """
        Return top-selling books for a given calendar month.

        - If year or month is None, the current UTC year/month is used.
        - Only orders with status 'completed' are counted.
        - Returns a list of tuples: (Book, units_sold), ordered by units_sold desc.
        """

        # Default to current UTC month if not specified
        now = datetime.now(timezone.utc)
        if year is None:
            year = now.year
        if month is None:
            month = now.month

        # Build month range [start, end)
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)

        # Aggregate sold quantities for completed orders within the month
        stmt = (
            select(Book, func.sum(OrderItem.quantity).label("units_sold"))
            .join(OrderItem, Book.id == OrderItem.book_id)
            .join(Order, OrderItem.order_id == Order.id)
            .where(
                Order.status == "completed",
                Order.order_date >= start,
                Order.order_date < end,
            )
            .group_by(Book.id)
            .order_by(desc(func.sum(OrderItem.quantity)))
            .limit(limit)
            .options(selectinload(Book.author))
        )

        result = await self._session.execute(stmt)
        rows = result.all()  # list of (Book, units_sold)
        # Normalize the aggregated value to int and return as tuples
        bestsellers: List[Tuple[Book, int]] = []
        for book_obj, units in rows:
            units_count = int(units) if units is not None else 0
            bestsellers.append((book_obj, units_count))

        return bestsellers


async def get_books_service(session: SessionDep) -> BooksService:
    """Dependency factory that returns a BooksService bound to the provided session."""
    return BooksService(session)


# Typing helper for route parameter annotations:
BooksServiceDep = Annotated[BooksService, Depends(get_books_service)]
