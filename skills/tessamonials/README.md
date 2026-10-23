# Tessamonials skill

A portable instruction skill for turning authorized customer-interview results into
private, evidence-led decisions. It supplies no connector plugin, OAuth client,
automation daemon, or credentials.

## Useful prompts

- “Review completed, non-test responses for my specified campaign this month.
  Start with stored summaries; surface repeated friction and counterexamples.
  Do not fetch transcripts or change anything.”
- “For these interview IDs, inspect authorized transcript pages and substantiate
  the three findings with minimal quotes and returned turn/position locators.”
- “Audit testimonial readiness for this campaign. Report the observed approval,
  anonymity, and visibility states; do not approve or publish anything.”
- “Draft revised interview questions locally from these findings. Leave all Tessa
  settings unchanged.”

## Setup and privacy

Read [SKILL.md](SKILL.md) before use. The dependency is an authorized Tessamonials
account/company membership and a runtime with native remote Streamable HTTP MCP,
OAuth 2.0 PKCE, dynamic registration, and **HTTPS callbacks**. No API-key environment
variable or mandatory local binary is declared: a native UI setup can satisfy the
runtime dependency. Installation alone does not establish authentication.

OpenClaw's current official route is **Settings → MCP**. Configure the server using
[references/read-only-server.json](references/read-only-server.json), merging only
that server and preserving others. Use the Gateway's own HTTPS browser address for
native Sign in. Do not substitute the CLI HTTP-loopback login: Tessa's documented
callback policy requires HTTPS. This package did not exercise sign-in and cannot
promise end-to-end compatibility on a particular Gateway version.[1][3][4][5]

The example uses only `tessa:read` and eight named read tools; it omits invitation
reads that can expose bearer links. `get_transcript` is available only for tasks
where the user authorized that private access, not for automatic bulk collection.
Tool filtering is defense in depth; scope, membership, audience policy, and task
scope still matter. Shared operator OAuth is inappropriate for unrelated users.

Tessamonials can have external service/plan limits. Existing stored-result reads
make no new Tessa model call; voice interviews consume the company's allowance.
This is not a promise that all accounts or service operations are free. No paid
runs are needed to use or validate these instructions.[1]

Tessa saves testimonial revisions approved for use by default, until participant
unapproval. Publication is a separate choice; anonymity and withdrawal remain
binding.[2] The skill's confirmation gates for later agent actions must not be
misrepresented as a mandatory extra participant-consent workflow.

## Contents

- `SKILL.md`: trigger, native setup, scoped review workflow, privacy, failure modes.
- `references/read-only-server.json`: operator-reviewed OpenClaw config example.
- `references/review-template.md`: evidence and coverage-focused private brief.
- `references/action-gates.md`: separate saved-edit, launch, prepare, send, approval,
  testimonial-visibility, and page-publication decisions.
- `references/sources.md`: official references and validation boundaries.
- `LISTING.md`: proposed catalog copy and verified product icon URL; not an
  unsupported metadata field or a plugin artwork claim.
- `LICENSE`: MIT-0, matching ClawHub's published-skill license policy.[6]

No scripts run on installation. The surrounding release-review directory contains
public-source captures and stdlib tests; it is **not** the skill publication root.
See `references/sources.md` for numbered source URLs.
