"""Fetch OutSystems docs for one source via a sparse git checkout.

Network/git access is isolated in :func:`sparse_clone` behind an injectable ``runner`` so
the logic can be tested offline. :func:`fetch_source` orchestrates clone → read ``toc.yml``
→ collect markdown into ``{href: content}``.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


class FetchError(RuntimeError):
    """A source could not be fetched (clone failure, missing ``toc.yml``, …)."""


@dataclass(frozen=True)
class DocSource:
    """Configuration for one documentation source."""

    name: str  # e.g. "odc"
    repo: str  # e.g. "https://github.com/OutSystems/docs-odc"
    branch: str = "main"
    src_path: str = "src"
    label: str = ""  # display title for the index (defaults to name)
    summary: str = ""  # one-line summary shown under the index title
    url_base: str = ""  # prefix for doc urls; url = f"{url_base}{href}"


@dataclass(frozen=True)
class FetchResult:
    """The result of fetching a source: raw ``toc.yml`` text + the markdown collection."""

    toc: str
    docs: dict[str, str]


def collect_docs(root, src_path="src") -> dict[str, str]:
    """Read all ``.md`` files under ``root/src_path`` into ``{href: content}``.

    Keys are paths relative to ``src_path`` (matching ``toc.yml`` hrefs).
    """
    base = Path(root) / src_path
    docs = {}
    for path in sorted(base.rglob("*.md")):
        docs[path.relative_to(base).as_posix()] = path.read_text(encoding="utf-8")
    return docs


def sparse_clone(repo, branch, dest, *, paths=("src",), runner=subprocess.run) -> None:
    """Shallow, blobless, sparse checkout of ``paths`` from ``repo``@``branch`` into ``dest``.

    Cone-mode sparse checkout also brings root-level files (e.g. ``toc.yml``) along.
    """
    dest = str(dest)
    commands = [
        ["git", "clone", "--filter=blob:none", "--no-checkout", "--depth", "1",
         "--branch", branch, repo, dest],
        ["git", "-C", dest, "sparse-checkout", "set", *paths],
        ["git", "-C", dest, "checkout"],
    ]
    for cmd in commands:
        result = runner(cmd, capture_output=True, text=True)
        if getattr(result, "returncode", 0) != 0:
            stderr = getattr(result, "stderr", "") or ""
            raise FetchError(f"git command failed: {' '.join(cmd)}\n{stderr}".rstrip())


def fetch_source(source: DocSource, dest, *, runner=subprocess.run) -> FetchResult:
    """Clone ``source`` into ``dest`` and return its ``toc.yml`` + markdown documents."""
    sparse_clone(source.repo, source.branch, dest, paths=(source.src_path,), runner=runner)
    toc_path = Path(dest) / "toc.yml"
    if not toc_path.exists():
        raise FetchError(f"toc.yml not found after checkout of {source.repo}")
    return FetchResult(
        toc=toc_path.read_text(encoding="utf-8"),
        docs=collect_docs(dest, source.src_path),
    )
