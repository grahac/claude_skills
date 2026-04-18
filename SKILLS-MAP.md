# Skills Map

Quick reference for where everything lives. 13 skills across 5 categories.

## Skill Directory Convention

Every skill follows this structure:
```
skill-name/
  SKILL.md              # When to use, core instructions, file map
  gotchas.md            # Failure patterns — update when things go wrong
  references/           # Detailed examples, checklists, criteria (read on demand)
  assets/               # Templates, starter files, reusable formats
  scripts/              # Executable scripts (Python, etc.)
```

## Product & Marketing

### hyperslide `/hyperslide`
Single-file HTML slide decks. No PowerPoint.
```
hyperslide/
  SKILL.md
  gotchas.md
  references/html-structure.md    # Required HTML/CSS/JS patterns
  assets/example.html             # Complete working reference (coffee-themed, 9 slides)
```

### website-extractor `/website-extractor`
Extract content + design from a site for rewrite.
```
website-extractor/
  SKILL.md
  gotchas.md
  references/extraction-format.md # Structured output format for the extraction document
```

### marketing-copywriter `/marketing-copywriter`
Conversion-focused copy for landing pages, emails, ads.
```
marketing-copywriter/
  SKILL.md
  gotchas.md
  references/copy-types.md        # Templates by format (headlines, email, ads, CTAs)
  references/frameworks.md        # AIDA, PAS, Before/After/Bridge
  references/voice-tone.md        # Tone calibration examples
  references/avoid-ai-patterns.md # AI words/patterns to avoid — check every time
  assets/copy-brief-template.md   # Fill out before writing any copy
```

### innovate `/innovate`
One bold, non-obvious addition to any plan.
```
innovate/
  SKILL.md
  gotchas.md
```

### nanobanana `/nanobanana`
Structured image generation via Gemini API.
```
nanobanana/
  SKILL.md
  gotchas.md
  requirements.txt
  scripts/nanobanana_generate.py  # Image generation script (requires GEMINI_API_KEY)
```

### appstore-images `/appstore-images`
App Store preview generator — iPhone, iPad, Mac with device mockups, gradients, and headline text.
```
appstore-images/
  SKILL.md
  fonts/                          # 7 bundled font presets (Montserrat, Oswald, Bebas, Anton, Archivo, MonaSans, Fredoka)
  scripts/appstore_preview.py     # Generates a single preview from a screenshot + flags
  scripts/requirements.txt        # Pillow
```

## Development

### elixir-simplifier `/elixir-simplifier`
Remove duplicate code, simplify Elixir/Phoenix/LiveView.
```
elixir-simplifier/
  SKILL.md
  gotchas.md
  references/code-examples.md     # DRY extraction examples (helpers, components, queries, slots)
  references/elixir-patterns.md   # Pattern matching, pipelines, with, guards
  references/liveview-patterns.md # Assign pipelines, handle_event, streams
```

### prompt-cache-optimizer `/prompt-cache-optimizer`
Audit AI API calls and hooks for caching anti-patterns.
```
prompt-cache-optimizer/
  SKILL.md
  gotchas.md
  references/anti-patterns.md     # 7 anti-patterns with before/after code fixes
```

### changelog `/changelog`
Keep a Changelog 1.1.0 spec maintenance.
```
changelog/
  SKILL.md
  gotchas.md
  references/format-example.md    # Full markdown template + comparison link format
  references/commit-categories.md # Heuristics for mapping commits to change types
  assets/changelog-template.md    # Starter CHANGELOG.md for new projects
```

## Productivity

### granola-scoop `/granola-scoop`
Extract meeting notes from Granola's local cache.
```
granola-scoop/
  SKILL.md
  gotchas.md
  scripts/extract.py              # Extraction script (reads Granola cache)
```

## Security

### security-audit-skills `/security-audit-skills`
Audit Claude Code config for security issues.
```
security-audit-skills/
  SKILL.md
  gotchas.md
  references/scan-locations.md    # All config paths to check
  references/security-criteria.md # Check criteria by severity
  assets/report-template.md       # Audit report output format
  assets/ignore-entry-template.md # Format for ignore list entries
```

## Strategy

### indispensable-need `/indispensable-need`
Multi-agent JTBD analysis to find a product's indispensable need — the high-stakes job with no good substitute.
```
indispensable-need/
  SKILL.md
  gotchas.md
  references/jtbd-framework.md     # Jobs to Be Done framework, dimensions, examples
```

## Contracts

### contract-manager `/contract-manager`
Multi-agent contract creation, review, and editing.
```
contract-manager/
  SKILL.md
  gotchas.md
  references/agent-personas.md       # Agent definitions + system prompt templates
  references/interview-flows.md      # Interview questions by mode x contract type
  references/dispute-resolution.md   # 3-round debate protocol
  references/nda-checklist.md        # NDA required clauses
  references/engagement-checklist.md # Engagement/consulting required clauses
  references/general-checklist.md    # General contract required clauses
  scripts/generate_docx.py           # JSON -> .docx generation
  scripts/codex_agent.py             # Optional 4th agent (Codex/OpenAI)
  scripts/requirements.txt
  scripts/sample_contract.json
```
