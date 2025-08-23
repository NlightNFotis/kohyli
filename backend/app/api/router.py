from fastapi import APIRouter, HTTPException

from app.database.models import Book
from app.database.session import SessionDep

router = APIRouter()


@router.get("/")
def root():
    """A simple welcome message (and online status)."""
    return {"message": "Welcome to Vivliopoleio Kohyli."}


@router.get("/book")
async def get_book(id: int, session: SessionDep) -> Book:
    """Retrieve all the products in the in-memory database."""
    book = await session.get(Book, id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    return book.model_dump()
