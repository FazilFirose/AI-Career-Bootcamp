import speech_recognition as sr


def listen() -> str:
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=12)
    except OSError as exc:
        raise RuntimeError("Microphone is not available. Check your input device.") from exc
    except sr.WaitTimeoutError as exc:
        raise RuntimeError("No speech detected. Please try again.") from exc

    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError as exc:
        raise RuntimeError("Could not understand the audio. Please speak clearly.") from exc
    except sr.RequestError as exc:
        raise RuntimeError(
            "Speech recognition service is unavailable. Check your internet connection."
        ) from exc

    cleaned_text = text.strip()
    if not cleaned_text:
        raise RuntimeError("No speech was recognized. Please try again.")

    return cleaned_text
