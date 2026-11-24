#!/usr/bin/env python3
"""Draw the front page that sums up Monday 23 November 2026.

A single 1024x1024 PNG newspaper front page: masthead with the date,
one lead story with a drawn globe, three featured stories with small
pictograms, and the rest of the day as a grid of short headlines.
Pure Pillow, no network, no clock, no randomness: the same run always
writes the same bytes.

Run:  python3 draw_image.py [output-path]
Default output is entry.png next to this file.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
GOLD = (201, 162, 39)
GREEN = (46, 125, 50)
GREY = (96, 90, 78)
FAINT = (203, 195, 179)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731

DATE_LINE = "MONDAY \u00b7 23 NOVEMBER 2026"

# (kicker, headline, summary) for the lead and the three features.
LEAD = (
    "CLIMATE \u00b7 ANTALYA, TURKEY",
    "COP31 ENDS\nWITH NO DEAL",
    "Record-long UN climate talks close without an overall agreement, "
    "split over phasing out fossil fuels and paying for adaptation.",
)

FEATURES = [
    (
        "UKRAINE \u00b7 LIBYA",
        "UKRAINE'S SEA DRONES SINK RUSSIAN SHIP OFF LIBYA",
        "Zelenskyy says seven naval drones sank the corvette Merkury at Benghazi.",
        "drones",
    ),
    (
        "MARKETS \u00b7 TECH",
        "NVIDIA BRINGS BACK HUANG; SHARES JUMP 33%",
        "Eleven days after he resigned, Jensen Huang is CEO again; the S&P 500 rebounds 4.8%.",
        "chip",
    ),
    (
        "EUROPE \u00b7 BRUSSELS",
        "EU PROPOSES 22ND ROUND OF RUSSIA SANCTIONS",
        "60 banks, crypto platforms and 70 shadow-fleet vessels targeted.",
        "stars",
    ),
]

# (kicker, headline) for the rest of the day: 31 stories.
GRID = [
    ("RUSSIA-UKRAINE", "Russian strikes kill at least 15 around Kyiv"),
    ("MIDDLE EAST", "Iran vows 'all means' against US Hormuz blockade"),
    ("MEXICO", "FBI most-wanted 'Chapo Isidro' captured in Sinaloa"),
    ("INDONESIA", "Sweets-factory fire kills at least 24; 30 missing"),
    ("ASIA", "India pledges \u20ac1.4bn to rebuild Nepal after floods"),
    ("SPACE", "BepiColombo enters orbit around Mercury"),
    ("CHINA", "Trump calls Putin 'my friend' after Xi summit"),
    ("USA", "Democrats win 258 House seats, most since 1992"),
    ("SCIENCE", "Anthropic: AI helped prove Riemann hypothesis"),
    ("USA", "Amtrak derails in Louisiana after hitting truck"),
    ("SUDAN", "Drone strikes hit homes and a UN building in Khartoum"),
    ("ISRAEL", "Settler attacks are 'Jewish terrorism', says opposition"),
    ("HEALTH", "NHS to trial AI in breast-cancer screening"),
    ("EUROPE", "Euro-area inflation rises to 4.0%"),
    ("EUROPE", "Finland summons Russian envoy; Moscow warns Estonia"),
    ("EUROPE", "Hungary's PM to visit Transcarpathia"),
    ("NIGERIA", "Tinubu: villa hit by water and power cuts"),
    ("IRAN", "Iran flogs singer Parastoo Ahmadi and band"),
    ("USA", "US sanctions 20+ in Iran shadow-banking network"),
    ("TURKEY", "Thousands rally in Istanbul against crackdown"),
    ("NIGERIA", "Rescue race after deadly boat accident"),
    ("GAZA", "UN staffer killed, three hurt in Israeli strike"),
    ("YEMEN", "Houthi attacks in Taiz kill two, wound eight"),
    ("BRITAIN", "UK voters: rising prices are the top concern"),
    ("EUROPE", "NATO in Berlin warns Russia; space defence pledged"),
    ("ISRAEL", "Netanyahu-Eisenkot coalition talks fail"),
    ("USA", "US tracked Alice Huang's China spy-agency contacts"),
    ("WORLD", "UN chief urges global AI-safety framework in a year"),
    ("MARKETS", "Asian shares slide; Nikkei falls over 5%"),
    ("MARKETS", "Kospi down 3.3% as chip stocks slide"),
    ("WORLD", "US and China agree a new AI dialogue channel"),
]


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, lines, fnt, fill, leading):
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=fnt, fill=fill)
    return y + len(lines) * leading


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def centred(draw, cx, y, text, fnt, fill):
    draw.text((cx - text_w(draw, text, fnt) / 2, y), text, font=fnt, fill=fill)


def star(draw, cx, cy, r, fill):
    """A small four-point star centred on (cx, cy)."""
    pts = [
        (cx, cy - r), (cx + r * 0.28, cy - r * 0.28),
        (cx + r, cy), (cx + r * 0.28, cy + r * 0.28),
        (cx, cy + r), (cx - r * 0.28, cy + r * 0.28),
        (cx - r, cy), (cx - r * 0.28, cy - r * 0.28),
    ]
    draw.polygon(pts, fill=fill)


def pictogram(draw, kind, x, y, s):
    """A small drawn icon inside the square (x, y, s, s)."""
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=2)
    if kind == "drones":
        # Sea, a ship hull, a drone above it and a blast star.
        draw.rectangle([x + 6, y + s - 16, x + s - 6, y + s - 10], fill=BLUE)
        draw.polygon([(x + 10, y + s - 16), (x + s - 10, y + s - 16),
                      (x + s - 18, y + s - 26), (x + 18, y + s - 26)], fill=INK)
        draw.rectangle([x + 24, y + s - 40, x + 30, y + s - 26], fill=INK)
        cx, cy = x + s - 20, y + 16
        draw.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=RED)
        for dx, dy in ((-9, -7), (9, -7), (-9, 7), (9, 7)):
            draw.line([cx + dx * 0.4, cy + dy * 0.4, cx + dx, cy + dy],
                      fill=INK, width=2)
            draw.ellipse([cx + dx - 3, cy + dy - 2, cx + dx + 3, cy + dy + 2],
                         outline=INK, width=1)
        star(draw, x + 16, y + 16, 7, GOLD)
    elif kind == "chip":
        # A processor: dark square, inner die, pins on four sides.
        draw.rectangle([x + 12, y + 12, x + s - 12, y + s - 12], fill=INK)
        draw.rectangle([x + 20, y + 20, x + s - 20, y + s - 20],
                       outline=GOLD, width=2)
        draw.text((x + s / 2 - 7, y + s / 2 - 8), "AI",
                  font=SANS_B(13), fill=GOLD)
        for i in range(3):
            px = x + 20 + i * 8
            draw.line([px, y + 4, px, y + 12], fill=INK, width=2)
            draw.line([px, y + s - 12, px, y + s - 4], fill=INK, width=2)
            py = y + 20 + i * 8
            draw.line([x + 4, py, x + 12, py], fill=INK, width=2)
            draw.line([x + s - 12, py, x + s - 4, py], fill=INK, width=2)
    elif kind == "stars":
        # EU circle of twelve gold stars on blue.
        draw.ellipse([x + 6, y + 6, x + s - 6, y + s - 6], fill=BLUE)
        import math
        cx, cy, r = x + s / 2, y + s / 2, s / 2 - 11
        for i in range(12):
            a = math.pi * 2 * i / 12 - math.pi / 2
            star(draw, cx + r * math.cos(a), cy + r * math.sin(a), 3.5, GOLD)


def draw_globe(draw, cx, cy, r):
    """Earth with a red crack: the climate talks broke down."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180),
                 outline=INK, width=3)
    # Land masses as green blobs.
    draw.ellipse([cx - r * 0.85, cy - r * 0.6, cx - r * 0.05, cy + r * 0.05],
                 fill=GREEN)
    draw.ellipse([cx + r * 0.1, cy - r * 0.05, cx + r * 0.85, cy + r * 0.55],
                 fill=GREEN)
    draw.ellipse([cx - r * 0.35, cy + r * 0.3, cx + r * 0.3, cy + r * 0.85],
                 fill=GREEN)
    draw.ellipse([cx + r * 0.3, cy - r * 0.85, cx + r * 0.8, cy - r * 0.35],
                 fill=GREEN)
    # Small white polar caps.
    draw.ellipse([cx - r * 0.45, cy - r - 1, cx + r * 0.45, cy - r * 0.62],
                 fill=(235, 244, 250))
    draw.ellipse([cx - r * 0.4, cy + r * 0.66, cx + r * 0.4, cy + r + 1],
                 fill=(235, 244, 250))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    # The crack.
    draw.line([(cx - r * 0.5, cy - r * 0.85), (cx - r * 0.1, cy - r * 0.25),
               (cx - r * 0.45, cy + r * 0.1), (cx + r * 0.05, cy + r * 0.55),
               (cx - r * 0.1, cy + r * 0.9)], fill=RED, width=5)


def masthead(draw):
    draw.line([(0, 6), (W, 6)], fill=INK, width=3)
    draw.line([(0, 11), (W, 11)], fill=INK, width=1)
    centred(draw, W / 2, 20, "THE WORLD IN ONE PAGE", SERIF_B(44), INK)
    centred(draw, W / 2, 74, DATE_LINE, SANS_B(20), RED)
    centred(draw, W / 2, 102, "35 stories from every continent \u2014 one day, one page",
            SANS(13), GREY)
    draw.line([(MARGIN, 126), (W - MARGIN, 126)], fill=INK, width=2)
    draw.line([(MARGIN, 130), (W - MARGIN, 130)], fill=INK, width=1)


def lead(draw):
    x, y = MARGIN, 144
    draw.text((x, y), LEAD[0], font=SANS_B(13), fill=RED)
    draw_wrapped(draw, x, y + 24, LEAD[1].split("\n"), SERIF_B(44), INK, 50)
    draw_wrapped(draw, x, y + 128, wrap(LEAD[2], SANS(15), 600), SANS(15), INK, 20)
    # Right-hand art: globe in a framed box with a NO DEAL stamp.
    bx, by, bw, bh = 664, 144, W - MARGIN - 664, 188
    draw.rectangle([bx, by, bx + bw, by + bh], outline=INK, width=2)
    draw_globe(draw, bx + bw / 2, by + 72, 54)
    stamp = "NO DEAL"
    sf = SANS_B(20)
    tw = text_w(draw, stamp, sf)
    sx, sy = bx + bw / 2 - tw / 2 - 8, by + bh - 34
    draw.rectangle([sx, sy, sx + tw + 16, sy + 28], outline=RED, width=3)
    draw.text((sx + 8, sy + 3), stamp, font=sf, fill=RED)
    centred(draw, bx + bw / 2, by + bh - 58,
            "Antalya: two weeks of talks, no deal", SANS(11), GREY)


def features(draw):
    y0 = 356
    col_w = 312
    for i, (kicker, headline, summary, art) in enumerate(FEATURES):
        x = MARGIN + i * (col_w + 16)
        pictogram(draw, art, x, y0, 56)
        draw.text((x + 66, y0 + 4), kicker, font=SANS_B(11), fill=RED)
        draw.text((x + 66, y0 + 22), "FEATURED", font=SANS(10), fill=GREY)
        hy = draw_wrapped(draw, x, y0 + 66, wrap(headline, SANS_B(16), col_w),
                          SANS_B(16), INK, 19)
        draw_wrapped(draw, x, hy + 6, wrap(summary, SANS(12), col_w),
                     SANS(12), INK, 15)
    draw.line([(MARGIN, 344), (W - MARGIN, 344)], fill=INK, width=1)
    draw.line([(MARGIN, 536), (W - MARGIN, 536)], fill=INK, width=2)


def grid(draw):
    y0 = 550
    draw.text((MARGIN, y0), "AROUND THE WORLD \u2014 31 MORE STORIES",
              font=SANS_B(13), fill=INK)
    draw.text((W - MARGIN - text_w(draw, "23 NOVEMBER 2026", SANS_B(13)), y0),
              "23 NOVEMBER 2026", font=SANS_B(13), fill=RED)
    top = y0 + 26
    cols, rows = 4, 8
    cw = (W - 2 * MARGIN - (cols - 1) * 12) // cols
    rh = 49
    for idx, (kicker, headline) in enumerate(GRID):
        r, c = divmod(idx, cols)
        x = MARGIN + c * (cw + 12)
        y = top + r * rh
        draw.text((x, y), kicker, font=SANS_B(10), fill=BLUE)
        size = 13
        lines = wrap(headline, SANS_B(size), cw)
        while len(lines) > 2 and size > 10:
            size -= 1
            lines = wrap(headline, SANS_B(size), cw)
        if len(lines) > 2:
            lines = lines[:2]
            lines[1] = lines[1][:-3].rstrip() + "\u2026"
        draw_wrapped(draw, x, y + 13, lines, SANS_B(size), INK, 15)
        if c:
            draw.line([(x - 6, y), (x - 6, y + rh - 8)], fill=FAINT, width=1)
        if r:
            draw.line([(x, y - 5), (x + cw, y - 5)], fill=FAINT, width=1)
    return top + rows * rh


def footer(draw, y):
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    centred(draw, W / 2, y + 10,
            "MONDAY 23 NOVEMBER 2026 \u00b7 35 STORIES \u00b7 AS REPORTED THAT DAY",
            SANS_B(11), INK)
    centred(draw, W / 2, y + 28,
            "Made for make.fun \u2014 Sum up 23 November's world news in one image",
            SANS(10), GREY)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    lead(draw)
    features(draw)
    end = grid(draw)
    footer(draw, end + 8)
    return img


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "entry.png"
    img = build()
    img.save(out, format="PNG")
    out.chmod(0o644)
    print(f"wrote {out} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
