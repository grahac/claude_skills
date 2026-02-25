---
name: website-extractor
description: Extract all content and design information from a website to enable a complete rewrite. Use when the user wants to rewrite, redesign, or create a new version of an existing website. Captures page content, brand identity (colors, fonts, tone), navigation structure, section-by-section copy, CTAs, and visual style. Triggers on "extract this website", "rewrite this site", "create a new version of", "redesign based on", or any request that involves analyzing an existing site before producing new content or code.
---

# Website Extractor

Extract all information needed to rewrite or redesign a website. Output a structured document that a rewrite agent can use directly.

## Workflow

### Step 1 — Open the site and screenshot

```bash
agent-browser open <url>
agent-browser screenshot --full site-full.png
```

Read the screenshot to get an overall visual impression: layout style, color palette, density, imagery approach.

### Step 2 — Get the full accessibility snapshot

```bash
agent-browser snapshot
```

This gives the full content tree: all headings, paragraphs, links, buttons, and labels in document order. Use this as the primary source for text content.

### Step 3 — Get the HTML for design signals

```bash
agent-browser get html
```

Scan the HTML for:
- **Tailwind classes**: color classes like `bg-indigo-600`, `text-gray-900`, `border-blue-500` directly reveal the palette
- **Custom CSS variables**: look for `var(--color-*)` patterns
- **Font references**: `font-family` declarations or Google Fonts `<link>` tags
- **Framework clues**: Next.js, Webflow, WordPress, etc.

### Step 4 — Navigate additional pages (if multi-page)

For each key page (About, Pricing, Features, etc.) visible in the nav:

```bash
agent-browser open <page-url>
agent-browser snapshot
```

Extract content from each page. Note which pages exist.

### Step 5 — Produce the extraction document

Write a structured markdown document following `references/extraction-format.md`.

Save it as `site-extraction.md` in the current directory (or wherever the user specifies).

## Tips

- **Prioritize the snapshot over raw HTML** for content — it's already cleaned up and readable
- **For colors**: Tailwind class names are exact hex values; look them up if needed. For custom CSS, note the variable names and any hex values found in `<style>` tags
- **For tone**: Read the hero and feature copy. Is it formal/casual, technical/approachable, bold/understated?
- **Don't guess colors from screenshots** — always extract from code; screenshots compress colors
- If the site is SPA/JS-rendered and snapshot is empty, scroll first: `agent-browser scroll down 500` then re-snapshot
- If agent-browser isn't installed: `npm install -g agent-browser && agent-browser install`

## Output

The extraction document is the deliverable. Tell the user where it was saved and offer to immediately pass it to a rewrite tool or describe what you found.
