import logging
import os
from typing import Any

from dotenv import load_dotenv
from pydantic import ValidationError

from settings import Settings

# ───────────────────────────────────────────────────────────────
# Logger Configuration
# ───────────────────────────────────────────────────────────────

logger = logging.getLogger("env_loader")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(message)s")
)
logger.addHandler(handler)


class EnvLoader:
    """
    Loads and validates environment variables from a .env file and the OS environment.

    Secret values (keys starting with "SECRET_") are masked when logging.
    """

    def __init__(self, env_file: str = ".env") -> None:
        """
        Initialize loader, load .env file, validate settings, and log them.

        Args:
            env_file (str): Path to the .env file to load.
        """
        logger.info(f"Loading .env file: {env_file}")
        load_dotenv(env_file)

        self.settings = self._load_settings()
        self._log_settings()

    def _load_settings(self) -> Settings:
        """
        Validate environment values and return a Settings instance.

        Raises:
            ValidationError: If one or more required fields are missing or invalid.
        """
        try:
            settings = Settings.model_validate(os.environ)
            logger.info("Environment validation succeeded")
            return settings
        except ValidationError as exc:
            logger.error("Environment validation failed:")
            logger.error(exc.json())
            raise

    def _log_settings(self) -> None:
        """
        Log validated environment settings.

        Keys starting with "SECRET_" are masked for security.
        """
        logger.info("Validated environment variables:")

        for key, value in self.settings.model_dump().items():
            if key.startswith("SECRET_"):
                logger.info(f"  {key} = *value*")
            else:
                logger.info(f"  {key} = {value}")

    def __getattr__(self, item: str) -> Any:
        """
        Forward attribute access to the internal Settings instance.

        Allows dotsyntax access like config.APP_NAME.
        """
        return getattr(self.settings, item)
