from typing import List

from fastapi import APIRouter, HTTPException

from app.database.models import Book, Author

from app.services.authors import AuthorsServiceDep
from app.services.books import BooksServiceDep

from .routers.orders import orders_router
from .routers.users import users_router

router = APIRouter()

combined_router = APIRouter()
combined_router.include_router(router)
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


@router.get("/authors")
async def get_all_authors(authors_service: AuthorsServiceDep) -> List[Author]:
    """Retrieve all the authors available in our store."""
    authors: List[Author] = await authors_service.get_all()
    return [a.model_dump() for a in authors]


@router.get("/authors/{id}")
async def get_author(id: int, authors_service: AuthorsServiceDep) -> Author:
    """Retrieve a specific author, by id, from the database."""
    author = await authors_service.get_by_id(id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")

    return author.model_dump()


@router.get("/authors/{id}/books")
async def get_author_books(author_id: int, authors_service: AuthorsServiceDep) -> List[Book]:
    """Retrieve all books by an author, by id, from the database."""
    books = await authors_service.get_books_for_author(author_id)
    return [b.model_dump() for b in books]


