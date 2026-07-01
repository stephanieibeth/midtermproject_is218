from app.exceptions import OperationError


class Add:
    def execute(self, a, b):
        return a + b


class Subtract:
    def execute(self, a, b):
        return a - b


class Multiply:
    def execute(self, a, b):
        return a * b


class Divide:
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero.")
        return a / b


class Power:
    def execute(self, a, b):
        return a ** b


class Root:
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Root degree cannot be zero.")
        return a ** (1 / b)


class Modulus:
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot use modulus by zero.")
        return a % b


class IntegerDivision:
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot integer divide by zero.")
        return a // b


class Percentage:
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot calculate percentage with zero.")
        return (a / b) * 100


class AbsoluteDifference:
    def execute(self, a, b):
        return abs(a - b)


class OperationFactory:
    operations = {
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
        "power": Power,
        "root": Root,
        "modulus": Modulus,
        "int_divide": IntegerDivision,
        "percent": Percentage,
        "abs_diff": AbsoluteDifference,
    }

    @classmethod
    def create_operation(cls, operation_name):
        if operation_name not in cls.operations:
            raise OperationError(f"Unknown operation: {operation_name}")
        return cls.operations[operation_name]()