from datetime import datetime, timedelta

import jwt

from app.config import jwt_settings


def generate_access_token(
    data: dict,
    expiry: timedelta = timedelta(minutes=jwt_settings.access_token_expire_minutes),
) -> str:
    return jwt.encode(
        payload={
            **data,
            "exp": datetime.now() + expiry,
        },
        algorithm=jwt_settings.JWT_ALGORITHM,
        key=jwt_settings.JWT_SECRET,
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            algorithms=[jwt_settings.JWT_ALGORITHM],
            key=jwt_settings.JWT_SECRET,
        )
    except jwt.PyJWTError:
        return None
