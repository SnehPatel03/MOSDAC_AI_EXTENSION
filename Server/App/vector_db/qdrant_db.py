import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams,Distance,PointStruct
import uuid
from embeddings.embeddings import embed_texts
from typing import List
import sys

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


qdrant = QdrantClient(url = os.getenv("QDRANT_URL","http://localhost:6333"),api_key=os.getenv("QDRANT_API_KEY"), timeout=60.0)

COLLECTION_NAME ="mosdac_chunks"

def init_collection(vector_size:int):
    try:
        if not qdrant.collection_exists(collection_name=COLLECTION_NAME):
            qdrant.create_collection(collection_name=COLLECTION_NAME,vectors_config=VectorParams(size =vector_size,distance = Distance.COSINE ))
        else:
            print(f"Collection already exist...")
    except Exception as e:
        print(f"ERROR IN INITILIZATION OF THE COLLECTION ERROR: {e}")
def upsert_chunks(chunks, embeddings, batch_size=100):
    """
    Store text chunks with their embeddings into Qdrant in batches.
    
    Args:
        chunks (list): List of dicts with metadata (url, title, content, etc.)
        embeddings (list): List of embedding vectors (same order as chunks)
        batch_size (int): Number of chunks to insert in one go (default 100)
    """
    total = len(chunks)
    print(f"🔹 Total chunks to insert: {total}")

    for i in range(0, total, batch_size):
        # Select one batch of data
        batch_chunks = chunks[i : i + batch_size]
        batch_embeddings = embeddings[i : i + batch_size]

        # Create structured data points for Qdrant
        points = [
            PointStruct(
                id=str(uuid.uuid4()),  # unique id for each vector
                vector=embedding,      # embedding vector (list of floats)
                payload={              # metadata about this chunk
                    "url": chunk.get("url", ""),
                    "title": chunk.get("title", ""),
                    "content": chunk.get("content", ""),
                    "chunk_id": chunk.get("chunk_id", j + i),
                },
            )
            for j, (chunk, embedding) in enumerate(zip(batch_chunks, batch_embeddings))
        ]

        # Try to insert into Qdrant
        try:
            qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=points,
                wait=True  # ensures operation completes before moving on
            )
            print(f"✅ Inserted {len(points)} chunks (batch {i // batch_size + 1})")
        except Exception as e:
            print(f"❌ Failed to insert batch {i // batch_size + 1}: {e}")
            raise
def search_vectors(query: str, top_k: int = 5) -> List[dict]:
    """
    Search for most relevant chunks in Qdrant for a given query.

    Args:
        query (str): User's search query
        top_k (int): Number of most relevant results to return

    Returns:
        List[dict]: Top matching results with similarity scores and metadata
    """
    try:
        print(f"🔹 Searching for: '{query}'")

        # 1️⃣ Generate embedding for the query text
        query_vector = embed_texts([query])[0]

        # 2️⃣ Perform similarity search in Qdrant
        search_results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k,
        )

        # 3️⃣ Parse and format search results
        results = []
        for res in search_results:
            results.append({
                "score": round(res.score, 4),
                "url": res.payload.get("url", ""),
                "title": res.payload.get("title", ""),
                "content": res.payload.get("content", "")[:300] + "...",  # show preview
                "chunk_id": res.payload.get("chunk_id", ""),
            })

        if results:
            print(f"✅ Found {len(results)} results:")
            for r in results:
                print(f"   → {r['title']} (score: {r['score']})")
        else:
            print("⚠️ No matches found.")

        return results

    except Exception as e:
        print(f"❌ Qdrant search failed: {e}")
        return []    
    
def search_vectors(query: str, top_k: int = 5) -> List[dict]:
    """
    Search for most relevant chunks in Qdrant for a given query.

    Args:
        query (str): User's search query
        top_k (int): Number of most relevant results to return

    Returns:
        List[dict]: Top matching results with similarity scores and metadata
    """
    try:
        print(f"🔹 Searching for: '{query}'")

        # 1️⃣ Generate embedding for the query text
        query_vector = embed_texts([query])[0]

        # 2️⃣ Perform similarity search in Qdrant
        search_results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k,
        )

        # 3️⃣ Parse and format search results
        results = []
        for res in search_results:
            results.append({
                "score": round(res.score, 4),
                "url": res.payload.get("url", ""),
                "title": res.payload.get("title", ""),
                "content": res.payload.get("content", "")[:300] + "...",  # show preview
                "chunk_id": res.payload.get("chunk_id", ""),
            })

        if results:
            print(f"✅ Found {len(results)} results:")
            for r in results:
                print(f"   → {r['title']} (score: {r['score']})")
        else:
            print("⚠️ No matches found.")

        return results

    except Exception as e:
        print(f"❌ Qdrant search failed: {e}")
        return []