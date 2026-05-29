"""Build and persist a local vector index (vectors + chunk metadata) as ``.npz``.

Embedding is supplied as an injected ``embed`` callable (``list[str] -> np.ndarray``) so the
index logic is testable offline; the real embedder (fastembed) is wired in at sync time.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import numpy as np


@dataclass
class VectorIndex:
    """Chunk vectors plus the per-row metadata needed to return search results."""

    vectors: np.ndarray  # shape (n, dim), float32
    chunks: list[dict]  # per-row metadata (text, source, source_path, section, title, url)


def build_index(chunks, embed, *, batch_size=512, progress=None) -> VectorIndex:
    """Embed each chunk's text (in batches) and pair the vectors with the chunk metadata.

    ``progress`` is an optional ``(done, total) -> None`` callback invoked after each batch.
    """
    texts = [chunk.text for chunk in chunks]
    metadata = [asdict(chunk) for chunk in chunks]
    if not texts:
        return VectorIndex(vectors=np.zeros((0, 0), dtype=np.float32), chunks=metadata)

    total = len(texts)
    batches = []
    for start in range(0, total, batch_size):
        batches.append(np.asarray(embed(texts[start:start + batch_size]), dtype=np.float32))
        if progress:
            progress(min(start + batch_size, total), total)
    return VectorIndex(vectors=np.vstack(batches), chunks=metadata)


def save_index(index: VectorIndex, path) -> None:
    """Persist a :class:`VectorIndex` to ``path`` as ``.npz`` (metadata as JSON, no pickle)."""
    np.savez(str(path), vectors=index.vectors, meta=np.array(json.dumps(index.chunks)))


def load_index(path) -> VectorIndex:
    """Load a :class:`VectorIndex` from a ``.npz`` file."""
    data = np.load(str(path), allow_pickle=False)
    return VectorIndex(vectors=data["vectors"], chunks=json.loads(data["meta"].item()))
