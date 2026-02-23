# Prompt Cache Anti-Patterns and Fixes

## Anti-Pattern 1: Timestamp in System Prompt

**Problem:** Any change to the system prompt invalidates the entire cache.

```python
# BEFORE — breaks cache every request
system = f"""You are a helpful assistant.
Current time: {datetime.now().isoformat()}
Instructions: ..."""
```

```python
# AFTER — cache the static system prompt, inject time via messages
system = """You are a helpful assistant.
Instructions: ..."""

# In the first user message or as a system-reminder:
messages = [
    {"role": "user", "content": f"<system-reminder>Current time: {datetime.now().isoformat()}</system-reminder>\n{user_input}"}
]
```

---

## Anti-Pattern 2: Dynamic Data in Hook Injection

**Problem:** Hooks that inject frequently-changing data via `PreToolUse` into the system prompt or early messages break prefix caching.

```json
// BEFORE — hook reads a changing file on every tool use
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{"type": "command", "command": "cat /tmp/current_context.json"}]
    }]
  }
}
```

```json
// AFTER — inject dynamic context only in PostToolUse or as a message reminder
// OR: if it must be PreToolUse, put it at the END of the message, not the start
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{"type": "command", "command": "cat /tmp/current_context.json"}]
    }]
  }
}
```

**Rule:** Hook output injected into messages is fine. Hook output that modifies the system prompt header is a cache breaker.

---

## Anti-Pattern 3: Non-Deterministic Tool Order

**Problem:** If tool definitions are built from a dynamic source (DB, plugin list) with non-deterministic order, the prefix changes between requests.

```python
# BEFORE — dict ordering or DB query order is not guaranteed
tools = {tool.name: tool.schema for tool in db.query(Tool).all()}
```

```python
# AFTER — always sort tools by a stable key
tools = sorted(
    [tool.to_schema() for tool in db.query(Tool).order_by(Tool.name).all()],
    key=lambda t: t["name"]
)
```

---

## Anti-Pattern 4: Adding/Removing Tools Mid-Session

**Problem:** Changing the tool set breaks the cache for the entire session.

```python
# BEFORE — removing tools based on mode
if plan_mode:
    tools = [t for t in all_tools if t["name"] in READ_ONLY_TOOLS]
else:
    tools = all_tools
```

```python
# AFTER — keep ALL tools always, use a tool or message to signal mode
# Option A: Add an EnterPlanMode / ExitPlanMode tool (like Claude Code does)
tools = all_tools  # never changes

# When entering plan mode, send a message instead of changing tools:
messages.append({
    "role": "user",
    "content": "<system-reminder>You are now in plan mode. Explore and plan only — do not edit files. Call exit_plan_mode when done.</system-reminder>"
})
```

---

## Anti-Pattern 5: Switching Models Mid-Session

**Problem:** Each model has its own cache. Switching models means rebuilding the entire prefix cache.

```python
# BEFORE — switches to cheaper model for "easy" questions
model = "claude-haiku-4-5" if is_simple_question(query) else "claude-opus-4-6"
```

```python
# AFTER — keep the same model for the session, use subagents for model switching
# If you need a cheaper model for a sub-task, pass a handoff message:
response = client.messages.create(
    model="claude-opus-4-6",  # main session model — never changes
    messages=messages
)

# For sub-tasks, create a NEW independent call (subagent pattern):
sub_response = client.messages.create(
    model="claude-haiku-4-5",
    system="You are a summarizer.",  # fresh, short context — no cache sharing needed
    messages=[{"role": "user", "content": f"Summarize: {data}"}]
)
```

---

## Anti-Pattern 6: Missing cache_control Breakpoints

**Problem:** Without explicit breakpoints, auto-caching may not cache where you expect, and you lose fine-grained control.

```python
# BEFORE — no cache breakpoints, relying entirely on auto-caching
response = client.messages.create(
    model="claude-opus-4-6",
    system=long_system_prompt,
    messages=messages
)
```

```python
# AFTER — explicit cache_control at the stable prefix boundary
response = client.messages.create(
    model="claude-opus-4-6",
    system=[
        {
            "type": "text",
            "text": static_base_instructions,
            "cache_control": {"type": "ephemeral"}  # cache this stable prefix
        },
        {
            "type": "text",
            "text": project_context,              # changes per project
            "cache_control": {"type": "ephemeral"}  # cache within project
        },
        {
            "type": "text",
            "text": session_context               # changes per session, no breakpoint
        }
    ],
    messages=messages
)
```

**Ordering rule:** `globally static` → `project static` → `session static` → `dynamic` (in messages)

---

## Anti-Pattern 7: Compaction/Summarization with Different Prefix

**Problem:** Running a summarization call with a different system prompt burns the cached tokens from the main conversation.

```python
# BEFORE — summary call has different system prompt, no cache hit
summary = client.messages.create(
    model="claude-opus-4-6",
    system="You are a summarizer.",  # different prefix = cache miss on all prior messages
    messages=[{"role": "user", "content": f"Summarize this conversation: {full_history}"}]
)
```

```python
# AFTER — use the SAME system prompt, append summary request as new message
summary = client.messages.create(
    model="claude-opus-4-6",
    system=main_session_system_prompt,  # identical to main session = cache hit
    messages=main_session_messages + [  # same history prefix
        {"role": "user", "content": "Please summarize our conversation so far in 500 words."}
    ]
)
```

---

## Hook Output Injection Patterns

### Safe: Inject into tool result content
Hook output appended to tool results does not affect the cached prefix.

### Safe: Inject as `<system-reminder>` in next user message
```bash
# Hook script that appends a reminder to next user turn
echo "<system-reminder>$(cat /tmp/context_update.txt)</system-reminder>"
```

### Unsafe: Hook modifies a file that's read into the system prompt
If a hook writes to a file that your app reads into the system prompt header, it breaks the cache on the next turn.

---

## cache_control Reference

The `cache_control` field goes on the **last** content block you want cached:

```python
# For system prompt arrays — mark the last stable block
{"type": "text", "text": "...", "cache_control": {"type": "ephemeral"}}

# For messages — mark the last message you want as a cache boundary
messages = [
    {"role": "user", "content": [
        {"type": "text", "text": long_document, "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": "Now answer: " + question}
    ]}
]
```

- `"type": "ephemeral"` — cache for 5 minutes (default; refreshed on each hit)
- Minimum cacheable size: ~1024 tokens (Claude 3.5+), ~2048 tokens (Claude 3.0)
- Cache is model-specific — switching models = cache miss
