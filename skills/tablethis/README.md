# TableThis instruction skill

Read and reconcile shared typed tables and Markdown documents in a chosen
TableThis workspace. Start read-only; turn an approved, evidence-backed draft into
a conflict-aware proposal only when asked. This package ships instructions, not
an MCP server, application plugin, custom OAuth client, or a live integration test.

## Use

Install/load this folder using your client's supported Agent Skills mechanism,
read `SKILL.md`, and configure the native remote OAuth MCP connection described
there. Current OpenClaw uses `mcp.servers` and Streamable HTTP; older clients may
need an upgrade or their own documented native remote-MCP route. Do not use
`openclaw mcp serve` to connect to TableThis. [1][2]

Example requests:

- "In TableThis workspace Sales, summarize the customer table's overdue follow-ups.
  Read only; show the query bounds and record IDs."
- "In workspace Research, compare this table with its supporting Markdown notes.
  Draft corrections with evidence; don't submit or apply anything."
- "Submit only the three proposals I approved for workspace X. Do not review or
  apply them; report their IDs and read-back status."

The skill first resolves the workspace, describes actual tool schemas and table
fields, reads bounded records/documents, and distinguishes draft/submitted/
approved/applied. No TableThis tool names or authenticated records were invented.

## Prerequisites, access, and cost

A remote Streamable HTTP MCP client supporting native OAuth, and authorized
TableThis workspace access. No environment variables or API keys are required by
this skill. The account owner completes sign-in at TableThis, where sign-up is
available. Service plan limits/costs are external to the skill; check TableThis
before adopting a paid workflow. This package does not assert a current price. [1]

Use `tables:read` and, only if needed, `documents:read` initially. Proposal
submission is an external write requiring explicit owner consent and the relevant
proposal scope. Scheduled/always-on clients are suggest-only; immediate edits,
review, and apply are not available to them. Roles constrain all calls. Not every
write is human-reviewed; immediate interactive edits exist with separate scopes.
No member-management permission is requested by this workflow. [1]

## Validate offline

Python 3.9+ standard library only; no install or network required:

```sh
python3 scripts/validate.py --root .
python3 -m unittest discover -s tests -v
```

The validator checks package shape, the intentionally restricted supported
frontmatter subset, scoped connection examples, links, permission/safety markers,
credential-like content, and file/symlink/size bounds. The tests exercise negative
fixtures as well as a valid package. Static checks are not proof of safety or
OAuth/runtime compatibility. The tests create disposable fixtures only under
`evidence/`, within this folder. Scripts never connect or authenticate. Validation
also works in a clean downloaded bundle, where ClawHub omits hidden source ignore
files and may add its own `.clawhub/origin.json` installation metadata.

Release evidence and listing drafts remain local and are excluded by
`.clawhubignore`; the CLI dry run and its exact observed result are recorded in
`VALIDATION.md`. No login, publication, authenticated tool discovery, workspace
reads, proposal writes, or broader product mutations were performed during build.
See [SOURCE-ATTRIBUTION.md](SOURCE-ATTRIBUTION.md) for upstream sources and license.

## Files

- `SKILL.md`: triggers, setup, real runtime discovery/call paths, workflows, gates.
- `references/connection.md`: least-privilege scope matrix and setup caveats.
- `references/workflows.md`: reconciliation, scheduled watch, review template.
- `scripts/validate.py`, `tests/test_validate.py`: offline package checks.
- `LICENSE`: MIT-0, matching ClawHub's skill licensing. [3]

## Sources

[1] https://www.tablethis.ai/docs
[2] https://docs.openclaw.ai/tools/mcp and https://docs.openclaw.ai/cli/mcp/registry
[3] https://docs.openclaw.ai/clawhub/skill-format
