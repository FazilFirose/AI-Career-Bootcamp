import sympy as sp


SAFE_GLOBALS = {
    "__builtins__": {},
}

SAFE_LOCALS = {
    name: getattr(sp, name)
    for name in (
        "Abs",
        "Eq",
        "E",
        "I",
        "Matrix",
        "N",
        "oo",
        "pi",
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sqrt",
        "log",
        "ln",
        "exp",
        "factor",
        "expand",
        "simplify",
        "solve",
        "diff",
        "integrate",
        "limit",
        "Rational",
        "Symbol",
        "symbols",
    )
}

SAFE_LOCALS.update(
    {
        "x": sp.Symbol("x"),
        "y": sp.Symbol("y"),
        "z": sp.Symbol("z"),
        "t": sp.Symbol("t"),
        "a": sp.Symbol("a"),
        "b": sp.Symbol("b"),
        "c": sp.Symbol("c"),
    }
)


def solve_sympy_expression(expression: str) -> str:
    parsed_expression = _parse_expression(expression)
    result = _solve(parsed_expression)
    return _format_answer(expression, result)


def _parse_expression(expression: str):
    try:
        return eval(expression, SAFE_GLOBALS, SAFE_LOCALS)
    except Exception as exc:
        raise RuntimeError(f"Invalid SymPy expression: {expression}") from exc


def _solve(expression):
    try:
        if isinstance(expression, sp.Equality):
            symbols = sorted(expression.free_symbols, key=lambda symbol: symbol.name)
            return sp.solve(expression, symbols[0]) if symbols else bool(expression)

        if getattr(expression, "is_Relational", False):
            symbols = sorted(expression.free_symbols, key=lambda symbol: symbol.name)
            return sp.solve(expression, symbols[0]) if symbols else bool(expression)

        if isinstance(expression, (list, tuple, dict, set)):
            return expression

        if hasattr(expression, "doit"):
            expression = expression.doit()

        return sp.simplify(expression)
    except Exception as exc:
        raise RuntimeError("SymPy could not solve this expression.") from exc


def _format_answer(expression: str, result) -> str:
    return f"SymPy expression:\n{expression}\n\nAnswer:\n{sp.pretty(result)}"
