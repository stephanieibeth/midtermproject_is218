"""Tests for calculator input validation."""

import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import (
    validate_number,
    validate_two_numbers,
)


@pytest.mark.parametrize(
    "value, expected",
    [
        (5, 5.0),
        (3.5, 3.5),
        (-10, -10.0),
        ("25", 25.0),
        (" 7.5 ", 7.5),
    ],
)
def test_validate_number(value, expected):
    assert validate_number(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "hello",
        "",
        None,
        object(),
    ],
)
def test_invalid_numeric_input(value):
    with pytest.raises(
        ValidationError,
        match="Invalid numeric input",
    ):
        validate_number(value)


@pytest.mark.parametrize(
    "value",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_non_finite_values(value):
    with pytest.raises(
        ValidationError,
        match="finite number",
    ):
        validate_number(value)


def test_boolean_is_invalid():
    with pytest.raises(
        ValidationError,
        match="Boolean values",
    ):
        validate_number(True)


def test_number_exceeds_maximum(monkeypatch):
    monkeypatch.setattr(
        CalculatorConfig,
        "MAX_INPUT_VALUE",
        100,
    )

    with pytest.raises(
        ValidationError,
        match="maximum allowed value",
    ):
        validate_number(101)


def test_negative_number_exceeds_maximum(monkeypatch):
    monkeypatch.setattr(
        CalculatorConfig,
        "MAX_INPUT_VALUE",
        100,
    )

    with pytest.raises(
        ValidationError,
        match="maximum allowed value",
    ):
        validate_number(-101)


def test_validate_two_numbers():
    first, second = validate_two_numbers("5", "2.5")

    assert first == 5.0
    assert second == 2.5