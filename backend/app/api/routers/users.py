from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.users import UserCreate

from app.database.models import User, Order
from app.services.users import UsersServiceDep

users_router = APIRouter(prefix="/users")


@users_router.get("")
async def get_all_users(users_service: UsersServiceDep) -> List[User]:
    """Retrieve all users from the database."""
    return await users_service.get_all()

@users_router.post("/signup")
async def create_user(user: UserCreate, users_service: UsersServiceDep) -> User:
    """Signup a new user."""
    return await users_service.create(user)

@users_router.post("/login")
async def login_user(
        request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
        users_service: UsersServiceDep
) -> User:
    """Login a user."""
    email, password = (request_form.username, request_form.password)

    user = await users_service.login(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return user

@users_router.get("/{id}")
async def get_user(id: int, users_service: UsersServiceDep) -> User:
    """Retrieve a specific user, by id, from the database."""
    user = await users_service.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@users_router.get("/email/{email}")
async def get_user_by_email(email: str, users_service: UsersServiceDep) -> User:
    """Retrieve a specific user by their email address."""
    user = await users_service.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@users_router.get("/{id}/orders")
async def get_user_orders(id: int, users_service: UsersServiceDep) -> List[Order]:
    """Retrieve all orders for a specific user."""
    user = await users_service.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return await users_service.get_orders_for_user(id)
