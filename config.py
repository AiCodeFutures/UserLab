from pydantic import BaseSettings, ConfigDict


class Settings(BaseSettings):
    """应用配置：使用 Pydantic v2 BaseSettings"""

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./userlab.db"

    # Pydantic v2 配置
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
