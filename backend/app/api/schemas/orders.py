from typing import List

from pydantic import BaseModel


# DTOs for orders
class OrderElement(BaseModel):
    book_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderElement]
