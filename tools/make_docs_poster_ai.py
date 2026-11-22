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
y = card(y, "•", "The short version", "Every place the tool asks an AI model, in the order of the doc. Each one is detailed below.", [
    [("1 · Throw away false alarms", "a person only looks at real problems"), ("2 · Name what is on screen", "when the fingerprint is not sure")],
    [("3 · Write tests and scripts", "from plain words: Atlas and Forge"), ("4 · Help people", "chat, voice, the docs Ask box")],
    [("5 · Live TV companion", "opt-in per device"), ("6 · Showcases: games and the drone", "the same look and press loop")],
    [("7 · Model tests", "not a product feature: they change nothing in the product")],
], ["Used: the answer changes what the tool does. Logged: a shadow answer,", "kept to measure the model, nothing changes."])
y = card(y, "•", "Cost", "All AI calls of the lab server, 30 days", [
    [("16.72 USD", "all AI calls, 30 days"), ("0 USD a call", "flat-rate plan (MiniMax)"), ("0 USD", "small models on the host"), ("Paid calls", "Claude Haiku and Sonnet")],
], ["Paid calls are the fallback when the flat plan fails, plus a few that need a strong model."])
y = card(y, "•", "Where it runs", "Three places", [
    [("Cloud models", "through the AI router"), ("Small models", "on the host CPU"), ("The owner's PC", "LM Studio, local Qwen models")],
], ["Settings → AI picks the model and a fallback for each usage key.", "Every cloud call is logged and shown on Monitoring → AI usage."])
y = card(y, "•", "What is NOT AI", "People often think it is", [
    [("Localize", "which screen is this? picture fingerprints"), ("KPI load times, zap times", "a clock and the screen fingerprint")],
    [("Freeze, black screen, no audio", "pixel and sound measurements on the host"), ("Navigation (goto)", "the navigation tree, shortest path")],
    [("Repair of a tree", "after an app update: walks every node, no model"), ("Screen memory for alerts", "a frame fingerprint judged harmless")],
], ["AI only helps Localize on a doubtful match (use case 2)."])
y = card(y, "1", "Throw away false alarms", "AI says this is noise, so a person only looks at real problems", [
    [("Alert triage", "USED · real or noise?"), ("Freeze triage", "LOGGED (shadow) · keep / dismiss"), ("Freeze word classifier", "measured, not wired yet")],
    [("Script result analysis", "USED · real app bug, or noise?"), ("Sherlock verdict", "LOGGED (shadow)"), ("Test Prompt", "after a failure · LOGGED (shadow)")],
], ["A frozen menu, a phone that went to sleep, a test that failed because the lab network blinked."])
y = card(y, "2", "Name what is on screen", "When the fingerprint is not sure, read a channel banner, read a score", [
    [("Localize second opinion", "mostly LOGGED · USED 2.6 %"), ("Text check second opinion", "LOGGED (shadow)")],
    [("Title translation", "USED · on the host CPU"), ("Channel banner", "USED · after a zap"), ("Unknown screens", "USED to propose names")],
    [("Screenshot description", "USED · for an AI agent"), ("OCR", "USED · Tesseract on the host CPU")],
], ["Localize second opinion is used only to confirm a low-confidence answer."])
y = card(y, "3", "Write tests and scripts", "From plain words, with the Atlas and Forge assistants", [
    [("Forge", "scripts, test cases, trees"), ("Atlas, test case skill", "test cases in the chat")],
    [("Test plan", "the steps from a goal"), ("Exploration, DOM", "reads a new app screen")],
], ["All USED. A person reviews what Forge builds."])
y = card(y, "4", "Help people", "Questions about the tool, the screen or a run", [
    [("Atlas", "the assistant in the app"), ("Voice", "spoken commands, answers"), ("Docs Ask", "the public docs question box")],
    [("Masterchief", "fleet chat, asks before acting"), ("Fleet health report", "daily summary of the fleet")],
    [("Ask AI on a frame", "a free question on the picture"), ("MCP", "the caller's own model, 0 USD for us")],
], ["All USED. Masterchief acts only with a confirm card."])
y = card(y, "5", "Live TV companion", "Opt-in per device", [
    [("Identify", "what is on: the programme"), ("Live read", "the score bug of a match"), ("Speech to text", "on the host CPU")],
    [("Facts, fact check, digest, gates", "about the programme, a claim, the news"), ("Caption translation", "best effort")],
], ["All USED on the companion panel."])
y = card(y, "6", "Showcases: games and the drone", "They prove the same look and press loop on harder screens", [
    [("Clash of Clans player", "one screenshot in, one tap out"), ("Pokémon strategist", "long-term plan and lessons")],
    [("2048 player", "picks each move"), ("League game review", "what went wrong after a game")],
    [("League small classifiers", "on the host CPU"), ("Drone", "target in the camera?"), ("Wakfu bot", "scripts and a lessons file")],
])
y = card(y, "7", "Model tests (not a product feature)", "Benchmarks: the same questions asked to several models to pick a route", [],
         ["They change nothing in the product."])
y = card(y, "•", "Freeze discard", "From a paid model to a 0.25 ms classifier", [
    [("9,861", "alerts avoided in 7 days"), ("1.7 s", "Haiku, today's paid hop"), ("0.25 ms", "the word classifier")],
    [("2 MB", "any host CPU, no GPU"), ("0 USD", "per call"), ("Retrains", "every night, not from itself")],
], ["Measured, not wired yet. See the poster Freeze: menu or stuck video?"], last=True)

y += 20
box(60, y, 1080, 120, "#2a2418", GOLD, 22, 2)
t(600, y + 50, "AI only where nothing simpler can decide.", 32, GOLD, 700, "middle")
t(600, y + 90, "Every answer is logged, so you can measure what AI really adds.", 21, TXT, 400, "middle")
t(600, y + 166, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
H = y + 210
body = o
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Where VirtualPyTest uses AI, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
t(60, 100, "AI IN THE LAB", 20, GOLD, 500, sp=3)
t(60, 180, "Where VirtualPyTest uses AI", 62, TXT, 700)
t(60, 236, "Most of the lab needs no AI at all: a screen is recognised by its fingerprint,", 24, MUT, 400, maxw=1080)
t(60, 272, "a key is a key, a load time is a clock. AI is asked only where that is not enough.", 24, MUT, 400, maxw=1080)
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
