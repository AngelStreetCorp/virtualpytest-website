#!/usr/bin/env python3
"""Writes docs/img/fingerprint.svg (Docs poster "Fingerprint").

Sources: Learn lesson 3.4 and its Go deeper (how a fingerprint is computed, how Localize names the screen), and
docs/agent/navigation/FINGERPRINT.md of the product repo. No date anywhere on the poster.
Run from the repo root. If DejaVu Sans Bold is installed (the font headless Chromium falls back to), every chip label
is measured and the script fails when one is wider than its chip.
"""
import os, sys

W = 1200
BG, PANEL, LINE, TXT, MUT, GOLD, CHIP = "#161616", "#212121", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d", "#2a2a2a"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
o, checks = [], []

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0, maxw=None):
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{esc(s)}</text>')
    if maxw:
        checks.append((s, size, w >= 600, maxw))

def box(x, y, w, h, fill=PANEL, stroke=LINE, r=22, sw=2):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

def arrow(x, y1, y2):
    o.append(f'<path d="M{x} {y1}V{y2-12}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x-12} {y2-18}L{x} {y2-4}L{x+12} {y2-18}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')

INNER_X, INNER_W, CH, CGAP, RGAP = 90, 1020, 70, 18, 14

def chip_rows(y, rows):
    """rows: list of lists of (name, caption). Each row is spread over the inner width. Returns the y under the chips."""
    for row in rows:
        n = len(row)
        w = (INNER_W - (n - 1) * CGAP) / n
        for i, (a, b) in enumerate(row):
            cx = INNER_X + i * (w + CGAP)
            box(round(cx), y, round(w), CH, fill=CHIP, r=16)
            t(round(cx + w / 2), y + 30, a, 22, TXT, 600, "middle", maxw=w - 20)
            t(round(cx + w / 2), y + 55, b, 16, MUT, 400, "middle", maxw=w - 16)
        y += CH + RGAP
    return y - RGAP

def card(y, n, title, sub, rows, notes=(), last=False):
    """One panel: number circle, title, grey sub line, chip rows, grey notes. Returns the y of the next card."""
    h = 112 + len(rows) * (CH + RGAP) - RGAP + 26 + len(notes) * 28 + 10 if rows else 112 + len(notes) * 28 + 6
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, title, 34, TXT, 700, maxw=1140 - 156 - 20)
    t(156, y + 82, sub, 21, MUT, 400, maxw=1140 - 156 - 20)
    ny = chip_rows(y + 112, rows) + 34 if rows else y + 120
    for i, line in enumerate(notes):
        t(600, ny + i * 28, line, 19, MUT, 400, "middle", maxw=1040)
    if not last:
        arrow(600, y + h, y + h + 50)
    return y + h + 50

o.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 HHH" width="1200" height="HHH" role="img" aria-labelledby="ti"><title id="ti">Fingerprint: the blob stored on a navigation node, the sibling check at save, the refresh script, the six abstain doors of identify_screen, and no references on a node whose fingerprint works, in one image</title>')
o.append('<rect width="1200" height="HHH" fill="%s"/>' % BG)
t(60, 100, "UI VERIFICATION · FINGERPRINT", 20, GOLD, 500, sp=3)
t(60, 180, "Fingerprint", 58, TXT, 700)
t(60, 236, "Which node is on screen right now?", 29, MUT, 400)
t(60, 276, "navigation_nodes.data.fingerprint, from pixels, in the doc's own words.", 24, MUT, 400)

import base64
GREEN, RED = "#4ade80", "#f87171"
def b64(name):
    return base64.b64encode(open(f"docs/img/fingerprint-real-{name}.jpg", "rb").read()).decode()

def example_card(y):
    """A drawn example (generic screens, tools/fingerprint_example_draw.py) run through the real matcher: zone bits,
    layout scores and confidence below are what identify_screen / fingerprint_evidence printed; none picked by hand."""
    h = 800
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, "•", 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, "A real result", 34, TXT, 700)
    t(156, y + 82, "Drawn screens, the real matcher. The rail changed, the screen is still named", 21, MUT, 400, maxw=960)
    ty = y + 116
    for x, name, cap in ((90, "stored", "Node screenshot: home"), (440, "live", "Live frame")):
        o.append(f'<image x="{x}" y="{ty}" width="320" height="180" href="data:image/jpeg;base64,{b64(name)}"/>')
        o.append(f'<rect x="{x}" y="{ty}" width="320" height="180" rx="6" fill="none" stroke="{LINE}" stroke-width="2"/>')
        t(x + 160, ty + 206, cap, 18, MUT, 400, "middle")
    # zones
    zx = 800
    t(zx, ty + 14, "ZONES", 16, GOLD, 600, sp=2); t(1110, ty + 14, "BITS ≤ 14", 16, GOLD, 600, "end", sp=1)
    for i, (z, b) in enumerate(ZONES_REAL):
        yy = ty + 48 + i * 33
        o.append(f'<line x1="{zx}" y1="{yy-22}" x2="1110" y2="{yy-22}" stroke="{LINE}" stroke-width="1"/>')
        ok = b <= 14
        t(zx, yy, z, 20, TXT, 500); t(1040, yy, str(b), 20, TXT if ok else RED, 600, "end")
        t(1088, yy, "✓" if ok else "✗", 22, GREEN if ok else RED, 700, "middle")
    # checks
    cy = ty + 250
    t(90, cy, "CHECKS", 16, GOLD, 600, sp=2); t(330, cy, "VALUE", 16, GOLD, 600, sp=2); t(470, cy, "NEEDS", 16, GOLD, 600, sp=2)
    for i, (c, v, n_) in enumerate(CHECKS_REAL):
        yy = cy + 34 + i * 32
        o.append(f'<line x1="90" y1="{yy-22}" x2="590" y2="{yy-22}" stroke="{LINE}" stroke-width="1"/>')
        t(90, yy, c, 19, TXT, 500); t(330, yy, v, 19, TXT, 600); t(470, yy, n_, 19, MUT, 400)
        t(570, yy, "✓", 20, GREEN, 700, "middle")
    # closest screens
    sx = 680
    t(sx, cy, "CLOSEST SCREENS", 16, GOLD, 600, sp=2); t(900, cy, "BEST / 2ND", 16, GOLD, 600, sp=1); t(1110, cy, "GAP", 16, GOLD, 600, "end", sp=1)
    for i, (nm, bs, gap) in enumerate(CLOSEST_REAL):
        yy = cy + 34 + i * 32
        o.append(f'<line x1="{sx}" y1="{yy-22}" x2="1110" y2="{yy-22}" stroke="{LINE}" stroke-width="1"/>')
        t(sx, yy, nm, 19, TXT if i == 0 else MUT, 600 if i == 0 else 400); t(900, yy, bs, 19, MUT, 400)
        t(1110, yy, gap, 19, GREEN if i == 0 else MUT, 600 if i == 0 else 400, "end")
    # bit grids of the zone that changed (the real 256 bits of both dHashes, XOR = the cells that differ)
    gy = y + 600
    t(90, gy, "BIT GRIDS · bottom zone, 16 x 16", 16, GOLD, 600, sp=2)
    st, lv = [int(c) for c in bin(int(BOTTOM_STORED, 16))[2:].zfill(256)], [int(c) for c in bin(int(BOTTOM_LIVE, 16))[2:].zfill(256)]
    for x, cap, bits, col in ((90, "Stored", st, "#f2f2f2"), (260, "Live", lv, "#f2f2f2"), (430, "Differ", [a ^ b for a, b in zip(st, lv)], RED)):
        cell = 8
        o.append(f'<rect x="{x}" y="{gy+16}" width="{16*cell}" height="{16*cell}" rx="4" fill="#161616" stroke="{LINE}"/>')
        o.append(f'<g fill="{col}">' + "".join(f'<rect x="{x+(i%16)*cell}" y="{gy+16+(i//16)*cell}" width="{cell}" height="{cell}"/>' for i, v in enumerate(bits) if v) + '</g>')
        t(x + 64, gy + 16 + 128 + 26, cap, 18, MUT, 400, "middle")
    t(620, gy + 70, "Each cell is one bit: brighter than its left", 19, MUT, 400, maxw=500)
    t(620, gy + 98, "neighbour or not. Same bits = same cell.", 19, MUT, 400, maxw=500)
    t(620, gy + 140, f"{sum(a ^ b for a, b in zip(st, lv))} cells differ in the bottom zone", 21, RED, 600, maxw=500)
    t(620, gy + 170, "(the rail changed): over the 14 bits line.", 19, MUT, 400, maxw=500)
    arrow(600, y + h, y + h + 50)
    return y + h + 50

def report_card(y):
    """The real fingerprint report page (render_fingerprint_report) of the drawn example, expanded Bit grids."""
    ih = 999
    h = 112 + ih + 40
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, "•", 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, "The fingerprint report", 34, TXT, 700)
    t(156, y + 82, "Every check, with its value and its limit. The same page opens from a run.", 21, MUT, 400, maxw=960)
    o.append(f'<image x="90" y="{y+112}" width="1020" height="{ih}" href="data:image/jpeg;base64,{b64("report")}"/>')
    o.append(f'<rect x="90" y="{y+112}" width="1020" height="{ih}" rx="6" fill="none" stroke="{LINE}" stroke-width="2"/>')
    t(600, y + 112 + ih + 28, "Drawn screens, run through the real matcher and the real report code.", 19, MUT, 400, "middle", maxw=1040)
    return y + h

# Values printed by the real code on the drawn frames (identify_screen, fingerprint_evidence.zone_distances / rank_nodes).
BOTTOM_STORED = "9094909490949094909490949094909490949094909492940000000000000000"
BOTTOM_LIVE = "94b494b494b494b494b494b494b494b494b494b494b496b40000000000000000"
ZONES_REAL = [("full", 12), ("top", 0), ("center", 0), ("left", 0), ("bottom", 24)]
CHECKS_REAL = [("Picture", "edges 3.5", "≥ 3.0"), ("Layout", "0 bits", "≤ 14"), ("2nd zone", "0 bits", "≤ 44"),
               ("Lead", "19 bits", "> 14"), ("Only match", "yes", "yes"), ("Confidence", "100%", "≥ 55%")]
CLOSEST_REAL = [("home", "0 / 0", "closest"), ("guide", "8 / 11", "+19"), ("movies", "10 / 11", "+21"), ("settings", "12 / 13", "+25")]

y = 330
y = card(y, "•", "Overview", "One card per section of the fingerprint doc, in its order", [
    [("The blob", "what is stored"), ("No references", "on a node whose fingerprint works")],
    [("Sibling check at save", "tied or claimed_by"), ("Fingerprints decay", "the refresh script")],
    [("The six abstain doors", "of identify_screen")],
])
y = card(y, "1", "The blob", "compute_fingerprint(img_bgr) returns", [
    [("dhash", "full frame, 256 bits"), ("regions", "full, top, center, left, bottom")],
    [("crop", "focused-tile logo dHash"), ("focus", "kind: nav, box or none"), ("title", "OCR heading, top-left")],
], ["Kept in navigation_nodes.data.fingerprint, built from the node screenshot.", "FINGERPRINT_VERSION = 6: v4 dhash + focus, v5 regions, v6 crop."])
y = example_card(y)
y = card(y, "2", "No references on a node whose fingerprint works", "A node is named by its fingerprint", [
    [("Reference", "a text, image or color check"), ("Not a reference", "identity, state, focus")],
    [("The fingerprint works", "its own screenshot names it alone"), ("reference_reason", "kept only where it does not")],
], ["The gate refuses a reference on a node whose fingerprint works.", "Nightly audit: REF_WITH_WORKING_FP."])
y = card(y, "3", "Sibling check at save", "Before a node screenshot is stored", [
    [("tied", "refused, unless force"), ("claimed_by", "saved, with a warning")],
    [("Declared twins", "never count")],
], ["The matcher is asked if Localize could tell the node from its siblings."])
y = card(y, "4", "Fingerprints decay: the refresh script", "A stored fingerprint is one frame", [
    [("Daily content", "rails, posters, recordings"), ("Localize answers Unknown", "on a page that passed")],
    [("fingerprint_refresh", "go to the node, prove it, save"), ("Periodic", "run it nightly")],
], ["A node it cannot prove arrives is not forced."])
y = card(y, "5", "The six abstain doors of identify_screen", "Each one removes candidates; empty is an abstention", [
    [("1 low-content frame", "edge density under 3.0"), ("2 no underline match", "nav underline matched no node")],
    [("3 far-region title gate", "region distance over 60"), ("4 title_score", "under 0.5 is dropped")],
    [("5 dHash fallback", "narrowing, margin 14"), ("6 confidence floor", "FP_MIN_CONFIDENCE 0.55")],
], ["Not a guess: with no match the result is known_screen or unknown."])
y = report_card(y)
H = y + 90
t(600, H - 30, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
o.append('</svg>')
svg = "\n".join(o).replace("HHH", str(H))
open("docs/img/fingerprint.svg", "w").write(svg)

FONTS = {True: "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", False: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"}
if os.path.exists(FONTS[True]):
    from PIL import ImageFont
    bad = []
    for s, size, bold, maxw in checks:
        wpx = ImageFont.truetype(FONTS[bold], size).getlength(s)
        if wpx > maxw:
            bad.append(f"{wpx:.0f} > {maxw:.0f} px: {s}")
    if bad:
        sys.exit("text wider than its box with the fallback font:\n  " + "\n  ".join(bad))
print(f"docs/img/fingerprint.svg written, {W}x{H}, {len(checks)} labels fit")
