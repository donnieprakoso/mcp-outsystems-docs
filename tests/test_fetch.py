"""Tests for Use Case #4: fetch docs from a configured source (git clone mocked)."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from osmcp.fetch import DocSource, FetchError, collect_docs, fetch_source, sparse_clone


def test_collect_docs_reads_markdown_relative_to_src(tmp_path):
    src = tmp_path / "src" / "getting-started"
    src.mkdir(parents=True)
    (src / "intro.md").write_text("Intro body\n", encoding="utf-8")
    (src / "install.md").write_text("Install body\n", encoding="utf-8")
    (tmp_path / "src" / "ignore.txt").write_text("nope", encoding="utf-8")

    # Keys are relative to `src/` (so they match toc.yml hrefs); non-markdown is ignored.
    assert collect_docs(tmp_path, "src") == {
        "getting-started/intro.md": "Intro body\n",
        "getting-started/install.md": "Install body\n",
    }


def test_sparse_clone_builds_expected_git_commands():
    calls = []

    def runner(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stderr="")

    sparse_clone("https://example/repo", "master", "/tmp/dest", paths=("src",), runner=runner)

    assert calls[0] == [
        "git", "clone", "--filter=blob:none", "--no-checkout", "--depth", "1",
        "--branch", "master", "https://example/repo", "/tmp/dest",
    ]
    assert ["git", "-C", "/tmp/dest", "sparse-checkout", "set", "src"] in calls
    assert ["git", "-C", "/tmp/dest", "checkout"] in calls


def test_sparse_clone_raises_fetch_error_on_failure():
    def runner(cmd, **kwargs):
        return SimpleNamespace(returncode=128, stderr="fatal: repository not found")

    with pytest.raises(FetchError, match="repository not found"):
        sparse_clone("https://example/missing", "main", "/tmp/dest", runner=runner)


def test_fetch_source_returns_toc_and_docs(tmp_path):
    source = DocSource(name="odc", repo="https://example/docs-odc", branch="main")

    def runner(cmd, **kwargs):
        # Simulate the clone by materialising the expected files in dest.
        if cmd[1] == "clone":
            dest = Path(cmd[-1])
            (dest / "src" / "gs").mkdir(parents=True)
            (dest / "src" / "gs" / "intro.md").write_text("body\n", encoding="utf-8")
            (dest / "toc.yml").write_text("- href: gs/intro.md\n", encoding="utf-8")
        return SimpleNamespace(returncode=0, stderr="")

    result = fetch_source(source, tmp_path / "checkout", runner=runner)

    assert result.toc == "- href: gs/intro.md\n"
    assert result.docs == {"gs/intro.md": "body\n"}
