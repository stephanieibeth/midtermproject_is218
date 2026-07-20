"""Application configuration loaded from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions import ConfigurationError


load_dotenv()


class CalculatorConfig:
    """Stores and validates calculator configuration settings."""

    LOG_DIR = Path(os.getenv("CALCULATOR_LOG_DIR", "logs"))
    HISTORY_DIR = Path(os.getenv("CALCULATOR_HISTORY_DIR", "history"))

    LOG_FILE_NAME = os.getenv(
        "CALCULATOR_LOG_FILE",
        "calculator.log",
    )

    HISTORY_FILE_NAME = os.getenv(
        "CALCULATOR_HISTORY_FILE",
        "calculator_history.csv",
    )

    MAX_HISTORY_SIZE = int(
        os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100")
    )

    AUTO_SAVE = (
        os.getenv("CALCULATOR_AUTO_SAVE", "true").lower()
        == "true"
    )

    PRECISION = int(
        os.getenv("CALCULATOR_PRECISION", "4")
    )

    MAX_INPUT_VALUE = float(
        os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000")
    )

    DEFAULT_ENCODING = os.getenv(
        "CALCULATOR_DEFAULT_ENCODING",
        "utf-8",
    )

    LOG_FILE = LOG_DIR / LOG_FILE_NAME
    HISTORY_FILE = HISTORY_DIR / HISTORY_FILE_NAME

    @classmethod
    def validate(cls) -> None:
        """Validate configuration values."""

        if cls.MAX_HISTORY_SIZE <= 0:
            raise ConfigurationError(
                "CALCULATOR_MAX_HISTORY_SIZE must be greater than zero."
            )

        if cls.PRECISION < 0:
            raise ConfigurationError(
                "CALCULATOR_PRECISION cannot be negative."
            )

        if cls.MAX_INPUT_VALUE <= 0:
            raise ConfigurationError(
                "CALCULATOR_MAX_INPUT_VALUE must be greater than zero."
            )

        if not cls.DEFAULT_ENCODING:
            raise ConfigurationError(
                "CALCULATOR_DEFAULT_ENCODING cannot be empty."
            )

    @classmethod
    def create_directories(cls) -> None:
        """Create the log and history directories."""

        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        cls.HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def initialize(cls) -> None:
        """Validate configuration and create required directories."""

        cls.validate()
        cls.create_directories()