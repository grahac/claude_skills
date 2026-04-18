#!/usr/bin/env python3
"""
App Store Preview Generator — Create beautiful preview screens for iOS, iPad, and macOS.

Takes a screenshot and optional text, composites them onto a colored background
with a realistic device mockup frame, drop shadow, and bold typography.

Usage:
    python appstore_preview.py \
        --screenshot app_screen.png \
        --device iphone \
        --headline "Large group chats finally make sense" \
        --subheadline "Follow the topics you care about." \
        --output preview.png \
        --bg-color "#F5A623" \
        --device-color "#2D2D2D" \
        --text-color "#FFFFFF"
"""

import argparse
import json
import math
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


# ---------------------------------------------------------------------------
# Device presets — canvas matches Apple's App Store requirements
# ---------------------------------------------------------------------------

DEVICES = {
    "iphone": {
        "canvas": (1290, 2796),
        # Device frame dimensions (the phone mockup)
        "frame_width": 1090,
        "frame_height": 2230,
        "frame_radius": 140,
        "frame_thickness": 16,
        "screen_radius": 124,
        # Positioning
        "frame_top": 540,
        # Dynamic island
        "dynamic_island": {"w": 280, "h": 40, "y": 34},
        # Side buttons (stick out slightly beyond frame edge)
        "side_buttons": True,
        "power_button": {"x_offset": -2, "y": 440, "w": 10, "h": 200, "radius": 5},
        "volume_up": {"x_offset": -8, "y": 360, "w": 10, "h": 130, "radius": 5},
        "volume_down": {"x_offset": -8, "y": 510, "w": 10, "h": 130, "radius": 5},
        # Text layout
        "text_area_top": 90,
        "text_area_bottom_margin": 40,
        "text_max_width": 1180,
        "headline_size": 142,
        "subheadline_size": 58,
        "headline_line_spacing": 1.12,
        "subheadline_line_spacing": 1.25,
        "headline_sub_gap": 40,
    },
    "iphone_small": {
        "canvas": (1284, 2778),
        "frame_width": 1080,
        "frame_height": 2210,
        "frame_radius": 138,
        "frame_thickness": 16,
        "screen_radius": 122,
        "frame_top": 540,
        "dynamic_island": {"w": 278, "h": 40, "y": 34},
        "side_buttons": True,
        "power_button": {"x_offset": -2, "y": 440, "w": 10, "h": 200, "radius": 5},
        "volume_up": {"x_offset": -8, "y": 360, "w": 10, "h": 130, "radius": 5},
        "volume_down": {"x_offset": -8, "y": 510, "w": 10, "h": 130, "radius": 5},
        "text_area_top": 90,
        "text_area_bottom_margin": 40,
        "text_max_width": 1170,
        "headline_size": 140,
        "subheadline_size": 56,
        "headline_line_spacing": 1.12,
        "subheadline_line_spacing": 1.25,
        "headline_sub_gap": 40,
    },
    "ipad": {
        "canvas": (2048, 2732),
        "frame_width": 1680,
        "frame_height": 2200,
        "frame_radius": 50,
        "frame_thickness": 20,
        "screen_radius": 32,
        "frame_top": 420,
        "side_buttons": False,
        "text_area_top": 80,
        "text_area_bottom_margin": 50,
        "text_max_width": 1700,
        "headline_size": 120,
        "subheadline_size": 54,
        "headline_line_spacing": 1.08,
        "subheadline_line_spacing": 1.3,
        "headline_sub_gap": 20,
    },
    "mac": {
        "canvas": (2880, 1800),
        # Window frame: titlebar (60) + content area (4:3 aspect, matches iPad landscape)
        "frame_width": 1920,
        "frame_height": 1500,   # 60 titlebar + 1440 content (1920 / 1.333 = 1440)
        "frame_radius": 20,
        "frame_thickness": 0,   # window has no visible outer frame
        "screen_radius": 0,     # content fills — outer rounding handled by window
        "frame_top": 270,
        "side_buttons": False,
        "window_chrome": {
            "titlebar_height": 60,
            "titlebar_color": "#E5E5E7",
            "titlebar_border": "#C7C7CC",
            "traffic_red": "#FF5F57",
            "traffic_yellow": "#FEBC2E",
            "traffic_green": "#28C840",
            "light_radius": 14,
            "light_spacing": 44,
            "light_left": 40,
        },
        "text_area_top": 60,
        "text_area_bottom_margin": 40,
        "text_max_width": 2400,
        "headline_size": 120,
        "subheadline_size": 52,
        "headline_line_spacing": 1.0,
        "subheadline_line_spacing": 1.25,
        "headline_sub_gap": 20,
    },
}

# Background color presets — solid colors that look great
COLOR_PRESETS = {
    "amber": "#F5A623",
    "coral": "#FF6B6B",
    "ocean": "#0077B6",
    "forest": "#2D6A4F",
    "lavender": "#7C3AED",
    "midnight": "#1E1E2E",
    "slate": "#475569",
    "rose": "#E11D48",
    "teal": "#0D9488",
    "indigo": "#4338CA",
    "charcoal": "#1C1C1E",
    "sky": "#0EA5E9",
    "emerald": "#059669",
    "orange": "#EA580C",
    "plum": "#7E22CE",
    "crimson": "#DC2626",
    "navy": "#1E3A5F",
    "gold": "#D97706",
    "mint": "#34D399",
    "steel": "#64748B",
}

# Font presets — headline/subheadline pairs bundled in fonts/
# Each entry: (headline_filename, subheadline_filename_or_None)
FONT_PRESETS = {
    # Rounded geometric black — default, matches reference App Store look
    "montserrat": ("Montserrat-Black.ttf", "Montserrat-Medium.ttf"),
    # Condensed, bold — classic editorial feel
    "oswald": ("Oswald-Bold.ttf", "Oswald-SemiBold.ttf"),
    # Ultra-condensed tall caps — minimal
    "bebas": ("BebasNeue-Regular.ttf", "MonaSansExpanded-Regular.ttf"),
    # Narrow heavy sans — sporty, punchy
    "anton": ("Anton-Regular.ttf", "MonaSansExpanded-Regular.ttf"),
    # Squat geometric black — modern, friendly
    "archivo": ("ArchivoBlack-Regular.ttf", "Montserrat-Medium.ttf"),
    # Wide geometric — original default
    "monasans": ("MonaSansExpanded-Black.ttf", "MonaSansExpanded-Regular.ttf"),
    # Rounded, friendly, cartoony — playful and approachable
    "fredoka": ("Fredoka-Medium.ttf", "Fredoka-Regular.ttf"),
}

# Gradient presets (two-color)
GRADIENT_PRESETS = {
    "sunset": ("#f12711", "#f5af19"),
    "aurora": ("#00c6ff", "#0072ff"),
    "ember": ("#f83600", "#f9d423"),
    "arctic": ("#E0EAFC", "#CFDEF3"),
    "dusk": ("#2C3E50", "#FD746C"),
    "neon": ("#12c2e9", "#c471ed"),
}


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def interpolate_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def fill_solid(image: Image.Image, color: str) -> None:
    draw = ImageDraw.Draw(image)
    draw.rectangle([(0, 0), image.size], fill=hex_to_rgb(color))


def fill_gradient(image: Image.Image, color_top: str, color_bottom: str, angle: float = 160.0) -> None:
    w, h = image.size
    c1 = hex_to_rgb(color_top)
    c2 = hex_to_rgb(color_bottom)
    pixels = image.load()
    rad = math.radians(angle)
    dx, dy = math.cos(rad), math.sin(rad)
    corners = [(0, 0), (w, 0), (0, h), (w, h)]
    projections = [x * dx + y * dy for x, y in corners]
    min_p, max_p = min(projections), max(projections)
    span = max_p - min_p if max_p != min_p else 1.0
    for py in range(h):
        for px in range(w):
            t = max(0.0, min(1.0, (px * dx + py * dy - min_p) / span))
            pixels[px, py] = interpolate_color(c1, c2, t)


def round_corners(image: Image.Image, radius: int) -> Image.Image:
    w, h = image.size
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (w - 1, h - 1)], radius=radius, fill=255)
    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    result.paste(image, mask=mask)
    return result


def find_font(
    size: int,
    bold: bool = False,
    black: bool = False,
    italic: bool = False,
    custom_path: str | None = None,
) -> ImageFont.FreeTypeFont:
    """Find a suitable font. Custom path first, then bundled Inter, then system fallbacks."""
    # If a custom font path is provided, use it directly
    if custom_path and os.path.exists(custom_path):
        try:
            return ImageFont.truetype(custom_path, size)
        except (OSError, IOError):
            pass

    # Resolve the fonts/ directory relative to this script
    fonts_dir = Path(__file__).parent.parent / "fonts"

    if black and italic:
        candidates = [
            str(fonts_dir / "Oswald-Bold.ttf"),
            str(fonts_dir / "MonaSansExpanded-BlackItalic.ttf"),
        ]
    elif black:
        candidates = [
            str(fonts_dir / "Montserrat-Black.ttf"),
            str(fonts_dir / "ArchivoBlack-Regular.ttf"),
            str(fonts_dir / "MonaSansExpanded-Black.ttf"),
        ]
    elif bold and italic:
        candidates = [
            str(fonts_dir / "Oswald-SemiBold.ttf"),
            str(fonts_dir / "MonaSansExpanded-BoldItalic.ttf"),
        ]
    elif bold:
        candidates = [
            str(fonts_dir / "Montserrat-Medium.ttf"),
            str(fonts_dir / "MonaSansExpanded-Bold.ttf"),
        ]
    elif italic:
        candidates = [
            str(fonts_dir / "MonaSansExpanded-Italic.ttf"),
            str(fonts_dir / "MonaSansExpanded-Regular.ttf"),
        ]
    else:
        candidates = [
            str(fonts_dir / "MonaSansExpanded-Regular.ttf"),
        ]

    # System fallbacks
    candidates += [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if (bold or black) else "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except (OSError, IOError):
                continue
    return ImageFont.load_default()


def wrap_text(draw, text: str, font, max_width: int) -> list[str]:
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def resolve_preset_fonts(preset: str | None) -> tuple[str | None, str | None]:
    """Map a --font preset name to (headline_path, subheadline_path) or (None, None)."""
    if not preset:
        return (None, None)
    entry = FONT_PRESETS.get(preset.lower())
    if not entry:
        return (None, None)
    fonts_dir = Path(__file__).parent.parent / "fonts"
    h = fonts_dir / entry[0]
    s = fonts_dir / entry[1] if entry[1] else None
    return (str(h) if h.exists() else None, str(s) if s and s.exists() else None)


def draw_text_block(
    canvas: Image.Image,
    headline: str | None,
    subheadline: str | None,
    device: dict,
    text_color: str,
    uppercase: bool = True,
    italic: bool = False,
    headline_font_path: str | None = None,
    subheadline_font_path: str | None = None,
) -> int:
    """Draw headline and subheadline. Returns the Y position of the bottom of text block."""
    draw = ImageDraw.Draw(canvas)
    canvas_w = device["canvas"][0]
    max_w = device["text_max_width"]
    color = hex_to_rgb(text_color)
    h_line_mult = device["headline_line_spacing"]
    s_line_mult = device["subheadline_line_spacing"]
    gap = device["headline_sub_gap"]

    y = device["text_area_top"]

    if headline:
        display_text = headline.upper() if uppercase else headline
        font = find_font(device["headline_size"], black=True, italic=italic, custom_path=headline_font_path)
        lines = wrap_text(draw, display_text, font, max_w)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            x = (canvas_w - tw) // 2
            draw.text((x, y), line, font=font, fill=color)
            y += int(th * h_line_mult)
        y += gap

    if subheadline:
        font_sub = find_font(device["subheadline_size"], bold=False, italic=italic, custom_path=subheadline_font_path)
        sub_lines = wrap_text(draw, subheadline, font_sub, max_w)
        for line in sub_lines:
            bbox = draw.textbbox((0, 0), line, font=font_sub)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            x = (canvas_w - tw) // 2
            draw.text((x, y), line, font=font_sub, fill=color)
            y += int(th * s_line_mult)

    return y


def draw_mac_window(
    canvas: Image.Image,
    screenshot: Image.Image,
    device: dict,
    wc: dict,
) -> None:
    """Render the screenshot as a macOS-style app window with titlebar + traffic lights."""
    draw = ImageDraw.Draw(canvas, "RGBA")
    canvas_w = device["canvas"][0]
    fw = device["frame_width"]
    fh = device["frame_height"]
    fr = device["frame_radius"]
    fy = device["frame_top"]
    fx = (canvas_w - fw) // 2
    tb_h = wc["titlebar_height"]

    # Drop shadow behind window
    shadow_expand = 80
    shadow = Image.new("RGBA", (fw + shadow_expand * 2, fh + shadow_expand * 2), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        [(shadow_expand, shadow_expand + 20), (shadow_expand + fw - 1, shadow_expand + fh + 19)],
        radius=fr,
        fill=(0, 0, 0, 110),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=50))
    canvas.paste(shadow, (fx - shadow_expand, fy - shadow_expand), shadow)

    # Build the window contents on its own RGBA layer, then round the whole thing
    win = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    wd = ImageDraw.Draw(win)

    # Titlebar background
    wd.rectangle([(0, 0), (fw - 1, tb_h - 1)], fill=hex_to_rgb(wc["titlebar_color"]))
    # Thin separator line below titlebar
    wd.rectangle([(0, tb_h - 1), (fw - 1, tb_h - 1)], fill=hex_to_rgb(wc["titlebar_border"]))

    # Traffic lights
    lr = wc["light_radius"]
    ls = wc["light_spacing"]
    lx = wc["light_left"]
    ly = tb_h // 2
    for i, key in enumerate(("traffic_red", "traffic_yellow", "traffic_green")):
        cx = lx + i * ls
        wd.ellipse([(cx - lr, ly - lr), (cx + lr, ly + lr)], fill=hex_to_rgb(wc[key]))

    # Screenshot content area — preserve aspect, cover then center-crop
    content_w = fw
    content_h = fh - tb_h
    ss = screenshot.convert("RGBA")
    sw, sh = ss.size
    scale = max(content_w / sw, content_h / sh)
    new_w, new_h = int(sw * scale), int(sh * scale)
    ss_resized = ss.resize((new_w, new_h), Image.LANCZOS)
    cx = (new_w - content_w) // 2
    cy = (new_h - content_h) // 2
    ss_cropped = ss_resized.crop((cx, cy, cx + content_w, cy + content_h))
    win.paste(ss_cropped, (0, tb_h), ss_cropped)

    # Round the outer window corners
    win = round_corners(win, fr)
    canvas.paste(win, (fx, fy), win)


def draw_device_frame(
    canvas: Image.Image,
    screenshot: Image.Image,
    device: dict,
    device_color: str,
) -> None:
    """Draw a realistic device mockup frame with the screenshot inside."""
    draw = ImageDraw.Draw(canvas, "RGBA")
    canvas_w = device["canvas"][0]
    fw = device["frame_width"]
    fh = device["frame_height"]
    ft = device["frame_thickness"]
    fr = device["frame_radius"]
    sr = device["screen_radius"]
    fy = device["frame_top"]
    fx = (canvas_w - fw) // 2

    # Mac-style window chrome (titlebar + traffic lights, preserves screenshot aspect)
    wc = device.get("window_chrome")
    if wc:
        draw_mac_window(canvas, screenshot, device, wc)
        return

    dc = hex_to_rgb(device_color)
    # Slightly lighter shade for highlights
    dc_light = tuple(min(255, c + 30) for c in dc)
    dc_dark = tuple(max(0, c - 20) for c in dc)

    # --- Drop shadow behind the entire device ---
    shadow_expand = 80
    shadow = Image.new("RGBA", (fw + shadow_expand * 2, fh + shadow_expand * 2), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        [(shadow_expand, shadow_expand + 15), (shadow_expand + fw - 1, shadow_expand + fh + 14)],
        radius=fr,
        fill=(0, 0, 0, 100),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=45))
    canvas.paste(shadow, (fx - shadow_expand, fy - shadow_expand), shadow)

    # --- Outer frame body (the device case) ---
    draw.rounded_rectangle(
        [(fx, fy), (fx + fw - 1, fy + fh - 1)],
        radius=fr,
        fill=dc,
    )

    # Subtle edge highlights for 3D effect
    # Top-left highlight
    draw.rounded_rectangle(
        [(fx + 1, fy + 1), (fx + fw - 2, fy + fh - 2)],
        radius=fr - 1,
        fill=None,
        outline=dc_light + (60,),
        width=2,
    )
    # Bottom-right shadow edge
    draw.rounded_rectangle(
        [(fx + 2, fy + 2), (fx + fw - 1, fy + fh - 1)],
        radius=fr - 1,
        fill=None,
        outline=dc_dark + (40,),
        width=1,
    )

    # --- Side buttons (iPhone only) ---
    if device.get("side_buttons"):
        # Right side — power button
        pb = device["power_button"]
        pbx = fx + fw + pb["x_offset"]
        pby = fy + pb["y"]
        draw.rounded_rectangle(
            [(pbx, pby), (pbx + pb["w"], pby + pb["h"])],
            radius=pb["radius"],
            fill=dc_dark,
        )
        # Left side — volume buttons
        for btn_key in ("volume_up", "volume_down"):
            vb = device[btn_key]
            vbx = fx + vb["x_offset"]
            vby = fy + vb["y"]
            draw.rounded_rectangle(
                [(vbx, vby), (vbx + vb["w"], vby + vb["h"])],
                radius=vb["radius"],
                fill=dc_dark,
            )

    # --- Screen area (inset from frame) ---
    screen_x = fx + ft
    screen_y = fy + ft
    screen_w = fw - ft * 2
    screen_h = fh - ft * 2

    # Black bezel behind screen
    draw.rounded_rectangle(
        [(screen_x, screen_y), (screen_x + screen_w - 1, screen_y + screen_h - 1)],
        radius=sr,
        fill=(0, 0, 0),
    )

    # Resize screenshot to fill the screen area
    screenshot = screenshot.convert("RGBA")
    screenshot = screenshot.resize((screen_w, screen_h), Image.LANCZOS)
    screenshot = round_corners(screenshot, sr)

    canvas.paste(screenshot, (screen_x, screen_y), screenshot)

    # --- Dynamic island (iPhone only) ---
    di = device.get("dynamic_island")
    if di:
        di_w = di["w"]
        di_h = di["h"]
        di_x = screen_x + (screen_w - di_w) // 2
        di_y = screen_y + di["y"]
        draw.rounded_rectangle(
            [(di_x, di_y), (di_x + di_w - 1, di_y + di_h - 1)],
            radius=di_h // 2,
            fill=(0, 0, 0, 255),
        )

    # --- MacBook camera notch (centered at top of screen) ---
    lb = device.get("laptop_body")
    if lb and lb.get("notch_width"):
        nw = lb["notch_width"]
        nh = lb["notch_height"]
        nx = screen_x + (screen_w - nw) // 2
        ny = screen_y
        draw.rounded_rectangle(
            [(nx, ny), (nx + nw - 1, ny + nh - 1)],
            radius=min(nh // 2, 12),
            fill=(0, 0, 0, 255),
        )

    # --- MacBook laptop base (hinge + rounded bottom deck) ---
    if lb:
        extra = lb["base_width_extra"]
        hinge_h = lb["hinge_height"]
        base_h = lb["base_height"]
        base_r = lb["base_radius"]
        hinge_y = fy + fh
        base_x0 = fx - extra // 2
        base_x1 = fx + fw + extra // 2
        # Thin hinge strip — same color as frame but a bit darker
        draw.rectangle(
            [(fx - 4, hinge_y), (fx + fw + 3, hinge_y + hinge_h - 1)],
            fill=dc_dark,
        )
        # Wider rounded base
        base_y0 = hinge_y + hinge_h
        base_y1 = base_y0 + base_h
        draw.rounded_rectangle(
            [(base_x0, base_y0), (base_x1 - 1, base_y1 - 1)],
            radius=base_r,
            fill=dc,
        )
        # Subtle trackpad notch on front edge (small semi-circle indent)
        notch_w = (base_x1 - base_x0) // 6
        notch_cx = (base_x0 + base_x1) // 2
        draw.rounded_rectangle(
            [(notch_cx - notch_w // 2, base_y0), (notch_cx + notch_w // 2, base_y0 + 6)],
            radius=3,
            fill=dc_dark,
        )


def generate_preview(
    screenshot_path: str,
    output_path: str,
    device_name: str = "iphone",
    headline: str | None = None,
    subheadline: str | None = None,
    bg_color: str | None = None,
    gradient: str | None = None,
    gradient_angle: float = 160.0,
    device_color: str = "#2D2D2D",
    text_color: str = "#FFFFFF",
    uppercase: bool = True,
    italic: bool = False,
    headline_font: str | None = None,
    subheadline_font: str | None = None,
    font_preset: str | None = None,
    metadata_path: str | None = None,
) -> Path:
    """Generate an App Store preview image."""
    device = DEVICES.get(device_name)
    if not device:
        print(f"Error: Unknown device '{device_name}'. Options: {list(DEVICES.keys())}", file=sys.stderr)
        sys.exit(1)

    # Load screenshot
    try:
        screenshot = Image.open(screenshot_path)
    except Exception as e:
        print(f"Error opening screenshot: {e}", file=sys.stderr)
        sys.exit(1)

    canvas_w, canvas_h = device["canvas"]
    canvas = Image.new("RGBA", (canvas_w, canvas_h))

    # Fill background — solid color or gradient
    if bg_color:
        resolved = COLOR_PRESETS.get(bg_color, bg_color)
        fill_solid(canvas, resolved)
    elif gradient:
        if gradient in GRADIENT_PRESETS:
            c1, c2 = GRADIENT_PRESETS[gradient]
        elif "," in gradient:
            parts = gradient.split(",")
            c1, c2 = parts[0].strip(), parts[1].strip()
        else:
            c1, c2 = "#1C1C1E", "#2D2D2D"
        fill_gradient(canvas, c1, c2, angle=gradient_angle)
    else:
        fill_solid(canvas, "#1C1C1E")

    # Resolve font preset (explicit paths win)
    preset_h, preset_s = resolve_preset_fonts(font_preset)
    headline_font = headline_font or preset_h
    subheadline_font = subheadline_font or preset_s

    # Draw text
    text_bottom = draw_text_block(
        canvas, headline, subheadline, device, text_color,
        uppercase=uppercase, italic=italic,
        headline_font_path=headline_font, subheadline_font_path=subheadline_font,
    )

    # Optionally adjust frame_top based on text bottom
    # If text is provided and pushes down, shift the device down
    min_frame_top = text_bottom + device["text_area_bottom_margin"]
    actual_frame_top = max(device["frame_top"], min_frame_top)

    # Check if device would go off canvas — shrink if needed
    available_height = canvas_h - actual_frame_top - 40  # 40px bottom margin
    frame_h = device["frame_height"]
    frame_w = device["frame_width"]

    if frame_h > available_height:
        scale = available_height / frame_h
        device = dict(device)  # copy so we don't mutate the preset
        device["frame_height"] = int(frame_h * scale)
        device["frame_width"] = int(frame_w * scale)
        device["frame_thickness"] = max(10, int(device["frame_thickness"] * scale))
        device["frame_radius"] = int(device["frame_radius"] * scale)
        device["screen_radius"] = int(device["screen_radius"] * scale)
        if device.get("side_buttons"):
            for key in ("power_button", "volume_up", "volume_down"):
                btn = dict(device[key])
                btn["y"] = int(btn["y"] * scale)
                btn["h"] = int(btn["h"] * scale)
                device[key] = btn

    device["frame_top"] = actual_frame_top

    # Draw device frame with screenshot
    draw_device_frame(canvas, screenshot, device, device_color)

    # Save
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = canvas.convert("RGB")
    canvas.save(output, quality=95)
    print(f"Preview saved: {output}")

    # Save metadata
    if metadata_path:
        bg = bg_color or gradient or "#1C1C1E"
        meta = {
            "generated_at": datetime.now().isoformat(),
            "device": device_name,
            "canvas_size": list(DEVICES.get(device_name, device)["canvas"]),
            "screenshot": str(Path(screenshot_path).name),
            "headline": headline,
            "subheadline": subheadline,
            "background": bg,
            "device_color": device_color,
            "text_color": text_color,
            "output": str(output.name),
        }
        meta_path = Path(metadata_path)
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)

    return output


def main():
    parser = argparse.ArgumentParser(description="App Store Preview Generator")
    parser.add_argument("--screenshot", "-s", required=True, help="Path to app screenshot")
    parser.add_argument("--output", "-o", required=True, help="Output preview image path")
    parser.add_argument(
        "--device", "-d", default="iphone",
        choices=list(DEVICES.keys()),
        help="Device type (default: iphone)",
    )
    parser.add_argument("--headline", help="Primary text (will be uppercased by default)")
    parser.add_argument("--subheadline", help="Secondary text line")
    parser.add_argument(
        "--bg-color",
        help=f"Background color: preset ({', '.join(list(COLOR_PRESETS.keys())[:8])}...) or hex",
    )
    parser.add_argument(
        "--gradient", "-g",
        help=f"Gradient preset ({', '.join(GRADIENT_PRESETS.keys())}) or 'hex1,hex2'",
    )
    parser.add_argument("--gradient-angle", type=float, default=160.0, help="Gradient angle in degrees")
    parser.add_argument("--device-color", default="#2D2D2D", help="Device frame color (default: dark gray)")
    parser.add_argument("--text-color", default="#FFFFFF", help="Text color hex (default: white)")
    parser.add_argument("--no-uppercase", action="store_true", help="Don't uppercase the headline")
    parser.add_argument("--italic", action="store_true", help="Use italic font variants")
    parser.add_argument("--headline-font", help="Custom font path for headline")
    parser.add_argument("--subheadline-font", help="Custom font path for subheadline")
    parser.add_argument(
        "--font",
        choices=list(FONT_PRESETS.keys()),
        help=f"Font preset: {', '.join(FONT_PRESETS.keys())}",
    )
    parser.add_argument("--metadata", "-m", help="Path to save generation metadata JSON")

    args = parser.parse_args()

    generate_preview(
        screenshot_path=args.screenshot,
        output_path=args.output,
        device_name=args.device,
        headline=args.headline,
        subheadline=args.subheadline,
        bg_color=args.bg_color,
        gradient=args.gradient,
        gradient_angle=args.gradient_angle,
        device_color=args.device_color,
        text_color=args.text_color,
        uppercase=not args.no_uppercase,
        italic=args.italic,
        headline_font=args.headline_font,
        subheadline_font=args.subheadline_font,
        font_preset=args.font,
        metadata_path=args.metadata,
    )


if __name__ == "__main__":
    main()
