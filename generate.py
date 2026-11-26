#!/usr/bin/env python3
"""Draw the 26 November 2026 front page: 'THE WORLD IN ONE DAY'.

Fresh build, written 2026-11-26 after the competition opened.
Reads nothing at runtime, uses no clock, no network, no randomness:
the same inputs always produce the same PNG bytes.
Run:  python3 generate.py   (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (18, 18, 18)
RED = (178, 30, 30)
BLUE = (28, 68, 128)
GREY = (110, 108, 100)
LIGHT = (238, 232, 216)
DARKBLUE = (16, 32, 64)

SERIF = os.path.join(HERE, "fonts", "DejaVuSerif-Bold.ttf")
SERIF_R = os.path.join(HERE, "fonts", "DejaVuSerif.ttf")
SANS = os.path.join(HERE, "fonts", "DejaVuSans.ttf")
SANS_B = os.path.join(HERE, "fonts", "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped paragraph; returns y after last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def badge(draw, x, y, text, fill=RED):
    """Small filled label; returns width used."""
    f = font(SANS_B, 11)
    w = int(draw.textlength(text, font=f)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 17], radius=3, fill=fill)
    draw.text((x + 6, y + 2), text, font=f, fill=(255, 255, 255))
    return w


def kicker(draw, x, y, text, fill=RED):
    draw.text((x, y), text, font=font(SANS_B, 11), fill=fill)
    return y + 15


# ---------------------------------------------------------------- stories
# region codes: AM Americas, EU Europe, AS Asia, AF Africa, ME Middle East, GL Global
BIG = [
    dict(
        n=1, region="AM", label="CONFIRMED",
        kick="NEW YORK  |  THANKSGIVING",
        head="PARADE POSTPONED",
        sub="100th Macy's march moved to Saturday — first weather delay in its history",
        body=("Macy's moved its 100th Thanksgiving Day Parade to Saturday, "
              "28 November, as a nor'easter bears down on New York — the "
              "first weather postponement in its history. Gusts of 50-60 mph "
              "are forecast; balloons are grounded past 23 mph sustained "
              "or 34 mph gusts."),
        scene="parade", stat="SAT 28 NOV",
    ),
    dict(
        n=2, region="EU", label="REPORTED",
        kick="UKRAINE  |  SAVASLEYKA AIR BASE",
        head="FIVE RUSSIAN JETS HIT",
        sub="Kyiv says 3 MiG-31s and 2 Su-34s damaged 300 km east of Moscow",
        body=("Ukraine's General Staff says a long-range strike on Savasleyka, "
              "300 km east of Moscow, damaged three MiG-31 interceptors — "
              "the jets that carry Kinzhal missiles — and two Su-34 bombers."),
        scene="airfield", stat="5 JETS",
    ),
    dict(
        n=3, region="GL", label="CONFIRMED",
        kick="TRADE  |  WASHINGTON",
        head="TARIFFS LAND ON 14 NATIONS",
        sub="China faces up to 20%, India up to 25%; world stocks slide",
        body=("The White House announced fresh tariffs on 14 trading partners, "
              "including China and the EU, after a probe into excess capacity. "
              "World shares fell 0.5%; Seoul's KOSPI plunged 6.2% and the "
              "Nasdaq slid 4% intraday."),
        scene="chart", stat="KOSPI -6.2%",
    ),
]

SMALL = [
    dict(n=4, region="EU", label="OFFICIAL", kick="BRUSSELS",
         head="EU leaders open Euro Summit",
         body="Euro Summit and special Council meet 26-27 Nov.",
         scene="stars"),
    dict(n=5, region="AS", label="CONFIRMED", kick="MUMBAI",
         head="18 years since 26/11",
         body="India marks the 2008 attacks; 174 people killed.",
         scene="candles"),
    dict(n=6, region="AM", label="OFFICIAL", kick="WASHINGTON",
         head="US data dump lands",
         body="PCE, Q3 GDP, jobless claims, Beige Book out.",
         scene="bars"),
    dict(n=7, region="AM", label="CONFIRMED", kick="MISSISSIPPI",
         head="Six die in Gulf plane crash",
         body="Cessna 210 down off Horn Island; 2 children dead.",
         scene="plane"),
    dict(n=8, region="AS", label="CONFIRMED", kick="SEOUL",
         head="Korea minister quits",
         body="Education chief Choi quits over exam cheating.",
         scene="exam"),
    dict(n=9, region="AS", label="REPORTED", kick="PYONGYANG",
         head="N. Korea orders Swiss out",
         body="Kim Yo-jong wants Swiss office in Pyongyang shut.",
         scene="flags"),
    dict(n=10, region="AM", label="CONFIRMED", kick="MADRID",
         head="Abrego Garcia reaches Spain",
         body="Leaves US voluntarily; hopes to return after Trump.",
         scene="spain"),
    dict(n=11, region="AM", label="CONFIRMED", kick="CARTAGENA",
         head="Siege ends, hostages free",
         body="Police raid frees all ~30 after 17 hours; 1 dead.",
         scene="siege"),
    dict(n=12, region="AM", label="CONFIRMED", kick="BRAZIL",
         head="Mosquitoes cut virus 68%",
         body="Wolbachia releases slash viral infections by 68%.",
         scene="mosquito"),
    dict(n=13, region="AS", label="CONFIRMED", kick="NEW DELHI",
         head="India space boom: $45bn",
         body="Space economy to hit $45bn in a decade.",
         scene="rocket"),
]

BRIEFS = [
    ("CANADA", "Ottawa reaffirms its inflation strategy as prices cool."),
    ("USA", "Consumer confidence nears a two-year high before the holidays."),
    ("EL SALVADOR", "Lines up $860m in debt financing for the new year."),
    ("BARBADOS", "Sets a February deadline for Caribbean AI rules."),
    ("VENEZUELA", "Reveals $237.5bn in public debt as talks continue."),
    ("ETHIOPIA", "Champions healthcare independence with local production."),
    ("EGYPT", "Suez Canal revenues gradually recovering, officials say."),
    ("IRAN", "Confronts deepening financial hardship as rial slides."),
    ("FRANCE", "Seeks independence in critical minerals supply."),
    ("BRITAIN", "Probes the legacy of its nuclear weapons tests."),
    ("POLAND", "Alarmed by renewed airspace violations on its border."),
    ("RUSSIA", "Raises defence allocations in next year's budget."),
    ("UKRAINE", "Renews economic cooperation with Hungary."),
    ("S. KOREA", "Moves to reinforce its electric-vehicle industry."),
    ("EMIRATES", "Tops the global airline rankings for a second year."),
    ("SPACE", "Close-up images of the DART-hit asteroid due out soon."),
    ("USA", "Attorney general dodges questions on the Nvidia probe."),
    ("MEXICO", "Probes cartel links of a prosecutor who aided the CIA."),
    ("USA", "Thanksgiving travel: FAA queue rule, airline waivers in force."),
    ("NATO", "Vows space defence amid reports of a Russian nuclear satellite. CLAIM"),
    ("GERMANY", "GfK consumer confidence out for December."),
    ("ECB", "Publishes accounts of its monetary policy meeting."),
    ("USA", "Thanksgiving costs: turkey up, cannabis cheaper this year."),
    ("USA", "Trump pardons turkeys Freedom and Feathers at the White House."),
    ("SENEGAL", "Reinstated as Africa Cup of Nations champions by top court."),
]

STATS = [
    ("100TH", "parade moved\nto Sat 28 Nov"),
    ("-0.5%", "MSCI world\nstocks fall"),
    ("-6.2%", "KOSPI plunge\nin Seoul"),
    ("$3,550", "gold holds\nnear record"),
    ("$93.28", "Brent crude\nrises 2%"),
    ("5", "Russian jets\nKyiv says hit"),
]

REGIONS = [("AMERICAS", "AM"), ("EUROPE", "EU"), ("ASIA", "AS"),
           ("AFRICA", "AF"), ("MIDDLE EAST", "ME"), ("GLOBAL", "GL")]

# map pins: (number, name, x, y) on a 1024-wide map strip
PINS = [
    (1, "New York", 250, 30), (2, "Savasleyka", 600, 14),
    (3, "Washington", 235, 50), (4, "Brussels", 472, 32),
    (5, "Mumbai", 702, 62), (6, "Mississippi", 200, 68),
    (7, "Seoul", 855, 44), (8, "Pyongyang", 828, 24),
    (9, "Madrid", 452, 48), (10, "Cartagena", 272, 74),
    (11, "New Delhi", 660, 40), (12, "London", 430, 12),
]


# ---------------------------------------------------------------- scenes
def scene_parade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 68, 92))
    # storm clouds
    for cx, cy, r in [(x + 40, y + 22, 26), (x + 110, y + 14, 32),
                      (x + 190, y + 24, 28), (x + 260, y + 16, 30),
                      (x + 330, y + 24, 26), (x + 410, y + 18, 28)]:
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(38, 50, 70))
    # rain
    for i in range(46):
        rx = x + 12 + (i * 37) % (w - 24)
        ry = y + 40 + (i * 53) % (h - 60)
        d.line([rx, ry, rx - 4, ry + 12], fill=(150, 170, 200), width=2)
    # street + buildings
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(70, 70, 74))
    for bx in (x + 8, x + w - 52):
        d.rectangle([bx, y + h - 78, bx + 44, y + h - 26], fill=(30, 34, 44))
        for wy in range(y + h - 72, y + h - 30, 12):
            d.rectangle([bx + 6, wy, bx + 16, wy + 7], fill=(240, 200, 90))
            d.rectangle([bx + 26, wy, bx + 36, wy + 7], fill=(240, 200, 90))
    # grounded balloon: deflated red ellipse on the street
    d.ellipse([x + w // 2 - 78, y + h - 66, x + w // 2 + 78, y + h - 30],
              fill=(178, 30, 30), outline=(120, 16, 16), width=2)
    d.ellipse([x + w // 2 - 40, y + h - 60, x + w // 2 + 40, y + h - 38],
              fill=(205, 55, 55))
    d.text((x + w // 2 - 52, y + h - 56), "GROUNDED", font=font(SANS_B, 13),
           fill=(255, 255, 255))
    # banner
    d.rectangle([x + 14, y + 8, x + 150, y + 30], fill=(178, 30, 30))
    d.text((x + 22, y + 12), "SAT 28 NOV", font=font(SANS_B, 13),
           fill=(255, 255, 255))


def scene_airfield(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 16, 30))
    for i in range(28):
        sx = x + (i * 97) % w
        sy = y + (i * 41) % 42
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 220, 220))
    # runway (no moon: it collided with the scene label)
    d.polygon([(x, y + h), (x + w, y + h), (x + w - 30, y + h - 34),
               (x + 30, y + h - 34)], fill=(48, 48, 54))
    for i in range(6):
        d.line([x + 40 + i * 62, y + h - 17, x + 58 + i * 62, y + h - 17],
               fill=(240, 210, 90), width=3)
    # two jet silhouettes (light grey so they read against the night sky)
    for jx in (x + 60, x + w - 190):
        d.polygon([(jx, y + h - 52), (jx + 96, y + h - 52), (jx + 118, y + h - 44),
                   (jx + 96, y + h - 38), (jx, y + h - 38)], fill=(64, 68, 86),
                  outline=(150, 150, 160))
        d.polygon([(jx + 44, y + h - 66), (jx + 58, y + h - 66),
                   (jx + 66, y + h - 52)], fill=(64, 68, 86),
                  outline=(150, 150, 160))
    # fire bursts
    for fx, fy, r in [(x + w // 2 - 20, y + h - 60, 16),
                      (x + w // 2 + 46, y + h - 48, 11)]:
        d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=(230, 110, 20))
        d.ellipse([fx - r // 2, fy - r // 2, fx + r // 2, fy + r // 2],
                  fill=(250, 200, 60))
    # (scene carries no text label: the kicker names the air base)


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=(200, 196, 184))
    for gy in range(1, 4):
        d.line([x + 8, y + gy * h // 4, x + w - 8, y + gy * h // 4],
               fill=(226, 222, 210))
    # falling candlesticks
    tops = [0.22, 0.30, 0.38, 0.50, 0.58, 0.68]
    cw = (w - 40) // len(tops)
    for i, t in enumerate(tops):
        cx = x + 22 + i * cw
        d.line([cx + cw // 2, y + h * (t - 0.08), cx + cw // 2,
                y + h * (t + 0.22)], fill=(178, 30, 30), width=2)
        d.rectangle([cx + 4, y + h * t, cx + cw - 4, y + h * (t + 0.14)],
                    fill=(178, 30, 30))
    # trend arrow
    d.line([x + 16, y + h * 0.18, x + w - 16, y + h * 0.82],
           fill=(178, 30, 30), width=4)
    d.polygon([(x + w - 16, y + h * 0.82), (x + w - 34, y + h * 0.74),
               (x + w - 30, y + h * 0.90)], fill=(178, 30, 30))
    d.rectangle([x + 10, y + 8, x + 118, y + 28], fill=(18, 18, 18))
    d.text((x + 17, y + 12), "14 NATIONS", font=font(SANS_B, 12),
           fill=(255, 255, 255))


def mini(d, kind, x, y, s=58):
    """Small 58x58 scene inside a small-story panel."""
    d.rectangle([x, y, x + s, y + s], fill=LIGHT, outline=(200, 196, 184))
    if kind == "stars":
        d.ellipse([x + 6, y + 6, x + s - 6, y + s - 6], fill=BLUE)
        for i in range(8):
            import math
            a = i * math.pi / 4
            px = x + s // 2 + int(17 * math.cos(a))
            py = y + s // 2 + int(17 * math.sin(a))
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(250, 210, 60))
        d.text((x + s // 2 - 4, y + s // 2 - 6), "EU", font=font(SANS_B, 11),
               fill=(255, 255, 255))
    elif kind == "candles":
        d.rectangle([x, y, x + s, y + s], fill=(30, 30, 34))
        for cx in (x + 14, x + 29, x + 44):
            d.rectangle([cx - 3, y + 24, cx + 3, y + 50], fill=(240, 235, 220))
            d.ellipse([cx - 3, y + 16, cx + 3, y + 24], fill=(250, 190, 60))
        d.text((x + 8, y + 6), "26/11", font=font(SANS_B, 10), fill=(255, 255, 255))
    elif kind == "bars":
        d.rectangle([x, y, x + s, y + s], fill=(255, 255, 255))
        for i, bh in enumerate((18, 30, 24, 40)):
            bx = x + 8 + i * 12
            d.rectangle([bx, y + s - 8 - bh, bx + 8, y + s - 8], fill=BLUE)
        d.text((x + 6, y + 4), "PCE GDP", font=font(SANS_B, 9), fill=INK)
    elif kind == "plane":
        d.rectangle([x, y, x + s, y + s], fill=(140, 190, 220))
        d.rectangle([x, y + 40, x + s, y + s], fill=(30, 90, 150))
        d.polygon([(x + 10, y + 20), (x + 46, y + 20), (x + 52, y + 26),
                   (x + 46, y + 30), (x + 10, y + 30)], fill=(255, 255, 255))
        d.polygon([(x + 26, y + 12), (x + 32, y + 12), (x + 36, y + 20)],
                  fill=(255, 255, 255))
        d.text((x + 6, y + 44), "6 DEAD", font=font(SANS_B, 10),
               fill=(255, 255, 255))
    elif kind == "exam":
        d.rectangle([x, y, x + s, y + s], fill=(255, 255, 255))
        d.rectangle([x + 12, y + 8, x + s - 12, y + s - 8], fill=(255, 255, 255),
                    outline=INK)
        for ly in (16, 24, 32, 40):
            d.line([x + 17, y + ly, x + s - 17, y + ly], fill=GREY)
        d.line([x + 16, y + 14, x + s - 14, y + s - 12], fill=RED, width=4)
        d.line([x + s - 14, y + 14, x + 16, y + s - 12], fill=RED, width=4)
    elif kind == "flags":
        d.rectangle([x, y, x + s // 2 - 1, y + s], fill=(200, 30, 40))
        d.ellipse([x + s // 4 - 7, y + s // 2 - 7, x + s // 4 + 7,
                   y + s // 2 + 7], fill=(255, 255, 255))
        d.rectangle([x + s // 2 + 1, y, x + s, y + s], fill=(255, 255, 255))
        d.rectangle([x + s // 2 + 1, y, x + s, y + s // 2], fill=(210, 30, 30))
        d.rectangle([x + s // 2 + 14, y + s // 2 + 6, x + s // 2 + 22,
                     y + s // 2 + 14], fill=(210, 30, 30))
    elif kind == "spain":
        d.rectangle([x, y, x + s, y + s], fill=(170, 30, 30))
        d.rectangle([x, y + 15, x + s, y + s - 15], fill=(250, 200, 40))
        d.polygon([(x + 12, y + 16), (x + 44, y + 16), (x + 50, y + 22),
                   (x + 44, y + 26), (x + 12, y + 26)], fill=(255, 255, 255))
    elif kind == "siege":
        d.rectangle([x, y, x + s, y + s], fill=(90, 110, 150))
        d.rectangle([x + 8, y + 22, x + s - 8, y + s - 10], fill=(200, 200, 200))
        d.rectangle([x + 8, y + 22, x + s - 8, y + 30], fill=(120, 30, 30))
        d.polygon([(x + 6, y + 40), (x + s - 6, y + 34), (x + s - 6, y + 42),
                   (x + 6, y + 48)], fill=(250, 210, 60))
        d.text((x + 8, y + 42), "POLICE", font=font(SANS_B, 9), fill=INK)
    elif kind == "mosquito":
        d.rectangle([x, y, x + s, y + s], fill=(255, 255, 255))
        d.ellipse([x + 14, y + 22, x + 34, y + 38], fill=(60, 60, 60))
        d.line([x + 34, y + 26, x + 52, y + 14], fill=INK, width=2)
        d.line([x + 34, y + 32, x + 52, y + 44], fill=INK, width=2)
        d.line([x + 14, y + 30, x + 4, y + 22], fill=INK, width=2)
        d.text((x + 4, y + 42), "-68%", font=font(SANS_B, 13), fill=RED)
    elif kind == "rocket":
        d.rectangle([x, y, x + s, y + s], fill=(16, 32, 64))
        for i in range(12):
            d.ellipse([x + (i * 53) % s, y + (i * 29) % 20,
                       x + (i * 53) % s + 2, y + (i * 29) % 20 + 2],
                      fill=(255, 255, 255))
        d.polygon([(x + 28, y + 8), (x + 36, y + 22), (x + 28, y + 44),
                   (x + 20, y + 22)], fill=(240, 240, 240))
        d.ellipse([x + 25, y + 20, x + 31, y + 26], fill=BLUE)
        d.polygon([(x + 24, y + 44), (x + 20, y + 52), (x + 28, y + 48)],
                  fill=(230, 110, 20))
        d.polygon([(x + 32, y + 44), (x + 36, y + 52), (x + 28, y + 48)],
                  fill=(230, 110, 20))


# ---------------------------------------------------------------- page
def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=(120, 116, 104), width=2)

    # ---- masthead
    d.rectangle([20, 10, W - 20, 66], fill=INK)
    d.text((512, 16), "THE WORLD IN ONE DAY",
           font=font(SERIF, 40), fill=(255, 255, 255), anchor="ma")
    d.text((28, 44), "EST. 2026", font=font(SANS_B, 10), fill=(200, 196, 184))
    d.text((W - 28, 44), "ONE PAGE  •  ONE DAY", font=font(SANS_B, 10),
           fill=(200, 196, 184), anchor="ra")

    # ---- date line
    d.text((20, 72), "THURSDAY 26 NOVEMBER 2026", font=font(SERIF, 26), fill=INK)
    d.text((W - 20, 80), "38 STORIES  •  13 SCENES  •  12 MAP PINS",
           font=font(SANS_B, 13), fill=RED, anchor="ra")
    d.line([20, 104, W - 20, 104], fill=INK, width=2)

    # ---- red standfirst
    d.rectangle([20, 110, W - 20, 134], fill=RED)
    d.text((512, 115),
           "PARADE POSTPONED  •  FIVE JETS HIT  •  TARIFFS LAND ON 14 NATIONS",
           font=font(SANS_B, 14), fill=(255, 255, 255), anchor="ma")

    # ---- stat strip
    sx, sy, sw, sh = 20, 142, 158, 52
    for i, (num, cap) in enumerate(STATS):
        x = sx + i * (sw + 6)
        d.rectangle([x, sy, x + sw, sy + sh], outline=(180, 176, 164), fill=(255, 255, 255))
        d.text((x + sw // 2, sy + 4), num, font=font(SERIF, 20), fill=RED, anchor="ma")
        for j, line in enumerate(cap.split("\n")):
            d.text((x + sw // 2, sy + 28 + j * 11), line, font=font(SANS, 9),
                   fill=GREY, anchor="ma")

    # ---- big stories: left = #1, right stacked = #2, #3
    by = 204
    # #1 left panel
    bx, bw = 20, 478
    d.rectangle([bx, by, bx + bw, by + 196], outline=(180, 176, 164), fill=(255, 255, 255))
    scene_parade(d, bx + 6, by + 6, bw - 12, 88)
    y = by + 100
    y = kicker(d, bx + 10, y, BIG[0]["kick"])
    d.text((bx + 10, y), BIG[0]["head"], font=font(SERIF, 24), fill=INK)
    y += 30
    d.text((bx + 10, y), BIG[0]["sub"], font=font(SANS_B, 10), fill=RED)
    y += 15
    para(d, bx + 10, y, BIG[0]["body"], font(SANS, 10), bw - 20, 12)
    badge(d, bx + bw - 92, by + 6, BIG[0]["label"])
    # #2 / #3 right stacked panels
    rx, rw = 510, 494
    for k, story in enumerate(BIG[1:]):
        py = by + k * 100
        d.rectangle([rx, py, rx + rw, py + 96], outline=(180, 176, 164), fill=(255, 255, 255))
        sw2 = 176
        if story["scene"] == "airfield":
            scene_airfield(d, rx + 6, py + 6, sw2, 84)
        else:
            scene_chart(d, rx + 6, py + 6, sw2, 84)
        tx = rx + sw2 + 14
        y = py + 6
        y = kicker(d, tx, y, story["kick"])
        d.text((tx, y), story["head"], font=font(SERIF, 17), fill=INK)
        y += 23
        para(d, tx, y, story["body"], font(SANS, 10), rw - sw2 - 24, 12)
        # badge sits on the scene's bottom-right corner, clear of the text
        badge(d, rx + 6 + sw2 - 92, py + 6 + 84 - 23, story["label"])

    # ---- region bar
    ry = 410
    counts = {}
    for s in BIG + SMALL:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for b in BRIEFS:
        pass
    # briefs counted from the story data above: AM 16, EU 9, AS 5, AF 3, ME 2, GL 3
    counts = {"AM": 16, "EU": 9, "AS": 5, "AF": 3, "ME": 2, "GL": 3}
    d.text((20, ry), "REGIONS", font=font(SANS_B, 11), fill=INK)
    x = 84
    for name, code in REGIONS:
        w = 60 + counts[code] * 9
        d.rectangle([x, ry, x + w, ry + 16], fill=RED if code == "AM" else BLUE
                    if code == "EU" else (60, 120, 70) if code == "AS" else
                    (150, 110, 20) if code == "AF" else (120, 70, 120) if code == "ME"
                    else GREY)
        d.text((x + 5, ry + 2), f"{name} {counts[code]}", font=font(SANS_B, 10),
               fill=(255, 255, 255))
        x += w + 5

    # ---- ten small stories: 2 rows x 5
    sy2 = 434
    pw, ph, gap = 192, 74, 6
    for i, s in enumerate(SMALL):
        row, col = divmod(i, 5)
        px = 20 + col * (pw + gap)
        py = sy2 + row * (ph + 6)
        d.rectangle([px, py, px + pw, py + ph], outline=(180, 176, 164),
                    fill=(255, 255, 255))
        mini(d, s["scene"], px + 5, py + 8, 58)
        tx = px + 68
        d.text((tx, py + 5), s["kick"], font=font(SANS_B, 9), fill=RED)
        y = py + 17
        for line in wrap(d, s["head"], font(SERIF, 12), pw - 74):
            d.text((tx, y), line, font=font(SERIF, 12), fill=INK)
            y += 14
        y = para(d, tx, y + 1, s["body"], font(SANS, 9), pw - 74, 11, fill=GREY)
        d.text((px + pw - 16, py + 4), str(s["n"]), font=font(SANS_B, 10),
               fill=(180, 176, 164))

    # ---- 25 briefs in 3 columns
    by2 = 598
    d.text((20, by2), "THE DAY IN BRIEF  —  25 MORE STORIES",
           font=font(SANS_B, 12), fill=INK)
    d.line([20, by2 + 18, W - 20, by2 + 18], fill=RED, width=2)
    cols = [BRIEFS[i::3] for i in range(3)]
    for ci, col in enumerate(cols):
        cx = 20 + ci * 330
        y = by2 + 28
        for j, (place, text) in enumerate(col):
            num = 14 + ci + j * 3
            d.text((cx, y), f"{num}.", font=font(SANS_B, 9), fill=RED)
            d.text((cx + 22, y), place + " — ", font=font(SANS_B, 9), fill=INK)
            tw = 330 - 22 - d.textlength(place + " — ", font=font(SANS_B, 9))
            lines = wrap(d, text, font(SANS, 9), tw)
            yy = y
            for li, line in enumerate(lines):
                if li == 0:
                    d.text((cx + 22 + d.textlength(place + " — ", font=font(SANS_B, 9)), yy),
                           line, font=font(SANS, 9), fill=INK)
                else:
                    d.text((cx + 22, yy), line, font=font(SANS, 9), fill=INK)
                yy += 11
            y = yy + 2
        # column rule
        if ci < 2:
            d.line([cx + 322, by2 + 26, cx + 322, by2 + 26 + 218], fill=(210, 206, 194))

    # ---- world map strip
    my = 852
    d.text((20, my), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=INK)
    d.rectangle([20, my + 18, W - 20, my + 96], fill=(214, 230, 240),
                outline=(180, 176, 164))
    mx, mw, mh = 20, W - 40, 78
    # simplified continents
    d.polygon([(mx + 30, my + 30), (mx + 120, my + 24), (mx + 150, my + 44),
               (mx + 130, my + 66), (mx + 60, my + 70), (mx + 34, my + 52)],
              fill=(120, 160, 110))  # N America
    d.polygon([(mx + 150, my + 62), (mx + 190, my + 58), (mx + 200, my + 80),
               (mx + 168, my + 88)], fill=(120, 160, 110))  # S America
    d.polygon([(mx + 430, my + 24), (mx + 500, my + 20), (mx + 520, my + 42),
               (mx + 480, my + 52), (mx + 440, my + 44)], fill=(120, 160, 110))  # Europe
    d.polygon([(mx + 520, my + 26), (mx + 640, my + 20), (mx + 700, my + 40),
               (mx + 660, my + 66), (mx + 560, my + 62)], fill=(120, 160, 110))  # Asia
    d.polygon([(mx + 440, my + 52), (mx + 500, my + 50), (mx + 510, my + 82),
               (mx + 470, my + 92), (mx + 448, my + 72)], fill=(120, 160, 110))  # Africa
    d.polygon([(mx + 830, my + 70), (mx + 890, my + 66), (mx + 900, my + 84),
               (mx + 850, my + 90)], fill=(120, 160, 110))  # Australia
    for n, name, px, py in PINS:
        d.ellipse([mx + px - 8, my + 18 + py - 8, mx + px + 8, my + 18 + py + 8],
                  fill=RED, outline=(255, 255, 255), width=1)
        d.text((mx + px, my + 18 + py - 5), str(n), font=font(SANS_B, 9),
               fill=(255, 255, 255), anchor="mm")
    d.text((20, my + 100), "1 New York  2 Savasleyka  3 Washington  4 Brussels  "
           "5 Mumbai  6 Mississippi  7 Seoul  8 Pyongyang  9 Madrid  "
           "10 Cartagena  11 New Delhi  12 London",
           font=font(SANS, 10), fill=GREY)

    # ---- date check box
    dy = 970
    d.rectangle([20, dy, W - 20, dy + 36], outline=RED, width=2, fill=(255, 244, 238))
    d.text((28, dy + 3), "DATE CHECK — WHY THIS IS 26 NOVEMBER:",
           font=font(SANS_B, 10), fill=RED)
    d.text((28, dy + 16),
           "Parade postponement, tariffs and the Savasleyka claim were all reported on 26 Nov "
           "(US filings of Wed 25 Nov reached Asia on Thu 26 Nov).",
           font=font(SANS, 9), fill=INK)
    d.text((28, dy + 26),
           "Left out as earlier news: BepiColombo Mercury arrival (21 Nov), Huawei verdict "
           "(24 Nov), Petrobras plan (23 Nov).",
           font=font(SANS, 9), fill=INK)
    d.text((512, 1012), "THE WORLD IN ONE DAY  •  THURSDAY 26 NOVEMBER 2026  •  "
           "38 STORIES, ALL DATED  •  CLAIMS LABELLED CLAIM / REPORTED",
           font=font(SANS_B, 9), fill=GREY, anchor="ma")
    return img


def main():
    img = draw_page()
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
