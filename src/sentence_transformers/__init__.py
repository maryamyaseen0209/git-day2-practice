"""Mock sentence_transformers module for Docker build"""
import numpy as np

class SentenceTransformer:
    def __init__(self, model_name, device=None, cache_folder=None):
        self.model_name = model_name
        self.device = device
    
    def encode(self, sentences, batch_size=32, show_progress_bar=False, 
               convert_to_numpy=True, convert_to_tensor=False, device=None,
               normalize_embeddings=False):
        """Return dummy embeddings - accepts all parameters"""
        if isinstance(sentences, str):
            embedding = np.random.randn(384) * 0.1
        else:
            embedding = np.random.randn(len(sentences), 384) * 0.1
        
        if normalize_embeddings:
            if embedding.ndim == 1:
                embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
            else:
                norms = np.linalg.norm(embedding, axis=1, keepdims=True)
                embedding = embedding / (norms + 1e-8)
        
        return embedding

# Also add a mock for the module itself
import sys
sys.modules['sentence_transformers'] = sys.modules[__name__]

