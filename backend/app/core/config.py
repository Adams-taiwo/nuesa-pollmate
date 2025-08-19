from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://taiwo_adams:new_age18@localhost:5432/pollmate"
    JWT_SECRET_KEY: str = "e48dc54936f3752927a89aaca846ce80"
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8"
    )


Config = Settings()
