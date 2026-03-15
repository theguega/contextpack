from typing import List
import numpy as np

class Embedder:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Embedder, cls).__new__(cls)
            # Lazy import to avoid hang on CLI startup
            from sentence_transformers import SentenceTransformer
            print("Loading embedding model (this may take a moment on first run)...")
            cls._instance.model = SentenceTransformer('all-MiniLM-L6-v2')
        return cls._instance

    def embed(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
