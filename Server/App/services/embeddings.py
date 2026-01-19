import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

MAX_BATCH_SIZE = 100


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convert list of texts into embeddings using Gemini API
    with safe batching (max 100 per request).
    """

    all_embeddings = []

    for i in range(0, len(texts), MAX_BATCH_SIZE):
        batch = texts[i:i + MAX_BATCH_SIZE]

        response = client.embeddings.create(
            model="text-embedding-004",
            input=batch
        )

        all_embeddings.extend(
            item.embedding for item in response.data
        )

    return all_embeddings
