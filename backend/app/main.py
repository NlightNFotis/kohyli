from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.database.models import Book
from app.database.session import create_tables, get_session, SessionDep


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Anything that happens before the yield happens before the app starts
    create_tables()

    yield

    # And anything that happens after the yield happens after the app stops
    return


app = FastAPI(
    title="Kohyli Bookstore",
    description="A simple API for a bookstore.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    """A simple welcome message (and online status)."""
    return {"message": "Welcome to Vivliopoleio Kohyli."}


@app.get("/book")
def get_book(id: int, session: SessionDep) -> Book:
    """Retrieve all the products in the in-memory database."""
    book = session.get(Book, id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    return book.model_dump()
