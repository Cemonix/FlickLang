from flicklang.ast import (
    ComparisonOp,
    If,
    Node,
    Number,
    BinaryOp,
    Program,
    String,
    UnaryOp,
    Variable,
    Assignment,
    Print,
)
from flicklang.models import TokenType
from typing import Dict, Any, cast


class Interpreter:
    def __init__(self) -> None:
        self.environment: Dict[str, Any] = {}

    def interpret(self, node: Node) -> Any:
        if isinstance(node, Program):
            for statement in node.statements:
                self.interpret(statement)
        else:
            # Dispatch to the specific visitor method based on the node type
            method_name = "visit_" + type(node).__name__
            visitor = getattr(self, method_name, self.no_visit_method)
            return visitor(node)

    def no_visit_method(self, node: Node) -> None:
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_Number(self, node: Number) -> int | float:
        try:
            return float(node.value) if "." in node.value else int(node.value)
        except:
            raise ValueError(f"Failed to convert '{node.value}' to a numeric type.")

    def visit_BinaryOp(self, node: BinaryOp) -> float:
        if node.op_token.type == TokenType.PLUS:
            return self.interpret(node.left) + self.interpret(node.right)
        elif node.op_token.type == TokenType.MINUS:
            return self.interpret(node.left) - self.interpret(node.right)
        elif node.op_token.type == TokenType.MULTIPLY:
            return self.interpret(node.left) * self.interpret(node.right)
        elif node.op_token.type == TokenType.DIVIDE:
            return self.interpret(node.left) / self.interpret(node.right)
        else:
            raise Exception(f"Unexpected binary operator: {node.op_token.type}")

    def visit_UnaryOp(self, node: UnaryOp) -> float:
        op_type = node.op_token.type
        if op_type == TokenType.MINUS:
            return -self.interpret(node.operand)
        else:
            raise Exception(f"Unsupported unary operator: {op_type}")

    def visit_Variable(self, node: Variable) -> float:
        var_name = node.token.value
        if var_name in self.environment:
            return self.environment[var_name]
        else:
            raise Exception(f"Variable '{var_name}' not defined")

    def visit_String(self, node: String) -> str:
        return node.value

    def visit_Assignment(self, node: Assignment) -> None:
        var_name = cast(Variable, node.variable_name)
        value = self.interpret(node.variable_value)
        self.environment[var_name.token.value] = value

    def visit_Print(self, node: Print) -> None:
        value = self.interpret(node.expr)
        print(value)

    def visit_If(self, node: If) -> Any:
        condition_result = self.interpret(node.condition)

        if condition_result:
            for statement in node.true_branch:
                self.interpret(statement)
        elif node.false_branch:
            if isinstance(node.false_branch, If):
                self.interpret(node.false_branch)
            else:
                for statement in node.false_branch:
                    self.interpret(statement)

    def visit_ComparisonOp(self, node: ComparisonOp) -> bool:
        left_value = self.interpret(node.left)
        right_value = self.interpret(node.right)

        if node.operator.type == TokenType.EQ:
            return left_value == right_value
        elif node.operator.type == TokenType.NEQ:
            return left_value != right_value
        elif node.operator.type == TokenType.GR:
            return left_value > right_value
        elif node.operator.type == TokenType.GRE:
            return left_value >= right_value
        elif node.operator.type == TokenType.LS:
            return left_value < right_value
        elif node.operator.type == TokenType.LSE:
            return left_value <= right_value
        else:
            raise Exception(f"Unsupported comparison operator: {node.operator.type}")
