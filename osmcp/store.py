"""In-memory document store loaded from the synced ``data/`` artifacts (serve phase)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from osmcp.index import VectorIndex, load_index
from osmcp.llms_full import parse_llms_full


@dataclass
class DocStore:
    """Everything the MCP server needs in memory to answer requests."""

    combined_index: str  # data/llms.txt (combined navigation)
    source_indexes: dict  # {source_name: per-source llms.txt}
    docs: dict  # {source_name: {href: full content}}
    index: VectorIndex  # vectors + chunk metadata
    synced_at: str | None = None  # ISO timestamp of the last sync

    def navigation(self, source=None) -> str:
        """Return the combined `llms.txt`, or one source's index when ``source`` is given."""
        if source is None:
            return self.combined_index
        if source not in self.source_indexes:
            raise KeyError(f"unknown source {source!r}; available: {sorted(self.source_indexes)}")
        return self.source_indexes[source]

    def get_doc(self, source, path):
        """Return the full Markdown for ``source``/``path``, or ``None`` if not found."""
        return self.docs.get(source, {}).get(path)

    def search(self, query_vector, k=5, source=None) -> list[dict]:
        """Return the top-``k`` chunks by cosine similarity, optionally scoped to ``source``."""
        rows = [
            i for i, chunk in enumerate(self.index.chunks)
            if source is None or chunk["source"] == source
        ]
        if not rows or self.index.vectors.shape[0] == 0:
            return []

        candidates = self.index.vectors[rows]
        query = np.asarray(query_vector, dtype=np.float32).reshape(-1)
        norms = np.linalg.norm(candidates, axis=1) * np.linalg.norm(query)
        scores = (candidates @ query) / (norms + 1e-12)

        results = []
        for j in np.argsort(-scores)[:k]:
            result = dict(self.index.chunks[rows[j]])
            result["score"] = float(scores[j])
            results.append(result)
        return results


def load_store(data_dir) -> DocStore:
    """Load combined/per-source indexes, full docs, and the vector index from ``data_dir``."""
    data_dir = Path(data_dir)
    source_indexes = {}
    docs = {}
    for child in sorted(data_dir.iterdir()):
        if child.is_dir() and (child / "llms-full.txt").exists():
            source_indexes[child.name] = (child / "llms.txt").read_text(encoding="utf-8")
            docs[child.name] = parse_llms_full(
                (child / "llms-full.txt").read_text(encoding="utf-8")
            )
    synced_at_path = data_dir / "synced_at.txt"
    synced_at = synced_at_path.read_text(encoding="utf-8").strip() if synced_at_path.exists() else None
    return DocStore(
        combined_index=(data_dir / "llms.txt").read_text(encoding="utf-8"),
        source_indexes=source_indexes,
        docs=docs,
        index=load_index(data_dir / "vectors.npz"),
        synced_at=synced_at,
    )
