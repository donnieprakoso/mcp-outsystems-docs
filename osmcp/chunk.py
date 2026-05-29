"""Split a Markdown document into heading-aware, embeddable chunks with metadata."""

from __future__ import annotations

import re
from dataclasses import dataclass

_HEADING = re.compile(r"^#{1,6}\s+(.*)$")


@dataclass(frozen=True)
class Chunk:
    """One embeddable segment of a document, carrying retrieval metadata."""

    text: str
    source: str  # platform tag: "odc" | "o11"
    source_path: str  # the document's href
    section: str  # heading this chunk belongs to
    title: str  # document title
    url: str  # link to the document


def chunk_markdown(content, *, source, source_path, title, url, max_words=400, overlap=50):
    """Split ``content`` into heading-aware chunks tagged with metadata.

    Each heading starts a section; sections longer than ``max_words`` are split into
    overlapping windows so a chunk never loses too much surrounding context.
    """
    chunks = []
    for section, text in _split_sections(content, title):
        for piece in _split_long(text, max_words, overlap):
            chunks.append(
                Chunk(
                    text=piece,
                    source=source,
                    source_path=source_path,
                    section=section,
                    title=title,
                    url=url,
                )
            )
    return chunks


def _split_long(text, max_words, overlap):
    """Split ``text`` into overlapping windows of at most ``max_words`` words."""
    words = text.split()
    if len(words) <= max_words:
        return [text]
    step = max(1, max_words - overlap)
    pieces = []
    for start in range(0, len(words), step):
        pieces.append(" ".join(words[start:start + max_words]))
        if start + max_words >= len(words):
            break
    return pieces


def _split_sections(content, title):
    """Yield ``(section_name, text)`` pairs, one per heading (preamble uses ``title``)."""
    sections = []
    name = title
    lines = []

    def flush():
        if any(line.strip() for line in lines):
            sections.append((name, "\n".join(lines).strip()))

    for line in content.splitlines():
        heading = _HEADING.match(line)
        if heading:
            flush()
            name = heading.group(1).strip()
            lines = [line]
        else:
            lines.append(line)
    flush()
    return sections
