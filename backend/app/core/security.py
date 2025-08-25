from typing import Annotated

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.database.models import User
from app.services.users import UsersServiceDep
from app.utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Dependency type for FastAPI automatic dependency injection
TokenDep = Annotated[str, Depends(oauth2_scheme)]


# Utility function to ensure the presence of a valid access token.
# To use used as a FastAPI dependency.
async def get_access_token(token: TokenDep) -> dict:
    data = decode_access_token(token)
    # Perform additional validation on the token data so that later
    # pipeline functions can depend on the presence of the correct data.
    if not data or not data.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )
    return data


# Convenience type for the token data - to simplify function signatures.
TokenData = Annotated[dict, Depends(get_access_token)]


# Utility function to retrieve a user by their ID from the database.
# To use used as a FastAPI dependency for the routes.
async def get_user_id(token_data: TokenData, users_service: UsersServiceDep) -> User:
    user = await users_service.get_by_id(token_data.get("user_id"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return user

# FastAPI dependency for the signed-in user.
SignedInUserDep = Annotated[User, Depends(get_user_id)]