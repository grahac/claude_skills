# HyperSlide Gotchas

Common failure patterns. Update this file every time something goes wrong.

## 1. Low contrast body text on dark slides
**Problem:** `--text-dark-body` is set to a muted gray that fails WCAG 4.5:1 against `--dark-bg`. Most common single failure.
**Fix:** Always verify body text contrast ratios. Muted colors look nice in a design tool but fail on screen. Prefer higher contrast values and verify before delivering.

## 2. Using Inter/Roboto/Arial/system fonts
**Problem:** Defaulting to generic sans-serif fonts that make every presentation look the same.
**Fix:** The skill explicitly bans these. Use the approved display + body font pairings from Phase 2 of SKILL.md. Load via Google Fonts.

## 3. Plain solid backgrounds on dark slides
**Problem:** Dark slides have a flat `background-color` with no depth or texture — looks cheap.
**Fix:** Always use gradient meshes, layered SVG textures, or noise patterns. Never plain solid fills on dark backgrounds.

## 4. Animations not resetting on scroll-back
**Problem:** Slide entry animations play once but don't replay when scrolling back up to a slide.
**Fix:** The IntersectionObserver must REMOVE the `.is-visible` class when a slide leaves the viewport, so it replays on re-entry.

## 5. Slide counter showing wrong total
**Problem:** The "X / N" counter doesn't match the actual number of slides, usually because slides were added/removed after the counter was coded.
**Fix:** Calculate total from `document.querySelectorAll('.slide').length` dynamically, not a hardcoded number.
