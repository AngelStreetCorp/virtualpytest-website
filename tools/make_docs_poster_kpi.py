#!/usr/bin/env python3
"""Writes docs/img/kpi.svg (Docs poster: how a KPI is measured, shown versus loaded; source: Learn topic 5 cards
response-time, deep-kpi, loaded, deep-loading, and docs/agent/execution/KPI.md "Loading time: shown vs loaded").
Run from the repo root. Every number is from one real measurement (docs/img/kpi-real-header.png, its KPI header):
press 0, first change 960 ms, match (the KPI) 1160 ms ±200 ms, fully loaded 1356 ms, capture 5.02 fps. The drawn
frames are generic; no frame of the real measurement is used (it shows an operator app).

Fails when a text is wider than its room in DejaVu Sans (headless Chromium's fallback font)."""
import base64

from PIL import Image, ImageFont

REAL = "docs/img/kpi-real-header.png"  # the KPI header of a real measurement (owner screenshot, cleaned for public use)
REAL_W, REAL_H = Image.open(REAL).size
REAL_B64 = base64.b64encode(open(REAL, "rb").read()).decode()

W = 1200
BG, PANEL, CHIP, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#2a2a2a", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
TTF = {True: "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", False: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"}
TILES = ["#8fb0c0", "#e0a96d", "#a8b89a", "#d39a9a"]  # filled tiles, as in the Learn card
GREYBOX = "#5a5a5a"
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


def harrow(x1, x2, y):
    o.append(f'<path d="M{x1} {y}H{x2-10}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x2-22} {y-12}L{x2-6} {y}L{x2-22} {y+12}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')


def layer(y, n, title, sub, h):
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, title, 34, TXT, 700, room=960)
    if sub:
        t(156, y + 82, sub, 21, MUT, 400, room=960)


def screen(x, y, w, h, state, title=True, filled=8):
    """A drawn TV screen. state: home (the screen before the press), blank (new page, nothing drawn yet),
    page (title + 8 tiles; `filled` of them drawn, the rest grey boxes)."""
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{max(3, w/40):.1f}" fill="#0d0d0d" stroke="#4a4a4a" stroke-width="{2 if w > 80 else 1}"/>')
    pad = w * 0.07
    if state == "blank":
        return
    if state == "home":
        # the old screen: a wide banner and one row of tiles
        o.append(f'<rect x="{x+pad:.1f}" y="{y+h*0.12:.1f}" width="{w*0.3:.1f}" height="{h*0.08:.1f}" rx="2" fill="#6a6a6a"/>')
        o.append(f'<rect x="{x+pad:.1f}" y="{y+h*0.28:.1f}" width="{w-2*pad:.1f}" height="{h*0.34:.1f}" rx="{w/60:.1f}" fill="#4c5f6b"/>')
        tw = (w - 2 * pad - 2 * (w * 0.03)) / 3
        for i in range(3):
            o.append(f'<rect x="{x+pad+i*(tw+w*0.03):.1f}" y="{y+h*0.70:.1f}" width="{tw:.1f}" height="{h*0.18:.1f}" rx="{w/80:.1f}" fill="{TILES[(i+1)%4]}" opacity="0.75"/>')
        return
    # page: a title bar, then 2 rows of 4 tiles
    if title:
        o.append(f'<rect x="{x+pad:.1f}" y="{y+h*0.12:.1f}" width="{w*0.36:.1f}" height="{h*0.09:.1f}" rx="2" fill="#bdbdbd"/>')
    gap = w * 0.035
    tw = (w - 2 * pad - 3 * gap) / 4
    th = h * 0.27
    for r in range(2):
        for c in range(4):
            k = r * 4 + c
            fill = TILES[(k + r) % 4] if k < filled else GREYBOX
            o.append(f'<rect x="{x+pad+c*(tw+gap):.1f}" y="{y+h*0.32+r*(th+h*0.06):.1f}" width="{tw:.1f}" height="{th:.1f}" rx="{w/80:.1f}" fill="{fill}"/>')


H = "@@H@@"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">How a KPI is measured: from the key press to the first frame where the screen is loaded, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# header
t(60, 90, "MEASURE", 20, GOLD, 500, sp=3)
t(60, 166, "How a KPI Is Measured", 62, TXT, 700)
t(60, 220, "A KPI is the time you wait: from the key press to the right screen.", 27, MUT, 400)
t(60, 258, "Shown is not loaded: we also time when the last grey box is filled.", 27, MUT, 400)

# 1 the key press
y = 300
P1 = 360
layer(y, "1", "The key press", "The clock starts when the key goes out", P1)
# remote
rx, ry = 150, y + 120
box(rx, ry, 110, 190, "#1b1b1b", "#555555", 26, 2.5)
o.append(f'<circle cx="{rx+55}" cy="{ry+70}" r="34" fill="none" stroke="#555555" stroke-width="2.5"/>')
o.append(f'<circle cx="{rx+55}" cy="{ry+70}" r="20" fill="{GOLD}"/>')
o.append(f'<path d="M{rx+49} {ry+60}L{rx+63} {ry+70}L{rx+49} {ry+80}Z" fill="#1a1a1a"/>')  # RIGHT, the real key
for k in range(3):
    o.append(f'<rect x="{rx+22+k*24}" y="{ry+134}" width="18" height="10" rx="4" fill="#555555"/><rect x="{rx+22+k*24}" y="{ry+156}" width="18" height="10" rx="4" fill="#555555"/>')
t(rx + 55, ry + 228, "Press · 0 s", 21, GOLD, 700, "middle", room=200)
harrow(300, 400, ry + 90)
# tv with the screen before the press
sx, sy = 420, ry + 6
screen(sx, sy, 260, 146, "home")
o.append(f'<path d="M{sx+100} {sy+160}H{sx+160}" stroke="#555555" stroke-width="5" stroke-linecap="round"/>')
t(sx + 130, ry + 228, "Home → Guide", 21, TXT, 700, "middle", room=260)
harrow(700, 800, ry + 90)
# recording: a stack of frames with a red dot
fx, fy = 830, ry + 26
for k in range(4, -1, -1):
    o.append(f'<rect x="{fx+k*18}" y="{fy+k*10}" width="170" height="96" rx="8" fill="#1b1b1b" stroke="{GOLD if k == 0 else "#4a4a4a"}" stroke-width="2"/>')
o.append(f'<circle cx="{fx+22}" cy="{fy+22}" r="8" fill="#e05a5a"/>')
t(fx + 38, fy + 29, "REC", 16, TXT, 700, room=60)
t(fx + 120, ry + 228, "5 frames a second", 21, TXT, 700, "middle", room=280)
arrow(600, y + P1, y + P1 + 40)

# 2 every frame after
y += P1 + 40
P2 = 680
layer(y, "2", "Every frame after", "Many apps first draw grey boxes, then fill them", P2)
# four big frames, at the real times of the measurement
big = [
    (0.0, "home", 8, "Press", "the screen before", False),
    (0.96, "blank", 8, "First change", "the page goes blank", False),
    (1.16, "page", 0, "Match", "the KPI, grey boxes left", True),
    (1.36, "page", 8, "Fully Loaded", "no grey box left", True),
]
bx0, bw, bh, bg = 90, 240, 135, 18
by = y + 116
for i, (ts, st, fl, name, cap, key) in enumerate(big):
    x = bx0 + i * (bw + bg)
    screen(x, by, bw, bh, st, filled=fl)
    if key:
        o.append(f'<rect x="{x-4}" y="{by-4}" width="{bw+8}" height="{bh+8}" rx="10" fill="none" stroke="{GOLD}" stroke-width="3"/>')
    t(x + bw / 2, by + bh + 42, f"{ts:g} s", 28, GOLD if key else TXT, 700, "middle", room=bw)
    t(x + bw / 2, by + bh + 72, name, 20, GOLD if key else TXT, 700, "middle", room=bw)
    t(x + bw / 2, by + bh + 98, cap, 17, MUT, 400, "middle", room=bw)
# the strip: one small frame per recorded frame (5 a second), on a true time scale from the press
sy = by + bh + 160
x0, x1, tmax = 110, 1110, 3.4
sc = (x1 - x0) / tmax
fw = 0.2 * sc - 6
fh = fw * 9 / 16
times = [round(0.16 + 0.2 * k, 2) for k in range(17)]  # 0.96, 1.16 and 1.36 are recorded frames


def state_at(ts):
    if ts < 0.96:
        return "home", 8
    if ts < 1.16:
        return "blank", 8
    if ts < 1.36:
        return "page", 0
    return "page", 8


mid = {}
for ts in times:
    xc = x0 + ts * sc
    x = xc - fw / 2
    st, fl = state_at(ts)
    screen(x, sy, fw, fh, st, filled=fl)
    mid[ts] = xc
    if ts in (0.96, 1.16, 1.36):
        o.append(f'<rect x="{x-3:.1f}" y="{sy-3}" width="{fw+6:.1f}" height="{fh+6:.1f}" rx="4" fill="none" stroke="{GOLD if ts > 1 else MUT}" stroke-width="2"/>')
mid[0.0] = x0
# the press: a gold line at 0 s
o.append(f'<path d="M{x0} {sy-8}V{sy+fh+8}" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>')
# connectors from the big frames down to their small frame
for i, (ts, *_r) in enumerate(big):
    bxm = bx0 + i * (bw + bg) + bw / 2
    o.append(f'<path d="M{bxm} {by+bh+110}C{bxm} {sy-30} {mid[ts]:.1f} {by+bh+120} {mid[ts]:.1f} {sy-8}" fill="none" stroke="#4a4a4a" stroke-width="2" stroke-dasharray="5 5"/>')
# time axis under the strip
ay = sy + fh + 22
o.append(f'<path d="M{x0} {ay}H{x1}" stroke="{LINE}" stroke-width="2"/>')
for k in range(4):
    xx = x0 + k * sc
    o.append(f'<path d="M{xx:.1f} {ay-6}V{ay+6}" stroke="{MUT}" stroke-width="2"/>')
    t(f"{xx:.1f}", ay + 28, f"{k} s", 17, MUT, 400, "middle", room=60)
# the 2 s look-ahead after Fully Loaded
bx1, bx2 = x0 + 1.36 * sc - fw / 2, x0 + 3.36 * sc + fw / 2
yb = ay + 48
o.append(f'<path d="M{bx1:.1f} {yb-10}V{yb}H{bx2:.1f}V{yb-10}" fill="none" stroke="{GOLD}" stroke-width="3"/>')
t(f"{(bx1 + bx2) / 2:.1f}", yb + 30, "Nothing new for 2 s", 20, GOLD, 700, "middle", room=bx2 - bx1)
t(600, y + P2 - 26, "Loaded means no grey box is left and nothing new is drawn for 2 seconds.", 20, MUT, 400, "middle")
arrow(600, y + P2, y + P2 + 40)

# 3 the number and its proof: the real KPI header of a measurement, embedded as sent
y += P2 + 40
iw = 1020
ih = round(REAL_H * iw / REAL_W)
P3 = 116 + 40 + ih + 90
layer(y, "3", "The number and its proof", "A real measurement from our platform", P3)
iy = y + 126
cut = 8  # the screenshot's top rows hold the page edge behind the header's rounded corners
o.append(f'<clipPath id="real"><rect x="90" y="{iy+cut}" width="{iw}" height="{ih-cut}" rx="16"/></clipPath>')
o.append(f'<image x="90" y="{iy}" width="{iw}" height="{ih}" clip-path="url(#real)" href="data:image/png;base64,{REAL_B64}"/>')
t(600, iy + ih + 50, "KPI 1.16 s ± 0.2 s, fully loaded 0.2 s later.", 22, GOLD, 700, "middle")
t(600, y + P3 - 26, "No frame passes? Fully Loaded stays empty: a finding, not a pass.", 20, MUT, 400, "middle")

# footer
y += P3
t(600, y + 56, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
Htot = y + 94
o.append("</svg>")
open("docs/img/kpi.svg", "w").write("\n".join(o).replace(H, str(Htot)))
print("docs/img/kpi.svg", Htot)
