"""Command-line REPL for the enhanced calculator."""

from app.calculator import (
    AutoSaveObserver,
    Calculator,
    LoggingObserver,
)
from app.exceptions import CalculatorError


OPERATION_COMMANDS = {
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "root",
    "modulus",
    "int_divide",
    "percent",
    "abs_diff",
}


def show_help() -> str:
    """Return the calculator help menu."""

    return """
Available commands:

Calculations:
  add a b
  subtract a b
  multiply a b
  divide a b
  power a b
  root a b
  modulus a b
  int_divide a b
  percent a b
  abs_diff a b

History:
  history
  clear
  undo
  redo
  save
  load

Other:
  help
  exit

Example:
  add 5 3
""".strip()


def create_calculator() -> Calculator:
    """Create a calculator with default observers."""

    calculator = Calculator()

    calculator.register_observer(
        LoggingObserver()
    )

    calculator.register_observer(
        AutoSaveObserver(calculator.history)
    )

    return calculator


def process_command(
    calculator: Calculator,
    user_input: str,
) -> str:
    """Process one command and return the result."""

    parts = user_input.strip().split()

    if not parts:
        return ""

    command = parts[0].lower()

    if command == "help":
        return show_help()

    if command == "history":
        return calculator.history.display()

    if command == "clear":
        return calculator.clear_history()

    if command == "undo":
        return calculator.undo()

    if command == "redo":
        return calculator.redo()

    if command == "save":
        return calculator.save_history()

    if command == "load":
        return calculator.load_history()

    if command == "exit":
        return "exit"

    if command in OPERATION_COMMANDS:
        if len(parts) != 3:
            return "Usage: operation number1 number2"

        result = calculator.calculate(
            command,
            parts[1],
            parts[2],
        )

        return f"Result: {result}"

    return (
        f"Unknown command: {command}. "
        "Type 'help' to see available commands."
    )


def main() -> None:
    """Run the calculator REPL."""

    calculator = create_calculator()

    print("Enhanced Calculator")
    print("Type 'help' to view commands.")

    while True:
        try:
            user_input = input(">>> ")

            output = process_command(
                calculator,
                user_input,
            )

            if output == "exit":
                print("Goodbye!")
                break

            if output:
                print(output)

        except CalculatorError as error:
            print(f"Error: {error}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()