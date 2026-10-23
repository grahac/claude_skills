# Bounded reconciliation playbooks

These are procedures and response templates, not fabricated TableThis records or
API request schemas. Fill them only with observed data and exact discovered IDs.
All reads stay within the explicitly selected workspace. All submissions require
owner consent, appropriate OAuth scopes, and role floors.

## Shared investigation boundary

For ordinary investigations and each scheduled run, use the single canonical
[investigation budgets](../SKILL.md#investigation-budgets-ordinary-and-scheduled-work).
Record default or explicitly owner-approved scoped ceilings before reading; do
not reset counters between tables, searches, cursor pages, retries, or re-reads.
Set adequate tool limits within every remaining budget; if a bounded read cannot
be established, stop. Before exceeding any budget, stop, report partial coverage
and usage, and request fresh owner approval of scoped replacement ceilings.
These are instruction defaults, not product API limits or a runtime sandbox.

## Research tracker / CRM cleanup

User: "Compare the customer table with the latest account notes. Suggest status
corrections but don't change anything."

1. List workspaces and resolve the explicit workspace; ask if none is specified.
2. Discover the schema/query/read/search tools through the active runtime and
   describe their exact schemas. Inspect field types and enum options.
3. Query the requested customers with narrow filters within the shared
   investigation boundary above. Search relevant Markdown notes and read context
   around matches only while all aggregate budgets permit. Follow cursors only
   within remaining budgets and record coverage; lack of a match is not proof
   of no evidence.
4. Reconcile using dated, attributable evidence. Flag conflicting sources and
   missing values; do not invent an enum value or infer personal information.
5. Return a draft review table below. End with "Product changes: none".
6. Only if asked to submit this specific proposal: confirm exact bounded items,
   re-read old values, then use the discovered proposal capability with the
   server's exact expected-value fields. Read back the resulting changeset.

## Shared company knowledge lookup

User: "In workspace X, where do the onboarding docs disagree with the team table?"

Within the shared investigation boundary: read schema → query named team rows →
search onboarding documents → read Markdown passages → report disagreements with
document/record IDs, budget usage, and query bounds. Null
document output can mean absent document scope, so report the access gap rather
than asserting there are no onboarding documents. Do not edit documents or read
members to infer team membership. Document proposal support must be discovered;
public docs only explicitly advertise immediate document edits via
`documents:write`. [1]

## Scheduled watch, no auto-apply

An owner may authorize a schedule with a fixed workspace, table, filter, proposal
ceiling, and evidence rule. The shared investigation boundary applies to each run,
including all row/page/document/passage/text dimensions; use its defaults unless
the owner explicitly approves scoped replacement ceilings. A cursor backlog or
missed run is not permission to expand them. Prefer read-only reporting. A suggest-only
connection may submit bounded proposals only if the owner has explicitly approved
that standing submission scope. Persist a returned change cursor only in an
owner-approved local/state location; no state path is created by this skill.
On missed runs or stale cursors, report gaps and re-read within limits. Do not
request immediate-write/review/apply permissions or auto-approve the proposals.
Those permissions are unavailable to scheduled/always-on clients. [1]

## Review table (template, not real product data)

Investigation receipt (required for read-only reports and proposal reviews):
workspace/targets/filter/date range; approved or default ceilings from the shared
investigation boundary; used/remaining records, record pages, documents, document
pages/calls, passages, and aggregate UTF-8 text bytes; coverage/stop reason; unread
cursors/targets; fresh owner approval needed before any budget expansion. Do not
label partial results complete or infer absence from unread evidence.

| Workspace/table ID | Record/field ID | Expected old value (typed) | Proposed new value (typed) | Evidence ID/passage | Why / uncertainty |
| --- | --- | --- | --- | --- | --- |
| Fill from observed results | Fill from observed results | Preserve exact value | Use schema type | Cite retrieved context | Explain and flag gaps |

For each submission record: owner-approved scope; schema checked at; records
re-read at; discovered tool ID; expected-value semantics; returned proposal ID;
read-back status; conflicts/skips; remaining human action. Do not copy this table
verbatim into tool args: only the live tool schema defines the payload.

## Conflict / unknown-result decision tree

- Expected old value differs from current value → stop that item, fetch current
  state/history, explain the competing edit. Redraft and seek fresh consent if
  effect changed. Never overwrite by updating the expected value blindly.
- Timeout after submission → do not automatically resubmit. Inspect pending
  changes/history for the same targets and intended diff; if uncertain, escalate.
- Proposal readback succeeds → report actual proposal status, not applied state.
- Broader interactive write explicitly approved → verify exact target readback
  and audit history; distinguish successful, failed, and unverified items.
- Search empty just after a write → use exact-ID readback/history; indexing may
  lag. Do not claim failure/success from search alone. [1]

## Sources

[1] https://www.tablethis.ai/docs
