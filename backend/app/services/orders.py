from typing import List, Annotated

from fastapi import Depends
from sqlmodel import select

from app.database.models import Order, OrderItem
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

    async def create(self, user_id: int, *args, **kwargs) -> Order:
        """Create a new order. Implementation detail depends on incoming payload shape.
        Left as NotImplemented for now to keep behavior explicit and centralized."""
        raise NotImplementedError


async def get_orders_service(session: SessionDep) -> OrdersService:
    """
    FastAPI dependency factory that receives an AsyncSession
    (via SessionDep) and returns an OrdersService instance.
    """
    return OrdersService(session)


OrdersServiceDep = Annotated[OrdersService, Depends(get_orders_service)]
