import pytest
from app.operations import OperationFactory
from app.exceptions import OperationError


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 5, 3, 8),
        ("subtract", 5, 3, 2),
        ("multiply", 5, 3, 15),
        ("divide", 6, 3, 2),
        ("power", 2, 3, 8),
        ("root", 27, 3, 3),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 25, 100, 25),
        ("abs_diff", 5, 10, 5),
    ],
)
def test_operations(operation, a, b, expected):
    op = OperationFactory.create_operation(operation)
    assert op.execute(a, b) == expected


def test_divide_by_zero():
    op = OperationFactory.create_operation("divide")
    with pytest.raises(OperationError):
        op.execute(5, 0)


def test_unknown_operation():
    with pytest.raises(OperationError):
        OperationFactory.create_operation("bad")