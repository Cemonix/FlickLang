import pytest

from flicklang.interpreter import Interpreter
from flicklang.ast import Number, BinaryOp, Assignment, Variable
from flicklang.models import Fundamental, Operator, Token


def test_number() -> None:
    interpreter = Interpreter()
    result = interpreter.visit(Number(token=Token(Fundamental.IDENTIFIER, '5'), value='5'))
    assert result == 5


def test_binary_operation() -> None:
    interpreter = Interpreter()
    left = Number(token=Token(Fundamental.IDENTIFIER, '10'), value='10')
    right = Number(token=Token(Fundamental.IDENTIFIER, '5'), value='5')
    node = BinaryOp(left=left, op_token=Token(Operator.PLUS, "+"), right=right)
    result = interpreter.visit(node)
    assert result == 15


def test_assignment() -> None:
    interpreter = Interpreter()
    name = Variable(name='x')
    value = Number(token=Token(Fundamental.IDENTIFIER, '10'), value='10')
    node = Assignment(variable_name=name, variable_value=value)
    interpreter.visit(node)
    assert interpreter.environment['x'] == 10
