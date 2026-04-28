# plugin-doctor gotchas

## Local source must be the object form

The string form `"source": "./"` (or any string starting with `./`) gets rejected by the schema validator. Always rewrite to:

```json
"source": { "type": "local", "path": "." }
```

This is the single most common cause of "Invalid schema" errors.

## Marketplace name vs plugin slug

`marketplace.json` has TWO `name` fields, and they are usually different:

- Top-level `name` → marketplace name (used in `/plugin install <plugin-slug>@<MARKETPLACE>`)
- `plugins[i].name` → plugin slug (becomes `/<PLUGIN-SLUG>:<command>`)

If the user types `/plugin install plugin@plugin` and the slash command becomes `/plugin:foo`, both fields were left as the placeholder `plugin`. Fix both.

## `/reload-plugins` is not optional

After EVERY install or marketplace update, the user must run `/reload-plugins`. Slash commands from a freshly installed plugin do NOT appear without it. Always end the install flow by reminding them.

## Marketplace update is not the same as install

Editing `marketplace.json` after the marketplace is registered does NOT auto-refresh. Run:

1. `/plugin marketplace update <marketplace-name>`
2. `/plugin install <plugin-slug>@<marketplace-name>` (or reinstall)
3. `/reload-plugins`

Skipping step 1 is why "I edited the file but it's still broken" happens.

## Dev installs leave directories behind

Sometimes `~/.claude/plugins/<plugin-slug>-dev/` or similar leftover directories prevent a clean reinstall. If install errors are confusing, check that directory and remove it.

## Claude Desktop is NOT the same as Claude Code

The CLI plugin model only works in Claude Code (the terminal CLI). If the user is asking about Claude Desktop plugins, this skill doesn't apply — tell them so explicitly rather than walking through marketplace add steps.

## Path must be the directory, not the JSON file

`/plugin marketplace add /path/to/plugin/.claude-plugin/marketplace.json` will fail. Pass the directory ABOVE `.claude-plugin/`, e.g. `/path/to/plugin/`.

## Project vs user scope

`/plugin install` defaults to project scope. For globally-available skills, prompt the user to choose user scope — they often forget and then wonder why the skill is missing in another project.
