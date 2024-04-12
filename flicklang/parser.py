from typing import List

from flicklang.ast import (
    Assignment,
    ComparisonOp,
    If,
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

        while (
            not isinstance(self.current_token, EOFToken)
            and self.current_token is not None
        ):
            statement = self.parse_statement()
            if statement is not None:
                statements.append(statement)

        return Program(statements)

    def parse_statement(self) -> Node:
        if self.current_token is None:
            raise Exception("Current token is None")

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
            return assignment
        elif self.current_token.type == TokenType.PRINT:
            return self.parse_print_statement()
        elif self.current_token.type == TokenType.IF:
            return self.parse_if_statement()
        else:
            return Print(self.expr())

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

    def parse_comparison(self) -> Node:
        if self.current_token is None:
            raise Exception("Current token is None")

        node = self.expr()

        while self.current_token.type in (
            TokenType.EQ,
            TokenType.NEQ,
            TokenType.GR,
            TokenType.GRE,
            TokenType.LS,
            TokenType.LSE,
        ):
            token = self.current_token
            self.eat(token.type)
            node = ComparisonOp(left=node, operator=token, right=self.expr())

        return node

    def parse_if_statement(self) -> If:
        if self.current_token is None:
            raise Exception("Current token is None")

        self.eat(TokenType.IF) if self.current_token.type == TokenType.IF else self.eat(TokenType.ELI)
        condition = self.parse_comparison()

        true_block = self.parse_block()

        false_block = None
        if self.current_token.type == TokenType.ELI:
            false_block = self.parse_if_statement()
        elif self.current_token.type == TokenType.EL:
            self.eat(TokenType.EL)
            false_block = self.parse_block()

        return If(condition, true_block, false_block)

    def parse_block(self) -> List[Node]:
        if self.current_token is None:
            raise Exception("Current token is None")

        statements = []
        self.eat(TokenType.BLOCK_START)
        while not self.current_token.type in (TokenType.BLOCK_END, TokenType.EOF):
            statements.append(self.parse_statement())
        self.eat(TokenType.BLOCK_END)
        return statements
