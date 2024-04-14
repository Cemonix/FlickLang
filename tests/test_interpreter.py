import pytest

from flicklang.interpreter import Interpreter
from flicklang.ast import Number, BinaryOp, Assignment, Variable
from flicklang.models import Operator, Token


def test_number() -> None:
    interpreter = Interpreter()
    result = interpreter.visit(Number(value='5'))
    assert result == 5


def test_binary_operation() -> None:
    interpreter = Interpreter()
    left = Number(value='10')
    right = Number(value='5')
    node = BinaryOp(left=left, op_token=Token(Operator.PLUS, "+"), right=right)
    result = interpreter.visit(node)
    assert result == 15


def test_assignment() -> None:
    interpreter = Interpreter()
    name = Variable(name='x')
    value = Number(value='10')
    node = Assignment(variable_name=name, variable_value=value)
    interpreter.visit(node)
    assert interpreter.environment['x'] == 10


def test_bubble_sort() -> None:
    from flicklang.lexer import Lexer
    from flicklang.parser import Parser
    source_code = """
        array = [5, 3, 7, 10]
        array_len = 4
        .. Bubble sort
        i = 0
        w i ls array_len
        {
            j = 0
            w j ls array_len
            {
                if array[i] ls array[j]
                {
                    temp = array[i]
                    array[i] = array[j]
                    array[j] = temp
                }
                j = j + 1
            }
            i = i + 1 
        }

        i = 0
        w i ls array_len
        {
            p array[i]
            i = i + 1
        }
    """
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(program)