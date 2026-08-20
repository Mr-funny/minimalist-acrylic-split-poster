# Minimalist Acrylic Split Poster

A reusable Codex Skill for turning each reference photo into its own premium 3:4 split editorial poster:

- the upper 50% preserves the original photograph with restrained editorial grading;
- the lower 50% reinterprets the same subject with a selectable visual style;
- titles, years, numbers, archive labels, and layout geometry are rendered deterministically with FFmpeg rather than generated as unreliable image text.

The upper photograph is never redrawn by ImageGen. When its aspect ratio does not fill the panel, the compositor keeps the complete original image in the foreground and uses a blurred copy of the same photo only as an edge extension.

## Included styles

1. East Asian negative-space acrylic storybook
2. `LAKESIDE TERRAIN` premium minimalist geometric editorial abstraction
3. Architectural collage, screen print, and blueprint
4. Travel-memory watercolor field note
5. Architectural travel sketchbook
6. Naive retro hand-drawn editorial illustration

Each style is isolated in its own prompt reference so visual languages are not mixed accidentally.

## Repository structure

```text
skills/minimalist-acrylic-split-poster/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/compose_split_poster.py
```

## Installation

Clone the repository and copy the Skill into your Codex skills directory:

```bash
git clone https://github.com/Mr-funny/minimalist-acrylic-split-poster.git
cp -R minimalist-acrylic-split-poster/skills/minimalist-acrylic-split-poster ~/.codex/skills/
```

Restart or reload Codex after installation.

## Requirements

- Python 3.10+
- FFmpeg with the `drawtext` filter
- Codex built-in ImageGen for generating the lower artwork
- macOS system fonts are used as defaults by the compositor

On another operating system, pass compatible font files with `--title-font`, `--text-font`, `--script-font`, or `--naive-font`.

## Compositor example

```bash
python3 skills/minimalist-acrylic-split-poster/scripts/compose_split_poster.py \
  --top /absolute/path/to/original.jpg \
  --bottom /absolute/path/to/styled-artwork.png \
  --output /absolute/path/to/poster.png \
  --type-layout panel-top-left \
  --title "LAKESIDE TERRAIN" \
  --left-meta "No. 01" \
  --right-meta "2026" \
  --top-grain 2
```

The output defaults to 1536×2048 with an exact 50:50 split.

## License

MIT. See [LICENSE](LICENSE).
