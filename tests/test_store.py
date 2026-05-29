"""Tests for the serve phase (UC #9–#12): the in-memory DocStore."""

import numpy as np
import pytest

from osmcp.fetch import DocSource, FetchResult
from osmcp.index import VectorIndex
from osmcp.store import DocStore, load_store
from osmcp.sync import sync_sources


def _store_with_vectors():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0], [0.9, 0.1]], dtype=np.float32)
    chunks = [
        {"text": "a", "source": "odc", "source_path": "a.md", "section": "S", "title": "A", "url": "u"},
        {"text": "b", "source": "o11", "source_path": "b.md", "section": "S", "title": "B", "url": "u"},
        {"text": "c", "source": "odc", "source_path": "c.md", "section": "S", "title": "C", "url": "u"},
    ]
    return DocStore("", {}, {}, VectorIndex(vectors=vectors, chunks=chunks))


def fake_embed(texts):
    # 2-d deterministic vectors so cosine ordering is predictable in search tests.
    return np.array([[float(len(t)), 1.0] for t in texts], dtype=np.float32)


def build_data(tmp_path):
    """Produce a realistic data/ dir using the real sync pipeline + a fake embedder."""
    source = DocSource(
        name="odc", repo="r", label="OutSystems Developer Cloud (ODC)", summary="ODC docs.",
    )
    toc = "# Getting Started\n- href: gs/intro.md\n- topics:\n    - href: gs/setup.md\n"
    docs = {
        "gs/intro.md": "# Intro\n\nWelcome to ODC.\n",
        "gs/setup.md": "# Setup\n\nInstall the tools.\n",
    }
    sync_sources(
        [source], tmp_path, fetch=lambda s: FetchResult(toc=toc, docs=docs), embed=fake_embed
    )
    return tmp_path


def test_load_store_reads_indexes_docs_and_vectors(tmp_path):
    store = load_store(build_data(tmp_path))

    assert store.combined_index.startswith("# OutSystems Documentation")
    assert "odc" in store.source_indexes
    assert store.docs["odc"]["gs/intro.md"].startswith("# Intro")
    assert store.docs["odc"]["gs/setup.md"].startswith("# Setup")
    assert len(store.index.chunks) >= 2


def test_load_store_reads_synced_at(tmp_path):
    store = load_store(build_data(tmp_path))
    assert store.synced_at and "T" in store.synced_at  # ISO 8601 timestamp


def test_navigation_returns_combined_or_per_source_index(tmp_path):
    store = load_store(build_data(tmp_path))
    assert store.navigation() == store.combined_index
    assert store.navigation("odc") == store.source_indexes["odc"]
    with pytest.raises(KeyError, match="unknown source"):
        store.navigation("nope")


def test_get_doc_returns_content_or_none(tmp_path):
    store = load_store(build_data(tmp_path))
    assert store.get_doc("odc", "gs/intro.md").startswith("# Intro")
    assert store.get_doc("odc", "does/not-exist.md") is None
    assert store.get_doc("nope", "gs/intro.md") is None


def test_search_returns_top_k_by_cosine():
    store = _store_with_vectors()
    results = store.search(np.array([1.0, 0.0], dtype=np.float32), k=2)
    assert [r["source_path"] for r in results] == ["a.md", "c.md"]
    assert results[0]["score"] >= results[1]["score"]


def test_search_filters_by_source():
    store = _store_with_vectors()
    results = store.search(np.array([0.0, 1.0], dtype=np.float32), k=5, source="odc")
    assert {r["source"] for r in results} == {"odc"}


def test_search_empty_index_returns_empty():
    empty = DocStore("", {}, {}, VectorIndex(np.zeros((0, 0), dtype=np.float32), []))
    assert empty.search(np.array([1.0, 0.0], dtype=np.float32)) == []
