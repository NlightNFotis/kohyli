from typing import List

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.database.models import Book, Author
from app.database.session import SessionDep

router = APIRouter()


@router.get("/")
def root():
    """A simple welcome message (and online status)."""
    return {"message": "Welcome to Vivliopoleio Kohyli."}


@router.get("/books")
async def get_all_books(session: SessionDep) -> List[Book]:
    """Retrieve all books available in our store."""
    result = await session.execute(select(Book))
    books: List[Book] = result.scalars().all()
    return [b.model_dump() for b in books]


@router.get("/books/{id}")
async def get_book(id: int, session: SessionDep) -> Book:
    """Retrieve a specific book, by id, from the database."""
    book = await session.get(Book, id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    return book.model_dump()


@router.get("/authors")
async def get_all_authors(session: SessionDep) -> List[Author]:
    """Retrieve all the authors available in our store."""
    result = await session.execute(select(Author))
    authors: List[Author] = result.scalars().all()
    return [a.model_dump() for a in authors]
