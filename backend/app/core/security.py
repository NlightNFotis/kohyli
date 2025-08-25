from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Dependency type for FastAPI automatic dependency injection
TokenDep = Annotated[str, Depends(oauth2_scheme)]
