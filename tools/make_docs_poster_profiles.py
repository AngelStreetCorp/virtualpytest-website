#!/usr/bin/env python3
"""Writes docs/img/profiles.svg (Docs poster: a profile is a set of services; source: the Learn lessons 0.3 and Go deeper Profiles). Run from the repo root."""
W, H = 1200, 2650
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

GREEN = "#4ade80"
def label(y, txt):
    t(90, y, txt, 17, GOLD, 600, sp=2)
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">A profile is a set of services: what a host runs for each device, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
t(60, 100, "INFRA ARCHITECTURE · PROFILES", 20, GOLD, 500, sp=3)
t(60, 180, "A profile is a set of services", 58, TXT, 700)
t(60, 236, "Each device turns on only the services it needs.", 29, MUT, 400)
t(60, 276, "Nothing else runs, so the host stays light.", 24, MUT, 400)

y = 330
layer(y, "1", "A host comes in three shapes", "Pick the one that fits the box", 250)
chips(90, y + 112, [("Full", "all services"), ("Lite", "one device, 1 GB board"), ("Runner", "web and API tests")], 320, 30)
t(600, y + 222, "The full host is the default.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

y = 640
layer(y, "2", "Each device has a profile", "The set of services that device needs", 250)
chips(90, y + 112, [("TV app", "all services"), ("Phone", "no sound, no subtitles"), ("Desktop", "the stream only"), ("Drone", "its own set")], 240, 18)
t(600, y + 222, "A TV box gets the TV profile and a phone the phone one, unless you choose.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

# matrix
y = 950
layer(y, "3", "What each profile runs", "Gold is on, grey is off", 560)
cols = ["TV app", "TV KPI", "Phone", "Desktop KPI", "Light"]
rowsd = [("Watch", [1,1,1,0,0]), ("Sound", [1,1,0,0,0]), ("Subtitles", [1,0,0,0,0]), ("Record 24 h", [1,1,1,0,0]), ("KPI scan", [1,1,1,1,0]), ("Picture quality", [1,0,1,0,0])]
x0, cw = 330, 160
for i, c in enumerate(cols):
    t(x0 + i * cw + cw // 2, y + 126, c, 20, TXT, 600, "middle")
for r, (nm, flags) in enumerate(rowsd):
    ry = y + 150 + r * 52
    t(100, ry + 36, nm, 22, TXT, 500)
    o.append(f'<line x1="90" y1="{ry+52}" x2="1110" y2="{ry+52}" stroke="{LINE}" stroke-width="1"/>')
    for i, f in enumerate(flags):
        o.append(f'<circle cx="{x0 + i*cw + cw//2}" cy="{ry+26}" r="12" fill="{GOLD if f else "#3a3a3a"}"/>')
t(600, y + 504, "Light: a device you only stream and drive. Desktop KPI keeps just the KPI scan.", 18, MUT, 400, "middle")
t(600, y + 534, "The stream is full for TV and phone, and lean for the light profiles.", 18, MUT, 400, "middle")
arrow(600, y + 560, y + 610)

y = 1570
layer(y, "4", "One setting per device", "Set it once, the host does the rest", 250)
chips(90, y + 112, [("Choose", "a profile per device"), ("Save", "the host config"), ("Applied", "services restart or stop"), ("Idle", "no device needs it")], 240, 18)
t(600, y + 222, "A service no device needs shows idle on the dashboard. That is not a failure.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

y = 1880
layer(y, "5", "Pay for what you run", "A real case: one small host, four devices", 310)
chips(90, y + 112, [("4 cores", "two TV boxes, two phones"), ("Every service", "ran for every device"), ("Load around 15", "on those 4 cores"), ("Subtitles", "about one core alone")], 240, 18)
t(600, y + 222, "Nobody read the subtitles. Switching off what nobody reads gives the CPU back.", 19, MUT, 400, "middle")
t(600, y + 262, "The three biggest costs: subtitle reading, picture quality filters,", 19, MUT, 400, "middle")
t(600, y + 292, "and the extra outputs of each stream.", 19, MUT, 400, "middle")
arrow(600, y + 310, y + 360)

y = 2250
layer(y, "6", "Keep what your tests read", "Switch off only what nobody reads", 290)
chips(90, y + 112, [("Zaps and KPI", "keep watch + KPI scan"), ("Subtitle tests", "keep the TV profile"), ("Phone you watch", "the light profile"), ("Black and freeze", "keep watch")], 240, 18)
t(600, y + 222, "A box that measures times keeps a full stream, because the KPI scan reads it.", 19, MUT, 400, "middle")
t(600, y + 262, "A device whose tests read subtitles keeps the full TV profile.", 19, MUT, 400, "middle")

t(600, 2610, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
o.append('</svg>')
open("docs/img/profiles.svg", "w").write("\n".join(o))
