import sympy as sp


SAFE_GLOBALS = {
    "__builtins__": {}
}

SAFE_LOCALS = {
    "sqrt": sp.sqrt,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "log": sp.log,
    "ln": sp.log,
    "exp": sp.exp,
    "pi": sp.pi,
    "E": sp.E,
    "factor": sp.factor,
    "expand": sp.expand,
    "simplify": sp.simplify,
    "diff": sp.diff,
    "integrate": sp.integrate,
    "solve": sp.solve,
    "Eq": sp.Eq,
}

# Common variables

x, y, z, t, a, b, c = sp.symbols("x y z t a b c")

SAFE_LOCALS.update({
    "x": x,
    "y": y,
    "z": z,
    "t": t,
    "a": a,
    "b": b,
    "c": c,
})


def solve_expression(expression: str):

    try:

        obj = eval(
            expression,
            SAFE_GLOBALS,
            SAFE_LOCALS
        )

    except Exception as e:

        raise Exception(
            f"Invalid SymPy Expression:\n{expression}"
        ) from e

    try:

        if isinstance(obj, sp.Equality):

            variable = list(obj.free_symbols)

            if variable:

                answer = sp.solve(obj, variable[0])

            else:

                answer = obj

        else:

            if hasattr(obj, "doit"):

                answer = obj.doit()

            else:

                answer = obj

        answer = sp.simplify(answer)

        return answer

    except Exception as e:

        raise Exception(
            "Unable to solve expression."
        ) from e