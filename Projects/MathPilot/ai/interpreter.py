from ai.groq_client import ask_groq
from ai.prompts import SYMPY_SYSTEM_PROMPT
from ai.preprocessor import preprocess


def interpret(question):

    cleaned_question = preprocess(question)

    if cleaned_question.strip() == "":
        raise Exception("Empty Question")

    expression = ask_groq(
        SYMPY_SYSTEM_PROMPT,
        cleaned_question
    )

    expression = expression.strip()

    if expression.upper() == "INVALID":
        raise Exception("Unable to understand the question.")

    return expression