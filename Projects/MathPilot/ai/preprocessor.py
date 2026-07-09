import re


def preprocess(text: str) -> str:

    text = text.lower().strip()

    # -------------------------
    # Basic operator replacements
    # -------------------------

    replacements = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "multiplied by": "*",
        "multiply by": "*",
        "into": "*",
        "divide by": "/",
        "divided by": "/",
        "over": "/",
        "modulus": "%",
        "mod": "%",
        "to the power of": "^",
        "raised to": "^",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # -------------------------
    # Whole Square
    # -------------------------

    text = re.sub(
        r"(.+?)\s+(the whole square|whole square|entire square|complete square|full square|bracket square)$",
        r"(\1)^2",
        text,
    )

    # -------------------------
    # Whole Cube
    # -------------------------

    text = re.sub(
        r"(.+?)\s+(the whole cube|whole cube|entire cube|complete cube|full cube|bracket cube)$",
        r"(\1)^3",
        text,
    )

    # -------------------------
    # Square Root
    # -------------------------

    text = re.sub(
        r"square root of",
        "sqrt",
        text,
    )

    # -------------------------
    # Cube Root
    # -------------------------

    text = re.sub(
        r"cube root of",
        "cbrt",
        text,
    )

    # -------------------------
    # Absolute Value
    # -------------------------

    text = re.sub(
        r"absolute value of",
        "abs",
        text,
    )

    # -------------------------
    # Brackets
    # -------------------------

    text = text.replace("open bracket", "(")
    text = text.replace("close bracket", ")")

    text = text.replace("left bracket", "(")
    text = text.replace("right bracket", ")")

    # -------------------------
    # Remove duplicate spaces
    # -------------------------

    text = " ".join(text.split())

    return text