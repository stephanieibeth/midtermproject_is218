"""Tests for calculator logging."""

from app.logger import Logger


def test_logger_creates_log_file(tmp_path):
    log_file = tmp_path / "test_calculator.log"

    logger = Logger.configure(log_file)
    logger.info("Test calculation message")

    for handler in logger.handlers:
        handler.flush()

    assert log_file.exists()

    contents = log_file.read_text(encoding="utf-8")

    assert "Test calculation message" in contents
    assert "INFO" in contents


def test_logger_info_method(tmp_path):
    log_file = tmp_path / "info.log"

    Logger.configure(log_file)
    Logger.info("Information message")

    for handler in Logger.get_logger().handlers:
        handler.flush()

    contents = log_file.read_text(encoding="utf-8")

    assert "Information message" in contents


def test_logger_warning_method(tmp_path):
    log_file = tmp_path / "warning.log"

    Logger.configure(log_file)
    Logger.warning("Warning message")

    for handler in Logger.get_logger().handlers:
        handler.flush()

    contents = log_file.read_text(encoding="utf-8")

    assert "Warning message" in contents
    assert "WARNING" in contents


def test_logger_error_method(tmp_path):
    log_file = tmp_path / "error.log"

    Logger.configure(log_file)
    Logger.error("Error message")

    for handler in Logger.get_logger().handlers:
        handler.flush()

    contents = log_file.read_text(encoding="utf-8")

    assert "Error message" in contents
    assert "ERROR" in contents