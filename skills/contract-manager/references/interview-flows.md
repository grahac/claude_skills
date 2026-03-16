# Interview Flows

## Overview
Before any contract operation, the orchestrator interviews the user to gather necessary context. Questions are organized by mode and contract type. Not all questions need to be asked — adapt based on what information is already provided.

## General Principles
- Ask the minimum questions needed. If the user provides extensive context upfront, skip questions already answered.
- Group related questions together rather than asking one at a time.
- Required questions are marked with **(Required)** — these must be answered before proceeding.
- Optional questions are marked with **(Optional)** — skip if the user doesn't volunteer the info.
- Always confirm the contract type first, then branch to the appropriate flow.

---

## Phase 0: Mode and Type Detection

Ask first:
1. **(Required)** What would you like to do? (Create a new contract / Review an existing contract / Edit an existing contract)
2. **(Required)** What type of contract? (NDA / Consulting/Freelance Engagement / Other — please describe)
3. **(Optional)** Which party are you? (This helps agents know whose interests to prioritize)

---

## Create Mode

### Create: NDA

**Round 1 — Core Terms** (ask together):
1. **(Required)** Who are the parties? (Full legal names, entity types if applicable)
2. **(Required)** Is this mutual or unilateral? If unilateral, who is the disclosing party?
3. **(Required)** What is the purpose of sharing confidential information? (e.g., evaluating a potential business relationship, due diligence for acquisition)
4. **(Required)** How long should the confidentiality obligation last? (e.g., 2 years, 5 years, perpetual for trade secrets)

**Round 2 — Specifics** (ask based on answers):
5. **(Required)** What types of information will be shared? (technical, financial, business plans, customer data, source code, etc.)
6. **(Optional)** Are there specific exclusions you want? (information already public, independently developed, etc.)
7. **(Optional)** Should there be a non-solicitation clause? (prevent hiring each other's employees)
8. **(Optional)** Should there be a non-compete provision? If so, what scope and duration?
9. **(Optional)** Any specific jurisdiction/governing law preference?
10. **(Optional)** Any special requirements? (e.g., GDPR compliance, export controls, specific industry regulations)

### Create: Engagement/Consulting Agreement

**Round 1 — Core Terms** (ask together):
1. **(Required)** Who is the client and who is the contractor/consultant? (Full legal names)
2. **(Required)** Describe the scope of work. What services will be provided? What are the specific deliverables?
3. **(Required)** What is the compensation structure? (Hourly rate, fixed fee, milestone-based, retainer)
4. **(Required)** What is the intended duration? (Start date, end date, or ongoing with termination notice)

**Round 2 — Details**:
5. **(Required)** Who owns the intellectual property created during the engagement? (Client owns all / Contractor retains and licenses / Shared)
6. **(Required)** Does the contractor have pre-existing IP that will be used? (If yes, it needs to be carved out)
7. **(Optional)** Payment terms? (Net 15, Net 30, upon delivery, milestones, etc.)
8. **(Optional)** Hours expectation? (Approximate hours/month for retainer engagements, overage rate if applicable)
9. **(Optional)** Can the contractor subcontract work?
10. **(Optional)** Is there a non-compete or exclusivity requirement?
11. **(Optional)** Any specific confidentiality concerns beyond standard?
12. **(Optional)** Does the contractor use AI tools? (If yes, include an Approved AI Tools provision and Exhibit A)
13. **(Optional)** Who provides equipment/tools/software?
14. **(Optional)** Preferred governing law/jurisdiction?
15. **(Optional)** Any insurance requirements? (Professional liability, E&O, etc.)
16. **(Optional)** Should residual knowledge (skills/techniques learned on the job) be retained by contractor?
17. **(Optional)** Do you have a reference contract or template to use as a structural guide?

### Create: General Contract

**Round 1 — Core Terms** (ask together):
1. **(Required)** Who are the parties? (Full legal names and roles)
2. **(Required)** What is the purpose of this contract? Describe the arrangement in detail.
3. **(Required)** What does each party give and receive? (The consideration/exchange)
4. **(Required)** What is the intended duration?

**Round 2 — Details**:
5. **(Required)** What are each party's key obligations? Be as specific as possible.
6. **(Optional)** Payment terms if applicable?
7. **(Optional)** Termination conditions? (For cause, for convenience, notice period)
8. **(Optional)** Confidentiality requirements?
9. **(Optional)** IP ownership provisions?
10. **(Optional)** Dispute resolution preference? (Mediation, arbitration, litigation)
11. **(Optional)** Governing law/jurisdiction?
12. **(Optional)** Any industry-specific requirements or regulations?
13. **(Optional)** Any other specific terms or concerns?

---

## Review Mode

### Review: All Contract Types

1. **(Required)** Please provide the contract text. (Paste it or provide a file path)
2. **(Required)** Which party are you in this contract? (Helps agents assess terms from your perspective)
3. **(Optional)** What are your primary concerns? (e.g., IP terms seem unfair, payment schedule is unclear, worried about liability)
4. **(Optional)** Is this a contract you've been asked to sign, or one you drafted?
5. **(Optional)** Are there specific sections you want extra attention on?
6. **(Optional)** What jurisdiction/governing law applies (if not stated in the contract)?
7. **(Optional)** Is there any context about the business relationship that would help? (e.g., relative bargaining power, industry norms)
8. **(Optional)** Are you comparing this against any industry standard or template?

---

## Edit Mode

### Edit: All Contract Types

1. **(Required)** Please provide the current contract text. (Paste it or provide a file path)
2. **(Required)** What changes do you want to make? Be as specific as possible.
3. **(Optional)** Why are these changes needed? (Context helps agents propose better edits)
4. **(Optional)** Are there any terms that must NOT change? (Preserve specific provisions)
5. **(Optional)** Which party are you? (Helps agents assess impact of changes)
6. **(Optional)** Has the other party proposed these changes, or are you proposing them?
7. **(Optional)** Any concerns about how the other party might react to these changes?
8. **(Optional)** Is this a renegotiation or an amendment to an existing signed contract?

---

## Interview Best Practices

- **Be conversational**: Let the user talk naturally. Extract answers from their narrative rather than forcing a rigid Q&A format.
- **Batch questions**: Ask Round 1 questions together, wait for answers, then ask Round 2 questions.
- **Adapt**: If the user provides a detailed brief upfront, extract answers and only ask what's missing.
- **Confirm understanding**: Before proceeding to agent work, summarize what you understood and ask the user to confirm.
- **Don't over-ask**: If something has a reasonable default, use it and note the assumption rather than asking.
- **Provide examples**: When asking about technical provisions (like IP ownership), give brief examples of common approaches.
- **Accept reference documents**: If the user provides a reference contract or template (PDF, docx, or pasted text), use it as structural guidance for the new contract.
- **Suggest what they might not think of**: Proactively ask about overage rates, hours caps, expense policies, and AI tool usage — users often don't think of these upfront.
- **Save user info**: If this is a returning user, check memory files for their entity name, address, and contact info to auto-fill.
