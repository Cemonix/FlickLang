from dataclasses import dataclass
from typing import Union
from enum import Enum


class Keyword(Enum):
    IF = "if"   # if
    ELI = "eli" # elif
    EL = "el"   # else
    W = "w"     # while loop
    P = "p"     # print
    FU = "fu"
    RET = "ret"


class Operator(Enum):
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"

class CompoundOperator(Enum):
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    MULTIPLY_ASSIGN = "*="
    DIVIDE_ASSIGN = "/="
    MODULO_ASSIGN = "%="


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


SyntaxTokenType = Union[Keyword, Fundamental, Operator, Symbol, Comparison, CompoundOperator]
operators = {item: item.value for item in Operator}
symbols = {item: item.value for item in Symbol}
keywords = {item: item.value for item in Keyword}
comparisons = {item: item.value for item in Comparison}
compound_operators = {item: item.value for item in CompoundOperator}

@dataclass
class Token:
    type: SyntaxTokenType
    value: str


@dataclass
class EOFToken:
    type: Fundamental
