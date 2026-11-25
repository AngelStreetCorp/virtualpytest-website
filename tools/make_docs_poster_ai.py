#!/usr/bin/env python3
"""Writes docs/img/ai-use-cases.svg (Docs poster "Where VirtualPyTest uses AI"): one step flow per use case, a badge
on each step that asks a model.

Source: the section "Step by step" of docs/ai/AI-USE-CASES.md in the product repo. Every step label and caption is
that section's words; change the doc first, then this file. Help people and Live TV companion are lists (no numbers,
no rail), because the doc says they are not a sequence. Run from the repo root.
Badges: "ai" = a cloud model answers and the answer is used, "shadow" = a cloud model answers, logged only,
"own" = our own small model, "host" = a small model on the host CPU, none = a rule, a clock or a measurement.
Every text is measured with DejaVu Sans (the font headless Chromium falls back to); the script fails on an overflow.
"""
import os, sys
from PIL import ImageFont

W = 1200
BG, PANEL, LINE, TXT, MUT, GOLD, CHIP = "#161616", "#212121", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d", "#2a2a2a"
TEAL, GOLD_BG, TEAL_BG = "#6dc5c9", "#2a2418", "#18272a"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
FONTS = {True: "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", False: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"}
o, bad, nlabels = [], [], 0

def width(s, size, bold, sp=0):
    return ImageFont.truetype(FONTS[bold], size).getlength(s) + sp * len(s)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0, maxw=None):
    global nlabels
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{esc(s)}</text>')
    if maxw:
        nlabels += 1
        wpx = width(s, size, w >= 600, sp)
        if wpx > maxw:
            bad.append(f"{wpx:.0f} > {maxw:.0f} px: {s}")

def box(x, y, w, h, fill=PANEL, stroke=LINE, r=22, sw=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

# badge kind -> (text, text colour, fill, stroke, dashed)
BADGES = {
    "ai": ("AI", "#1a1a1a", GOLD, GOLD, False),
    "shadow": ("AI · LOGGED ONLY", GOLD, "none", GOLD, True),
    "own": ("OUR MODEL", "#10201f", TEAL, TEAL, False),
    "host": ("HOST MODEL", TEAL, "none", TEAL, False),
}
BH = 26

def badge_w(kind):
    return round(width(BADGES[kind][0], 14, True, 1) + 26)

def badge(x, y, kind):
    """Draws the pill with its left edge at x, centred on y. Returns its width."""
    s, col, fill, stroke, dashed = BADGES[kind]
    w = badge_w(kind)
    box(x, y - BH // 2, w, BH, fill, stroke, 13, 2, "5 4" if dashed else "")
    t(x + w / 2, y + 5, s, 14, col, 700, "middle", 1)
    return w

ROW_X, ROW_W, ROW_H, PITCH = 90, 1020, 44, 54
LABEL_X, CAP_X, LABEL_MAX = 148, 470, 310

def step_rows(y, steps, numbered=True):
    """steps: (label, caption, [badge kinds]). One row per step, joined by a rail when numbered. Returns the y under the rows."""
    for i, (label, cap, kinds) in enumerate(steps):
        ai, own = any(k in ("ai", "shadow") for k in kinds), any(k in ("own", "host") for k in kinds)
        fill, stroke = (GOLD_BG, GOLD) if ai else (TEAL_BG, TEAL) if own else (CHIP, LINE)
        if i and numbered:
            o.append(f'<path d="M{ROW_X+28} {y-(PITCH-ROW_H)}V{y}" stroke="{LINE}" stroke-width="3"/>')
        box(ROW_X, y, ROW_W, ROW_H, fill, stroke, 12, 1.5, "6 5" if kinds == ["shadow"] else "")
        cy = y + ROW_H // 2
        if numbered:
            o.append(f'<circle cx="{ROW_X+28}" cy="{cy}" r="13" fill="{stroke if (ai or own) else "#4a4a4a"}"/>')
            t(ROW_X + 28, cy + 5, str(i + 1), 15, "#1a1a1a" if (ai or own) else TXT, 700, "middle")
        else:
            o.append(f'<circle cx="{ROW_X+28}" cy="{cy}" r="5" fill="{stroke if (ai or own) else "#6a6a6a"}"/>')
        t(LABEL_X, cy + 7, label, 20, TXT, 600, maxw=LABEL_MAX)
        bx = ROW_X + ROW_W - 12
        for k in reversed(kinds):
            bx -= badge_w(k)
            badge(bx, cy, k)
            bx -= 8
        t(CAP_X, cy + 6, cap, 16, MUT, 400, maxw=bx - 8 - CAP_X)
        y += PITCH
    return y - (PITCH - ROW_H)

total = {"steps": 0, "ai": 0, "own": 0, "none": 0}

def card(y, n, title, sub, flows, numbered=True):
    """flows: list of (start line in gold caps, steps). Returns the y of the next card."""
    steps_all = [s for _, st in flows for s in st]
    n_ai = sum(1 for s in steps_all if any(k in ("ai", "shadow") for k in s[2]))
    total["steps"] += len(steps_all); total["ai"] += n_ai
    total["own"] += sum(1 for s in steps_all if any(k in ("own", "host") for k in s[2]))
    total["none"] += sum(1 for s in steps_all if not s[2])
    h = 104 + sum(40 + len(st) * PITCH - (PITCH - ROW_H) + 22 for _, st in flows) + 4
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    counter = f"AI in {n_ai} of {len(steps_all)} " + ("steps" if numbered else "items")
    t(1110, y + 48, counter, 19, GOLD, 600, "end")
    t(156, y + 50, title, 34, TXT, 700, maxw=1110 - width(counter, 19, True) - 24 - 156)
    t(156, y + 82, sub, 20, MUT, 400, maxw=950)
    fy = y + 104
    for start, st in flows:
        t(ROW_X, fy + 22, start.upper(), 15, GOLD, 600, sp=1.5, maxw=ROW_W)
        fy = step_rows(fy + 40, st, numbered) + 22
    return y + h + 28

def chips(y, items, h=70):
    n = len(items); w = (1020 - (n - 1) * 18) / n
    for i, (a, b) in enumerate(items):
        cx = 90 + i * (w + 18)
        box(round(cx), y, round(w), h, CHIP, LINE, 16)
        t(round(cx + w / 2), y + 30, a, 21, TXT, 600, "middle", maxw=w - 20)
        t(round(cx + w / 2), y + 55, b, 16, MUT, 400, "middle", maxw=w - 16)

AI, SH, OWN, HOST = ["ai"], ["shadow"], ["own"], ["host"]
CARDS = [
    ("1", "Discard incidents", "So a person only looks at real problems", [
        ("A freeze, black screen or no audio alert", [
            ("Host raises the alert", "pixel and sound measurements on the host", []),
            ("Screen memory", "a frame judged harmless before: discarded, no model", []),
            ("OCR", "reads the words on the first and last frame", []),
            ("Freeze word classifier", "a sure menu is discarded, in 0.25 ms", OWN),
            ("Alert triage", "a vision model judges the rest: real or noise?", AI),
            ("Freeze triage", "still screen by design or a real freeze?", SH),
            ("Alert kept or discarded", "a person only looks at the real ones", []),
        ])]),
    ("2", "Discard scripts", "Failed runs caused by the lab are set aside", [
        ("A test run failed", [
            ("Sherlock signature table", "a failure already judged: no model, logged only", []),
            ("Sherlock verdict", "a small decision model, used when 0.9 sure or more", AI),
            ("Script result analysis", "else the LLM reads the report, logs, screenshots", AI),
            ("Verdict on the run", "real app bug, or noise: lab network, device asleep", []),
            ("Test Prompt", "app failure, stale test or retry?", SH),
        ])]),
    ("3", "Classify unknown screens", "When the fingerprint is not sure", [
        ("Localize: which screen is this?", [
            ("Fingerprint", "picture fingerprints compared with the stored screens", []),
            ("Title translation", "screen titles compared in English", HOST),
            ("Localize second opinion", "only on a doubtful match: a tie, low confidence", OWN + AI),
            ("Screen or unknown", "without a sure yes the answer becomes unknown", []),
        ]),
        ("Channel banner, after every zap", [
            ("OCR on fixed crops", "reads programme, times and number, in 0.3 s", []),
            ("Line-up of the box", "the number gives the name, once two answers agree", []),
            ("Logo table", "a known logo gives the name", []),
            ("A new logo", "the AI reads a logo once, then never again", AI),
        ]),
        ("Unknown screens: a screen Localize could not name", [
            ("Seen 5 times or more", "only then is a name asked for", []),
            ("Our screen namer", "answers only when sure", OWN),
            ("Cloud model", "names the rest", AI),
            ("A person decides", "accepts, merges or dismisses the proposed name", []),
        ])]),
    ("4", "Create scripts", "From plain words. No code, no Python.", [
        ("A request in plain words", [
            ("Exploration", "reads a new app screen, when a crawl runs", AI),
            ("Test plan", "plans the steps of a test from a goal", AI),
            ("Forge or Atlas", "builds the script, test case or navigation tree", AI),
            ("Saved", "a virtual script, a test case or a tree", []),
            ("A person reviews", "the result is checked by a person", []),
        ])]),
    ("5", "Help people", "Questions about the tool, a screen or a run", [
        ("Not a sequence: each one answers on its own", [
            ("Atlas", "the assistant in the app", AI),
            ("Voice", "spoken commands and spoken answers", AI),
            ("Ask AI", "questions about the docs; the Ask cache first", AI),
            ("Masterchief", "fleet chat and scheduled checks; asks first", AI),
            ("Fleet health report", "a daily summary of the fleet", AI),
            ("MCP", "external AI tools, with their own model", []),
        ])]),
    ("6", "Live TV companion", "Opt-in per device", [
        ("Not a sequence: each one runs on its own", [
            ("Identify", "what is on: screen type, programme", AI),
            ("Live read", "re-reads a fixed crop: the score, the speaker name", AI),
            ("Facts and fact check", "a web search about the programme or a claim", AI),
            ("Speech to text", "live transcript of the audio", HOST),
            ("Caption translation", "best effort, else the source text is shown", AI),
        ])]),
]
LISTS = {"5", "6"}

y = 520                       # the legend card is drawn last, once the steps are counted
for c in CARDS:
    y = card(y, *c, numbered=c[0] not in LISTS)

box(60, y, 1080, 196)
t(90, y + 50, "What is NOT AI", 30, TXT, 700)
t(90, y + 80, "People often think it is. No model at all.", 20, MUT, 400)
chips(y + 104, [("Load and zap times", "a clock and the fingerprint"), ("Navigation", "the shortest path in the tree"), ("Repair of a tree", "rules, after an app update")])
y += 196 + 28
box(60, y, 1080, 196)
t(90, y + 50, "Cost", 30, TXT, 700)
t(90, y + 80, "All AI calls, 30 days", 20, MUT, 400)
chips(y + 104, [("16.72 USD", "all AI calls"), ("0 USD a call", "flat-rate plan"), ("0 USD", "small models, our boxes"), ("Paid calls", "only as a backup")])
y += 196 + 34
box(60, y, 1080, 120, GOLD_BG, GOLD, 22, 2)
t(600, y + 50, "AI only where nothing simpler can decide.", 32, GOLD, 700, "middle")
t(600, y + 90, "Every cloud call is logged.", 21, TXT, 400, "middle")
t(600, y + 166, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
H = y + 210

body, o = o, []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Where VirtualPyTest uses AI, step by step</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
t(60, 100, "AI IN THE LAB", 20, GOLD, 500, sp=3)
t(60, 180, "Where VirtualPyTest uses AI", 62, TXT, 700)
t(60, 236, "Each use case, step by step. A badge marks the steps that ask a model.", 26, MUT, 400, maxw=1080)
# legend card
ly = 280
box(60, ly, 1080, 212)
t(90, ly + 46, "How to read", 30, TXT, 700)
t(1110, ly + 44, f"{total['ai']} of {total['steps']} steps ask a cloud model. {total['none']} use no model.", 18, GOLD, 600, "end", maxw=800)
LEG = [("ai", "a cloud model answers"), ("own", "our own small model, 0 USD"),
       ("shadow", "the answer changes nothing"), ("host", "a small model on the host CPU")]
for i, (k, txt) in enumerate(LEG):
    lx, lyy = 90 + (i % 2) * 519, ly + 70 + (i // 2) * 48
    box(lx, lyy, 501, 38, CHIP, LINE, 12, 1.5)
    bw = badge(lx + 10, lyy + 19, k)
    t(lx + 10 + bw + 12, lyy + 25, txt, 17, TXT, 400, maxw=501 - bw - 32)
t(90, ly + 192, "No badge: a rule, a clock or a measurement. No model.", 18, MUT, 400, maxw=1020)
o += body
o.append('</svg>')
out = "docs/img/ai-use-cases.svg"
open(out, "w").write("\n".join(o))
if bad:
    sys.exit("text wider than its box with the fallback font:\n  " + "\n  ".join(bad))
print(f"{out} written, {W}x{H}, {nlabels} labels fit, totals {total}")
