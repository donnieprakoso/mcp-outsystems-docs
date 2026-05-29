"""Shared helpers for rendering generated text artifacts (``llms.txt``/``llms-full.txt``)."""

from __future__ import annotations

from collections.abc import Iterator

# A parsed toc entry, matching the output of :func:`osmcp.toc.parse_toc`.
TocEntry = dict  # {"href": str, "children": list[TocEntry]}

# Maps a top-level intro href to its section title (from osmcp.toc.parse_section_titles).
SectionTitles = dict[str, str]


def header(title: str, summary: str) -> str:
    """Render the shared H1 title + blockquote summary preamble."""
    return f"# {title}\n\n> {summary}\n"


def document(blocks: list[str]) -> str:
    """Join blocks with blank-line separators and a single trailing newline."""
    return "\n".join(blocks).rstrip() + "\n"


def iter_hrefs(tree: list[TocEntry]) -> Iterator[str]:
    """Yield every ``href`` in the tree, depth-first, in navigation order."""
    for node in tree:
        yield node["href"]
        yield from iter_hrefs(node["children"])


def humanize(text: str) -> str:
    """Turn a path/filename into a title, e.g. ``a/hello-world.md`` -> ``Hello World``."""
    name = text.rsplit("/", 1)[-1].removesuffix(".md")
    return name.replace("-", " ").replace("_", " ").title()
