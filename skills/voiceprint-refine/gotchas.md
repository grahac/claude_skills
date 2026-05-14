# Voiceprint Refine — Gotchas

## Summarizing the voiceprint back to the user
Don't recap the file before asking what to refine. The user knows what's in it —
they're here because something specific felt wrong in practice. Go straight to the
question.

## Over-broad category expansion
When a user says "add X to my ban list", don't silently expand to a full category.
Ask first. They may want only the specific phrase; expanding the category might
block things they actually use.

## New exemplar contradicts existing ban list
If the user pastes a sample that contains a phrase already in Section 1, flag it
before adding. Don't silently add an exemplar that the ban list would prohibit — that
creates a contradiction the runtime can't resolve.

## Editing without confirming
Always summarize the planned changes in Step 3 and get a yes before touching the file.
"Fix my voiceprint" is not specific enough to act on.

## Replacing a section instead of amending it
Unless the user explicitly asked to remove something, add to the existing content.
Replacing a section silently discards patterns that were validated in the original
creator run.

## Updating version comment
Don't change the `<!-- voiceprint-version: ... -->` comment. It reflects what template
version the file was built with, not whether it's been refined. Only `/voiceprint-creator`
should set this.

## Pre-v1.0 files (no version comment)
These were built before versioning was added. Don't block the user — refine normally.
Optionally mention they can rerun `/voiceprint-creator` to regenerate with the full
new structure (sentence metrics, exemplars, transformations) if they want.
