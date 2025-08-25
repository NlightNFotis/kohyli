from typing import List

from fastapi import APIRouter, HTTPException

from app.database.models import User, Order
from app.services.users import UsersServiceDep

user_router = APIRouter(prefix="/users")

@user_router.get("/")
async def get_all_users(users_service: UsersServiceDep) -> List[User]:
    """Retrieve all users from the database."""
    users = await users_service.get_all()
    return [u.model_dump() for u in users]


@user_router.get("/{id}")
async def get_user(id: int, users_service: UsersServiceDep) -> User:
    """Retrieve a specific user, by id, from the database."""
    user = await users_service.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.model_dump()


@user_router.get("/email/{email}")
async def get_user_by_email(email: str, users_service: UsersServiceDep) -> User:
    """Retrieve a specific user by their email address."""
    user = await users_service.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.model_dump()


@user_router.get("/{id}/orders")
async def get_user_orders(id: int, users_service: UsersServiceDep) -> List[Order]:
    """Retrieve all orders for a specific user."""
    user = await users_service.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    orders = await users_service.get_orders_for_user(id)
    return [o.model_dump() for o in orders]