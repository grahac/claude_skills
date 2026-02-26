# HyperSlide HTML Structure Reference

## Core Mechanics (required on every presentation)

```html
<!-- Fixed slide counter — top right -->
<div id="slide-counter">1 / N</div>

<!-- Nav arrow — bottom center, hides on last slide -->
<button id="nav-arrow" aria-label="Next slide">
  <svg ...> <!-- down-arrow chevron --> </svg>
</button>

<!-- Scroll container -->
<div class="presentation" id="pres">
  <section class="slide dark" id="slide-1">...</section>
  <section class="slide light" id="slide-2">...</section>
  <!-- alternate dark/light, can repeat pattern -->
</div>
```

## Required CSS

```css
html, body { height: 100%; overflow: hidden; }

.presentation {
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
}

.slide {
  scroll-snap-align: start;
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 48px 64px;
}
```

## CSS Custom Properties Pattern

Always use a `:root` block with these variables (values generated fresh per presentation):

```css
:root {
  --dark-bg: /* primary dark color */;
  --light-bg: /* primary light color, usually white or near-white */;
  --card-dark-bg: /* translucent white, e.g. rgba(255,255,255,0.07) */;
  --card-dark-border: /* translucent white border */;
  --card-light-bg: /* subtle tinted background for cards on light slides */;
  --card-light-border: /* mid-tone border matching the palette */;
  --text-dark-heading: /* near-white */;
  --text-dark-body: /* muted light color — verify 4.5:1 contrast against --dark-bg */;
  --text-light-heading: /* dark, matches --dark-bg or nearby */;
  --text-light-body: /* mid-dark body text — verify 4.5:1 contrast against --light-bg */;
  --accent: /* primary accent/highlight color */;
  --font-display: /* distinctive display font — Fraunces, Cormorant, Syne, Instrument Serif, etc. */;
  --font-body: /* refined body font — DM Sans, Plus Jakarta Sans, Manrope, Literata, etc. */;
}
```

**Font rules:**
- Load both fonts via Google Fonts `<link>` tag with the weights needed
- NEVER use Inter, Roboto, Arial, or system fonts
- Headings always use `var(--font-display)`, body/prose uses `var(--font-body)`
- Display font: 2–3 weights (e.g. 400, 700, 700 italic)
- Body font: 2 weights (400, 500 or 600)

## Typography Scale

All heading sizes use `clamp()`. Push sizes up — presentations are viewed at distance:

```css
/* Title slide headline — the biggest type on screen */
.slide-h1-title {
  font-family: var(--font-display);
  font-size: clamp(44px, 6.5vw, 80px);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.02em;
}

/* Section headings (dark slides) */
.slide-h1-dark {
  font-family: var(--font-display);
  font-size: clamp(36px, 5vw, 64px);
  font-weight: 700;
  color: var(--text-dark-heading);
  line-height: 1.08;
  letter-spacing: -0.015em;
}

/* Section headings (light slides) */
.slide-h1-light {
  font-family: var(--font-display);
  font-size: clamp(32px, 4.5vw, 58px);
  font-weight: 700;
  color: var(--text-light-heading);
  line-height: 1.1;
  letter-spacing: -0.01em;
}

/* Body / supporting text — minimum 15px, never 12–13px for paragraphs */
.slide-h2-dark {
  font-family: var(--font-body);
  font-size: clamp(15px, 2vw, 20px);
  font-weight: 400;
  color: var(--text-dark-body);
  line-height: 1.6;
}

/* Card body, bullets, prose */
.body-text {
  font-family: var(--font-body);
  font-size: 15px; /* never below 15px */
  line-height: 1.55;
}

/* Slide labels — eyebrow text */
.slide-label {
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 12px;
}
```

## Slide Entry Animations (required)

Every slide's content must animate in when it becomes visible. Use IntersectionObserver to add `.is-visible`.

```css
/* Default state: hidden and shifted down */
.slide > * {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.55s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Stagger children when slide becomes visible */
.slide.is-visible > *:nth-child(1) { opacity: 1; transform: none; transition-delay: 0.05s; }
.slide.is-visible > *:nth-child(2) { opacity: 1; transform: none; transition-delay: 0.15s; }
.slide.is-visible > *:nth-child(3) { opacity: 1; transform: none; transition-delay: 0.25s; }
.slide.is-visible > *:nth-child(4) { opacity: 1; transform: none; transition-delay: 0.35s; }
.slide.is-visible > *:nth-child(5) { opacity: 1; transform: none; transition-delay: 0.42s; }
```

```js
// In your JS — add/remove .is-visible as slides enter and leave
const animObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('is-visible');
    } else {
      e.target.classList.remove('is-visible'); // reset so it replays on revisit
    }
  });
}, { root: pres, threshold: 0.4 });

slides.forEach(s => animObserver.observe(s));
```

## Required JavaScript

```js
const pres = document.getElementById('pres');
const counter = document.getElementById('slide-counter');
const arrow = document.getElementById('nav-arrow');
const slides = document.querySelectorAll('.slide');
const total = slides.length;
let current = 0;

function updateUI(idx) {
  current = idx;
  counter.textContent = `${idx + 1} / ${total}`;
  arrow.classList.toggle('hidden', idx >= total - 1);
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) updateUI(Array.from(slides).indexOf(e.target));
  });
}, { root: pres, threshold: 0.6 });

slides.forEach(s => observer.observe(s));

arrow.addEventListener('click', () => {
  if (current < total - 1) slides[current + 1].scrollIntoView({ behavior: 'smooth' });
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
    e.preventDefault();
    if (current < total - 1) slides[current + 1].scrollIntoView({ behavior: 'smooth' });
  }
  if (e.key === 'ArrowUp' || e.key === 'PageUp') {
    e.preventDefault();
    if (current > 0) slides[current - 1].scrollIntoView({ behavior: 'smooth' });
  }
});

updateUI(0);
```

## Atmospheric Backgrounds

Dark slides must have depth — never a plain solid fill. Options:

```css
/* Option A: Gradient mesh (two-tone dark) */
.slide.dark {
  background: radial-gradient(ellipse at 20% 50%, #1a0a2e 0%, #0a0a0a 60%),
              linear-gradient(135deg, #0d1117 0%, #1a0a2e 100%);
}

/* Option B: Layered SVG texture + gradient */
.slide.dark.textured {
  background-image: url("data:image/svg+xml;..."),
    linear-gradient(160deg, var(--dark-bg) 0%, #2a1520 100%);
  background-size: cover, cover;
}

/* Option C: Subtle noise overlay via pseudo-element */
.slide.dark::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,..."); /* fine dot grid or concentric circles */
  opacity: 0.03;
  pointer-events: none;
}
```

Light slides can be flat or very subtly tinted — they need less atmosphere than dark slides.

## Slide Types & Layout Patterns

### Title slide (slide 1 — always dark)
- Centered column, emoji or icon, large headline, lighter subtitle
- Eyebrow label above in accent color, uppercase, wide letter-spacing
- Use display font at `clamp(44px, 6.5vw, 80px)` — this is the moment to make an impression

### Problem / Context slide (light)
- Stat row: flex row with 2–4 key numbers, accent value, small label
- Two-column card grid below

### Vision / Three pillars slide (dark)
- Centered header + three equal cards in a row with icon, title, description

### Process / Flow slide (light)
- Horizontal chain: pill steps connected by → arrows
- Supporting two-column cards below
- Optional callout box at bottom

### Big statement slide (dark)
- Single massive number or short phrase — display font, italic bold, `clamp(56px, 10vw, 100px)`
- Supporting sentence below in lighter weight body font

### Data / Chart slide (light)
- Bar chart built with pure CSS divs (no libraries)
- Each bar: label (right-aligned, fixed width) + track div + fill div with inline width %

### Detail / Two-column slide (dark)
- Left: 2–3 stacked info boxes (label + value format)
- Right: headline + body + metric boxes in a row

### Roadmap / Grid slide (light)
- 2×2 card grid, each with phase tag, title, bullet list

### CTA / Closing slide (dark)
- Centered, large italic-accent headline, body text, contact line

## Design Principles

- **Committed aesthetic**: pick a bold direction and execute it — editorial, luxury, techy, organic, brutalist
- **Two-font pairing**: display font for headings, body font for prose — never the same family for both
- **No generic fonts**: never Inter, Roboto, Arial, or system fonts
- **Responsive type**: always `clamp(min, preferred, max)` for headings; minimum sizes are generous
- **Body text minimum**: 15px — never 12–13px for paragraph content
- **Contrast**: verify `--text-dark-body` and `--text-light-body` at 4.5:1 against their backgrounds
- **No hardcoded hex colors in layout**: use CSS vars everywhere
- **Atmospheric backgrounds**: dark slides need depth (gradient mesh, layered texture) — never plain solid
- **Slide entry animations**: required — staggered fade+translate on `.is-visible`, reset on leave
- **Cards**: 12–16px border-radius, subtle border
- **Single tone per slide**: dark or light, not mixed — use alternating pattern

## Style Reference Extraction

When user provides a website URL for style inspiration:
1. Use agent-browser or WebFetch to capture the site
2. Extract: primary colors (dark, light, accent), font family/weights, border-radius style (sharp vs. rounded), overall vibe (minimal, bold, editorial, corporate)
3. Translate into fresh CSS vars — do NOT recreate the site's layout, only adapt its color language and typographic personality
4. Pick Google Fonts that match the vibe — one display, one body. If the site uses a characterful display font, find a similar free alternative
