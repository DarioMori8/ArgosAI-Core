import ast
import operator
from engine.tools.tool_registry import register_tool


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod
}


def safe_eval(node):

    if isinstance(node, ast.Constant):
        return node.value

    elif isinstance(node, ast.UnaryOp):

        if isinstance(node.op, ast.USub):
            return -safe_eval(node.operand)

        raise ValueError("Unary operator not allowed")

    elif isinstance(node, ast.BinOp):

        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)

        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)

        raise ValueError("Operator not allowed")

    else:
        raise ValueError("Invalid expression")


def run(expression: str):

    try:

        tree = ast.parse(expression, mode="eval")

        result = safe_eval(tree.body)

        return {
            "expression": expression,
            "result": result
        }

    except Exception as e:

        return {
            "error": str(e)
        }


register_tool("calculator", run)