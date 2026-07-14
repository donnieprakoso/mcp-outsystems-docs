"""Resolve repo doc paths to verified canonical URLs using the site's sitemap.

Safety rule: only ever return a URL that appears in the sitemap; when a confident match
can't be made, return ``None`` (the caller omits the link rather than risk a wrong one).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

SITEMAP_INDEX = "https://success.outsystems.com/sitemap.xml"

# Each platform's docs live under a distinct URL segment.
_PLATFORM_MARKER = {"odc": "/outsystems_developer_cloud/", "o11": "/documentation/11/"}
# Tokens that carry no disambiguating signal.
_STOP_TOKENS = {"eap", "md", "intro", "documentation", "outsystems", "developer", "cloud", "11"}


def resolve_url(title, repo_path, source, urls):
    """Return the canonical URL for a doc, or ``None`` if no confident match.

    Matches the page title's slug against each sitemap URL's final segment, scoped to the
    doc's platform. When several candidates remain, the one whose path shares the most
    tokens with ``repo_path`` wins; ties (or no candidates) yield ``None``.
    """
    marker = _PLATFORM_MARKER.get(source)
    slug = _slug(title)
    candidates = [u for u in urls if marker and marker in u and _leaf(u) == slug]
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    wanted = _tokens(repo_path)
    ranked = sorted(candidates, key=lambda u: len(wanted & _tokens(u)), reverse=True)
    top = len(wanted & _tokens(ranked[0]))
    if top == 0 or len(wanted & _tokens(ranked[1])) == top:
        return None  # ambiguous — omit rather than risk the wrong page
    return ranked[0]


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def _leaf(url):
    return url.rstrip("/").rsplit("/", 1)[-1]


def _tokens(text):
    return {t for t in re.split(r"[^a-z0-9]+", text.lower()) if t and t not in _STOP_TOKENS}


def parse_sitemap_urls(xml):
    """Extract the ``<loc>`` URLs from a sitemap or sitemap-index document, de-duplicated."""
    seen = {}
    for loc in re.findall(r"<loc>\s*(.*?)\s*</loc>", xml, re.S):
        seen.setdefault(loc, None)
    return list(seen)


def fetch_sitemap(get=None, url=SITEMAP_INDEX):
    """Return all page URLs, following a sitemap index into its sub-sitemaps.

    ``get`` is an injected ``url -> xml`` callable (defaults to a plain HTTP GET).
    """
    get = get or _http_get
    xml = get(url)
    locs = parse_sitemap_urls(xml)
    if "<sitemapindex" in xml:
        pages = {}
        for sub in locs:
            for page in fetch_sitemap(get, sub):
                pages.setdefault(page, None)
        return list(pages)
    return locs


def fetch_sitemap_with_cache(cache_path, *, get=None, url=SITEMAP_INDEX, warn=None):
    """Fetch sitemap URLs, persisting a local cache and falling back to it on failure.

    On success the URL list is written to ``cache_path`` as JSON. On failure the cache
    is loaded if it exists (with an optional ``warn(message)`` callback); otherwise the
    original exception is re-raised.
    """
    cache_path = Path(cache_path)
    try:
        urls = fetch_sitemap(get=get, url=url)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(urls), encoding="utf-8")
        return urls
    except Exception as exc:
        if cache_path.exists():
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            if warn:
                warn(f"sitemap fetch failed ({exc}); using cached copy ({len(cached)} URLs).")
            return cached
        raise


def doc_title(content):
    """Return a document's first H1 heading text, or ``None`` if it has none."""
    match = re.search(r"(?m)^#\s+(.+?)\s*$", content)
    return match.group(1) if match else None


def _http_get(url):  # pragma: no cover - thin network wrapper
    import urllib.request

    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")
