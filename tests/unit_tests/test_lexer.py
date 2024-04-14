import pytest

from flicklang.exceptions import TokenizationError
from flicklang.lexer import Lexer
from flicklang.models import (
    Comparison,
    CompoundOperator,
    EOFToken,
    Keyword,
    Token,
    Fundamental,
    Operator,
    Symbol,
)


def test_tokenize_numbers() -> None:
    lexer = Lexer("123 456.789")
    tokens = lexer.tokenize()
    assert tokens == [
        Token(Fundamental.NUMBER, "123"),
        Token(Fundamental.NUMBER, "456.789"),
        EOFToken(Fundamental.EOF),
    ]


def test_tokenize_operators() -> None:
    lexer = Lexer("+ - * / %")
    tokens = lexer.tokenize()
    expected = [
        Token(Operator.PLUS, "+"),
        Token(Operator.MINUS, "-"),
        Token(Operator.MULTIPLY, "*"),
        Token(Operator.DIVIDE, "/"),
        Token(Operator.MODULO, "%"),
        EOFToken(Fundamental.EOF),
    ]
    assert tokens == expected


def test_skip_comments() -> None:
    lexer = Lexer(".. This is a comment\n123")
    tokens = lexer.tokenize()
    assert tokens == [Token(Fundamental.NUMBER, "123"), EOFToken(Fundamental.EOF)]


def test_tokenize_strings() -> None:
    lexer = Lexer("'hello' 'world'")
    tokens = lexer.tokenize()
    assert tokens == [
        Token(Fundamental.STRING, "hello"),
        Token(Fundamental.STRING, "world"),
        EOFToken(Fundamental.EOF),
    ]


def test_unterminated_string() -> None:
    lexer = Lexer("'hello")
    with pytest.raises(TokenizationError):
        lexer.tokenize()


def test_complex_arithmetic_expression() -> None:
    lexer = Lexer("varName = 3 * (4 + 5)")
    tokens = lexer.tokenize()
    expected = [
        Token(Fundamental.IDENTIFIER, "varName"),
        Token(Operator.ASSIGN, "="),
        Token(Fundamental.NUMBER, "3"),
        Token(Operator.MULTIPLY, "*"),
        Token(Symbol.LPAREN, "("),
        Token(Fundamental.NUMBER, "4"),
        Token(Operator.PLUS, "+"),
        Token(Fundamental.NUMBER, "5"),
        Token(Symbol.RPAREN, ")"),
        EOFToken(Fundamental.EOF),
    ]
    assert tokens == expected


def test_complex_expression() -> None:
    lexer = Lexer("varName = 3 * (4 + 5) if varName gr 13 {p 'hello'}")
    tokens = lexer.tokenize()
    expected = [
        Token(Fundamental.IDENTIFIER, "varName"),
        Token(Operator.ASSIGN, "="),
        Token(Fundamental.NUMBER, "3"),
        Token(Operator.MULTIPLY, "*"),
        Token(Symbol.LPAREN, "("),
        Token(Fundamental.NUMBER, "4"),
        Token(Operator.PLUS, "+"),
        Token(Fundamental.NUMBER, "5"),
        Token(Symbol.RPAREN, ")"),
        Token(Keyword.IF, "if"),
        Token(Fundamental.IDENTIFIER, "varName"),
        Token(Comparison.GR, "gr"),
        Token(Fundamental.NUMBER, "13"),
        Token(Symbol.BLOCK_START, "{"),
        Token(Keyword.P, "p"),
        Token(Fundamental.STRING, "hello"),
        Token(Symbol.BLOCK_END, "}"),
        EOFToken(Fundamental.EOF),
    ]
    assert tokens == expected


def test_tokenize_compound_operators() -> None:
    lexer = Lexer("+= -= *= /= %=")
    tokens = lexer.tokenize()
    expected = [
        Token(CompoundOperator.PLUS_ASSIGN, "+="),
        Token(CompoundOperator.MINUS_ASSIGN, "-="),
        Token(CompoundOperator.MULTIPLY_ASSIGN, "*="),
        Token(CompoundOperator.DIVIDE_ASSIGN, "/="),
        Token(CompoundOperator.MODULO_ASSIGN, "%="),
        EOFToken(Fundamental.EOF),
    ]
    assert tokens == expected, "Compound operators were not tokenized correctly."
