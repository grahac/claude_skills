# Website Extractor Gotchas

Common failure patterns. Update this file every time something goes wrong.

## 1. Guessing colors from screenshots instead of code
**Problem:** Extracting colors by eyeballing a screenshot — compressed images shift colors and you get wrong hex values.
**Fix:** Always extract colors from Tailwind classes, CSS variables, or inline styles in the HTML. Screenshots are for layout impression only.

## 2. Empty snapshot on SPA/JS-rendered sites
**Problem:** Running `agent-browser snapshot` returns minimal or empty content because the page hasn't finished rendering.
**Fix:** Scroll first (`agent-browser scroll down 500`), wait briefly, then re-snapshot. Some SPAs lazy-load content on scroll.

## 3. Missing secondary pages
**Problem:** Only extracting the homepage and missing critical pages (Pricing, About, Features) that define the site's full content.
**Fix:** Check the navigation for all key pages and extract each one. The extraction document should cover every page visible in the nav.

## 4. Mixing up content tone analysis with actual copy extraction
**Problem:** Summarizing what the copy says instead of extracting the actual words. The rewrite agent needs the real copy, not a paraphrase.
**Fix:** Extract copy verbatim section-by-section. Tone analysis goes in a separate section — don't merge them.

## 5. agent-browser not installed
**Problem:** The skill assumes `agent-browser` is available globally but it may not be installed.
**Fix:** Check availability first. If not installed, suggest `npm install -g agent-browser && agent-browser install`. Don't fail silently.
