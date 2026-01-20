
import os
import sys
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat.prompt import hyde_prompt, final_answer_prompt
from vector_db.qdrant_db import search_vectors


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def build_context(results: List[Dict]) -> str:
    context_text = ""

    for i, r in enumerate(results, start=1):
        context_text += f"""
[Context {i}]
Title: {r.get("title", "")}
Content: {r.get("content", "")}
Relevance Score: {r.get("score", 0)}
"""

    return context_text.strip()


def generate_hyde_answer(query: str) -> str:
   
    prompt = hyde_prompt(query)

    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": "You are a MOSDAC domain expert creating hypothetical answers for retrieval."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("HyDE generation failed:", e)
        return query  

def generate_final_answer(query: str, context: str) -> str:
    """
    Generate final user-facing answer using retrieved context.

    Args:
        query (str): User question
        context (str): Retrieved context

    Returns:
        str: Final answer
    """

    prompt = final_answer_prompt(context, query)

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a MOSDAC expert answering strictly from provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()

def ask_mosdac(query: str, top_k: int = 5) -> str:
    hyde_text = generate_hyde_answer(query)

    results = search_vectors(hyde_text, top_k=top_k)

    if not results:
        return "No relevant MOSDAC information found."

    context = build_context(results)
    return generate_final_answer(query, context)

if __name__=="__main__":
    ask_mosdac("WHAT IS MOSDAC")