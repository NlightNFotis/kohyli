from redis.asyncio import Redis

from app.config import db_settings

_token_blacklist = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=db_settings.REDIS_DB,
)


async def add_token_to_blacklist(jti: str):
    await _token_blacklist.set(jti, 1)


async def is_token_blacklisted(jti: str) -> bool:
    return await _token_blacklist.exists(jti)
