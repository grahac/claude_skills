---
name: indispensable-need
description: Identify the indispensable need for a product — the high-stakes job to be done that has no good substitute. Analyzes on functional, emotional, and social dimensions using multiple parallel agents, competitive research, and deep codebase reading. Use when the user says "indispensable need", "what makes this indispensable", "why would someone need this", "find the JTBD", or any variation of wanting to understand what makes (or could make) a product impossible to replace.
---

# Indispensable Need

Find the one thing that makes a product irreplaceable — the job to be done that is critically important AND poorly served by alternatives.

## What is an Indispensable Need?

An indispensable need sits at the intersection of two forces:

1. **High importance** — the job matters deeply to the person (not nice-to-have, but load-bearing in their life or work)
2. **No good substitute** — existing alternatives fail to do this job well, or do it with painful tradeoffs

When both are true, you have a product that people can't quit. When only one is true, you have either a commodity (important but substitutable) or a novelty (unique but unimportant).

## Input

This skill accepts **either**:
- **Text after the command**: a product description, pitch, URL, or concept to analyze
- **No text**: read the current codebase to understand the product being built

If no text is provided, deeply read the codebase — README, landing pages, core features, config, tests — to understand what the product does and who it's for.

## Execution

### Phase 1: Deep Understanding

Before any analysis, build a thorough understanding of the product:

1. **If text was provided**: Parse the product description. Use WebSearch to find the product's website, docs, reviews, and any public information.
2. **If reading codebase**: Read broadly — README, router/routes, core modules, database schema, tests, UI components. Understand what the product actually does, not just what it claims to do.
3. **Use WebSearch** to find:
   - Direct competitors and alternatives
   - User reviews, complaints, and praise (Reddit, HN, Twitter, G2, Capterra)
   - The category/market the product operates in
   - Adjacent products that partially solve the same jobs

### Phase 2: Multi-Agent Analysis

Launch **four parallel agents**, each analyzing from a different angle. Each agent should do its own web research and codebase reading as needed.

#### Agent 1: Functional Jobs Analyst
Analyze the **functional dimension** — what is the user trying to get done?
- What specific tasks does this product enable?
- Which of these tasks are high-frequency and high-stakes?
- For each key task: what do people use today if this product doesn't exist? How painful is the workaround?
- Where is the functional gap widest between this product and alternatives?

#### Agent 2: Emotional Jobs Analyst
Analyze the **emotional dimension** — how does the user want to feel?
- What anxiety or frustration does this product relieve?
- What confidence or peace of mind does it create?
- What emotional jobs are competitors completely ignoring?
- Is there an emotional need so acute that people will tolerate a worse functional product just to have it met?

#### Agent 3: Social Jobs Analyst
Analyze the **social dimension** — how does the user want to be perceived?
- Does using this product signal something about the user (competence, taste, values)?
- Does it change how others interact with or perceive the user's work?
- Are there social costs to NOT using it (falling behind, looking outdated)?
- Is there a social dynamic (team adoption, network effects) that makes switching away painful?

#### Agent 4: Competitive Moat Analyst
Analyze the **substitutability dimension** — why can't someone just use something else?
- Map every serious alternative (direct competitors, adjacent tools, manual workarounds, doing nothing)
- For each alternative: what does it do well? Where does it fall short?
- What would a user lose by switching away from this product?
- Is there structural lock-in (data, integrations, learning curve) or is it purely about capability?
- What emerging competitors or trends could erode the current position?

### Phase 3: Synthesis — The Indispensable Need

After all four agents report back, synthesize their findings into a single, sharp insight.

The synthesis must be **candid** — not cheerleading, not diplomatic. If the product doesn't have an indispensable need yet, say so clearly and explain what it would take to get one.

## Output Format

```
## Product Understanding
[2-3 sentences: what this product is and who it's for]

## Competitive Landscape
[Brief map of alternatives — what exists, what's gaining traction, what's declining]

## Functional Analysis
[Key functional jobs and how well-served they are by alternatives]

## Emotional Analysis
[Key emotional jobs — what feelings are at stake]

## Social Analysis
[Key social jobs — how usage affects perception and relationships]

## Substitutability Analysis
[How easy/hard it is to replace this product, and why]

---

## The Indispensable Need

**[One sentence: the indispensable need, stated clearly]**

[2-3 paragraphs explaining:]
- Why this specific need is the one that matters most
- Why alternatives fail to meet it (the substitution gap)
- What makes this insight non-obvious

## The Secret Insight

**[One sentence: the strategic implication — the thing to build around]**

[1-2 paragraphs: what this means for product decisions — what to double down on, what to stop doing, and what moat this creates if executed well]

## Candid Assessment

**Current indispensability: [High / Medium / Low / Not yet]**

[Honest evaluation: does this product currently own an indispensable need, or is it still searching for one? What's the biggest risk to its position?]
```

## Key Principles

- **Candor over comfort.** The whole point is to find truth, not to validate. If the product is a commodity, say so.
- **Specificity over abstraction.** "Users need it for their workflow" is useless. "Solo consultants use it to generate SOWs in 10 minutes instead of 2 hours, and no competitor handles variable pricing structures" is useful.
- **One need, not five.** The goal is to find THE indispensable need — the single strongest one. Mention others but commit to one.
- **Evidence over intuition.** Every claim should be grounded in competitive research, user signals, or observable product behavior.
- **Creative angles welcome.** The best insights come from unexpected frames — looking at the problem through the lens of a different industry, a different user segment, or a counterintuitive tradeoff.

## File Map

```
indispensable-need/
  SKILL.md                          # This file — core instructions
  gotchas.md                        # Failure patterns
  references/jtbd-framework.md      # Jobs to Be Done analysis framework and examples
```
