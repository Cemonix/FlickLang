from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    STRING = auto()
    EOF = auto()
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    LPAREN = "("
    RPAREN = ")"
    PRINT = "p"
    BLOCK_START = '{'
    BLOCK_END = '}'
    IF = 'if'
    ELI = 'elif'
    EL = 'else'
    EQ = 'eq'
    NEQ = 'neq'
    GR = 'gr'
    LS = 'ls'
    GRE = 'gre'
    LSE = 'lse'

class Token:
    def __init__(self, type: TokenType, value: str) -> None:
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class EOFToken(Token):
    def __init__(self, type: TokenType, value: str | None) -> None:
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return (
            f"EOFToken({self.type}, {self.value})"
            if self.value is not None
            else f"EOFToken({self.type})"
        )
