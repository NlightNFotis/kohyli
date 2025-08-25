from typing import List

from fastapi import APIRouter, HTTPException

from ..schemas.users import UserCreate

from app.database.models import User, Order
from app.services.users import UsersServiceDep

users_router = APIRouter(prefix="/users")


@users_router.get("")
async def get_all_users(users_service: UsersServiceDep) -> List[User]:
    """Retrieve all users from the database."""
    users = await users_service.get_all()
    return [u.model_dump() for u in users]

@users_router.post("/signup")
async def create_user(user: UserCreate, users_service: UsersServiceDep) -> User:
    """Signup a new user."""
    return await users_service.create(user)

@users_router.get("/{id}")
async def get_user(id: int, users_service: UsersServiceDep) -> User:
    """Retrieve a specific user, by id, from the database."""
    user = await users_service.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.model_dump()


@users_router.get("/email/{email}")
async def get_user_by_email(email: str, users_service: UsersServiceDep) -> User:
    """Retrieve a specific user by their email address."""
    user = await users_service.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.model_dump()


@users_router.get("/{id}/orders")
async def get_user_orders(id: int, users_service: UsersServiceDep) -> List[Order]:
    """Retrieve all orders for a specific user."""
    user = await users_service.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    orders = await users_service.get_orders_for_user(id)
    return [o.model_dump() for o in orders]
