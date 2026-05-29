"""Tests for Use Case #1: parse ``toc.yml`` into an ordered, nested document tree."""

from osmcp.toc import parse_section_titles, parse_toc

# Mirrors the real OutSystems toc.yml schema: section titles are YAML *comments*
# (ignored here), data keys are only `href` and `topics`, and an item's children
# live in the next sibling `- topics:` block (recursively).
SAMPLE_TOC = """\
# Getting started
- href: getting-started/intro.md
- topics:
    - href: getting-started/install.md
    - href: getting-started/hello-world.md

# Building apps
- href: building-apps/intro.md
- topics:
    - href: building-apps/data/intro.md
    - topics:
        - href: building-apps/data/entities.md
"""


def test_parse_toc_empty_input_returns_empty_list():
    # Empty text, and a file with only comments/blank lines, yield no entries.
    assert parse_toc("") == []
    assert parse_toc("# just a section comment\n\n") == []


def test_parse_toc_hoists_topics_without_a_preceding_href():
    # A `topics` block with no preceding `href` sibling is lifted to the current level
    # rather than dropped.
    toc = """\
- topics:
    - href: a.md
    - href: b.md
"""
    assert parse_toc(toc) == [
        {"href": "a.md", "children": []},
        {"href": "b.md", "children": []},
    ]


def test_parse_toc_ignores_unknown_entries():
    # Entries that are neither `href` nor `topics` are skipped without error.
    toc = """\
- href: a.md
- note: ignore me
- href: b.md
"""
    assert parse_toc(toc) == [
        {"href": "a.md", "children": []},
        {"href": "b.md", "children": []},
    ]


def test_parse_section_titles_maps_intro_href_to_comment_title():
    # The comment immediately above a section's intro `- href:` is that section's title.
    sample = """\
# Getting started with ODC
- href: eap/getting-started/intro.md
- topics:
    - href: eap/getting-started/install.md

# Onboarding for developers
- href: eap/onboarding/intro.md
- topics:
    - href: eap/onboarding/differences-sql.md
"""
    assert parse_section_titles(sample) == {
        "eap/getting-started/intro.md": "Getting started with ODC",
        "eap/onboarding/intro.md": "Onboarding for developers",
    }


def test_parse_section_titles_skips_uncommented_sections_and_nested_comments():
    # A section with no preceding comment is omitted; comments inside `topics` (indented)
    # are not treated as top-level section titles.
    sample = """\
# Top section
- href: a/intro.md
- topics:
    # nested comment (ignored)
    - href: a/child.md
- href: b/intro.md
"""
    assert parse_section_titles(sample) == {"a/intro.md": "Top section"}


def test_parse_toc_preserves_order_and_nesting():
    assert parse_toc(SAMPLE_TOC) == [
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
