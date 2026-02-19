from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    URL: str = Field(..., alias="ODOO_URL")
    DATABASE: str = Field(..., alias="ODOO_DB")
    USER: str = Field(..., alias="ODOO_USER")
    API_KEY: str = Field(..., alias="ODOO_API_KEY")

    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    EXPIRE: int = Field(12, alias="TOKEN_EXPIRE")

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", case_sensitive=True
    )


settings = Settings()
