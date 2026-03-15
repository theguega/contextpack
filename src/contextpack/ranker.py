from typing import List
from .models import ContextChunk
from .embeddings import Embedder, cosine_similarity
import numpy as np

def rank_chunks(query: str, chunks: List[ContextChunk], top_k: int = 5) -> List[ContextChunk]:
    """
    Ranks chunks by cosine similarity to the query.
    """
    if not chunks:
        return []

    embedder = Embedder()
    query_emb = embedder.embed([query])[0]
    chunk_texts = [c.text for c in chunks]
    chunk_embs = embedder.embed(chunk_texts)
    
    for i, chunk in enumerate(chunks):
        chunk.score = cosine_similarity(query_emb, chunk_embs[i])
        
    ranked = sorted(chunks, key=lambda x: x.score, reverse=True)
    return ranked[:top_k]
