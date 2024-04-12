from dataclasses import dataclass
from typing import List, Optional, Union

from flicklang.models import Token


@dataclass
class Node:
    pass


@dataclass
class Program(Node):
    statements: List[Node]


@dataclass
class Number(Node):
    token: Token
    value: str

    def __post_init__(self):
        if not self.token.value:
            raise ValueError("Number token has no value.")


@dataclass
class BinaryOp(Node):
    left: Node
    op_token: Token
    right: Node


@dataclass
class UnaryOp(Node):
    op_token: Token
    operand: Node


@dataclass
class Assignment(Node):
    variable_name: Node
    variable_value: Node


@dataclass
class Variable(Node):
    token: Token
    value: str

    def __post_init__(self):
        if not self.token.value:
            raise ValueError("Variable token has no value.")


@dataclass
class Print(Node):
    expr: Node


@dataclass
class String(Node):
    token: Token
    value: str


@dataclass
class If(Node):
    condition: Node
    true_branch: List[Node]
    false_branch: Optional[Union["If", List[Node]]] = None


@dataclass
class ComparisonOp(Node):
    left: Node
    operator: Token
    right: Node


@dataclass
class ArrayLiteral(Node):
    elements: List[Node]


@dataclass
class WhileLoop(Node):
    condition: Node
    body: List[Node]
