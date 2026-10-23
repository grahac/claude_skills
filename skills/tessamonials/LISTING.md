# Proposed ClawHub listing (not published)

- **Slug:** `tessamonials`
- **Display name:** Tessamonials — Interview Evidence Review
- **Version:** `1.0.0`
- **Categories:** `integrations`, `research`
- **Topics:** `customer-feedback`, `interview-analysis`, `testimonials`, `mcp`
- **Homepage:** https://tessamonials.com/docs/mcp
- **Product site:** https://tessamonials.com/
- **Verified official product icon URL:** https://tessamonials.com/images/favicon.svg?v=2

Icon provenance: the public Tessamonials homepage's `link rel="icon"` declares
`/images/favicon.svg?v=2`. A public GET on October 22, 2026 returned HTTP 200 and
`image/svg+xml`; the captured body parses as SVG. Source captures and its SHA-256
are retained outside this installable skill in the release-review evidence.[8][9]

This is a **skill**, not an OpenClaw plugin. The URL is listing material for an
operator/editor; no unsupported `icon` frontmatter field is claimed. OpenClaw's
publishing docs describe bundled `assets/icon.png` for **plugin** artwork, which is
not a guarantee that this skill listing can display a remote icon.[6][7]

## Summary

Review authorized Tessamonials interviews and campaign results with evidence,
coverage counts, counterexamples, and testimonial-readiness checks. Private analysis
by default; optional local drafts only when requested. Native MCP OAuth setup is
required. Launches, invitation email, approvals, and publication are separate gates.

## Requirements and limits

An authorized Tessamonials account/company membership and a compatible native MCP
runtime are required. OpenClaw setup uses Settings → MCP on the Gateway's own HTTPS
origin; the documented CLI loopback callback is not the default route for Tessa's
HTTPS-only callback policy. No API key, custom auth bridge, or automatic installer.
Service plan/voice allowances may apply.[1][3][4]

The review tested only public metadata, unauthenticated HTTP behavior, bundle
structure, and static instruction/config properties. No company data, private
interviews, OAuth login, invitations, approvals, launches, or publication were
exercised. Do not describe this listing as officially endorsed, security-certified,
or end-to-end tested. Publisher identity, brand permission, slug availability,
server-side security review, and publication remain owner decisions.

## Proposed version notes

Initial read-first interview-review skill, eight-tool least-privilege configuration,
evidence brief template, and explicit consent/exposure boundaries.

See [references/sources.md](references/sources.md) for official sources.
