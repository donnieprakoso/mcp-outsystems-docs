"""Real embedder adapter backed by ``fastembed`` (ONNX, fully local).

``fastembed`` is imported lazily and the model is constructed on first use, so the ~100MB
model downloads only when an actual embed happens — never at import or in the test suite.
On corrupt cache (NoSuchFile), clears the cache and retries once.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import numpy as np
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
FASTEMBED_CACHE_PATH = os.getenv("FASTEMBED_CACHE_PATH", "./temp/fastembed_cache")


def _clear_fastembed_cache():
    """Clear the fastembed model cache to recover from corruption."""
    cache_dir = Path(FASTEMBED_CACHE_PATH).expanduser().resolve()
    if cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)


def fastembed_embedder(model_name: str = DEFAULT_MODEL):
    """Return an ``embed(list[str]) -> np.ndarray`` callable backed by ``fastembed``.

    The model is loaded lazily on the first call (this is when the download happens).
    On corrupt cache (NoSuchFile), clears the cache and retries once.
    """
    model = None
    cache_path = Path(FASTEMBED_CACHE_PATH).expanduser().resolve()
    cache_path.mkdir(parents=True, exist_ok=True)
    os.environ["FASTEMBED_CACHE_PATH"] = str(cache_path)

    def embed(texts):
        nonlocal model
        if model is None:
            from fastembed import TextEmbedding

            try:
                model = TextEmbedding(model_name)
            except Exception as e:
                # If cache is corrupt (NoSuchFile), clear it and retry
                if "NoSuchFile" in e.__class__.__name__ or "File doesn't exist" in str(e):
                    _clear_fastembed_cache()
                    model = TextEmbedding(model_name)
                else:
                    raise
        return np.array(list(model.embed(list(texts))), dtype=np.float32)

    return embed
