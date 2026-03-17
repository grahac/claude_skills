# Prompt Cache Optimizer Gotchas

Common failure patterns. Update this file every time something goes wrong.

## 1. Assuming data is static without confirming
**Problem:** Classifying something as "project static" that actually changes per request (e.g., a file the user edits frequently being read into the system prompt).
**Fix:** Always present classifications to the user and get confirmation before generating fixes. Step 4 exists for a reason — never skip it.

## 2. Moving dynamic data out of system prompt but into the wrong place
**Problem:** Moving a timestamp out of the system prompt but putting it as the first user message, which still breaks the prefix for all subsequent messages.
**Fix:** Dynamic data should go at the END of the message flow, not the beginning. Append it to tool results or as a `<system-reminder>` in the latest user turn.

## 3. Breaking tool functionality while fixing cache
**Problem:** Removing a PreToolUse hook's dynamic injection without realizing the agent depends on that data being available at tool-use time.
**Fix:** Understand what each hook does before changing it. Move the injection point (e.g., to PostToolUse) rather than removing it entirely.

## 4. Not checking tool definition order stability
**Problem:** Tools are sorted in code but the sort key changes between requests (e.g., sorting by last-updated timestamp instead of name).
**Fix:** Always sort by a stable, deterministic key like tool name. Verify the tool list is identical between consecutive requests.

## 5. Recommending model switching when the user needs it
**Problem:** Telling the user to stop switching models mid-session when their use case genuinely requires different models for different sub-tasks.
**Fix:** Recommend the subagent pattern — keep the main session on one model, spin up independent calls with fresh context for sub-tasks on cheaper models.
