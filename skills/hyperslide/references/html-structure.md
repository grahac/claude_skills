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
  --text-dark-body: /* muted light color */;
  --text-light-heading: /* dark, matches --dark-bg or nearby */;
  --text-light-body: /* mid-dark body text */;
  --accent: /* primary accent/highlight color */;
  --font: /* single Google Font family */;
}
```

## Slide Types & Layout Patterns

### Title slide (slide 1 — always dark)
- Centered column, emoji or icon, large headline, lighter subtitle
- Eyebrow label above in accent color, uppercase, wide letter-spacing

### Problem / Context slide (light)
- Stat row: flex row with 2–4 key numbers, orange value, small label
- Two-column card grid below

### Vision / Three pillars slide (dark)
- Centered header + three equal cards in a row with icon, title, description

### Process / Flow slide (light)
- Horizontal chain: pill steps connected by → arrows
- Supporting two-column cards below
- Optional amber callout box at bottom

### Big statement slide (dark)
- Single massive number or short phrase in italic bold
- Supporting sentence below in lighter weight

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

- **Responsive type**: Always use `clamp(min, preferred, max)` for headings
- **No hardcoded hex colors in layout**: use CSS vars everywhere
- **Slide labels**: 11px, 700 weight, 0.14em letter-spacing, uppercase, accent color
- **Cards**: 12–16px border-radius, subtle border, no box-shadow needed
- **Background texture**: Optional subtle SVG pattern (concentric circles, gentle curves, dots) at 2–5% opacity on dark slides — embedded as inline data URI
- **Single font**: Load one Google Font family (2–3 weights: 300, 500/600, 700)
- **No external JS libraries**: everything vanilla

## Style Reference Extraction

When user provides a website URL for style inspiration:
1. Use agent-browser or WebFetch to capture the site
2. Extract: primary colors (dark, light, accent), font family/weights, border-radius style (sharp vs. rounded), overall vibe (minimal, bold, editorial, corporate)
3. Translate into fresh CSS vars — do NOT recreate the site's layout, only adapt its color language and typographic personality
4. Pick a Google Font that matches the vibe if the site uses a custom/paid font
