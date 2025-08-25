from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    JWT_SECRET: str = "default is fotis!"
    JWT_ALGORITHM: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


jwt_settings = JWTSettings()
