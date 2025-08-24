from typing import List

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.database.models import Book, Author, User, Order
from app.database.session import SessionDep
from app.services.orders import OrdersServiceDep

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


@router.get("/authors/{id}")
async def get_author(id: int, session: SessionDep) -> Author:
    """Retrieve a specific author, by id, from the database."""
    author = await session.get(Author, id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")

    return author.model_dump()


@router.get("/authors/{id}/books")
async def get_author_books(id: int, session: SessionDep) -> List[Book]:
    """Retrieve all books by an author, by id, from the database."""
    author = await session.get(Author, id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")

    stmt = select(Book).where(Book.author_id == id)
    result = await session.execute(stmt)

    books = result.scalars().all()
    return [b.model_dump() for b in books]


@router.get("/users")
async def get_all_users(session: SessionDep) -> List[User]:
    """Retrieve all users from the database."""
    result = await session.execute(select(User))
    users: List[User] = result.scalars().all()
    return [u.model_dump() for u in users]


@router.get("/users/{id}")
async def get_user(id: int, session: SessionDep) -> User:
    """Retrieve a specific user, by id, from the database."""
    user = await session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.model_dump()


@router.get("/users/email/{email}")
async def get_user_by_email(email: str, session: SessionDep) -> User:
    """Retrieve a specific user by their email address."""
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.model_dump()


@router.get("/users/{id}/orders")
async def get_user_orders(id: int, session: SessionDep) -> List[Order]:
    """Retrieve all orders for a specific user."""
    user = await session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    stmt = select(Order).where(Order.user_id == id)
    result = await session.execute(stmt)
    orders = result.scalars().all()
    return [o.model_dump() for o in orders]


@router.get("/orders")
async def get_all_orders(orders_service: OrdersServiceDep) -> List[Order]:
    """Retrieve all orders from the database."""
    orders = await orders_service.get_all()
    return [o.model_dump() for o in orders]


# TODO: This needs to take in a list of books, but we need to see
# how to pass them in from the frontend. Probably needs to take it
# in the request body, but we may need a new Pydantic model for that.
@router.post("/orders/{user_id}")
async def create_order(user_id: int, orders_service: OrdersServiceDep) -> Order:
    """Create a new order for a specific user."""
    raise NotImplementedError

    orders_service.create(user_id)
    # TODO

@router.get("/orders/{id}")
async def get_order(id: int, orders_service: OrdersServiceDep) -> Order:
    """Retrieve a specific order by id."""
    order = await orders_service.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order.model_dump()


@router.patch("/orders/{id}/cancel")
async def cancel_order(id: int, orders_service: OrdersServiceDep) -> Order:
    """Cancel an order by id."""
    order = await orders_service.cancel(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order.model_dump()


@router.get("/orders/{id}/items")
async def get_order_items(id: int, orders_service: OrdersServiceDep) -> List[Book]:
    """Retrieve all items for a specific order."""
    items = await orders_service.get_items(id)
    if not items:
        raise HTTPException(status_code=404, detail="Order not found.")

    # TODO: This is a OrdersItem - should we convert to book
    return [b.model_dump() for b in items]
