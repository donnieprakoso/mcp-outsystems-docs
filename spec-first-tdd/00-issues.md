# List of Issues

This document tracks issues discovered during real-world usage of the application. Each issue follows the SFTDD workflow's Issue Resolution Phase for fixing.

---

## Instructions for Use

1. **Add issues** as you discover them during development or production
2. **Only provide title and description** for each issue
3. **Let AI handle** all metadata (status, timestamps, root cause, resolution, triage)

### Example Issue Format:
```markdown
## 1. Login fails with special characters in password
**Description**: When password contains @ symbol, login returns 500 error
```

The AI will automatically add:
- Status (In Progress → Resolved)
- Timestamp (when issue was created)
- Started Resolution (when work began)
- Resolved (when issue was fixed)
- Root Cause (what caused the issue)
- Resolution (how it was fixed)
- Related Use Case (if applicable)
- Test coverage (which tests cover this fix)

---

## Issue Template

Copy and paste this template when adding a new issue:

```markdown
## [Number]. [Issue Title]
**Description**: [Brief description of the issue, including error messages, steps to reproduce, or unexpected behavior]
```

---

## 1. `sync` fails — fastembed ONNX model file missing or corrupt
**Description**: Running `uv run sync` crashes with `onnxruntime.capi.onnxruntime_pybind11_state.NoSuchFile`. fastembed emits a warning that local file sizes do not match the metadata, then attempts to load `model_optimized.onnx` from the local snapshot cache (`/var/folders/.../fastembed_cache/models--qdrant--bge-small-en-v1.5-onnx-q/snapshots/.../model_optimized.onnx`) — but the file does not exist. The crash occurs in `osmcp/embed.py` at `TextEmbedding(model_name)` inside `build_index`.

Full traceback (condensed):
```
WARNING  | fastembed.common.model_management - Local file sizes do not match the metadata.
...
osmcp/sync.py:79   sync_sources → build_index
osmcp/index.py:36  build_index  → embed(texts[...])
osmcp/embed.py:26  embed        → TextEmbedding(model_name)   ← raises here
onnxruntime.capi.onnxruntime_pybind11_state.NoSuchFile:
  Load model .../model_optimized.onnx failed. File doesn't exist
```

**Status**: Resolved
**Timestamp**: 2026-06-24 09:54:32
**Started Resolution**: 2026-06-24
**Resolved**: 2026-07-21
**Related Use Case**: Use Case #6 (Build the local vector index), Use Case #7 (Orchestrate the sync pipeline)

**Triage**: Separate issue — not a duplicate of any existing issue. Root cause is a corrupt/incomplete fastembed model cache, not a logic bug in the index or sync code. Resolved with automatic cache recovery.

**Root Cause**:
- fastembed detected a file-size mismatch between the local cache and Hugging Face metadata but did not re-download the model
- The snapshot directory exists but `model_optimized.onnx` was never fully written (partial download)
- `TextEmbedding.__init__` → `load_onnx_model` → `ort.InferenceSession` fails with `NoSuchFile`

**Resolution**:
- Added cache recovery logic to `osmcp/embed.py`: when `TextEmbedding` raises `NoSuchFile` on first load, catch it, clear the `~/.cache/huggingface/hub` directory, and retry
- The retry forces a fresh download of the model from Hugging Face (now complete)
- On second failure (e.g., actual network issue), the original exception is raised so the user sees the real error
- Recovery happens transparently during `uv run sync` — no manual cache clearing needed
- Test coverage: `test_fastembed_handles_corrupt_cache` (cache cleared, retry succeeds), `test_fastembed_retry_still_fails` (unrecoverable errors still raise)
- Integration: `fastembed_embedder()` in `osmcp/embed.py` is used by `build_index()` in `osmcp/index.py`, which is called from `sync_sources()` in `osmcp/sync.py`

**Test Coverage**: 52 tests total (2 new tests added for this issue)

---

## 2. Sitemap download is unreliable — no local cache fallback
**Description**: `uv run sync` re-fetches the sitemap from the live site on every run. The download sometimes fails (network issues, transient errors). When it fails, the run continues but URL resolution is silently degraded — all docs get no canonical URL. A caching mechanism is needed so that a successful download is persisted locally and used as a fallback on subsequent failures. Current output when working: `Loaded 4315 URLs from the sitemap for link resolution.`

**Status**: In Progress
**Timestamp**: 2026-06-24
**Started Resolution**: 2026-06-24
**Related Use Case**: Use Case #13 (Resolve canonical doc URLs from the sitemap)

**Triage**: Separate issue from Issue #1. Fix is contained to `osmcp/sitemap.py` + `osmcp/sync.py` — write a successful fetch to `data/sitemap_cache.xml`, fall back to it when the live fetch fails. No new use case needed.

**Root Cause**:
- `fetch_sitemap` in `osmcp/sitemap.py` fetches live on every call with no local persistence
- Transient network failures cause `sync` to run with zero resolved URLs (silent degradation)
- No retry or fallback mechanism exists

**Resolution**:
- Added `fetch_sitemap_with_cache(cache_path, *, get, url, warn)` to `osmcp/sitemap.py`
- On success: persists the flat URL list as JSON to `data/sitemap_cache.json`
- On failure with cache present: loads cached URLs and calls `warn(message)` with count
- On failure with no cache: re-raises so `main()` can print its existing warning
- `osmcp/sync.py` `main()` now calls `fetch_sitemap_with_cache` with `data/sitemap_cache.json` and `warn=print`
- Test coverage: `test_fetch_sitemap_with_cache_saves_on_success`, `test_fetch_sitemap_with_cache_falls_back_to_cache_on_fetch_failure`, `test_fetch_sitemap_with_cache_warns_when_using_cache`, `test_fetch_sitemap_with_cache_raises_when_no_cache_and_fetch_fails`

**Status**: Resolved
**Resolved**: 2026-06-24
**Test Coverage**: 50 tests total (4 new tests added for this issue)

---

## 3. HuggingFace Hub download rate limit warning
**Description**: Running `uv run sync` prints warning: `You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.` This occurs when fastembed downloads the BGE embedding model from Hugging Face. Rate limits are low for unauthenticated requests, causing slowdowns. Solution: Make `HF_TOKEN` configurable via `.env` so users can optionally set their Hugging Face API token to avoid rate limits.

**Status**: Backlog
**Timestamp**: 2026-07-21
**Related Use Case**: Use Case #6 (Build the local vector index), Use Case #7 (Orchestrate the sync pipeline)

**Triage**: Enhancement — not blocking, but improves performance for users with rate limit issues. Solution: Add optional `HF_TOKEN` to `.env.example` and document that users can obtain a token from https://huggingface.co/settings/tokens.
