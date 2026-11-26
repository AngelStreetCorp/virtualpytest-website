#!/usr/bin/env python3
"""Writes docs/img/test-to-report.svg (Docs poster: one real QuickTest, from the steps to the report).

Sources: Learn card learn/cards/quicktest.html (4.2, title "A quick test, step by step"); product docs
features/quicktest.md, features/visual-capture.md, user-guide/running-tests.md, user-guide/sharing-reports.md.
The two pictures are real screens of our platform (dark theme): the QuickTest Builder with a 3-step test on a public
demo website, and the report of its run. Run from the repo root:

    python3 tools/make_docs_poster_test-to-report.py [--from DIR]

--from DIR rebuilds docs/img/test-to-report-real-steps.jpg and -real-report.jpg from DIR/quicktest-steps.png
(1400x596) and DIR/quicktest-report.png (1280x980): the builder is cropped to its top bar and its steps, and the
report's dates and clock times are painted over with the background (no date on a poster).

Fails when a text is wider than its room in DejaVu Sans (headless Chromium's fallback font)."""
import base64
import sys

from PIL import Image, ImageDraw, ImageFont

W = 1200
BG, PANEL, CHIP, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#2a2a2a", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
TTF = {True: "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", False: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"}
STEPS_JPG, REPORT_JPG = "docs/img/test-to-report-real-steps.jpg", "docs/img/test-to-report-real-report.jpg"
o = []


def prepare(src):
    b = Image.open(f"{src}/quicktest-steps.png").convert("RGB")
    top, steps = b.crop((296, 0, 1400, 46)), b.crop((296, 272, 1400, 580))
    out = Image.new("RGB", (1104, 46 + 308), (22, 22, 22))
    out.paste(top, (0, 0))
    out.paste(steps, (0, 46))
    out.save(STEPS_JPG, quality=88)
    r = Image.open(f"{src}/quicktest-report.png").convert("RGB")
    d = ImageDraw.Draw(r)
    d.rectangle((405, 10, 660, 40), fill=r.getpixel((900, 25)))  # date, start and end time
    for y, x0 in ((410, 135), (555, 172), (617, 135), (763, 172), (825, 135)):  # Start / End clock lines
        d.rectangle((x0, y - 7, 620, y + 7), fill=r.getpixel((800, y)))
    r.save(REPORT_JPG, quality=88)


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


def box(x, y, w, h, fill=PANEL, stroke=LINE, r=22, sw=2):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def arrow(x, y1, y2):
    o.append(f'<path d="M{x} {y1}V{y2-12}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x-12} {y2-18}L{x} {y2-4}L{x+12} {y2-18}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')


def layer(y, n, title, sub, h):
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, title, 34, TXT, 700, room=960)
    if sub:
        t(156, y + 82, sub, 21, MUT, 400, room=960)


def shot(path, x, y, w):
    """Embed a real screenshot (base64 JPG) at width w; returns its height."""
    im = Image.open(path)
    h = round(im.height * w / im.width)
    data = base64.b64encode(open(path, "rb").read()).decode()
    o.append(f'<rect x="{x-3}" y="{y-3}" width="{w+6}" height="{h+6}" rx="10" fill="none" stroke="{LINE}" stroke-width="2"/>')
    o.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="data:image/jpeg;base64,{data}"/>')
    return h


def chips(x, y, items, w, gap=18, h=70):
    for i, (a, b) in enumerate(items):
        cx = x + i * (w + gap)
        box(cx, y, w, h, fill=CHIP, r=16)
        t(cx + w / 2, y + 30, a, 22, TXT, 600, "middle", room=w - 16)
        t(cx + w / 2, y + 55, b, 16, MUT, 400, "middle", room=w - 16)


if "--from" in sys.argv:
    prepare(sys.argv[sys.argv.index("--from") + 1])

H = "@@H@@"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">A quick test, step by step: the steps you write in the QuickTest Builder, then the report you get</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# header (Learn lesson 4.2, QuickTest)
t(60, 90, "WRITE TESTS · QUICKTEST", 20, GOLD, 500, sp=3)
t(60, 166, "A quick test, step by step", 62, TXT, 700)
t(60, 220, "Go to a website, check one text, done.", 29, MUT, 400)
t(60, 258, "Real screens from our platform.", 21, MUT, 400)

# 1 the steps you write
y = 300
layer(y, "1", "Write your steps", "QuickTest Builder: pick the user interface, add steps", 0)
ih = shot(STEPS_JPG, 90, y + 112, 1020)
cy = y + 112 + ih + 22
chips(90, cy, [("Interface", "the website to test"), ("Go to node", "home, then products"), ("Verification", "the text Products")], 328, 18)
P1 = cy + 70 + 30 - y
o[[i for i, s in enumerate(o) if s.startswith(f'<rect x="60" y="{y}"')][0]] = f'<rect x="60" y="{y}" width="1080" height="{P1}" rx="22" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>'
arrow(600, y + P1, y + P1 + 40)

# 2 the report you get
y += P1 + 40
layer(y, "2", "Open the report", "Status PASS in 23 s, a screenshot for every step", 0)
ih = shot(REPORT_JPG, 160, y + 112, 880)
P2 = 112 + ih + 34
o[[i for i, s in enumerate(o) if s.startswith(f'<rect x="60" y="{y}"')][0]] = f'<rect x="60" y="{y}" width="1080" height="{P2}" rx="22" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>'
arrow(600, y + P2, y + P2 + 40)

# 3 what every report keeps (the report's own section names)
y += P2 + 40
P3 = 186
box(60, y, 1080, P3, "#2a2418", GOLD)
t(90, y + 54, "Same report as every test", 30, GOLD, 700)
chips(90, y + 84, [("Test Mosaic", "all steps at a glance"), ("Video timeline", "the whole run"), ("Test Steps", "each with a screenshot"), ("Share", "a link that expires")], 240, 18)

# footer
y += P3
t(600, y + 56, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
Htot = y + 94
o.append("</svg>")
open("docs/img/test-to-report.svg", "w").write("\n".join(o).replace(H, str(Htot)))
print("docs/img/test-to-report.svg", Htot)
