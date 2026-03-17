---
name: elixir-simplifier
description: Simplifies and refines Elixir/Phoenix/LiveView code for clarity, consistency, and maintainability. Applies KISS principles, proper Phoenix patterns, and idiomatic Elixir. Use when reviewing or refactoring Elixir code.
---

# Elixir/LiveView Code Simplifier

Expert Elixir code simplification focused on **removing duplicate code** and enhancing clarity, consistency, and maintainability while preserving exact functionality.

## File Map

| File | What it contains | When to read |
|------|-----------------|--------------|
| `references/code-examples.md` | Before/after examples for DRY extraction (helpers, components, queries, slots) | When removing duplicate code |
| `references/elixir-patterns.md` | Pattern matching, pipelines, with statements, guard clauses | When simplifying Elixir idioms |
| `references/liveview-patterns.md` | Assign pipelines, handle_event patterns, streams | When simplifying LiveView code |
| `gotchas.md` | Common failure patterns | When something goes wrong |

## Core Principles

### 1. Remove Duplicate Code (DRY)
This is the primary focus. Actively search for and eliminate:
- Repeated code blocks across functions
- Similar logic in multiple LiveView modules
- Copy-pasted template fragments
- Duplicated queries or data transformations

### 2. Preserve Functionality
- Never change what the code does - only how it does it
- All original features, outputs, and behaviors must remain intact
- If unsure about behavior impact, ask before changing

### 3. KISS - Keep It Simple
- Prefer straightforward solutions over clever ones
- Avoid over-engineering and unnecessary abstractions
- One function should do one thing well
- If a function is getting long, refactor into smaller private functions

### 4. LiveView Over JavaScript
- Always prefer LiveView's capabilities over JavaScript
- Only use JavaScript hooks when LiveView absolutely cannot handle it
- Use `phx-*` bindings instead of custom JS event handlers
- Prefer server-side state management

### 5. Phoenix Patterns
- **NEVER** put Repo calls in `_web` modules - always use context modules
- Follow the Phoenix context pattern strictly
- Keep controllers thin, contexts rich
- SQL and Repo calls belong in context modules only

### 6. Template Syntax
- Use new `{}` HEEx syntax over `<%= %>` when possible
- Example: `{@user.name}` instead of `<%= @user.name %>`
- Keep templates clean and logic-free

### 7. No Hardcoded Colors
- Never use inline color hex codes like `bg-[#4f46e5]`
- Use Tailwind's named colors or CSS variables
- Define custom colors in `tailwind.config.js` if needed

### 8. No Fallbacks
- Do not add defensive fallbacks that mask errors
- Let it crash - fail fast with clear errors
- If something unexpected happens, surface it immediately
- Prompt before adding any fallback behavior

## What NOT to Do

1. **Don't add Logger unless needed** - Only add logging where it provides value
2. **Don't add type specs everywhere** - Add them where they clarify complex functions
3. **Don't over-document** - Code should be self-documenting; comments for "why", not "what"
4. **Don't create abstractions for single use** - Wait until you have 3+ similar patterns
5. **Don't add error handling for impossible states** - Trust your types and patterns

## Refinement Process

1. **Read the code** - Understand what it does before suggesting changes
2. **Identify violations** - Check against the principles above
3. **Suggest minimal changes** - Only what's needed, no scope creep
4. **Verify compilation** - Run `mix compile` after changes
5. **Run tests** - Ensure `mix test` still passes

## When to Use

Invoke `/elixir-simplifier` when:
- **Finding and removing duplicate code** across modules
- Reviewing recently written Elixir/Phoenix/LiveView code
- Extracting repeated patterns into shared components or functions
- Refactoring existing code for clarity
- Checking if code follows Phoenix patterns

See `references/` for before/after code examples for each pattern type.
