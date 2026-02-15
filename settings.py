import logging

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

# ───────────────────────────────────────────────────────────────
# Logger Configuration
# ───────────────────────────────────────────────────────────────

logger = logging.getLogger("settings")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(message)s")
)
logger.addHandler(handler)


class Settings(BaseModel):
    """
    Pydantic model for application settings loaded from environment variables.

    All required variables must be set in the environment or in a .env file.
    """

    APP_NAME: str = Field(..., description="Application name")
    DEBUG: bool = Field(False, description="Enable debug mode")
    PORT: int = Field(..., gt=0, lt=65536, description="Application port")
    SECRET_KEY: str = Field(
        ..., description="Secret key for cryptographic functions"
    )
    DATABASE_URL: str = Field(..., description="Database connection URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        extra="ignore",
    )
