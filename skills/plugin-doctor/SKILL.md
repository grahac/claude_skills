---
name: plugin-doctor
description: Diagnose and fix Claude Code plugin/marketplace install problems. Use when the user says "marketplace not found", "/plugin install fails", "Invalid schema", "force install for user", "/reload-plugins isn't working", asks about plugin install failures, or hits any of the recurring install/marketplace edge cases. Walks the add → update → install → reload flow, validates marketplace.json schema, and resolves the common name/slug confusions.
---

# Plugin Doctor

Diagnose Claude Code plugin and marketplace install issues. The recurring failure modes:

1. `marketplace add` errors on schema (e.g. `source: "./"` rejected; needs object form for local).
2. Marketplace name vs plugin name mismatch (`/plugin install plugin@plugin` vs `/plugin install pluginname@marketplacename`).
3. `/reload-plugins` not run after install — slash command doesn't appear.
4. User-scope vs project-scope install confusion.
5. Marketplace updates not pulled in after `marketplace.json` edit.

## Workflow

### Step 1 — Identify which failure mode

Ask the user (or read from their pasted error) which of these matches:

- `Failed to parse marketplace file ... Invalid schema` → **Schema problem.** Go to Step 2.
- `Marketplace ".../plugin" not found` → **Marketplace not registered.** Go to Step 3.
- `/plugin install` runs but slash command doesn't work → **Reload missing.** Go to Step 4.
- Slash command is wrong shape (e.g. `/plugin` instead of `/myplugin`) → **Naming mismatch.** Go to Step 5.
- Was working, now isn't, after editing the plugin → **Stale marketplace.** Go to Step 6.

### Step 2 — Schema validation

The two common mistakes in `.claude-plugin/marketplace.json`:

```json
// WRONG — local source as bare string with trailing slash
{ "name": "x", "source": "./" }

// RIGHT — object form for local same-dir
{ "name": "x", "source": { "type": "local", "path": "." } }
```

Read the file. If `source` is a string starting with `./`, rewrite as the object form. Validate the rest of the schema:

```json
{
  "name": "marketplace-name",
  "owner": { "name": "...", "email": "..." },
  "plugins": [
    {
      "name": "plugin-slug",
      "source": { "type": "local", "path": "." },
      "description": "..."
    }
  ]
}
```

### Step 3 — Re-add the marketplace

```bash
/plugin marketplace add /absolute/path/to/plugin/dir
```

The path must contain `.claude-plugin/marketplace.json`. If "not found" persists:
- Check the path exists and contains `.claude-plugin/marketplace.json`.
- Run `cat /path/.claude-plugin/marketplace.json` and validate as Step 2.
- Try the parent dir if the path points at the marketplace.json file itself.

### Step 4 — Reload after install

After every `/plugin install`, the user must run `/reload-plugins` (or restart the CLI). Tell them this. The slash command from a freshly installed plugin will not appear without it.

### Step 5 — Naming mismatch

Plugin install syntax is `<plugin-slug>@<marketplace-name>`. These are usually different:

- `marketplace.json` top-level `name` = marketplace name (e.g. `cyborgscore`).
- `marketplace.json` `plugins[i].name` = plugin slug (e.g. `cyborgscore`, may match — that's fine).
- Slash command becomes `/<plugin-slug>:<command-name>`.

If user sees `/plugin install plugin@plugin` working but expects `/cyborgscore`, the plugin was likely registered with `name: "plugin"`. Update `marketplace.json` `plugins[0].name` and `name` to the desired slug. Then Step 6.

### Step 6 — Refresh stale marketplace

After editing `marketplace.json`:

```bash
/plugin marketplace update <marketplace-name>
/plugin install <plugin-slug>@<marketplace-name>
/reload-plugins
```

If the marketplace still shows old data, remove and re-add:

```bash
rm -rf ~/.claude/plugins/<plugin-slug>-dev      # if a dev install hangs around
/plugin marketplace remove <marketplace-name>
/plugin marketplace add /path/to/plugin
```

## Install scope

`/plugin install` defaults to project scope. To install for the user globally, run from any directory and accept the user-scope prompt, or pre-set with `~/.claude/settings.json` plugin entries. If unsure, ask the user which scope they want before running install.

## End-to-end verification

After fixing, confirm with the user:

1. `/plugin marketplace list` shows the marketplace.
2. `/plugin list` shows the plugin as installed.
3. The slash command (e.g. `/<plugin-slug>:<command>`) appears in the available skills/commands list after `/reload-plugins`.

If any of these fail, loop back to the matching step.

## What this skill does NOT cover

- Plugin code bugs (skill scripts erroring after install). That's debugging, not installation.
- Claude Desktop installation (the CLI is Claude Code; Desktop's plugin model is separate and unsupported as of this skill's writing).
- Publishing a plugin to a public marketplace.
