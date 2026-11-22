#!/usr/bin/env python3
"""Writes docs/img/freeze-discard.svg (Docs poster: how a freeze alert is told menu or stuck video). Run from the repo root."""
W, H = 1200, 3350
BG, PANEL, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
o = []
def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0):
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{s}</text>')
def box(x, y, w, h, fill=PANEL, stroke=LINE, r=22, sw=2):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def arrow(x, y1, y2):
    o.append(f'<path d="M{x} {y1}V{y2-12}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x-12} {y2-18}L{x} {y2-4}L{x+12} {y2-18}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
def chips(x, y, items, w, gap=16, h=70):
    for i, (a, b) in enumerate(items):
        cx = x + i * (w + gap)
        box(cx, y, w, h, fill="#2a2a2a", r=16)
        t(cx + w / 2, y + 30, a, 22, TXT, 600, "middle")
        t(cx + w / 2, y + 55, b, 16, MUT, 400, "middle")
def layer(y, n, title, sub, h):
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, title, 34, TXT, 700)
    t(156, y + 82, sub, 21, MUT, 400)

GREEN, BLUE = "#4ade80", "#7aa7ff"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Menu or stuck video: how a freeze alert is decided, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
t(60, 100, "AI IN THE LAB · FREEZE ALERTS", 20, GOLD, 500, sp=3)
t(60, 180, "Freeze: menu or stuck video?", 58, TXT, 700)
t(60, 236, "A tiny word model decides in 0.25 ms. Only a sure menu is discarded.", 29, MUT, 400)
t(60, 276, "No language model, no GPU, 0 USD per call.", 24, MUT, 400)

y = 330
layer(y, "1", "The alert", "The picture stopped moving: is it a problem?", 500)
chips(90, y + 112, [("Under 0.8%", "of pixels changed"), ("Menu", "still by design"), ("Stuck video", "a real incident")], 320, 30)
t(600, y + 222, "Same alert, two cases. Only one must be kept.", 19, MUT, 400, "middle")
# a real alert: three frames, Diff 0.0, and the picture is only a screensaver
import base64
_shot = base64.b64encode(open("docs/img/freeze-real-screensaver.jpg", "rb").read()).decode()
for i, lab in enumerate(("Frame -2 · Diff 0.0", "Frame -1 · Diff 0.0", "Current · Diff 0.0")):
    t(90 + 170 + i * 340, y + 262, lab, 16, MUT, 500, "middle")
o.append(f'<clipPath id="ss"><rect x="90" y="{y+272}" width="1020" height="192" rx="12"/></clipPath>')
o.append(f'<image x="90" y="{y+272}" width="1020" height="192" clip-path="url(#ss)" href="data:image/jpeg;base64,{_shot}"/>')
t(600, y + 488, "A real alert on a screensaver. No words to read, so the word model keeps it (0.00).", 19, GOLD, 600, "middle")
arrow(600, y + 500, y + 550)

y = 890
layer(y, "2", "Read the words", "OCR reads the first and the last frame", 250)
chips(90, y + 112, [("First frame", "Home Search Guide"), ("Last frame", "the words again"), ("Device", "stb, mobile, web"), ("No model", "no AI call")], 240, 18)
t(600, y + 222, "The same facts a paid AI model used to get, 1.7 s a call.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

y = 1200
layer(y, "3", "Cut into pieces, weigh them", "Each piece has a learnt weight", 250)
chips(90, y + 112, [("Whole words", "Search, Guide"), ("Word pairs", "tv guide"), ("Letter groups", "2 to 5 letters"), ("Weights", "menu up, video down")], 240, 18)
t(600, y + 222, "A typo like Settinqs still shares most pieces with Settings.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

y = 1510
layer(y, "4", "Decide with a safety band", "The score runs from 0 to 1", 380)
bx0, bx1, by = 150, 1050, y + 130
box(bx0, by, bx1 - bx0, 28, "#2a2a2a", LINE, 14, 2)
o.append(f'<rect x="{bx0}" y="{by}" width="{0.1*(bx1-bx0)}" height="28" rx="14" fill="#16254a" stroke="{BLUE}" stroke-width="2"/>')
o.append(f'<rect x="{bx0+0.9*(bx1-bx0)}" y="{by}" width="{0.1*(bx1-bx0)}" height="28" rx="14" fill="#12301e" stroke="{GREEN}" stroke-width="2"/>')
for v, lab in ((0.1, "0.1"), (0.9, "0.9")):
    x = bx0 + v * (bx1 - bx0)
    o.append(f'<line x1="{x}" y1="{by-12}" x2="{x}" y2="{by+40}" stroke="{TXT}" stroke-width="3"/>')
    t(x, by - 20, lab, 20, TXT, 600, "middle")
for v, c in ((0.04, BLUE), (0.60, GOLD), (0.99, GREEN)):
    o.append(f'<circle cx="{bx0+v*(bx1-bx0)}" cy="{by+14}" r="11" fill="{c}"/>')
for i, (sc, a, b, c) in enumerate([("0.04", "Video: keep", "real incident", BLUE), ("0.60", "Unsure", "bigger check decides", GOLD), ("0.99", "Menu: discard", "alert set aside", GREEN)]):
    cx = 90 + i * 350
    box(cx, y + 200, 320, 130, "#2a2a2a", c, 18, 2)
    t(cx + 160, y + 250, sc, 36, c, 700, "middle")
    t(cx + 160, y + 288, a, 24, TXT, 600, "middle")
    t(cx + 160, y + 314, b, 17, MUT, 400, "middle")
arrow(600, y + 380, y + 430)


# 4b: real examples (real captures of public pages, real OCR words, the real model's score)
import base64
def img(name):
    return base64.b64encode(open(f"docs/img/freeze-real-{name}.jpg", "rb").read()).decode()
y = 1940
layer(y, "5", "Real examples", "Real screens, the words OCR read, the real model's score", 590)
CASES = [("phone", "A phone home screen", "Clock Samsung Free Gaming Hub OneDrive", "0.72", "Unsure: bigger check", GOLD),
         ("tv", "A TV home screen", "Search Home Shop Apps Dune Recommended", "1.00", "Menu: discard", GREEN),
         ("cast", "A live weather cast", "42 40 43 43 44 40 (numbers only)", "0.05", "Video: keep the alert", BLUE)]
IH = 250   # the whole capture is shown inside this box (contain, never cropped by the card)
for i, (nm, ttl, words, sc, dec, col) in enumerate(CASES):
    cx = 90 + i * 350
    box(cx, y + 110, 320, 420, "#2a2a2a", col, 18, 2)
    o.append(f'<clipPath id="c{i}"><rect x="{cx}" y="{y+110}" width="320" height="{IH}" rx="18"/></clipPath>')
    o.append(f'<rect x="{cx}" y="{y+110}" width="320" height="{IH}" rx="18" fill="#0d0d0d"/>')
    o.append(f'<image x="{cx+6}" y="{y+116}" width="308" height="{IH-12}" preserveAspectRatio="xMidYMid meet" clip-path="url(#c{i})" href="data:image/jpeg;base64,{img(nm)}"/>')
    t(cx + 160, y + 110 + IH + 34, ttl, 20, TXT, 600, "middle")
    t(cx + 160, y + 110 + IH + 60, words[:40], 13, MUT, 400, "middle")
    t(cx + 160, y + 110 + IH + 108, sc, 34, col, 700, "middle")
    t(cx + 160, y + 110 + IH + 142, dec, 19, TXT, 600, "middle")
t(600, y + 562, "Real captures, first and last frame the same, scored by the real model.", 17, MUT, 400, "middle")
arrow(600, y + 590, y + 640)

y = 2580
layer(y, "6", "When words are not enough", "A live weather cast or a sports ticker", 250)
chips(90, y + 112, [("Same words", "on moving video"), ("Score", "stays in the middle"), ("Unsure", "bigger check decides"), ("Small model", "learns the answer")], 240, 18)
t(600, y + 222, "AI model or vision check answers, as before. Nothing is lost.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

y = 2890
layer(y, "7", "It learns every night", "Retrained in 1 second from new labels", 250)
chips(90, y + 112, [("Collect", "unsure alerts"), ("Mistakes", "stored as opposite"), ("Never", "its own answers"), ("Test first", "95% or not used")], 240, 18)
t(600, y + 222, "A new version goes live only if it is not worse. The old file is kept.", 19, MUT, 400, "middle")

box(60, 3180, 1080, 120, "#2a2418", GOLD, 22, 2)
t(600, 3230, "0.25 ms · 2 MB · 0 USD per call", 32, GOLD, 700, "middle")
t(600, 3270, "On 1,554 subtitle lines it never saw, 0% were called menu.", 21, TXT, 400, "middle")
t(600, 3326, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
o.append('</svg>')
open("docs/img/freeze-discard.svg", "w").write("\n".join(o))
