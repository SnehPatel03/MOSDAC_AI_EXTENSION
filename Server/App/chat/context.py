from typing import List

# Hard limit to protect LLM token usage
MAX_CONTEXT_CHARS = 3000


def build_context(documents: List[dict]) -> str:
    """
    Build a clean, concise context string from retrieved documents.

    Parameters:
    - documents: list of retrieved document dicts
      Each document is expected to have a 'text' field

    Returns:
    - context string to be passed to the LLM
    """

    context_chunks = []
    total_length = 0

    for doc in documents:
        text = doc.get("text", "").strip()

        if not text:
            continue

        if total_length + len(text) > MAX_CONTEXT_CHARS:
            remaining = MAX_CONTEXT_CHARS - total_length
            context_chunks.append(text[:remaining])
            break

        context_chunks.append(text)
        total_length += len(text)


    context = "\n\n".join(context_chunks)

    return context
