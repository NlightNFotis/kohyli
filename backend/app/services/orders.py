from typing import List, Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import select
from datetime import datetime, timezone
from decimal import Decimal

from app.database.models import Order, OrderItem, Book, User
from app.database.session import SessionDep


class OrdersService:
    """Encapsulate DB operations and other logic for orders."""

    def __init__(self, session: SessionDep):
        self._session = session

    async def get_all(self) -> List[Order]:
        result = await self._session.execute(select(Order))
        return result.scalars().all()

    async def get_by_id(self, order_id: int) -> Order | None:
        return await self._session.get(Order, order_id)

    async def get_by_user(self, user_id: int) -> List[Order]:
        stmt = select(Order).where(Order.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def cancel(self, order_id: int) -> Order | None:
        order = await self.get_by_id(order_id)
        if not order:
            return None
        order.status = "Cancelled"
        await self._session.commit()
        await self._session.refresh(order)
        return order

    async def get_items(self, order_id: int) -> List[OrderItem] | None:
        """
        Return list of specific order items for the given order_id.
        Avoids lazy-loading the relationship on the order instance,
        by querying the OrderItem table directly in the async context.
        """
        order = await self.get_by_id(order_id)
        if not order:
            return None

        stmt = select(OrderItem).where(OrderItem.order_id == order_id)
        result = await self._session.execute(stmt)
        items = result.scalars().all()
        return items

    async def get_items_with_books(self, order_id: int) -> List[dict] | None:
        """
        Return list of order items including the associated book data.
        Each element is a dict with book fields plus quantity and price_at_purchase.
        """
        items = await self.get_items(order_id)
        if items is None:
            return None

        enriched = []
        for item in items:
            book = await self._session.get(Book, item.book_id)
            if not book:
                # If book was removed from catalog, include minimal data
                enriched.append(
                    {
                        "book_id": item.book_id,
                        "title": None,
                        "quantity": item.quantity,
                        "price_at_purchase": str(item.price_at_purchase),
                    }
                )
                continue

            book_data = book.model_dump()
            # attach order-specific fields
            book_data["quantity"] = item.quantity
            book_data["price_at_purchase"] = str(item.price_at_purchase)
            enriched.append(book_data)

        return enriched

    async def create(self, user_id: int, elements: List[dict]) -> Order:
        """
        Create a new order for the given user_id.

        elements: List of dicts with keys 'book_id' and 'quantity'
        """
        # Verify user exists
        user = await self._session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        # Prepare items and validate stock
        items_objs: List[OrderItem] = []
        total_price = Decimal("0.00")

        for elem in elements:
            book_id = elem.book_id
            quantity = elem.quantity
            if quantity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid quantity for book {book_id}.",
                )

            book = await self._session.get(Book, book_id)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Book with id {book_id} not found.",
                )

            if book.stock_quantity < quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for book id {book_id}. Requested {quantity}, available {book.stock_quantity}.",
                )

            # Create OrderItem and reserve stock
            item_price: Decimal = book.price
            items_objs.append(
                OrderItem(
                    book_id=book.id, quantity=quantity, price_at_purchase=item_price
                )
            )

            total_price += item_price * quantity

            # decrement stock
            book.stock_quantity = book.stock_quantity - quantity
            self._session.add(book)

        # Create Order with items (SQLModel relationship will persist OrderItems)
        order = Order(
            user_id=user_id,
            order_date=datetime.now(timezone.utc),
            total_price=total_price,
            status="Created",
            items=items_objs,
        )

        self._session.add(order)
        await self._session.commit()
        await self._session.refresh(order)
        return order


async def get_orders_service(session: SessionDep) -> OrdersService:
    """
    FastAPI dependency factory that receives an AsyncSession
    (via SessionDep) and returns an OrdersService instance.
    """
    return OrdersService(session)


OrdersServiceDep = Annotated[OrdersService, Depends(get_orders_service)]
