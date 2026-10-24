#!/usr/bin/env python3
"""
ascii_art.py - Convert any image to ASCII art.

Usage:
    python ascii_art.py INPUT [options]

Examples:
    python ascii_art.py photo.jpg
    python ascii_art.py photo.jpg --width 120 --color
    python ascii_art.py photo.jpg --charset blocks --invert -o out.txt
    python ascii_art.py https://example.com/image.png --width 80
"""

import argparse
import ssl
import sys
import urllib.request
from io import BytesIO

import certifi
from PIL import Image

CHARSETS = {
    # Light-to-dark ramps, each ordered from "sparse" (background) to "dense" (foreground)
    "standard": " .:-=+*#%@",
    "detailed": " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
    "blocks": " ░▒▓█",
    "simple": " #",
}

# Monospace terminal cells are taller than wide; this corrects aspect ratio distortion.
CHAR_ASPECT_CORRECTION = 0.55


def load_image(source: str) -> Image.Image:
    if source.startswith("http://") or source.startswith("https://"):
        req = urllib.request.Request(source, headers={"User-Agent": "ascii-art-cli"})
        ctx = ssl.create_default_context(cafile=certifi.where())
        with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
            data = resp.read()
        return Image.open(BytesIO(data))
    return Image.open(source)


def resize_image(img: Image.Image, width: int, height: int = None) -> Image.Image:
    orig_w, orig_h = img.size
    if height is None:
        ratio = orig_h / orig_w
        height = max(1, int(width * ratio * CHAR_ASPECT_CORRECTION))
    return img.resize((width, height))


def pixel_to_char(value: int, charset: str, invert: bool) -> str:
    ramp = charset[::-1] if invert else charset
    index = int(value / 255 * (len(ramp) - 1))
    return ramp[index]


def image_to_ascii(img: Image.Image, width: int, height: int, charset: str, invert: bool, color: bool):
    img = resize_image(img, width, height)
    rgb_img = img.convert("RGB")
    gray_img = img.convert("L")

    lines = []
    w, h = gray_img.size
    gray_pixels = gray_img.load()
    rgb_pixels = rgb_img.load()

    for y in range(h):
        row_chars = []
        for x in range(w):
            gray_val = gray_pixels[x, y]
            ch = pixel_to_char(gray_val, charset, invert)
            if color:
                r, g, b = rgb_pixels[x, y]
                row_chars.append(f"\x1b[38;2;{r};{g};{b}m{ch}\x1b[0m")
            else:
                row_chars.append(ch)
        lines.append("".join(row_chars))
    return "\n".join(lines)


def strip_ansi(text: str) -> str:
    import re
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def main():
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("input", help="Path to an image file, or an http(s) URL")
    parser.add_argument("-w", "--width", type=int, default=100, help="Output width in characters (default: 100)")
    parser.add_argument("--height", type=int, default=None, help="Output height in characters (default: auto, aspect-correct)")
    parser.add_argument(
        "-c", "--charset",
        choices=CHARSETS.keys(),
        default="standard",
        help="Character ramp to use (default: standard)",
    )
    parser.add_argument("--invert", action="store_true", help="Invert light/dark mapping")
    parser.add_argument("--color", action="store_true", help="Output with ANSI 24-bit color (terminal only)")
    parser.add_argument("-o", "--output", help="Write result to this file instead of stdout")
    args = parser.parse_args()

    try:
        img = load_image(args.input)
    except Exception as e:
        print(f"Error loading image '{args.input}': {e}", file=sys.stderr)
        sys.exit(1)

    charset = CHARSETS[args.charset]
    ascii_art = image_to_ascii(img, args.width, args.height, charset, args.invert, args.color)

    if args.output:
        text_to_write = ascii_art if args.color else ascii_art
        with open(args.output, "w", encoding="utf-8") as f:
            # Strip ANSI codes when saving to file unless user wants raw escape codes too;
            # keep color codes in the file so cat/less -R can replay them.
            f.write(text_to_write)
        print(f"Saved ASCII art to {args.output}")
    else:
        print(ascii_art)


if __name__ == "__main__":
    main()
