from typing import List

from fastapi import APIRouter, HTTPException

from app.database.models import Author, Book
from app.services.authors import AuthorsServiceDep

authors_router = APIRouter(prefix="/authors")


@authors_router.get("")
async def get_all_authors(authors_service: AuthorsServiceDep) -> List[Author]:
    """Retrieve all the authors available in our store."""
    authors: List[Author] = await authors_service.get_all()
    return [a.model_dump() for a in authors]


@authors_router.get("/{id}")
async def get_author(id: int, authors_service: AuthorsServiceDep) -> Author:
    """Retrieve a specific author, by id, from the database."""
    author = await authors_service.get_by_id(id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")

    return author.model_dump()


@authors_router.get("/{author_id}/books")
async def get_author_books(
    author_id: int, authors_service: AuthorsServiceDep
) -> List[Book]:
    """Retrieve all books by an author, by id, from the database."""
    books = await authors_service.get_books_for_author(author_id)
    return [b.model_dump() for b in books]
