from typing import List

from flicklang.ast import (
    ArrayIndex,
    ArrayIndexAssignment,
    ArrayLiteral,
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
    WhileLoop,
)
from flicklang.models import (
    Token,
    SyntaxTokenType,
    EOFToken,
    Keyword,
    Symbol,
    Fundamental,
    Operator,
    Comparison,
)


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
            self.current_token.type == Fundamental.IDENTIFIER
            and self.peek_token().type == Operator.ASSIGN
        ):
            variable_token = self.current_token
            self.eat(Fundamental.IDENTIFIER)
            self.eat(Operator.ASSIGN)
            assignment = Assignment(
                variable_name=Variable(variable_token.value),
                variable_value=self.expr(),
            )
            return assignment
        elif (
            self.current_token.type == Fundamental.IDENTIFIER
            and self.peek_token().type == Symbol.LBRACKET
        ):
            return self.parse_array_access_or_assignment()
        elif self.current_token.type == Keyword.P:
            return self.parse_print_statement()
        elif self.current_token.type == Keyword.IF:
            return self.parse_if_statement()
        elif self.current_token.type == Keyword.W:
            return self.parse_while_loop()
        else:
            return self.expr()

    def eat(self, token_type: SyntaxTokenType) -> None:
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
            return EOFToken(Fundamental.EOF)

    def factor(self) -> Node:
        """Parse a factor (number or parenthesized expression), reducing consecutive unary minus."""
        if self.current_token is None:
            raise Exception("Current token is None")

        # Count consecutive unary minus operators
        unary_minus_count = 0
        while self.current_token.type == Operator.MINUS:
            self.eat(Operator.MINUS)
            unary_minus_count += 1

        if self.current_token.type == Fundamental.NUMBER:
            node = Number(self.current_token, self.current_token.value)
            self.eat(Fundamental.NUMBER)
        elif self.current_token.type == Symbol.LPAREN:
            self.eat(Symbol.LPAREN)
            node = self.expr()
            self.eat(Symbol.RPAREN)
        elif (
            self.current_token.type == Fundamental.IDENTIFIER
            and self.peek_token().type == Symbol.LBRACKET
        ):
            node = self.parse_array_access_or_assignment()
        elif self.current_token.type == Symbol.LBRACKET:
            node = self.parse_array_literal()
        elif self.current_token.type == Fundamental.IDENTIFIER:
            node = Variable(self.current_token.value)
            self.eat(Fundamental.IDENTIFIER)
        elif self.current_token.type == Fundamental.STRING:
            node = String(self.current_token, self.current_token.value)
            self.eat(Fundamental.STRING)
        else:
            raise Exception(f"Unexpected token: {self.current_token.type}")

        if unary_minus_count % 2 == 1:
            return UnaryOp(op_token=Token(Operator.MINUS, "-"), operand=node)

        return node

    def term(self):
        """Parse a term (factor followed by zero or more multiplication/division)."""
        node: Node = self.factor()

        while self.current_token is not None and self.current_token.type in (
            Operator.MULTIPLY,
            Operator.DIVIDE,
            Operator.MODULO,
        ):
            token = self.current_token
            if token.type == Operator.MULTIPLY:
                self.eat(Operator.MULTIPLY)
            elif token.type == Operator.DIVIDE:
                self.eat(Operator.DIVIDE)
            elif token.type == Operator.MODULO:
                self.eat(Operator.MODULO)
            node = BinaryOp(left=node, op_token=token, right=self.factor())
        return node

    def expr(self):
        """Parse an expression (term followed by zero or more addition/subtraction)."""
        node = self.term()
        while self.current_token is not None and self.current_token.type in (
            Operator.PLUS,
            Operator.MINUS,
        ):
            token = self.current_token
            if token.type == Operator.PLUS:
                self.eat(Operator.PLUS)
            elif token.type == Operator.MINUS:
                self.eat(Operator.MINUS)
            node = BinaryOp(left=node, op_token=token, right=self.term())
        return node

    def parse_print_statement(self) -> Print:
        self.eat(Keyword.P)
        expr = self.expr()
        return Print(expr)

    def parse_comparison(self) -> Node:
        if self.current_token is None:
            raise Exception("Current token is None")

        node = self.expr()

        while self.current_token.type in (
            Comparison.EQ,
            Comparison.NEQ,
            Comparison.GR,
            Comparison.GRE,
            Comparison.LS,
            Comparison.LSE,
        ):
            token = self.current_token
            self.eat(token.type)
            node = ComparisonOp(left=node, operator=token, right=self.expr())

        return node

    def parse_if_statement(self) -> If:
        if self.current_token is None:
            raise Exception("Current token is None")

        (
            self.eat(Keyword.IF)
            if self.current_token.type == Keyword.IF
            else self.eat(Keyword.ELI)
        )
        condition = self.parse_comparison()

        true_block = self.parse_block()

        # Only if statement
        if self.current_token is None:
            return If(condition, true_block, None)

        false_block = None
        if self.current_token.type == Keyword.ELI:
            false_block = self.parse_if_statement()
        elif self.current_token.type == Keyword.EL:
            self.eat(Keyword.EL)
            false_block = self.parse_block()

        return If(condition, true_block, false_block)

    def parse_block(self) -> List[Node]:
        if self.current_token is None:
            raise Exception("Current token is None")

        statements = []
        self.eat(Symbol.BLOCK_START)
        while not self.current_token.type in (Symbol.BLOCK_END, Fundamental.EOF):
            statements.append(self.parse_statement())
        self.eat(Symbol.BLOCK_END)
        return statements

    def parse_array_literal(self) -> ArrayLiteral:
        if self.current_token is None:
            raise Exception("Current token is None")

        elements = []
        self.eat(Symbol.LBRACKET)
        if not self.current_token.type == Symbol.RBRACKET:
            elements.append(self.expr())
            while self.current_token.type == Symbol.COMMA:
                self.eat(Symbol.COMMA)
                elements.append(self.expr())
        self.eat(Symbol.RBRACKET)
        return ArrayLiteral(elements)

    def parse_array_access_or_assignment(self) -> ArrayIndexAssignment | ArrayIndex:
        if self.current_token is None:
            raise Exception("Current token is None")

        variable_token = self.current_token
        self.eat(Fundamental.IDENTIFIER)
        self.eat(Symbol.LBRACKET)
        index = self.expr()
        self.eat(Symbol.RBRACKET)

        if self.current_token.type == Operator.ASSIGN:
            self.eat(Operator.ASSIGN)
            value = self.expr()
            return ArrayIndexAssignment(
                array=Variable(variable_token.value), index=index, value=value
            )
        else:
            return ArrayIndex(array=Variable(variable_token.value), index=index)

    def parse_while_loop(self) -> WhileLoop:
        if self.current_token is None:
            raise Exception("Current token is None")

        self.eat(Keyword.W)
        condition = self.parse_comparison()
        body = self.parse_block()

        return WhileLoop(condition, body)
