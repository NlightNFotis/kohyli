from typing import List, Optional

from fastapi import APIRouter, HTTPException

from app.api.schemas.books_authors import BookRead, BestSellerRead
from app.database.models import Book
from app.services.books import BooksServiceDep

books_router = APIRouter(prefix="/books")


@books_router.get("", response_model=List[BookRead])
async def get_all_books(books_service: BooksServiceDep) -> List[BookRead]:
    """Retrieve all books available in our store."""
    books: List[Book] = await books_service.get_all()
    # convert the ORM instances into DTO instances
    result = []
    for b in books:
        bd = b.model_dump()
        bd["author"] = b.author.model_dump() if getattr(b, "author", None) else None
        result.append(BookRead(**bd))
    return result


@books_router.get("/bestsellers/monthly", response_model=List[BestSellerRead])
async def get_monthly_bestsellers(
    year: Optional[int] = None,
    month: Optional[int] = None,
    limit: int = 10,
    books_service: BooksServiceDep = None,
) -> List[BestSellerRead]:
    """
    Retrieve the top-selling books for a calendar month.
    - year and month are optional (defaults to current UTC month)
    - limit controls how many rows are returned
    """
    # Call the service to get tuples of (Book, units_sold)
    rows = await books_service.get_monthly_bestsellers(year=year, month=month, limit=limit)

    result: List[BestSellerRead] = []
    for book_obj, units in rows:
        # Build book DTO the same way other routes do
        bd = book_obj.model_dump()
        bd["author"] = book_obj.author.model_dump() if getattr(book_obj, "author", None) else None
        book_dto = BookRead(**bd)
        result.append(BestSellerRead(book=book_dto, units_sold=units))

    return result



@books_router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, books_service: BooksServiceDep) -> BookRead:
    """Retrieve a specific book, by id, from the database."""
    book: Book | None = await books_service.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    # Convert the ORM instance into the DTO that the route advertises.
    book_data = book.model_dump()
    book_data["author"] = book.author.model_dump() if getattr(book, "author", None) else None
    return BookRead(**book_data)
