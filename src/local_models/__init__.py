"""
Local Model Implementations for Mac Studio
Replaces NVIDIA NIMs with local Apple Silicon-optimized models
"""

from .reasoning_model import LocalReasoningModel
from .embedding_model import LocalEmbeddingModel

__all__ = ['LocalReasoningModel', 'LocalEmbeddingModel']

