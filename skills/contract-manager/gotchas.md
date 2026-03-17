# Contract Manager Gotchas

Common failure patterns. Update this file every time something goes wrong.

## 1. Agents seeing each other's work during Round 1
**Problem:** Passing one agent's draft to another during the independent work phase, contaminating their analysis.
**Fix:** Round 1 agents must run in parallel with NO visibility into each other's outputs. Cross-review only happens in Round 2.

## 2. Dumping raw agent outputs to the user
**Problem:** Presenting three full contract drafts side-by-side instead of synthesizing the best position.
**Fix:** Read all outputs yourself and present a synthesized result using the four-category format from `references/agent-personas.md`.

## 3. Generating .docx without checking for blockers
**Problem:** Running `generate_docx.py` before verifying the checklist, producing a document with critical missing clauses.
**Fix:** Always run checklist verification (Step 8) before Step 10. Critical missing items are BLOCKERS — do not proceed to .docx.

## 4. python-docx not installed
**Problem:** The `generate_docx.py` script fails because `python-docx` isn't installed.
**Fix:** Check for it before running. Print `pip3 install python-docx` and stop. Do not attempt fallbacks.

## 5. Forgetting Exhibit A for engagement contracts
**Problem:** Engagement/consulting contracts missing a separate Scope of Work exhibit, putting scope details in the main body.
**Fix:** Always include an Exhibit A for engagement contracts. This separates scope from core terms, allowing scope updates without amending the agreement.
