from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置：使用 Pydantic v2 BaseSettings"""

    SECRET_KEY: str = "a_very_secret_key"  # Add a default for simplicity
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./userlab.db"

    # Pydantic v2-style config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
