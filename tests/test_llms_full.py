"""Tests for Use Case #3: generate per-source ``llms-full.txt``."""

from osmcp.llms_full import generate_llms_full_txt, parse_llms_full

TREE = [
    {
        "href": "getting-started/intro.md",
        "children": [
            {"href": "getting-started/install.md", "children": []},
        ],
    },
]
DOCS = {
    "getting-started/intro.md": "Welcome to ODC.\n",
    "getting-started/install.md": "Install steps here.\n",
}


def test_generate_llms_full_txt_concatenates_docs_in_order():
    # H1 title + summary, then each document in navigation order, separated by a delimiter
    # that records the source href.
    assert generate_llms_full_txt(TREE, DOCS, title="ODC", summary="ODC docs.") == (
        "# ODC\n"
        "\n"
        "> ODC docs.\n"
        "\n"
        "---\n"
        "source: getting-started/intro.md\n"
        "---\n"
        "\n"
        "Welcome to ODC.\n"
        "\n"
        "---\n"
        "source: getting-started/install.md\n"
        "---\n"
        "\n"
        "Install steps here.\n"
    )


def test_generate_llms_full_txt_inserts_section_headers_from_titles():
    out = generate_llms_full_txt(
        TREE,
        DOCS,
        title="ODC",
        summary="s.",
        section_titles={"getting-started/intro.md": "Getting Started"},
    )
    assert "## Getting Started\n" in out
    # the heading precedes the section's first document
    assert out.index("## Getting Started") < out.index("source: getting-started/intro.md")


def test_generate_llms_full_txt_tolerates_missing_doc_content():
    tree = [{"href": "a.md", "children": []}]
    out = generate_llms_full_txt(tree, {}, title="T", summary="s.")
    # No KeyError; the document is simply emitted with an empty body.
    assert "source: a.md" in out


def test_parse_llms_full_round_trips_generated_output():
    tree = [{"href": "a/intro.md", "children": []}, {"href": "b/intro.md", "children": []}]
    docs = {"a/intro.md": "Alpha body.\n", "b/intro.md": "Beta body.\n"}
    full = generate_llms_full_txt(
        tree, docs, title="T", summary="s.",
        section_titles={"a/intro.md": "Section A", "b/intro.md": "Section B"},
    )
    # Recovers each doc's body; the next section's heading is not leaked into it.
    assert parse_llms_full(full) == {"a/intro.md": "Alpha body.", "b/intro.md": "Beta body."}
