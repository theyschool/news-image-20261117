#!/usr/bin/env python3
"""Render the news-image-20261117 poster: 'THE WORLD IN ONE DAY',
Tuesday 17 November 2026. All text is drawn with real fonts
(Liberation Serif/Sans); every illustration is drawn with PIL
primitives. No AI-generated imagery, no network. Deterministic:
same input, same bytes out."""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 247, 240)
INK = (26, 26, 26)
NAVY = (15, 42, 74)
NAVY_DARK = (10, 30, 54)
GOLD = (232, 184, 75)
RED = (185, 28, 28)
GRAY = (110, 110, 105)
RULE = (200, 192, 178)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def draw_tracked(draw, xy, s, f, fill, tracking=0):
    """Draw text with manual letter tracking (PIL has no tracking)."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x


def wrap(draw, s, f, max_w):
    """Greedy word wrap to lines fitting max_w."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, s, f, fill, tracking=0):
    w = sum(draw.textlength(ch, font=f) + tracking for ch in s) - tracking
    draw_tracked(draw, (cx - w / 2, y), s, f, fill, tracking)
    return w

# ---------------------------------------------------------------- illustrations
# Every picture is drawn from primitives: flat colour, bold shapes, no text.

def ill_bridge(draw, box):
    """Lead: the Kerch bridge, its road arch collapsed into the strait."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # dusk sky
    draw.rectangle(box, fill=(232, 222, 200))
    # sun low on the horizon
    sx, sy = x0 + int(w * 0.78), y0 + int(h * 0.22)
    draw.ellipse([sx - 18, sy - 18, sx + 18, sy + 18], fill=(232, 184, 75))
    # sea
    sea = y0 + int(h * 0.72)
    draw.rectangle([x0, sea, x1, y1], fill=(110, 168, 205))
    for i, wy in enumerate((0.80, 0.88)):
        yy = y0 + int(h * wy)
        draw.line([(x0 + 8, yy), (x1 - 8, yy)], fill=(255, 255, 255), width=3)
    # bridge deck: left span intact, middle span fallen, right span intact
    deck = y0 + int(h * 0.42)
    dk = (38, 52, 74)
    draw.rectangle([x0 + 8, deck, x0 + int(w * 0.38), deck + 10], fill=dk)
    draw.rectangle([x0 + int(w * 0.62), deck, x1 - 8, deck + 10], fill=dk)
    # fallen span, tilted down into the water
    draw.polygon([(x0 + int(w * 0.38), deck + 2),
                  (x0 + int(w * 0.58), deck + 2),
                  (x0 + int(w * 0.55), deck + int(h * 0.26)),
                  (x0 + int(w * 0.40), deck + int(h * 0.24))], fill=dk)
    # arch: left half standing, right half broken off
    cx, cy = x0 + int(w * 0.50), deck
    draw.arc([cx - int(w * 0.30), cy - int(h * 0.30),
              cx + int(w * 0.30), cy + int(h * 0.30)],
             start=180, end=270, fill=(185, 28, 28), width=8)
    # broken arch fragment sinking
    draw.arc([x0 + int(w * 0.52), deck + int(h * 0.10),
              x0 + int(w * 0.72), deck + int(h * 0.30)],
             start=250, end=330, fill=(185, 28, 28), width=8)
    # support pillars
    for fx in (0.10, 0.34, 0.66, 0.90):
        px = x0 + int(w * fx)
        draw.rectangle([px - 5, deck + 10, px + 5, sea], fill=(70, 70, 70))
    # splash where the span fell
    for dx, dy in ((0.48, 0.70), (0.52, 0.74), (0.56, 0.70)):
        draw.ellipse([x0 + int(w * dx) - 4, y0 + int(h * dy) - 4,
                      x0 + int(w * dx) + 4, y0 + int(h * dy) + 4],
                     fill=(255, 255, 255))
    # smoke plume from the strike
    for i, (fx, fy, r) in enumerate(((0.485, 0.30, 9), (0.515, 0.21, 11), (0.545, 0.13, 8))):
        draw.ellipse([x0 + int(w * fx) - r, y0 + int(h * fy) - r,
                      x0 + int(w * fx) + r, y0 + int(h * fy) + r],
                     fill=(120, 120, 115))


def ill_gulf(draw, box):
    """Gulf: radar dish sweeping, hostile drones overhead, shield below.
    Fixed sizes scale with the box so the picture reads in the large
    lead slot as well as in a grid cell."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sc = min(w, h) / 168.0
    draw.rectangle(box, fill=(245, 232, 200))
    cx, cy = x0 + w // 2, y0 + int(h * 0.62)
    # signal arcs
    for r in (34, 52, 70):
        r = int(r * sc)
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340,
                 fill=(46, 125, 50), width=max(2, int(4 * sc)))
    # radar dish
    R = int(46 * sc)
    draw.pieslice([cx - R, cy - R, cx + R, cy + R], start=180, end=360,
                  fill=(70, 70, 70))
    draw.rectangle([cx - int(4 * sc), cy, cx + int(4 * sc), cy + int(34 * sc)],
                   fill=(70, 70, 70))
    draw.rectangle([cx - int(26 * sc), cy + int(34 * sc),
                    cx + int(26 * sc), cy + int(40 * sc)], fill=(70, 70, 70))
    # drones
    def drone(dx, dy, s):
        s = max(4, int(s * sc))
        draw.ellipse([dx - s, dy - s // 2, dx + s, dy + s // 2], fill=(26, 26, 26))
        draw.line([(dx - s - 6, dy - s // 2 - 4), (dx + s + 6, dy - s // 2 - 4)],
                  fill=(26, 26, 26), width=2)
        draw.line([(dx - s - 6, dy + s // 2 + 4), (dx + s + 6, dy + s // 2 + 4)],
                  fill=(26, 26, 26), width=2)
        draw.line([(dx, dy - s), (dx, dy + 8)], fill=(26, 26, 26), width=2)
    drone(x0 + int(w * 0.24), y0 + int(h * 0.20), 12)
    drone(x0 + int(w * 0.76), y0 + int(h * 0.14), 10)
    drone(x0 + int(w * 0.55), y0 + int(h * 0.30), 8)
    # interception burst
    bx, by = x0 + int(w * 0.76), y0 + int(h * 0.14)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        draw.line([(bx + 16 * sc * math.cos(a), by + 16 * sc * math.sin(a)),
                   (bx + 26 * sc * math.cos(a), by + 26 * sc * math.sin(a))],
                  fill=(185, 28, 28), width=3)


def ill_plane(draw, box):
    """Diplomacy: jet crossing a globe."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(220, 232, 240))
    cx, cy, r = x0 + w // 2, y0 + int(h * 0.62), int(min(w, h) * 0.30)
    # globe
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 90, 136))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=3)
    for k in (-0.55, 0, 0.55):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=270 + k * 90, end=270 + k * 90 + 180,
                 fill=(255, 255, 255), width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=2)
    draw.arc([cx - int(r * 0.55), cy - int(r * 0.32), cx + int(r * 0.55), cy + int(r * 0.32)],
             start=0, end=360, fill=(255, 255, 255), width=2)
    # jet: clean side profile in the sky above the globe
    jx, jy = x0 + int(w * 0.10), y0 + int(h * 0.10)
    # fuselage: long tapered body, nose to the right
    draw.polygon([(jx, jy + 6), (jx + 58, jy), (jx + 76, jy + 4), (jx + 76, jy + 8),
                  (jx + 58, jy + 12), (jx, jy + 12)], fill=(26, 26, 26))
    # main wing sweeping down-back
    draw.polygon([(jx + 30, jy + 10), (jx + 44, jy + 10), (jx + 34, jy + 30), (jx + 24, jy + 30)],
                 fill=(26, 26, 26))
    # tail fin
    draw.polygon([(jx + 4, jy + 8), (jx + 12, jy - 10), (jx + 18, jy - 10), (jx + 16, jy + 8)],
                 fill=(26, 26, 26))
    # flight path dashes behind the jet
    for i in range(3):
        px = jx + 84 + i * 16
        draw.line([(px, jy + 6), (px + 9, jy + 6)], fill=(110, 110, 105), width=2)


def ill_jet(draw, box):
    """Airspace: a fighter jet scrambling past a red rising sun."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(224, 232, 240))
    # rising sun
    cx, cy = x0 + int(w * 0.72), y0 + int(h * 0.34)
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(185, 28, 28))
    # clouds
    for fx, fy in ((0.18, 0.78), (0.45, 0.86), (0.72, 0.80)):
        ex, ey = x0 + int(w * fx), y0 + int(h * fy)
        draw.ellipse([ex - 22, ey - 8, ex + 22, ey + 8], fill=(255, 255, 255))
    # fighter jet, nose up-right
    jx, jy = x0 + int(w * 0.06), y0 + int(h * 0.42)
    draw.polygon([(jx, jy + 10), (jx + 52, jy), (jx + 72, jy + 6), (jx + 72, jy + 12),
                  (jx + 52, jy + 18), (jx, jy + 16)], fill=(26, 26, 26))
    # swept wing
    draw.polygon([(jx + 26, jy + 14), (jx + 42, jy + 14), (jx + 30, jy + 34), (jx + 20, jy + 34)],
                 fill=(26, 26, 26))
    # tail fin
    draw.polygon([(jx + 2, jy + 12), (jx + 10, jy - 8), (jx + 16, jy - 8), (jx + 14, jy + 12)],
                 fill=(26, 26, 26))
    # second jet, smaller, behind
    jx2, jy2 = x0 + int(w * 0.30), y0 + int(h * 0.62)
    draw.polygon([(jx2, jy2 + 6), (jx2 + 34, jy2), (jx2 + 46, jy2 + 4), (jx2 + 46, jy2 + 8),
                  (jx2 + 34, jy2 + 12), (jx2, jy2 + 10)], fill=(70, 70, 70))
    # contrail dashes
    for i in range(3):
        px = jx + 80 + i * 14
        draw.line([(px, jy + 8), (px + 8, jy + 8)], fill=(110, 110, 105), width=2)


def ill_sudan(draw, box):
    """Sudan: a drone over desert ground, a rising toll chart."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(240, 228, 200))
    # desert sun
    sx, sy = x0 + int(w * 0.22), y0 + int(h * 0.22)
    draw.ellipse([sx - 18, sy - 18, sx + 18, sy + 18], fill=(232, 184, 75))
    # dunes
    base = y0 + int(h * 0.78)
    draw.polygon([(x0, base), (x0 + int(w * 0.35), y0 + int(h * 0.62)),
                  (x0 + int(w * 0.70), base)], fill=(214, 186, 140))
    draw.rectangle([x0, base, x1, y1], fill=(190, 158, 110))
    # drone silhouette in the sky
    dx, dy = x0 + int(w * 0.62), y0 + int(h * 0.30)
    s = 12
    draw.ellipse([dx - s, dy - s // 2, dx + s, dy + s // 2], fill=(26, 26, 26))
    draw.line([(dx - s - 7, dy - s // 2 - 4), (dx + s + 7, dy - s // 2 - 4)],
              fill=(26, 26, 26), width=2)
    draw.line([(dx - s - 7, dy + s // 2 + 4), (dx + s + 7, dy + s // 2 + 4)],
              fill=(26, 26, 26), width=2)
    # rising toll bars, low to high
    bx = x0 + int(w * 0.10)
    bbase = y0 + int(h * 0.90)
    for i, bh in enumerate((14, 24, 38, 56)):
        draw.rectangle([bx + i * 20, bbase - bh, bx + i * 20 + 13, bbase],
                       fill=(185, 28, 28))

# ---------------------------------------------------------------- composition

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 172], fill=RED)
    f_kick = font(SANS_BOLD, 25)
    draw_centered(d, W // 2, 24, "T H E   W O R L D   I N   O N E   D A Y",
                  f_kick, GOLD, tracking=2)
    f_date = font(SERIF, 58)
    draw_centered(d, W // 2, 62, "TUESDAY 17 NOVEMBER 2026", f_date, (255, 255, 255))
    d.line([(W // 2 - 330, 132), (W // 2 + 330, 132)], fill=GOLD, width=2)
    f_sub = font(SANS, 21)
    draw_centered(d, W // 2, 146, "Five stories that defined the day  —  from Crimea to Bahrain to Tokyo",
                  f_sub, (200, 214, 228))

    # --- lead story: Crimea bridge falls ---
    ill_bridge(d, (24, 196, 400, 454))
    d.rectangle([24, 196, 400, 454], outline=INK, width=2)
    tx = 424
    f_lkick = font(SANS_BOLD, 20)
    draw_tracked(d, (tx, 198), "UKRAINE  •  RUSSIA", f_lkick, RED, tracking=1)
    f_lhead = font(SERIF, 45)
    d.text((tx, 226), "CRIMEA BRIDGE", font=f_lhead, fill=INK)
    d.text((tx, 272), "FALLS INTO SEA", font=f_lhead, fill=INK)
    f_lbody = font(SANS, 23)
    lead = ("Ukraine strikes the Kerch bridge for a second straight "
            "day; the road arch collapses into the strait and traffic "
            "halts. Russia hits Kyiv's bridges in reply.")
    y = 330
    for line in wrap(d, lead, f_lbody, 1000 - tx - 8):
        d.text((tx, y), line, font=f_lbody, fill=INK)
        y += 30
    f_lfoot = font(SANS_BOLD, 19)
    d.text((tx, 428), "Two killed; road and rail traffic suspended",
           font=f_lfoot, fill=GRAY)

    # --- divider ---
    d.line([(24, 478), (1000, 478)], fill=RULE, width=2)

    # --- four stories, 2 x 2 grid ---
    stories = [
        ("MIDDLE EAST  •  SECURITY", "BAHRAIN DRONES",
         "Iran fires drones at a US radar base in Bahrain; the attack "
         "is intercepted, with no casualties or damage reported.",
         ill_gulf, (46, 125, 50)),
        ("ASIA  •  AIRSPACE", "JETS SCRAMBLED",
         "Japan launches fighter jets and protests after two suspected "
         "Russian aircraft violate its airspace early on Tuesday.",
         ill_jet, (185, 28, 28)),
        ("AFRICA  •  SUDAN", "SUDAN'S TOLL",
         "A UN report counts 2,230 civilians killed this year, over "
         "1,630 by drones; Kordofan bears two-thirds of the toll.",
         ill_sudan, (185, 28, 28)),
        ("US  •  DIPLOMACY", "TRUMP TO ASIA",
         "The president flies to Asia ahead of Thursday's Shenzhen "
         "summit with Xi and Putin; the Ukraine war tops the agenda.",
         ill_plane, (15, 42, 74)),
    ]
    f_ckick = font(SANS_BOLD, 18)
    f_chead = font(SERIF, 31)
    f_cbody = font(SANS, 20)
    cell_w, cell_h = 476, 236
    for i, (kick, head, body, ill, col) in enumerate(stories):
        cx0 = 24 + (i % 2) * (cell_w + 24)
        cy0 = 496 + (i // 2) * (cell_h + 16)
        # illustration, left
        ill(d, (cx0, cy0, cx0 + 168, cy0 + 168))
        d.rectangle([cx0, cy0, cx0 + 168, cy0 + 168], outline=INK, width=2)
        tx2 = cx0 + 184
        tw = cx0 + cell_w - tx2
        draw_tracked(d, (tx2, cy0 + 2), kick, f_ckick, col, tracking=1)
        d.text((tx2, cy0 + 28), head, font=f_chead, fill=INK)
        y = cy0 + 70
        for line in wrap(d, body, f_cbody, tw):
            d.text((tx2, y), line, font=f_cbody, fill=INK)
            y += 26

    # --- footer ---
    d.line([(24, 984), (1000, 984)], fill=RULE, width=2)
    f_foot = font(SANS, 16)
    draw_centered(d, W // 2, 992,
                  "Sources: Reuters, Associated Press, OHCHR, Just Security  •  17 November 2026",
                  f_foot, GRAY)
    return img


if __name__ == "__main__":
    render().save("entry.png", "PNG")
    print("wrote entry.png")
