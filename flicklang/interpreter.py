from flicklang.ast import (
    ArrayIndex,
    ArrayIndexAssignment,
    ArrayLiteral,
    ComparisonOp,
    CompoundAssignment,
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
from flicklang.exceptions import ExecutionError
from flicklang.models import CompoundOperator, Operator, Comparison
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

    def visit_Number(self, node: Number) -> int | float:
        try:
            return float(node.value) if "." in node.value else int(node.value)
        except:
            raise ValueError(f"Failed to convert '{node.value}' to a numeric type.")

    def visit_String(self, node: String) -> str:
        return node.value
    
    def visit_Variable(self, node: Variable) -> float:
        var_name = node.name
        if var_name in self.environment:
            return self.environment[var_name]
        else:
            raise ExecutionError(f"Undefined variable: {var_name}")
        
    def visit_BinaryOp(self, node: BinaryOp) -> float:
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op_token.type == Operator.PLUS:
            return left + right
        elif node.op_token.type == Operator.MINUS:
            return left - right
        elif node.op_token.type == Operator.MULTIPLY:
            return left * right
        elif node.op_token.type == Operator.DIVIDE:
            if right == 0:
                raise ExecutionError("Division by zero.")
            return left / right
        elif node.op_token.type == Operator.MODULO:
            if right == 0:
                raise ExecutionError("Modulo by zero.")
            return left % right
        else:
            raise ExecutionError(f"Unsupported operator: {node.op_token.type}")

    def visit_UnaryOp(self, node: UnaryOp) -> float:
        op_type = node.op_token.type
        if op_type == Operator.MINUS:
            return -self.visit(node.operand)
        else:
            raise ExecutionError(f"Unsupported unary operator: {op_type}")

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
            raise ExecutionError(f"Unsupported comparison operator: {node.operator.type}")
    
    def visit_ArrayLiteral(self, node: ArrayLiteral) -> list:
        return [self.visit(element) for element in node.elements]

    def visit_ArrayIndex(self, node: ArrayIndex) -> Any:
        array = self.visit(node.array)
        index = self.visit(node.index)

        if not isinstance(array, list):
            raise ExecutionError("Attempting to index a non-list type.")

        try:
            if not isinstance(index, int):
                raise ExecutionError("Array index must be an integer.")
            return array[index]
        except IndexError:
            raise ExecutionError(f"Array index out of bounds: {index}")

    def visit_ArrayIndexAssignment(self, node: ArrayIndexAssignment) -> None:
        array_val = self.visit(node.array)
        index_val = self.visit(node.index)

        if not isinstance(index_val, int):
            raise TypeError(f"Index has to be int. Index type was {type(index_val)}.")

        value_val = self.visit(node.value)
        array_val[index_val] = value_val

    def visit_Assignment(self, node: Assignment) -> None:
        variable = cast(Variable, node.variable_name)
        value = self.visit(node.variable_value)
        self.environment[variable.name] = value

    def visit_CompoundAssignment(self, node: CompoundAssignment) -> None:
        variable_name = cast(Variable, node.variable_name)
        if variable_name.name not in self.environment:
            raise ExecutionError(f"Undefined variable: '{variable_name}'")

        current_value = self.environment[variable_name.name]
        new_value = self.visit(node.variable_value)

        if node.op_token.type == CompoundOperator.PLUS_ASSIGN:
            updated_value = current_value + new_value
        elif node.op_token.type == CompoundOperator.MINUS_ASSIGN:
            updated_value = current_value - new_value
        elif node.op_token.type == CompoundOperator.MULTIPLY_ASSIGN:
            updated_value = current_value * new_value
        elif node.op_token.type == CompoundOperator.DIVIDE_ASSIGN:
            if new_value == 0:
                raise ExecutionError("Division by zero in compound assignment.")
            updated_value = current_value / new_value
        elif node.op_token.type == CompoundOperator.MODULO_ASSIGN:
            if new_value == 0:
                raise ExecutionError("Modulo by zero in compound assignment.")
            updated_value = current_value % new_value
        else:
            raise ExecutionError(f"Unsupported compound operator: {node.op_token.type}")

        self.environment[variable_name.name] = updated_value

    def visit_Print(self, node: Print) -> None:
        output = ' '.join(str(self.visit(expr)) for expr in node.expressions)
        print(output)

    def visit_If(self, node: If) -> Any:
        condition_result = self.visit(node.condition)
        if not isinstance(condition_result, bool):
            raise ExecutionError("Condition expression must evaluate to a boolean.")

        if condition_result:
            for statement in node.true_branch:
                self.visit(statement)
        elif node.false_branch is not None:
            if isinstance(node.false_branch, If):
                self.visit(node.false_branch)
            else:
                for statement in node.false_branch:
                    self.visit(statement)

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

    def visit(self, node: Node) -> Any:
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node)

    def no_visit_method(self, node: Node) -> None:
        raise ExecutionError(f"No visit_{type(node).__name__} method defined")
    