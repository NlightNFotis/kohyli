from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel

# DTOs for books and authors

class AuthorRead(SQLModel):
    id: int
    first_name: str
    last_name: str
    biography: Optional[str] = None

class BookRead(SQLModel):
    id: int
    title: str
    isbn: str
    price: Decimal
    published_date: datetime
    description: Optional[str] = None
    stock_quantity: int
    cover_image_url: Optional[str] = None
    author: Optional[AuthorRead] = None

class BestSellerRead(SQLModel):
    """
    Response model for a bestseller entry.

    Contains the book DTO and the units_sold for the requested month.
    """
    book: BookRead
    units_sold: int
