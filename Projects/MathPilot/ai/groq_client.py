import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.1-8b-instant"


def ask_groq(system_prompt, user_prompt):

    response = client.chat.completions.create(

        model=MODEL,

        temperature=0,

        messages=[

            {
                "role":"system",
                "content":system_prompt
            },

            {
                "role":"user",
                "content":user_prompt
            }

        ]

    )

    return response.choices[0].message.content.strip()