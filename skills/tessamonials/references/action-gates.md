# Action gates — reference, not permission

Default: private reads under `tessa:read`. Only a separately authorized task may
cross a write gate, after an operator reviews the necessary scope and tool-filter
change. `tessa:write` also permits invitation email; do not request it for reviews.
This package neither enables nor invokes writes. Tool semantics below come from
Tessa's official MCP guide.[1] Always inspect current runtime input schemas.

## Gate checklist

Before any effect, show the company ID/name, campaign/interview/invitation target,
exact proposed payload/content, exposure, and whether the operation is reversible.
Require confirmation for that named operation; do not reuse authorization for a
later gate. Record only a minimal private action receipt, not recipient secrets.
If permission is absent, leave a local draft and stop. Read back the exact target
after a permitted change, without fetching unrelated private data.

| Gate / tools | Required decision and boundary | Read-back / failure handling |
|---|---|---|
| Saved setup: `create_campaign`, `rename_campaign`, `update_campaign`, `set_campaign_notifications` | Explicitly authorize those saved edits. Campaign creation starts **paused** and collects nothing until launch. Read `get_campaign` first for updates and use its current revision; do not overwrite newer edits. Notifications are team-email settings, not recipient-invite sending. | `get_campaign` or the relevant documented read tool. Conflict → reread, preview differences, renew confirmation. No automatic launch. |
| Launch/pause/archive/restore: `set_campaign_state` | Separate explicit state-change approval; owner/admin role required. Show the target state. Restore leaves a campaign paused, not live. | `get_campaign` current state. No role escalation. |
| Prepare recipient: `create_invitation`, `update_recipient_context` | Authorize the exact recipient/context. Invitation creation needs a **live** campaign and an `idempotency_key`; do not launch merely to satisfy it. Creation prepares a personal link and **does not email**. Use the same key for an authorized retry; do not invent a new key to bypass uncertainty. | Prefer `list_invitations` (omits links) for status. Fetch `get_invitation` only if needed and separately authorized to handle the secret link. Never paste the link into a report. |
| Send email: `send_invitation` | Separate approval of the exact existing invitation/recipient and the email content/settings exposed by the live schema. If content is not exposed, disclose that limitation before confirmation. Never infer send permission from “prepare” or “create a link”. | `list_invitations` timeline/status. **Queued is not delivered**. Ambiguous result → inspect, never blindly resend. |
| Approve: `approve_testimonial` | Separate authorization to approve the **exact current draft** on the participant's behalf. Review current consent/unapproval/withdrawal and attribution first. Never automatically reverse a participant's unapproval or withdrawal; resolve with the authorized owner and participant workflow. Do not call approval as a prerequisite for every already-approved testimonial. | `list_testimonials` approval state plus current consent details as needed. Approval starts hidden and approved words are never edited. Changed draft → renewed review, not stale approval. |
| Individual exposure: `set_testimonial_visibility` | Separate visibility approval for the named approved testimonial, its exact approved wording and attribution. Honor anonymity and withdrawal. Setting visibility may expose it if the page is already public; hiding a page is not license to pre-stage visibility without authorization. | Reread `list_testimonials` for approval and visibility **if returned by the live schema**. If visibility is absent, report verification incomplete; never assume approval meant permission to show it. |
| Page exposure: `set_testimonials_page_visibility` | Separate approval of the exact campaign page becoming public/private. Inspect which testimonials are currently visible; publishing a page can expose **all** visible approved items on it. Do not publish just because one item was approved. | Use a live-schema-supported read that returns page visibility; do not assume `get_campaign` contains this field. If none exists, report verification incomplete. If verification would require a public fetch, obtain task-level permission; do not follow arbitrary returned URLs. |

## Product consent, not a fabricated extra requirement

Tessa saves testimonial revisions approved by default; once a participant unapproves,
that choice persists across later revisions until they approve again.[2] Saved
approval does not itself publish. Do not claim mandatory separate participant
approval exists for every draft. These **agent action-confirmation gates** are a
safety policy for writes, not a description of Tessa requiring extra consent UI.

A participant's withdrawal stops reuse even if an older report showed approval.
Do not reconstruct erased content from cache, infer consent from silence, alter
approved words, or turn a private paraphrase into a participant quote. Missing
state is unknown, not permission.[1][2]

## Scope of this reference

No deletion tool is documented here. New/unknown tools, undocumented arguments,
or requested effects beyond these descriptions require current source/schema review
and separate authorization. Tessa roles and OAuth scopes both apply on each call;
never bypass either. See [sources.md](sources.md) for official sources.
