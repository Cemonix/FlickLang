from typing import List

from flicklang.ast import (
    Assignment,
    Node,
    Number,
    BinaryOp,
    Print,
    Program,
    String,
    UnaryOp,
    Variable,
)
from flicklang.models import EOFToken, Token, TokenType


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current_token: Token | None = None
        self.pos = -1
        self.advance()

    def parse(self) -> Program:
        statements: List[Node] = []

        while not isinstance(self.current_token, EOFToken) and self.current_token is not None:
            if (
                self.current_token.type == TokenType.IDENTIFIER
                and self.peek_token().type == TokenType.ASSIGN
            ):
                variable_token = self.current_token
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.ASSIGN)
                assignment = Assignment(
                    variable_name=Variable(variable_token), variable_value=self.expr()
                )
                statements.append(assignment)
            elif self.current_token.type == TokenType.PRINT:
                statements.append(self.parse_print_statement())
            else:
                expr = self.expr()
                statements.append(Print(expr))

        return Program(statements)

    def eat(self, token_type: TokenType) -> None:
        if self.current_token is None:
            raise Exception("Current token is None")

        if self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(
                f"Expected token {token_type}, got {self.current_token.type}"
            )

    def advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def peek_token(self) -> Token | EOFToken:
        peek_pos = self.pos + 1
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        else:
            return EOFToken(TokenType.EOF, None)

    def factor(self) -> Node:
        """Parse a factor (number or parenthesized expression), reducing consecutive unary minus."""
        if self.current_token is None:
            raise Exception("Current token is None")

        # Count consecutive unary minus operators
        unary_minus_count = 0
        while self.current_token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            unary_minus_count += 1

        if self.current_token.type == TokenType.NUMBER:
            node = Number(self.current_token)
            self.eat(TokenType.NUMBER)
        elif self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
        elif self.current_token.type == TokenType.IDENTIFIER:
            node = Variable(self.current_token)
            self.eat(TokenType.IDENTIFIER)
        elif self.current_token.type == TokenType.STRING:
            node = String(self.current_token)
            self.eat(TokenType.STRING)
        else:
            raise Exception(f"Unexpected token: {self.current_token.type}")

        if unary_minus_count % 2 == 1:
            return UnaryOp(op_token=Token(TokenType.MINUS, "-"), operand=node)

        return node

    def term(self):
        """Parse a term (factor followed by zero or more multiplication/division)."""
        node: Node = self.factor()

        while self.current_token is not None and self.current_token.type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            node = BinaryOp(left=node, op_token=token, right=self.factor())
        return node

    def expr(self):
        """Parse an expression (term followed by zero or more addition/subtraction)."""
        node = self.term()
        while self.current_token is not None and self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinaryOp(left=node, op_token=token, right=self.term())
        return node

    def parse_print_statement(self) -> Print:
        self.eat(TokenType.PRINT)
        expr = self.expr()
        return Print(expr)
