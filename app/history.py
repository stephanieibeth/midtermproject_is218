"""Calculation history management and CSV persistence."""

from pathlib import Path

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError


class History:
    """Stores completed calculations and manages CSV persistence."""

    def __init__(self) -> None:
        self.calculations: list[Calculation] = []

    def add(self, calculation: Calculation) -> None:
        """Add a calculation and enforce the maximum history size."""

        self.calculations.append(calculation)

        if len(self.calculations) > CalculatorConfig.MAX_HISTORY_SIZE:
            self.calculations.pop(0)

    def clear(self) -> None:
        """Remove all calculations from history."""

        self.calculations.clear()

    def __len__(self) -> int:
        """Return the number of stored calculations."""

        return len(self.calculations)

    def __iter__(self):
        """Allow iteration over stored calculations."""

        return iter(self.calculations)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert calculation history into a pandas DataFrame."""

        columns = [
            "operation",
            "operand1",
            "operand2",
            "result",
            "timestamp",
        ]

        data = [
            calculation.to_dict()
            for calculation in self.calculations
        ]

        return pd.DataFrame(data, columns=columns)

    def save(self, file_path: Path | None = None) -> None:
        """Save calculation history to a CSV file."""

        target_file = file_path or CalculatorConfig.HISTORY_FILE

        try:
            target_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            dataframe = self.to_dataframe()

            dataframe.to_csv(
                target_file,
                index=False,
                encoding=CalculatorConfig.DEFAULT_ENCODING,
            )

        except (OSError, ValueError, pd.errors.ParserError) as error:
            raise OperationError(
                f"Could not save calculation history: {error}"
            ) from error

    def load(self, file_path: Path | None = None) -> None:
        """Load calculation history from a CSV file."""

        target_file = file_path or CalculatorConfig.HISTORY_FILE

        if not target_file.exists():
            raise OperationError(
                f"History file does not exist: {target_file}"
            )

        try:
            dataframe = pd.read_csv(
                target_file,
                encoding=CalculatorConfig.DEFAULT_ENCODING,
            )

            required_columns = {
                "operation",
                "operand1",
                "operand2",
                "result",
                "timestamp",
            }

            if not required_columns.issubset(dataframe.columns):
                raise OperationError(
                    "History file is missing required columns."
                )

            loaded_calculations = [
                Calculation.from_dict(row.to_dict())
                for _, row in dataframe.iterrows()
            ]

            self.calculations = loaded_calculations

        except OperationError:
            raise

        except (
            OSError,
            ValueError,
            KeyError,
            pd.errors.ParserError,
            pd.errors.EmptyDataError,
        ) as error:
            raise OperationError(
                f"Could not load calculation history: {error}"
            ) from error

    def display(self) -> str:
        """Return history as readable text."""

        if not self.calculations:
            return "No calculation history available."

        return "\n".join(
            f"{index}. {calculation}"
            for index, calculation in enumerate(
                self.calculations,
                start=1,
            )
        )