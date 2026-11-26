#!/usr/bin/env python3
"""Writes docs/img/av-quality.svg (Docs poster: Audio and Video Quality; source: Learn cards av-quality.html,
deep-avq.html, deep-zapping.html and their chapter texts in index.html). Run from the repo root.

Every number is one the Learn cards show (picture 4.1 from blur 5.6 and blocks 18, sound 4.7 from -20 LUFS and
3 s of silence, zap 1.6 s with 1.1 s black, key 0.5 s before the black). Pictures are drawn, no real screen.
Fails when a text is wider than its room in DejaVu Sans (headless Chromium's fallback font)."""
import math
from PIL import ImageFont

W = 1200
BG, PANEL, CHIP, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#2a2a2a", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
OK, WARN, BAD = "#4ade80", "#f59e0b", "#ef4444"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
TTF = {True: "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", False: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"}
o = []


def fit(s, size, bold, room):
    try:
        font = ImageFont.truetype(TTF[bold], size)
    except OSError:
        return
    plain = s.replace("&amp;", "&")
    if font.getlength(plain) > room:
        raise SystemExit(f"too wide ({font.getlength(plain):.0f} > {room}): {plain}")


def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0, room=1060):
    fit(s, size, w >= 600, room)
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{s}</text>')


def box(x, y, w, h, fill=PANEL, stroke=LINE, r=22, sw=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def arrow(x, y1, y2):
    o.append(f'<path d="M{x} {y1}V{y2-12}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x-12} {y2-18}L{x} {y2-4}L{x+12} {y2-18}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')


def layer(y, n, title, sub, h):
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, title, 34, TXT, 700, room=960)
    if sub:
        t(156, y + 82, sub, 21, MUT, 400, room=960)


def scene(x, y, w, h, kind="a", blocks=False):
    """A drawn TV picture: sky, sun, hills. kind 'b' is the other channel (night, moon). blocks adds square blocks."""
    cid = f"c{len(o)}"
    o.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{max(3, w/40):.0f}"/></clipPath><g clip-path="url(#{cid})">')
    if kind == "black":
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#050505"/></g>')
        return
    sky, hill1, hill2, orb = ("#6fa8d6", "#3f7d4a", "#2f6138", "#f4d35e") if kind == "a" else ("#2b2d5c", "#4b3f72", "#362c57", "#e8e8f0")
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{sky}"/>')
    o.append(f'<circle cx="{x+w*0.74:.1f}" cy="{y+h*0.3:.1f}" r="{h*0.13:.1f}" fill="{orb}"/>')
    o.append(f'<path d="M{x} {y+h*0.7:.1f}Q{x+w*0.3:.1f} {y+h*0.4:.1f} {x+w*0.6:.1f} {y+h*0.68:.1f}T{x+w} {y+h*0.62:.1f}V{y+h}H{x}Z" fill="{hill1}"/>')
    o.append(f'<path d="M{x} {y+h*0.85:.1f}Q{x+w*0.45:.1f} {y+h*0.66:.1f} {x+w} {y+h*0.86:.1f}V{y+h}H{x}Z" fill="{hill2}"/>')
    if blocks:
        s = w / 16
        for i, j in [(2, 6), (3, 6), (3, 7), (4, 7), (8, 5), (9, 5), (9, 6), (12, 7), (13, 7), (13, 8), (6, 8), (7, 8)]:
            shade = ["#5c8f62", "#4a7a52", "#7fae7a", "#386944"][(i + j) % 4]
            o.append(f'<rect x="{x+i*s:.1f}" y="{y+j*s:.1f}" width="{s:.1f}" height="{s:.1f}" fill="{shade}" stroke="#2a4a30" stroke-width="1"/>')
    o.append("</g>")


def tv(x, y, w, h, kind="a", blocks=False):
    box(x - 10, y - 10, w + 20, h + 20, "#0d0d0d", "#4a4a4a", 14, 2)
    scene(x, y, w, h, kind, blocks)


def wave(x, y, w, h, gap=None, step=6, seed=1.0):
    """A drawn sound wave: vertical bars; gap = (x0, x1) fraction with no sound."""
    n = int(w / step)
    for i in range(n):
        f = i / n
        if gap and gap[0] <= f <= gap[1]:
            a = 1.5
        else:
            a = h / 2 * (0.35 + 0.55 * abs(math.sin(i * 0.37 * seed) * math.cos(i * 0.11 + seed)))
        cx = x + i * step
        o.append(f'<path d="M{cx:.1f} {y+h/2-a:.1f}V{y+h/2+a:.1f}" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>')


def gauge(x, y, w, label, value, lo_txt, hi_txt, frac, mark=None, mark_txt=""):
    """A horizontal scale with a dot at frac (0..1); mark = a target tick."""
    t(x, y, label, 20, TXT, 700, room=w * 0.6)
    t(x + w, y, value, 20, GOLD, 700, "end", room=w * 0.5)
    by = y + 18
    o.append(f'<rect x="{x}" y="{by}" width="{w}" height="12" rx="6" fill="#333"/>')
    o.append(f'<rect x="{x}" y="{by}" width="{w*frac:.1f}" height="12" rx="6" fill="{GOLD}" opacity="0.55"/>')
    o.append(f'<circle cx="{x+w*frac:.1f}" cy="{by+6}" r="10" fill="{GOLD}" stroke="#161616" stroke-width="3"/>')
    if mark is not None:
        mx = x + w * mark
        o.append(f'<path d="M{mx:.1f} {by-6}V{by+18}" stroke="{TXT}" stroke-width="3"/>')
    t(x, by + 38, lo_txt, 16, MUT, 400, room=w * 0.45)
    t(x + w, by + 38, hi_txt, 16, MUT, 400, "end", room=w * 0.45)
    if mark_txt:
        t(x + w * mark, by + 38, mark_txt, 16, TXT, 600, "middle", room=120)


def score(x, y, w, name, val, color=OK):
    box(x, y, w, 70, "#2a2418", GOLD, 16, 2)
    t(x + 24, y + 45, name, 24, TXT, 700, room=w / 2)
    fit(f"{val} / 5", 34, True, w / 2)
    o.append(f'<text x="{x+w-24}" y="{y+47}" font-family="{F}" font-size="34" font-weight="700" fill="{color}" text-anchor="end">{val}<tspan font-size="20" fill="{MUT}"> / 5</tspan></text>')


H = "@@H@@"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Audio and Video Quality: a picture and sound score every minute, and how a zap is timed, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# header (Learn card av-quality: eyebrow, title, sub)
t(60, 90, "MONITOR 24/7 · A/V QUALITY", 20, GOLD, 500, sp=3)
t(60, 166, "Audio and Video Quality", 62, TXT, 700)
t(60, 220, "A picture and sound score, every minute, 24 h", 29, MUT, 400)

# 1 One minute at a time (deep-avq step 1 and 3)
y = 270
P1 = 310
layer(y, "1", "One minute at a time", "Every device, every minute: what it really shows and plays", P1)
tv(110, y + 112, 240, 135, "a")
t(230, y + 292, "Live TV", 20, MUT, 600, "middle", room=280)
# 60 pictures: a strip of small frames, one a second
sx, sy = 420, y + 112
t(sx, sy + 4, "60 pictures", 22, TXT, 700, room=300)
t(sx + 670, sy + 4, "one a second", 18, MUT, 400, "end", room=300)
for i in range(11):
    scene(sx + i * 62, sy + 20, 56, 32, "a")
t(sx, sy + 92, "60 s of sound", 22, TXT, 700, room=300)
wave(sx, sy + 106, 670, 48, seed=1.3)
t(sx, y + 292, "Black or frozen frames do not count.", 20, MUT, 400, room=640)
arrow(600, y + P1, y + P1 + 40)

# 2 The picture score + the sound score (deep-avq steps 2, 4, 5; numbers as on the card)
y += P1 + 40
P2 = 440
layer(y, "2", "Two scores, from 5 down", "Sharp is 5, the worst is 2. A silent minute scores 0.", P2)
# picture half
px = 100
tv(px + 10, y + 116, 210, 118, "a", blocks=True)
t(px + 115, y + 266, "Blur and blocks", 18, MUT, 600, "middle", room=220)
gauge(px + 260, y + 120, 230, "Blur", "5.6", "4 sharp", "9 worst", (5.6 - 4) / 5)
gauge(px + 260, y + 204, 230, "Blocks", "18", "10", "40", (18 - 10) / 30)
score(px, y + 320, 490, "Picture", "4.1")
# sound half
qx = 620
wave(qx + 10, y + 118, 470, 64, gap=(0.58, 0.66), step=6, seed=0.7)
t(qx + 10 + 470 * 0.62, y + 110, "Silence 3 s", 16, TXT, 600, "middle", room=120)
gauge(qx + 10, y + 212, 470, "Loudness", "−20 LUFS", "−40", "−10", (40 - 20) / 30, mark=(40 - 23) / 30, mark_txt="target −23")
t(qx + 10, y + 298, "No clipping", 18, MUT, 600, room=300)
score(qx, y + 320, 490, "Sound", "4.7")
t(600, y + P2 - 24, "Close to −23, little silence, no clipping: a good sound.", 19, MUT, 400, "middle")
arrow(600, y + P2, y + P2 + 40)

# 3 A row every minute (av-quality card + deep-avq step 6)
y += P2 + 40
P3 = 380
layer(y, "3", "The last 24 hours", "Both scores are kept for every device, one row a minute, for 7 days", P3)
gx, gy, gw = 110, y + 146, 980
NB = 48
bw = gw / NB
heights = []
for i in range(NB):
    v = 0.86 + 0.08 * math.sin(i * 0.9) * math.cos(i * 0.31)
    if i == 31:
        v = 0.28
    elif i in (30, 32):
        v = 0.55
    heights.append(v)
for i, v in enumerate(heights):
    c = OK if v >= 0.7 else (WARN if v >= 0.45 else BAD)
    h = 100 * v
    o.append(f'<rect x="{gx+i*bw+2:.1f}" y="{gy+100-h:.1f}" width="{bw-4:.1f}" height="{h:.1f}" rx="3" fill="{c}"/>')
o.append(f'<path d="M{gx} {gy+104}H{gx+gw}" stroke="{LINE}" stroke-width="2"/>')
for lx, lab, an in [(gx, "00:00", "start"), (gx + gw / 2, "12:00", "middle"), (gx + gw, "Now", "end")]:
    t(lx, gy + 128, lab, 18, MUT, 500, an, room=100)
# the drop and its button
dx = gx + 31 * bw + bw / 2
o.append(f'<path d="M{dx:.1f} {gy+70}V{gy-10}" stroke="{BAD}" stroke-width="2" stroke-dasharray="5 4"/>')
box(dx - 92, gy - 46, 184, 36, "#3a1d1d", BAD, 18, 2)
t(dx, gy - 21, "Quality drop", 18, TXT, 700, "middle", room=170)
box(1090 - 220, gy + 144, 220, 42, GOLD, GOLD, 21, 0)
t(1090 - 110, gy + 172, "▶ Play that minute", 19, "#1a1a1a", 700, "middle", room=200)
# legend
for i, (c, lab) in enumerate([(OK, "green from 4"), (WARN, "amber from 2.5"), (BAD, "red below")]):
    lx = 110 + i * 190
    o.append(f'<circle cx="{lx+8}" cy="{gy+166}" r="8" fill="{c}"/>')
    t(lx + 24, gy + 172, lab, 18, MUT, 500, room=160)
t(600, y + P3 - 22, "Quick, approximate scores, not a certified measure.", 19, MUT, 400, "middle")
arrow(600, y + P3, y + P3 + 40)

# 4 How a zap is measured (deep-zapping: CH + 0.5 s before the black, black 1.1 s, zap 1.6 s)
y += P3 + 40
P4 = 490
layer(y, "4", "How a zap is measured", "Key press to new picture, with the black time inside it", P4)
ax, aw = 120, 960
sec = aw / 3.0  # 0 s .. 3 s
fy = y + 136
fw, fh = 100, 56
frames = [(-0.5, "a"), (0.0, "a"), (0.5, "black"), (1.05, "black"), (1.6, "b"), (2.2, "b")]
x0 = ax + 0.6 * sec  # time 0 (the key press)
for tm, kind in frames:
    cx = x0 + tm * sec
    box(cx - fw / 2 - 4, fy - 4, fw + 8, fh + 8, "#0d0d0d", "#4a4a4a", 8, 1.5)
    scene(cx - fw / 2, fy, fw, fh, kind)
t(x0 - 0.5 * sec, fy - 16, "Channel 1", 18, MUT, 600, "middle", room=140)
t(x0 + 1.9 * sec, fy - 16, "Channel 2", 18, MUT, 600, "middle", room=140)
# time axis
ay = fy + 116
o.append(f'<path d="M{ax} {ay}H{ax+aw}" stroke="{LINE}" stroke-width="3"/>')
for k in range(4):
    tx = x0 + k * sec
    if tx <= ax + aw:
        o.append(f'<path d="M{tx:.1f} {ay-6}V{ay+6}" stroke="{MUT}" stroke-width="2"/>')
        t(tx + 6, ay + 26, f"{k} s", 16, MUT, 500, "middle", room=60)
# the key press
box(x0 - 36, fy + 66, 72, 34, "#1a1a1a", GOLD, 8, 2)
t(x0, fy + 90, "CH +", 18, GOLD, 700, "middle", room=64)
o.append(f'<path d="M{x0:.1f} {fy+100}V{ay}" stroke="{GOLD}" stroke-width="2" stroke-dasharray="4 4"/>')
# black bracket (0.5 s .. 1.6 s) and zap bracket (0 .. 1.6 s)
b0, b1, z1 = x0 + 0.5 * sec, x0 + 1.6 * sec, x0 + 1.6 * sec
o.append(f'<path d="M{b1:.1f} {fy+100}V{ay+118}" stroke="{GOLD}" stroke-width="2" stroke-dasharray="4 4"/>')
by = ay + 66
o.append(f'<path d="M{b0:.1f} {by+12}V{by}H{b1:.1f}V{by+12}" fill="none" stroke="{MUT}" stroke-width="3"/>')
t((b0 + b1) / 2, by - 10, "Black 1.1 s", 20, TXT, 700, "middle", room=200)
zy = ay + 122
o.append(f'<path d="M{x0:.1f} {zy+12}V{zy}H{z1:.1f}V{zy+12}" fill="none" stroke="{GOLD}" stroke-width="4"/>')
t((x0 + z1) / 2, zy - 10, "Zap 1.6 s", 24, GOLD, 700, "middle", room=240)
# what makes it a zap: three checks, the card's own words
cy = y + 396
for i, (a, b) in enumerate([("Black or frozen", "under 10 s"), ("Channel key", "under 10 s before"), ("A gap in the sound", "not a dark scene")]):
    cx = 90 + i * (327 + 20)
    box(cx, cy, 327, 70, CHIP, LINE, 16)
    t(cx + 163, cy + 30, a, 22, TXT, 600, "middle", room=310)
    t(cx + 163, cy + 55, b, 16, MUT, 400, "middle", room=310)

# footer
y += P4
t(600, y + 56, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
Htot = y + 94
o.append("</svg>")
open("docs/img/av-quality.svg", "w").write("\n".join(o).replace(H, str(Htot)))
print("docs/img/av-quality.svg", Htot)
