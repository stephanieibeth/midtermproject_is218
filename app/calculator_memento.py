"""Memento object used to store calculator history snapshots."""

from app.calculation import Calculation


class CalculatorMemento:
    """Stores a copy of calculator history for undo and redo."""

    def __init__(
        self,
        calculations: list[Calculation],
    ) -> None:
        self._calculations = list(calculations)

    def get_saved_history(self) -> list[Calculation]:
        """Return a copy of the saved calculation history."""

        return list(self._calculations)