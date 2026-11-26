#!/usr/bin/env python3
"""Writes docs/img/watched.svg (Docs poster: what a host does all day, even with no test running: the Stream captures
the picture and sound once, and the watcher services read that same copy side by side).
Sources: Learn 6.1 "Your devices, watched 24/7" and its Go deeper, Learn 0.3 / 0.4, and the product docs
docs/agent/platform/SERVICES.md, backend_host/scripts/run_ffmpeg.md, docs/agent/devices/MONITOR_PROFILES.md.
Service names are spelled as in the `services` poster. Fails when a text is wider than its room in DejaVu Sans
(headless Chromium's fallback font). Run from the repo root."""
import os
from PIL import ImageFont

W = 1200
BG, PANEL, CHIP, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#2a2a2a", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
RED, GREEN = "#ef5350", "#4ade80"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
TTF = {True: "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", False: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"}
o = []


def fit(s, size, bold, room):
    if room and os.path.exists(TTF[bold]):
        n = ImageFont.truetype(TTF[bold], size).getlength(s.replace("&amp;", "&"))
        if n > room:
            raise SystemExit(f"too wide ({n:.0f} > {room}): {s}")


def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0, room=None):
    fit(s, size, w >= 600, room)
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{s}</text>')


def box(x, y, w, h, fill=PANEL, stroke=LINE, r=22, sw=2, extra=""):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def line(x1, y1, x2, y2, c=GOLD, sw=3, extra=""):
    o.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" fill="none" {extra}/>')


def arrow(x, y1, y2):
    o.append(f'<path d="M{x} {y1}V{y2-12}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x-12} {y2-18}L{x} {y2-4}L{x+12} {y2-18}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')


def harrow(x1, x2, y, c=GOLD, sw=3):
    o.append(f'<path d="M{x1} {y}H{x2-8}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/><path d="M{x2-14} {y-8}L{x2-2} {y}L{x2-14} {y+8}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


def layer(y, n, title, sub, h):
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, title, 34, TXT, 700, room=960)
    t(156, y + 82, sub, 21, MUT, 400, room=960)


def screen(x, y, w, h, kind="scene", r=6):
    """A drawn generic screen: scene (sky, sun, hills), black, bars (no signal), menu, subtitle."""
    cid = f"c{len(o)}"
    o.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>')
    o.append(f'<g clip-path="url(#{cid})">')
    if kind in ("scene", "subtitle"):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#35577a"/>')
        o.append(f'<circle cx="{x+w*0.74}" cy="{y+h*0.3}" r="{h*0.13}" fill="{GOLD}"/>')
        o.append(f'<path d="M{x} {y+h*0.78}Q{x+w*0.25} {y+h*0.45} {x+w*0.5} {y+h*0.72}T{x+w} {y+h*0.6}V{y+h}H{x}Z" fill="#3f6b4a"/>')
        o.append(f'<path d="M{x} {y+h*0.9}Q{x+w*0.4} {y+h*0.68} {x+w} {y+h*0.88}V{y+h}H{x}Z" fill="#2f5238"/>')
        if kind == "subtitle":
            o.append(f'<rect x="{x+w*0.14}" y="{y+h*0.74}" width="{w*0.72}" height="{h*0.17}" rx="3" fill="#000" fill-opacity="0.65"/>')
    elif kind == "black":
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#000"/>')
    elif kind == "bars":
        cols = ["#c0c0c0", "#c0c000", "#00c0c0", "#00c000", "#c000c0", "#c00000", "#0000c0"]
        bw = w / len(cols)
        for i, c in enumerate(cols):
            o.append(f'<rect x="{x+i*bw}" y="{y}" width="{bw+0.5}" height="{h}" fill="{c}"/>')
    elif kind == "menu":
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#26303b"/>')
        for i in range(4):
            fx = x + w * 0.08 + i * w * 0.225
            o.append(f'<rect x="{fx}" y="{y+h*0.35}" width="{w*0.19}" height="{h*0.4}" rx="3" fill="{GOLD if i == 0 else "#4b5866"}"/>')
        o.append(f'<rect x="{x+w*0.08}" y="{y+h*0.12}" width="{w*0.35}" height="{h*0.1}" rx="2" fill="#8a96a3"/>')
    o.append('</g>')
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" stroke="#555" stroke-width="2"/>')


def wave(x, y, w, amp, n=24, c=GOLD, flat_from=None):
    """A sound wave as vertical bars, flat (silent) from bar index flat_from on."""
    step = w / n
    for i in range(n):
        a = amp * (0.35 + 0.65 * abs(((i * 7) % 11) / 10 - 0.5) * 2) if flat_from is None or i < flat_from else 1.5
        col = c if flat_from is None or i < flat_from else RED
        o.append(f'<rect x="{x+i*step+step*0.2:.1f}" y="{y-a:.1f}" width="{step*0.6:.1f}" height="{2*a:.1f}" rx="1.5" fill="{col}"/>')


H_PLACE = "@@H@@"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H_PLACE}" width="{W}" height="{H_PLACE}" role="img" aria-labelledby="ti"><title id="ti">Your devices, watched 24/7: the host captures the picture and sound once, and several services read that same copy, each catching a different problem</title>')
o.append(f'<rect width="{W}" height="{H_PLACE}" fill="{BG}"/>')
t(60, 100, "MONITOR 24/7 · WHAT A HOST DOES ALL DAY", 20, GOLD, 500, sp=3, room=1080)
t(60, 180, "Your devices, watched 24/7", 62, TXT, 700, room=1080)
t(60, 236, "The video is captured once. Many watchers read it.", 29, MUT, 400, room=1080)
t(60, 276, "Each one catches a different problem, even when no test runs.", 24, MUT, 400, room=1080)

# 1 · captured once
y = 330
layer(y, "1", "Captured once", "The Stream service records the picture and the sound, day and night", 430)
# device
screen(100, y + 140, 230, 140, "scene")
o.append(f'<rect x="195" y="{y+280}" width="40" height="14" fill="#444"/><rect x="165" y="{y+294}" width="100" height="8" rx="4" fill="#444"/>')
t(215, y + 336, "Your device", 20, TXT, 600, "middle", room=230)
t(215, y + 362, "TV box, phone, PC", 16, MUT, 400, "middle", room=230)
# cable
o.append(f'<path d="M330 {y+210}C370 {y+210} 380 {y+210} 420 {y+210}" stroke="{MUT}" stroke-width="5" fill="none" stroke-linecap="round"/>')
t(375, y + 196, "picture", 14, MUT, 400, "middle")
t(375, y + 236, "+ sound", 14, MUT, 400, "middle")
# host
box(420, y + 130, 230, 170, fill=CHIP, r=18)
t(535, y + 166, "Host", 22, TXT, 700, "middle")
for i in range(3):
    o.append(f'<circle cx="{450+i*16}" cy="{y+284}" r="4" fill="{GREEN if i == 0 else "#555"}"/>')
box(450, y + 186, 170, 70, fill="#2f2a22", stroke=GOLD, r=14)
t(535, y + 218, "Stream", 22, GOLD, 700, "middle", room=150)
t(535, y + 242, "always on", 15, MUT, 400, "middle", room=150)
t(535, y + 336, "Next to your device", 16, MUT, 400, "middle", room=230)
# outputs
harrow(650, 700, y + 215)
ox = 720
# filmstrip
o.append(f'<rect x="{ox}" y="{y+128}" width="390" height="58" rx="6" fill="#0e0e0e"/>')
for i in range(6):
    screen(ox + 8 + i * 64, y + 136, 56, 42, "scene", r=3)
t(ox, y + 210, "Frames, 5 a second", 18, TXT, 600, room=390)
wave(ox, y + 252, 390, 18, n=40)
t(ox, y + 296, "Sound", 18, TXT, 600, room=390)
for i in range(6):
    box(ox + i * 66, y + 312, 58, 26, fill="#2f2a22", stroke=GOLD, r=6, sw=1.5)
t(ox, y + 362, "Short video pieces", 18, TXT, 600, room=390)
t(600, y + 406, "One copy, made once. Every watcher below reads this same copy.", 19, MUT, 400, "middle", room=1020)
arrow(600, y + 430, y + 480)

# 2 · many watchers
y = 810
P2H = 1080
layer(y, "2", "Many watchers read it", "Side by side, each one looks for a different problem", P2H)
# the copy, at the top, fanning out to the cards
box(420, y + 116, 360, 58, fill="#0e0e0e", stroke=GOLD, r=10)
for i in range(5):
    screen(430 + i * 69, y + 124, 62, 42, "scene", r=3)
CW, CH, GAP = 320, 360, 30
cx0 = [90 + i * (CW + GAP) for i in range(3)]
rows_y = [y + 250, y + 250 + CH + 26]
for cx in cx0:
    o.append(f'<path d="M600 {y+174}C600 {y+212} {cx+CW/2} {y+208} {cx+CW/2} {y+246}" stroke="{GOLD}" stroke-width="2.5" fill="none" stroke-dasharray="6 6"/>')

cards = [
    ("Monitor image", "A bad picture", ["Checks every frame,", "5 a second"]),
    ("Monitor audio", "Lost sound", ["Checks the sound every 5 s.", "Can also write down speech"]),
    ("Subtitles", "The words on screen", ["Reads them only while", "live video plays"]),
    ("KPI", "A slow screen", ["Times the key press to", "the right screen"]),
    ("Timeline", "When it went wrong", ["Small pictures of the", "last 24 hours"]),
    ("Archiver", "The proof, kept", ["The last 24 hours of video,", "saved from RAM to disk"]),
]
for k, (name, catch, grey) in enumerate(cards):
    cx, cy = cx0[k % 3], rows_y[k // 3]
    box(cx, cy, CW, CH, fill=CHIP, r=18)
    t(cx + 22, cy + 40, name, 24, TXT, 700, room=CW - 44)
    dx, dy = cx + 20, cy + 62  # drawing area 280 x 150
    o.append(f'<rect x="{dx}" y="{dy}" width="280" height="150" rx="10" fill="#1b1b1b"/>')
    if k == 0:   # black, frozen, no signal
        for j, (kind, lab) in enumerate([("black", "black"), ("scene", "frozen"), ("bars", "no signal")]):
            sx = dx + 12 + j * 90
            screen(sx, dy + 30, 76, 50, kind, r=4)
            if kind == "scene":
                o.append(f'<rect x="{sx+29}" y="{dy+43}" width="7" height="24" rx="2" fill="#fff"/><rect x="{sx+40}" y="{dy+43}" width="7" height="24" rx="2" fill="#fff"/>')
            o.append(f'<rect x="{sx-3}" y="{dy+27}" width="82" height="56" rx="6" fill="none" stroke="{RED}" stroke-width="2.5"/>')
            t(sx + 38, dy + 112, lab, 16, TXT, 600, "middle", room=88)
    elif k == 1:   # sound, then silence
        wave(dx + 14, dy + 66, 252, 30, n=26, flat_from=15)
        o.append(f'<line x1="{dx+14+252*15/26}" y1="{dy+22}" x2="{dx+14+252*15/26}" y2="{dy+108}" stroke="{RED}" stroke-width="2" stroke-dasharray="4 4"/>')
        t(dx + 214, dy + 46, "silent", 16, RED, 600, "middle")
        box(dx + 14, dy + 112, 252, 30, fill="#262626", stroke=LINE, r=8, sw=1.5)
        t(dx + 140, dy + 133, "“Good evening, and welcome”", 15, MUT, 400, "middle", room=240)
    elif k == 2:   # subtitle read off the screen
        screen(dx + 14, dy + 14, 200, 122, "subtitle", r=6)
        t(dx + 114, dy + 120, "See you tomorrow", 13, "#fff", 600, "middle", room=140)
        o.append(f'<rect x="{dx+38}" y="{dy+101}" width="152" height="29" rx="4" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="5 4"/>')
        harrow(dx + 218, dx + 246, dy + 115, GOLD, 2.5)
        t(dx + 262, dy + 110, "Aa", 20, GOLD, 700, "middle")
        t(dx + 262, dy + 130, "text", 13, MUT, 400, "middle")
    elif k == 3:   # key press, stopwatch, screen
        o.append(f'<rect x="{dx+18}" y="{dy+30}" width="56" height="92" rx="16" fill="#333" stroke="#555" stroke-width="2"/>')
        o.append(f'<circle cx="{dx+46}" cy="{dy+62}" r="15" fill="{GOLD}"/>')
        t(dx + 46, dy + 67, "OK", 13, "#1a1a1a", 700, "middle")
        for j in range(3):
            o.append(f'<circle cx="{dx+34+j*12}" cy="{dy+100}" r="3.5" fill="#666"/>')
        o.append(f'<path d="M{dx+82} {dy+76}H{dx+170}" stroke="{GOLD}" stroke-width="2.5" stroke-dasharray="5 5"/>')
        o.append(f'<circle cx="{dx+126}" cy="{dy+76}" r="22" fill="#1b1b1b" stroke="{GOLD}" stroke-width="3"/><rect x="{dx+121}" y="{dy+46}" width="10" height="6" rx="2" fill="{GOLD}"/><path d="M{dx+126} {dy+76}L{dx+126} {dy+62}M{dx+126} {dy+76}L{dx+136} {dy+82}" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>')
        harrow(dx + 152, dx + 178, dy + 76, GOLD, 2.5)
        screen(dx + 180, dy + 40, 88, 72, "menu", r=5)
        t(dx + 46, dy + 140, "key press", 13, MUT, 400, "middle")
        t(dx + 224, dy + 140, "screen shown", 13, MUT, 400, "middle")
    elif k == 4:   # thumbnails across the day, one black one outlined
        hours = ["00 h", "03 h", "06 h", "09 h"]
        for j in range(8):
            sx = dx + 12 + j * 33
            kind = "black" if j == 2 else ("menu" if j in (5, 6) else "scene")
            screen(sx, dy + 40, 30, 40, kind, r=3)
        o.append(f'<rect x="{dx+75}" y="{dy+35}" width="40" height="50" rx="5" fill="none" stroke="{RED}" stroke-width="2.5"/>')
        o.append(f'<line x1="{dx+12}" y1="{dy+98}" x2="{dx+273}" y2="{dy+98}" stroke="#555" stroke-width="2"/>')
        for j, hlab in enumerate(hours):
            hx = dx + 12 + j * 66 + 15
            o.append(f'<line x1="{hx}" y1="{dy+94}" x2="{hx}" y2="{dy+102}" stroke="#555" stroke-width="2"/>')
            t(hx, dy + 120, hlab, 13, MUT, 400, "middle")
        t(dx + 95, dy + 26, "3 a.m.", 14, RED, 600, "middle")
    elif k == 5:   # minutes into the 24 h store
        for j in range(5):
            box(dx + 14, dy + 22 + j * 22, 60, 16, fill="#2f2a22", stroke=GOLD, r=4, sw=1.5)
        t(dx + 44, dy + 140, "RAM", 13, MUT, 400, "middle")
        harrow(dx + 84, dx + 124, dy + 72, GOLD, 2.5)
        # disk with a 24 h ring
        o.append(f'<circle cx="{dx+196}" cy="{dy+70}" r="48" fill="#262626" stroke="#555" stroke-width="2"/>')
        o.append(f'<circle cx="{dx+196}" cy="{dy+70}" r="38" fill="none" stroke="{GOLD}" stroke-width="7" stroke-dasharray="200 39" transform="rotate(-90 {dx+196} {dy+70})"/>')
        t(dx + 196, dy + 78, "24 h", 20, TXT, 700, "middle")
        t(dx + 196, dy + 140, "disk", 13, MUT, 400, "middle")
    t(cx + 22, cy + 250, "Catches", 14, GOLD, 600, sp=2)
    t(cx + 22, cy + 278, catch, 21, TXT, 700, room=CW - 44)
    t(cx + 22, cy + 310, grey[0], 17, MUT, 400, room=CW - 44)
    t(cx + 22, cy + 334, grey[1], 17, MUT, 400, room=CW - 44)
t(600, y + P2H - 40, "None of them presses a key: the device is only watched.", 19, MUT, 400, "middle", room=1020)
arrow(600, y + P2H, y + P2H + 50)

# 3 · a problem that lasts
y = 810 + P2H + 50
layer(y, "3", "A problem that lasts becomes an incident", "Even at 3 a.m., with no test running", 380)
bx, by, bw = 100, y + 160, 640
# good frames, then black for 30 s
o.append(f'<rect x="{bx}" y="{by}" width="250" height="44" rx="8" fill="#2f5238"/>')
o.append(f'<rect x="{bx+250}" y="{by}" width="{bw-250}" height="44" rx="8" fill="#000" stroke="{RED}" stroke-width="2.5"/>')
t(bx + 125, by + 29, "picture OK", 18, TXT, 600, "middle", room=230)
t(bx + 250 + (bw - 250) / 2, by + 29, "black screen", 18, TXT, 600, "middle", room=360)
o.append(f'<path d="M{bx+250} {by+62}V{by+74}H{bx+bw}V{by+62}" stroke="{GOLD}" stroke-width="2.5" fill="none"/>')
t(bx + 250 + (bw - 250) / 2, by + 100, "lasts 30 seconds", 18, GOLD, 600, "middle", room=360)
harrow(bx + bw + 14, bx + bw + 64, by + 22)
# incident card
ix = 820
box(ix, y + 120, 290, 180, fill=CHIP, stroke=RED, r=16)
o.append(f'<circle cx="{ix+28}" cy="{y+150}" r="9" fill="{RED}"/>')
t(ix + 46, y + 157, "Incident", 20, TXT, 700, room=220)
screen(ix + 22, y + 176, 110, 66, "black", r=5)
t(ix + 146, y + 200, "black screen", 16, TXT, 600, room=130)
t(ix + 146, y + 224, "with its picture", 15, MUT, 400, room=130)
t(ix + 22, y + 278, "Closed when the picture is back", 15, MUT, 400, room=250)
t(600, y + 318, "The same for a frozen picture or lost sound.", 19, MUT, 400, "middle", room=1020)
t(600, y + 350, "A short black between two channels is not an incident: it is timed as a zap.", 19, MUT, 400, "middle", room=1020)
arrow(600, y + 380, y + 430)

# 4 · a profile chooses the watchers
y = y + 430
P4H = 470
layer(y, "4", "A profile is a set of services", "Each device turns on only the services it needs", P4H)
cols = ["Monitor image", "Monitor audio", "Subtitles", "KPI", "Archiver"]
devs = [("TV app", "a TV box", [1, 1, 1, 1, 1]), ("Phone", "a phone", [1, 0, 0, 1, 1]),
        ("Desktop KPI", "a PC, timed", [0, 0, 0, 1, 0]), ("Light", "stream and drive", [0, 0, 0, 0, 0])]
x0, cwid = 330, 156
for i, c in enumerate(cols):
    t(x0 + i * cwid + cwid // 2, y + 136, c, 17, TXT, 600, "middle", room=cwid - 6)
for r, (nm, cap, flags) in enumerate(devs):
    ry = y + 156 + r * 58
    o.append(f'<line x1="90" y1="{ry+58}" x2="1110" y2="{ry+58}" stroke="{LINE}" stroke-width="1"/>')
    t(100, ry + 28, nm, 21, TXT, 600, room=220)
    t(100, ry + 49, cap, 15, MUT, 400, room=220)
    for i, f in enumerate(flags):
        o.append(f'<circle cx="{x0 + i*cwid + cwid//2}" cy="{ry+30}" r="12" fill="{GOLD if f else "#3a3a3a"}"/>')
t(600, y + 418, "The Stream always runs. Gold is on, grey is off: the rest stays idle.", 19, MUT, 400, "middle", room=1020)
t(600, y + 448, "Switch off what nobody reads, and the host gets its CPU back.", 19, MUT, 400, "middle", room=1020)

# gold band
y = y + P4H + 40
box(60, y, 1080, 120, fill="#2f2a22", stroke=GOLD, r=22)
t(600, y + 54, "Captured once. Read by many.", 32, GOLD, 700, "middle", room=1020)
t(600, y + 92, "Each watcher catches a different problem.", 22, TXT, 400, "middle", room=1020)

H = y + 120 + 80
t(600, H - 30, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
o.append('</svg>')
open("docs/img/watched.svg", "w").write("\n".join(o).replace(H_PLACE, str(H)))
print("docs/img/watched.svg", W, H)
