"""Tests for Use Case #13: resolve canonical doc URLs from the sitemap."""

import json

import pytest

from osmcp.sitemap import doc_title, fetch_sitemap, fetch_sitemap_with_cache, parse_sitemap_urls, resolve_url

ODC = "https://success.outsystems.com/documentation/outsystems_developer_cloud"
O11 = "https://success.outsystems.com/documentation/11"

URLS = [
    f"{ODC}/getting_started/build_a_basic_web_app/",
    f"{ODC}/building_apps/user_interface/screens/best_practices_for_building_screens/",
    f"{O11}/building_apps/user_interface/screens/best_practices_for_building_screens/",
]


def test_resolve_url_single_match_by_title_slug():
    assert (
        resolve_url("Build a basic Web app", "eap/getting-started/sample-app.md", "odc", URLS)
        == f"{ODC}/getting_started/build_a_basic_web_app/"
    )


def test_resolve_url_scopes_by_platform():
    # The same title-slug exists for ODC and O11; the source picks the right platform.
    path = "eap/building-apps/ui/creating-screens/best-practices-screens.md"
    assert resolve_url("Best practices for building screens", path, "odc", URLS).startswith(ODC)
    assert resolve_url("Best practices for building screens", path, "o11", URLS).startswith(O11)


def test_resolve_url_returns_none_when_no_match():
    assert resolve_url("A Page That Does Not Exist", "x.md", "odc", URLS) is None


def test_resolve_url_disambiguates_within_platform_by_path_tokens():
    urls = [
        f"{ODC}/building_apps/data/sharing_data/",
        f"{ODC}/integration_with_systems/sharing_data/",
    ]
    assert (
        resolve_url("Sharing data", "eap/building-apps/data/sharing.md", "odc", urls)
        == f"{ODC}/building_apps/data/sharing_data/"
    )


def test_parse_sitemap_urls_extracts_and_dedupes_locs():
    xml = (
        "<urlset><url><loc>https://x/a/</loc></url>"
        "<url><loc>https://x/b/</loc></url>"
        "<url><loc>https://x/a/</loc></url></urlset>"
    )
    assert parse_sitemap_urls(xml) == ["https://x/a/", "https://x/b/"]


def test_fetch_sitemap_follows_index_into_sub_sitemaps():
    index = "<sitemapindex><sitemap><loc>https://x/sub.xml</loc></sitemap></sitemapindex>"
    sub = "<urlset><url><loc>https://x/page1/</loc></url></urlset>"
    pages = {"https://x/index.xml": index, "https://x/sub.xml": sub}
    assert fetch_sitemap(get=lambda u: pages[u], url="https://x/index.xml") == ["https://x/page1/"]


def test_doc_title_reads_first_h1():
    assert doc_title("# Build a basic Web app\n\nbody") == "Build a basic Web app"
    assert doc_title("no heading here") is None


# --- Issue #2: sitemap cache ---

_XML = "<urlset><url><loc>https://x/a/</loc></url></urlset>"


def test_fetch_sitemap_with_cache_saves_on_success(tmp_path):
    cache = tmp_path / "sitemap_cache.json"
    urls = fetch_sitemap_with_cache(cache, get=lambda u: _XML)
    assert urls == ["https://x/a/"]
    assert json.loads(cache.read_text(encoding="utf-8")) == ["https://x/a/"]


def test_fetch_sitemap_with_cache_falls_back_to_cache_on_fetch_failure(tmp_path):
    cache = tmp_path / "sitemap_cache.json"
    cache.write_text(json.dumps(["https://x/cached/"]), encoding="utf-8")

    def failing_get(u):
        raise ConnectionError("network down")

    urls = fetch_sitemap_with_cache(cache, get=failing_get)
    assert urls == ["https://x/cached/"]


def test_fetch_sitemap_with_cache_warns_when_using_cache(tmp_path):
    cache = tmp_path / "sitemap_cache.json"
    cache.write_text(json.dumps(["https://x/cached/"]), encoding="utf-8")

    def failing_get(u):
        raise ConnectionError("down")

    warnings = []
    fetch_sitemap_with_cache(cache, get=failing_get, warn=warnings.append)
    assert warnings and any("cache" in w.lower() for w in warnings)


def test_fetch_sitemap_with_cache_raises_when_no_cache_and_fetch_fails(tmp_path):
    cache = tmp_path / "sitemap_cache.json"

    def failing_get(u):
        raise ConnectionError("down")

    with pytest.raises(ConnectionError):
        fetch_sitemap_with_cache(cache, get=failing_get)
