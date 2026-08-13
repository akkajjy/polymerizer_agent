import numpy as np
from sentence_transformers import SentenceTransformer

_model = None

def get_model() -> SentenceTransformer:
    """Lazy loading singleton pattern: the model is loaded only once during the first call, and the same instance is reused subsequently"""
    global _model
    if _model is None:
        _model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return _model

def compute_embedding(text: str) -> list[float]:
    model = get_model()
    vec = model.encode(text, normalize_embeddings=True)
    return vec.tolist()

def cosine_similarity(a: list[float], b: list[float]) -> float:
    # the vector has been normalized, and at this point, the dot product is equal to the cosine similarity, so there is no need to calculate the modulus again
    return float(np.dot(np.array(a), np.array(b)))

