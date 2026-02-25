---
name: hyperslide
description: Build beautiful single-file HTML slide deck presentations with scroll-snap navigation, animated slide counter, and polished design. Use when user asks to "create a presentation", "make slides", "build a slide deck", "present this code", "make an HTML presentation", "turn this into slides", or wants to present any content (code analysis, business problem, project pitch, technical architecture, research findings) as a visual deck. Generates a self-contained .html file — no PowerPoint, no external tools needed.
---

# HyperSlide

Generate a polished, self-contained HTML presentation. Each presentation is a single `.html` file with scroll-snap full-screen slides, a fixed slide counter, keyboard navigation, and a nav arrow.

See `assets/example.html` for a complete working reference (coffee-themed, 9 slides).
See `references/html-structure.md` for the required HTML/CSS/JS patterns.

## Phase 1: Brief

Ask the user two questions (can be combined in one message):

1. **Content** — What should the presentation cover? Accept any of:
   - Free-form description ("I want to present our Q3 results")
   - Code/files to analyze ("analyze this repo and make slides about the architecture")
   - A problem statement ("here's our product problem, make a pitch deck")
   - Slide-by-slide narration ("slide 1: title, slide 2: the problem we solve...")

2. **Style** — Do they have a website whose visual style they'd like to draw from?
   - If yes: fetch/browse the URL and extract the color palette, font personality, and vibe
   - If no: ask for a mood (e.g., "minimal & editorial", "bold & techy", "warm & approachable") — then generate a fresh palette

Do NOT ask for exact colors or fonts. You will derive these.

## Phase 2: Design

From the style reference (URL or mood description), generate:
- A `--dark-bg` and `--light-bg` (the two slide backgrounds)
- An `--accent` color
- Card and border colors derived from the palette
- A Google Font pairing that fits the vibe (single family, 2–3 weights)
- An optional SVG background texture for dark slides (inline data URI, 2–5% opacity)

Rules:
- Never copy a site's layout — extract only its color language and typographic personality
- Never hardcode hex values in layout CSS — always use `var(--x)`
- Palette must have sufficient contrast (WCAG AA minimum)

## Phase 3: Structure

Plan the slides based on the content brief. Standard narrative arc:

1. **Title** — Brand/project name, one-line descriptor
2. **Problem / Context** — Stats, current pain points
3. **Vision / Solution** — What you're building and why
4. **How It Works** — Process flow, architecture, or method
5. **Big Statement** — A single powerful number or insight
6. **Data / Evidence** — Charts, breakdowns, comparisons
7. **Detail / Deep Dive** — Technical or operational specifics
8. **Roadmap** — Phases, milestones, timeline
9. **CTA / Close** — Call to action, contact, next steps

Adjust this arc for the content type:
- Code architecture: problem → current structure → pain points → proposed structure → benefits → migration path → close
- Pitch deck: hook → problem → solution → market → product → traction → ask
- Research: question → method → findings → implications → recommendations

Each slide needs: a `slide-label` (eyebrow text), a headline, and supporting content.

## Phase 4: Generate

Write the complete single-file HTML. Requirements:
- All CSS in a `<style>` block in `<head>` — no external stylesheets
- All JS in a `<script>` block before `</body>` — no external libraries
- Google Fonts loaded via `<link>` tag
- SVG background textures as inline data URIs
- Charts as pure CSS div-based bars (no Chart.js, no D3)
- Diagrams as SVG or styled HTML — no canvas
- File saved as `[topic]-presentation.html` in the current working directory

Follow the patterns in `references/html-structure.md` exactly for:
- Scroll-snap mechanics
- Slide counter
- Nav arrow (hides on last slide)
- Keyboard navigation (ArrowDown/Up, Space, PageDown/Up)
- CSS custom properties structure

## Phase 5: UX Review (if agent-browser is available)

After generating the file, check if `npx agent-browser` is available:

```bash
which npx && npx agent-browser --version 2>/dev/null
```

If available, open the file in a browser and review each slide:

```bash
npx agent-browser
# Navigate to: file:///path/to/presentation.html
# Take a snapshot of each slide
# Check: Does it look beautiful? Are there overflow issues? Is text readable?
```

Report any visual issues found and fix them before delivering.

If agent-browser is not available, skip silently — do not mention it to the user.

## Phase 6: Audit

Before delivering, self-audit against this checklist:

**Design**
- [ ] Dark and light slides genuinely alternate (not all one color)
- [ ] Accent color appears consistently on labels, stats, and highlights
- [ ] Typography uses `clamp()` for all headings
- [ ] Cards have consistent border-radius and border style
- [ ] No slide feels empty — every slide has a visual element beyond text

**Content**
- [ ] Slide 1 is a strong title slide with a clear one-line descriptor
- [ ] At least one "big statement" slide (large number or bold claim)
- [ ] Bullet points are concise (max 8 words per bullet)
- [ ] The narrative has a clear arc with a strong closing slide

**Technical**
- [ ] Slide counter reads "X / N" correctly
- [ ] Nav arrow is hidden on the last slide
- [ ] Keyboard navigation works
- [ ] File is self-contained (no broken external links)

Fix any failures before delivering.

## Delivery

Tell the user:
- The filename and path
- How many slides were generated
- How to navigate: scroll, arrow keys, or the nav button
- Any design choices you made (palette source, font choice)
