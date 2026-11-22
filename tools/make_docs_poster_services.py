#!/usr/bin/env python3
"""Writes docs/img/services.svg (Docs poster: every platform service, grouped in server and host; source docs/agent/platform/SERVICES.md of the product repo). Run from the repo root."""
W, H = 1200, 2110
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
def rows(y0, groups):
    """groups: [(label, [(name, caption)x<=4])] -> next y"""
    y = y0
    for lab, items in groups:
        label(y, lab)
        chips(90, y + 12, items, 240, 18, 66)
        y += 112
    return y
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Services are background jobs: every VirtualPyTest service, grouped in server and host, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
t(60, 100, "INFRA ARCHITECTURE · SERVICES", 20, GOLD, 500, sp=3)
t(60, 180, "Services are background jobs", 62, TXT, 700)
t(60, 236, "Stream, watch, record, measure: each is its own job.", 29, MUT, 400)
t(60, 276, "Every one is named vpt-something and shown on the Status page.", 24, MUT, 400)

# server
y = 330
layer(y, "1", "Backend server", "One per server. The web app talks to it", 420)
rows(y + 130, [("ALWAYS ON", [("Server API", "the web app's backend"), ("Discard Incident", "sets harmless alerts aside"), ("Discard Scripts", "reads failed runs"), ("Heatmap", "the 24 h picture")]),
                ("IN THE BACKGROUND", [("Match runs", "the Localize history"), ("Unknown screens", "names new screens, hourly"), ("Freeze retrain", "learns every night"), ("Fleet health", "live and daily report")])])
t(600, y + 392, "A server box can also be a host: it runs both lists.", 19, MUT, 400, "middle")
arrow(600, y + 420, y + 470)

# host
y = 800
layer(y, "2", "Device host", "One next to your devices, in the lab or anywhere", 670)
rows(y + 130, [("CORE", [("Host API", "devices, remotes, actions"), ("Stream", "captures each device"), ("Archiver", "RAM to disk"), ("Timeline", "thumbnail strips")]),
                ("WATCH", [("Monitor image", "freeze, black, no signal"), ("Monitor audio", "sound and transcript"), ("AV quality", "picture and sound scores"), ("KPI", "times of actions")]),
                ("DRIVE", [("BLE remote", "one per Bluetooth link"), ("Emulator", "Android on a screen"), ("VNC", "a remote desktop"), ("Media server", "local video relay")]),
                ("WHERE USED", [("Subtitles", "optional"), ("Companion", "live-TV second screen"), ("Local model", "optional, one host"), ("Localize bench", "scheduled check")])])
t(600, y + 642, "Each host runs the ones it needs. The names are the same everywhere.", 19, MUT, 400, "middle")
arrow(600, y + 670, y + 720)

# dashboard
y = 1520
layer(y, "3", "Seen on the Status page", "Every service is declared there, so a stopped one shows", 330)
chips(90, y + 112, [("Always on", "green while running"), ("Timer", "idle between runs is fine"), ("Per device", "N of M running"), ("Not installed", "optional and absent")], 240, 18)
t(600, y + 222, "A scheduled job is red only when its last run failed.", 19, MUT, 400, "middle")
t(600, y + 262, "Deploys restart only the server, the host and the stream.", 19, MUT, 400, "middle")
t(600, y + 292, "The other services need a restart by hand after a change.", 19, MUT, 400, "middle")

box(60, 1900, 1080, 120, "#2a2418", GOLD, 22, 2)
t(600, 1950, "Named vpt-something. Shown on the Status page.", 32, GOLD, 700, "middle")
t(600, 1990, "A stopped service is seen at once, not found by a failed test.", 21, TXT, 400, "middle")
t(600, 2070, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
o.append('</svg>')
open("docs/img/services.svg", "w").write("\n".join(o))
