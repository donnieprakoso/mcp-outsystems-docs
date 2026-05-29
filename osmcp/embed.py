"""Real embedder adapter backed by ``fastembed`` (ONNX, fully local).

``fastembed`` is imported lazily and the model is constructed on first use, so the ~100MB
model downloads only when an actual embed happens — never at import or in the test suite.
"""

from __future__ import annotations

import numpy as np

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"


def fastembed_embedder(model_name: str = DEFAULT_MODEL):
    """Return an ``embed(list[str]) -> np.ndarray`` callable backed by ``fastembed``.

    The model is loaded lazily on the first call (this is when the download happens).
    """
    model = None

    def embed(texts):
        nonlocal model
        if model is None:
            from fastembed import TextEmbedding

            model = TextEmbedding(model_name)
        return np.array(list(model.embed(list(texts))), dtype=np.float32)

    return embed
