from typing import List

from fastapi import APIRouter, HTTPException

from app.api.schemas.books_authors import BookRead
from app.database.models import Book
from app.services.books import BooksServiceDep

books_router = APIRouter(prefix="/books")


@books_router.get("", response_model=List[BookRead])
async def get_all_books(books_service: BooksServiceDep) -> List[BookRead]:
    """Retrieve all books available in our store."""
    books: List[Book] = await books_service.get_all()
    # convert the ORM instances into DTO instances
    return [BookRead(**b.model_dump()) for b in books]



@books_router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, books_service: BooksServiceDep) -> BookRead:
    """Retrieve a specific book, by id, from the database."""
    book: Book | None = await books_service.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    return BookRead(**book.model_dump())
