# ascii-art-cli

Convert any image (local file or URL) to ASCII art, right in your terminal.

## Install

```bash
uv sync
```

Requires Python 3.11+, Pillow, and certifi.

## Usage

```bash
uv run python ascii_art.py INPUT [options]
```

### Examples

```bash
# Basic
uv run python ascii_art.py photo.jpg

# Wider output, full color (true-color ANSI, terminal only)
uv run python ascii_art.py photo.jpg --width 120 --color

# Block-shaded charset, inverted, saved to a file
uv run python ascii_art.py photo.jpg --charset blocks --invert -o out.txt

# Straight from a URL
uv run python ascii_art.py https://example.com/image.png --width 80
```

### Options

| Flag | Description |
|---|---|
| `-w, --width N` | Output width in characters (default: 100) |
| `--height N` | Output height in characters (default: auto, aspect-corrected) |
| `-c, --charset {standard,detailed,blocks,simple}` | Character ramp to use (default: standard) |
| `--invert` | Invert light/dark mapping |
| `--color` | 24-bit ANSI color output (terminal only) |
| `-o, --output FILE` | Write result to a file instead of stdout |

## Notes

- Character cells in a terminal are taller than wide, so height is corrected by a fixed factor (0.55) when auto-computed from the image aspect ratio.
- `--color` output embeds ANSI escape codes; it looks right in a terminal (or `less -R`) but will show raw escape codes in a plain text viewer.
