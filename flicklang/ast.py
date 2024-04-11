from typing import List

from flicklang.models import Token


class Node:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__} Node"


class Program(Node):
    def __init__(self, statements: List[Node]) -> None:
        self.statements = statements

    def __repr__(self) -> str:
        return f"Program({self.statements})"
    
    
class Number(Node):
    def __init__(self, token: Token) -> None:
        if not token.value:
            raise ValueError("Number token has no value.")
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f"Number({self.value})"


class BinaryOp(Node):
    def __init__(self, left: Node, op_token: Token, right: Node) -> None:
        self.left = left
        self.op_token = op_token
        self.right = right

    def __repr__(self) -> str:
        return f"BinaryOp({self.left.__repr__()}, {self.op_token.value}, {self.right.__repr__()})"


class UnaryOp(Node):
    def __init__(self, op_token: Token, operand: Node) -> None:
        self.op_token = op_token
        self.operand = operand

    def __repr__(self) -> str:
        return f"UnaryOp({self.op_token.value}, {self.operand.__repr__()})"


class Assignment(Node):
    def __init__(self, variable_name: Node, variable_value: Node) -> None:
        self.variable_name = variable_name
        self.variable_value = variable_value

    def __repr__(self) -> str:
        return f"Assignment({self.variable_name.__repr__()}, {self.variable_value.__repr__()})"


class Variable(Node):
    def __init__(self, token: Token) -> None:
        if not token.value:
            raise ValueError("Number token has no value.")
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f"Var({self.value})"


class Print(Node):
    def __init__(self, expr: Node) -> None:
        self.expr: Node = expr

    def __repr__(self) -> str:
        return f"Print({self.expr.__repr__()})"


class String(Node):
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f'String("{self.value}")'