---
name: prompt-cache-optimizer
description: Audit and optimize AI/LLM API calls and Claude Code hooks for prompt caching efficiency. Use when the user wants to reduce AI API costs, improve response latency, review hooks for cache-breaking patterns, or optimize system prompt structure. Triggers on "optimize prompt caching", "reduce AI costs", "review hooks for caching", "cache hit rate", "prompt cache audit", or "optimize my AI calls".
---

# Prompt Cache Optimizer

Audit hooks and AI API calls for prompt caching anti-patterns, then produce concrete fixes that maximize cache hit rate.

## Core Principle

Prompt caching is prefix matching — the API caches everything from the start of the request up to each `cache_control` breakpoint. Any change in the prefix breaks the cache for everything after it.

**Optimal ordering:** `static system prompt + tools` → `project context (CLAUDE.md)` → `session context` → `conversation messages`

See `references/anti-patterns.md` for detailed patterns and code examples.

## Workflow

### Step 1 — Scan for hooks

Scan these locations for hooks:

```bash
cat ~/.claude/settings.json 2>/dev/null
cat .claude/settings.json 2>/dev/null
cat .claude/settings.local.json 2>/dev/null
```

For each hook found, identify:
- **Event type**: `PreToolUse`, `PostToolUse`, `Notification`, `Stop`, `SubagentStop`
- **Command**: what script or inline command runs
- **Output**: what data the hook injects into messages (read the script if needed)

### Step 2 — Scan for AI API calls

Search the project for LLM/AI API usage:

```bash
# Anthropic SDK
grep -r "messages\.create\|anthropic\|chat_completion\|system_prompt\|cache_control" --include="*.py" --include="*.ts" --include="*.js" --include="*.ex" --include="*.exs" -l .

# OpenAI-style
grep -r "openai\|ChatCompletion\|chat\.completions" --include="*.py" --include="*.ts" --include="*.js" -l .

# LangChain / generic
grep -r "langchain\|llm\.\|LLM\|SystemMessage\|HumanMessage" --include="*.py" -l .
```

Read any matching files to understand how system prompts and tool definitions are constructed.

### Step 3 — Classify what you found

For each hook and AI call, classify every data element being injected as:

| Classification | Examples | Cache impact |
|---|---|---|
| **Globally static** | Base instructions, persona, tool schemas | Safe in system prompt |
| **Project static** | CLAUDE.md, repo structure, DB schema | Safe with `cache_control` breakpoint |
| **Session static** | User name, project path, auth token | Safe once per session with `cache_control` |
| **Frequently dynamic** | Timestamps, current file contents, env vars, request data | **CACHE BREAKER** — must move to messages |
| **Per-turn dynamic** | Tool results, conversation history | Already in messages (fine) |

Make your best guess at each element's classification before asking the user. Common patterns to flag automatically:
- `datetime.now()`, `Date.now()`, `Time.now`, `new Date()`, `DateTime.utc_now()` → frequently dynamic
- `current_user`, `user.id`, `session.id` → session static (ok once, bad if regenerated)
- File reads in hooks that read files the user might edit → frequently dynamic
- `ENV["..."]`, `process.env.X`, `System.get_env/1` → check if it changes per request
- Tool lists built from dynamic sources (DB queries, plugin lists) → check if order is deterministic

### Step 4 — Confirm with user

Present your classification as a table and ask the user to confirm or correct before generating fixes:

```
I found the following data being injected into your AI prompts. Please confirm
whether my classification is correct — this determines what can be safely cached:

| Data | Location | My guess | Confirm? |
|---|---|---|---|
| Current timestamp | hooks/log.sh → PreToolUse | Frequently dynamic ❌ | [y/n] |
| CLAUDE.md content | system prompt | Project static ✅ | [y/n] |
| Tool list from DB | my_agent.py:45 | Check: is order deterministic? | [y/n] |
```

Do not proceed to fixes until the user has confirmed the classification.

### Step 5 — Generate report

Produce a report with:

```
# Prompt Cache Audit Report
Date: [date]

## Summary
- Hooks reviewed: N
- AI call sites: N
- Cache-breaking issues found: N critical, N warnings

## Critical Issues (break cache every request)
[List each with file:line, what it does, and exact fix]

## Warnings (potential cache fragility)
[List each with recommendation]

## Recommendations
[Prioritized list of changes, highest impact first]
```

For each issue, provide a concrete before/after code fix. See `references/anti-patterns.md` for fix templates.

### Step 6 — Offer to apply fixes

After the report, ask which fixes the user wants applied. Apply them surgically — only change what's needed to fix the cache issue.

## Key Rules

- **Never silently assume** — always confirm dynamic vs static classification with the user
- **One fix at a time** — apply changes surgically, don't refactor surrounding code
- **Hooks are highest priority** — hooks that run on every `PreToolUse` and inject dynamic data are the most damaging
- **Order matters** — static before dynamic, always

## References

- Anti-patterns and code fix templates: `references/anti-patterns.md`
