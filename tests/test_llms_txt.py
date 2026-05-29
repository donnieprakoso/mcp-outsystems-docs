"""Tests for Use Case #2: generate per-source + combined ``llms.txt`` (Option C)."""

from osmcp.llms_txt import combine_llms_txt, generate_llms_txt

# A parsed toc tree (the output shape of osmcp.toc.parse_toc).
TREE = [
    {
        "href": "getting-started/intro.md",
        "children": [
            {"href": "getting-started/install.md", "children": []},
            {"href": "getting-started/hello-world.md", "children": []},
        ],
    },
    {
        "href": "building-apps/intro.md",
        "children": [
            {
                "href": "building-apps/data/intro.md",
                "children": [
                    {"href": "building-apps/data/entities.md", "children": []},
                ],
            },
        ],
    },
]


def test_generate_llms_txt_structure():
    # H1 title, blockquote summary, one H2 section per top-level entry (named from the
    # folder), and a flat bullet list of links (named from the filename) for the entry
    # and all its descendants, in navigation order.
    assert generate_llms_txt(
        TREE,
        title="OutSystems Developer Cloud (ODC)",
        summary="ODC documentation.",
    ) == (
        "# OutSystems Developer Cloud (ODC)\n"
        "\n"
        "> ODC documentation.\n"
        "\n"
        "## Getting Started\n"
        "- [Intro](getting-started/intro.md)\n"
        "- [Install](getting-started/install.md)\n"
        "- [Hello World](getting-started/hello-world.md)\n"
        "\n"
        "## Building Apps\n"
        "- [Intro](building-apps/intro.md)\n"
        "- [Intro](building-apps/data/intro.md)\n"
        "- [Entities](building-apps/data/entities.md)\n"
    )


def test_generate_llms_txt_with_no_entries_emits_header_only():
    # An empty tree still produces a valid index: just the title and summary.
    assert generate_llms_txt([], title="Empty", summary="Nothing here.") == (
        "# Empty\n\n> Nothing here.\n"
    )


def test_generate_llms_txt_uses_section_titles_when_provided():
    # Real section titles (from parse_section_titles) override the folder-derived heading.
    tree = [
        {
            "href": "getting-started/intro.md",
            "children": [{"href": "getting-started/install.md", "children": []}],
        }
    ]
    out = generate_llms_txt(
        tree,
        title="ODC",
        summary="s.",
        section_titles={"getting-started/intro.md": "Getting Started with ODC"},
    )
    assert "## Getting Started with ODC\n" in out
    assert "## Getting Started\n" not in out  # folder-derived fallback was overridden


def test_combine_llms_txt_labels_platforms():
    # Each platform is an H2 label; its sections are demoted to H3 beneath it so ODC and
    # O11 navigation never get conflated.
    sources = [
        {
            "label": "OutSystems Developer Cloud (ODC)",
            "tree": [{"href": "getting-started/intro.md", "children": []}],
        },
        {
            "label": "OutSystems 11 (O11)",
            "tree": [{"href": "building-apps/intro.md", "children": []}],
        },
    ]
    assert combine_llms_txt(
        sources,
        title="OutSystems Documentation",
        summary="Combined ODC + O11 docs.",
    ) == (
        "# OutSystems Documentation\n"
        "\n"
        "> Combined ODC + O11 docs.\n"
        "\n"
        "## OutSystems Developer Cloud (ODC)\n"
        "\n"
        "### Getting Started\n"
        "- [Intro](getting-started/intro.md)\n"
        "\n"
        "## OutSystems 11 (O11)\n"
        "\n"
        "### Building Apps\n"
        "- [Intro](building-apps/intro.md)\n"
    )
