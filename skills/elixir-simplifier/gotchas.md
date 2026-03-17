# Elixir Simplifier Gotchas

Common failure patterns. Update this file every time something goes wrong.

## 1. Over-abstracting shared code too early
**Problem:** Extracting a shared helper after seeing only 2 similar usages, then the implementations diverge and the abstraction becomes a burden.
**Fix:** Wait until you have 3+ genuinely identical patterns before extracting. Two is a coincidence, three is a pattern.

## 2. Breaking `use` macro compilation order
**Problem:** Extracting common LiveView handlers into a `__using__` macro that references functions not yet defined in the using module.
**Fix:** Always include `defoverridable` for any callbacks defined in macros. Test compilation after extraction.

## 3. Changing behavior while simplifying
**Problem:** Refactoring a `case` into pattern-matched function heads that subtly change the match order or miss a clause.
**Fix:** Ensure every original clause is covered. Run `mix test` after every change. When in doubt, keep the original structure.

## 4. Moving Repo calls but not the imports
**Problem:** Moving a query from a web module to a context module but forgetting to add `import Ecto.Query` in the context.
**Fix:** After moving any Repo/query code, always verify the destination module has the necessary imports. Run `mix compile`.

## 5. Replacing `<%= %>` with `{}` in non-HEEx templates
**Problem:** Using `{}` syntax in EEx templates (non-HEEx) or in `~E` sigils where it's not supported.
**Fix:** Only use `{}` syntax in `.heex` files and `~H` sigils. Check the file extension before suggesting the change.
