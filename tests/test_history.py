"""Tests for calculation history management."""

import pandas as pd
import pytest

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError
from app.history import History


def create_calculation(
    operation="add",
    operand1=2,
    operand2=3,
    result=5,
):
    """Create a calculation for history tests."""

    return Calculation(
        operation,
        operand1,
        operand2,
        result,
        timestamp="2026-07-01T12:00:00",
    )


def test_history_starts_empty():
    history = History()

    assert len(history) == 0
    assert history.calculations == []


def test_add_calculation():
    history = History()
    calculation = create_calculation()

    history.add(calculation)

    assert len(history) == 1
    assert history.calculations[0] == calculation


def test_clear_history():
    history = History()
    history.add(create_calculation())

    history.clear()

    assert len(history) == 0


def test_history_iteration():
    history = History()
    calculation = create_calculation()

    history.add(calculation)

    assert list(history) == [calculation]


def test_maximum_history_size(monkeypatch):
    monkeypatch.setattr(
        CalculatorConfig,
        "MAX_HISTORY_SIZE",
        2,
    )

    history = History()

    history.add(create_calculation("add", 1, 1, 2))
    history.add(create_calculation("add", 2, 2, 4))
    history.add(create_calculation("add", 3, 3, 6))

    assert len(history) == 2
    assert history.calculations[0].operand1 == 2
    assert history.calculations[1].operand1 == 3


def test_to_dataframe():
    history = History()
    history.add(create_calculation())

    dataframe = history.to_dataframe()

    assert isinstance(dataframe, pd.DataFrame)
    assert len(dataframe) == 1

    assert list(dataframe.columns) == [
        "operation",
        "operand1",
        "operand2",
        "result",
        "timestamp",
    ]


def test_empty_history_dataframe():
    history = History()

    dataframe = history.to_dataframe()

    assert dataframe.empty

    assert list(dataframe.columns) == [
        "operation",
        "operand1",
        "operand2",
        "result",
        "timestamp",
    ]


def test_save_history(tmp_path):
    history = History()
    history.add(create_calculation())

    history_file = tmp_path / "history.csv"

    history.save(history_file)

    assert history_file.exists()

    dataframe = pd.read_csv(history_file)

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["operation"] == "add"
    assert dataframe.iloc[0]["result"] == 5


def test_load_history(tmp_path):
    history_file = tmp_path / "history.csv"

    dataframe = pd.DataFrame(
        [
            {
                "operation": "multiply",
                "operand1": 4,
                "operand2": 5,
                "result": 20,
                "timestamp": "2026-07-01T12:00:00",
            }
        ]
    )

    dataframe.to_csv(history_file, index=False)

    history = History()
    history.load(history_file)

    assert len(history) == 1

    calculation = history.calculations[0]

    assert calculation.operation == "multiply"
    assert calculation.operand1 == 4
    assert calculation.operand2 == 5
    assert calculation.result == 20


def test_load_missing_file(tmp_path):
    history = History()
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(
        OperationError,
        match="does not exist",
    ):
        history.load(missing_file)


def test_load_file_with_missing_columns(tmp_path):
    history_file = tmp_path / "invalid.csv"

    dataframe = pd.DataFrame(
        [
            {
                "operation": "add",
                "result": 5,
            }
        ]
    )

    dataframe.to_csv(history_file, index=False)

    history = History()

    with pytest.raises(
        OperationError,
        match="missing required columns",
    ):
        history.load(history_file)


def test_display_empty_history():
    history = History()

    assert history.display() == (
        "No calculation history available."
    )


def test_display_history():
    history = History()
    history.add(create_calculation())

    output = history.display()

    assert "1." in output
    assert "add" in output
    assert "2, 3" in output
    assert "= 5" in output