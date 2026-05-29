# Project: OutSystems MCP Documentation Hub

## Project Context

**Description**: An MCP server that exposes OutSystems ODC and O11 documentation and best
practices to AI assistants. A **local** build (run manually or on a local schedule) syncs
the official docs, regenerates a standardized `llms.txt` index, and builds a fully local
semantic-search index — all written to a git-ignored local `data/` directory. A local MCP
server then serves those docs to assistants like Claude via resources and tools.

**Tech Stack**:
- **Language**: Python 3.11+
- **Framework**: FastMCP (official MCP Python SDK, `mcp[cli]`)
- **Testing**: pytest
- **Package Manager**: uv
- **Embeddings**: `fastembed` (ONNX runtime, model `BAAI/bge-small-en-v1.5`) — local & offline
- **Vector Search**: brute-force NumPy cosine similarity; index stored as `.npz`
- **Docs Sources** (multi-source config list of `{name, repo, branch, src_path}`):
  - `docs-odc` (ODC) — GitHub, `main` branch, sparse-checkout `src/` + `toc.yml`
  - `docs-product` (O11) — GitHub, `master` branch, sparse-checkout `src/` + `toc.yml`
- **Sync/Automation**: **local** — run via `uv run sync` (manually or a local `cron`/`launchd` schedule). No CI; nothing is committed back.
- **Storage**: synced docs + all derived artifacts written to a **git-ignored local `data/` dir**, namespaced per source — e.g. `data/odc/` and `data/o11/` (each with its own `llms.txt`, `llms-full.txt`), a top-level **combined** `data/llms.txt` (labeled ODC/O11 sections), and a shared `data/vectors.npz`.
- **Licensing**: both source repos are **CC BY-NC-ND 4.0**. Artifacts are produced for local NonCommercial use only and are **never committed/shared** (NoDerivatives). See Notes.
- **Transport**: stdio (local MCP server)

**Architecture**: Two phases — **Build** (local ingestion) and **Serve** (local MCP server).

```
╔════════════ BUILD — local sync (uv run sync; manual or cron/launchd) ═════════╗
║                                                                               ║
║  docs-odc (main) ─┐                       per source: {odc,o11}/llms.txt       ║
║  docs-product     ├▶ sparse-checkout ─▶ parse toc.yml ─┬▶ {odc,o11}/llms-full  ║
║   (master)        ┘   (src/ + toc.yml)                 └▶ combined llms.txt    ║
║                                  │                        (labeled ODC/O11)    ║
║                                  ▼                                             ║
║              chunk (+ source tag) ─▶ embed (fastembed/ONNX) ─▶ vectors.npz     ║
║                                                                               ║
║        ▼ write artifacts to a git-ignored local data/ dir (NOT committed) ▼   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
                                     │
   local data/ (git-ignored):  odc/ + o11/ (docs mirror, llms.txt, llms-full.txt)
                               • combined llms.txt • vectors.npz
                                     │
╔═════════════════════ SERVE — local MCP server (stdio) ═══════════════════════╗
║                                                                               ║
║  Claude ◀── stdio ──▶ FastMCP server                                          ║
║                         • load docs/ + llms.txt + vectors.npz at startup (RAM)║
║                         • resource: combined llms.txt (ODC/O11 sections)      ║
║                                      + per-source llms.txt                     ║
║                         • tool: get_doc(path)         (return a full document)║
║                         • tool: search_docs(query, k, source?) (embed query → ║
║                                              NumPy cosine, optional source     ║
║                                              filter → top-k)                  ║
║                                                                               ║
║   Fully local: no hosted inference, no hosted vector DB; offline after the    ║
║   one-time model download (or vendored ONNX model for full air-gap).          ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Repository Layout** (workflow ↔ code are kept separate):
```
Code_2026-05-29_OutSystemsMCP/      ← project root (run uv/pytest here)
├── pyproject.toml, uv.lock, .gitignore
├── osmcp/            (package code)
├── tests/            (pytest suite)
├── data/             (synced/derived artifacts — git-ignored)
└── spec-first-tdd/   ← SFTDD workflow + trackers only (its own git repo)
    ├── 00-sftdd-workflow.md   (generic methodology — kept pristine/reusable)
    ├── 00-use-case.md         (this file)
    └── 00-issues.md
```
> Generated code lives at the **project root**; SFTDD docs/trackers live in
> `spec-first-tdd/`. All paths in this tracker (e.g. `osmcp/toc.py`) are relative to the
> project root. The trackers I update are one level down in `spec-first-tdd/`.

**Development Environment**:
- **OS**: macOS
- **Runtime**: Python 3.11+
- **Package Manager**: uv
- **Test Command**: `uv run pytest` — run from the **project root** (`Code_2026-05-29_OutSystemsMCP/`), not from `spec-first-tdd/`. (`pythonpath` is set in `pyproject.toml`.)

---

## Use Cases

> Decomposed into atomic beads and grouped by phase. Each is processed one at a time via
> the SFTDD Red → Green → Enhancement → Refactor cycle.
> **Recommended starting bead: Use Case #1 (Parse `toc.yml`)** — a pure function, no I/O,
> the cleanest possible first Red test.

### 🏗️ Build Phase

### 1. Parse `toc.yml` into an ordered document tree
**Description**: Given the text of `toc.yml`, produce an ordered structure of sections and
document entries (title, href/path, nesting), preserving OutSystems' own navigation order.

> **Schema note**: In the real `toc.yml`, section titles are YAML *comments* (`# …`) and
> the only data keys are `href` + `topics` (an item's children are the next sibling
> `topics` block, recursively). This bead parses the `href`/nesting tree; deriving section
> titles from comments is deferred to the **Enhancement phase**.

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 4 tests (4 passing) — order/nesting, empty input, topics-hoisting, unknown-entry handling
**Last Updated**: 2026-05-29

**Implementation**: `osmcp/toc.py` (`parse_toc`); tests in `tests/test_toc.py`.
**Follow-up**: deriving **section titles from YAML comments** is a distinct feature (needs
raw-text parsing, not `yaml.safe_load`) — tracked as Use Case #1.1.

---

### 1.1. Parse section titles from `toc.yml` comments
**Description**: In `toc.yml`, each section's title is a YAML *comment* (`# …`) immediately
above the section's intro `- href:`. Since `yaml.safe_load` discards comments, parse them
from the raw text into a map of `{top-level intro href → section title}`, and let
`generate_llms_txt` use those real titles (falling back to folder-derived names when absent).

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 3 tests (3 passing) — title mapping, uncommented/nested-comment edges, llms.txt integration
**Last Updated**: 2026-05-29

**Implementation**: `osmcp/toc.py` (`parse_section_titles`); `osmcp/llms_txt.py` now accepts
`section_titles`. Suite total: **10 tests**.

---

### 2. Generate per-source + combined `llms.txt` index (Option C)
**Description**: Two tightly-coupled pure functions. (a) From one source's parsed tree,
generate that source's `llms.txt` (H1 title, blockquote summary, H2 sections of Markdown
links — per the llms.txt spec). (b) Combine the per-source indexes into a top-level
`llms.txt` with clearly-labeled platform sections (`## OutSystems Developer Cloud (ODC)`,
`## OutSystems 11 (O11)`) so platforms never get conflated.

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 3 tests (3 passing) — per-source structure, empty tree, combined platform labels
**Last Updated**: 2026-05-29

**Implementation**: `osmcp/llms_txt.py` (`generate_llms_txt`, `combine_llms_txt`); tests in `tests/test_llms_txt.py`.
**Note**: section names derived from `href` folders, link text from filenames (best-effort).
Will improve once the section-titles / frontmatter-titles feature lands. Suite total: **7 tests**.

---

### 3. Generate per-source `llms-full.txt`
**Description**: For each source, given its fetched documents in navigation order, generate
that source's `llms-full.txt` — full document contents concatenated with clear
per-document delimiters and source references (kept per-source to preserve the ODC/O11
boundary).

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 3 tests (3 passing) — ordered concatenation, section headers from titles, missing-doc tolerance
**Last Updated**: 2026-05-29

**Implementation**: `osmcp/llms_full.py` (`generate_llms_full_txt`); shared helpers extracted
to `osmcp/_render.py` (`header`, `document`, `iter_hrefs`). Suite total: **13 tests**.

---

### 4. Fetch docs from a configured source (multi-source)
**Description**: Given a source config (`repo`, `branch`, `src_path`), sparse-checkout
`src/` + `toc.yml` and return the collection of documents (relative path + content). Works
across sources with differing branches (`docs-odc`=`main`, `docs-product`=`master`). Handle
missing paths and network/clone failures gracefully. Output is written to the git-ignored
local `data/` dir.

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 4 tests (4 passing) — collect_docs, sparse_clone commands, clone-failure error, fetch_source orchestration
**Last Updated**: 2026-05-29

**Implementation**: `osmcp/fetch.py` (`DocSource`, `FetchResult`, `FetchError`, `collect_docs`,
`sparse_clone`, `fetch_source`). Git is shallow + blobless + cone sparse-checkout (`src/` +
root `toc.yml`), isolated behind an injectable `runner` (tests run offline). Suite total: **17 tests**.

---

### 5. Chunk Markdown into embeddable segments
**Description**: Split each document into heading-aware chunks (~300–500 tokens, slight
overlap), each carrying metadata: **`source`/`platform` (`odc` | `o11`)**, `source_path`,
`title`, `section`, `url`. The `source` tag is what keeps retrieval from mixing platforms.

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 4 tests (4 passing) — heading split + metadata, overlapping windows, no-heading fallback, empty doc
**Last Updated**: 2026-05-29

**Implementation**: `osmcp/chunk.py` (`Chunk`, `chunk_markdown`). Heading-aware sections,
long sections split into overlapping word-windows; every chunk carries `source` (odc|o11),
`source_path`, `section`, `title`, `url`. Suite total: **21 tests**.

---

### 6. Build the local vector index
**Description**: Embed all chunks with `fastembed` (pinned model) and write a local
`vectors.npz` index (vectors + chunk metadata) that can be round-tripped (saved/loaded).

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 3 tests (3 passing) — build/metadata, save↔load round-trip, empty index
**Last Updated**: 2026-05-29

**Implementation**: `osmcp/index.py` (`VectorIndex`, `build_index`, `save_index`, `load_index`).
Embedder is **injected** (`list[str] → np.ndarray`); tests use a deterministic fake — no model
download. `.npz` stores vectors + JSON metadata (`allow_pickle=False`).
**Deferred**: the real `fastembed` adapter (pinned `BAAI/bge-small-en-v1.5`) + the ~100MB model
download are wired in at the sync step (#7), not here. Suite total: **24 tests**.

---

### 7. Orchestrate the sync pipeline
**Description**: A single `uv run sync` entry point that, for every configured source,
composes fetch → parse → generate per-source `llms.txt`/`llms-full.txt` → chunk → embed,
then builds the **combined top-level `llms.txt`** across sources and writes all artifacts
to the git-ignored local `data/` dir, idempotently.

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 2 tests (2 passing) — single-source artifacts, multi-source combined + tagged index
**Last Updated**: 2026-05-29

**Implementation**: `osmcp/sync.py` (`sync_sources`, `SyncReport`, `_build_source_artifacts`,
`_git_fetch`, `main`) + `osmcp/embed.py` (`fastembed_embedder`, lazy). `fetch`/`embed` injected
(tests offline). Entry point `uv run sync` wired via `[project.scripts]` (project now packaged
with hatchling); `fastembed` added — model downloads only on a real `uv run sync`. Suite total: **26 tests**.

---

### 8. Local scheduled sync (no CI, no commit)
**Description**: Document how to run `uv run sync` on a local schedule (`cron`/`launchd`)
so artifacts in `data/` stay fresh. No GitHub Action and nothing committed — required by
the CC BY-NC-ND license. Ensure `data/` is `.gitignore`d. *(Infra/docs; verified by running
the command, not pytest.)*

**Status**: Completed
**Last Phase Completed**: N/A (docs/infra)
**Current Phase**: Done
**Test Coverage**: 0 tests (docs bead — verified by running `uv run sync`)
**Last Updated**: 2026-05-29

**Implementation**: project `README.md` documents setup, `uv run sync`, agent registration, and
the **local schedule** (cron one-liner + macOS `launchd`). No CI; `data/` is `.gitignore`d per
the CC BY-NC-ND license.

---

### 🌐 Serve Phase

### 9. Load artifacts at server startup
**Description**: On startup, load the per-source docs mirror, the combined + per-source
`llms.txt`, and `vectors.npz` into memory so subsequent requests need no disk/network access.

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 2 tests (2 passing) — load_store integration, parse_llms_full round-trip
**Last Updated**: 2026-05-29

**Implementation**: `osmcp/store.py` (`DocStore`, `load_store`) + `osmcp/llms_full.py`
(`parse_llms_full` recovers full docs from `llms-full.txt`, since we keep no separate mirror).
Suite total: **28 tests**.

---

### 10. Expose `llms.txt` as MCP resources
**Description**: Serve the **combined** `llms.txt` (labeled ODC/O11 sections) as the
primary MCP navigation resource, plus the per-source `llms.txt` files, so an assistant can
read the documentation structure and choose what to fetch (Tier-0 navigation).

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 1 test (1 passing) — `navigation()` combined / per-source / unknown-source error
**Last Updated**: 2026-05-29

**Implementation**: `DocStore.navigation()` in `osmcp/store.py`; exposed as the MCP resource
`llms://index` in `osmcp/server.py` (FastMCP).

---

### 11. `get_doc(path)` tool
**Description**: Given a document path, return that document's full Markdown content (or a
clear not-found error).

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 1 test (1 passing) — found / not-found / unknown-source
**Last Updated**: 2026-05-29

**Implementation**: `DocStore.get_doc(source, path)` in `osmcp/store.py`; exposed as the
`get_doc` MCP tool in `osmcp/server.py`.

---

### 12. `search_docs(query, k, source?)` semantic tool
**Description**: Embed the query locally with the same pinned `fastembed` model, run
NumPy cosine similarity against `vectors.npz`, and return the top-k chunks with source
metadata. Accepts an optional `source` filter (`odc` | `o11`) so results can be scoped to
one platform. Fully local, no hosted services.

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 3 tests (3 passing) — cosine top-k ranking, source filter, empty index
**Last Updated**: 2026-05-29

**Implementation**: `DocStore.search(query_vector, k, source)` (NumPy cosine) in
`osmcp/store.py`; exposed as the `search_docs` MCP tool in `osmcp/server.py`, which embeds
the query locally via `fastembed_embedder()` (lazy). Server entry point: `osmcp-serve`.
Suite total: **34 tests** + `osmcp/server.py` wiring test.

---

### 13. Resolve canonical doc URLs from the sitemap
**Description**: Repo paths don't map mechanically to the public docs site (leaf slug comes
from the page *title*, folders are renamed, hierarchy is restructured). Resolve each doc to a
**verified** canonical URL by matching its title-slug against the site's `sitemap.xml`
(authoritative, static XML — no JS), scoped by platform and disambiguated by path tokens.
Return nothing when unsure, so a link is either real or absent (never a 404).

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 8 tests (8 passing) — slug match, platform scoping, token disambiguation,
no-match→None, sitemap parse, index-follow fetch, H1 title, sync URL wiring
**Last Updated**: 2026-05-29

**Implementation**: `osmcp/sitemap.py` (`resolve_url`, `parse_sitemap_urls`, `fetch_sitemap`
[injected HTTP], `doc_title`). Wired into `osmcp/sync.py` via `sitemap_urls`; `main` fetches
the sitemap (graceful fallback, `--no-links` to skip). **Verified-or-omit** guarantees no
broken links. Suite total: **42 tests**.

---

### 14. Sync progress output
**Description**: `uv run sync` should report human-readable progress (per-source stages and
per-batch embedding) instead of a single line, so long runs show a sense of progress.

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 2 tests (2 passing) — `build_index` per-batch progress, `sync_sources` stage messages
**Last Updated**: 2026-05-29

**Implementation**: `progress` callback on `sync_sources` (per-source stages) and on
`build_index` (now batched, reports `(done, total)`); `main` passes `print`. Suite total: **44 tests**.

---

### 15. Surface "last updated" timestamp via MCP
**Description**: Record when the docs were last synced and expose it through the MCP so every
MCP-backed answer can show how fresh the served docs are.

**Status**: Completed
**Last Phase Completed**: Refactor
**Current Phase**: Refactor (completed)
**Test Coverage**: 3 tests (3 passing) — sync writes timestamp, store loads it, server returns it + `last_updated` tool
**Last Updated**: 2026-05-29

**Implementation**: `sync_sources` writes `data/synced_at.txt` (`now` injectable) and sets
`SyncReport.synced_at`; `DocStore.synced_at` loaded by `load_store`; `search_docs` returns
`{"synced_at", "results"}` and a new `last_updated` MCP tool. Claude appends the timestamp to
MCP-backed answers (saved as a preference). Suite total: **46 tests**.

---

## Notes
- **Licensing (CC BY-NC-ND 4.0)**: both `docs-odc` and `docs-product` use this license.
  NoDerivatives allows *producing* adapted material (index, concatenated text, embeddings)
  for NonCommercial use but forbids *Sharing* it — so the build runs locally and `data/`
  (synced docs + all derived artifacts) is `.gitignore`d and never committed/pushed.
- `llms.txt` is a **generated artifact**, produced during the Build phase (Use Case #2) and
  written to local `data/`; the Serve phase only reads it. Its generation logic is identical
  whether the build runs locally or in CI — moving to a local build did not change it.
- The semantic retriever is **retrieval-only** — the server returns chunks; Claude (the MCP
  client) does the reasoning/generation. No LLM runs inside the server.
- **Platform separation (Option C)**: ODC and O11 are distinct platforms. Navigation keeps
  them apart via a combined `llms.txt` with labeled sections + per-source files; retrieval
  keeps them apart via a `source`/`platform` tag on every chunk and an optional `source`
  filter on `search_docs`. This prevents the tool from giving O11 answers to ODC questions.
- Build-phase pure functions (#1, #2, #3, #5) and ranking logic (#12) are TDD'd with
  deterministic inputs; the real embedding model appears only in a couple of integration
  tests via an injectable embedder.
