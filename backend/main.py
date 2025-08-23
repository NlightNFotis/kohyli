from fastapi import FastAPI

app = FastAPI(
    title="Kohyli Bookstore",
    description="A simple API for a bookstore.",
    version="0.1.0",
)


@app.get("/")
def root():
    """A simple welcome message (and online status)."""
    return {"message": "Welcome to Vivliopoleio Kohyli.."}


# Very simple in-memory database for now
products = []


@app.get("/books")
def get_all_products():
    """Retrieve all the products in the in-memory database."""
    return products
