#!/usr/bin/env python3
"""Writes docs/img/standalone.svg (Docs poster: the whole platform on one machine, a Raspberry Pi 5 or one VM / PC).
Sources: product docs get-started/raspberry-pi-standalone.md, hardware.md (section 1, sizing), docker.md,
proxmox.md section "One VM"; Learn lesson 0.5 (learn/cards/install-anywhere.html). Drawings reused from
tools/make_docs_poster_install_anywhere.py panels 1 and 2. Run from the repo root.

Fails when a text is wider than its room in DejaVu Sans (headless Chromium's fallback font)."""
from PIL import ImageFont

W = 1200
BG, PANEL, CHIP, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#2a2a2a", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
WARM = "#2a2418"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,DejaVu Sans Mono,monospace"
TTF = {(True, False): "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
       (False, False): "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
       (True, True): "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
       (False, True): "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"}
o = []


def fit(s, size, bold, room, mono=False):
    try:
        font = ImageFont.truetype(TTF[(bold, mono)], size)
    except OSError:
        return
    plain = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    if font.getlength(plain) > room:
        raise SystemExit(f"too wide ({font.getlength(plain):.0f} > {room}): {plain}")


def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0, room=1060, mono=False):
    fit(s, size, w >= 600, room, mono)
    fam = MONO if mono else F
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


def wire(x1, y1, x2, y2, color=MUT, sw=2.5, dash=""):
    m = (x1 + x2) / 2
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o.append(f'<path d="M{x1} {y1}C{m} {y1} {m} {y2} {x2} {y2}" fill="none" stroke="{color}" stroke-width="{sw}"{d}/>')


def device_tv(x, y):
    o.append(f'<rect x="{x}" y="{y}" width="46" height="30" rx="4" fill="none" stroke="{MUT}" stroke-width="2.5"/><path d="M{x+15} {y+37}H{x+31}" stroke="{MUT}" stroke-width="2.5" stroke-linecap="round"/>')


def device_phone(x, y):
    o.append(f'<rect x="{x}" y="{y}" width="20" height="36" rx="4" fill="none" stroke="{MUT}" stroke-width="2.5"/>')


def capture_card(x, y):
    """The small HDMI to USB stick: a body and a plug."""
    o.append(f'<rect x="{x}" y="{y}" width="58" height="22" rx="5" fill="{CHIP}" stroke="{GOLD}" stroke-width="2"/><rect x="{x+58}" y="{y+6}" width="10" height="10" rx="2" fill="{GOLD}"/>')


def terminal(x, y, w, h, label, lines):
    box(x, y, w, h, "#111111", LINE, 14, 2)
    o.append(f'<path d="M{x} {y+36}H{x+w}" stroke="{LINE}" stroke-width="2"/>')
    for k, c in enumerate(["#e06d6d", GOLD, "#4ade80"]):
        o.append(f'<circle cx="{x+22+k*18}" cy="{y+18}" r="5.5" fill="{c}"/>')
    t(x + 84, y + 25, label, 17, TXT, 700, room=w - 100)
    for i, ln in enumerate(lines):
        t(x + 20, y + 72 + i * 32, ln, 16, GOLD if i == len(lines) - 1 else TXT, 400, room=w - 36, mono=True)


H = "@@H@@"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Everything on one machine: the whole platform on one Raspberry Pi 5 or one VM, what to plug in and how to install it</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# header: eyebrow = doc name, title = proxmox.md "One VM: everything on one machine" (docker.md "one machine")
t(60, 90, "RASPBERRY PI STANDALONE", 20, GOLD, 500, sp=3)
t(60, 166, "Everything on one machine", 62, TXT, 700)
t(60, 220, "One Raspberry Pi 5 on a desk, or one VM or PC.", 29, MUT, 400)

# 1 what runs on it (raspberry-pi-standalone.md "What runs on it", the doc's parts and jobs)
y = 270
P1 = 258
GAP = 36
layer(y, "1", "What runs on it", "The whole platform, on one board or one machine", P1)
parts = [("Frontend", "The web app"), ("Server", "API, schedules, results"), ("Host", "Drives the devices"),
         ("Database", "Keeps the data"), ("Storage", "Files and queues"), ("Grafana", "Dashboards. Optional")]
CW, CG = 328, 18
for i, (a, b) in enumerate(parts):
    cx, cy = 90 + (i % 3) * (CW + CG), y + 104 + (i // 3) * 76
    box(cx, cy, CW, 64, CHIP, GOLD if a == "Host" else LINE, 16, 2)
    t(cx + 22, cy + 28, a, 22, GOLD if a == "Host" else TXT, 700, room=CW - 36)
    t(cx + 22, cy + 52, b, 17, MUT, 400, room=CW - 36)
arrow(600, y + P1, y + P1 + GAP)

# 2 one Raspberry Pi 5 (raspberry-pi-standalone.md "The board", hardware.md section 1)
y += P1 + GAP
P2 = 486
layer(y, "2", "One Raspberry Pi 5", "For a home lab or a demo. Up to 4 devices.", P2)
bx, by, bw, bh = 100, y + 112, 380, 210
box(bx, by, bw, bh, WARM, GOLD, 16, 2)
for k in range(18):  # pin header along the top edge
    o.append(f'<circle cx="{bx+44+k*17}" cy="{by+14}" r="3" fill="{GOLD}" opacity="0.55"/>')
t(bx + 24, by + 54, "Raspberry Pi 5", 24, TXT, 700, room=230)
t(bx + bw - 24, by + 54, "16 GB", 24, GOLD, 700, "end", room=90)
# fan in its case
fx, fy = bx + 70, by + 130
o.append(f'<circle cx="{fx}" cy="{fy}" r="38" fill="none" stroke="{MUT}" stroke-width="2.5"/><circle cx="{fx}" cy="{fy}" r="7" fill="{MUT}"/>')
for k in range(4):
    o.append(f'<path d="M{fx} {fy}q14 -10 26 -4" fill="none" stroke="{MUT}" stroke-width="3" stroke-linecap="round" transform="rotate({k*90} {fx} {fy})"/>')
t(fx, by + bh - 14, "fan", 15, MUT, 400, "middle", room=80)
# microSD / NVMe disk
o.append(f'<path d="M{bx+156} {by+96}h54l14 14v58h-68z" fill="{CHIP}" stroke="{MUT}" stroke-width="2"/>')
t(bx + 190, by + 144, "128", 16, TXT, 700, "middle", room=60)
t(bx + 190, by + bh - 14, "disk", 15, MUT, 400, "middle", room=80)
# blue USB 3 ports and the Ethernet port on the right edge
for k in range(2):
    o.append(f'<rect x="{bx+bw-64}" y="{by+80+k*38}" width="44" height="28" rx="4" fill="#2b5fae" stroke="#5b8de0" stroke-width="1.5"/>')
t(bx + bw - 42, by + 166, "USB 3", 15, MUT, 400, "middle", room=70)
o.append(f'<rect x="{bx+bw-64}" y="{by+176}" width="44" height="22" rx="3" fill="{CHIP}" stroke="{MUT}" stroke-width="1.5"/>')
t(bx + bw - 76, by + 193, "LAN", 15, MUT, 400, "end", room=60)
# wired network
rx, ry = 560, y + 338
wire(bx + bw - 20, by + 187, rx, ry + 17)
box(rx, ry, 120, 34, CHIP, LINE, 10, 2)
t(rx + 60, ry + 23, "network", 16, TXT, 600, "middle", room=110)
t(rx + 134, ry + 23, "cable, not Wi-Fi", 16, MUT, 400, room=200)
# powered USB hub, then one capture card per device
hx, hy = 560, y + 180
wire(bx + bw - 20, by + 94, hx, hy + 32)
box(hx, hy, 130, 64, CHIP, LINE, 12, 2)
t(hx + 65, hy + 26, "USB hub", 18, TXT, 700, "middle", room=118)
t(hx + 65, hy + 46, "powered", 15, MUT, 400, "middle", room=118)
t(hx + 65, hy + 82, "for 2+ cards", 15, MUT, 400, "middle", room=130)
t(915, y + 124, "1 capture card per device", 18, MUT, 400, "middle", room=380)
for i in range(4):
    cy = y + 156 + i * 46
    wire(hx + 130, hy + 32, 770, cy)
    capture_card(770, cy - 11)
    o.append(f'<path d="M838 {cy}H884" stroke="{MUT}" stroke-width="2"/>')
    if i == 2:
        device_phone(896, cy - 18)
    else:
        device_tv(894, cy - 18)
t(966, y + 176, "HDMI", 15, MUT, 400, room=80)
chips(90, y + 392, [("16 GB", "8 GB = 1 device"), ("Up to 4", "devices"), ("128 GB", "microSD or NVMe"), ("~30 min", "to first test")], 240, 20)
arrow(600, y + P2, y + P2 + GAP)

# 3 one VM or PC (proxmox.md "One VM", hardware.md "One VM running everything", docker.md)
y += P2 + GAP
P3 = 336
layer(y, "3", "Or one VM or PC", "Debian 12 or Ubuntu 22.04 or newer. The same parts.", P3)
vx, vy, vw, vh = 90, y + 104, 1020, 180
box(vx, vy, vw, vh, CHIP, LINE, 16, 2)
o.append(f'<path d="M{vx} {vy+40}H{vx+vw}" stroke="{LINE}" stroke-width="2"/>')
for k, c in enumerate(["#e06d6d", GOLD, "#4ade80"]):
    o.append(f'<circle cx="{vx+26+k*20}" cy="{vy+20}" r="6" fill="{c}"/>')
t(vx + 96, vy + 27, "One VM", 18, TXT, 700, room=200)
rows = [("CPU", 4, 2, "4 cores", "+2 cores per capture card"),
        ("RAM", 8, 4, "8 GB", "+4 GB per capture card"),
        ("Disk", 0, 0, "60 GB", "")]
for r, (lab, n, extra, val, plus) in enumerate(rows):
    ry = vy + 56 + r * 40
    t(vx + 30, ry + 24, lab, 19, MUT, 600, room=80)
    x0 = vx + 120
    if n:
        step = 200 / n
        for k in range(n):
            o.append(f'<rect x="{x0+k*step:.1f}" y="{ry+4}" width="{step-6:.1f}" height="26" rx="4" fill="{GOLD}"/>')
        t(x0 + 216, ry + 24, val, 19, TXT, 700, room=100)
        for k in range(extra):
            o.append(f'<rect x="{x0+330+k*step:.1f}" y="{ry+4}" width="{step-6:.1f}" height="26" rx="4" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="5 4"/>')
        t(x0 + 330 + extra * step + 14, ry + 24, plus, 19, GOLD, 600, room=420)
    else:
        o.append(f'<rect x="{x0}" y="{ry+4}" width="194" height="26" rx="4" fill="{GOLD}"/>')
        t(x0 + 216, ry + 24, val, 19, TXT, 700, room=100)
t(600, y + P3 - 20, "On a VM, the hypervisor passes each USB capture card through.", 19, MUT, 400, "middle")
arrow(600, y + P3, y + P3 + GAP)

# 4 install (raspberry-pi-standalone.md "Install", proxmox.md "One VM")
y += P3 + GAP
P4 = 376
layer(y, "4", "Install in a few commands", "Then open http://&lt;address&gt;:5073 and add your devices.", P4)
TWD = 500
terminal(90, y + 104, TWD, 184, "Raspberry Pi: Docker",
         ["git clone .../virtualpytest.git", "cd virtualpytest", "./setup/docker/install_docker.sh", "./setup/docker/launch.sh"])
terminal(610, y + 104, TWD, 184, "One VM: one script",
         ["git clone .../virtualpytest.git", "cd virtualpytest", "sudo -v &amp;&amp; ./setup/local/linux/install_all.sh"])
t(90 + TWD / 2, y + 320, "The first build is slow", 20, TXT, 600, "middle", room=TWD)
t(90 + TWD / 2, y + 346, "images are built on the Pi", 18, MUT, 400, "middle", room=TWD)
t(610 + TWD / 2, y + 320, "Most of an hour", 20, TXT, 600, "middle", room=TWD)
t(610 + TWD / 2, y + 346, "safe to run again", 18, MUT, 400, "middle", room=TWD)

# gold band: when you outgrow it (raspberry-pi-standalone.md "Tips", last line)
y += P4 + 30
box(60, y, 1080, 96, WARM, GOLD, 22, 2)
t(600, y + 42, "Outgrow it? The Pi stays useful as a host next to the devices,", 22, GOLD, 700, "middle")
t(600, y + 74, "and the rest moves to a Proxmox node.", 22, GOLD, 700, "middle")

# footer
y += 96
t(600, y + 52, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
Htot = y + 84
o.append("</svg>")
open("docs/img/standalone.svg", "w").write("\n".join(o).replace(H, str(Htot)))
print("docs/img/standalone.svg", Htot)
