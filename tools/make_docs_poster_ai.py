#!/usr/bin/env python3
"""Writes docs/img/ai-use-cases.svg (Docs poster "Where VirtualPyTest uses AI").

Source: docs/ai/AI-USE-CASES.md of the product repo. The poster mirrors that doc one to one: same sections, same
order, the doc's section titles and item names word for word. No date anywhere on the poster.
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
y = card(y, "•", "Overview", "Five use cases. Details below.", [
    [("1 · Discard false alarms", "only real problems reach you"), ("2 · Name what is on screen", "when the fingerprint is unsure")],
    [("3 · Write tests and scripts", "from plain words"), ("4 · Help people", "chat, voice, docs")],
    [("5 · Live TV companion", "opt-in per device")],
])
y = card(y, "•", "Cost", "All AI calls, 30 days", [
    [("16.72 USD", "all AI calls"), ("0 USD a call", "flat-rate plan"), ("0 USD", "small models on the host"), ("Paid calls", "only as a backup")],
], ["Most answers cost nothing."])
y = card(y, "•", "Where it runs", "Three places", [
    [("Cloud models", "chosen per use case"), ("Small models", "on the host"), ("Your own PC", "for low-priority work")],
], ["Every cloud call is logged."])
y = card(y, "•", "What is NOT AI", "People often think it is", [
    [("Localize", "which screen is this?"), ("Load and zap times", "a clock")],
    [("Freeze, black screen, no audio", "measured on the host"), ("Navigation", "the shortest path in the tree")],
    [("Repair of a tree", "after an app update"), ("Screen memory", "a screen judged harmless once")],
], ["AI only helps Localize when a match is doubtful."])
y = card(y, "1", "Discard false alarms", "So a person only looks at real problems", [
    [("Alert triage", "real or noise?"), ("Freeze triage", "menu or stuck video?"), ("Freeze word classifier", "reads the words only")],
    [("Script result analysis", "app bug or lab noise?"), ("Test Prompt", "app failure or stale test?")],
], ["A frozen menu, a sleeping phone, a network blink."])
y = card(y, "2", "Name what is on screen", "When the fingerprint is not sure", [
    [("Localize second opinion", "a doubtful match"), ("Text check second opinion", "a close score")],
    [("Channel banner", "read after a zap"), ("Unknown screens", "named for you"), ("OCR", "reads the words on screen")],
], ["It only confirms a doubtful answer."])
y = card(y, "3", "Write tests and scripts", "From plain words", [
    [("Forge", "scripts, tests, trees"), ("Atlas", "tests in the chat")],
    [("Test plan", "the steps from a goal"), ("Exploration", "reads a new app")],
], ["A person reviews what is written."])
y = card(y, "4", "Help people", "Questions about the tool, a screen or a run", [
    [("Atlas", "the assistant in the app"), ("Voice", "spoken commands"), ("Ask AI", "questions about the docs")],
    [("Masterchief", "fleet chat, asks first"), ("Fleet health report", "a daily summary")],
])
y = card(y, "5", "Live TV companion", "Opt-in per device", [
    [("Identify", "what is on now"), ("Live read", "the score of a match"), ("Speech to text", "on the host")],
    [("Facts and fact check", "about the programme"), ("Caption translation", "best effort")],
])
y = card(y, "•", "Freeze discard", "From a paid model to a 0.25 ms classifier", [
    [("9,861", "alerts avoided in 7 days"), ("1.7 s", "the paid check today"), ("0.25 ms", "the word classifier")],
    [("2 MB", "any host, no GPU"), ("0 USD", "per call"), ("Retrains", "every night")],
], ["See the poster Freeze: menu or stuck video?"], last=True)

y += 20
box(60, y, 1080, 120, "#2a2418", GOLD, 22, 2)
t(600, y + 50, "AI only where nothing simpler can decide.", 32, GOLD, 700, "middle")
t(600, y + 90, "Every AI answer is logged and counted.", 21, TXT, 400, "middle")
t(600, y + 166, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
H = y + 210
body = o
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Where VirtualPyTest uses AI, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
t(60, 100, "AI IN THE LAB", 20, GOLD, 500, sp=3)
t(60, 180, "Where VirtualPyTest uses AI", 62, TXT, 700)
t(60, 236, "Most of the lab needs no AI.", 26, MUT, 400, maxw=1080)
t(60, 274, "AI is asked only where nothing simpler can decide.", 26, MUT, 400, maxw=1080)
o += body
o.append('</svg>')
open("docs/img/ai-use-cases.svg", "w").write("\n".join(o))

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
print(f"docs/img/ai-use-cases.svg written, {W}x{H}, {len(checks)} labels fit")
