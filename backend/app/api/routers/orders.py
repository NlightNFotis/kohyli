from typing import List

from fastapi import APIRouter, HTTPException

from app.api.schemas.orders import OrderCreate
from app.database.models import Order, Book
from app.services.orders import OrdersServiceDep

orders_router = APIRouter(prefix="/orders")


@orders_router.get("")
async def get_all_orders(orders_service: OrdersServiceDep) -> List[Order]:
    """Retrieve all orders from the database."""
    orders = await orders_service.get_all()
    return [o.model_dump() for o in orders]


@orders_router.post("/{user_id}")
async def create_order(
    user_id: int, payload: OrderCreate, orders_service: OrdersServiceDep
) -> Order:
    """Create a new order for a specific user.

    Expects JSON body like:
    {
      "items": [
        {"book_id": 1001, "quantity": 2},
        {"book_id": 1002, "quantity": 1}
      ]
    }
    """
    order = await orders_service.create(user_id, payload.items)
    if not order:
        raise HTTPException(status_code=400, detail="Failed to create order.")
    return order.model_dump()


@orders_router.get("/{id}")
async def get_order(id: int, orders_service: OrdersServiceDep) -> dict:
    """Retrieve a specific order by id and include book details for each item."""
    order = await orders_service.get_by_id(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    # Get order items with associated book details
    items_with_books = await orders_service.get_items_with_books(id)

    order_data = order.model_dump()
    order_data["books"] = items_with_books or []
    return order_data


@orders_router.patch("/{id}/cancel")
async def cancel_order(id: int, orders_service: OrdersServiceDep) -> Order:
    """Cancel an order by id."""
    order = await orders_service.cancel(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order.model_dump()
