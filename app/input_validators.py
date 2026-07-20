"""Input validation helpers for calculator commands."""

from math import isfinite
from numbers import Real

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


def validate_number(value: object) -> float:
    """
    Convert a value to a float and validate its allowed range.

    Args:
        value: The value entered by the user.

    Returns:
        The validated value as a float.

    Raises:
        ValidationError: If the value is not numeric, is not finite,
        or exceeds the configured maximum input value.
    """

    if isinstance(value, bool):
        raise ValidationError("Boolean values are not valid numbers.")

    if isinstance(value, Real):
        number = float(value)
    else:
        try:
            number = float(str(value).strip())
        except (TypeError, ValueError) as error:
            raise ValidationError(
                f"Invalid numeric input: {value}"
            ) from error

    if not isfinite(number):
        raise ValidationError(
            "Input must be a finite number."
        )

    if abs(number) > CalculatorConfig.MAX_INPUT_VALUE:
        raise ValidationError(
            "Input exceeds the maximum allowed value of "
            f"{CalculatorConfig.MAX_INPUT_VALUE}."
        )

    return number


def validate_two_numbers(
    first_value: object,
    second_value: object,
) -> tuple[float, float]:
    """
    Validate and return two numeric inputs.

    Args:
        first_value: The first calculator operand.
        second_value: The second calculator operand.

    Returns:
        A tuple containing two validated floats.
    """

    first_number = validate_number(first_value)
    second_number = validate_number(second_value)

    return first_number, second_number