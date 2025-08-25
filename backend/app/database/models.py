from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


class Author(SQLModel, table=True):
    """
    Represents an author of books.
    """

    id: int = Field(primary_key=True, index=True)
    first_name: str
    last_name: str
    biography: Optional[str] = None


class User(SQLModel, table=True):
    """
    Represents a customer or user of the bookstore.
    """

    id: int = Field(primary_key=True, index=True)
    first_name: str
    last_name: str
    email: EmailStr = Field(unique=True)
    password_hash: str
    created_at: datetime


class Book(SQLModel, table=True):
    """
    Represents an individual book product.
    """

    id: int = Field(primary_key=True, index=True)
    title: str
    author_id: int
    isbn: str
    price: Decimal
    published_date: datetime
    description: Optional[str] = None
    stock_quantity: int
    cover_image_url: Optional[str] = None


class Review(SQLModel, table=True):
    """
    Represents a review for a specific book.
    """

    id: int = Field(primary_key=True, index=True)
    book_id: int = Field(foreign_key="book.id")
    user_id: int = Field(foreign_key="user.id")
    # Rating to be expressed in stars, must be between 1 and 5
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    created_at: datetime


class OrderItem(SQLModel, table=True):
    """
    Represents an individual book within an order. This is a junction model.
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    order_id: int = Field(foreign_key="order.id")
    book_id: int = Field(foreign_key="book.id")
    quantity: int = Field(..., gt=0)  # Quantity must be greater than 0
    price_at_purchase: Decimal

    order: "Order" = Relationship(back_populates="items")


class Order(SQLModel, table=True):
    """
    Represents a customer's purchase.
    """

    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    order_date: datetime
    total_price: Decimal
    status: str
    items: List[OrderItem] = Relationship(
        back_populates="order", sa_relationship_kwargs={"cascade": "all, delete"}
    )
