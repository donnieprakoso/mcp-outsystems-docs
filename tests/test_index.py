"""Tests for Use Case #6: build/save/load the local vector index (embedder injected)."""

import numpy as np

from osmcp.chunk import Chunk
from osmcp.index import build_index, load_index, save_index


def fake_embed(texts):
    # Deterministic, dependency-free stand-in for fastembed: vector = [len(text), 1.0].
    return np.array([[float(len(t)), 1.0] for t in texts], dtype=np.float32)


def _chunks():
    return [
        Chunk(text="abc", source="odc", source_path="a.md", section="S", title="T", url="u"),
        Chunk(text="hello", source="o11", source_path="b.md", section="S2", title="T2", url="u2"),
    ]


def test_build_index_reports_progress_per_batch():
    chunks = [
        Chunk(text=f"t{i}", source="odc", source_path="a.md", section="S", title="A", url="u")
        for i in range(5)
    ]
    seen = []
    index = build_index(
        chunks, embed=fake_embed, batch_size=2, progress=lambda done, total: seen.append((done, total))
    )
    assert index.vectors.shape == (5, 2)
    assert seen == [(2, 5), (4, 5), (5, 5)]


def test_build_index_embeds_chunks_and_preserves_metadata():
    index = build_index(_chunks(), embed=fake_embed)

    assert index.vectors.shape == (2, 2)
    assert index.vectors[0, 0] == 3.0  # len("abc")
    assert index.vectors[1, 0] == 5.0  # len("hello")
    assert index.chunks[0]["source"] == "odc"
    assert index.chunks[1]["source_path"] == "b.md"
    assert index.chunks[0]["text"] == "abc"


def test_save_and_load_index_round_trips(tmp_path):
    index = build_index(_chunks(), embed=fake_embed)
    path = tmp_path / "vectors.npz"

    save_index(index, path)
    loaded = load_index(path)

    assert np.array_equal(loaded.vectors, index.vectors)
    assert loaded.chunks == index.chunks


def test_build_and_round_trip_empty_index(tmp_path):
    index = build_index([], embed=fake_embed)  # embed is not called when there are no chunks
    assert index.vectors.shape == (0, 0)
    assert index.chunks == []

    path = tmp_path / "empty.npz"
    save_index(index, path)
    loaded = load_index(path)
    assert loaded.vectors.shape == (0, 0)
    assert loaded.chunks == []
