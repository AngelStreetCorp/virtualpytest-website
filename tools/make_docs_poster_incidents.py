#!/usr/bin/env python3
"""Writes docs/img/incidents.svg (Docs poster: the path of one incident, from the host to the people who act on it).

Title = Learn lesson 6.1 "Incidents Caught Live" (learn/cards/incidents.html). Starts where the posters `watched`
(the host's watchers, a problem that lasts 30 s becomes an incident) and `freeze-discard` (how one freeze is decided)
stop. Sources: learn/cards/incidents.html, learn/cards/discard-incidents.html, learn/cards/deep-incidents.html,
virtualpytest docs/user-guide/monitoring.md (What is checked, Route alerts) and docs/agent/ai/ALERT_TRIAGE.md.
Drawn examples only. Run from the repo root.

Fails when a text is wider than its room in DejaVu Sans (headless Chromium's fallback font)."""
from PIL import ImageFont

W = 1200
BG, PANEL, CHIP, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#2a2a2a", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
RED, GREEN = "#ef4444", "#4ade80"
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


def harrow(x1, x2, y, col=GOLD):
    o.append(f'<path d="M{x1} {y}H{x2-10}" stroke="{col}" stroke-width="4" stroke-linecap="round"/><path d="M{x2-20} {y-11}L{x2-4} {y}L{x2-20} {y+11}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')


def curve(x1, y1, x2, y2, col=GOLD, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    mx = (x1 + x2) / 2
    o.append(f'<path d="M{x1} {y1}C{mx} {y1} {mx} {y2} {x2-8} {y2}" fill="none" stroke="{col}" stroke-width="3.5"{d}/>'
             f'<path d="M{x2-18} {y2-9}L{x2-4} {y2}L{x2-18} {y2+9}" fill="none" stroke="{col}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')


def layer(y, n, title, sub, h):
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, title, 34, TXT, 700, room=960)
    if sub:
        t(156, y + 82, sub, 21, MUT, 400, room=960)


def tag(x, y, s, col, size=17):
    """A coloured pill (incident type, verdict, event)."""
    font_w = ImageFont.truetype(TTF[True], size).getlength(s)
    w = font_w + 26
    o.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size+15}" rx="{(size+15)/2}" fill="none" stroke="{col}" stroke-width="2"/>')
    t(x + w / 2, y + size + 6, s, size, col, 700, "middle", room=w)
    return w


# drawn screens (generic, no app) -------------------------------------------------------------------------------
def scr_black(x, y, w, h):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#050505" stroke="#444" stroke-width="1.5"/>')


def scr_menu(x, y, w, h):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#1f2a3a" stroke="#444" stroke-width="1.5"/>')
    o.append(f'<rect x="{x+8}" y="{y+8}" width="{w*0.4:.0f}" height="7" rx="3" fill="#8aa0bf"/>')
    tw = (w - 16 - 3 * 6) / 4
    for r in range(2):
        for c in range(4):
            fill = "#e0a96d" if (r, c) == (0, 0) else "#3b4d66"
            o.append(f'<rect x="{x+8+c*(tw+6):.0f}" y="{y+24+r*(h*0.33):.0f}" width="{tw:.0f}" height="{h*0.26:.0f}" rx="3" fill="{fill}"/>')


def scr_standby(x, y, w, h):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#0b0b12" stroke="#444" stroke-width="1.5"/>')
    o.append(f'<circle cx="{x+w/2}" cy="{y+h/2-4}" r="{h*0.16:.0f}" fill="none" stroke="#6b7280" stroke-width="3"/>'
             f'<path d="M{x+w/2} {y+h/2-4-h*0.24:.0f}V{y+h/2-4:.0f}" stroke="#6b7280" stroke-width="3" stroke-linecap="round"/>')


def scr_video(x, y, w, h):
    """A landscape picture (a frame of a programme)."""
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#5b7fa6" stroke="#444" stroke-width="1.5"/>')
    o.append(f'<circle cx="{x+w*0.75:.0f}" cy="{y+h*0.3:.0f}" r="{h*0.12:.0f}" fill="#f6d27a"/>')
    o.append(f'<path d="M{x} {y+h*0.8:.0f}L{x+w*0.3:.0f} {y+h*0.42:.0f}L{x+w*0.5:.0f} {y+h*0.65:.0f}L{x+w*0.7:.0f} {y+h*0.38:.0f}L{x+w} {y+h*0.78:.0f}V{y+h-6}Q{x+w} {y+h} {x+w-6} {y+h}H{x+6}Q{x} {y+h} {x} {y+h-6}Z" fill="#2f4a33"/>')


def incident_card(x, y, kind, draw, verdict=None):
    """A small incident: picture plus its type. verdict = (text, colour) shown under it."""
    box(x, y, 196, 124, CHIP, LINE, 14)
    draw(x + 12, y + 12, 172, 76)
    t(x + 98, y + 112, kind, 17, TXT, 700, "middle", room=180)


H = "@@H@@"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Incidents Caught Live: the path of one incident, from the host to the people who act on it, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# header
t(60, 90, "MONITOR 24/7 · INCIDENTS", 20, GOLD, 500, sp=3)
t(60, 166, "Incidents Caught Live", 62, TXT, 700)
t(60, 218, "Watched 24/7, even when no test runs.", 29, TXT, 600)
t(60, 256, "Incidents open on their own, then reach the people who act.", 24, MUT, 400)
t(60, 294, "Before this: Your devices, watched 24/7. One freeze up close: Freeze: menu or stuck video?", 18, MUT, 400)

# 1 the incident ------------------------------------------------------------------------------------------------
y = 322
P1 = 372
layer(y, "1", "An incident opens, with its picture", "A black screen, a freeze or no sound that lasted 30 seconds", P1)
# drawn device, wired to its host (always on), a 30 s clock, then the incident card
tx, ty = 100, y + 116
o.append(f'<rect x="{tx}" y="{ty}" width="180" height="112" rx="12" fill="#0d0d0d" stroke="{MUT}" stroke-width="3"/>')
scr_video(tx + 9, ty + 9, 162, 94)
o.append(f'<path d="M{tx+70} {ty+122}H{tx+110}" stroke="{MUT}" stroke-width="4" stroke-linecap="round"/>')
t(tx + 90, ty + 150, "Your device", 18, MUT, 400, "middle", room=180)
hx, hy = 306, ty + 8
o.append(f'<path d="M{tx+180} {ty+56}H{hx}" stroke="{MUT}" stroke-width="3"/>')
box(hx, hy, 130, 96, "#2a2418", GOLD, 14, 2.5)
t(hx + 65, hy + 30, "Host", 20, GOLD, 700, "middle", room=110)
ex, ey = hx + 65, hy + 62
o.append(f'<path d="M{ex-30} {ey}Q{ex} {ey-24} {ex+30} {ey}Q{ex} {ey+24} {ex-30} {ey}Z" fill="none" stroke="{GOLD}" stroke-width="3"/><circle cx="{ex}" cy="{ey}" r="9" fill="{GOLD}"/>')
t(hx + 65, ty + 150, "always on", 18, GOLD, 600, "middle", room=130)
# timer
cx, cy = 505, ty + 56
o.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="none" stroke="{GOLD}" stroke-width="7"/>')
t(cx, cy + 9, "30 s", 24, TXT, 700, "middle", room=70)
harrow(440, 464, cy, MUT)
harrow(546, 586, cy)
# no test, no script: a crossed-out script page
sx, sy = 100, ty + 178
box(sx, sy, 436, 54, "none", LINE, 27, 2, "8 6")
o.append(f'<rect x="{sx+22}" y="{sy+11}" width="26" height="32" rx="3" fill="none" stroke="{MUT}" stroke-width="2.5"/>'
         f'<path d="M{sx+28} {sy+21}H{sx+42}M{sx+28} {sy+28}H{sx+42}M{sx+28} {sy+35}H{sx+38}" stroke="{MUT}" stroke-width="2"/>'
         f'<path d="M{sx+16} {sy+46}L{sx+54} {sy+8}" stroke="{RED}" stroke-width="3.5" stroke-linecap="round"/>')
t(sx + 70, sy + 35, "No test, no script to write", 21, TXT, 600, room=350)
# incident card (like a row of the Incidents page)
ix, iy = 596, y + 104
box(ix, iy, 514, 220, "#2a1d1d", RED, 16, 2)
t(ix + 24, iy + 38, "INCIDENT", 18, RED, 700, sp=3, room=200)
scr_video(ix + 24, iy + 60, 200, 114)
t(ix + 124, iy + 200, "proof frame", 16, MUT, 400, "middle", room=190)
tag(ix + 250, iy + 60, "Freeze", RED, 18)
t(ix + 250, iy + 128, "Channel 14 · TV box", 20, TXT, 600, room=250)
y += P1
arrow(600, y, y + 36)

# 2 the triage --------------------------------------------------------------------------------------------------
y += 36
P2 = 556
layer(y, "2", "Automatic triage: harmless ones are discarded", "Many alarms are harmless, like a menu left open", P2)
# three incoming incidents on the left
cols = [("Freeze", scr_menu), ("Black screen", scr_standby), ("Freeze", scr_video)]
ly = [y + 116, y + 251, y + 386]
for (kind, draw), yy in zip(cols, ly):
    incident_card(100, yy - 14, kind, draw)
# triage box in the middle
bx, by, bw, bh = 410, y + 178, 300, 220
box(bx, by, bw, bh, "#2a2418", GOLD, 18, 2.5)
t(bx + bw / 2, by + 44, "AUTOMATIC TRIAGE", 18, GOLD, 700, "middle", sp=2, room=bw - 20)
# a small eye: it looks at the picture
ex, ey = bx + bw / 2, by + 98
o.append(f'<path d="M{ex-42} {ey}Q{ex} {ey-34} {ex+42} {ey}Q{ex} {ey+34} {ex-42} {ey}Z" fill="none" stroke="{GOLD}" stroke-width="3.5"/><circle cx="{ex}" cy="{ey}" r="12" fill="{GOLD}"/>')
t(bx + bw / 2, by + 158, "Looks at the picture", 20, TXT, 600, "middle", room=bw - 20)
t(bx + bw / 2, by + 188, "Real problem or not?", 18, MUT, 400, "middle", room=bw - 20)
for yy in ly:
    curve(296, yy + 50, bx, by + bh / 2, MUT)
# results on the right
rx = 790
res = [("Menu left open", "Discarded", MUT, y + 116), ("Standby screen", "Discarded", MUT, y + 251), ("Picture stuck", "Kept", RED, y + 386)]
for i, (what, verdict, col, yy) in enumerate(res):
    curve(bx + bw, by + bh / 2, rx, yy + 50, GOLD if verdict == "Kept" else MUT, "" if verdict == "Kept" else "7 6")
    box(rx, yy, 320, 100, "#2a1d1d" if verdict == "Kept" else CHIP, RED if verdict == "Kept" else LINE, 14, 2)
    t(rx + 22, yy + 42, what, 21, TXT if verdict == "Kept" else MUT, 700, room=280)
    tag(rx + 22, yy + 56, verdict, col, 16)
t(600, y + P2 - 24, "A screen judged harmless is remembered: next time, no AI call.", 21, GOLD, 700, "middle")
y += P2
arrow(600, y, y + 36)

# 3 the alert reaches people ------------------------------------------------------------------------------------
y += 36
P3 = 362
layer(y, "3", "Only the kept alerts are sent", "To an email address or a webhook of yours", P3)
# a drawn message (email)
mx, my = 100, y + 104
box(mx, my, 500, 200, "#f2f2f2", "#f2f2f2", 14)
o.append(f'<rect x="{mx}" y="{my}" width="500" height="40" rx="14" fill="#e4e4e4"/><rect x="{mx}" y="{my+26}" width="500" height="14" fill="#e4e4e4"/>')
o.append(f'<rect x="{mx+18}" y="{my+12}" width="24" height="17" rx="2" fill="none" stroke="#7a5a2e" stroke-width="2"/><path d="M{mx+18} {my+13}L{mx+30} {my+22}L{mx+42} {my+13}" fill="none" stroke="#7a5a2e" stroke-width="2"/>')
t(mx + 54, my + 27, "Email", 17, "#7a5a2e", 700, room=200)
t(mx + 22, my + 78, "[DOWN] Frozen picture on 14", 23, "#1a1a1a", 700, room=460)
scr_video(mx + 22, my + 98, 130, 74)
t(mx + 168, my + 120, "proof frame", 18, "#4a4a4a", 600, room=300)
t(mx + 168, my + 150, "link to the incident", 18, "#7a5a2e", 600, room=300)
t(mx + 168, my + 178, "channel, device, cause", 16, "#6e6e6e", 400, room=300)
# the three events, as a column on the right
ev = [("DOWN", RED, "when the alert opens", "usually within 2 minutes"),
      ("STILL DOWN", GOLD, "nobody acknowledged it", "after the minutes you set"),
      ("RESOLVED", GREEN, "the picture is back", "")]
ex0, ey0 = 650, y + 112
for i, (name, col, a, b) in enumerate(ev):
    yy = ey0 + i * 70
    o.append(f'<circle cx="{ex0+10}" cy="{yy+16}" r="9" fill="{col}"/>')
    if i < 2:
        o.append(f'<path d="M{ex0+10} {yy+28}V{yy+66}" stroke="{LINE}" stroke-width="3"/>')
    t(ex0 + 34, yy + 24, name, 21, col, 700, room=170)
    t(ex0 + 200, yy + 24, a, 18, TXT, 600, room=260)
    if b:
        t(ex0 + 200, yy + 48, b, 16, MUT, 400, room=260)
t(600, y + P3 - 22, "A false alarm never reaches you.", 22, GOLD, 700, "middle")
y += P3
arrow(600, y, y + 36)

# 4 people act on the Incidents page -----------------------------------------------------------------------------
y += 36
P4 = 312
layer(y, "4", "People act on the Incidents page", "Monitoring, then Incidents", P4)
px, py = 100, y + 104
box(px, py, 1000, 150, "#f2f2f2", "#f2f2f2", 14)
o.append(f'<rect x="{px}" y="{py}" width="1000" height="36" rx="14" fill="#e4e4e4"/><rect x="{px}" y="{py+22}" width="1000" height="14" fill="#e4e4e4"/>')
for k, c in enumerate(("#ef4444", "#f59e0b", "#22c55e")):
    o.append(f'<circle cx="{px+22+k*18}" cy="{py+18}" r="5.5" fill="{c}"/>')
t(px + 90, py + 25, "Incidents", 17, "#1a1a1a", 700, room=200)
scr_video(px + 20, py + 52, 140, 80)
t(px + 180, py + 82, "Freeze", 21, "#b91c1c", 700, room=160)
t(px + 180, py + 112, "Channel 14 · TV box", 17, "#4a4a4a", 500, room=230)
o.append(f'<rect x="{px+430}" y="{py+66}" width="120" height="34" rx="17" fill="#dcfce7"/>')
t(px + 490, py + 89, "Resolved", 17, "#15803d", 700, "middle", room=110)
# Discard / Keep buttons
o.append(f'<rect x="{px+620}" y="{py+62}" width="150" height="44" rx="10" fill="#ffffff" stroke="#b8b8b8" stroke-width="2"/>')
t(px + 695, py + 91, "Discard", 19, "#1a1a1a", 700, "middle", room=140)
o.append(f'<rect x="{px+790}" y="{py+62}" width="150" height="44" rx="10" fill="{GOLD}"/>')
t(px + 865, py + 91, "Keep", 19, "#1a1a1a", 700, "middle", room=140)
t(600, y + P4 - 26, "Your Discard or Keep teaches the triage that screen.", 22, GOLD, 700, "middle")
y += P4

# footer
t(600, y + 50, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
Htot = y + 84
o.append("</svg>")
open("docs/img/incidents.svg", "w").write("\n".join(o).replace(H, str(Htot)))
print("docs/img/incidents.svg", Htot)
