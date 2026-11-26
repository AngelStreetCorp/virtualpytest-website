#!/usr/bin/env python3
"""Writes docs/img/localize.svg (Docs poster "How Localize names the screen", for humans).

Sources: Learn lesson 3.4 "Know every screen by its layout" and its Go deeper "How Localize names the screen"
(3.4/deep2), and docs/agent/navigation/FINGERPRINT.md of the product repo. The plain-language companion of the
`fingerprint` poster: same words (fingerprint, saved screen, highlight, title, not sure), no dhash and no bits.
Every screen is drawn and generic; every number comes from tools/localize_example_values.json, written by
tools/localize_example_draw.py from the real ImageHelpers.identify_screen. No date anywhere on the poster.
Run from the repo root. If DejaVu Sans is installed (the font headless Chromium falls back to), every label with a
width limit is measured and the script fails when one is too wide.
"""
import base64, json, os, sys

W = 1200
BG, PANEL, LINE, TXT, MUT, GOLD, CHIP = "#161616", "#212121", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d", "#2a2a2a"
GREEN, RED = "#4ade80", "#f87171"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
o, checks = [], []
V = json.load(open("tools/localize_example_values.json"))
LIVE = V["live"]
NAMES = {"home": "Home", "home_movies": "Home · Movies tab", "home_guide": "Home · Guide tab",
         "recordings": "Recordings", "favourites": "Favourites", "settings": "Settings"}
SHORT = {"home": "Home", "home_movies": "Home · Movies", "home_guide": "Home · Guide",
         "recordings": "Recordings", "favourites": "Favourites", "settings": "Settings"}
TAB = {"home": "Home", "home_movies": "Movies", "home_guide": "Guide"}   # the tab each drawn screen highlights
FLOOR = V["FP_SELF_DRIFT_FLOOR"]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0, maxw=None):
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{esc(s)}</text>')
    if maxw:
        checks.append((s, size, w >= 600, maxw))

def box(x, y, w, h, fill=PANEL, stroke=LINE, r=22, sw=2):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

def arrow(x, y1, y2):
    o.append(f'<path d="M{x} {y1}V{y2-12}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x-12} {y2-18}L{x} {y2-4}L{x+12} {y2-18}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')

def arrow_r(x1, x2, y):
    o.append(f'<path d="M{x1} {y}H{x2-12}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x2-18} {y-12}L{x2-4} {y}L{x2-18} {y+12}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')

def shot(x, y, name, w=320, h=180, stroke=LINE, sw=2):
    data = base64.b64encode(open(f"docs/img/localize-real-{name}.jpg", "rb").read()).decode()
    o.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/jpeg;base64,{data}"/>')
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{stroke}" stroke-width="{sw}"/>')

def ring(x, y, w, h):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{GOLD}" stroke-width="3"/>')

def answer(y, label, right):
    """The gold answer bar: 'You are on <label>' and the confidence on the right."""
    box(90, y, 1020, 64, fill="#2a2418", stroke=GOLD, r=16, sw=2)
    t(116, y + 41, "You are on", 22, MUT, 400)
    t(240, y + 42, label, 28, GOLD, 700, maxw=600)
    t(1086, y + 40, right, 20, MUT, 400, "end", maxw=260)

def card(y, n, title, sub, h, draw, last=False):
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, title, 34, TXT, 700, maxw=1140 - 156 - 20)
    t(156, y + 82, sub, 21, MUT, 400, maxw=1140 - 156 - 20)
    draw(y + 112)
    if not last:
        arrow(600, y + h, y + h + 50)
    return y + h + 50

def dist(live, node):
    return next(r["dist"] for r in LIVE[live]["ranked"] if r["node_id"] == node)

def conf(c):
    return f"confidence {c:.2f}"

# ---------------------------------------------------------------- 1. live screen -> fingerprint -> the wall
def c1(y):
    L = "live_movies"
    shot(90, y, L)
    t(250, y + 208, "The live screen", 19, MUT, 400, "middle")
    arrow_r(426, 476, y + 90)
    cell, gx = 11, 486
    bits = bin(int(LIVE[L]["dhash"], 16))[2:].zfill(256)
    o.append(f'<rect x="{gx}" y="{y+2}" width="{16*cell}" height="{16*cell}" rx="4" fill="#161616" stroke="{LINE}"/>')
    o.append(f'<g fill="{TXT}">' + "".join(f'<rect x="{gx+(i%16)*cell+1}" y="{y+3+(i//16)*cell}" width="{cell-2}" height="{cell-2}" rx="1"/>' for i, b in enumerate(bits) if b == "1") + "</g>")
    t(gx + 88, y + 208, "Its fingerprint", 19, MUT, 400, "middle")
    tx = 712
    for i, line in enumerate(["The screen is shrunk to a tiny grid.", "Each square notes if it is lighter or",
                              "darker than its neighbour. Small details", "melt away; the layout stays.",
                              "Like a face: new hair, same face."]):
        t(tx, y + 40 + i * 32, line, 20, TXT if i < 4 else GOLD, 400 if i < 4 else 600, maxw=1110 - tx)
    # the wall of saved screens
    wy = y + 262
    t(90, wy, "SAVED SCREENS OF THE NAVIGATION TREE", 16, GOLD, 600, sp=2)
    t(1110, wy, "SQUARES THAT DIFFER", 16, GOLD, 600, "end", sp=1)
    order = [r["node_id"] for r in LIVE[L]["ranked"]]
    tw, th, gap = 150, 84, 24
    for i, n in enumerate(order):
        x, d = 90 + i * (tw + gap), dist(L, n)
        close = d <= FLOOR
        shot(x, wy + 18, n, tw, th, GOLD if close else LINE, 3 if close else 2)
        t(x + tw // 2, wy + 18 + th + 26, SHORT[n], 17, TXT, 600, "middle", maxw=tw + gap - 6)
        t(x + tw // 2, wy + 18 + th + 54, str(d), 24, GOLD if close else MUT, 700, "middle")
    ny = wy + 18 + th + 96
    n_close = sum(1 for r in LIVE[L]["ranked"] if r["dist"] <= FLOOR)
    t(600, ny, f"{n_close} saved screens are close: same layout, new posters. Which one is it?", 20, TXT, 500, "middle", maxw=1020)

# ---------------------------------------------------------------- 2. look-alikes: the highlight
def c2(y):
    L, lf = "live_movies", LIVE["live_movies"]["live_focus"]
    t(90, y + 10, f"On the live screen the highlight is under {TAB['home_movies']}.", 21, TXT, 500, maxw=1020)
    y += 40
    win = LIVE[L]["candidates"][0]["node_id"]
    for i, n in enumerate(["home", "home_movies", "home_guide"]):
        x = 90 + i * 350
        f = V["wall"][n]["focus"]
        ok = n == win
        shot(x, y, n, stroke=GOLD if ok else LINE, sw=3 if ok else 2)
        ring(round(x + (f["x"] - f["width"] / 2) * 320 - 8), y + 8, round(f["width"] * 320 + 16), 26)
        t(x + 160, y + 212, NAMES[n], 21, TXT, 700, "middle", maxw=320)
        t(x + 160, y + 240, f"{dist(L, n)} squares differ", 18, MUT, 400, "middle", maxw=320)
        t(x + 160, y + 270, f"highlight under {TAB[n]} {'✓' if ok else '✗'}", 19, GREEN if ok else RED, 600, "middle", maxw=320)
    answer(y + 300, NAMES[win], conf(LIVE[L]["candidates"][0]["confidence"]))

# ---------------------------------------------------------------- 3. look-alikes: the title
def c3(y):
    L = "live_favourites"
    lt = LIVE[L]["title"]
    win = LIVE[L]["candidates"][0]["node_id"]
    shot(90, y, L)
    ring(90 + 8, y + 3, 76, 22)
    t(250, y + 212, "The live screen", 21, TXT, 700, "middle")
    t(250, y + 240, f"title read: {lt}", 18, MUT, 400, "middle", maxw=320)
    for i, n in enumerate(["recordings", "favourites"]):
        x = 440 + i * 350
        ok = n == win
        shot(x, y, n, stroke=GOLD if ok else LINE, sw=3 if ok else 2)
        ring(x + 8, y + 3, 76, 22)
        t(x + 160, y + 212, NAMES[n], 21, TXT, 700, "middle", maxw=320)
        t(x + 160, y + 240, f"{dist(L, n)} squares differ", 18, MUT, 400, "middle", maxw=320)
        sc = LIVE[L]["title_scores"][n]
        t(x + 160, y + 270, f"title match {sc:.2f} {'✓' if ok else '✗'}", 19, GREEN if ok else RED, 600, "middle", maxw=320)
    answer(y + 300, NAMES[win], conf(LIVE[L]["candidates"][0]["confidence"]))

# ---------------------------------------------------------------- 4. not sure
def c4(y):
    L = "live_search"
    shot(90, y, L)
    t(250, y + 212, "The live screen", 21, TXT, 700, "middle")
    t(250, y + 240, "a screen not saved in the tree", 18, MUT, 400, "middle", maxw=320)
    sx = 470
    t(sx, y + 14, "CLOSEST SCREENS", 16, GOLD, 600, sp=2)
    t(1110, y + 14, "SQUARES THAT DIFFER", 16, GOLD, 600, "end", sp=1)
    for i, r in enumerate(LIVE[L]["ranked"][:4]):
        yy = y + 50 + i * 36
        o.append(f'<line x1="{sx}" y1="{yy-24}" x2="1110" y2="{yy-24}" stroke="{LINE}" stroke-width="1"/>')
        t(sx, yy, NAMES[r["node_id"]], 20, TXT, 500)
        t(1110, yy, str(r["dist"]), 20, RED, 600, "end")
    best = LIVE[L]["ranked"][0]["dist"]
    t(sx, y + 210, f"A saved screen must be within {FLOOR}. The closest is {best}.", 19, MUT, 400, maxw=1110 - sx)
    t(sx, y + 240, "It says so and shows these screens; it never picks one.", 19, MUT, 400, maxw=1110 - sx)
    box(90, y + 270, 1020, 64, fill="#2a2418", stroke=GOLD, r=16, sw=2)
    t(116, y + 270 + 42, "Not sure", 28, GOLD, 700)
    t(1086, y + 270 + 40, "no answer is better than a wrong one", 20, MUT, 400, "end", maxw=700)

# ---------------------------------------------------------------- 5. black screen / no signal
def c5(y):
    for i, (L, cap) in enumerate([("live_black", "the box is asleep"), ("live_bars", "no picture reaches the lab")]):
        x = 90 + i * 350
        shot(x, y, L)
        t(x + 160, y + 212, LIVE[L]["state_label"], 22, GOLD, 700, "middle", maxw=320)
        t(x + 160, y + 240, cap, 18, MUT, 400, "middle", maxw=320)
    tx = 790
    for i, line in enumerate(["These two look the same", "on every device: a TV box,", "a phone, a TV.",
                              "No saved screen needed,", "named on every device."]):
        t(tx, y + 40 + i * 32, line, 20, TXT if i < 3 else GOLD, 400 if i < 3 else 600, maxw=1110 - tx)

# ---------------------------------------------------------------- 6. why it matters (chips)
INNER_X, INNER_W, CH, CGAP = 90, 1020, 70, 18
def c6(y):
    row = [("Before a goto", "where am I? then go"), ("Arrival", "the goto proves it"),
           ("Measures", "when a screen shows"), ("Monitoring", "every device, all day")]
    w = (INNER_W - 3 * CGAP) / 4
    for i, (a, b) in enumerate(row):
        cx = INNER_X + i * (w + CGAP)
        box(round(cx), y, round(w), CH, fill=CHIP, r=16)
        t(round(cx + w / 2), y + 30, a, 22, TXT, 600, "middle", maxw=w - 20)
        t(round(cx + w / 2), y + 55, b, 16, MUT, 400, "middle", maxw=w - 16)
    t(600, y + 112, "Lost, with no known position? A goto asks Localize first,", 20, TXT, 500, "middle", maxw=1020)
    t(600, y + 142, "then finds the way from the screen it names.", 20, TXT, 500, "middle", maxw=1020)

o.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 @@H@@" width="1200" height="@@H@@" role="img" aria-labelledby="ti"><title id="ti">How Localize names the screen: the live screen is turned into a fingerprint, compared with every saved screen, look-alikes are told apart by the highlight and the title, a screen it cannot name gets a not sure answer, and black screen and no signal are named on any device</title>')
o.append('<rect width="1200" height="@@H@@" fill="%s"/>' % BG)
t(60, 100, "UI VERIFICATION · LOCALIZE", 20, GOLD, 500, sp=3)
t(60, 180, "How Localize names the screen", 58, TXT, 700, maxw=1080)
t(60, 236, "Where am I? It looks at the live screen and names it,", 29, MUT, 400, maxw=1080)
t(60, 276, "the way you know a face. When it is not sure, it says so.", 29, MUT, 400, maxw=1080)

y = 330
y = card(y, "1", "Which screen is this?", "The live fingerprint is compared with every saved screen", 112 + 262 + 18 + 84 + 96 + 30, c1)
y = card(y, "2", "Look-alikes: where is the highlight?", "Same layout: the underline under the menu tab decides", 112 + 40 + 300 + 64 + 30, c2)
y = card(y, "3", "Look-alikes: read the title", "Same squares: the title in the top-left corner decides", 112 + 300 + 64 + 30, c3)
y = card(y, "4", "One answer, or \"not sure\"", "No saved screen is close enough: it never guesses", 112 + 270 + 64 + 30, c4)
y = card(y, "5", "Black Screen and No Signal", "Named on any device, from the picture alone", 112 + 260, c5)
y = card(y, "6", "Why it matters", "A test knows where it is before it presses a key", 112 + 160, c6, last=True)
H = y + 40
t(600, H - 30, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
o.append("</svg>")
svg = "\n".join(o).replace("@@H@@", str(H))
open("docs/img/localize.svg", "w").write(svg)

FONTS = {True: "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", False: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"}
if os.path.exists(FONTS[True]):
    from PIL import ImageFont
    bad = []
    for s, size, bold, maxw in checks:
        wpx = ImageFont.truetype(FONTS[bold], size).getlength(s)
        if wpx > maxw:
            bad.append(f"{wpx:.0f} > {maxw:.0f} px: {s}")
    if bad:
        sys.exit("text wider than its box with the fallback font:\n  " + "\n  ".join(bad))
print(f"docs/img/localize.svg written, {W}x{H}, {len(checks)} labels fit")
