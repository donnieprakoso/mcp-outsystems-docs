"""Wiring tests for the FastMCP server: tools/resource delegate to the DocStore."""

import numpy as np

import osmcp.server as server
from osmcp.index import VectorIndex
from osmcp.store import DocStore


def _fake_store():
    return DocStore(
        combined_index="COMBINED INDEX",
        source_indexes={"odc": "ODC INDEX"},
        docs={"odc": {"a.md": "Full body."}},
        index=VectorIndex(
            np.array([[1.0, 0.0]], dtype=np.float32),
            [{"text": "a", "source": "odc", "source_path": "a.md", "section": "S",
              "title": "A", "url": "u"}],
        ),
        synced_at="2026-05-29T12:00:00+00:00",
    )


def test_server_resource_and_tools_delegate_to_store(monkeypatch):
    # Pre-load the module globals so nothing touches disk/network/model.
    monkeypatch.setattr(server, "_store", _fake_store())
    monkeypatch.setattr(server, "_embed", lambda texts: np.array([[1.0, 0.0]], dtype=np.float32))

    assert server.llms_index() == "COMBINED INDEX"
    assert server.get_doc("odc", "a.md") == "Full body."
    assert "not found" in server.get_doc("odc", "missing.md").lower()

    payload = server.search_docs("anything", k=1)
    assert payload["results"][0]["source_path"] == "a.md"
    assert payload["synced_at"] == "2026-05-29T12:00:00+00:00"
    assert server.last_updated() == "2026-05-29T12:00:00+00:00"
