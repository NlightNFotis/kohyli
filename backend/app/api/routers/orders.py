from typing import List

from fastapi import APIRouter, HTTPException

from app.database.models import Order, Book
from app.services.orders import OrdersServiceDep

orders_router = APIRouter(prefix="/orders")


@orders_router.get("/")
async def get_all_orders(orders_service: OrdersServiceDep) -> List[Order]:
    """Retrieve all orders from the database."""
    orders = await orders_service.get_all()
    return [o.model_dump() for o in orders]


# TODO: This needs to take in a list of books, but we need to see
# how to pass them in from the frontend. Probably needs to take it
# in the request body, but we may need a new Pydantic model for that.
@orders_router.post("/{user_id}")
async def create_order(user_id: int, orders_service: OrdersServiceDep) -> Order:
    """Create a new order for a specific user."""
    raise NotImplementedError

    orders_service.create(user_id)
    # TODO


@orders_router.get("/{id}")
async def get_order(id: int, orders_service: OrdersServiceDep) -> Order:
    """Retrieve a specific order by id."""
    order = await orders_service.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order.model_dump()


@orders_router.patch("/{id}/cancel")
async def cancel_order(id: int, orders_service: OrdersServiceDep) -> Order:
    """Cancel an order by id."""
    order = await orders_service.cancel(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order.model_dump()


@orders_router.get("/{id}/items")
async def get_order_items(id: int, orders_service: OrdersServiceDep) -> List[Book]:
    """Retrieve all items for a specific order."""
    items = await orders_service.get_items(id)
    if not items:
        raise HTTPException(status_code=404, detail="Order not found.")

    # TODO: This is a OrdersItem - should we convert to book
    return [b.model_dump() for b in items]
