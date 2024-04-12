from flicklang.lexer import Lexer
from flicklang.parser import Parser
from flicklang.models import TokenType, Token
from flicklang.ast import Assignment, Number, BinaryOp, UnaryOp


def test_basic_arithmetic_expression() -> None:
    expression = "3 + 4 * 2"

    tokens = Lexer(expression).tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    # Check if the AST matches the expected structure:
    #       +
    #      / \
    #     3   *
    #        / \
    #       4   2
    assert isinstance(ast, BinaryOp), "Root of AST should be a BinaryOp."
    assert (
        isinstance(ast.left, Number) and ast.left.value == "3"
    ), "Left child of root should be Number(3)."
    assert isinstance(ast.right, BinaryOp), "Right child of root should be a BinaryOp."
    assert (
        isinstance(ast.right.left, Number) and ast.right.left.value == "4"
    ), "Left child of right BinaryOp should be Number(4)."
    assert (
        isinstance(ast.right.right, Number) and ast.right.right.value == "2"
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
        ast = parser.parse()

        assert isinstance(
            ast, case["expected"]
        ), f"Test failed for input '{case['input']}'. Expected {case['expected'].__name__}, got {type(ast).__name__}."

    print("All parser tests with unary and binary minus passed.")


def test_variable_assignment() -> None:
    test_cases = [
        {"input": "x = 5", "expected": Assignment},
        {"input": "a = 10 x = a", "expected": Assignment},
    ]

    for case in test_cases:
        tokens = Lexer(case["input"]).tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert isinstance(
            ast, case["expected"]
        ), f"Test failed for input '{case['input']}'. Expected {case['expected'].__name__}, got {type(ast).__name__}."

    print("All parser tests with variable assignment passed.")


if __name__ == "__main__":
    test_variable_assignment()
