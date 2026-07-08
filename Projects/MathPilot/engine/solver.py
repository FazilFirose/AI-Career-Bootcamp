from collections.abc import Callable

from ai.interpreter import interpret_question
from engine.math_engine import solve_sympy_expression


StatusCallback = Callable[[str], None]


def process_question(
    question: str,
    status_callback: StatusCallback | None = None,
) -> str:
    cleaned_question = question.strip()
    if not cleaned_question:
        raise RuntimeError("Enter or speak a math question first.")

    _update_status(status_callback, "Understanding...")
    sympy_expression = interpret_question(cleaned_question)

    _update_status(status_callback, "Solving...")
    return solve_sympy_expression(sympy_expression)


def _update_status(status_callback: StatusCallback | None, status: str) -> None:
    if status_callback is not None:
        status_callback(status)
