import os

from dotenv import load_dotenv
from groq import Groq


DEFAULT_MODEL = "llama-3.1-8b-instant"


def build_client() -> Groq:
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Groq API key is missing. Set GROQ_API_KEY in your .env file.")

    return Groq(api_key=api_key)


def ask_groq(system_prompt: str, user_prompt: str) -> str:
    client = build_client()
    model = os.getenv("GROQ_MODEL", DEFAULT_MODEL)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
            max_tokens=120,
        )
    except Exception as exc:
        raise RuntimeError(f"Groq request failed: {exc}") from exc

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Groq returned an empty response.")

    return content.strip()
