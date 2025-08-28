from datetime import datetime, timezone, timedelta
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
        stmt = (
            select(Book)
            .options(selectinload(Book.author))
            .where(Book.author_id == author_id)
        )
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

        # Default to current UTC month if not specified (use naive UTC times to match model datetimes)
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

        # First, aggregate sold quantities per book_id for completed orders within the month.
        # Aggregate on OrderItem.book_id to avoid GROUP BY issues when selecting full Book entity.
        agg_stmt = (
            select(OrderItem.book_id, func.sum(OrderItem.quantity).label("units_sold"))
            .join(Order, Order.id == OrderItem.order_id)
            .where(
                # We want to take into account in-flight orders as well.
                (Order.status == "Created") | (Order.status == "Completed"),
                Order.order_date >= start,
                Order.order_date < end,
            )
            .group_by(OrderItem.book_id)
            .order_by(desc(func.sum(OrderItem.quantity)))
            .limit(limit)
        )

        agg_result = await self._session.execute(agg_stmt)
        agg_rows = agg_result.all()  # list of (book_id, units_sold)
        if not agg_rows:
            return []

        # Preserve ordering from aggregation
        book_ids = [row[0] for row in agg_rows]

        # Fetch the Book objects for these ids (load authors too)
        books_stmt = (
            select(Book).options(selectinload(Book.author)).where(Book.id.in_(book_ids))
        )
        books_result = await self._session.execute(books_stmt)
        books = books_result.scalars().all()

        # Map books by id for quick lookup
        books_by_id = {b.id: b for b in books}

        # Reassemble ordered list of (Book, units_sold)
        bestsellers: List[Tuple[Book, int]] = []
        for book_id, units in agg_rows:
            book_obj = books_by_id.get(book_id)
            if book_obj is None:
                # skip if book record not found for some reason
                continue
            units_count = int(units) if units is not None else 0
            bestsellers.append((book_obj, units_count))

        return bestsellers

    async def get_new_arrivals(
        self, days: int = 30, limit: Optional[int] = 10
    ) -> List[Book]:
        """
        Return books published within the last `days` days (default 30).
        Results are ordered by published_date descending and authors are loaded.
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        stmt = (
            select(Book)
            .options(selectinload(Book.author))
            .where(Book.published_date >= cutoff)
            .order_by(desc(Book.published_date))
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        return result.scalars().all()


async def get_books_service(session: SessionDep) -> BooksService:
    """Dependency factory that returns a BooksService bound to the provided session."""
    return BooksService(session)


# Typing helper for route parameter annotations:
BooksServiceDep = Annotated[BooksService, Depends(get_books_service)]
