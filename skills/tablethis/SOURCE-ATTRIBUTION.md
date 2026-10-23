# Source attribution and release provenance

Original skill instructions, templates, and validation code prepared on
2026-10-22; not an official TableThis or OpenClaw endorsement. Distribution license:
MIT-0 (`LICENSE`), consistent with ClawHub's current skill-format licensing.
No upstream implementation code or complete upstream documentation is bundled.
References below remain governed by their respective owners' terms.

Public primary sources inspected live on 2026-10-22:

1. TableThis homepage: https://www.tablethis.ai/ — product identity and official
   icon discovery.
2. TableThis connector docs: https://www.tablethis.ai/docs — hosted MCP endpoint,
   OAuth clients, typed tables/Markdown capabilities, workspace scoping, nine
   scopes, role/async boundaries, expected-value conflicts, audit and recovery.
3. OpenClaw outbound MCP guide: https://docs.openclaw.ai/tools/mcp — native
   `mcp.servers`, Settings → MCP, OAuth and runtime guidance.
4. OpenClaw registry reference: https://docs.openclaw.ai/cli/mcp/registry — exact
   CLI commands, Gateway-stop requirement, replacing vs updating definitions,
   distinct mcporter registry, approval semantics.
5. OpenClaw transport/OAuth reference:
   https://docs.openclaw.ai/cli/mcp/transports — `streamable-http`, native OAuth,
   `oauth.scope`, shared operator credentials and separate requester identity.
6. OpenClaw Tool Search: https://docs.openclaw.ai/tools/tool-search — actual
   `tool_search`, `tool_describe`, `dispatch_action` shapes and harness differences.
7. ClawHub skill format: https://docs.openclaw.ai/clawhub/skill-format — supported
   frontmatter, runtime metadata, regular files/ignore handling, MIT-0 license.
8. ClawHub publishing: https://docs.openclaw.ai/clawhub/publishing — skill CLI
   dry-run, category/topic limits, pending security checks. A local dry run does
   not establish publisher ownership, registry validation or moderation success.
9. Public OAuth metadata:
   https://app.tablethis.ai/.well-known/oauth-protected-resource and
   https://app.tablethis.ai/.well-known/oauth-authorization-server — advertised
   resource/scopes, issuer, PKCE and registration/token endpoint URLs. Endpoint
   URLs were observed only; registration, authorization and token exchange were
   not performed.

The official TableThis SVG icon URL was discovered in the live site's
`link[rel=icon]` and GET-verified as HTTP 200 `image/svg+xml`:
https://www.tablethis.ai/images/logo-c39ed0804ac9b212eb3dce23b696a9f2.svg?vsn=d
The URL is provided for listing review, not copied as a relicensed asset and not
a claim that ClawHub skills accept a remote icon frontmatter field. Do not apply
plugin-only `assets/icon.png` rules to this instruction skill.

Local evidence under `evidence/` preserves retrieval/probe records and public
document text for review; it is excluded from publication. Direct urllib requests
were blocked with HTTP 403, so live public browser retrieval was used instead.
No cookies/Authorization headers were supplied in the endpoint probes, and no
private/account content was read. Exact TableThis tool names and argument schemas
remain an authenticated operator acceptance check, intentionally not guessed here.
