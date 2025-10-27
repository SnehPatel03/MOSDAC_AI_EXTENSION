import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def embed_texts(texts):
    """
      
    Convert list of texts into embeddings using Gemini API
    through OpenAI-compatible SDK structure.
    
    """
     
    response = client.embeddings.create(
        model="text-embedding-004",  
        input=texts
    )
    
    return [item.embedding for item in response.data]
