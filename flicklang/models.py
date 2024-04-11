from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    STRING = auto()
    EOF = auto()
    ASSIGN = '='
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    PRINT = 'p'


class Token:
    def __init__(self, type: TokenType, value: str | None) -> None:
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"
