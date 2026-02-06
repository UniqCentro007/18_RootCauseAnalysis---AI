import os
import json
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")


def call_llm(prompt: str):
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an IT root cause analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    text = completion.choices[0].message.content

    try:
        return json.loads(text)
    except:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
