"""Tests for the fastembed adapter with cache recovery."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

from osmcp.embed import fastembed_embedder


def test_fastembed_handles_corrupt_cache():
    """When model cache is corrupt (file missing), clear cache and retry.

    Simulates: fastembed detects file-size mismatch, fails to re-download,
    then TextEmbedding raises NoSuchFile on __init__. Our embedder should
    recover by clearing the cache and retrying.
    """
    call_count = 0

    class NoSuchFile(Exception):
        """Simulate onnxruntime.capi.onnxruntime_pybind11_state.NoSuchFile."""
        pass

    def mock_text_embedding(model_name):
        """Simulate: first call fails (corrupt cache), second call succeeds."""
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # First call: corrupt cache
            raise NoSuchFile("Load model .../model_optimized.onnx failed. File doesn't exist")
        else:
            # Second call: cache was cleared, model loads
            mock_model = MagicMock()
            mock_model.embed = lambda texts: [[0.1, 0.2, 0.3]] * len(texts)
            return mock_model

    # Patch at the point of import (inside the embed function)
    with patch("fastembed.TextEmbedding", side_effect=mock_text_embedding):
        embedder = fastembed_embedder("BAAI/bge-small-en-v1.5")
        result = embedder(["hello world"])

        # Should have succeeded on retry
        assert result.shape == (1, 3)
        assert call_count == 2  # First call failed, second succeeded


def test_fastembed_retry_still_fails():
    """When cache clear + retry still fails, raise the original error."""
    class NoSuchFile(Exception):
        """Simulate onnxruntime.capi.onnxruntime_pybind11_state.NoSuchFile."""
        pass

    def mock_text_embedding_always_fails(model_name):
        """Always fail — even after cache clear."""
        raise NoSuchFile("Load model failed (unrecoverable)")

    with patch("fastembed.TextEmbedding", side_effect=mock_text_embedding_always_fails):
        embedder = fastembed_embedder("BAAI/bge-small-en-v1.5")
        with pytest.raises(NoSuchFile, match="unrecoverable"):
            embedder(["hello world"])
