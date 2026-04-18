---
name: appstore-images
description: Create beautiful App Store preview screenshots for iOS (iPhone), iPad, and macOS. Takes app screenshots and optional text lines, composites them onto gradient backgrounds with device framing, shadows, and typography. Use when user asks to "create app store screenshots", "make preview screens", "generate app store images", "app store marketing images", or wants polished device-framed previews for App Store listings.
---

# App Store Preview Generator

Create polished, App Store-ready preview screens by compositing app screenshots onto gradient backgrounds with headline text, device framing, rounded corners, and drop shadows. Supports iPhone, iPad, and Mac.

Requires `Pillow` — install with:
```bash
pip install -r ~/.claude/skills/appstore-images/scripts/requirements.txt
```

## Phase 1: Gather Inputs

Ask the user for:

1. **Screenshots** — one or more app screenshots (PNG/JPG paths). These are the raw captures from the app.
2. **Device** — which platform: `iphone`, `iphone_small`, `ipad`, or `mac`. Default to `iphone` if not specified.
3. **Text** (optional) — a headline and/or subheadline to display above the screenshot.

If the user provides screenshots without specifying text, generate the previews without text — the screenshots alone on a gradient background still look great.

If the user hasn't specified a gradient, pick one that complements the screenshot's dominant colors. Available presets:

| Preset | Colors | Best for |
|--------|--------|----------|
| `ocean` | Dark teal to steel blue | Productivity, finance |
| `sunset` | Red-orange to gold | Social, lifestyle |
| `midnight` | Near-black to dark gray | Utilities, dark-mode apps |
| `aurora` | Cyan to blue | Weather, travel |
| `lavender` | Purple to indigo | Creative, wellness |
| `forest` | Teal to green | Health, nature |
| `coral` | Pink to light blue | Social, dating |
| `slate` | Navy to blue-gray | Business, enterprise |
| `ember` | Red to yellow | Food, entertainment |
| `arctic` | Light blue to pale gray | Minimalist, light-mode apps |
| `plum` | Deep purple to violet | Music, nightlife |
| `charcoal` | Deep navy to dark blue | Default — works with everything |

Custom gradients: pass any two hex colors as `"#hex1,#hex2"`.

### Font Presets

Pass `--font <preset>` to pick a bundled headline/subheadline pairing. Default is **montserrat** — a wide, rounded, heavy geometric black that matches our App Store reference style.

| Preset | Headline feel | Best for |
|--------|---------------|----------|
| `montserrat` | Rounded geometric black | Default — warm, modern, marketing-forward |
| `oswald` | Condensed bold sans | Editorial, magazine cover |
| `bebas` | Ultra-condensed tall caps | Minimal, fashion |
| `anton` | Narrow heavy sans | Sporty, punchy |
| `archivo` | Squat geometric black | Modern, friendly |
| `monasans` | Wide geometric expanded | Bold, tech-forward |
| `fredoka` | Rounded, friendly, cartoony | Playful, approachable, consumer apps |

Override individual fonts with `--headline-font <path>` / `--subheadline-font <path>`.

## Phase 2: Generate Previews

### Single Screenshot

```bash
python ~/.claude/skills/appstore-images/scripts/appstore_preview.py \
  --screenshot "path/to/screenshot.png" \
  --output "appstore-previews/preview-01.png" \
  --device iphone \
  --headline "Track Your Habits" \
  --subheadline "Beautiful. Simple. Effective." \
  --gradient lavender \
  --text-color "#FFFFFF" \
  --font oswald \
  --metadata "appstore-previews/preview-01.json"
```

### Batch — Multiple Screenshots

When the user provides multiple screenshots, generate a preview for each. Use consistent gradient and text styling across the set, but vary the headline per screen to tell a story:

```
Screen 1: "Track Your Habits"      — showing the main dashboard
Screen 2: "See Your Progress"      — showing analytics/charts
Screen 3: "Stay Motivated"         — showing streaks/achievements
Screen 4: "Beautiful Dark Mode"    — showing dark theme
```

Run one command per screenshot. Save all outputs in the same directory.

### Multi-Device Sets

When generating for multiple device types (iPhone + iPad + Mac), run separate passes with the appropriate `--device` flag. Organize outputs by device:

```
appstore-previews/
  iphone/
    preview-01.png
    preview-02.png
  ipad/
    preview-01.png
    preview-02.png
  mac/
    preview-01.png
    preview-02.png
```

## Phase 3: Present & Iterate

After generating, show the user:
1. The generated preview image(s) — display the file path and read/show the image
2. The gradient and text settings used
3. Suggestions for refinement

### Iteration Options

Common refinements to offer:
- **"different gradient"** — try another preset or custom hex pair
- **"change the text"** — update headline/subheadline
- **"lighter/darker"** — swap gradient direction or pick a lighter/darker preset
- **"no text"** — regenerate without text for a cleaner look
- **"different device"** — regenerate for iPad or Mac
- **"rotate gradient"** — change `--gradient-angle` (default 160°, try 45°, 90°, 200°)

### Text Guidelines

For effective App Store preview text:
- **Headlines**: 2-4 words max. Action-oriented or benefit-focused. "Track Your Habits" not "A Comprehensive Habit Tracking Application"
- **Subheadlines**: One short phrase that reinforces the headline. Optional — skip if the screenshot speaks for itself.
- **Contrast**: Use white text (`#FFFFFF`) on dark gradients, dark text (`#1a1a2e`) on light gradients like `arctic`

## Device Reference

| Device | Canvas Size | Use Case |
|--------|------------|----------|
| `iphone` | 1290 x 2796 | iPhone 6.7" — required for App Store |
| `iphone_small` | 1284 x 2778 | iPhone 6.5" — optional secondary |
| `ipad` | 2048 x 2732 | iPad Pro 12.9" — required for iPad apps |
| `mac` | 2880 x 1800 | Mac App Store — renders as a MacBook with screen, hinge, and base |

## Enhancement: Nano Banana Background

For extra-premium previews, use Nano Banana to generate a custom photographic background instead of a flat gradient:

1. Generate a background image with Nano Banana matching the app's aesthetic
2. Use that image as a base instead of the gradient
3. Composite the screenshot on top with the same framing

This is an advanced workflow — only suggest it if the user asks for something beyond gradients, or if the app's brand has a strong visual identity that would benefit from a custom photographic backdrop.
