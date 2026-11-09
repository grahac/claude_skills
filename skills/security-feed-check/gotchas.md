# Gotchas

- **pwn.watch returns 403 to the default Python User-Agent.** `check.py` sends its own. Keep it if you edit the script.
- **The Zero Wire web page blocks scripts** (Cloudflare bot challenge, 403). The RSS feed at `/security/zero-wire/rss` does not. Use the feed.
- **Zero Wire guids look like `slug@2026-11-05`.** The date changes when Cloudflare updates an item, which is how updates are detected. Its "last reviewed" date can be later than the guid date.
- **Codex sandboxes often block network access.** Run with network enabled (for example `codex exec --sandbox workspace-write -c sandbox_workspace_write.network_access=true`), or the feed fetch fails.
- **The first run marks everything as new.** That is expected; `--commit` after the report establishes the baseline.
- **Repo default branch is not what is deployed.** Release-history timestamps can also be stale relative to the running image. Check the running machine before recommending a redeploy.
- **Keyword matching is whole-word.** `node` does not match `nodejs`. Tune the watchlist, not the script, when results are noisy or missing.
