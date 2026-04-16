import ollama
import os

EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")


def generate_embedding(text: str):
    response = ollama.embeddings(
        model=EMBED_MODEL,
        prompt=text
    )
    return response["embedding"]