from pydantic import BaseModel
import uuid
from typing import List, Optional


class ProductImage(BaseModel):
    """Represents a product image."""

    id: str = str(uuid.uuid4())
    url: str
    alt_text: Optional[str] = None


class ProductVariant(BaseModel):
    """Represents a product variant like size or color."""

    id: str = str(uuid.uuid4())
    type: str  # e.g., "color", "size"
    value: str  # e.g., "red", "medium"
    additional_price: float = 0.0


class Product(BaseModel):
    """Represents a single product in the store."""

    id: str = str(uuid.uuid4())
    name: str
    description: str
    price: float
    stock_quantity: int
    category: str
    images: List[ProductImage] = []
    variants: List[ProductVariant] = []
