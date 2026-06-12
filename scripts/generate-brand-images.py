"""
NoteStack Brand Image Generator — Refined
Stratified Warmth philosophy: layered knowledge, chromatic depth, geometric precision.
Every pixel considered, every element placed with master-level care.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

# ── Color Palette ──
NAVY    = (0x1E, 0x32, 0x46, 255)
PEACH   = (0xF0, 0xBE, 0x96, 255)
GOLD    = (0xE6, 0xD2, 0xAA, 255)
CORAL   = (0xF0, 0x82, 0x6E, 255)
BLUE    = (0x78, 0xBE, 0xFA, 255)
BROWN   = (0x50, 0x3C, 0x3C, 255)
YELLOW  = (0xFA, 0xE6, 0x64, 255)
WHITE   = (0xFA, 0xFA, 0xFA, 255)

# Refined variants
PEACH_LIGHT = (0xF6, 0xCF, 0xAD, 255)
GOLD_LIGHT  = (0xF2, 0xE0, 0xBE, 255)
GOLD_DARK   = (0xD4, 0xBC, 0x8C, 255)
NAVY_DARK   = (0x14, 0x24, 0x36, 255)
NAVY_LIGHT  = (0x32, 0x4C, 0x64, 255)
BLUE_LIGHT  = (0xA8, 0xD6, 0xFC, 255)
BLUE_DARK   = (0x58, 0x9E, 0xE0, 255)
CORAL_LIGHT = (0xF6, 0xA4, 0x92, 255)
CORAL_DARK  = (0xE0, 0x6A, 0x56, 255)
BROWN_LIGHT = (0x6E, 0x54, 0x54, 255)

OUTPUT_DIR = '/Users/turbo.su/Project/note-stack/docs/public'
FONT_DIR   = '/Users/turbo.su/.claude/skills/canvas-design/canvas-fonts'

def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(4))

def create_canvas(w, h):
    return Image.new('RGBA', (w, h), (0, 0, 0, 0))

def rc(cx, cy, w, h, r):
    """Rounded rect bbox from center: (x0, y0, x1, y1, radius)."""
    return (cx - w//2, cy - h//2, cx + w//2, cy + h//2, r)

def rr(draw, bbox, fill, outline=None, w=0):
    x0, y0, x1, y1, r = bbox
    draw.rounded_rectangle((x0, y0, x1, y1), radius=r, fill=fill, outline=outline, width=w)

def dot(draw, x, y, r, color):
    draw.ellipse((x-r, y-r, x+r, y+r), fill=color)

def line(draw, x0, y0, x1, y1, color, width=2):
    draw.line((x0, y0, x1, y1), fill=color, width=width)


# ═══════════════════════════════════════════════════════════════
# ICON  (1280 × 1214)
# ═══════════════════════════════════════════════════════════════

def create_icon():
    W, H = 1280, 1214
    img = create_canvas(W, H)
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2

    # ── Soft atmospheric halo ──
    for r in range(420, 280, -3):
        alpha = int(10 * (1 - (420 - r) / 140))
        if alpha > 0:
            d.ellipse((cx - r, cy - r + 50, cx + r, cy + r + 50),
                      fill=(GOLD[0], GOLD[1], GOLD[2], alpha))

    # ── Constellation of small dots (upper region) ──
    import random
    random.seed(47)
    for _ in range(28):
        angle = random.uniform(0.15, math.pi - 0.15)
        dist = random.uniform(230, 440)
        px = int(cx + dist * math.cos(angle))
        py = int(cy - dist * math.sin(angle) + 60)
        size = random.uniform(2.5, 7)
        alpha = random.randint(50, 140)
        c = random.choice([GOLD, BLUE, CORAL, YELLOW])
        dot(d, px, py, size, (*c[:3], alpha))

    # ── THE CARD STACK — the heart of the composition ──
    # Each card is a stratum; together they form a geological core sample
    # of knowledge. Widths peak at center, colors transition warm→cool.
    cards = [
        # (y_off, width, height, color, x_off, radius)
        (-210, 480, 150, BROWN_LIGHT,  30, 20),  # base — earth
        (-158, 520, 148, BROWN,       -25, 21),
        (-108, 560, 146, NAVY_DARK,    35, 22),  # deep stratum
        (-60,  600, 144, NAVY,        -20, 22),
        (-15,  630, 142, NAVY_LIGHT,   28, 23),  # transition
        (28,   640, 140, PEACH,       -32, 23),  # warm heart
        (68,   620, 138, GOLD_DARK,    20, 22),
        (105,  580, 132, GOLD,        -18, 21),
        (140,  520, 124, GOLD_LIGHT,   25, 20),
        (172,  440, 110, YELLOW,      -10, 18),  # top — light
    ]

    for y_off, cw, ch, color, x_off, radius in cards:
        card_x = cx + x_off
        card_y = cy + y_off

        # Main card body
        rr(d, rc(card_x, card_y, cw, ch, radius), color)

        # Inner luminous line — like the edge of a page
        im = 12
        inner_color = lerp(color, (255, 255, 255, 50), 0.18)
        rr(d, rc(card_x, card_y, cw - im*2, ch - im*2, max(3, radius - 5)), inner_color)

    # ── Floating crystal (knowledge ascending) ──
    crystal_y = cy - 300
    cs = 48  # crystal size
    pts = [
        (cx, crystal_y - cs),
        (cx + int(cs * 0.55), crystal_y + int(cs * 0.05)),
        (cx + int(cs * 0.08), crystal_y + int(cs * 0.55)),
        (cx - int(cs * 0.08), crystal_y + int(cs * 0.55)),
        (cx - int(cs * 0.55), crystal_y + int(cs * 0.05)),
    ]
    d.polygon(pts, fill=BLUE)
    # Inner facet
    inner_pts = [
        (cx, crystal_y - cs + 14),
        (cx + int(cs * 0.35), crystal_y + int(cs * 0.10)),
        (cx, crystal_y + int(cs * 0.35)),
        (cx - int(cs * 0.35), crystal_y + int(cs * 0.10)),
    ]
    d.polygon(inner_pts, fill=BLUE_LIGHT)

    # ── Vertical ribbon/bookmark — a thread of continuity ──
    rx = cx + 185
    ry_top = cy - 90
    ry_bot = cy + 180
    ribbon = [
        (rx - 13, ry_top),
        (rx + 13, ry_top),
        (rx + 9, ry_bot - 18),
        (rx, ry_bot),
        (rx - 9, ry_bot - 18),
    ]
    d.polygon(ribbon, fill=CORAL)
    # Subtle ribbon highlight
    highlight = [
        (rx - 5, ry_top + 10),
        (rx + 5, ry_top + 10),
        (rx + 4, ry_top + 60),
        (rx - 4, ry_top + 60),
    ]
    d.polygon(highlight, fill=CORAL_LIGHT)

    # ── Accent dots: a descending rhythm on the right ──
    for i in range(6):
        dy = cy - 140 + i * 52
        dx = cx + 370
        size = 5.5 - abs(i - 2.5) * 0.7
        alpha = 190 - abs(i - 2.5) * 28
        dot(d, dx, dy, max(2.5, size), (*CORAL[:3], int(alpha)))

    # ── Left-side golden arcs: memory of turning pages ──
    for i in range(4):
        ay = cy - 80 + i * 68
        ax = cx - 355
        ar = 16 - i * 2
        d.arc((ax - ar, ay - ar, ax + ar, ay + ar), 0, 180, fill=GOLD, width=2)

    # ── Bottom: a horizontal rule of knowing — punctuated ──
    ry = cy + 440
    rw = 320
    line(d, cx - rw, ry, cx - 35, ry, GOLD_DARK, width=3)
    dot(d, cx - 18, ry, 5, PEACH)
    dot(d, cx, ry, 3.5, CORAL)
    dot(d, cx + 15, ry, 6, GOLD)
    line(d, cx + 33, ry, cx + rw, ry, GOLD_DARK, width=3)

    # ── Corner registration marks — precision framing ──
    co = 180
    cl = 70
    corners = [
        (co, co, 1, 1), (W - co, co, -1, 1),
        (co, H - co, 1, -1), (W - co, H - co, -1, -1),
    ]
    for cpx, cpy, dx, dy in corners:
        line(d, cpx, cpy, cpx + cl * dx, cpy, NAVY_DARK, width=2)
        line(d, cpx, cpy, cpx, cpy + cl * dy, NAVY_DARK, width=2)
        dot(d, cpx, cpy, 3.5, GOLD)

    # ── Sparkles near crystal — moments of insight ──
    sparkles = [
        (cx - 135, crystal_y - 25),
        (cx + 155, crystal_y - 40),
        (cx + 95, crystal_y + 38),
        (cx - 100, crystal_y + 55),
    ]
    random.seed(73)
    for spx, spy in sparkles:
        sz = random.uniform(7, 13)
        alpha = random.randint(130, 210)
        star = [
            (spx, spy - sz),
            (spx + sz * 0.25, spy - sz * 0.25),
            (spx + sz, spy),
            (spx + sz * 0.25, spy + sz * 0.25),
            (spx, spy + sz),
            (spx - sz * 0.25, spy + sz * 0.25),
            (spx - sz, spy),
            (spx - sz * 0.25, spy - sz * 0.25),
        ]
        d.polygon(star, fill=(*YELLOW[:3], alpha))

    return img


# ═══════════════════════════════════════════════════════════════
# LOGO  (365 × 95)
# ═══════════════════════════════════════════════════════════════

def create_logo(text_color, accent_blue):
    W, H = 365, 95
    img = create_canvas(W, H)
    d = ImageDraw.Draw(img)

    # ── Icon mark: condensed card stack + crystal ──
    mx, my = 70, H // 2

    mini_cards = [
        (mx - 2,  my - 4,  36, 11, 4, CORAL),
        (mx + 1,  my + 1,  40, 12, 4, PEACH),
        (mx - 1,  my + 6,  44, 12, 4, GOLD),
    ]
    for cx, cy, cw, ch, r, color in mini_cards:
        rr(d, rc(cx, cy, cw, ch, r), color)
        inner = rc(cx, cy, cw - 8, ch - 8, max(2, r - 2))
        rr(d, inner, lerp(color, (255, 255, 255, 50), 0.22))

    # Crystal above
    cry = my - 18
    cs2 = 9
    pts = [
        (mx, cry - cs2),
        (mx + cs2//2, cry + 1),
        (mx, cry + cs2//2),
        (mx - cs2//2, cry + 1),
    ]
    d.polygon(pts, fill=accent_blue)

    # ── Wordmark — "NoteStack" ──
    tx = 120
    ty = H // 2

    font = None
    for fp in [
        os.path.join(FONT_DIR, 'Outfit-Bold.ttf'),
        os.path.join(FONT_DIR, 'InstrumentSans-Bold.ttf'),
        os.path.join(FONT_DIR, 'WorkSans-Bold.ttf'),
        os.path.join(FONT_DIR, 'BricolageGrotesque-Bold.ttf'),
        os.path.join(FONT_DIR, 'Outfit-Regular.ttf'),
        os.path.join(FONT_DIR, 'InstrumentSans-Regular.ttf'),
    ]:
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, 34)
            break

    text = "NoteStack"
    if font:
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        d.text((tx, ty - th//2 - bbox[1]), text, fill=text_color, font=font)

        # Decorative endpoint dots
        end_x = tx + tw + 18
        dot_color = CORAL if text_color == NAVY else GOLD
        dot(d, end_x, ty - 5, 3.5, dot_color)
        dot(d, end_x + 15, ty + 7, 2.5, accent_blue)

    return img


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Generating icon (1280×1214)...")
    icon = create_icon()
    icon.save(os.path.join(OUTPUT_DIR, 'rspress-icon.png'), 'PNG', optimize=True)
    print("  ✓ rspress-icon.png")

    print("Generating light logo (365×95)...")
    light = create_logo(NAVY, BLUE)
    light.save(os.path.join(OUTPUT_DIR, 'rspress-light-logo.png'), 'PNG', optimize=True)
    print("  ✓ rspress-light-logo.png")

    print("Generating dark logo (365×95)...")
    dark = create_logo(WHITE, BLUE_LIGHT)
    dark.save(os.path.join(OUTPUT_DIR, 'rspress-dark-logo.png'), 'PNG', optimize=True)
    print("  ✓ rspress-dark-logo.png")

    print("\nDone — all three images regenerated.")

if __name__ == '__main__':
    main()
