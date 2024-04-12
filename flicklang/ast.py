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
    value: str


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
    name: str


@dataclass
class Print(Node):
    expressions: List[Node]


@dataclass
class String(Node):
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
class ArrayIndex(Node):
    array: Node
    index: Node


@dataclass
class ArrayIndexAssignment(Node):
    array: Variable
    index: Node
    value: Node


@dataclass
class WhileLoop(Node):
    condition: Node
    body: List[Node]
