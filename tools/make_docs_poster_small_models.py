#!/usr/bin/env python3
"""Writes docs/img/small-models.svg (Docs poster "Our own small models").

Source: docs/ai/AI-USE-CASES.md of the product repo, section "Our own small models: how we trained them". The poster
follows that section in its order: the six steps, one card per model (the table's columns), what moved the score,
the lessons. No date anywhere on the poster.
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

body = []
y = 330
y = card(y, "•", "Overview", "Three small models of our own, taught by the cloud models", [
    [("The six steps", "the same for every job"), ("Freeze word classifier", "discard incidents")],
    [("Localize model", "which screen is this?"), ("Screen namer", "name an unknown screen")],
    [("What moved the score", "better labels"), ("Lessons", "smaller is often enough")],
])
y = card(y, "•", "The six steps", "The same for every job", [
    [("1 · Data", "the logged calls of the job"), ("2 · Test set", "two strong judges agree"), ("3 · Teacher", "writes the answers")],
    [("4 · Train", "a LoRA in 15 to 30 min"), ("5 · Replay", "past calls it never saw"), ("6 · Serve", "sure answers only")],
], ["A run on a rented GPU costs 0.4 to 1.6 USD. The cloud model stays the fallback."])
y = card(y, "1", "Freeze word classifier", "Discard incidents: is a still screen a menu or a stuck video?", [
    [("Word pieces", "no language model"), ("2 MB", "plain Python"), ("0.25 ms", "per alert")],
    [("95.6 to 99.2 %", "on three test sets"), ("0 % of subtitles", "called menu"), ("Every night", "learns again")],
], ["Taught by Haiku and Sonnet on 4,235 sure freeze rows. Runs on the server."])
y = card(y, "2", "Localize model", "Which known screen is this, when the fingerprint is not sure?", [
    [("Qwen3 0.6B", "+ LoRA"), ("640 MB", "8-bit"), ("1.3 s", "on a 20-core lab box")],
    [("98.9 %", "on its test set"), ("Short prompts", "770 to 240 tokens"), ("Smallest", "that holds both jobs")],
], ["Taught by Haiku, with Sonnet on the near-ties. Answers the Localize calls of its box."])
y = card(y, "3", "Screen namer", "Name a screen Localize does not know", [
    [("SmolVLM-256M", "a vision model"), ("365 MB", "8-bit"), ("4.7 s", "on 4 cores")],
    [("84 % answered", "only when sure"), ("98.3 % right", "on those"), ("One box", "for every server")],
], ["Taught by Sonnet on 3,621 lab screenshots, Opus judging the disagreements."])
y = card(y, "•", "What moved the score", "Each round one GPU run: better labels, not a bigger model", [
    [("Still screens only", "freeze"), ("Second teacher", "on the unsure rows"), ("Fewer subtitles", "freeze")],
    [("Merge kinds", "the teachers mix up"), ("Own mistakes", "judged by Opus"), ("Not bigger", "500M was not better")],
])
y = card(y, "•", "Lessons", "What we would do again", [
    [("Smaller is enough", "freeze needs no LLM"), ("Cut calls first", "then make it small")],
    [("Answer when sure", "94 % becomes 98 %"), ("Truth is not perfect", "judges agree 89 %")],
], last=True)

y += 20
box(60, y, 1080, 120, "#2a2418", GOLD, 22, 2)
t(600, y + 50, "Taught by the cloud models. Answers only when sure.", 32, GOLD, 700, "middle")
t(600, y + 90, "The rest goes to the cloud model, as before.", 21, TXT, 400, "middle")
t(600, y + 166, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
H = y + 210
body = o
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Our own small models, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
t(60, 100, "AI IN THE LAB", 20, GOLD, 500, sp=3)
t(60, 180, "Our own small models", 62, TXT, 700)
t(60, 236, "How we trained them, one per use case.", 26, MUT, 400, maxw=1080)
t(60, 274, "Small, fast, free, and on our own boxes.", 26, MUT, 400, maxw=1080)
o += body
o.append('</svg>')
open("docs/img/small-models.svg", "w").write("\n".join(o))

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
print(f"docs/img/small-models.svg written, {W}x{H}, {len(checks)} labels fit")
