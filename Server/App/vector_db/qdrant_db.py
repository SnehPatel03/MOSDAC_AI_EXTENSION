import os
import sys
import uuid
from typing import List
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from services.embeddings import embed_texts

load_dotenv()


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=60.0
)

COLLECTION_NAME = "mosdac_chunks"


def init_collection(vector_size: int):
    """Create collection if it doesn't exist"""
    if not qdrant.collection_exists(collection_name=COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
        print("Collection created")
    else:
        print("Collection already exists")


def upsert_chunks(chunks, embeddings, batch_size=100):

    total = len(chunks)
    print("Inserting", total, "chunks...")

    for i in range(0, total, batch_size):
        batch_chunks = chunks[i:i + batch_size]
        batch_embeddings = embeddings[i:i + batch_size]

        points = []

        for j in range(len(batch_chunks)):
            chunk = batch_chunks[j]
            embedding = batch_embeddings[j]

            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,      
                payload={
                    "url": chunk.get("url", ""),
                    "title": chunk.get("title", ""),
                    "content": chunk.get("content", ""),
                    "chunk_id": chunk.get("chunk_id", i + j)
                }
            )
            points.append(point)

        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
            wait=True
        )

        print("Inserted batch", (i // batch_size) + 1) # calculation 😎

        
        
def search_vectors(query: str, top_k: int = 5):
    query_vector = embed_texts([query])[0]

    results_raw = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        prefetch=[],
        query=query_vector,
        limit=top_k,
        with_payload=True,
        with_vectors=False
    )

    results = []
    for point in results_raw.points:
        results.append({
            "score": round(point.score, 4),
            "url": point.payload.get("url", ""),
            "title": point.payload.get("title", ""),
            "content": point.payload.get("content", "")[:300]
        })

    return results
