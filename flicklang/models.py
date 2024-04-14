from dataclasses import dataclass
from typing import Union
from enum import Enum


class Keyword(Enum):
    IF = "if"   # if
    ELI = "eli" # elif
    EL = "el"   # else
    W = "w"     # while loop
    P = "p"     # print


class Operator(Enum):
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"


class Symbol(Enum):
    LPAREN = "("
    RPAREN = ")"
    BLOCK_START = "{"
    BLOCK_END = "}"
    LBRACKET = "["
    RBRACKET = "]"
    COMMA = ","


class Comparison(Enum):
    EQ = "eq"
    NEQ = "neq"
    GR = "gr"
    LS = "ls"
    GRE = "gre"
    LSE = "lse"


class Fundamental(Enum):
    NUMBER = "number"
    IDENTIFIER = "identifier"
    STRING = "string"
    EOF = "eof"


SyntaxTokenType = Union[Keyword, Fundamental, Operator, Symbol, Comparison]


@dataclass
class Token:
    type: SyntaxTokenType
    value: str


@dataclass
class EOFToken:
    type: Fundamental
