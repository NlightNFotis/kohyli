from typing import List

from fastapi import APIRouter, HTTPException

from app.database.models import Book

from app.services.books import BooksServiceDep

from .routers.authors import authors_router
from .routers.orders import orders_router
from .routers.users import users_router

router = APIRouter()

combined_router = APIRouter()
combined_router.include_router(router)
combined_router.include_router(authors_router)
combined_router.include_router(users_router)
combined_router.include_router(orders_router)

@router.get("/")
def root():
    """A simple welcome message (and online status)."""
    return {"message": "Welcome to Vivliopoleio Kohyli."}


@router.get("/books")
async def get_all_books(books_service: BooksServiceDep) -> List[Book]:
    """Retrieve all books available in our store."""
    books: List[Book] = await books_service.get_all()
    return [b.model_dump() for b in books]


@router.get("/books/{id}")
async def get_book(id: int, books_service: BooksServiceDep) -> Book:
    """Retrieve a specific book, by id, from the database."""
    book = await books_service.get_by_id(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    return book.model_dump()





