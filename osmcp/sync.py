"""Orchestrate the build pipeline: fetch → parse → generate → chunk → embed → write."""

from __future__ import annotations

import argparse
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from osmcp._render import humanize
from osmcp.chunk import chunk_markdown
from osmcp.fetch import DocSource, fetch_source
from osmcp.index import build_index, save_index
from osmcp.llms_full import generate_llms_full_txt
from osmcp.llms_txt import combine_llms_txt, generate_llms_txt
from osmcp.sitemap import doc_title, fetch_sitemap_with_cache, resolve_url
from osmcp.toc import parse_section_titles, parse_toc

COMBINED_TITLE = "OutSystems Documentation"
COMBINED_SUMMARY = "Combined index of OutSystems ODC and O11 documentation."

DEFAULT_SOURCES = [
    DocSource(
        name="odc",
        repo="https://github.com/OutSystems/docs-odc",
        branch="main",
        label="OutSystems Developer Cloud (ODC)",
        summary="OutSystems Developer Cloud (ODC) documentation.",
    ),
    DocSource(
        name="o11",
        repo="https://github.com/OutSystems/docs-product",
        branch="master",
        label="OutSystems 11 (O11)",
        summary="OutSystems 11 (O11) documentation.",
    ),
]


@dataclass
class SyncReport:
    """Summary of a sync run."""

    num_sources: int
    num_chunks: int
    synced_at: str = ""


def sync_sources(
    sources, data_dir, *, fetch, embed, sitemap_urls=None, progress=None, now=None
) -> SyncReport:
    """Run the full pipeline for each source, writing all artifacts under ``data_dir``.

    ``fetch`` (``DocSource -> FetchResult``) and ``embed`` (``list[str] -> np.ndarray``) are
    injected so the orchestration is testable offline. When ``sitemap_urls`` is provided,
    each chunk's ``url`` is the verified canonical URL (or empty when unresolved).
    ``progress`` is an optional ``(message) -> None`` callback for human-readable status.
    """
    say = progress or (lambda _message: None)
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    combined_inputs = []
    all_chunks = []
    for i, source in enumerate(sources, 1):
        say(f"[{i}/{len(sources)}] {source.name}: fetching…")
        result = fetch(source)
        combined_input, chunks = _build_source_artifacts(source, result, data_dir, sitemap_urls)
        say(f"[{i}/{len(sources)}] {source.name}: {len(result.docs)} docs → {len(chunks)} chunks")
        combined_inputs.append(combined_input)
        all_chunks.extend(chunks)

    (data_dir / "llms.txt").write_text(
        combine_llms_txt(combined_inputs, title=COMBINED_TITLE, summary=COMBINED_SUMMARY),
        encoding="utf-8",
    )
    say(f"embedding {len(all_chunks)} chunks…")
    index = build_index(
        all_chunks, embed, progress=lambda done, total: say(f"  embedded {done}/{total} chunks")
    )
    save_index(index, data_dir / "vectors.npz")

    timestamp = (now or (lambda: datetime.now(timezone.utc)))().isoformat()
    (data_dir / "synced_at.txt").write_text(timestamp, encoding="utf-8")
    say(f"done (synced_at {timestamp})")

    return SyncReport(num_sources=len(sources), num_chunks=len(all_chunks), synced_at=timestamp)


def _build_source_artifacts(source, result, data_dir, sitemap_urls=None):
    """Write one source's ``llms.txt``/``llms-full.txt`` and return its combined-index input
    plus the chunks to embed."""
    tree = parse_toc(result.toc)
    titles = parse_section_titles(result.toc)
    label = source.label or source.name

    src_dir = data_dir / source.name
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / "llms.txt").write_text(
        generate_llms_txt(tree, title=label, summary=source.summary, section_titles=titles),
        encoding="utf-8",
    )
    (src_dir / "llms-full.txt").write_text(
        generate_llms_full_txt(
            tree, result.docs, title=label, summary=source.summary, section_titles=titles
        ),
        encoding="utf-8",
    )

    chunks = []
    for href, content in result.docs.items():
        chunks.extend(
            chunk_markdown(
                content,
                source=source.name,
                source_path=href,
                title=humanize(href),
                url=_doc_url(source, href, content, sitemap_urls),
            )
        )
    return {"label": label, "tree": tree, "titles": titles}, chunks


def _doc_url(source, href, content, sitemap_urls):
    """Verified canonical URL for a doc (empty if unresolved); falls back to href when no
    sitemap is supplied."""
    if sitemap_urls is None:
        return f"{source.url_base}{href}" if source.url_base else href
    title = doc_title(content) or humanize(href)
    return resolve_url(title, href, source.name, sitemap_urls) or ""


def _git_fetch(source):
    """Real fetch: shallow sparse-clone into a temp dir; content is read into memory."""
    with tempfile.TemporaryDirectory() as tmp:
        return fetch_source(source, tmp)


def main(argv=None) -> SyncReport:
    """CLI entry point (``uv run sync``): sync configured sources into ``data/``."""
    parser = argparse.ArgumentParser(
        prog="sync", description="Sync OutSystems docs into the local data/ directory."
    )
    parser.add_argument("--data-dir", default="data", help="output directory (default: data)")
    parser.add_argument(
        "--source", action="append", choices=[s.name for s in DEFAULT_SOURCES],
        help="limit to specific source(s); repeatable (default: all)",
    )
    parser.add_argument(
        "--no-links", action="store_true",
        help="skip fetching the sitemap (chunks get no canonical URLs)",
    )
    args = parser.parse_args(argv)

    from osmcp.embed import fastembed_embedder  # lazy: avoids importing fastembed for --help

    selected = set(args.source) if args.source else None
    sources = [s for s in DEFAULT_SOURCES if selected is None or s.name in selected]

    sitemap_urls = None
    if not args.no_links:
        cache_path = Path(args.data_dir) / "sitemap_cache.json"
        try:
            sitemap_urls = fetch_sitemap_with_cache(cache_path, warn=print)
            print(f"Loaded {len(sitemap_urls)} URLs from the sitemap for link resolution.")
        except Exception as exc:  # noqa: BLE001 - links are optional; never fail the sync
            print(f"Warning: could not fetch sitemap ({exc}); proceeding without links.")

    report = sync_sources(
        sources, args.data_dir, fetch=_git_fetch, embed=fastembed_embedder(),
        sitemap_urls=sitemap_urls, progress=print,
    )
    print(f"Synced {report.num_sources} source(s), {report.num_chunks} chunks → {args.data_dir}")
    return report


if __name__ == "__main__":
    main()
