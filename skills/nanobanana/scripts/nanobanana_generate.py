#!/usr/bin/env python3
"""
Nano Banana — Structured image generation with Gemini API.

Generates an image from a composed prompt string and saves both the image
and the structured JSON prompt for reuse.

Usage:
    python nanobanana_generate.py \
        --prompt "A premium candle on marble..." \
        --output output.png \
        --prompt-json prompt.json \
        --aspect 4:5 \
        --size 2K

Environment:
    GEMINI_API_KEY - Required API key
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types


def generate(
    prompt: str,
    output_path: str,
    prompt_json_path: str | None = None,
    prompt_data: dict | None = None,
    model: str = "gemini-2.5-flash-image",
    aspect_ratio: str | None = None,
    image_size: str | None = None,
) -> tuple[Path, str | None]:
    """Generate an image and save the structured prompt.

    Args:
        prompt: Composed prompt string for the API
        output_path: Where to save the generated image
        prompt_json_path: Where to save the structured prompt JSON
        prompt_data: The full structured prompt dict to save
        model: Gemini model to use
        aspect_ratio: Output aspect ratio
        image_size: Output resolution

    Returns:
        Tuple of (image path, optional text response from model)
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    config_kwargs = {"response_modalities": ["TEXT", "IMAGE"]}

    image_config_kwargs = {}
    if aspect_ratio:
        image_config_kwargs["aspect_ratio"] = aspect_ratio
    if image_size:
        image_config_kwargs["image_size"] = image_size

    if image_config_kwargs:
        config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

    config = types.GenerateContentConfig(**config_kwargs)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    response = client.models.generate_content(
        model=model,
        contents=[prompt],
        config=config,
    )

    text_response = None
    image_saved = False

    for part in response.parts:
        if part.text is not None:
            text_response = part.text
        elif part.inline_data is not None:
            image = part.as_image()
            image.save(output)
            image_saved = True

    if not image_saved:
        print("Error: No image was generated. Check your prompt and try again.", file=sys.stderr)
        sys.exit(1)

    # Save the structured prompt JSON alongside the image
    if prompt_json_path:
        json_path = Path(prompt_json_path)
        json_path.parent.mkdir(parents=True, exist_ok=True)

        save_data = {
            "generated_at": datetime.now().isoformat(),
            "model": model,
            "aspect_ratio": aspect_ratio,
            "image_size": image_size,
            "composed_prompt": prompt,
            "image_file": str(output.name),
        }

        if prompt_data:
            save_data["structured_prompt"] = prompt_data

        if text_response:
            save_data["model_response"] = text_response

        with open(json_path, "w") as f:
            json.dump(save_data, f, indent=2)

    return output, text_response


def main():
    parser = argparse.ArgumentParser(
        description="Nano Banana — Structured image generation",
    )
    parser.add_argument("--prompt", "-p", required=True, help="Composed prompt string")
    parser.add_argument("--output", "-o", required=True, help="Output image path")
    parser.add_argument("--prompt-json", "-j", help="Path to save the structured prompt JSON")
    parser.add_argument("--prompt-data", help="Structured prompt as JSON string (saved alongside)")
    parser.add_argument(
        "--model", "-m",
        default="gemini-2.5-flash-image",
        choices=["gemini-2.5-flash-image", "gemini-3-pro-image-preview"],
        help="Model to use (default: gemini-2.5-flash-image)",
    )
    parser.add_argument(
        "--aspect", "-a",
        choices=["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
        help="Aspect ratio",
    )
    parser.add_argument(
        "--size", "-s",
        choices=["1K", "2K", "4K"],
        help="Image resolution (4K only with pro model)",
    )

    args = parser.parse_args()

    prompt_data = None
    if args.prompt_data:
        prompt_data = json.loads(args.prompt_data)

    output, text = generate(
        prompt=args.prompt,
        output_path=args.output,
        prompt_json_path=args.prompt_json,
        prompt_data=prompt_data,
        model=args.model,
        aspect_ratio=args.aspect,
        image_size=args.size,
    )

    print(f"Image saved: {output}")
    if text:
        print(f"Model: {text}")


if __name__ == "__main__":
    main()
