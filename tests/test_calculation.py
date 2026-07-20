"""Tests for the Calculation model."""

from app.calculation import Calculation


def test_create_calculation():
    calculation = Calculation("add", 5, 3, 8)

    assert calculation.operation == "add"
    assert calculation.operand1 == 5
    assert calculation.operand2 == 3
    assert calculation.result == 8
    assert calculation.timestamp is not None


def test_calculation_to_dict():
    calculation = Calculation(
        "multiply",
        4,
        5,
        20,
        timestamp="2026-07-01T12:00:00",
    )

    data = calculation.to_dict()

    assert data == {
        "operation": "multiply",
        "operand1": 4,
        "operand2": 5,
        "result": 20,
        "timestamp": "2026-07-01T12:00:00",
    }


def test_calculation_from_dict():
    data = {
        "operation": "subtract",
        "operand1": "10",
        "operand2": "4",
        "result": "6",
        "timestamp": "2026-07-01T12:00:00",
    }

    calculation = Calculation.from_dict(data)

    assert calculation.operation == "subtract"
    assert calculation.operand1 == 10.0
    assert calculation.operand2 == 4.0
    assert calculation.result == 6.0


def test_calculation_string():
    calculation = Calculation(
        "divide",
        10,
        2,
        5,
        timestamp="2026-07-01T12:00:00",
    )

    assert str(calculation) == "divide(10, 2) = 5"


def test_calculations_are_equal():
    first = Calculation(
        "add",
        2,
        3,
        5,
        timestamp="2026-07-01T12:00:00",
    )
    second = Calculation(
        "add",
        2,
        3,
        5,
        timestamp="2026-07-01T12:00:00",
    )

    assert first == second


def test_calculation_not_equal_to_other_type():
    calculation = Calculation("add", 2, 3, 5)

    assert calculation != "not a calculation"