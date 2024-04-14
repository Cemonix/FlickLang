from typing import List, cast

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
from flicklang.exceptions import ParsingError
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
    comparison_types = {item for item in Comparison}

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current_token: Token | EOFToken = EOFToken(Fundamental.EOF)
        self.pos = -1
        self.advance()

    def advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = EOFToken(Fundamental.EOF)

    def eat(self, token_type: SyntaxTokenType) -> None:
        if isinstance(self.current_token, EOFToken):
            raise ParsingError(f"Expected {token_type} but found EOF", self.current_token)

        if self.current_token.type != token_type:
            raise ParsingError(
                f"Expected {token_type}, but found {self.current_token.type}",
                self.current_token
            )
    
        self.advance()

    def peek_token(self) -> Token | EOFToken:
        peek_pos = self.pos + 1
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        else:
            return EOFToken(Fundamental.EOF)

    def parse(self) -> Program:
        statements: List[Node] = []
        while not isinstance(self.current_token, EOFToken):
            statement = self.parse_statement()
            if statement is not None:
                statements.append(statement)
            else:
                raise ParsingError(
                    "Unexpected token while parsing statements.", self.current_token
                )

        if isinstance(self.current_token, EOFToken) and self.pos < len(self.tokens) - 1:
            raise ParsingError("Unexpected end of file.", self.current_token)

        return Program(statements)

    def parse_statement(self) -> Node:
        """
        Parses a single statement based on the current token.
        """
        if isinstance(self.current_token, EOFToken):
            raise ParsingError(
                "Unexpected EOF while parsing statements.", self.current_token
            )

        if self.current_token.type == Fundamental.IDENTIFIER:
            return self.parse_identifier_starting_statement()
        elif self.current_token.type == Keyword.P:
            return self.parse_print_statement()
        elif self.current_token.type == Keyword.IF:
            return self.parse_if_statement()
        elif self.current_token.type == Keyword.W:
            return self.parse_while_loop_statement()
        else:
            return self.expression()

    def parse_identifier_starting_statement(self) -> Node:
        """
        Handles statements that start with an identifier which could be an assignment or array access.
        """
        next_token = self.peek_token()
        if next_token.type == Operator.ASSIGN:
            return self.parse_assignment()
        elif next_token.type == Symbol.LBRACKET:
            return self.parse_array_access_or_assignment()

        raise ParsingError("Invalid syntax after identifier.", self.current_token)

    def parse_if_statement(self) -> If:
        if isinstance(self.current_token, EOFToken):
            raise ParsingError(
                "Unexpected EOF while parsing if statement.", self.current_token
            )

        (
            self.eat(Keyword.IF)
            if self.current_token.type == Keyword.IF
            else self.eat(Keyword.ELI)
        )

        condition = self.parse_comparison()
        true_block = self.parse_block()

        # If statement ending program
        if isinstance(self.current_token, EOFToken):
            return If(condition, true_block, None)

        false_block = None
        if self.current_token.type == Keyword.ELI:
            false_block = self.parse_if_statement()
        elif self.current_token.type == Keyword.EL:
            self.eat(Keyword.EL)
            false_block = self.parse_block()

        return If(condition, true_block, false_block)

    def parse_while_loop_statement(self) -> WhileLoop:
        if isinstance(self.current_token, EOFToken):
            raise ParsingError(
                "Unexpected EOF while parsing while loop statement.", self.current_token
            )

        self.eat(Keyword.W)
        condition = self.parse_comparison()
        body = self.parse_block()

        return WhileLoop(condition, body)

    def parse_print_statement(self) -> Print:
        self.eat(Keyword.P)
        expressions = [self.expression()]

        while (
            not isinstance(self.current_token, EOFToken)
            and self.current_token.type == Symbol.COMMA
        ):
            self.eat(Symbol.COMMA)
            expressions.append(self.expression())

        return Print(expressions)

    def parse_block(self) -> List[Node]:
        statements = []
        self.eat(Symbol.BLOCK_START)
        while self.current_token.type != Symbol.BLOCK_END:
            if isinstance(self.current_token, EOFToken):
                raise ParsingError(
                    "Unexpected EOF while parsing array literal.", self.current_token
                )
            statements.append(self.parse_statement())
        self.eat(Symbol.BLOCK_END)
        return statements
    
    def parse_assignment(self) -> Node:
        """
        Parses an assignment statement.
        """
        if isinstance(self.current_token, EOFToken):
            raise ParsingError(
                "Unexpected EOF while parsing assignment.", self.current_token
            )

        identifier = self.current_token
        self.eat(Fundamental.IDENTIFIER)
        self.eat(Operator.ASSIGN)
        return Assignment(
            variable_name=Variable(identifier.value),
            variable_value=self.expression(),
        )
    
    def parse_comparison(self) -> Node:
        if isinstance(self.current_token, EOFToken):
            raise ParsingError(
                "Unexpected EOF while parsing comparison.", self.current_token
            )

        node = self.expression()

        while self.current_token.type in Parser.comparison_types:
            token = self.current_token
            self.eat(token.type)
            node = ComparisonOp(left=node, operator=token, right=self.expression())

        return node
    
    def parse_array_literal(self) -> ArrayLiteral:
        elements = []
        self.eat(Symbol.LBRACKET)

        if isinstance(self.current_token, EOFToken):
            raise ParsingError(
                "Unexpected EOF while parsing array literal.", self.current_token
            )
        
        if not self.current_token.type == Symbol.RBRACKET:
            elements.append(self.expression())
            while self.current_token.type == Symbol.COMMA:
                self.eat(Symbol.COMMA)
                elements.append(self.expression())

        self.eat(Symbol.RBRACKET)
        return ArrayLiteral(elements)
    
    def parse_array_access_or_assignment(self) -> ArrayIndexAssignment | ArrayIndex:
        if isinstance(self.current_token, EOFToken):
            raise ParsingError(
                "Unexpected EOF while parsing statements.", self.current_token
            )

        variable_token = self.current_token
        self.eat(Fundamental.IDENTIFIER)
        self.eat(Symbol.LBRACKET)
        index = self.expression()
        self.eat(Symbol.RBRACKET)

        if self.current_token.type == Operator.ASSIGN:
            self.eat(Operator.ASSIGN)
            value = self.expression()
            return ArrayIndexAssignment(
                array=Variable(variable_token.value), index=index, value=value
            )
        else:
            return ArrayIndex(array=Variable(variable_token.value), index=index)
    
    def expression(self) -> Node | BinaryOp:
        """Parse an expression (term followed by zero or more addition/subtraction)."""
        node = self.term()

        while self.current_token.type in (
            Operator.PLUS,
            Operator.MINUS,
        ):
            if isinstance(self.current_token, EOFToken):
                raise ParsingError(
                    "Unexpected EOF while parsing expression.", self.current_token
                )
            
            token = self.current_token
            if token.type == Operator.PLUS:
                self.eat(Operator.PLUS)
            elif token.type == Operator.MINUS:
                self.eat(Operator.MINUS)

            node = BinaryOp(left=node, op_token=token, right=self.term())
        return node
    
    def term(self) -> Node | BinaryOp:
        """Parse a term (factor followed by zero or more multiplication/division)."""
        node: Node = self.factor()

        while self.current_token.type in (Operator.MULTIPLY, Operator.DIVIDE, Operator.MODULO):
            if isinstance(self.current_token, EOFToken):
                raise ParsingError(
                    "Unexpected EOF while parsing term.", self.current_token
                )
            
            token = self.current_token
            if token.type == Operator.MULTIPLY:
                self.eat(Operator.MULTIPLY)
            elif token.type == Operator.DIVIDE:
                self.eat(Operator.DIVIDE)
            elif token.type == Operator.MODULO:
                self.eat(Operator.MODULO)

            node = BinaryOp(left=node, op_token=token, right=self.factor())
        return node
    
    def factor(self) -> Node:
        """Parse a factor (number or parenthesized expression), reducing consecutive unary minus."""
        # Count consecutive unary minus operators
        unary_minus_count = 0
        while self.current_token.type == Operator.MINUS:
            self.eat(Operator.MINUS)
            unary_minus_count += 1

        node = self.parse_simple_factor()

        # Apply unary minus if there were an odd number of them
        if unary_minus_count % 2 == 1:
            return UnaryOp(op_token=Token(Operator.MINUS, "-"), operand=node)

        return node
    
    def parse_simple_factor(self) -> Node:
        """Parse a simple factor without unary minus handling."""
        self.current_token = cast(Token, self.current_token)
        if self.current_token.type == Fundamental.NUMBER:
            value = self.current_token.value
            self.eat(Fundamental.NUMBER)
            return Number(value)
        elif self.current_token.type == Symbol.LPAREN:
            self.eat(Symbol.LPAREN)
            node = self.expression()
            self.eat(Symbol.RPAREN)
            return node
        elif self.current_token.type == Fundamental.IDENTIFIER:
            if self.peek_token().type == Symbol.LBRACKET:
                return self.parse_array_access_or_assignment()
            value = self.current_token.value
            self.eat(Fundamental.IDENTIFIER)
            return Variable(value)
        elif self.current_token.type == Fundamental.STRING:
            value = self.current_token.value
            self.eat(Fundamental.STRING)
            return String(value)
        elif self.current_token.type == Symbol.LBRACKET:
            return self.parse_array_literal()
        else:
            raise ParsingError(f"Unexpected token type in factor: {self.current_token.type}", self.current_token)
        