from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import hashlib


class VectorService:
    def __init__(self):
        self.client = None
        self.model = None
        self.collection_name = "upsc_pyqs"

    async def initialize(self):
        """Initialize Qdrant client and embedding model"""
        self.client = QdrantClient(host="localhost", port=6333)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config={
                "size": 384,
                "distance": "Cosine"
            }
        )

        print("✓ VectorService initialized")

    def embed_text(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    async def add_documents(self, texts: List[str], metadatas: List[Dict]) -> int:
        """
        Safely add documents to Qdrant
        """
        # 🔒 SAFETY CHECK
        if not texts or not metadatas:
            print("⚠ Skipping Qdrant insert (empty batch)")
            return 0

        points = []

        for text, meta in zip(texts, metadatas):
            text = text.strip()
            if not text:
                continue

            # Stable unique ID (prevents overwrite)
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
            print("⚠ No valid vectors created, skipping upsert")
            return 0

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        return len(points)

    def search(self, query: str, limit: int = 3) -> List[Dict]:
        """Search similar documents"""
        query_vector = self.embed_text(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )

        return [r.payload for r in results]
