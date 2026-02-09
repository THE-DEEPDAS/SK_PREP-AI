
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class EmbeddingGenerator:
    """Generate embeddings for text"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for list of texts"""
        embeddings = self.model.encode(texts)
        return embeddings
    
    def generate_single(self, text: str) -> np.ndarray:
        """Generate embedding for single text"""
        embedding = self.model.encode([text])[0]
        return embedding

# Global instance
embedding_generator = EmbeddingGenerator()

def generate_embeddings(texts: List[str]) -> np.ndarray:
    """Helper function to generate embeddings"""
    return embedding_generator.generate_embeddings(texts)