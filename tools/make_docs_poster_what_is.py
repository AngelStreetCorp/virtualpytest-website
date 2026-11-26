#!/usr/bin/env python3
"""Writes docs/img/what-is-virtualpytest.svg (the first Docs poster). Run from the repo root."""
W, H = 1200, 2480
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

o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">What is VirtualPyTest, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
# header
t(60, 100, "OPEN SOURCE · AI-NATIVE · ANY SCREEN", 20, GOLD, 500, sp=3)
t(60, 180, "What is VirtualPyTest?", 70, TXT, 700)
t(60, 236, "Any device with a screen, tested and monitored 24/7 by AI.", 29, MUT, 400)
t(60, 276, "Real remotes, HDMI capture and verification. No per-device licenses.", 24, MUT, 400)

# devices
y = 330
layer(y, "1", "Your devices", "Anything with a screen and a controller", 250)
chips(90, y + 112, [("Web", "browser"), ("Mobile", "Android, iOS"), ("Tablet", "touch"), ("TV &amp; set-top", "remote + HDMI"), ("Streams", "watched only")], 190, 17)
t(600, y + 222, "Cloud device farms work too, driven as ordinary devices.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

# control
y = 640
layer(y, "2", "Control", "Press the real keys, see the real screen", 250)
chips(90, y + 112, [("Remote", "IR · Bluetooth"), ("ADB / app", "phone control"), ("Browser", "web driver"), ("HDMI capture", "video + audio")], 240, 18)
t(600, y + 222, "Hosts run next to the devices, in the lab or anywhere.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

# map
y = 950
layer(y, "3", "Map the app once", "The user interface: screens become a reusable graph", 380)
# mini graph
nodes = [(250, y+170, "Home"), (470, y+150, "Live TV"), (470, y+250, "Settings"), (700, y+170, "Guide"), (930, y+150, "Player"), (930, y+260, "Info")]
edges = [(0,1),(0,2),(1,3),(3,4),(2,5),(4,5)]
for a, b in edges:
    o.append(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{LINE}" stroke-width="4"/>')
for x, yy, n in nodes:
    box(x - 70, yy - 28, 140, 56, "#2a2a2a", GOLD, 28, 2)
    t(x, yy + 8, n, 22, TXT, 600, "middle")
t(600, y + 350, "Change one screen, every test that uses it follows.", 21, MUT, 400, "middle")
arrow(600, y + 380, y + 430)

# understand
y = 1380
layer(y, "4", "Prove what is on screen", "Localize and fingerprint: check the screen, not just the click", 250)
chips(90, y + 112, [("Reference", "image + text"), ("Localize", "find the element"), ("Fingerprint", "is this screen X?"), ("A/V quality", "black · freeze · audio")], 240, 18)
t(600, y + 222, "Works in any language, on any resolution.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

# run
y = 1690
layer(y, "5", "Run and measure", "Scripts and campaigns, with KPIs on every run", 250)
chips(90, y + 112, [("No code", "visual builder"), ("Python", "full logic"), ("UI variables", "same screens, every build"), ("KPIs", "loading · zapping")], 240, 18)
t(600, y + 222, "Every run keeps the video, the steps and the diff.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

# watch
y = 2000
layer(y, "6", "Watch 24/7", "Monitoring that alerts the moment it breaks", 250)
chips(90, y + 112, [("Incidents", "caught live"), ("Heatmap", "where it hurts"), ("Timeline", "rewind 24 h"), ("Dashboards", "live screens"), ("Analytics", "Grafana you own")], 190, 17)
t(600, y + 222, "Hosts, devices and system health, all in one place.", 19, MUT, 400, "middle")

# AI side rail + footer
box(60, 2290, 1080, 120, "#2a2418", GOLD, 22, 2)
t(600, 2340, "AI drives it all", 32, GOLD, 700, "middle")
t(600, 2380, "A built-in MCP server lets any AI client inspect and control a real device.", 21, TXT, 400, "middle")
t(600, 2452, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
o.append('</svg>')
open("docs/img/what-is-virtualpytest.svg", "w").write("\n".join(o))
