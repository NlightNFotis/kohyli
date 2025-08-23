from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# Using a custom type for decimal to ensure precision
from decimal import Decimal


# --- Core Models ---

class Author(BaseModel):
    """
    Represents an author of books.
    """
    id: int
    first_name: str
    last_name: str
    biography: Optional[str] = None


class User(BaseModel):
    """
    Represents a customer or user of the bookstore.
    """
    id: int
    first_name: str
    last_name: str
    email: str
    password_hash: str
    created_at: datetime


class Book(BaseModel):
    """
    Represents an individual book product.
    """
    id: int
    title: str
    author_id: int
    isbn: str
    price: Decimal
    published_date: datetime
    description: Optional[str] = None
    stock_quantity: int
    cover_image_url: Optional[str] = None


class Review(BaseModel):
    """
    Represents a review for a specific book.
    """
    id: int
    book_id: int
    user_id: int
    rating: int = Field(..., ge=1, le=5)  # Rating must be between 1 and 5
    comment: Optional[str] = None
    created_at: datetime


class OrderItem(BaseModel):
    """
    Represents an individual book within an order. This is a junction model.
    """
    id: int
    order_id: int
    book_id: int
    quantity: int = Field(..., gt=0)  # Quantity must be greater than 0
    price_at_purchase: Decimal


class Order(BaseModel):
    """
    Represents a customer's purchase.
    """
    id: int
    user_id: int
    order_date: datetime
    total_price: Decimal
    status: str
    items: List[OrderItem] = []  # A list of items in the order
