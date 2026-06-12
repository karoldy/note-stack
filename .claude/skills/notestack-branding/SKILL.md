---
name: notestack-branding
description: >-
  Regenerate or update NoteStack brand images (favicon, logo, icon).
  Use this skill whenever the user wants to recreate, redesign, refresh,
  or generate the NoteStack icon, logo, favicon, or brand images in
  docs/public/. Also use when the user mentions rspress-icon,
  rspress-light-logo, rspress-dark-logo, or wants to tweak the site's
  visual branding.
---

# NoteStack Brand Image Generator

Generate the three NoteStack brand images that live in `docs/public/`:

| File | Dimensions | Use |
|---|---|---|
| `rspress-icon.png` | 1280×1214 | Favicon / app icon |
| `rspress-light-logo.png` | 365×95 | Nav logo (light mode) |
| `rspress-dark-logo.png` | 365×95 | Nav logo (dark mode) |

## Color Palette

```
Navy   #1E3246    Peach  #F0BE96    Gold   #E6D2AA
Coral  #F0826E    Blue   #78BEFA    Brown  #503C3C
Yellow #FAE664    White  #FAFAFA
```

## Workflow

### 1. Understand the design philosophy

Read `design-philosophy.md` at the project root for the "Stratified Warmth"
aesthetic that drives the visual language — layered cards, geological strata
metaphor, warm-to-cool chromatic progression, generous negative space.

### 2. Generate the images

Run the project's generation script:

```bash
python3 scripts/generate-brand-images.py
```

This writes all three PNGs directly to `docs/public/`. Requires **Pillow**
(`pip3 install Pillow`). The script loads fonts from the canvas-design skill
at `~/.claude/skills/canvas-design/canvas-fonts/` if available.

### 3. Verify

```bash
python3 -c "
from PIL import Image
for f in ['rspress-icon.png','rspress-light-logo.png','rspress-dark-logo.png']:
    img = Image.open(f'docs/public/{f}')
    print(f'{f}: {img.size}')
"
```

### 4. Preview (optional)

```bash
npx rspress dev
```

## When things go wrong

- **Pillow missing**: `pip3 install Pillow`
- **Fonts missing**: script falls back to default PIL font
- **Wrong colors**: edit the palette at the top of `scripts/generate-brand-images.py`
- **Composition off**: tweak the card configs or logo positioning in the same script

## Design summary

The icon centers on a card stack of 10 overlapping rounded rectangles with
horizontal offsets creating a stratum rhythm. A blue diamond floats above as
a "knowledge crystal", with coral ribbon, golden arcs, accent dots, and corner
registration marks framing the composition. The logo pairs a condensed 3-card
mark with the "NoteStack" wordmark — navy `#1E3246` for light mode, white
`#FAFAFA` for dark mode.
