from ai.groq_client import ask_groq
from ai.prompts import SYMPY_SYSTEM_PROMPT


def interpret(question):

    if question.strip() == "":
        raise Exception("Empty Question")

    expression = ask_groq(
        SYMPY_SYSTEM_PROMPT,
        question
    )

    expression = expression.strip()

    if expression.upper() == "INVALID":
        raise Exception("Unable to understand the question.")

    return expression