---
name: nanobanana
description: Generate professional photo-realistic images using structured JSON prompts and Google's Gemini image API (Nano Banana). Transforms plain English descriptions into detailed prompt specifications with lighting, camera, composition, style, and negative prompts. Use when user asks to "generate an image", "create a product shot", "make a lifestyle photo", "create ad creative", "generate a hero image", or wants professional-quality AI imagery for brands, products, or campaigns.
---

# Nano Banana — Structured Image Generation

Transform plain-English descriptions into professional-grade images by constructing structured JSON prompts with full control over lighting, camera, composition, style, and negative constraints. Then fire to Google's Gemini image API and save everything organized.

Requires `GEMINI_API_KEY` environment variable.

## Phase 1: Brief

Ask the user what they want to create. Accept any of:
- A plain description ("product shot of a candle on marble")
- A brand context ("we sell premium coffee, need hero images for ads")
- A reference image to match or riff on
- An iteration request ("same scene but warmer lighting")

Ask what **use case** this is for if not obvious:
- Product shot (e-commerce, catalog)
- Lifestyle image (social, editorial)
- Ad creative (paid social, display)
- Hero image (website, landing page)
- Brand asset (packaging mockup, logo context)

Do NOT ask for technical camera details — you will derive those.

## Phase 2: Build the Structured Prompt

This is the core of the skill. Convert the user's plain description into a structured JSON prompt object. Every field matters — this is what separates slot-machine prompting from consistent, professional output.

### Prompt Schema

```json
{
  "scene": {
    "subject": "Primary subject — what is in the frame",
    "environment": "Setting/backdrop description",
    "action": "What the subject is doing or how it's positioned",
    "props": "Supporting objects in the scene"
  },
  "camera": {
    "angle": "Eye-level | Low angle | High angle | Bird's eye | Dutch angle | Three-quarter",
    "shot_type": "Close-up | Medium | Wide | Full body | Detail/macro | Over-the-shoulder",
    "lens": "24mm | 35mm | 50mm | 85mm | 100mm macro | 135mm | 200mm",
    "depth_of_field": "Shallow (f/1.4-2.8) | Medium (f/4-5.6) | Deep (f/8-16)",
    "focus": "What the focal point is"
  },
  "lighting": {
    "type": "Natural | Studio | Mixed | Dramatic | Flat",
    "setup": "Specific lighting description — softbox, rim light, golden hour, overcast, etc.",
    "direction": "Front | Side | Back | Overhead | Under | Rembrandt | Loop | Butterfly",
    "quality": "Soft/diffused | Hard/specular | Mixed",
    "color_temperature": "Warm (3200K) | Neutral (5500K) | Cool (6500K+) | Mixed"
  },
  "style": {
    "mood": "The emotional feel — luxurious, energetic, calm, raw, editorial, etc.",
    "color_grading": "Color treatment — warm tones, desaturated, high contrast, pastel, etc.",
    "aesthetic": "Visual reference — editorial, commercial, lifestyle, cinematic, minimalist, etc.",
    "texture": "Surface quality — matte, glossy, film grain, clean digital, etc."
  },
  "technical": {
    "aspect_ratio": "1:1 | 2:3 | 3:2 | 4:3 | 4:5 | 9:16 | 16:9",
    "resolution": "1K | 2K | 4K",
    "model": "gemini-2.5-flash-image | gemini-3-pro-image-preview"
  },
  "negative": "What to avoid — plastic skin, text artifacts, distorted hands, oversaturation, stock photo feel, etc."
}
```

### Deriving the Prompt

When building the JSON:

**For product shots:**
- Default to 85mm or 100mm macro, shallow DoF
- Studio lighting with softbox, clean backdrop
- Eye-level or slightly elevated angle
- Aspect ratio matching the platform (1:1 for catalog, 4:5 for Instagram, 16:9 for web hero)

**For lifestyle images:**
- Default to 35mm or 50mm, medium DoF
- Natural lighting, golden hour or soft overcast
- Three-quarter or candid angle
- Warm color grading, editorial mood

**For ad creative:**
- Match the platform format (9:16 for stories, 1:1 for feed, 16:9 for display)
- Bold, high-contrast lighting
- Clean composition with space for text overlay
- Commercial aesthetic

**For hero images:**
- Wide lens (24-35mm), deep or medium DoF
- Dramatic or atmospheric lighting
- 16:9 or 21:9 aspect ratio
- Cinematic color grading

### Default Negative Prompts

Always include unless the user wants otherwise:
- "plastic skin, uncanny valley, distorted features"
- "misspelled text, garbled letters, text artifacts"
- "oversaturated, HDR look, over-processed"
- "stock photo watermark, generic stock feel"
- "blurry, out of focus subject, motion blur on subject"

Add category-specific negatives:
- Products: "floating objects, inconsistent shadows, unrealistic reflections"
- People: "extra fingers, distorted hands, asymmetric face, dead eyes"
- Food: "plastic-looking food, unnatural colors, floating ingredients"

## Phase 3: Compose the Final Prompt

Flatten the JSON into a single, dense prompt string optimized for Gemini. Format:

```
[scene.subject], [scene.action], [scene.environment], [scene.props].
Shot on [camera.lens] at [camera.depth_of_field], [camera.shot_type], [camera.angle].
[lighting.setup], [lighting.direction] lighting, [lighting.quality], [lighting.color_temperature].
[style.mood] mood, [style.color_grading], [style.aesthetic] style, [style.texture].
Avoid: [negative].
```

This is the prompt sent to the API. The structured JSON is saved alongside for reuse.

## Phase 4: Generate

### Setup

Check for the generation script:
```bash
test -f ~/.claude/skills/gemini-imagegen/scripts/generate_image.py && echo "ready" || echo "missing"
```

If the gemini-imagegen scripts are available, use them. Otherwise, use the inline Python pattern.

### Output Organization

Create an organized output structure:
```
nanobanana-output/
  [project-name]/
    [timestamp]-[short-desc].png      # The generated image
    [timestamp]-[short-desc].json     # The structured prompt JSON
```

Create the output directory if it doesn't exist:
```bash
mkdir -p nanobanana-output/[project-name]
```

### Generation Script

Use this Python script to generate:

```bash
python ~/.claude/skills/nanobanana/scripts/nanobanana_generate.py \
  --prompt "the composed prompt string" \
  --output "nanobanana-output/[project]/[timestamp]-[desc].png" \
  --prompt-json "nanobanana-output/[project]/[timestamp]-[desc].json" \
  --aspect "4:5" \
  --size "2K" \
  --model "gemini-2.5-flash-image"
```

The script saves both the image and the full structured JSON prompt for reuse.

### Model Selection

- Use `gemini-2.5-flash-image` (Nano Banana) for speed and iteration — good for most shots
- Use `gemini-3-pro-image-preview` (Nano Banana Pro) when:
  - Text rendering matters (logos, packaging with labels)
  - Maximum quality is needed (hero images, print)
  - Complex multi-element compositions
  - 4K resolution is required

## Phase 5: Present & Iterate

After generation, show the user:
1. The generated image (open or display the file path)
2. The structured prompt JSON used
3. Suggestions for iteration

### Iteration Workflow

When the user wants to refine:
- "warmer" → adjust `lighting.color_temperature` and `style.color_grading`
- "more dramatic" → adjust `lighting.type`, `lighting.direction`, increase contrast
- "closer" → change `camera.shot_type` and `camera.lens`
- "cleaner background" → simplify `scene.environment`, add background clutter to negative
- "more lifestyle" → shift `style.aesthetic`, change `lighting.type` to natural
- "less AI-looking" → add film grain to `style.texture`, add "over-processed" to negative

Update the JSON, recompose the prompt, regenerate. Save each iteration with incrementing filenames so the user can compare.

### Batch Generation

When the user needs multiple variations:
- Generate 3-5 variations by adjusting one axis at a time (lighting, angle, color grading)
- Save all with descriptive names
- Present as a contact sheet for comparison

## Phase 6: Save for Reuse

When the user is happy with a result, the JSON prompt becomes a reusable template:

```
nanobanana-output/
  [project]/
    templates/
      product-hero.json      # Saved template
      lifestyle-warm.json    # Saved template
```

Templates can be loaded and modified for future campaigns — same lighting, same style, different products.

## Prompt Engineering Rules

1. **Be specific, not flowery.** "Soft diffused light from a 3-foot octabox, camera left" beats "beautiful dreamy lighting"
2. **Camera details ground the image.** Lens focal length and aperture are the single biggest lever for realism
3. **Negative prompts are as important as positive.** Always specify what to avoid
4. **Match the use case.** Instagram ads need different compositions than website heroes
5. **Iterate on one axis.** Change lighting OR angle OR color — not everything at once
6. **Use Pro for text.** If the image includes any readable text, switch to `gemini-3-pro-image-preview`
