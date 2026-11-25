#!/usr/bin/env python3
"""Writes docs/img/hosts-anywhere.svg (Docs poster: servers and hosts, anywhere; source: Learn lessons 0.1 and 0.2,
scripts/promo/concepts/SCRIPTS.md "0.2", docs/technical/architecture/architecture.md). Run from the repo root.

Fails when a text is wider than its room in DejaVu Sans (headless Chromium's fallback font)."""
from PIL import ImageFont

W = 1200
BG, PANEL, CHIP, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#2a2a2a", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
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


def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0, room=1060):
    fit(s, size, w >= 600, room)
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{s}</text>')


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
    t(156, y + 82, sub, 21, MUT, 400, room=960)


def link(x1, y1, x2, y2):
    """A host-to-server or server-to-frontend line: grey wire with gold dots, as in the lesson's pulses."""
    o.append(f'<path d="M{x1} {y1}C{x1} {(y1+y2)/2} {x2} {(y1+y2)/2} {x2} {y2}" fill="none" stroke="{LINE}" stroke-width="4"/>')
    for k in (0.3, 0.6):
        # point on the cubic at k (control points share x with their ends)
        mx = x1 + (x2 - x1) * (3 * k * k - 2 * k * k * k)
        my = y1 + (y2 - y1) * k
        o.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="6" fill="{GOLD}"/>')


def device_tv(x, y):
    o.append(f'<rect x="{x}" y="{y}" width="46" height="30" rx="4" fill="none" stroke="{MUT}" stroke-width="2.5"/><path d="M{x+15} {y+37}H{x+31}" stroke="{MUT}" stroke-width="2.5" stroke-linecap="round"/>')


def device_phone(x, y):
    o.append(f'<rect x="{x}" y="{y}" width="20" height="36" rx="4" fill="none" stroke="{MUT}" stroke-width="2.5"/>')


def host(x, y, label="host"):
    """A small host box (Pi / mini PC): gold outline, two LEDs."""
    box(x, y, 92, 44, "#2a2418", GOLD, 10, 2)
    t(x + 40, y + 29, label, 18, GOLD, 600, "middle", room=60)
    o.append(f'<circle cx="{x+76}" cy="{y+16}" r="3.5" fill="{GOLD}"/><circle cx="{x+76}" cy="{y+28}" r="3.5" fill="#4ade80"/>')


def site(x, y, w, name, n_hosts):
    """A site card with its hosts and devices; returns the top-centre point of each host."""
    box(x, y, w, 170, CHIP, LINE, 18)
    t(x + 20, y + 36, name, 22, TXT, 700, room=w - 120)
    t(x + w - 20, y + 36, f"{n_hosts} host" + ("s" if n_hosts > 1 else ""), 17, MUT, 400, "end", room=100)
    tops = []
    slot = w / n_hosts
    for i in range(n_hosts):
        hx = x + slot * i + slot / 2 - 72
        host(hx, y + 64)
        device_tv(hx + 104, y + 70)
        device_phone(hx + 112, y + 118) if n_hosts == 1 else device_phone(hx + 116, y + 118)
        o.append(f'<path d="M{hx+92} {y+86}H{hx+104}" stroke="{MUT}" stroke-width="2"/>')
        tops.append((hx + 46, y + 64))
    return tops


H = "@@H@@"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Servers and hosts, anywhere: nothing central, one frontend sees them all, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# header
t(60, 100, "INFRA ARCHITECTURE · DECENTRALIZED", 20, GOLD, 500, sp=3)
t(60, 180, "Servers and hosts, anywhere", 62, TXT, 700)
t(60, 236, "Nothing central: one frontend sees them all.", 29, MUT, 400)
t(60, 276, "Run a server in the cloud or on site, and put hosts wherever your devices are.", 22, MUT, 400)

# 1 three parts (lesson 0.1)
y = 330
layer(y, "1", "Frontend, server and host", "Click in a browser; the host by the device acts", 250)
chips(90, y + 112, [("Frontend", "where you click"), ("Server", "plans, keeps the results"), ("Host", "by your devices, acts")], 324, 21)
t(600, y + 222, "Only the host touches a device. It cannot sit in the cloud: it is wired to them.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

# 2 the map (lesson 0.2 card, same words and counts)
y = 640
PH = 820
layer(y, "2", "Nothing central", "Servers anywhere, hosts at any site, one frontend", PH)
# frontend card (a laptop screen with the server list)
fx, fy = 420, y + 120
box(fx, fy, 360, 214, "#f2f2f2", "#f2f2f2", 16)
t(fx + 24, fy + 38, "FRONTEND", 18, "#7a5a2e", 700, sp=2, room=200)
for i, (nm, on) in enumerate([("Server 1", False), ("Server 2", False), ("All servers", True)]):
    ry = fy + 56 + i * 46
    box(fx + 20, ry, 320, 38, GOLD if on else "#e4e4e4", GOLD if on else "#e4e4e4", 10, 0)
    t(fx + 40, ry + 26, nm, 19, "#1a1a1a", 700 if on else 500, room=280)
o.append(f'<path d="M{fx-20} {fy+222}H{fx+380}L{fx+356} {fy+236}H{fx+4}Z" fill="#cfcfcf"/>')
# servers
sy = y + 400
servers = [(170, "SERVER 1", "Cloud · 3 hosts"), (690, "SERVER 2", "On site · 1 host")]
for sx, a, b in servers:
    box(sx, sy, 340, 96, "#111111", LINE, 16)
    for k in range(3 if a.endswith("1") else 1):
        o.append(f'<rect x="{sx+22}" y="{sy+20+k*20}" width="48" height="14" rx="3" fill="#2a2a2a" stroke="{GOLD}" stroke-width="1.5"/>')
    t(sx + 92, sy + 42, a, 22, TXT, 700, sp=2, room=230)
    t(sx + 92, sy + 72, b, 19, MUT, 400, room=230)
# sites
ty = y + 600
mark = len(o)  # wires go under the site cards: they end at the card edge, not across the labels
lab = site(90, ty, 400, "Lab", 2)
office = site(510, ty, 290, "Office", 1)
home = site(820, ty, 290, "At home", 1)
cards_svg, o[mark:] = o[mark:], []
for hx, hy in lab + office:
    link(hx, ty, 340, sy + 96)
for hx, hy in home:
    link(hx, ty, 860, sy + 96)
o.extend(cards_svg)
for sx, _, _ in servers:
    link(sx + 170, sy, 600 + (sx - 430) * 0.25, fy + 236)
t(600, y + PH - 14, "4 hosts, one list", 22, GOLD, 700, "middle")
t(100, fy + 96, "each host joins one server,", 17, MUT, 400, room=300)
t(100, fy + 120, "a server sees", 17, MUT, 400, room=260)
t(100, fy + 144, "only its own hosts", 17, MUT, 400, room=260)
arrow(600, y + PH, y + PH + 50)

# 3 where hosts go
y = 640 + PH + 50
layer(y, "3", "A host goes where the devices are", "A small computer, plugged into your TVs, boxes and phones", 250)
chips(90, y + 112, [("Raspberry Pi", "a small board"), ("Mini PC", "any Linux PC"), ("Mac", "works too"), ("Windows", "works too")], 240, 18)
t(600, y + 222, "Remote, USB and HDMI capture all plug into the host, not the server.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

# 4 heavy work
y += 310
layer(y, "4", "Each host does the heavy work", "Next to its own devices, day and night", 250)
chips(90, y + 112, [("Capture", "video + audio"), ("Watch 24/7", "black · freeze · audio"), ("Record 24 h", "rewind any moment"), ("Scheduled tests", "run on the host")], 240, 18)
t(600, y + 222, "One more host is more power: each one works for its own devices.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

# 5 joining
y += 310
layer(y, "5", "A host joins one server", "Set it up once, it calls its server", 250)
chips(90, y + 112, [("Plug in", "next to the devices"), ("Point it", "at one server"), ("Registers", "host calls out, HTTPS"), ("Checks in", "every 30 s")], 240, 18)
t(600, y + 222, "Each host joins one server. One server can have many hosts.", 19, MUT, 400, "middle")
arrow(600, y + 250, y + 300)

# 6 add a site
y += 310
layer(y, "6", "A new site is one more host", "Plug a host in there and point it at a server", 290)
cards = [(90, "Lab", False), (350, "Office", False), (610, "At home", False), (870, "+ New site", True)]
for cx, nm, new in cards:
    box(cx, y + 112, 240, 110, "#2a2418" if new else CHIP, GOLD if new else LINE, 16, 2, "10 8" if new else "")
    t(cx + 120, y + 146, nm, 22, GOLD if new else TXT, 700, "middle", room=220)
    host(cx + 74, y + 162)
t(600, y + 262, "Nothing changes on the other sites, and the frontend lists the new host.", 19, MUT, 400, "middle")

# band + footer
y += 340
box(60, y, 1080, 120, "#2a2418", GOLD, 22, 2)
t(600, y + 50, "One frontend sees them all", 32, GOLD, 700, "middle")
t(600, y + 90, "Pick one server, or All servers to see every host in one list.", 21, TXT, 400, "middle")
t(600, y + 172, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
Htot = y + 210
o.append("</svg>")
open("docs/img/hosts-anywhere.svg", "w").write("\n".join(o).replace(H, str(Htot)))
print("docs/img/hosts-anywhere.svg", Htot)
