from ai.groq_client import ask_groq
from ai.prompts import SYMPY_CONVERSION_SYSTEM_PROMPT


def interpret_question(question: str) -> str:
    cleaned_question = question.strip()
    if not cleaned_question:
        raise RuntimeError("Enter a math question first.")

    expression = ask_groq(SYMPY_CONVERSION_SYSTEM_PROMPT, cleaned_question)
    expression = _clean_expression(expression)

    if not expression or expression.upper() == "INVALID":
        raise RuntimeError("Groq could not convert this question into SymPy syntax.")

    if "\n" in expression:
        raise RuntimeError("Groq returned more than one expression. Please rephrase.")

    return expression


def _clean_expression(expression: str) -> str:
    cleaned = expression.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.lower().startswith("python"):
            cleaned = cleaned[6:].strip()

    return cleaned
