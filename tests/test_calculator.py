"""Tests for the main Calculator class."""

import pytest

from app.calculator import (
    AutoSaveObserver,
    Calculator,
    CalculatorObserver,
    LoggingObserver,
)
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


class RecordingObserver(CalculatorObserver):
    """Observer used only for testing."""

    def __init__(self) -> None:
        self.calculations = []

    def update(self, calculation) -> None:
        self.calculations.append(calculation)


def test_calculator_starts_empty():
    calculator = Calculator()

    assert len(calculator.history) == 0
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 5, 3, 8),
        ("subtract", 10, 4, 6),
        ("multiply", 3, 4, 12),
        ("divide", 10, 2, 5),
        ("power", 2, 3, 8),
        ("root", 27, 3, 3),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 25, 100, 25),
        ("abs_diff", 5, 10, 5),
    ],
)
def test_calculate(operation, a, b, expected):
    calculator = Calculator()

    result = calculator.calculate(
        operation,
        a,
        b,
    )

    assert result == expected
    assert len(calculator.history) == 1


def test_calculate_rounds_result(monkeypatch):
    monkeypatch.setattr(
        CalculatorConfig,
        "PRECISION",
        2,
    )

    calculator = Calculator()

    result = calculator.calculate(
        "divide",
        1,
        3,
    )

    assert result == 0.33


def test_calculate_invalid_input():
    calculator = Calculator()

    with pytest.raises(ValidationError):
        calculator.calculate(
            "add",
            "hello",
            5,
        )


def test_register_and_notify_observer():
    calculator = Calculator()
    observer = RecordingObserver()

    calculator.register_observer(observer)

    calculator.calculate(
        "add",
        2,
        3,
    )

    assert len(observer.calculations) == 1
    assert observer.calculations[0].result == 5


def test_remove_observer():
    calculator = Calculator()
    observer = RecordingObserver()

    calculator.register_observer(observer)
    calculator.remove_observer(observer)

    calculator.calculate(
        "add",
        2,
        3,
    )

    assert observer.calculations == []


def test_remove_unregistered_observer():
    calculator = Calculator()
    observer = RecordingObserver()

    calculator.remove_observer(observer)

    assert calculator.observers == []


def test_undo():
    calculator = Calculator()

    calculator.calculate("add", 2, 3)
    calculator.calculate("multiply", 4, 5)

    message = calculator.undo()

    assert message == "Undo successful."
    assert len(calculator.history) == 1
    assert (
        calculator.history.calculations[0].operation
        == "add"
    )


def test_undo_when_empty():
    calculator = Calculator()

    assert calculator.undo() == "Nothing to undo."


def test_redo():
    calculator = Calculator()

    calculator.calculate("add", 2, 3)
    calculator.calculate("multiply", 4, 5)

    calculator.undo()
    message = calculator.redo()

    assert message == "Redo successful."
    assert len(calculator.history) == 2


def test_redo_when_empty():
    calculator = Calculator()

    assert calculator.redo() == "Nothing to redo."


def test_new_calculation_clears_redo_stack():
    calculator = Calculator()

    calculator.calculate("add", 2, 3)
    calculator.calculate("multiply", 4, 5)

    calculator.undo()

    assert len(calculator.redo_stack) == 1

    calculator.calculate("subtract", 10, 4)

    assert calculator.redo_stack == []


def test_clear_history():
    calculator = Calculator()
    calculator.calculate("add", 2, 3)

    message = calculator.clear_history()

    assert message == "History cleared."
    assert len(calculator.history) == 0


def test_clear_empty_history():
    calculator = Calculator()

    assert (
        calculator.clear_history()
        == "History is already empty."
    )


def test_save_history(tmp_path, monkeypatch):
    history_file = tmp_path / "history.csv"

    monkeypatch.setattr(
        CalculatorConfig,
        "HISTORY_FILE",
        history_file,
    )

    calculator = Calculator()
    calculator.calculate("add", 2, 3)

    message = calculator.save_history()

    assert message == "History saved."
    assert history_file.exists()


def test_load_history(tmp_path, monkeypatch):
    history_file = tmp_path / "history.csv"

    monkeypatch.setattr(
        CalculatorConfig,
        "HISTORY_FILE",
        history_file,
    )

    first_calculator = Calculator()
    first_calculator.calculate("add", 2, 3)
    first_calculator.save_history()

    second_calculator = Calculator()
    message = second_calculator.load_history()

    assert message == "History loaded."
    assert len(second_calculator.history) == 1


def test_logging_observer(tmp_path, monkeypatch):
    log_file = tmp_path / "calculator.log"

    monkeypatch.setattr(
        CalculatorConfig,
        "LOG_FILE",
        log_file,
    )

    from app.logger import Logger

    Logger.configure(log_file)

    observer = LoggingObserver()

    calculator = Calculator()
    calculator.register_observer(observer)
    calculator.calculate("add", 2, 3)

    for handler in Logger.get_logger().handlers:
        handler.flush()

    contents = log_file.read_text(
        encoding="utf-8"
    )

    assert "Calculation completed" in contents
    assert "add" in contents


def test_auto_save_observer(
    tmp_path,
    monkeypatch,
):
    history_file = tmp_path / "auto_save.csv"

    monkeypatch.setattr(
        CalculatorConfig,
        "HISTORY_FILE",
        history_file,
    )
    monkeypatch.setattr(
        CalculatorConfig,
        "AUTO_SAVE",
        True,
    )

    calculator = Calculator()

    observer = AutoSaveObserver(
        calculator.history
    )

    calculator.register_observer(observer)

    calculator.calculate("add", 2, 3)

    assert history_file.exists()


def test_auto_save_disabled(
    tmp_path,
    monkeypatch,
):
    history_file = tmp_path / "disabled.csv"

    monkeypatch.setattr(
        CalculatorConfig,
        "HISTORY_FILE",
        history_file,
    )
    monkeypatch.setattr(
        CalculatorConfig,
        "AUTO_SAVE",
        False,
    )

    calculator = Calculator()

    observer = AutoSaveObserver(
        calculator.history
    )

    calculator.register_observer(observer)

    calculator.calculate("add", 2, 3)

    assert not history_file.exists()