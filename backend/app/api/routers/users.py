from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.users import UserCreate, JWTToken

from app.core.security import TokenDep, SignedInUserDep
from app.database.models import User, Order
from app.services.users import UsersServiceDep
from ...utils import decode_access_token

users_router = APIRouter(prefix="/users")


@users_router.post("/signup")
async def create_user(user: UserCreate, users_service: UsersServiceDep) -> User:
    """Signup a new user."""
    return await users_service.create(user)


@users_router.post("/login")
async def login_user(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    users_service: UsersServiceDep,
) -> JWTToken:
    """Login a user."""
    email, password = (request_form.username, request_form.password)

    token = await users_service.login(email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Email or password incorrect.")

    return JWTToken(access_token=token, type="jwt")


@users_router.delete("/delete")
async def delete_user(users_service: UsersServiceDep, user: SignedInUserDep) -> bool:
    # We don't need to perform validation for the user here, as that will
    # have been done by the dependency.
    await users_service.delete(user.id)
    return True


@users_router.get("/orders")
async def get_user_orders(
    users_service: UsersServiceDep, user: SignedInUserDep
) -> List[Order]:
    """Retrieve all orders for a specific user."""
    return await users_service.get_orders_for_user(user.id)
