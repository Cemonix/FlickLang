import pytest

from flicklang.parser import Parser
from flicklang.models import (
    Comparison,
    CompoundOperator,
    Keyword,
    Token,
    Fundamental,
    Operator,
    Symbol,
    EOFToken,
)
from flicklang.ast import (
    CompoundAssignment,
    If,
    Program,
    Number,
    BinaryOp,
    Assignment,
    Variable,
    WhileLoop,
)


def test_parse_number() -> None:
    tokens = [Token(Fundamental.NUMBER, "42"), EOFToken(Fundamental.EOF)]
    parser = Parser(tokens)
    result = parser.parse()

    assert isinstance(result, Program)
    assert isinstance(result.statements[0], Number)
    assert result.statements[0].value == "42"


def test_parse_arithmetic_expression() -> None:
    tokens = [
        Token(Fundamental.NUMBER, "3"),
        Token(Operator.PLUS, "+"),
        Token(Fundamental.NUMBER, "4"),
        Token(Operator.MULTIPLY, "*"),
        Token(Fundamental.NUMBER, "5"),
        EOFToken(Fundamental.EOF),
    ]
    parser = Parser(tokens)
    result = parser.parse()

    # Expecting (3 + (4 * 5))
    assert isinstance(result, Program)
    assert isinstance(result.statements[0], BinaryOp)
    assert result.statements[0].op_token.value == "+"
    assert isinstance(result.statements[0].right, BinaryOp)
    assert result.statements[0].right.op_token.value == "*"


def test_parse_variable_assignment() -> None:
    tokens = [
        Token(Fundamental.IDENTIFIER, "x"),
        Token(Operator.ASSIGN, "="),
        Token(Fundamental.NUMBER, "10"),
        EOFToken(Fundamental.EOF),
    ]
    parser = Parser(tokens)
    result = parser.parse()

    assert isinstance(result, Program)
    assert isinstance(result.statements[0], Assignment)
    assert isinstance(result.statements[0].variable_name, Variable)
    assert result.statements[0].variable_name.name == "x"
    assert isinstance(result.statements[0].variable_value, Number)
    assert result.statements[0].variable_value.value == "10"


def test_complex_expression_parsing() -> None:
    tokens = [
        Token(Fundamental.NUMBER, "2"),
        Token(Operator.PLUS, "+"),
        Token(Fundamental.NUMBER, "3"),
        Token(Operator.MULTIPLY, "*"),
        Token(Symbol.LPAREN, "("),
        Token(Fundamental.NUMBER, "4"),
        Token(Operator.MINUS, "-"),
        Token(Fundamental.NUMBER, "1"),
        Token(Symbol.RPAREN, ")"),
        EOFToken(Fundamental.EOF),
    ]
    parser = Parser(tokens)
    result = parser.parse()

    # Expecting 2 + 3 * (4 - 1)
    assert isinstance(result, Program)
    assert isinstance(result.statements[0], BinaryOp)
    assert result.statements[0].op_token.value == "+"
    assert isinstance(result.statements[0].right, BinaryOp)
    assert result.statements[0].right.op_token.value == "*"
    assert isinstance(result.statements[0].right.right, BinaryOp)
    assert result.statements[0].right.right.op_token.value == "-"


def test_nested_loops():
    tokens = [
        Token(Keyword.W, "w"),
        Token(Fundamental.IDENTIFIER, "x"),
        Token(Comparison.LS, "ls"),
        Token(Fundamental.NUMBER, "10"),
        Token(Symbol.BLOCK_START, "{"),
        Token(Keyword.W, "w"),
        Token(Fundamental.IDENTIFIER, "y"),
        Token(Comparison.LS, "ls"),
        Token(Fundamental.NUMBER, "5"),
        Token(Symbol.BLOCK_START, "{"),
        Token(Fundamental.IDENTIFIER, "z"),
        Token(Operator.ASSIGN, "="),
        Token(Fundamental.IDENTIFIER, "z"),
        Token(Operator.PLUS, "+"),
        Token(Fundamental.NUMBER, "1"),
        Token(Symbol.BLOCK_END, "}"),
        Token(Symbol.BLOCK_END, "}"),
        EOFToken(Fundamental.EOF),
    ]
    parser = Parser(tokens)
    result = parser.parse()

    assert isinstance(result, Program)
    assert isinstance(result.statements[0], WhileLoop)
    assert isinstance(result.statements[0].body[0], WhileLoop)
    assert isinstance(result.statements[0].body[0].body[0], Assignment)


def test_complex_conditionals() -> None:
    tokens = [
        Token(Keyword.IF, "if"),
        Token(Fundamental.IDENTIFIER, "x"),
        Token(Comparison.EQ, "eq"),
        Token(Fundamental.NUMBER, "10"),
        Token(Symbol.BLOCK_START, "{"),
        Token(Fundamental.IDENTIFIER, "result"),
        Token(Operator.ASSIGN, "="),
        Token(Fundamental.STRING, "ten"),
        Token(Symbol.BLOCK_END, "}"),
        Token(Keyword.ELI, "eli"),
        Token(Fundamental.IDENTIFIER, "x"),
        Token(Comparison.LS, "ls"),
        Token(Fundamental.NUMBER, "10"),
        Token(Symbol.BLOCK_START, "{"),
        Token(Fundamental.IDENTIFIER, "result"),
        Token(Operator.ASSIGN, "="),
        Token(Fundamental.STRING, "less than ten"),
        Token(Symbol.BLOCK_END, "}"),
        Token(Keyword.EL, "el"),
        Token(Symbol.BLOCK_START, "{"),
        Token(Fundamental.IDENTIFIER, "result"),
        Token(Operator.ASSIGN, "="),
        Token(Fundamental.STRING, "greater"),
        Token(Symbol.BLOCK_END, "}"),
        EOFToken(Fundamental.EOF),
    ]
    parser = Parser(tokens)
    result = parser.parse()

    # Validate proper linkage and structure of if-elif-else blocks
    assert isinstance(result, Program)
    assert isinstance(result.statements[0], If)
    assert isinstance(result.statements[0].false_branch, If)
    if isinstance(result.statements[0].false_branch.false_branch, list):
        assert isinstance(result.statements[0].false_branch.false_branch[0], Assignment)
    else:
        assert (
            False
        ), "The false branch of the 'elif' should be a list of Nodes or None if there's no 'else'"


def test_parse_compound_assignments() -> None:
    tokens = [
        Token(Fundamental.IDENTIFIER, "x"),
        Token(CompoundOperator.PLUS_ASSIGN, "+="),
        Token(Fundamental.NUMBER, "5"),
        EOFToken(Fundamental.EOF),
    ]
    parser = Parser(tokens)
    result = parser.parse()

    assert isinstance(result, Program), "The result should be a Program node."
    assert isinstance(
        result.statements[0], CompoundAssignment
    ), "The first statement should be a CompoundAssignment."
    assert (
        result.statements[0].op_token.type == CompoundOperator.PLUS_ASSIGN
    ), "Operator token type mismatch."
    assert isinstance(
        result.statements[0].variable_name, Variable
    ), "The variable_name attribute of the CompoundAssignment should be an instance of Variable."
    assert (
        result.statements[0].variable_name.name == "x"
    ), f"Expected the variable name to be 'x', but got {result.statements[0].variable_name.name}."
    assert isinstance(
        result.statements[0].variable_value, Number
    ), "The variable_value attribute of the CompoundAssignment should be an instance of Number."
    assert (
        result.statements[0].variable_value.value == "5"
    ), f"Expected the variable value to be '5', but got {result.statements[0].variable_value.value}."
