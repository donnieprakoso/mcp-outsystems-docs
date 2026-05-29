"""FastMCP server exposing the OutSystems documentation store over stdio.

Serves the combined ``llms.txt`` as a navigation resource and ``get_doc`` / ``search_docs``
as tools. The store and the (local) query embedder are loaded lazily on first use, so the
model downloads only when a search actually runs — never at import.
"""

from __future__ import annotations

import os

from mcp.server.fastmcp import FastMCP

from osmcp.embed import fastembed_embedder
from osmcp.store import load_store

DATA_DIR = os.environ.get("OSMCP_DATA_DIR", "data")

mcp = FastMCP("outsystems-docs")
_store = None
_embed = None


def _ensure_loaded():
    global _store, _embed
    if _store is None:
        _store = load_store(DATA_DIR)
    if _embed is None:
        _embed = fastembed_embedder()
    return _store, _embed


@mcp.resource("llms://index")
def llms_index() -> str:
    """The combined OutSystems ODC + O11 documentation index (llms.txt)."""
    store, _ = _ensure_loaded()
    return store.navigation()


@mcp.tool()
def get_doc(source: str, path: str) -> str:
    """Return the full Markdown of a document. ``source`` is ``odc`` or ``o11``."""
    store, _ = _ensure_loaded()
    doc = store.get_doc(source, path)
    return doc if doc is not None else f"Document not found: {source}/{path}"


@mcp.tool()
def search_docs(query: str, k: int = 5, source: str | None = None) -> dict:
    """Semantic search over the docs. Optionally scope to one platform (``odc``/``o11``).

    Returns ``{"synced_at": <ISO timestamp>, "results": [...]}`` so the caller can show how
    fresh the docs are.
    """
    store, embed = _ensure_loaded()
    query_vector = embed([query])[0]
    return {"synced_at": store.synced_at, "results": store.search(query_vector, k=k, source=source)}


@mcp.tool()
def last_updated() -> str:
    """Return the ISO timestamp of the last docs sync (when the local data was built)."""
    store, _ = _ensure_loaded()
    return store.synced_at or "unknown"


def main() -> None:
    """Run the MCP server over stdio (entry point: ``osmcp-serve``)."""
    mcp.run()


if __name__ == "__main__":
    main()
