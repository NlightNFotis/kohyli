from fastapi import APIRouter

from .routers.authors import authors_router
from .routers.books import books_router
from .routers.orders import orders_router
from .routers.users import users_router

router = APIRouter()


@router.get("/")
def root():
    """A simple welcome message (and online status)."""
    return {"message": "Welcome to Vivliopoleio Kohyli."}


combined_router = APIRouter()
combined_router.include_router(router)
combined_router.include_router(authors_router)
combined_router.include_router(books_router)
combined_router.include_router(users_router)
combined_router.include_router(orders_router)
