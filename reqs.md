# Requirements — OutSystems Documentation MCP

## Overview
A local MCP (Model Context Protocol) server that gives AI coding agents semantic search over the official OutSystems ODC and O11 documentation. Runs fully offline (local embeddings, no hosted services) and never redistributes OutSystems' CC BY-NC-ND docs — only serves them locally to the user's own agent.

## Problem
Coding agents need accurate, up-to-date OutSystems documentation to answer questions and generate correct code, but general web search/training data is unreliable, unverified, and can go stale.

## Functional Requirements

### 1. Sync pipeline (`uv run sync`)
- Fetch docs from the official `docs-odc` and `docs-product` (O11) GitHub repos (shallow sparse clone).
- Parse each source's table of contents and Markdown docs.
- Resolve canonical, verified URLs for each doc via the official sitemap (skippable with `--no-links`).
- Chunk Markdown content for embedding.
- Generate `llms.txt` / `llms-full.txt` per source, plus a combined index.
- Embed all chunks locally (fastembed) and persist a NumPy vector index (`vectors.npz`).
- Record a `synced_at` UTC timestamp for freshness tracking.
- Support syncing all sources or a single one (`--source odc` / `--source o11`).

### 2. MCP server (`osmcp-serve`, stdio)
- `search_docs(query, k=5, source?)` — embed the query locally, return top-`k` semantically similar chunks, scoped to `odc`/`o11` if specified. Response includes `synced_at` so callers can show freshness.
- `get_doc(source, path)` — return the full Markdown of one document.
- `last_updated()` — return the ISO timestamp of the last sync.
- `llms://index` (resource) — combined ODC + O11 navigation index.
- Store and embedder load lazily on first use (no model download at import/startup).

## Non-Functional Requirements
- **Fully local**: no network calls at query time; embeddings and vector search run offline.
- **License-compliant**: docs are fetched and cached locally only, never redistributed (CC BY-NC-ND); no CI/hosted sync — scheduling is left to the user (cron/launchd).
- **Freshness-transparent**: every answer surfaces the last sync timestamp.
- **Verified links**: doc URLs are resolved against the official sitemap so links never break.
- **Testable pipeline**: fetch/embed are injected dependencies so sync logic is testable without network or model access.

## Out of Scope
- Hosted/remote MCP server or multi-user deployment.
- Automatic/CI-based scheduled syncing.
- Redistribution of OutSystems documentation content.

## Tech Stack
Python 3.11+, `uv`, `fastembed`, `numpy`, `mcp[cli]`, `pyyaml`. Built incrementally using Spec-First TDD.
