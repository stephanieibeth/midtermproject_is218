"""Tests for calculator configuration."""

from pathlib import Path

import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_configuration_values_loaded():
    assert CalculatorConfig.MAX_HISTORY_SIZE > 0
    assert CalculatorConfig.PRECISION >= 0
    assert CalculatorConfig.MAX_INPUT_VALUE > 0
    assert CalculatorConfig.DEFAULT_ENCODING


def test_configuration_paths():
    assert isinstance(CalculatorConfig.LOG_DIR, Path)
    assert isinstance(CalculatorConfig.HISTORY_DIR, Path)
    assert CalculatorConfig.LOG_FILE.name == "calculator.log"
    assert (
        CalculatorConfig.HISTORY_FILE.name
        == "calculator_history.csv"
    )


def test_create_directories(tmp_path, monkeypatch):
    log_directory = tmp_path / "test_logs"
    history_directory = tmp_path / "test_history"

    monkeypatch.setattr(
        CalculatorConfig,
        "LOG_DIR",
        log_directory,
    )
    monkeypatch.setattr(
        CalculatorConfig,
        "HISTORY_DIR",
        history_directory,
    )

    CalculatorConfig.create_directories()

    assert log_directory.exists()
    assert history_directory.exists()


def test_validate_valid_configuration():
    CalculatorConfig.validate()


def test_invalid_max_history_size(monkeypatch):
    monkeypatch.setattr(
        CalculatorConfig,
        "MAX_HISTORY_SIZE",
        0,
    )

    with pytest.raises(
        ConfigurationError,
        match="must be greater than zero",
    ):
        CalculatorConfig.validate()


def test_invalid_precision(monkeypatch):
    monkeypatch.setattr(
        CalculatorConfig,
        "PRECISION",
        -1,
    )

    with pytest.raises(
        ConfigurationError,
        match="cannot be negative",
    ):
        CalculatorConfig.validate()


def test_invalid_max_input_value(monkeypatch):
    monkeypatch.setattr(
        CalculatorConfig,
        "MAX_INPUT_VALUE",
        0,
    )

    with pytest.raises(
        ConfigurationError,
        match="must be greater than zero",
    ):
        CalculatorConfig.validate()


def test_empty_encoding(monkeypatch):
    monkeypatch.setattr(
        CalculatorConfig,
        "DEFAULT_ENCODING",
        "",
    )

    with pytest.raises(
        ConfigurationError,
        match="cannot be empty",
    ):
        CalculatorConfig.validate()