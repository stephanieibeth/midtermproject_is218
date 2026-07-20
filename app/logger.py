"""Logging configuration for the calculator application."""

import logging
from pathlib import Path

from app.calculator_config import CalculatorConfig


class Logger:
    """Provides application-wide logging methods."""

    _logger: logging.Logger | None = None

    @classmethod
    def configure(
        cls,
        log_file: Path | None = None,
    ) -> logging.Logger:
        """
        Configure and return the calculator logger.

        Args:
            log_file: Optional path used mainly for testing.

        Returns:
            The configured logging instance.
        """

        CalculatorConfig.initialize()

        target_file = log_file or CalculatorConfig.LOG_FILE

        logger = logging.getLogger("calculator")
        logger.setLevel(logging.INFO)
        logger.propagate = False

        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()

        file_handler = logging.FileHandler(
            target_file,
            encoding=CalculatorConfig.DEFAULT_ENCODING,
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        cls._logger = logger
        return logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Return the configured logger."""

        if cls._logger is None:
            return cls.configure()

        return cls._logger

    @classmethod
    def info(cls, message: str) -> None:
        """Write an informational log message."""

        cls.get_logger().info(message)

    @classmethod
    def warning(cls, message: str) -> None:
        """Write a warning log message."""

        cls.get_logger().warning(message)

    @classmethod
    def error(cls, message: str) -> None:
        """Write an error log message."""

        cls.get_logger().error(message)