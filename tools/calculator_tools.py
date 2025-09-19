# tools/calculator_tools.py
import ast

def safe_eval(expr: str):
    """
    Very small safe evaluator supporting arithmetic operations.
    Allowed: + - * / ** % // parentheses, floats and ints.
    """
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    node = ast.parse(expr, mode="eval")

    allowed = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv,
        ast.USub, ast.UAdd, ast.Load, ast.Tuple, ast.List
    )

    for n in ast.walk(node):
        if not isinstance(n, allowed):
            raise ValueError(f"Unsafe or unsupported expression element: {type(n).__name__}")

    compiled = compile(node, "<ast>", "eval")
    return eval(compiled, {"__builtins__": {}}, {})

def calculate(expression: str) -> str:
    try:
        result = safe_eval(expression)
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"
