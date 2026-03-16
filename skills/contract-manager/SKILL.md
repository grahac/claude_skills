# Contract Manager

Multi-agent contract management skill. Creates, reviews, and edits contracts using three specialized Claude subagents that independently analyze, cross-review, debate disagreements, verify required clauses, and produce professional `.docx` output.

## Trigger

Activate when the user wants to:
- **Create** a new contract (NDA, consulting/freelance engagement, or general)
- **Review** an existing contract for risks, clarity, and business viability
- **Edit** an existing contract with specific changes

Keywords: "contract", "NDA", "agreement", "engagement letter", "consulting agreement", "draft a contract", "review this contract", "edit this contract"

## Quick Reference — File Map

| File | Purpose | When to Read |
|------|---------|-------------|
| `references/agent-personas.md` | Agent definitions + system prompt templates | Before spawning any agent |
| `references/interview-flows.md` | Interview questions by mode × contract type | Before interviewing the user |
| `references/dispute-resolution.md` | 3-round debate protocol (AGREE/ELEVATE/CHALLENGE) | Before starting Round 2 cross-review |
| `references/nda-checklist.md` | NDA required clauses (Critical/Important/Optional) | When contract type is NDA |
| `references/engagement-checklist.md` | Engagement/consulting required clauses | When contract type is engagement |
| `references/general-checklist.md` | General contract required clauses | When contract type is general/other |
| `scripts/generate_docx.py` | JSON → .docx generation | When producing final document |
| `scripts/codex_agent.py` | Optional 4th agent (Codex/OpenAI) | When user requests outside perspective |

## Workflow Overview

```
User Request
    │
    ▼
┌─────────────┐
│  Interview   │  ← Read interview-flows.md for questions
│  (gather     │
│   context)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Round 1:    │  ← Read agent-personas.md for system prompts
│  Independent │  Spawn 3 Claude agents in parallel (+ optional Codex)
│  Work        │  Each produces complete draft/review/edit
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Round 2:    │  ← Read dispute-resolution.md
│  Cross-      │  Each agent sees all Round 1 outputs
│  Review      │  Responds: AGREE / ELEVATE / CHALLENGE
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Round 3:    │  Only for CHALLENGED items
│  Resolution  │  Rebuttal → Response → Tiebreaker vote
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Checklist   │  ← Read appropriate checklist file
│  Verification│  Critical missing = BLOCKER
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  User Review │  Present comparison, checklist results,
│  & Decision  │  unresolved splits → user picks/merges
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Generate    │  ← Run scripts/generate_docx.py
│  .docx       │  Build JSON → produce document
└─────────────┘
```

## Step-by-Step Instructions

### Step 1: Detect Mode and Contract Type

Read `references/interview-flows.md` Phase 0 questions. Determine:
- **Mode**: Create / Review / Edit
- **Contract type**: NDA / Engagement / General
- **Which party** the user represents (if applicable)

If the user's initial message already contains enough context, extract answers and skip redundant questions.

### Step 2: Interview

Using the appropriate section of `references/interview-flows.md`:

**Create mode**: Ask Round 1 core questions together. Wait for answers. Then ask Round 2 detail questions (skip any already answered). Proactively suggest provisions users often forget: hours caps with overage rates, AI tool usage, residual knowledge retention, and expense policies.

**Review mode**: Get the contract text and the user's concerns. Ask clarifying questions only as needed.

**Edit mode**: Get the contract text and desired changes. Confirm what must NOT change.

**Auto-fill**: Check memory files for returning user info (entity name, address, email). If found, confirm with the user and pre-populate.

**Reference documents**: If the user provides a reference contract or template, use it as structural guidance for the new contract.

Before proceeding, summarize your understanding back to the user and confirm it's correct.

### Step 3: Load References

Read these files before spawning agents:
1. `references/agent-personas.md` — get system prompt templates
2. The appropriate checklist:
   - NDA → `references/nda-checklist.md`
   - Engagement → `references/engagement-checklist.md`
   - General → `references/general-checklist.md`

### Step 4: Check Codex Availability (Optional)

If the user requests an outside perspective, or for high-value contracts:

```bash
python3 scripts/codex_agent.py --check
```

If exit code 0, Codex is available. Note the backend (`codex` or `openai`).

### Step 5: Round 1 — Independent Agent Work

Spawn **three Claude Task subagents in parallel** using the Task tool:

For each agent (The Shield, The Plain Speaker, The Deal Maker):

1. Build the system prompt by combining:
   - The agent's system prompt template from `agent-personas.md`
   - Mode-specific instructions (draft/review/edit) from `agent-personas.md`
   - The contract context gathered during interview

2. Launch via Task tool with `subagent_type: "general-purpose"`:
   - Set a clear description (e.g., "Shield agent: draft NDA")
   - Include the full system prompt and contract context in the task prompt
   - Tell each agent to produce a COMPLETE output (full draft, full review, or full edit)

3. If Codex is available, also run it in parallel:
   ```bash
   # Write system prompt and user prompt to uniquely-named temp files
   python3 scripts/codex_agent.py --prompt /tmp/codex_prompt_<unique_id>.txt --system /tmp/codex_system_<unique_id>.txt --output /tmp/codex_output_<unique_id>.txt --mode draft
   ```

**All agents run simultaneously with NO visibility into each other's work.**

### Step 6: Round 2 — Cross-Review (Streamlined by Default)

Read `references/dispute-resolution.md` for the full protocol.

**Streamlined mode (default)**: Read all Round 1 outputs yourself and synthesize the best position on each point of disagreement. Only spawn full cross-review agents if you identify genuinely unresolvable conflicts between agents. This saves time and context while still getting independent perspectives.

**Full cross-review mode** (for complex/high-value contracts): Spawn **three new Claude Task subagents in parallel**, one per persona. Each receives:
- Their own Round 1 output
- The other two agents' Round 1 outputs (and Codex output if available)
- Instructions to respond to each substantive point with: **AGREE**, **ELEVATE**, or **CHALLENGE**

The cross-review prompt for each agent should include:
```
Review the outputs from the other agents. For each substantive clause, recommendation, or edit, respond with:

AGREE — Accept as-is
ELEVATE — Accept but flag for user attention (explain the trade-off)
CHALLENGE — Disagree (state what's wrong, propose alternative, explain why)

Use the format from dispute-resolution.md.
```

### Step 7: Round 3 — Resolution (If Needed)

Only proceed to Round 3 if there are CHALLENGED items from Round 2.

For each challenged item:
1. Spawn the **original author** agent to provide a rebuttal (max 200 words)
2. Spawn the **challenger** agent to respond (max 200 words)
3. Spawn the **third agent** as tiebreaker to vote with reasoning

If any items remain unresolved after tiebreaker, format them as **User Decision Points** per the dispute-resolution.md template and present to the user.

### Step 8: Checklist Verification

Using the appropriate checklist file, verify the final contract text against every item:

- **CRITICAL missing items** → BLOCKER. Do not proceed to .docx generation. Present the missing items to the user and ask how to address them. Re-engage agents if needed.
- **IMPORTANT missing items** → WARNING. Present to user with recommendation to address them.
- **OPTIONAL missing items** → SUGGESTION. Note them but don't block.

Format the checklist results:

```
## Checklist Verification: [Contract Type]

### BLOCKERS (Critical — must address)
- ❌ [Item name]: [What's missing and why it matters]

### WARNINGS (Important — recommended)
- ⚠️ [Item name]: [What's missing and suggestion]

### SUGGESTIONS (Optional)
- 💡 [Item name]: [What could be added]

### PASSED
- ✅ [Item name]: Found in Section [X]
```

### Step 9: Present Results to User

**Keep it simple.** Do not dump raw agent outputs. Synthesize and distill into the four-category format defined in the "Presenting Final Results to the User" section of `references/agent-personas.md`.

**Create mode**: Also include:
- Summary of key terms
- Checklist results
- Any unresolved agent disagreements (with both sides' arguments)

**Review mode**: Also include:
- Checklist of missing clauses
- Prioritized recommendations

**Edit mode**: Also include:
- Redline summary of changes
- Impact assessment

### Step 10: Generate .docx

Once the user approves the final text, build the JSON input for `generate_docx.py`:

```json
{
  "title": "Contract Title",
  "date": "Month Day, Year",
  "parties": [
    {"name": "Full Legal Name", "role": "Role", "address": "Full Address"}
  ],
  "recitals": "WHEREAS clauses...",
  "sections": [
    {"number": "1", "heading": "Section Title", "content": "Section text..."},
    {"number": "1.1", "heading": "Subsection Title", "content": "Subsection text..."}
  ],
  "signature_blocks": [
    {"party": "Party Name", "name_line": "Signer Name", "title_line": "Title"}
  ]
}
```

Write the JSON to a uniquely-named temp file (e.g., using a timestamp or UUID to avoid collisions), then run:

```bash
python3 scripts/generate_docx.py --input /tmp/contract_<unique_id>.json --output ~/Desktop/contract.docx
```

**Prerequisites**: `python-docx` must be installed. If not:
```bash
pip3 install python-docx
```

Tell the user where the file was saved.

For **review mode**, generate a review report .docx instead of a contract. Omit `parties` and `signature_blocks` from the JSON (they are optional). Structure the JSON sections as the review findings organized by topic.

**Engagement contracts**: Include an Exhibit A (Scope of Work) by default. This separates the scope from the main agreement, allowing updates without amending the core terms. If the contractor uses AI tools, include an Approved AI Tools section in the exhibit.

## Agent Spawning

For each agent (The Shield, The Plain Speaker, The Deal Maker), construct the Task prompt by combining:

1. The agent's **system prompt template** from `references/agent-personas.md`
2. The **mode-specific instructions** (draft/review/edit) from `references/agent-personas.md`
3. The **contract context** block:

```
CONTRACT CONTEXT:
- Type: [NDA/Engagement/General]
- Parties: [Details]
- Key Terms: [From interview]
- Jurisdiction: [If specified]
- Special Requirements: [If any]
```

4. A mode-appropriate instruction (e.g., "Draft a COMPLETE [contract type]..." or "Review the following contract...")

For **cross-review mode**, give each agent their own Round 1 output plus the other agents' outputs, with instructions to respond using AGREE/ELEVATE/CHALLENGE per `references/dispute-resolution.md`.

## Error Handling

- **python-docx not installed**: Print install command and stop. Do not attempt fallback.
- **Codex unavailable**: Proceed with three Claude agents only. Note in output that Codex was not used.
- **Agent produces incomplete output**: Re-run that single agent with a reminder to produce complete output.
- **All agents agree on everything in Round 2**: Skip Round 3. Note the consensus.
- **Checklist BLOCKER found**: Do not generate .docx. Present the gap and ask user how to proceed.
- **User provides contract as file path**: Read the file content before passing to agents.

## Important Notes

- **Reading contract file inputs**: For review/edit mode, the user may provide a contract as a file. PDF files can be read directly with the Read tool. For `.docx` files, use `python3 -c "import docx; doc = docx.Document('<path>'); print('\n'.join(p.text for p in doc.paragraphs))"` to extract text. For pasted text, use it directly.
- Always read the referenced files before using them — don't rely on cached knowledge of their contents.
- Agents should never see each other's work during Round 1. This is critical for independent analysis.
- The user always has final say. Agent consensus is a recommendation, not a decision.
- For review and edit modes, preserve the original contract's numbering when possible.
- When in doubt about a legal question, note the uncertainty and suggest the user consult an attorney.
- Output paths default to `~/Desktop/` unless the user specifies otherwise.
