# Dispute Resolution Protocol

## Overview

When three agents independently produce contract content (drafts, reviews, or edits), they must cross-review each other's work to reach consensus. This protocol governs how disagreements are identified, debated, and resolved in a maximum of 3 rounds.

## Streamlined Mode (Default)

In practice, the full 3-round debate is often unnecessary. When agents largely agree (which is common for standard contract types), use this streamlined approach:

1. **Round 1**: Independent work (always required)
2. **Synthesis**: The orchestrator reads all Round 1 outputs and extracts key differences. Instead of spawning full cross-review agents, synthesize the best position on each point of disagreement.
3. **Round 3**: Only if the synthesis reveals genuinely unresolvable conflicts, escalate those specific items through the full rebuttal/tiebreaker process.

This saves time and context window while still getting the benefit of independent perspectives.

## Full Round Structure

Use the full protocol below for complex or high-value contracts where streamlined synthesis is insufficient.

### Round 1: Independent Work

- Each agent works independently with NO visibility into the others' outputs
- Each produces their complete work product (full draft, review, or edit)
- Outputs are collected but not yet shared between agents

### Round 2: Cross-Review

- Each agent receives ALL outputs from Round 1 (their own + the other two agents')
- For each substantive point (clause, recommendation, edit), each agent responds with one of:
  - **AGREE** — Accept this point as-is. No further discussion needed.
  - **ELEVATE** — Accept but flag for user attention. The point is technically acceptable but the user should be aware of a trade-off. Include a brief note explaining why.
  - **CHALLENGE** — Disagree with this point. Must provide:
    - What specifically is wrong or concerning
    - What the alternative should be
    - Why the alternative is better (with reasoning)

- Format for Round 2 responses:

```
## Cross-Review: [Agent Name]

### On [Other Agent]'s Section [X]: [Brief Description]
**Verdict**: AGREE / ELEVATE / CHALLENGE
**Reasoning**: [Explanation]
**Alternative** (if CHALLENGE): [Proposed alternative language or approach]

### On [Other Agent]'s Section [Y]: [Brief Description]
**Verdict**: AGREE / ELEVATE / CHALLENGE
...
```

### Round 3: Resolution

- Only CHALLENGED items proceed to Round 3
- For each challenged item:
  1. The original author provides a **rebuttal** (max 200 words): defend their position or propose a compromise
  2. The challenger provides a **response** (max 200 words): maintain challenge or accept compromise
  3. The **third agent** (who wasn't involved in the dispute) acts as **tiebreaker**: votes for one position with reasoning

- Tiebreaker format:

```
### Tiebreaker: [Disputed Item]
**Ruling**: Support [Agent A] / Support [Agent B] / Propose Compromise
**Reasoning**: [Why this resolution is best]
**Final Language** (if applicable): [The resolved clause text]
```

## Resolution Outcomes

### Consensus Reached

If all challenged items are resolved (either through rebuttal acceptance or tiebreaker), the final contract incorporates the resolved positions. Document all resolutions in a summary.

### Persistent Splits

If any item remains unresolved after Round 3 (tiebreaker supports a position but losing agent still objects strongly), it becomes a **User Decision Point**:

```
## User Decision Required

### Item: [Description]
**Position A** ([Agent Name]):
[Their argument, max 150 words]

**Position B** ([Agent Name]):
[Their argument, max 150 words]

**Tiebreaker voted for**: Position [A/B]
**Tiebreaker reasoning**: [Brief summary]

**Your options**:
1. Accept Position A
2. Accept Position B
3. Provide your own resolution
```

## User Clarification Requests

At ANY point during Rounds 1-3, an agent may pause to request user clarification. This should be used when:

- A factual question about the deal cannot be assumed
- Legal jurisdiction affects the analysis significantly
- A business decision is needed that the agent cannot make
- The user's intent regarding a specific provision is unclear

Format:

```
## Clarification Needed from User
**Agent**: [Name]
**Question**: [Specific question]
**Why it matters**: [Brief explanation of how the answer affects the contract]
**Default if no answer**: [What the agent will assume if the user doesn't respond]
```

## Debate Rules

1. **Substance over style**: Challenges must be about content, not wording preferences (wording is The Plain Speaker's domain)
2. **Cite specifics**: Always reference specific clause numbers or provisions
3. **Propose alternatives**: Never challenge without offering a concrete alternative
4. **Stay in role**: Each agent should challenge from their area of expertise
5. **Acknowledge good points**: If another agent's approach is genuinely better, AGREE — don't challenge for the sake of it
6. **Proportional response**: Minor issues should be ELEVATED, not CHALLENGED. Reserve CHALLENGE for substantive disagreements
7. **User interests first**: All agents ultimately serve the user's interests, not their own perspective

## Presenting Results to the User

See the "Presenting Final Results to the User" section in `agent-personas.md` for the canonical output format.

## Integration with Checklist Verification

After dispute resolution is complete and the final contract text is assembled:

1. Run the appropriate checklist (NDA, engagement, or general) against the final text
2. Any CRITICAL missing items reopens discussion — agents must address them
3. IMPORTANT missing items are noted as warnings in the final report
4. OPTIONAL missing items are noted as suggestions
5. Checklist results are included in the final output to the user
