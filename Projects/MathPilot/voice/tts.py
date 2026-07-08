def speak(text: str) -> None:
    cleaned_text = _naturalize_answer(text)
    if not cleaned_text:
        return

    try:
        import pyttsx3
    except ImportError as exc:
        raise RuntimeError("pyttsx3 is required for text-to-speech.") from exc

    try:
        engine = pyttsx3.init()
        engine.say(cleaned_text)
        engine.runAndWait()
    except Exception as exc:
        raise RuntimeError(f"Text-to-speech failed: {exc}") from exc


def _naturalize_answer(text: str) -> str:
    answer = _extract_final_answer(text)
    if not answer:
        return ""

    normalized = answer.replace("\n", " ").strip()
    normalized = normalized.replace("*", " times ")
    normalized = normalized.replace("^", " to the power of ")
    normalized = normalized.replace("+", " plus ")
    normalized = normalized.replace("=", " equals ")
    normalized = normalized.replace("[", "").replace("]", "")

    if "," in normalized:
        parts = [part.strip() for part in normalized.split(",") if part.strip()]
        if len(parts) > 1:
            return f"The solutions are {_join_words(parts)}."

    return f"The answer is {normalized}."


def _extract_final_answer(text: str) -> str:
    marker = "Answer:"
    if marker not in text:
        return text.strip()

    return text.split(marker, maxsplit=1)[1].strip()


def _join_words(parts: list[str]) -> str:
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"

    return f"{', '.join(parts[:-1])}, and {parts[-1]}"
