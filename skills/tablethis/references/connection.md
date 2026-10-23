# Connection and permissions reference

Checked against public official docs on 2026-10-22. Do not run connection/auth
steps as part of package validation. This reference does not contain credentials.

## Native OpenClaw connection

Current route: `mcp.servers` → remote `streamable-http` → `auth: "oauth"`.
Use Settings → MCP for live configuration/sign-in, including the scoped editor
for OAuth scope. The SKILL.md CLI alternative is operator-only and requires
stopping the local Gateway for mutations, login, and live probes. Read-only
`openclaw mcp status --verbose` and `openclaw mcp doctor tablethis` need no probe.
Inspect an existing entry before replacing it. `openclaw mcp set` replaces an entry;
`configure` updates specific fields. Commands address the installation that owns
the chosen state directory; restarting an unrelated CLI will not refresh a remote
Gateway. [2][3]

`openclaw mcp serve` exposes OpenClaw conversations to other clients: it is not
the route to TableThis. OpenClaw's native registry is distinct from mcporter's
`config/mcporter.json`; installing this skill does not configure either one. [2]

Do not set `--approval approve` or persistent "Allow Always" grants as a setup
shortcut. Approval may apply to a tool even when its arguments change. Runtime
approval is separate from TableThis OAuth scopes, roles, and product changeset
review. The skill's confirmation gates still apply when a runtime would not
prompt. [2]

For a client other than OpenClaw, use its supported native remote HTTP MCP/OAuth
route to the same endpoint, then discover schemas. No generic API key or bespoke
OAuth helper is required. [1]

## Least-privilege scope matrix

| Intent | Needed scope | Skill rule |
| --- | --- | --- |
| Read typed tables, records, history, pending changes | `tables:read` | Default, narrow queries |
| Read/search Markdown documents and passages | `documents:read` | Add only for document tasks |
| Suggest record changes | `records:write_proposals` | Approved bounded submission only |
| Suggest tables/fields changes | `schema:write` | Approved schema proposal only |
| Approve/reject changes | `changes:review` | Separate interactive owner task |
| Apply already-approved changes | `changes:apply` | Separate interactive owner task |
| Edit tables/fields/records immediately; broader app operations | `app:write` | Not requested by default |
| Edit documents immediately | `documents:write` | Not requested by default |
| Members, owner grants, company-domain access | `workspace:manage` | Not requested by this workflow |

Scopes are capabilities, not a grant to every workspace. Membership and role
floors apply to every call. Scheduled/always-on clients are suggest-only and
cannot receive immediate-write, review, or apply permissions. Do not interpret
`schema:write` as permission to apply a schema immediately, or `app:write` as
membership administration. Document read and write are separate permissions. [1]

If an existing connection already has broad scopes, do not claim the skill makes
it read-only at the server. Ask the operator to use a dedicated least-privilege
connection/re-authorization and inspect granted permissions. Behavior instructions
and tool filters are additional guardrails, not substitutes for account access.
Shared operator credentials must not be offered to unrelated channel users;
per-requester OAuth is a separate administrator-designed identity decision. [3]

## Public unauthenticated evidence

A GET to `/mcp` returned HTTP 401 with `WWW-Authenticate` pointing to
`https://app.tablethis.ai/.well-known/oauth-protected-resource`. Public protected
resource metadata advertises the MCP URL and the nine scopes above. Authorization
server metadata advertises authorization-code + refresh-token grants, PKCE S256,
and public-client token auth (`none`). These checks establish advertised public
metadata only, not successful registration, OAuth interoperability, tool discovery,
workspace access, or any product read/write. No registration or token POST was
performed. See local release evidence (not included in the install bundle).

## Sources

[1] https://www.tablethis.ai/docs
[2] https://docs.openclaw.ai/tools/mcp and https://docs.openclaw.ai/cli/mcp/registry
[3] https://docs.openclaw.ai/cli/mcp/transports
