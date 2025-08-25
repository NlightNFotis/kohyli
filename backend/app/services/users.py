from typing import List, Annotated

from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User, Order
from app.database.session import SessionDep


class UsersService:
    """Encapsulate DB operations for users."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> List[User]:
        """Return all users."""
        result = await self._session.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, user_id: int) -> User | None:
        """Return a user by id or None if not found."""
        return await self._session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        """Return a user by email or None if not found."""
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    # FOTIS: This is a mirror of users_service.get_orders_for_user. We
    # should probably delete one of the two, but let's keep this around
    # for now.
    async def get_orders_for_user(self, user_id: int) -> List[Order]:
        """Return all orders for a given user id."""
        stmt = select(Order).where(Order.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()


async def get_users_service(session: SessionDep) -> UsersService:
    """
    Dependency factory for UsersService.

    Usage in routes:
      svc: UsersService = Depends(get_users_service)
    """
    return UsersService(session)


# Typing helper for route parameter annotations:
UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]
