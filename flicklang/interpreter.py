from flicklang.ast import (
    ArrayLiteral,
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
    WhileLoop,
)
from flicklang.models import Operator, Comparison
from typing import Dict, Any, cast


class Interpreter:
    def __init__(self) -> None:
        self.environment: Dict[str, Any] = {}

    def interpret(self, node: Node) -> Any:
        if isinstance(node, Program):
            for statement in node.statements:
                self.interpret(statement)
        else:
            self.visit(node)

    def visit(self, node: Node) -> Any:
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
        if node.op_token.type == Operator.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op_token.type == Operator.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op_token.type == Operator.MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op_token.type == Operator.DIVIDE:
            return self.visit(node.left) / self.visit(node.right)
        else:
            raise Exception(f"Unexpected binary operator: {node.op_token.type}")

    def visit_UnaryOp(self, node: UnaryOp) -> float:
        op_type = node.op_token.type
        if op_type == Operator.MINUS:
            return -self.visit(node.operand)
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
        value = self.visit(node.variable_value)
        self.environment[var_name.token.value] = value

    def visit_Print(self, node: Print) -> None:
        value = self.visit(node.expr)
        print(value)

    def visit_If(self, node: If) -> Any:
        condition_result = self.visit(node.condition)

        if condition_result:
            for statement in node.true_branch:
                self.visit(statement)
        elif node.false_branch:
            if isinstance(node.false_branch, If):
                self.visit(node.false_branch)
            else:
                for statement in node.false_branch:
                    self.visit(statement)

    def visit_ComparisonOp(self, node: ComparisonOp) -> bool:
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

        if node.operator.type == Comparison.EQ:
            return left_value == right_value
        elif node.operator.type == Comparison.NEQ:
            return left_value != right_value
        elif node.operator.type == Comparison.GR:
            return left_value > right_value
        elif node.operator.type == Comparison.GRE:
            return left_value >= right_value
        elif node.operator.type == Comparison.LS:
            return left_value < right_value
        elif node.operator.type == Comparison.LSE:
            return left_value <= right_value
        else:
            raise Exception(f"Unsupported comparison operator: {node.operator.type}")
        
    def visit_ArrayLiteral(self, node: ArrayLiteral) -> list:
        return [self.visit(element) for element in node.elements]
    
    def visit_WhileLoop(self, node: WhileLoop) -> None:
        while True:
            condition_result = self.visit(node.condition)
            if isinstance(node.condition, ComparisonOp):
                condition_eval = self.visit_ComparisonOp(node.condition)
            else:
                condition_eval = condition_result
                
            if not condition_eval:
                break

            for statement in node.body:
                self.visit(statement)
