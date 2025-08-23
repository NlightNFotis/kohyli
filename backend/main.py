from typing import Union

from fastapi import FastAPI

app = FastAPI(
    title="Kohyli Artisan Goods E-Shop API",
    description="A simple API for a local artisan goods store from Crete.",
    version="0.1.0",
)


@app.get("/")
def root():
    """A simple welcome message (and online status)."""
    return {"message": "Welcome to Kohyli Artisan Goods E-Shop API."}


# Very simple in-memory database for now
products = []


@app.get("/products")
def get_all_products():
    """Retrieve all the products in the in-memory database."""
    return products
