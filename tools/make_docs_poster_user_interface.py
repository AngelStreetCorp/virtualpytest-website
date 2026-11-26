#!/usr/bin/env python3
"""Writes docs/img/user-interface.svg (Docs poster: map your app once as a user interface, any test goes to any
screen by pathfinding from where Localize says it is, every move records its KPI (and a channel key its zap),
a variant covers another model without a copy). Source: Learn cards 2.1 user-interface.html ("Map Your App"),
2.2 go-anywhere.html, fingerprint-lesson.html, deep-kpi.html, deep-zapping.html, docs/agent/execution/KPI.md
(kpi_mode screen / zap), docs/agent/navigation/NAVIGATION.md ("Where the path starts"),
2.3 variants.html, and docs/user-guide/running-tests.md "Variants and values for one run".
Run from the repo root.

Fails when a text is wider than its room in DejaVu Sans (headless Chromium's fallback font)."""
from PIL import ImageFont

W = 1200
BG, PANEL, CHIP, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#2a2a2a", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,DejaVu Sans Mono,Menlo,Consolas,monospace"
TTF = {True: "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", False: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"}
o = []


def fit(s, size, bold, room):
    try:
        font = ImageFont.truetype(TTF[bold], size)
    except OSError:
        return
    plain = s.replace("&amp;", "&").replace("&quot;", '"')
    if font.getlength(plain) > room:
        raise SystemExit(f"too wide ({font.getlength(plain):.0f} > {room}): {plain}")


def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0, room=1060, fam=F):
    fit(s, size, w >= 600, room)
    o.append(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{s}</text>')


def box(x, y, w, h, fill=PANEL, stroke=LINE, r=22, sw=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def arrow(x, y1, y2):
    o.append(f'<path d="M{x} {y1}V{y2-12}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x-12} {y2-18}L{x} {y2-4}L{x+12} {y2-18}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')


def move(x1, y1, x2, y2, color=MUT, sw=3):
    """A move between two screens: a straight line with an arrow head at (x2, y2)."""
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 14 * math.cos(a), y2 - 14 * math.sin(a)
    l = (hx - 9 * math.sin(a), hy + 9 * math.cos(a))
    r = (hx + 9 * math.sin(a), hy - 9 * math.cos(a))
    o.append(f'<path d="M{x1} {y1}L{hx:.1f} {hy:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
    o.append(f'<path d="M{l[0]:.1f} {l[1]:.1f}L{x2} {y2}L{r[0]:.1f} {r[1]:.1f}Z" fill="{color}"/>')


def screen(x, y, name, kind, w=180, h=110, hi=False, size=22):
    """A drawn TV screen: a small picture of the screen and its name."""
    box(x, y, w, h, "#2a2418" if hi else "#111111", GOLD if hi else MUT, 10, 3 if hi else 2)
    c = "#4a4a4a"
    if kind == "home":  # a row of tiles
        for k in range(4):
            o.append(f'<rect x="{x+14+k*(w-28)/4:.1f}" y="{y+14}" width="{(w-28)/4-8:.1f}" height="{h*0.3:.1f}" rx="3" fill="{c}"/>')
    elif kind == "guide":  # programme grid
        for k in range(3):
            o.append(f'<rect x="{x+14}" y="{y+12+k*11}" width="{w*0.35:.1f}" height="7" rx="2" fill="{c}"/><rect x="{x+20+w*0.35:.1f}" y="{y+12+k*11}" width="{w*0.45:.1f}" height="7" rx="2" fill="{c}"/>')
    elif kind == "live":  # a play mark
        cx, cy = x + w / 2, y + h * 0.3
        o.append(f'<path d="M{cx-9} {cy-12}L{cx+12} {cy}L{cx-9} {cy+12}Z" fill="{c}"/>')
    elif kind == "settings":  # a list
        for k in range(3):
            o.append(f'<rect x="{x+14}" y="{y+12+k*11}" width="{w*0.6:.1f}" height="7" rx="2" fill="{c}"/>')
    t(x + w / 2, y + h - 22, name, size, GOLD if hi else TXT, 700, "middle", room=w - 16)


def layer(y, n, title, sub, h):
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 60, title, 34, TXT, 700, room=960)
    if sub:
        t(156, y + 94, sub, 21, MUT, 400, room=960)


H = "@@H@@"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Map Your App: map your app once as a user interface, pathfinding and Localize, a KPI on every move, one variant per model</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# header
t(60, 90, "USER INTERFACE", 20, GOLD, 500, sp=3)
t(60, 166, "Map Your App", 62, TXT, 700)
t(60, 220, "Map your app once. Every test reuses the same screens and keys.", 27, MUT, 400)


# 1 the map (card 2.1)
y = 270
P1 = 362
layer(y, "1", "Your app: screens and the moves between them", "Each move: a screen, a key, the next screen", P1)
y1 = y + 140
SW, SH = 170, 106
xs1 = [110, 380, 650, 920]  # Settings, Home, Guide, Live TV
names = [("Settings", "settings"), ("Home", "home"), ("Guide", "guide"), ("Live TV", "live")]
for (nm, kind), x in zip(names, xs1):
    screen(x, y1, nm, kind, SW, SH)
for i, (fwd, back, fwd_left) in enumerate([("Menu", "Back", True), ("OK", "Back", False), ("OK", "Back", False)]):
    a, b = xs1[i] + SW, xs1[i + 1]
    mid = (a + b) / 2
    hi = i == 1
    c = GOLD if hi else MUT
    if fwd_left:  # Home -> Settings goes left
        move(b - 8, y1 + 36, a + 8, y1 + 36, c, 3)
        move(a + 8, y1 + 74, b - 8, y1 + 74, MUT, 3)
    else:
        move(a + 8, y1 + 36, b - 8, y1 + 36, GOLD if hi else MUT, 4 if hi else 3)
        move(b - 8, y1 + 74, a + 8, y1 + 74, MUT, 3)
    t(mid, y1 + 24, fwd, 19, GOLD if hi else MUT, 700, "middle", room=96)
    t(mid, y1 + 100, back, 18, MUT, 600, "middle", room=96)
t(600, y1 + SH + 52, "Home + OK = Guide", 30, GOLD, 700, "middle")
t(600, y + P1 - 22, "You map it once. Every test reuses it.", 21, MUT, 400, "middle")
arrow(600, y + P1, y + P1 + 40)

# 2 goto: Localize, then pathfinding (cards 2.2 go-anywhere, fingerprint lesson step 6; NAVIGATION.md "Where the path starts")
y += P1 + 40
P2 = 384
layer(y, "2", "Write goto, we find the way", "Pathfinding takes the shortest path on the map", P2)
ty = y + 140
box(90, ty, 260, 120, "#111111", LINE, 16)
t(112, ty + 36, "YOUR TEST", 16, MUT, 700, sp=2, room=220)
t(112, ty + 78, 'goto("Settings")', 22, GOLD, 700, fam=MONO, room=226)
t(112, ty + 106, "Just one line", 17, MUT, 400, room=220)
sw2, sh2 = 160, 100
xs = [420, 670, 920]
sy = ty + 10
screen(xs[0], sy, "Guide", "guide", sw2, sh2, size=20)
screen(xs[1], sy, "Home", "home", sw2, sh2, size=20)
screen(xs[2], sy, "Settings", "settings", sw2, sh2, hi=True, size=20)
move(350 + 10, ty + 60, xs[0] - 8, ty + 60, GOLD, 3)
for i, key in enumerate(["Back", "Menu"]):
    a, b = xs[i] + sw2, xs[i + 1]
    move(a + 8, sy + 50, b - 8, sy + 50, GOLD, 4)
    t((a + b) / 2, sy + 36, key, 19, GOLD, 700, "middle", room=80)
# Localize pills: where it starts, where it arrived
for x, label in [(xs[0], "You are here"), (xs[2], "Arrived ✓")]:
    box(x + 5, sy + sh2 + 14, sw2 - 10, 54, "#2a2418", GOLD, 12, 1.5)
    t(x + sw2 / 2, sy + sh2 + 36, "Localize", 15, GOLD, 700, "middle", sp=1, room=sw2 - 20)
    t(x + sw2 / 2, sy + sh2 + 58, label, 16, TXT, 600, "middle", room=sw2 - 20)
t(xs[1] + sw2 / 2, sy + sh2 + 48, "Shortest: 2 steps", 19, GOLD, 700, "middle", room=230)
t(600, y + P2 - 26, "Localize names the live screen by its fingerprint: the path starts there.", 19, MUT, 400, "middle")
arrow(600, y + P2, y + P2 + 40)

# 3 measured in the background (deep-kpi, deep-zapping, KPI.md kpi_mode screen / zap)
y += P2 + 40
P3 = 364
layer(y, "3", "Every move records its KPI", "Measured in the background: the test never waits", P3)
ky = y + 128
for cx, tag, key, nm, kind, val, cap in [
        (90, "KPI", "OK", "Guide", "guide", "1.6 s", "From the key press to the new screen"),
        (620, "ZAP", "CH+", "Live TV", "live", "1.6 s", "From the channel key to the new picture")]:
    box(cx, ky, 490, 172, CHIP, LINE, 18)
    t(cx + 24, ky + 36, tag, 18, GOLD, 700, sp=2, room=100)
    # key pill
    box(cx + 24, ky + 64, 76, 44, "#111111", GOLD, 22, 2)
    t(cx + 62, ky + 93, key, 18, GOLD, 700, "middle", room=66)
    # the measured time between the press and the screen
    o.append(f'<path d="M{cx+112} {ky+86}H{cx+318}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="6 6"/>')
    o.append(f'<path d="M{cx+112} {ky+74}V{ky+98}M{cx+318} {ky+74}V{ky+98}" stroke="{GOLD}" stroke-width="3"/>')
    box(cx + 168, ky + 70, 94, 32, "#2a2418", "#2a2418", 10, 0)
    t(cx + 215, ky + 93, val, 19, TXT, 700, "middle", room=86)
    screen(cx + 330, ky + 44, nm, kind, 136, 84, size=17)
    t(cx + 245, ky + 152, cap, 17, MUT, 400, "middle", room=450)
t(600, y + P3 - 24, "A plain goto already gives these numbers, with no extra test.", 21, GOLD, 700, "middle")
arrow(600, y + P3, y + P3 + 40)

# 4 variants (card 2.3 + running-tests.md)
y += P3 + 40
P4 = 520
layer(y, "4", "Many models, one map", "Add only what differs; the same test runs on all", P4)
cy = y + 116
box(450, cy, 300, 72, "#111111", LINE, 16)
t(600, cy + 32, 'goto("Guide")', 24, GOLD, 700, "middle", fam=MONO, room=270)
t(600, cy + 58, "Same test", 17, MUT, 400, "middle", room=270)
cards = [(90, "Model A", "Base", "OK", False), (620, "Model B", "Variant", "Right, OK", True)]
ky = y + 222
for cx, model, tag, key, edited in cards:
    o.append(f'<path d="M600 {cy+72}C600 {ky-30} {cx+245} {cy+100} {cx+245} {ky-6}" fill="none" stroke="{LINE}" stroke-width="3"/>')
for cx, model, tag, key, edited in cards:
    box(cx, ky, 490, 210, CHIP, GOLD if edited else LINE, 18, 2, "10 8" if edited else "")
    t(cx + 24, ky + 38, model, 22, TXT, 700, room=200)
    tw = 100 if edited else 80
    box(cx + 466 - tw, ky + 16, tw, 32, "#2a2418" if edited else "#333333", GOLD if edited else "#333333", 16, 1.5)
    t(cx + 466 - tw / 2, ky + 38, tag, 16, GOLD if edited else MUT, 600, "middle", room=tw - 12)
    sx1, sx2 = cx + 24, cx + 316
    screen(sx1, ky + 70, "Home", "home", 150, 92, size=19)
    screen(sx2, ky + 70, "Guide", "guide", 150, 92, size=19)
    move(sx1 + 150 + 8, ky + 116, sx2 - 8, ky + 116, GOLD if edited else MUT, 4 if edited else 3)
    t((sx1 + 150 + sx2) / 2, ky + 102, key, 18, GOLD if edited else MUT, 700, "middle", room=128)
    t(cx + 245, ky + 186, "Only this move is edited" if edited else "Base map", 18, GOLD if edited else MUT, 600 if edited else 400, "middle", room=440)
t(600, y + P4 - 56, "No copy of the map: a variant keeps only what changes, like one key.", 20, TXT, 600, "middle")
t(600, y + P4 - 24, "A variant can be a model, a firmware, a language or an app build.", 19, MUT, 400, "middle")

# footer
y += P4
t(600, y + 56, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
Htot = y + 94
o.append("</svg>")
open("docs/img/user-interface.svg", "w").write("\n".join(o).replace(H, str(Htot)))
print("docs/img/user-interface.svg", Htot)
