from qdrant_client import QdrantClient
from typing import List, Dict
from openai import OpenAI
import hashlib
import os
import time

from app.config import settings


class VectorService:
    def __init__(self):
        self.client = None
        self.collection_name = "upsc_pyqs"

        # OpenRouter embeddings
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is not set")

        self.embed_client = OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
        )
        self.embed_model = settings.OPENROUTER_EMBED_MODEL

    async def initialize(self):

        # IMPORTANT FIX
        host = os.getenv("QDRANT_HOST", "localhost")
        port = int(os.getenv("QDRANT_PORT", 6333))

        print("CONNECTING TO QDRANT:", host, port)

        # Wait for Qdrant
        for i in range(10):
            try:
                self.client = QdrantClient(
                    url=f"http://{host}:{port}"
                )

                self.client.recreate_collection(
                    collection_name=self.collection_name,
                    vectors_config={
                        "size": 768,
                        "distance": "Cosine"
                    }
                )

                print("✓ VectorService initialized")
                return

            except Exception as e:
                print(f"Waiting for Qdrant... attempt {i+1}")
                print("ERROR:", e)
                time.sleep(2)

        raise RuntimeError("Qdrant not reachable")

    def embed_text(self, text: str):
        response = self.embed_client.embeddings.create(
            model=self.embed_model,
            input=text,
        )

        return response.data[0].embedding

    async def add_documents(self, texts: List[str], metadatas: List[Dict]) -> int:

        if not texts or not metadatas:
            print("⚠ Skipping empty batch")
            return 0

        points = []

        for text, meta in zip(texts, metadatas):

            text = text.strip()
            if not text:
                continue

            uid = hashlib.md5(text.encode("utf-8")).hexdigest()

            vector = self.embed_text(text)

            points.append({
                "id": uid,
                "vector": vector,
                "payload": {
                    "text": text,
                    **meta
                }
            })

        if not points:
            print("⚠ No valid vectors")
            return 0

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        return len(points)

    def search(self, query: str, limit: int = 3) -> List[Dict]:

        query_vector = self.embed_text(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )

        return [r.payload for r in results]