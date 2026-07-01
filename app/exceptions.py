class CalculatorError(Exception):
    """Base exception for the calculator."""
    pass


class OperationError(CalculatorError):
    """Raised when an arithmetic operation cannot be completed."""
    pass


class ValidationError(CalculatorError):
    """Raised when the user's input is invalid."""
    pass


class ConfigurationError(CalculatorError):
    """Raised when configuration settings are invalid."""
    pass