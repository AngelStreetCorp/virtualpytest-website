#!/usr/bin/env python3
"""Writes docs/img/proxmox.svg (Docs poster "Production on Proxmox": the node, the network, every VM with its size, job,
services and ports, who talks to whom, the install order and the day-two rules). Source: product docs
get-started/prod-proxmox.md and proxmox.md, plus the values measured on our node. No IP address on the poster.
Run from the repo root.

Fails when a text is wider than its room in DejaVu Sans (headless Chromium's fallback font)."""
from PIL import ImageFont

W = 1200
BG, PANEL, CHIP, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#2a2a2a", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
WARM, NODE, GREEN = "#2a2418", "#1b1b1b", "#4ade80"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
TTF = {True: "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", False: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"}
o = []


def fit(s, size, bold, room):
    try:
        font = ImageFont.truetype(TTF[bold], size)
    except OSError:
        return
    plain = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    if font.getlength(plain) > room:
        raise SystemExit(f"too wide ({font.getlength(plain):.0f} > {room}): {plain}")


def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0, room=1060):
    fit(s, size, w >= 600, room)
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{s}</text>')


def box(x, y, w, h, fill=PANEL, stroke=LINE, r=22, sw=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def line(x1, y1, x2, y2, color=MUT, sw=2.5, dash="", head=True):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{sw}" fill="none"{d}/>')
    if head:
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - 11 * math.cos(a - 0.45), y2 - 11 * math.sin(a - 0.45))
        p2 = (x2 - 11 * math.cos(a + 0.45), y2 - 11 * math.sin(a + 0.45))
        o.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f}L{x2} {y2}L{p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


def arrow(x, y1, y2):
    o.append(f'<path d="M{x} {y1}V{y2-12}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x-12} {y2-18}L{x} {y2-4}L{x+12} {y2-18}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')


def layer(y, n, title, sub, h):
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, title, 34, TXT, 700, room=960)
    if sub:
        t(156, y + 82, sub, 21, MUT, 400, room=960)


def device_tv(x, y):
    o.append(f'<rect x="{x}" y="{y}" width="46" height="30" rx="4" fill="none" stroke="{MUT}" stroke-width="2.5"/><path d="M{x+15} {y+37}H{x+31}" stroke="{MUT}" stroke-width="2.5" stroke-linecap="round"/>')


def host_box(x, y, label="host"):
    box(x, y, 92, 44, WARM, GOLD, 10, 2)
    t(x + 40, y + 29, label, 18, GOLD, 600, "middle", room=60)
    o.append(f'<circle cx="{x+76}" cy="{y+16}" r="3.5" fill="{GOLD}"/><circle cx="{x+76}" cy="{y+28}" r="3.5" fill="{GREEN}"/>')


def pill(x, y, w, name, cap="", gold=False, h=None):
    h = h or (56 if cap else 40)
    box(x, y, w, h, WARM if gold else CHIP, GOLD if gold else LINE, 12, 2)
    if cap:
        t(x + w / 2, y + 24, name, 18, GOLD if gold else TXT, 700, "middle", room=w - 14)
        t(x + w / 2, y + 45, cap, 15, MUT, 400, "middle", room=w - 14)
    else:
        t(x + w / 2, y + 26, name, 18, GOLD if gold else TXT, 700, "middle", room=w - 14)


H = "@@H@@"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Production on Proxmox: one node, one VM per role, every VM with its size, job and ports, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# header
t(60, 80, "GET STARTED", 20, GOLD, 500, sp=3)
t(60, 152, "Production on Proxmox", 62, TXT, 700)
t(60, 204, "How our production runs: one node, one VM per role. Copy it.", 29, MUT, 400)

# 1 The node: ours and enough, drawn as two machines with their specs
G = 32
y = 254
P1 = 368
layer(y, "1", "The node", "One Proxmox machine holds every VM", P1)
specs = [("Ours", True, [("CPU", "AMD Ryzen 9 3900"), ("", "12 cores / 24 threads"), ("RAM", "128 GB"),
                         ("Disk", "2 x 1.9 TB NVMe"), ("Software", "Proxmox VE 9"), ("Backup", "Proxmox Backup Server")]),
         ("Enough for the same setup", False, [("CPU", "8 cores / 16 threads"), ("RAM", "64 GB"),
                                               ("Disk", "2 x 1 TB NVMe"), ("Software", "Proxmox VE 8 or 9"), ("Backup", "any off-site copy")])]
for k, (name, ours, rows) in enumerate(specs):
    mx, my, mw = 90 + k * 520, y + 106, 500
    # the machine: a rack chassis with drive bays and LEDs
    box(mx, my, mw, 64, WARM if ours else CHIP, GOLD if ours else LINE, 10, 2)
    for b in range(2):
        o.append(f'<rect x="{mx+18+b*62}" y="{my+16}" width="52" height="32" rx="4" fill="{NODE}" stroke="{GOLD if ours else MUT}" stroke-width="1.5"/><path d="M{mx+28+b*62} {my+40}H{mx+60+b*62}" stroke="{GOLD if ours else MUT}" stroke-width="2"/>')
    t(mx + 146, my + 40, name, 19, GOLD if ours else TXT, 700, room=300)
    o.append(f'<circle cx="{mx+mw-40}" cy="{my+32}" r="5" fill="{GREEN}"/><circle cx="{mx+mw-22}" cy="{my+32}" r="5" fill="{GOLD}"/>')
    for r, (lab, val) in enumerate(rows):
        ry = my + 96 + r * 28
        t(mx + 20, ry, lab, 17, MUT, 600, room=110)
        t(mx + 130, ry, val, 19, TXT, 600 if r == 0 or lab else 400, room=360)
arrow(600, y + P1, y + P1 + G)

# 2 Network: only the proxy is reachable; VMs on a private bridge; hosts at other sites call out
y += P1 + G
P2 = 496
layer(y, "2", "Network", "Only the proxy is reachable", P2)
# internet cloud
cx, cy = 600, y + 148
o.append(f'<path d="M{cx-90} {cy+22}a32 32 0 0 1 10-58a44 44 0 0 1 80-14a36 36 0 0 1 66 14a30 30 0 0 1 24 58z" fill="{CHIP}" stroke="{MUT}" stroke-width="2"/>')
t(cx, cy + 6, "Internet", 20, TXT, 700, "middle", room=160)
# browser (laptop) on the left
bx, by = 170, y + 110
box(bx, by, 96, 58, CHIP, MUT, 6, 2.5)
o.append(f'<path d="M{bx-14} {by+66}H{bx+110}" stroke="{MUT}" stroke-width="4" stroke-linecap="round"/>')
t(bx + 48, by + 96, "Browser", 18, TXT, 700, "middle", room=140)
line(bx + 110, by + 30, cx - 96, cy - 6, MUT)
# hosts at another site on the right: they call out
sx, sy = 868, y + 104
box(sx, sy, 236, 96, CHIP, LINE, 14, 2)
t(sx + 16, sy + 26, "Another site", 16, MUT, 600, room=200)
host_box(sx + 16, sy + 38)
o.append(f'<path d="M{sx+108} {sy+60}H{sx+124}" stroke="{MUT}" stroke-width="2"/>')
device_tv(sx + 126, sy + 44)
device_tv(sx + 180, sy + 44)
line(sx, sy + 60, cx + 100, cy - 4, GOLD, 2.5)
t(cx + 248, y + 226, "HTTPS out: no VPN, no port opened", 16, GOLD, 600, "middle", room=330)
# the node frame
nx, ny, nw, nh = 90, y + 238, 1020, 238
box(nx, ny, nw, nh, NODE, LINE, 18, 2)
t(nx + nw - 20, ny + 30, "Proxmox node", 18, MUT, 600, "end", room=200)
# public address badge, then the proxy
line(cx, cy + 24, cx, ny - 2, GOLD, 3)
box(cx - 90, ny - 16, 180, 30, GOLD, GOLD, 15, 2)
t(cx, ny + 5, "public address", 16, "#1a1a1a", 700, "middle", room=170)
pw = 220
box(cx - pw / 2, ny + 34, pw, 54, WARM, GOLD, 12, 2)
t(cx, ny + 68, "proxy", 22, GOLD, 700, "middle", room=200)
line(cx, ny + 14, cx, ny + 34, GOLD, 3)
# the bridge
bry = ny + 116
o.append(f'<rect x="{nx+20}" y="{bry-5}" width="{nw-40}" height="10" rx="5" fill="{LINE}"/>')
t(nx + 30, bry - 14, "vmbr0: private bridge, one /24 network", 16, MUT, 600, room=420)
t(nx + nw - 30, bry - 14, "internet out through the node (NAT)", 16, MUT, 400, "end", room=360)
line(cx, ny + 88, cx, bry - 6, GOLD, 3, head=False)
# what the proxy reaches, on the bridge
targets = [("frontend", "the app"), ("server", "/server API"), ("host", "/host/&lt;name&gt;/"),
           ("monitoring", "Grafana"), ("storage", "files"), ("database", "API")]
TW, TG = 156, 9
x0 = nx + (nw - (6 * TW + 5 * TG)) / 2
for i, (a, b) in enumerate(targets):
    px = x0 + i * (TW + TG)
    o.append(f'<path d="M{px+TW/2} {bry+5}V{bry+22}" stroke="{GOLD}" stroke-width="2.5"/>')
    pill(px, bry + 22, TW, a, b)
t(600, ny + nh - 18, "Fixed addresses: the VM id is the last number of its address.", 18, MUT, 400, "middle")
arrow(600, y + P2, y + P2 + G)

# 3 The VMs: every VM as a box inside the node
y += P2 + G
P3 = 772
layer(y, "3", "The VMs", "Debian 12 (Langfuse: Debian 13), CPU x86-64-v2-AES, start on boot", P3)
vms = [
    ("107", "proxy", "2 vCPU · 2 GB RAM", "32 GB disk", ["The only door from", "the internet, with TLS"], ["nginx"], ["80, 443 web", "8443 Studio, password"], "install_nginx.sh"),
    ("105", "frontend", "4 vCPU · 4 GB RAM", "32 GB disk", ["The web app", "people open"], ["vpt-frontend-prod", "(+ demo)"], ["5073 (5074 demo)"], "install_frontend.sh"),
    ("103", "server", "2 vCPU · 4 GB RAM", "32 GB disk", ["API, schedules,", "hosts list, results"], ["vpt-server, workers:", "incidents, scripts,", "heatmap"], ["5109"], "install_server.sh"),
    ("109", "host", "2 vCPU · 4 GB RAM", "32 + 32 GB disk", ["Drives devices in the", "data center: web, emulators"], ["vpt-host, vpt-stream,", "monitors, vpt-kpi,", "vpt-vnc, mediamtx"], ["6109 API, 6080 desktop", "8554, 8889 live video"], "install_host.sh"),
    ("102", "database", "2 vCPU · 4 GB RAM", "32 + 32 GB disk", ["Keeps all data: devices,", "tests, results, users"], ["Supabase in Docker:", "Postgres, auth,", "REST API, Studio"], ["54321 API, 54323 Studio", "54322 Postgres"], "install_db.sh"),
    ("101", "storage", "2 vCPU · 8 GB RAM", "32 + 424 GB disk", ["Files: screenshots,", "videos, reports. Queues"], ["MinIO, Redis, NFS"], ["9000 files, 9001 console", "6379 Redis, 2049 NFS"], "install_storage.sh"),
    ("106", "monitoring", "4 vCPU · 3 GB RAM", "32 GB disk", ["Dashboards", "and charts"], ["Grafana,", "image renderer"], ["3000"], "install_grafana.sh"),
    ("192", "langfuse", "4 vCPU · 8 GB RAM", "32 + 60 GB disk", ["Traces every AI call:", "prompt, cost, time"], ["Langfuse v3 in Docker:", "web, worker, ClickHouse,", "Postgres, Redis, MinIO"], ["3000"], "Docker Compose"),
]
nx, ny, nw = 90, y + 108, 1020
VW, VG, VH = 240, 16, 288
nh = 2 * VH + 16 + 62
box(nx, ny, nw, nh, NODE, LINE, 18, 2)
for i, (vid, name, size, disk, job, runs, ports, inst) in enumerate(vms):
    vx, vy = nx + 6 + (i % 4) * (VW + VG), ny + 18 + (i // 4) * (VH + 16)
    proxy = name == "proxy"
    box(vx, vy, VW, VH, WARM if proxy else CHIP, GOLD if proxy else LINE, 14, 2)
    box(vx + 14, vy + 14, 56, 28, GOLD if proxy else NODE, GOLD, 8, 1.5)
    t(vx + 42, vy + 34, vid, 17, "#1a1a1a" if proxy else GOLD, 700, "middle", room=50)
    t(vx + 82, vy + 36, name, 22, GOLD if proxy else TXT, 700, room=VW - 92)
    t(vx + 14, vy + 66, size, 16, TXT, 600, room=VW - 22)
    t(vx + 14, vy + 86, disk, 16, TXT, 600, room=VW - 22)
    for k, s in enumerate(job):
        t(vx + 14, vy + 110 + k * 19, s, 15, MUT, 400, room=VW - 22)
    o.append(f'<path d="M{vx+14} {vy+140}H{vx+VW-14}" stroke="{LINE}" stroke-width="1.5"/>')
    t(vx + 14, vy + 160, "RUNS", 12, GOLD, 600, sp=2, room=100)
    for k, s in enumerate(runs):
        t(vx + 14, vy + 178 + k * 19, s, 15, TXT, 400, room=VW - 22)
    t(vx + 14, vy + 240, "PORTS", 12, GOLD, 600, sp=2, room=100)
    for k, s in enumerate(ports):
        t(vx + 14, vy + 258 + k * 19, s, 15, TXT, 600, room=VW - 22)
    t(vx + VW - 14, vy + 240, inst, 12, MUT, 400, "end", room=150)
t(nx + 24, ny + nh - 24, "Our production VMs: 22 vCPU, 37 GB RAM, about 800 GB of disk.", 19, GOLD, 700, room=700)
t(nx + nw - 24, ny + nh - 24, "SCSI disks: discard, iothread", 16, MUT, 400, "end", room=300)
arrow(600, y + P3, y + P3 + G)

# 4 Who talks to whom inside the node
y += P3 + G
P4 = 368
layer(y, "4", "Who talks to whom", "Inside the node, on the private bridge", P4)
groups = [("server", "calls", [("database", "all data"), ("storage", "files, job queues"),
                               ("monitoring", "dashboards"), ("langfuse", "AI call traces")]),
          ("hosts", "call", [("server", "register, report"), ("database", ""),
                             ("storage", "upload captures")]),
          ("storage", "shares /shared over NFS", [("server", ""), ("frontend", ""), ("hosts", ""),
                                                  ("database", "dumps go here")])]
CW = 330
for g, (src, verb, dests) in enumerate(groups):
    gx = 90 + g * (CW + 15)
    pill(gx + 50, y + 100, CW - 100, src, gold=True, h=40)
    t(gx + CW / 2, y + 164, verb, 16, GOLD, 600, "middle", room=CW - 20)
    for k, (d, cap) in enumerate(dests):
        dy = y + 178 + k * 46
        o.append(f'<path d="M{gx+30} {y+140}V{dy+20}H{gx+52}" stroke="{GOLD}" stroke-width="2" fill="none"/>')
        o.append(f'<path d="M{gx+46} {dy+14}L{gx+54} {dy+20}L{gx+46} {dy+26}" fill="none" stroke="{GOLD}" stroke-width="2"/>')
        box(gx + 56, dy, CW - 56, 40, CHIP, LINE, 10, 1.5)
        t(gx + 72, dy + 26, d, 17, TXT, 700, room=120)
        if cap:
            t(gx + CW - 12, dy + 26, cap, 14, MUT, 400, "end", room=CW - 190)
arrow(600, y + P4, y + P4 + G)

# 5 Order: six install steps
y += P4 + G
P5 = 338
layer(y, "5", "Order", "Install the VMs in this order", P5)
steps = [("Create the VMs", ["fixed addresses; pass capture", "cards and IR to device VMs"]),
         ("Database first", ["copy its 4 keys to server and", "hosts: URL, anon key, service", "key, JWT secret"]),
         ("Storage, server", ["then monitoring", "and Langfuse"]),
         ("Frontend", ["built with the", "public addresses"]),
         ("Proxy", ["with certificates"]),
         ("Hosts", ["each pointed at the server.", "Check: every host shows", "in Devices"])]
SW = 336
for i, (head, body) in enumerate(steps):
    sx, sy = 90 + (i % 3) * (SW + 6), y + 100 + (i // 3) * 112
    box(sx, sy, SW - 6, 104, CHIP, LINE, 14, 1.5)
    o.append(f'<circle cx="{sx+28}" cy="{sy+28}" r="16" fill="{GOLD}"/>')
    t(sx + 28, sy + 34, str(i + 1), 17, "#1a1a1a", 700, "middle")
    t(sx + 54, sy + 35, head, 20, TXT, 700, room=SW - 70)
    for k, s in enumerate(body):
        t(sx + 54, sy + 56 + k * 18, s, 15, MUT, 400, room=SW - 70)
arrow(600, y + P5, y + P5 + G)

# 6 Day two
y += P5 + G
P6 = 196
layer(y, "6", "Day two", "", P6)
rules = [("Back up", ["every VM each night, off site,", "plus the daily database dump"]),
         ("Grow the disk", ["each VM has its own data disk:", "grow the disk, not the VM"]),
         ("Too slow?", ["add RAM to the database", "and the server first"])]
for i, (head, body) in enumerate(rules):
    sx, sy = 90 + i * (SW + 6), y + 88
    box(sx, sy, SW - 6, 86, CHIP, LINE, 14, 1.5)
    t(sx + 20, sy + 30, head, 20, GOLD, 700, room=SW - 40)
    for k, s in enumerate(body):
        t(sx + 20, sy + 54 + k * 19, s, 15, TXT, 400, room=SW - 40)

# footer
y += P6
t(600, y + 46, "Hosts for real TVs and boxes are a Raspberry Pi or mini PC at each site, not VMs.", 18, MUT, 400, "middle")
t(600, y + 80, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
Htot = y + 112
o.append("</svg>")
open("docs/img/proxmox.svg", "w").write("\n".join(o).replace(H, str(Htot)))
print("docs/img/proxmox.svg", Htot)
