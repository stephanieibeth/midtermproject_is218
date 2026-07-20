"""Tests for the Calculator Memento pattern."""

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def test_memento_saves_history():
    calculation = Calculation(
        "add",
        2,
        3,
        5,
        timestamp="2026-07-01T12:00:00",
    )

    original_history = [calculation]

    memento = CalculatorMemento(original_history)

    saved_history = memento.get_saved_history()

    assert saved_history == original_history


def test_memento_returns_new_list():
    calculation = Calculation(
        "add",
        2,
        3,
        5,
    )

    original_history = [calculation]

    memento = CalculatorMemento(original_history)

    saved_history = memento.get_saved_history()

    assert saved_history is not original_history


def test_original_list_change_does_not_change_memento():
    calculation = Calculation(
        "add",
        2,
        3,
        5,
    )

    original_history = [calculation]

    memento = CalculatorMemento(original_history)

    original_history.clear()

    saved_history = memento.get_saved_history()

    assert len(saved_history) == 1


def test_returned_list_change_does_not_change_memento():
    calculation = Calculation(
        "add",
        2,
        3,
        5,
    )

    memento = CalculatorMemento([calculation])

    first_result = memento.get_saved_history()
    first_result.clear()

    second_result = memento.get_saved_history()

    assert len(second_result) == 1