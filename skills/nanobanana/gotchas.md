# Nano Banana Gotchas

Common failure patterns. Update this file every time something goes wrong.

## 1. Missing GEMINI_API_KEY
**Problem:** The generation script fails because the `GEMINI_API_KEY` environment variable isn't set.
**Fix:** Check for the key before running anything. Print a clear error message with instructions if missing. Don't attempt fallbacks.

## 2. Using the wrong model for text-heavy images
**Problem:** Generating an image with readable text (logos, packaging labels) using `gemini-2.5-flash-image`, which produces garbled text.
**Fix:** Always use `gemini-3-pro-image-preview` when the image includes any readable text. Flash is for speed and iteration only.

## 3. Changing too many variables at once during iteration
**Problem:** User says "make it better" and you adjust lighting, angle, color grading, and composition simultaneously — impossible to know what helped.
**Fix:** Iterate on one axis at a time. Change lighting OR angle OR color — not everything at once. Save each iteration for comparison.

## 4. Flowery prompt language instead of technical specifics
**Problem:** Writing "beautiful dreamy lighting" instead of "soft diffused light from a 3-foot octabox, camera left."
**Fix:** Camera details and specific lighting setups produce dramatically better results than vague adjectives. Be technical.

## 5. Wrong aspect ratio for the target platform
**Problem:** Generating a 16:9 image for an Instagram feed post (which needs 4:5 or 1:1).
**Fix:** Always ask about the use case/platform and set the correct aspect ratio in `technical.aspect_ratio` before generating.
