"""
Integration test for JWT whitelist functionality.

This test verifies:
1. Tokens are added to whitelist upon generation
2. Token validation checks the whitelist
3. Logout removes tokens from whitelist
"""
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import timedelta

from app.utils import generate_access_token, decode_access_token


class MockRedis:
    """Mock Redis client for testing."""
    
    def __init__(self):
        self._store = {}
    
    async def set(self, key: str, value, ex: int = None):
        """Mock Redis SET operation with expiration."""
        self._store[key] = {"value": value, "ex": ex}
        return True
    
    async def exists(self, key: str) -> bool:
        """Mock Redis EXISTS operation."""
        return key in self._store
    
    async def delete(self, key: str):
        """Mock Redis DELETE operation."""
        if key in self._store:
            del self._store[key]
        return True
    
    def clear(self):
        """Clear the mock store."""
        self._store.clear()


@pytest_asyncio.fixture
async def mock_redis():
    """Provide a mock Redis instance for testing."""
    redis_mock = MockRedis()
    
    # Patch the Redis instance in the redis module
    with patch('app.database.redis._token_whitelist', redis_mock):
        yield redis_mock
        redis_mock.clear()


@pytest.mark.asyncio
async def test_token_added_to_whitelist_on_generation(mock_redis):
    """Test that a token is added to the whitelist when generated."""
    # Generate a token
    token = await generate_access_token(
        data={"user_id": 123, "email": "test@example.com"},
        expiry=timedelta(minutes=60)
    )
    
    # Decode to get jti
    decoded = decode_access_token(token)
    jti = decoded.get("jti")
    
    # Verify token is in whitelist
    assert jti in mock_redis._store
    assert mock_redis._store[jti]["ex"] == 60 * 60  # 60 minutes in seconds


@pytest.mark.asyncio
async def test_token_validation_checks_whitelist(mock_redis):
    """Test that token validation checks if token is in whitelist."""
    from app.database.redis import is_token_whitelisted
    
    # Generate a token
    token = await generate_access_token(
        data={"user_id": 456, "email": "user@example.com"},
        expiry=timedelta(minutes=30)
    )
    
    # Decode to get jti
    decoded = decode_access_token(token)
    jti = decoded.get("jti")
    
    # Check token is whitelisted
    is_whitelisted = await is_token_whitelisted(jti)
    assert is_whitelisted is True


@pytest.mark.asyncio
async def test_logout_removes_token_from_whitelist(mock_redis):
    """Test that logout removes token from whitelist."""
    from app.database.redis import remove_token_from_whitelist, is_token_whitelisted
    
    # Generate a token
    token = await generate_access_token(
        data={"user_id": 789, "email": "logout@example.com"},
        expiry=timedelta(minutes=15)
    )
    
    # Decode to get jti
    decoded = decode_access_token(token)
    jti = decoded.get("jti")
    
    # Verify token is initially whitelisted
    assert await is_token_whitelisted(jti) is True
    
    # Remove token from whitelist (simulate logout)
    await remove_token_from_whitelist(jti)
    
    # Verify token is no longer whitelisted
    assert await is_token_whitelisted(jti) is False


@pytest.mark.asyncio
async def test_whitelist_expiration_matches_token_expiration(mock_redis):
    """Test that whitelist entry has same expiration as token."""
    # Generate token with custom expiration
    custom_expiry = timedelta(minutes=120)
    token = await generate_access_token(
        data={"user_id": 999, "email": "expire@example.com"},
        expiry=custom_expiry
    )
    
    # Decode to get jti
    decoded = decode_access_token(token)
    jti = decoded.get("jti")
    
    # Check that Redis entry has correct expiration
    assert jti in mock_redis._store
    assert mock_redis._store[jti]["ex"] == int(custom_expiry.total_seconds())


@pytest.mark.asyncio
async def test_non_whitelisted_token_returns_false(mock_redis):
    """Test that a non-existent token is not whitelisted."""
    from app.database.redis import is_token_whitelisted
    
    # Check a random jti that was never added
    fake_jti = "00000000-0000-0000-0000-000000000000"
    is_whitelisted = await is_token_whitelisted(fake_jti)
    
    assert is_whitelisted is False
