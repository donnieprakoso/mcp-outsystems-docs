"""Parse an OutSystems ``toc.yml`` into an ordered, nested document tree.

The OutSystems ``toc.yml`` uses only two data keys: ``href`` (a document path) and
``topics`` (a nested list). An item's children are the entries of the *immediately
following* sibling ``topics`` block, applied recursively.

Section titles are YAML comments, which ``yaml.safe_load`` discards; :func:`parse_toc`
returns the structural tree, while :func:`parse_section_titles` recovers those titles
from the raw text.
"""

from __future__ import annotations

import yaml

# A parsed entry: {"href": <path>, "children": [<TocEntry>, ...]}.
TocEntry = dict


def parse_toc(text: str) -> list[TocEntry]:
    """Parse ``toc.yml`` text into an ordered list of nested ``TocEntry`` dicts."""
    return _build_tree(yaml.safe_load(text) or [])


def parse_section_titles(text: str) -> dict[str, str]:
    """Map each top-level section's intro ``href`` to its title.

    Titles are YAML comments (``# …``) that ``yaml.safe_load`` discards, so they are read
    from the raw text: a top-level comment becomes the title of the next top-level
    ``- href:`` entry.
    """
    titles: dict[str, str] = {}
    pending: str | None = None
    for line in text.splitlines():
        if line[:1].isspace() or not line.strip():
            continue  # only top-level (column-0) lines carry section structure
        stripped = line.strip()
        if stripped.startswith("#"):
            pending = stripped.lstrip("#").strip()
        elif stripped.startswith("- href:"):
            if pending:
                titles[stripped[len("- href:"):].strip()] = pending
            pending = None
        elif stripped.startswith("- topics:"):
            pending = None
    return titles


def _build_tree(items: list) -> list[TocEntry]:
    """Convert a raw ``toc.yml`` list into href nodes.

    Each ``href`` item becomes a node; a following ``topics`` item supplies the children
    of the preceding node. A ``topics`` block with no preceding node is hoisted to the
    current level, and entries with neither key are skipped.
    """
    nodes: list[TocEntry] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if "href" in item:
            nodes.append({"href": item["href"], "children": []})
        elif "topics" in item:
            children = _build_tree(item["topics"] or [])
            target = nodes[-1]["children"] if nodes else nodes
            target.extend(children)
    return nodes
