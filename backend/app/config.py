from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file=".env", env_ignore_empty=True, extra="ignore"
)


class JWTSettings(BaseSettings):
    JWT_SECRET: str = "default is fotis!"
    JWT_ALGORITHM: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = _base_config


jwt_settings = JWTSettings()


class DatabaseSettings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    model_config = _base_config


db_settings = DatabaseSettings()
