"""Generate ``llms.txt`` indexes from a parsed ``toc.yml`` document tree.

Two pure functions implement Option C of the project design:

* :func:`generate_llms_txt` renders one source's index (H1 title, blockquote summary, and
  one H2 section per top-level entry).
* :func:`combine_llms_txt` merges several sources into a single top-level index, with each
  platform as a labeled H2 section and its own sections demoted to H3 so ODC and O11
  navigation never get conflated.

Section headings use real titles from ``parse_section_titles`` when supplied, falling back
to the ``href`` folder name; link text is derived from each ``href``'s filename.
"""

from __future__ import annotations

from typing import NotRequired, TypedDict

from osmcp._render import SectionTitles, TocEntry, document, header, humanize, iter_hrefs


class Source(TypedDict):
    """One documentation source to combine."""

    label: str
    tree: list[TocEntry]
    titles: NotRequired[SectionTitles]


def generate_llms_txt(
    tree: list[TocEntry],
    *,
    title: str,
    summary: str,
    section_titles: SectionTitles | None = None,
) -> str:
    """Render one source's ``llms.txt`` from its parsed document tree."""
    return document([header(title, summary), *_render_sections(tree, 2, section_titles)])


def combine_llms_txt(sources: list[Source], *, title: str, summary: str) -> str:
    """Combine per-source trees into a top-level index with labeled platform sections."""
    parts = [header(title, summary)]
    for source in sources:
        parts.append(f"## {source['label']}\n")
        parts.extend(_render_sections(source["tree"], 3, source.get("titles")))
    return document(parts)


def _render_sections(
    tree: list[TocEntry], level: int, titles: SectionTitles | None = None
) -> list[str]:
    """Render each top-level entry as a heading (at ``level``) followed by its links."""
    titles = titles or {}
    hashes = "#" * level
    blocks = []
    for node in tree:
        heading = titles.get(node["href"]) or _section_name(node["href"])
        links = "\n".join(f"- [{humanize(href)}]({href})" for href in iter_hrefs([node]))
        blocks.append(f"{hashes} {heading}\n{links}\n")
    return blocks


def _section_name(href: str) -> str:
    parts = href.split("/")
    folder = parts[-2] if len(parts) >= 2 else parts[-1]
    return humanize(folder)
