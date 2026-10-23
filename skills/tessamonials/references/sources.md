# Official source notes

Reviewed October 22, 2026 (UTC). The numbered sources below are official product
and OpenClaw documentation, not inferred from community recipes. Runtime input
schemas may change: inspect them when connected instead of treating this guide as
a frozen tool schema.

## What was established

- [1] Remote URL/transport, PKCE + dynamic client registration, HTTPS callbacks,
  scopes/roles, 21 server-side tool names and effects, company IDs, paused campaign
  creation, revision checks, separate prepare/send and approve/publish operations,
  cursor limits, retained-result reads, and invitation-link secrecy.
- [2] Saved testimonial revisions approved by default, persistent participant
  unapproval, anonymity, withdrawal, and separate external-copy deletion processes.
- [3] Native OpenClaw Settings → MCP setup and shared OAuth browser Sign in on the
  Gateway's own HTTPS address; saved credentials alone do not prove tool health.
- [4] Streamable HTTP configuration; runtime-owned OAuth; shared/per-requester
  identity boundaries; normal CLI loopback callback; reconnect without replaying a
  failed tool call. The HTTPS browser path is the documented integration candidate,
  not an exercised Tessamonials/OpenClaw login result.
- [5] Current `openclaw mcp` registry syntax, tool filters, config-only vs live
  checks, and the requirement to stop the local Gateway for CLI mutations/login/
  probes. Config reload is not a cross-process restart guarantee.
- [6] Supported skill frontmatter, matching portable directory/name, supporting
  regular files, runtime metadata, and MIT-0 skill license.
- [7] Skill publish dry-run, category/topic rules, pending security review, and the
  distinction between skill listing material and bundled plugin artwork.
- [8][9] Homepage-declared official favicon, verified by a public GET and SVG parse.

## Public-only validation boundary

The surrounding release-review directory (not part of the installable skill)
retains HTTP statuses, selected headers, hashes, retrieved public source bodies,
local tests, and exact CLI dry-run output. Public OAuth metadata and the expected
unauthenticated 401 establish discovery/auth boundaries only. They do **not** prove
that sign-in, dynamic client registration, tool schemas, live company access, or
private transcript pagination works. No account creation, sign-in, private reads,
launch, invitation preparation/send, approval, publication, or paid operation was
performed. No publish or login command should be run as part of installing this
skill.

The actual CLI preview result and limitations are in the release review's
`VALIDATION.md`. Skill metadata has no invented auth/config installer fields;
conceptual sign-in prerequisites are documented in prose instead.

## Sources

[1] https://tessamonials.com/docs/mcp — product-mcp
[2] https://tessamonials.com/consent — product-consent
[3] https://docs.openclaw.ai/tools/mcp — openclaw-mcp-connect
[4] https://docs.openclaw.ai/cli/mcp/transports — openclaw-mcp-transports
[5] https://docs.openclaw.ai/cli/mcp/registry — openclaw-mcp-registry
[6] https://docs.openclaw.ai/clawhub/skill-format — openclaw-skill-format
[7] https://docs.openclaw.ai/clawhub/publishing — openclaw-publishing
[8] https://tessamonials.com — product-home
[9] https://tessamonials.com/images/favicon.svg?v=2 — product-icon
