from typing import List

from fastapi import APIRouter, HTTPException

from app.database.models import Book
from app.services.books import BooksServiceDep

books_router = APIRouter(prefix="/books")


@books_router.get("/")
async def get_all_books(books_service: BooksServiceDep) -> List[Book]:
    """Retrieve all books available in our store."""
    books: List[Book] = await books_service.get_all()
    return [b.model_dump() for b in books]


@books_router.get("/{book_id}")
async def get_book(book_id: int, books_service: BooksServiceDep) -> Book:
    """Retrieve a specific book, by id, from the database."""
    book = await books_service.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    return book.model_dump()
