import pytest

from flicklang.interpreter import Interpreter
from flicklang.ast import CompoundAssignment, Number, BinaryOp, Assignment, Variable
from flicklang.models import CompoundOperator, Operator, Token


def test_number() -> None:
    interpreter = Interpreter()
    result = interpreter.visit(Number(value="5"))
    assert result == 5


def test_binary_operation() -> None:
    interpreter = Interpreter()
    left = Number(value="10")
    right = Number(value="5")
    node = BinaryOp(left=left, op_token=Token(Operator.PLUS, "+"), right=right)
    result = interpreter.visit(node)
    assert result == 15


def test_assignment() -> None:
    interpreter = Interpreter()
    name = Variable(name="x")
    value = Number(value="10")
    node = Assignment(variable_name=name, variable_value=value)
    interpreter.visit(node)
    assert interpreter.environment["x"] == 10


def test_interpret_compound_assignments() -> None:
    interpreter = Interpreter()
    interpreter.environment = {"x": 10}
    compound_assign_node = CompoundAssignment(
        variable_name=Variable(name="x"),
        op_token=Token(CompoundOperator.PLUS_ASSIGN, "+="),
        variable_value=Number(value="5"),
    )
    interpreter.visit(compound_assign_node)
    assert (
        interpreter.environment["x"] == 15
    ), "Compound assignment failed to update environment correctly."
