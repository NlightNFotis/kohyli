from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

from app.config import jwt_settings


def generate_access_token(
    data: dict,
    expiry: timedelta = timedelta(minutes=jwt_settings.access_token_expire_minutes),
) -> str:
    return jwt.encode(
        payload={
            **data,
            "exp": datetime.now(timezone.utc) + expiry,
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
    # capture token expiration error separately so that we can more
    # gracefully
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired."
        )
    except jwt.PyJWTError:
        return None
