from redis.asyncio import Redis

from app.config import db_settings

_token_whitelist = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=db_settings.REDIS_DB,
)


async def add_token_to_whitelist(jti: str, expiration_seconds: int):
    """Add a token to the whitelist with an expiration time."""
    await _token_whitelist.set(jti, 1, ex=expiration_seconds)


async def is_token_whitelisted(jti: str) -> bool:
    """Check if a token exists in the whitelist."""
    return await _token_whitelist.exists(jti)


async def remove_token_from_whitelist(jti: str):
    """Remove a token from the whitelist (used during logout)."""
    await _token_whitelist.delete(jti)
