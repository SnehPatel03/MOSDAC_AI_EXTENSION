
from typing import Final


def hyde_prompt(query: str) -> str:
    """
    Generate a HyDE (Hypothetical Document Embedding) prompt.

    Used only to improve vector similarity search.
    The output of this prompt is NEVER shown to the user.

    Args:
        query (str): User question

    Returns:
        str: HyDE prompt text
    """

    return f"""
You are a technical expert from MOSDAC (Meteorological and Oceanographic Satellite Data Archival Centre).

Based on your expertise, write a comprehensive and well-structured answer to the following question.

Rules:
- Write as if extracting information from official MOSDAC documentation and datasets
- Use technical terminology related to satellite data, meteorology, oceanography, and remote sensing
- Include dataset names, instruments, parameters, and spatial/temporal coverage
- Mention satellite missions such as INSAT, OCM, SCATSAT, etc.
- Structure the answer using clear sections or bullet points

Question:
{query}

Generate a detailed hypothetical answer:
""".strip()



def final_answer_prompt(context: str, query: str) -> str:
    """
    Generate the final user-facing prompt.

    Enforces strict context-based answering to avoid hallucinations.

    Args:
        context (str): Retrieved context from vector database
        query (str): User question

    Returns:
        str: Final prompt text
    """

    return f"""
You are an AI assistant for MOSDAC.

Answer the user's question using ONLY the information provided in the context below.
If the answer is not present in the context, respond exactly with:
"I could not find this information in the MOSDAC data."

--- CONTEXT START ---
{context}
--- CONTEXT END ---

User Question:
{query}

Provide a clear, concise, and technically accurate answer:
""".strip()
