import os
from dotenv import load_dotenv
import sys
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vector_db.qdrant_db import search_vectors

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def generate_hypothetical_ans(query: str) -> str:
    """
    Generates a technical MOSDAC-style answer.
    Used ONLY to improve vector search (not shown to user).
    """

    hypo_prompt = f"""
    You are a technical expert from MOSDAC (Meteorological and Oceanographic Satellite Data Archival Centre). 
    Based on your expertise, write a comprehensive, well-structured answer to the following question.
    
    Important: 
    - Write as if you are extracting information from official MOSDAC documentation and datasets
    - Use technical terminology appropriate for satellite data, remote sensing, and oceanography
    - Include specific details about datasets, instruments, parameters, and temporal/spatial coverage
    - Structure the answer with clear sections and bullet points where appropriate
    - Mention specific satellite missions (OCM, SCATSAT, INSAT, etc.) and data products
    
    Question: {query}
    
    Generate a detailed hypothetical answer:
    """

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
                    "content": hypo_prompt
                }
            ],
            temperature=0.3,
            # max_tokens=700
        )

        return response.choices[0].message.content.strip()

    except Exception as error:
        print("HyDE error:", error)
        return query

def build_context(results: list) -> str:
   

    context_text = ""

    for i, r in enumerate(results, start=1):
        context_text += f"""
[Context {i}]
Title: {r.get("title", "")}
Content: {r.get("content", "")}
Relevance Score: {r.get("score", 0)}
"""

    return context_text.strip()


def generate_final_answer(query: str, context: str) -> str:
  
    final_prompt = f"""
You are an AI assistant for MOSDAC.

Answer the user question ONLY using the context below.
If the answer is not found, say clearly:
"I could not find this information in the MOSDAC data."

Context:
{context}

User Question:
{query}

Answer clearly and technically:
"""

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a MOSDAC expert answering strictly from provided context."
            },
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        temperature=0.1,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()

def ask_mosdac(query: str) -> str:
    print("Generating HyDE answer...")
    hyde_text = generate_hypothetical_ans(query)
    print("Searching vector database...")
    results = search_vectors(hyde_text, top_k=5)
    if not results:
        return "No relevant MOSDAC information found."
    context = build_context(results)
    print("Generating final answer...")
    return generate_final_answer(query, context)


if __name__ == "__main__":
    while True:
        user_query = input("\nAsk a question (type 'exit' to quit): ")
        if user_query.lower() == "exit":
            break

        answer = ask_mosdac(user_query)
        print("\nAnswer:\n", answer)
