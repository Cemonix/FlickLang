from flicklang.interpreter import Interpreter
from flicklang.lexer import Lexer
from flicklang.parser import Parser
from flicklang.ast import Assignment, Number, BinaryOp, UnaryOp


def test_basic_arithmetic_expression() -> None:
    expression = "3 + 4 * 2"

    tokens = Lexer(expression).tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    # Check if the AST matches the expected structure:
    #       +
    #      / \
    #     3   *
    #        / \
    #       4   2
    assert isinstance(program, BinaryOp), "Root of AST should be a BinaryOp."
    assert (
        isinstance(program.left, Number) and program.left.value == "3"
    ), "Left child of root should be Number(3)."
    assert isinstance(
        program.right, BinaryOp
    ), "Right child of root should be a BinaryOp."
    assert (
        isinstance(program.right.left, Number) and program.right.left.value == "4"
    ), "Left child of right BinaryOp should be Number(4)."
    assert (
        isinstance(program.right.right, Number) and program.right.right.value == "2"
    ), "Right child of right BinaryOp should be Number(2)."

    print("Test passed: Basic arithmetic expression parsed correctly.")


def test_parser_with_unary_and_binary_minus() -> None:
    test_cases = [
        {"input": "-3", "expected": UnaryOp},
        {"input": "3 - 2", "expected": BinaryOp},
        {"input": "-3 + 5", "expected": BinaryOp},
        {"input": "4 + -3", "expected": BinaryOp},
        {"input": "-3 * -2", "expected": BinaryOp},
        {"input": "-3 - -2", "expected": BinaryOp},
        {"input": "(-3 + 5) - 2", "expected": BinaryOp},
        {"input": "-(3 + 5)", "expected": UnaryOp},
        {"input": "--3", "expected": Number},
        {"input": "---3", "expected": UnaryOp},
    ]

    for case in test_cases:
        tokens = Lexer(case["input"]).tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        assert isinstance(
            program, case["expected"]
        ), f"Test failed for input '{case['input']}'. Expected {case['expected'].__name__}, got {type(program).__name__}."

    print("All parser tests with unary and binary minus passed.")


def test_variable_assignment() -> None:
    test_cases = [
        {"input": "x = 5", "expected": Assignment},
        {"input": "a = 10 x = a", "expected": Assignment},
    ]

    for case in test_cases:
        tokens = Lexer(case["input"]).tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        assert isinstance(
            program, case["expected"]
        ), f"Test failed for input '{case['input']}'. Expected {case['expected'].__name__}, got {type(program).__name__}."

    print("All parser tests with variable assignment passed.")


def test() -> None:
    tokens = Lexer(
        """
        array = [5, 3, 7, 10, -5, 3]
        array_len = 6
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
    ).tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(program)


if __name__ == "__main__":
    test()
