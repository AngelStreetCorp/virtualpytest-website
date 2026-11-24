#!/usr/bin/env python3
"""Writes docs/img/fingerprint.svg (Docs poster "Know every screen by its layout").

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

o.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 HHH" width="1200" height="HHH" role="img" aria-labelledby="ti"><title id="ti">Know every screen by its layout: what a screen fingerprint is, how it is made, how Localize uses it, when it says not sure, and how it stays fresh, in one image</title>')
o.append('<rect width="1200" height="HHH" fill="%s"/>' % BG)
t(60, 100, "UI VERIFICATION · FINGERPRINTS", 20, GOLD, 500, sp=3)
t(60, 180, "Know every screen by its layout", 54, TXT, 700)
t(60, 236, "A fingerprint is a short code of a screen.", 29, MUT, 400)
t(60, 276, "No picture to take. Any screen named in 11 ms.", 24, MUT, 400)
y = 330
y = card(y, "1", "What a fingerprint is", "A picture signature of one screen, stored on its node", [
    [("Whole frame", "256 bits, 64 hex chars"), ("5 regions", "full, top, centre, left, bottom")],
    [("Focus", "the underline or tile"), ("Focused tile", "a small crop of it"), ("Title", "read from the top-left")],
], ["The screen is greyed, shrunk to 17 x 16, and each cell is brighter than its left cell or not.", "Details melt away. The layout stays."])
y = card(y, "2", "Made when the node is saved", "From the node screenshot, nothing to type", [
    [("Screenshot", "taken on the node"), ("Fingerprint", "computed from it"), ("Stored", "on the node")],
    [("Look-alikes", "a tie with a sibling is refused")],
], ["It is kept in the node data, next to the screenshot.", "Saving a node that Localize could not tell from another asks you first."])
y = card(y, "3", "Localize names the live screen", "The live frame against every reachable node", [
    [("Live frame", "fingerprinted once, 11 ms"), ("Compare", "bits that differ, per region")],
    [("2 regions agree", "closest within 14 bits"), ("Focus matches", "same underline, same tab"), ("Title", "tells look-alikes apart")],
], ["All 27 screens of a real map are compared in under a tenth of a millisecond.", "One screen left: that is its name, with a confidence."])
y = card(y, "4", "When it is not sure, it says so", "An empty list is an abstention, never a guess", [
    [("Nothing to see", "black, asleep, fading"), ("No underline match", "no tab agrees")],
    [("Far and no title", "spurious match refused"), ("Too many left", "it cannot tell them apart")],
], ["Unknown is a good answer. A wrong name would be worse."])
y = card(y, "5", "Daily content drifts", "A stored fingerprint is one frame", [
    [("Posters change", "rails, recordings, heroes"), ("Match fails", "Localize answers Unknown")],
    [("fingerprint_refresh", "go to the node, prove it, save"), ("Nightly", "a scheduled run")],
], ["The script recaptures every fingerprint-verified node of a tree.", "A node it cannot prove is reported, never forced."])
y = card(y, "6", "It replaces reference images", "One check per node, once it works", [
    [("Before", "an image or text check per node"), ("After", "the fingerprint names the screen")],
    [("goto", "proves it arrived"), ("Localize", "names the screen"), ("Monitoring", "all day, every device")],
], ["Text checks still read a value, like a version number.", "The focused tab or tile keeps its own focus check."], last=True)
H = y + 20
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
