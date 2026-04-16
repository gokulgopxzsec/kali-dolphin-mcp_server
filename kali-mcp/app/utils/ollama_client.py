import os
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "dolphin-llama3:8b")


def ask_ollama(prompt: str):
    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model": DEFAULT_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    return response.json()["response"]