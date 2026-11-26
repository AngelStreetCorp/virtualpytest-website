#!/usr/bin/env python3
"""Writes docs/img/remotes.svg (Docs poster: Its Own Remote, built around the controller; sources: Learn cards
own-remote.html and any-device.html, docs/technical/architecture/CONTROLLER_CREATION_GUIDE.md (controller types,
registry), APPIUM_REMOTE_IMPLEMENTATION.md, docs/get-started/hardware.md and configuration.md (IR transmitter, IR over
serial), docs/user-guide/nintendo-switch.md (Bluetooth controller), troubleshooting.md (Android by USB), local-dev.md
(Android over ADB on the network), the network remote of a TV (docs/agent/devices), the fixnet modem on its serial port
(release notes: send digits, play audio). Run from the repo root.

Fails when a text is wider than its room in DejaVu Sans (headless Chromium's fallback font)."""
from PIL import ImageFont

W = 1200
BG, PANEL, CHIP, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#2a2a2a", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
DARKG = "#2a2418"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
MONO = "DejaVu Sans Mono,Menlo,Consolas,monospace"
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


def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0, room=1060, fam=F):
    fit(s, size, w >= 600, room)
    o.append(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{s}</text>')


def box(x, y, w, h, fill=PANEL, stroke=LINE, r=22, sw=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def arrow(x, y1, y2):
    o.append(f'<path d="M{x} {y1}V{y2-12}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x-12} {y2-18}L{x} {y2-4}L{x+12} {y2-18}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')


def chips(x, y, items, w, gap=16, h=70):
    for i, (a, b) in enumerate(items):
        cx = x + i * (w + gap)
        box(cx, y, w, h, fill=CHIP, r=16)
        t(cx + w / 2, y + 30, a, 22, TXT, 600, "middle", room=w - 16)
        t(cx + w / 2, y + 55, b, 16, MUT, 400, "middle", room=w - 16)


def layer(y, n, title, sub, h):
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, title, 34, TXT, 700, room=960)
    if sub:
        t(156, y + 82, sub, 21, MUT, 400, room=960)


def key(cx, cy, label, r=30, size=22):
    """A round remote key, gold."""
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GOLD}" stroke="#f3d3a8" stroke-width="3"/>')
    t(cx, cy + size * 0.36, label, size, "#1a1a1a", 700, "middle", room=2 * r)


def pills(cx, y, labels, gold_first=True):
    """The keys a device takes, as small pills centred on cx (the first is the one OK becomes)."""
    widths = [ImageFont.truetype(TTF[True], 16).getlength(s) + 26 for s in labels]
    total = sum(widths) + 8 * (len(labels) - 1)
    x = cx - total / 2
    for i, (s, w) in enumerate(zip(labels, widths)):
        on = gold_first and i == 0
        box(x, y, w, 32, GOLD if on else "#333333", GOLD if on else "#444444", 16, 1.5)
        t(x + w / 2, y + 22, s, 16, "#1a1a1a" if on else TXT, 700, "middle", room=w)
        x += w + 8


def waves(x, y, flip=False):
    """Infrared: three arcs leaving a point."""
    s = -1 if flip else 1
    for k, r in enumerate((12, 22, 32)):
        o.append(f'<path d="M{x+s*r*0.5} {y-r*0.85}A{r} {r} 0 0 {1 if s>0 else 0} {x+s*r*0.5} {y+r*0.85}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" opacity="{1-k*0.25}"/>')


def stb(x, y):
    """A drawn set-top box with a small screen above it."""
    o.append(f'<rect x="{x}" y="{y}" width="110" height="30" rx="6" fill="#333" stroke="{MUT}" stroke-width="2.5"/>'
             f'<circle cx="{x+14}" cy="{y+15}" r="4" fill="#4ade80"/><rect x="{x+70}" y="{y+11}" width="28" height="8" rx="3" fill="#555"/>')


def tv(x, y, w=110, h=66):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#111" stroke="{MUT}" stroke-width="2.5"/>'
             f'<path d="M{x+w/2-18} {y+h+8}H{x+w/2+18}" stroke="{MUT}" stroke-width="2.5" stroke-linecap="round"/>')


def ir_dongle(x, y):
    """A small USB infrared transmitter."""
    o.append(f'<rect x="{x}" y="{y}" width="40" height="20" rx="5" fill="{DARKG}" stroke="{GOLD}" stroke-width="2"/>'
             f'<circle cx="{x+40}" cy="{y+10}" r="5" fill="{GOLD}"/>')


def bt_rune(cx, cy, s=1.0, col=GOLD):
    """The Bluetooth rune, drawn as lines."""
    p = lambda dx, dy: f"{cx+dx*s:.1f} {cy+dy*s:.1f}"
    o.append(f'<path d="M{p(-9,-9)}L{p(9,9)}L{p(0,18)}V{cy-18*s:.1f}L{p(9,-9)}L{p(-9,9)}" fill="none" stroke="{col}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')


def remote(x, y):
    """A drawn handheld remote."""
    o.append(f'<rect x="{x}" y="{y}" width="34" height="96" rx="14" fill="#333" stroke="{MUT}" stroke-width="2.5"/>'
             f'<circle cx="{x+17}" cy="{y+30}" r="9" fill="none" stroke="{MUT}" stroke-width="2"/><circle cx="{x+17}" cy="{y+30}" r="3.5" fill="{GOLD}"/>'
             f'<circle cx="{x+10}" cy="{y+58}" r="3" fill="{MUT}"/><circle cx="{x+24}" cy="{y+58}" r="3" fill="{MUT}"/>'
             f'<circle cx="{x+10}" cy="{y+72}" r="3" fill="{MUT}"/><circle cx="{x+24}" cy="{y+72}" r="3" fill="{MUT}"/>')


def phone(x, y):
    o.append(f'<rect x="{x}" y="{y}" width="56" height="100" rx="10" fill="#111" stroke="{MUT}" stroke-width="2.5"/>'
             f'<rect x="{x+20}" y="{y+6}" width="16" height="4" rx="2" fill="#444"/>')


def browser(x, y, w=170, h=104):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#f2f2f2" stroke="{MUT}" stroke-width="2"/>'
             f'<path d="M{x} {y+22}H{x+w}" stroke="#cfcfcf" stroke-width="2"/>'
             + "".join(f'<circle cx="{x+14+i*14}" cy="{y+11}" r="4" fill="#bdbdbd"/>' for i in range(3)))


def cursor(x, y):
    o.append(f'<path d="M{x} {y}L{x} {y+26}L{x+7} {y+20}L{x+12} {y+31}L{x+17} {y+29}L{x+12} {y+18}L{x+21} {y+18}Z" fill="#1a1a1a" stroke="#f2f2f2" stroke-width="1.8" stroke-linejoin="round"/>')


def console(x, y):
    """A drawn game console and its controller."""
    o.append(f'<rect x="{x}" y="{y}" width="96" height="44" rx="8" fill="#333" stroke="{MUT}" stroke-width="2.5"/>'
             f'<path d="M{x+14} {y+30}H{x+50}" stroke="#555" stroke-width="5" stroke-linecap="round"/><circle cx="{x+80}" cy="{y+22}" r="4" fill="#4ade80"/>')


def gamepad(x, y):
    o.append(f'<path d="M{x+12} {y}H{x+58}Q{x+70} {y} {x+70} {y+14}V{y+30}Q{x+70} {y+42} {x+58} {y+38}L{x+48} {y+30}H{x+22}L{x+12} {y+38}Q{x} {y+42} {x} {y+30}V{y+14}Q{x} {y} {x+12} {y}Z" fill="#333" stroke="{MUT}" stroke-width="2.5"/>'
             f'<path d="M{x+15} {y+16}H{x+27}M{x+21} {y+10}V{y+22}" stroke="{MUT}" stroke-width="2.5"/><circle cx="{x+52}" cy="{y+12}" r="4" fill="{GOLD}"/><circle cx="{x+46}" cy="{y+21}" r="3.5" fill="{MUT}"/>')


def wifi(cx, cy, s=1.0):
    """Network: three arcs and a dot."""
    for k, r in enumerate((10, 20, 30)):
        r *= s
        o.append(f'<path d="M{cx-r*0.75:.1f} {cy-r*0.66:.1f}A{r:.1f} {r:.1f} 0 0 1 {cx+r*0.75:.1f} {cy-r*0.66:.1f}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" opacity="{1-k*0.2}"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{GOLD}"/>')


def modem(x, y):
    o.append(f'<rect x="{x}" y="{y}" width="90" height="40" rx="8" fill="#333" stroke="{MUT}" stroke-width="2.5"/>'
             f'<path d="M{x+70} {y}V{y-26}" stroke="{MUT}" stroke-width="2.5" stroke-linecap="round"/>'
             + "".join(f'<circle cx="{x+16+i*14}" cy="{y+20}" r="3.5" fill="{"#4ade80" if i == 0 else "#555"}"/>' for i in range(3)))


H = "@@H@@"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Its Own Remote: one key, written once, goes out through the controller each device uses, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# header (Learn card own-remote.html)
t(60, 90, "CONTROL ANY DEVICE", 20, GOLD, 500, sp=3)
t(60, 166, "Its Own Remote", 62, TXT, 700)
t(60, 220, "Its own controller, its own keys, for every device", 29, MUT, 400)

# 1 the test sends a key, written once
y = 270
P1 = 290
layer(y, "1", "Tests send the same keys", "Write the test once", P1)
tx, ty = 156, y + 112
box(tx, ty, 470, 140, "#1b1b1b", LINE, 14)
t(tx + 22, ty + 32, "TEST", 16, GOLD, 700, sp=2, room=200)
for i, (step, on) in enumerate([("Press HOME", False), ("Press OK", True)]):
    ry = ty + 46 + i * 42
    if on:
        box(tx + 14, ry, 442, 36, DARKG, GOLD, 8, 1.5)
    t(tx + 30, ry + 25, f"{i+1}", 18, MUT, 600, room=20, fam=MONO)
    t(tx + 62, ry + 25, step, 20, GOLD if on else TXT, 600 if on else 400, room=370, fam=MONO)
o.append(f'<path d="M{tx+470} {ty+105}H{895}" stroke="{GOLD}" stroke-width="4" stroke-dasharray="2 12" stroke-linecap="round"/>')
key(960, ty + 70, "OK", 58, 40)
arrow(600, y + P1, y + P1 + 40)

# 2 one key, seven controllers, each drawn with its device
y += P1 + 40
P2 = 950
layer(y, "2", "The right remote for each device", "The key goes out through the controller the device uses", P2)
kx, ky = 600, y + 150
CW, CH, GAP = 240, 290, 24
row1 = [(84 + i * (CW + GAP), y + 245) for i in range(4)]
row2 = [(216 + i * (CW + GAP), y + 245 + CH + 40) for i in range(3)]
for cx, cy in row1:
    ex = cx + CW / 2
    o.append(f'<path d="M{kx} {ky+30}C{kx} {ky+75} {ex} {cy-55} {ex} {cy}" fill="none" stroke="{LINE}" stroke-width="4"/>')
    o.append(f'<circle cx="{ex}" cy="{cy-14}" r="6" fill="{GOLD}"/>')
for cx, cy in row2:
    gx = cx + CW / 2  # row 2 centres sit on the gaps of row 1
    top = row1[0][1] - 30
    if gx == kx:
        o.append(f'<path d="M{kx} {ky+30}V{cy}" fill="none" stroke="{LINE}" stroke-width="4"/>')
    else:
        o.append(f'<path d="M{kx} {ky+30}C{kx} {ky+70} {gx} {top-40} {gx} {top}V{cy}" fill="none" stroke="{LINE}" stroke-width="4"/>')
    o.append(f'<circle cx="{gx}" cy="{cy-14}" r="6" fill="{GOLD}"/>')
key(kx, ky, "OK", 34, 26)


def card(x, y, ctl, name, keys):
    """Controller on top (the pill), the drawn device, its name, and its keys (gold: what OK becomes)."""
    box(x, y, CW, CH, CHIP, LINE, 18)
    w = ImageFont.truetype(TTF[True], 19).getlength(ctl) + 32
    box(x + CW / 2 - w / 2, y + 18, w, 36, DARKG, GOLD, 18, 1.5)
    t(x + CW / 2, y + 43, ctl, 19, GOLD, 700, "middle", room=w)
    t(x + CW / 2, y + 222, name, 22, TXT, 700, "middle", room=CW - 20)
    pills(x + CW / 2, y + 240, keys)


def lbl(x, y, s):
    t(x, y, s, 15, MUT, 400, "middle", room=110)


x, cy = row1[0]
card(x, cy, "Infrared", "TV box", ["OK", "Menu", "Back"])
ir_dongle(x + 22, cy + 122)
waves(x + 74, cy + 132)
stb(x + 112, cy + 117)
lbl(x + 42, cy + 108, "transmitter")

x, cy = row1[1]
card(x, cy, "Bluetooth", "Game console", ["A", "B", "Home"])
gamepad(x + 20, cy + 104)
bt_rune(x + 115, cy + 125, 0.9)
console(x + 132, cy + 104)

x, cy = row1[2]
card(x, cy, "Network remote", "TV", ["OK", "Home", "Back"])
wifi(x + 52, cy + 150)
tv(x + 100, cy + 82, 110, 72)

x, cy = row1[3]
card(x, cy, "USB", "Phone", ["Tap", "Swipe", "Back"])
phone(x + 140, cy + 72)
o.append(f'<path d="M{x+168} {cy+172}V{cy+180}Q{x+168} {cy+186} {x+160} {cy+186}H{x+62}" fill="none" stroke="{MUT}" stroke-width="3"/>')
box(x + 30, cy + 174, 34, 24, "#333", MUT, 5, 2)
lbl(x + 72, cy + 120, "by cable")

x, cy = row2[0]
card(x, cy, "Serial", "Modem", ["Send digits"])
modem(x + 120, cy + 120)
o.append(f'<path d="M{x+120} {cy+140}H{x+52}" stroke="{MUT}" stroke-width="3" stroke-dasharray="6 5"/>')
box(x + 26, cy + 128, 30, 24, "#333", MUT, 5, 2)
lbl(x + 70, cy + 116, "serial port")

x, cy = row2[1]
card(x, cy, "ADB", "TV box", ["OK", "Back"])
wifi(x + 62, cy + 150)
stb(x + 108, cy + 124)
lbl(x + 62, cy + 176, "network")

x, cy = row2[2]
card(x, cy, "Appium", "Phone", ["Tap", "Type", "Home"])
phone(x + 92, cy + 72)
o.append(f'<circle cx="{x+120}" cy="{cy+124}" r="14" fill="none" stroke="{GOLD}" stroke-width="3"/><circle cx="{x+120}" cy="{cy+124}" r="5" fill="{GOLD}"/>')

t(600, y + P2 - 24, "Each device gets the controller it really needs.", 22, GOLD, 700, "middle")
arrow(600, y + P2, y + P2 + 40)

# 3 a new controller is added once (CONTROLLER_CREATION_GUIDE: registry of all controllers)
y += P2 + 40
P3 = 340
layer(y, "3", "A new controller, added once", "Every test can use it", P3)
rx, ry = 100, y + 116
box(rx, ry, 640, 164, "#1b1b1b", LINE, 16)
t(rx + 22, ry + 34, "CONTROLLERS", 16, GOLD, 700, sp=2, room=300)
names = ["Infrared", "Bluetooth", "Network remote", "USB", "Serial", "ADB", "Appium"]
px, py = rx + 22, ry + 54
for nm in names + ["+ New"]:
    w = ImageFont.truetype(TTF[True], 17).getlength(nm) + 28
    if px + w > rx + 620:
        px, py = rx + 22, py + 46
    new = nm.startswith("+")
    box(px, py, w, 34, DARKG if new else "#333333", GOLD if new else "#444444", 17, 2 if new else 1.5, "6 5" if new else "")
    t(px + w / 2, py + 23, nm, 17, GOLD if new else TXT, 700, "middle", room=w)
    px += w + 10
# the tests that use it
for i in range(3):
    bx, by = 820, ry + i * 58
    box(bx, by, 290, 48, "#1b1b1b", LINE, 12)
    t(bx + 20, by + 31, "TEST", 15, GOLD, 700, sp=2, room=80)
    t(bx + 90, by + 32, "Press OK", 19, TXT, 600, room=180, fam=MONO)
    o.append(f'<path d="M{bx+246} {by+24}l7 7l13 -14" fill="none" stroke="#4ade80" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="M{rx+640} {ry+82}C{rx+680} {ry+82} {bx-40} {by+24} {bx} {by+24}" fill="none" stroke="{LINE}" stroke-width="3"/>')
t(600, y + P3 - 22, "It lives on the host: no test changes.", 19, MUT, 400, "middle")

# footer
y += P3
t(600, y + 56, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
Htot = y + 94
o.append("</svg>")
open("docs/img/remotes.svg", "w").write("\n".join(o).replace(H, str(Htot)))
print("docs/img/remotes.svg", Htot)
