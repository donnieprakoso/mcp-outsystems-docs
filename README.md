# OutSystems Documentation MCP (unofficial)

A local [MCP](https://modelcontextprotocol.io) server that gives your AI agent **semantic search over the OutSystems ODC & O11 documentation** — with verified source links and a freshness timestamp. Runs **fully local** (offline embeddings, no hosted services).

> Unofficial / community project. Docs are © OutSystems (CC BY-NC-ND 4.0); this tool keeps everything local and never redistributes them.

## Get started

Prerequisites: [`uv`](https://docs.astral.sh/uv/) and Python 3.11+.

```bash
git clone <your-repo-url> outsystems-documentation-mcp
cd outsystems-documentation-mcp
uv sync
```

## Sync the docs

```bash
uv run sync                 # ODC + O11 (default)
uv run sync --source odc    # one platform
```

This pulls the latest docs and builds a local `data/` index (the first run downloads a ~100 MB embedding model, then it's offline). Re-run anytime to refresh.

## Add it to your agent

**Option A — manual.** Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "outsystems-docs": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/outsystems-documentation-mcp", "osmcp-serve"]
    }
  }
}
```

Claude Code:

```bash
claude mcp add outsystems-docs -- uv run --directory /path/to/outsystems-documentation-mcp osmcp-serve
```

**Option B — let an agent install it.** Paste this prompt into your coding agent:

```
Clone <your-repo-url>, run `uv sync` then `uv run sync`, and register the
`osmcp-serve` command as a stdio MCP server named "outsystems-docs"
(uv run --directory <repo path> osmcp-serve). Then call search_docs to confirm it works.
```

## What you get

__Pending screenshots__

![Semantic search over the docs](screenshots/search.png)
![Verified source links in answers](screenshots/links.png)
![Freshness timestamp on every answer](screenshots/timestamp.png)

| Capability | What it does |
|---|---|
| `search_docs(query, k, source?)` | Semantic search; optional `odc`/`o11` filter |
| `get_doc(source, path)` | Full Markdown of a single doc |
| `llms://index` (resource) | Combined, labeled ODC + O11 navigation |
| `last_updated` | When your local docs were last synced |
| Verified links | URLs resolved against the official sitemap (never broken) |
| Fully local | Offline embeddings + NumPy search; nothing leaves your machine |

## FAQ

**How does it work?** `uv run sync` fetches the official docs, generates `llms.txt`/`llms-full.txt`, and builds a local vector index. The server loads those and answers `search_docs` by embedding your query locally and ranking by cosine similarity.

**Is it accurate?** Answers come from the official OutSystems docs and link back to verified URLs. Results are only as fresh as your last `uv run sync` — check the timestamp shown with each answer.

**How do I sync?** `uv run sync` (add `--source odc` or `--source o11` to limit; `--no-links` to skip URL resolution).

**How do I make it sync automatically?** Schedule it locally — no CI (license: don't redistribute). Example cron (daily 7am):

```cron
0 7 * * * cd /path/to/outsystems-documentation-mcp && uv run sync >> sync.log 2>&1
```

On macOS you can use a `launchd` LaunchAgent with `StartCalendarInterval` instead.

## Built with Spec-First TDD

This project was built one atomic use case at a time using **Spec-First TDD** — [github.com/donnieprakoso/spec-first-tdd](https://github.com/donnieprakoso/spec-first-tdd).

---

Feel free to open an issue or share feedback. 🙌
