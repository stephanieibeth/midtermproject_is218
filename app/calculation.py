"""Calculation model for storing completed arithmetic operations."""

from datetime import datetime


class Calculation:
    """Represents one completed calculator operation."""

    def __init__(
        self,
        operation: str,
        operand1: float,
        operand2: float,
        result: float,
        timestamp: str | None = None,
    ) -> None:
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert the calculation into a dictionary for pandas."""

        return {
            "operation": self.operation,
            "operand1": self.operand1,
            "operand2": self.operand2,
            "result": self.result,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Calculation":
        """Create a Calculation object from dictionary or CSV data."""

        return cls(
            operation=str(data["operation"]),
            operand1=float(data["operand1"]),
            operand2=float(data["operand2"]),
            result=float(data["result"]),
            timestamp=str(data["timestamp"]),
        )

    def __str__(self) -> str:
        """Return a readable version of the calculation."""

        return (
            f"{self.operation}("
            f"{self.operand1}, {self.operand2}) = {self.result}"
        )

    def __eq__(self, other: object) -> bool:
        """Allow two Calculation objects to be compared in tests."""

        if not isinstance(other, Calculation):
            return NotImplemented

        return self.to_dict() == other.to_dict()