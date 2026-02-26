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

**Commit to a BOLD aesthetic direction first.** Pick one and execute it with conviction — the worst result is a timid middle ground:
- **Editorial/Magazine**: large italic display type, strong vertical rhythm, high contrast
- **Luxury/Refined**: tight tracking, generous whitespace, subtle textures, restrained palette
- **Energetic/Techy**: gradient fills, sharp geometric shapes, dynamic grid
- **Warm/Organic**: earth tones, soft curves, generous roundness
- **Brutalist/Raw**: off-grid placement, unexpected color, unapologetic weight

From the style reference (URL or mood description), generate:
- A `--dark-bg` and `--light-bg` (the two slide backgrounds)
- An `--accent` color
- Card and border colors derived from the palette
- Atmospheric backgrounds: gradient meshes, layered SVG textures, or noise — never plain solid fills
- A **two-font pairing**: a distinctive display font for headings + a refined readable body font

**Font rules:**
- NEVER use Inter, Roboto, Arial, or system fonts — they are generic and forgettable
- Display font options (choose one that fits the aesthetic): Fraunces, Cormorant Garamond, Playfair Display, Syne, Clash Display, Bebas Neue, Instrument Serif, Radio Canada Big, Libre Baskerville
- Body font options: DM Sans, Plus Jakarta Sans, Outfit, Manrope, Lato, Literata, Source Serif 4
- Load both via Google Fonts with the weights needed (300, 500/600, 700 for display; 400, 500 for body)

**Contrast rules:**
- Body text: minimum 4.5:1 contrast ratio against its background (WCAG AA)
- `--text-dark-body` is a common failure point — muted colors often fail; verify the value
- Large headings (≥24px bold): minimum 3:1 is acceptable but 4.5:1 is preferred
- Never rely on light gray body text on white — it almost always fails

Rules:
- Never copy a site's layout — extract only its color language and typographic personality
- Never hardcode hex values in layout CSS — always use `var(--x)`

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
- Google Fonts loaded via `<link>` tag (both display and body fonts)
- Atmospheric backgrounds: gradient meshes or layered SVG textures as inline data URIs — never plain solid fills on dark slides
- Charts as pure CSS div-based bars (no Chart.js, no D3)
- Diagrams as SVG or styled HTML — no canvas
- File saved as `[topic]-presentation.html` in the current working directory

**Slide entry animations are required.** Every slide must animate its content in when it becomes visible:
- Use `IntersectionObserver` to add an `.is-visible` class when a slide enters the viewport
- Default state: `opacity: 0; transform: translateY(28px)`
- Animated state: `opacity: 1; transform: translateY(0)` over 0.55s with `cubic-bezier(0.16, 1, 0.3, 1)` easing
- Stagger direct child elements with 80–120ms `animation-delay` increments
- Reset animation when slide leaves view so it replays on revisit

Follow the patterns in `references/html-structure.md` exactly for:
- Scroll-snap mechanics
- Slide counter
- Nav arrow (hides on last slide)
- Keyboard navigation (ArrowDown/Up, Space, PageDown/Up)
- CSS custom properties structure
- Animation and font pairing patterns

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
- [ ] Committed to a single bold aesthetic direction — not a timid middle ground
- [ ] Dark slide backgrounds have atmospheric depth (gradient mesh or layered texture), not plain solid fills
- [ ] Accent color appears consistently on labels, stats, and highlights
- [ ] Two distinct fonts: a display font for headings and a body font for prose (never Inter/Roboto/Arial)
- [ ] Typography uses `clamp()` for all headings — title slides at least `clamp(44px, 6.5vw, 80px)`
- [ ] Body/prose text is 15px minimum — never 12–13px for paragraph content
- [ ] Cards have consistent border-radius and border style
- [ ] No slide feels empty — every slide has a visual element beyond text

**Contrast & Readability**
- [ ] Body text (dark slides): `--text-dark-body` passes 4.5:1 contrast against `--dark-bg`
- [ ] Body text (light slides): `--text-light-body` passes 4.5:1 contrast against `--light-bg`
- [ ] Slide labels (uppercase eyebrow text) pass 3:1 minimum — accent color on dark bg commonly fails this

**Animation**
- [ ] Every slide has an `.is-visible` triggered entry animation
- [ ] Children stagger with 80–120ms delays (not all at once)
- [ ] Animations reset when slide leaves view (replay on revisit)

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
