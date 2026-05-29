"""Tests for Use Case #5: chunk Markdown into embeddable segments with metadata."""

from osmcp.chunk import Chunk, chunk_markdown

DOC = """\
# Building Mobile Apps

Intro paragraph about mobile.

## Getting Started

Install the tools.

## Publishing

Push to the store.
"""


def test_chunk_markdown_splits_by_heading_with_metadata():
    chunks = chunk_markdown(
        DOC,
        source="odc",
        source_path="building-apps/mobile.md",
        title="Building Mobile Apps",
        url="https://docs/odc/building-apps/mobile.md",
    )

    meta = dict(
        source="odc",
        source_path="building-apps/mobile.md",
        title="Building Mobile Apps",
        url="https://docs/odc/building-apps/mobile.md",
    )
    assert chunks == [
        Chunk(text="# Building Mobile Apps\n\nIntro paragraph about mobile.",
              section="Building Mobile Apps", **meta),
        Chunk(text="## Getting Started\n\nInstall the tools.",
              section="Getting Started", **meta),
        Chunk(text="## Publishing\n\nPush to the store.",
              section="Publishing", **meta),
    ]


def test_chunk_markdown_splits_long_sections_into_overlapping_windows():
    text = "alpha beta gamma delta epsilon zeta eta theta iota kappa"
    chunks = chunk_markdown(
        text, source="o11", source_path="a.md", title="A", url="u",
        max_words=4, overlap=1,
    )
    assert [c.text for c in chunks] == [
        "alpha beta gamma delta",
        "delta epsilon zeta eta",  # one-word overlap with the previous window
        "eta theta iota kappa",
    ]
    assert all(c.section == "A" and c.source == "o11" for c in chunks)


def test_chunk_markdown_with_no_headings_uses_title_as_section():
    chunks = chunk_markdown(
        "Just a paragraph.", source="odc", source_path="x.md", title="X Doc", url="u"
    )
    assert len(chunks) == 1
    assert chunks[0].section == "X Doc"
    assert chunks[0].text == "Just a paragraph."


def test_chunk_markdown_empty_document_yields_no_chunks():
    assert chunk_markdown(
        "\n\n  \n", source="odc", source_path="x.md", title="X", url="u"
    ) == []
