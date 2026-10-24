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

# Block-shaded charset, force no inversion, saved to a file
uv run python ascii_art.py photo.jpg --charset blocks --no-invert -o out.txt

# Straight from a URL
uv run python ascii_art.py https://example.com/image.png --width 80
```

### Options

| Flag | Description |
|---|---|
| `-w, --width N` | Output width in characters (default: 100) |
| `--height N` | Output height in characters (default: auto, aspect-corrected) |
| `-c, --charset {standard,detailed,blocks,simple}` | Character ramp to use (default: standard) |
| `--invert` | Force-invert light/dark mapping |
| `--no-invert` | Force-disable inversion (overrides auto-detection) |
| `--color` | 24-bit ANSI color output (terminal only) |
| `-o, --output FILE` | Write result to a file instead of stdout |

## Notes

- Character cells in a terminal are taller than wide, so height is corrected by a fixed factor (0.55) when auto-computed from the image aspect ratio.
- `--color` output embeds ANSI escape codes; it looks right in a terminal (or `less -R`) but will show raw escape codes in a plain text viewer.
- **Inversion is auto-detected by default**: the border pixels of the image are sampled, and if the average brightness is high (light background, e.g. a product photo on white) the mapping is auto-inverted so the subject renders as foreground instead of the background swallowing the whole frame. Pass `--invert` or `--no-invert` to override.
