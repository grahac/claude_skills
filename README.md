# Claude Code Skills

A collection of custom skills for [Claude Code](https://claude.ai/claude-code).

## Installation

To use these skills globally across all your Claude Code projects:

```bash
# Clone into your .claude/skills directory
git clone https://github.com/grahac/claude_skills.git ~/.claude/skills/claude_skills

# Or copy individual skills
cp -r skills/elixir-simplifier ~/.claude/skills/
```

## Available Skills

### elixir-simplifier

Simplifies and refines Elixir/Phoenix/LiveView code with a focus on **removing duplicate code**.

**Use when:**
- Finding and removing duplicate code across modules
- Extracting repeated patterns into shared components
- Reviewing recently written Elixir/Phoenix/LiveView code
- Refactoring existing code for clarity
- Checking if code follows Phoenix patterns

**Key principles:**
- DRY - Remove duplicate code (primary focus)
- KISS - Keep it simple
- LiveView over JavaScript
- Phoenix context patterns (no Repo in `_web` modules)
- HEEx `{}` syntax over `<%= %>`
- No hardcoded color hex codes
- No defensive fallbacks - let it crash

**Invoke:** `/elixir-simplifier`

## Contributing

PRs welcome! Add new skills in the `skills/` directory following the existing format.

## License

MIT
