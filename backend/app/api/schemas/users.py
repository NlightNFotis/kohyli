from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Model for creating a new user."""

    first_name: str
    last_name: str
    email: EmailStr
    password: str

class JWTToken(BaseModel):
    """Model for JWT tokens returned by the API after login workflow."""
    access_token: str
    type: str