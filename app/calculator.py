"""Main calculator service using Factory, Memento, and Observer patterns."""

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.history import History
from app.input_validators import validate_two_numbers
from app.logger import Logger
from app.operations import OperationFactory


class CalculatorObserver:
    """Base observer interface."""

    def update(self, calculation: Calculation) -> None:
        """Respond to a completed calculation."""

        raise NotImplementedError


class LoggingObserver(CalculatorObserver):
    """Logs each completed calculation."""

    def update(self, calculation: Calculation) -> None:
        Logger.info(
            f"Calculation completed: "
            f"{calculation.operation}("
            f"{calculation.operand1}, "
            f"{calculation.operand2}) "
            f"= {calculation.result}"
        )


class AutoSaveObserver(CalculatorObserver):
    """Automatically saves history after each calculation."""

    def __init__(self, history: History) -> None:
        self.history = history

    def update(self, calculation: Calculation) -> None:
        if CalculatorConfig.AUTO_SAVE:
            self.history.save()


class Calculator:
    """Coordinates validation, operations, history, and observers."""

    def __init__(self) -> None:
        CalculatorConfig.initialize()

        self.history = History()
        self.observers: list[CalculatorObserver] = []
        self.undo_stack: list[CalculatorMemento] = []
        self.redo_stack: list[CalculatorMemento] = []

    def register_observer(
        self,
        observer: CalculatorObserver,
    ) -> None:
        """Register an observer."""

        self.observers.append(observer)

    def remove_observer(
        self,
        observer: CalculatorObserver,
    ) -> None:
        """Remove a registered observer."""

        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(
        self,
        calculation: Calculation,
    ) -> None:
        """Notify all observers of a new calculation."""

        for observer in self.observers:
            observer.update(calculation)

    def save_state(self) -> None:
        """Save the current history before changing it."""

        memento = CalculatorMemento(
            self.history.calculations
        )

        self.undo_stack.append(memento)
        self.redo_stack.clear()

    def calculate(
        self,
        operation_name: str,
        first_value: object,
        second_value: object,
    ) -> float:
        """Validate inputs, execute an operation, and store the result."""

        first_number, second_number = validate_two_numbers(
            first_value,
            second_value,
        )

        operation = OperationFactory.create_operation(
            operation_name
        )

        result = operation.execute(
            first_number,
            second_number,
        )

        rounded_result = round(
            result,
            CalculatorConfig.PRECISION,
        )

        self.save_state()

        calculation = Calculation(
            operation=operation_name,
            operand1=first_number,
            operand2=second_number,
            result=rounded_result,
        )

        self.history.add(calculation)
        self.notify_observers(calculation)

        return rounded_result

    def undo(self) -> str:
        """Restore the previous history state."""

        if not self.undo_stack:
            return "Nothing to undo."

        current_state = CalculatorMemento(
            self.history.calculations
        )

        self.redo_stack.append(current_state)

        previous_state = self.undo_stack.pop()

        self.history.calculations = (
            previous_state.get_saved_history()
        )

        return "Undo successful."

    def redo(self) -> str:
        """Restore the most recently undone history state."""

        if not self.redo_stack:
            return "Nothing to redo."

        current_state = CalculatorMemento(
            self.history.calculations
        )

        self.undo_stack.append(current_state)

        next_state = self.redo_stack.pop()

        self.history.calculations = (
            next_state.get_saved_history()
        )

        return "Redo successful."

    def clear_history(self) -> str:
        """Save the current state and clear history."""

        if not self.history.calculations:
            return "History is already empty."

        self.save_state()
        self.history.clear()

        return "History cleared."

    def save_history(self) -> str:
        """Save history to CSV."""

        self.history.save()
        return "History saved."

    def load_history(self) -> str:
        """Load history from CSV."""

        self.save_state()
        self.history.load()

        return "History loaded."