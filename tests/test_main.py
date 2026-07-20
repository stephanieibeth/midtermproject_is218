"""Tests for the calculator REPL."""

from main import (
    create_calculator,
    process_command,
    show_help,
)


def test_show_help():
    output = show_help()

    assert "Available commands" in output
    assert "add a b" in output
    assert "history" in output
    assert "exit" in output


def test_create_calculator():
    calculator = create_calculator()

    assert len(calculator.observers) == 2


def test_empty_command():
    calculator = create_calculator()

    assert process_command(calculator, "") == ""


def test_add_command():
    calculator = create_calculator()

    result = process_command(calculator, "add 5 3")

    assert result == "Result: 8.0"


def test_invalid_argument_count():
    calculator = create_calculator()

    result = process_command(calculator, "add 5")

    assert result == "Usage: operation number1 number2"


def test_history_command():
    calculator = create_calculator()

    process_command(calculator, "add 5 3")

    result = process_command(calculator, "history")

    assert "add" in result
    assert "= 8.0" in result


def test_clear_command():
    calculator = create_calculator()

    process_command(calculator, "add 5 3")

    result = process_command(calculator, "clear")

    assert result == "History cleared."


def test_undo_command():
    calculator = create_calculator()

    process_command(calculator, "add 5 3")

    result = process_command(calculator, "undo")

    assert result == "Undo successful."


def test_redo_command():
    calculator = create_calculator()

    process_command(calculator, "add 5 3")
    process_command(calculator, "undo")

    result = process_command(calculator, "redo")

    assert result == "Redo successful."


def test_help_command():
    calculator = create_calculator()

    result = process_command(calculator, "help")

    assert "Available commands" in result


def test_exit_command():
    calculator = create_calculator()

    assert process_command(calculator, "exit") == "exit"


def test_unknown_command():
    calculator = create_calculator()

    result = process_command(calculator, "dance")

    assert "Unknown command" in result