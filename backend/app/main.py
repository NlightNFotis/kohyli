from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.session import create_tables


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


# Very simple in-memory database for now
products = []


@app.get("/books")
def get_all_products():
    """Retrieve all the products in the in-memory database."""
    return products
