"""Generate a per-source ``llms-full.txt`` — full doc contents concatenated in order.

Documents are emitted in navigation order, each preceded by a delimiter recording its
source ``href``. When ``section_titles`` is supplied, an H2 heading is inserted ahead of
each top-level section's documents.
"""

from __future__ import annotations

import re

from osmcp._render import SectionTitles, TocEntry, document, header, iter_hrefs

_SOURCE_MARKER = re.compile(r"(?m)^---\nsource: (.+)\n---\n")


def generate_llms_full_txt(
    tree: list[TocEntry],
    docs: dict[str, str],
    *,
    title: str,
    summary: str,
    section_titles: SectionTitles | None = None,
) -> str:
    section_titles = section_titles or {}
    blocks = [header(title, summary)]
    for node in tree:
        heading = section_titles.get(node["href"])
        if heading:
            blocks.append(f"## {heading}\n")
        for href in iter_hrefs([node]):
            content = docs.get(href, "").rstrip()
            blocks.append(f"---\nsource: {href}\n---\n\n{content}\n")
    return document(blocks)


def parse_llms_full(text: str) -> dict[str, str]:
    """Inverse of :func:`generate_llms_full_txt`: recover ``{href: content}``.

    Splits on the ``source:`` delimiters; any trailing section heading that belongs to the
    *next* section is dropped from a document's body.
    """
    parts = _SOURCE_MARKER.split(text)[1:]  # drop the title/summary preamble
    docs = {}
    for href, body in zip(parts[::2], parts[1::2]):
        docs[href.strip()] = _strip_trailing_heading(body)
    return docs


def _strip_trailing_heading(body: str) -> str:
    lines = body.strip("\n").rstrip().split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    if lines and re.match(r"^#{1,6}\s", lines[-1]):  # heading introducing the next section
        lines.pop()
    return "\n".join(lines).strip()
