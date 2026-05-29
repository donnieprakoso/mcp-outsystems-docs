"""Tests for Use Case #7: orchestrate the sync pipeline (fetch + embed injected)."""

from datetime import datetime, timezone

import numpy as np

from osmcp.fetch import DocSource, FetchResult
from osmcp.index import load_index
from osmcp.sync import sync_sources


def fake_embed(texts):
    return np.array([[float(len(t))] for t in texts], dtype=np.float32)


def make_fetch(results):
    def fetch(source):
        return results[source.name]

    return fetch


def test_sync_writes_per_source_and_combined_artifacts(tmp_path):
    toc = "# Getting Started\n- href: getting-started/intro.md\n"
    docs = {"getting-started/intro.md": "# Intro\n\nWelcome to ODC.\n"}
    source = DocSource(
        name="odc", repo="r", branch="main",
        label="OutSystems Developer Cloud (ODC)", summary="ODC docs.",
    )
    fetch = make_fetch({"odc": FetchResult(toc=toc, docs=docs)})

    report = sync_sources([source], tmp_path, fetch=fetch, embed=fake_embed)

    # Per-source index uses the real comment-derived section title.
    odc_llms = (tmp_path / "odc" / "llms.txt").read_text(encoding="utf-8")
    assert odc_llms.startswith("# OutSystems Developer Cloud (ODC)")
    assert "## Getting Started" in odc_llms
    assert (tmp_path / "odc" / "llms-full.txt").exists()

    # Combined top-level index labels the platform.
    combined = (tmp_path / "llms.txt").read_text(encoding="utf-8")
    assert "## OutSystems Developer Cloud (ODC)" in combined

    # Vector index built from the source-tagged chunks.
    index = load_index(tmp_path / "vectors.npz")
    assert len(index.chunks) >= 1
    assert index.chunks[0]["source"] == "odc"

    assert report.num_sources == 1


def test_sync_combines_multiple_sources_keeping_platforms_tagged(tmp_path):
    odc = DocSource(name="odc", repo="r1", label="OutSystems Developer Cloud (ODC)")
    o11 = DocSource(name="o11", repo="r2", branch="master", label="OutSystems 11 (O11)")
    fetch = make_fetch({
        "odc": FetchResult(toc="# A\n- href: a/intro.md\n", docs={"a/intro.md": "ODC body\n"}),
        "o11": FetchResult(toc="# B\n- href: b/intro.md\n", docs={"b/intro.md": "O11 body\n"}),
    })

    report = sync_sources([odc, o11], tmp_path, fetch=fetch, embed=fake_embed)

    combined = (tmp_path / "llms.txt").read_text(encoding="utf-8")
    assert "## OutSystems Developer Cloud (ODC)" in combined
    assert "## OutSystems 11 (O11)" in combined
    assert (tmp_path / "odc" / "llms.txt").exists()
    assert (tmp_path / "o11" / "llms.txt").exists()

    index = load_index(tmp_path / "vectors.npz")
    assert {c["source"] for c in index.chunks} == {"odc", "o11"}
    assert report.num_sources == 2


def test_sync_reports_progress(tmp_path):
    msgs = []
    source = DocSource(name="odc", repo="r", label="ODC", summary="s.")
    toc = "# GS\n- href: a/intro.md\n"
    docs = {"a/intro.md": "# Intro\n\nbody\n"}

    sync_sources(
        [source], tmp_path, fetch=lambda s: FetchResult(toc=toc, docs=docs),
        embed=fake_embed, progress=msgs.append,
    )

    joined = "\n".join(msgs)
    assert "odc" in joined  # per-source stage reported
    assert any("embed" in m.lower() for m in msgs)  # the slow step is announced


def test_sync_writes_synced_at_timestamp(tmp_path):
    source = DocSource(name="odc", repo="r", label="ODC", summary="s.")
    fixed = datetime(2026, 5, 29, 12, 0, 0, tzinfo=timezone.utc)

    report = sync_sources(
        [source], tmp_path,
        fetch=lambda s: FetchResult(toc="# A\n- href: a.md\n", docs={"a.md": "# A\n\nb\n"}),
        embed=fake_embed, now=lambda: fixed,
    )

    assert (tmp_path / "synced_at.txt").read_text(encoding="utf-8").strip() == fixed.isoformat()
    assert report.synced_at == fixed.isoformat()


def test_sync_resolves_canonical_urls_from_sitemap(tmp_path):
    source = DocSource(name="odc", repo="r", label="ODC", summary="s.")
    toc = "# GS\n- href: getting-started/sample-app.md\n"
    docs = {"getting-started/sample-app.md": "# Build a basic Web app\n\nbody\n"}
    sitemap = [
        "https://success.outsystems.com/documentation/outsystems_developer_cloud/"
        "getting_started/build_a_basic_web_app/",
    ]

    sync_sources(
        [source], tmp_path, fetch=lambda s: FetchResult(toc=toc, docs=docs),
        embed=fake_embed, sitemap_urls=sitemap,
    )

    index = load_index(tmp_path / "vectors.npz")
    # The chunk's url is the verified canonical URL resolved from the H1 title.
    assert index.chunks[0]["url"] == sitemap[0]
