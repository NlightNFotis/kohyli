from datetime import datetime, timedelta
from typing import List, Annotated

import jwt
from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.config import jwt_settings
from app.api.schemas.users import UserCreate
from app.database.models import User, Order
from app.database.session import SessionDep
from app.utils import generate_access_token


class UsersService:
    """Encapsulate DB operations for users."""

    def __init__(self, session: AsyncSession):
        self._session = session
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create(self, user_signup: UserCreate) -> User:
        """Create a new user (part of the signup workflow)."""
        user = User(**user_signup.model_dump(exclude=["password"]))
        user.password_hash = self._pwd_context.hash(user_signup.password)
        user.created_at = datetime.now()

        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def login(self, email: str, password: str) -> str | None:
        """Verify user credentials and a JWT token if valid."""
        user = await self.get_by_email(email)
        if (
            not user  # user hasn't signed up yet
            or not self._pwd_context.verify(
                password, user.password_hash
            )  # wrong password
        ):
            return None

        token = generate_access_token(
            data={
                "user": {
                    # TODO: FOTIS: VERY UNSAFE! Change this to be encrypted or something
                    "user_id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            }
        )

        return token

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
