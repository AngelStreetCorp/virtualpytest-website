#!/usr/bin/env python3
"""Writes docs/img/ai-use-cases.svg (Docs poster: where VirtualPyTest uses AI and why; source: docs/AI-USE-CASES.md of the product repo, numbers checked 2026-11-22). Run from the repo root."""
W, H = 1200, 3320
BG, PANEL, LINE, TXT, MUT, GOLD = "#161616", "#212121", "#3a3a3a", "#f2f2f2", "#a8a8a8", "#e0a96d"
F = "Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
o = []
def t(x, y, s, size=28, fill=TXT, w=500, anchor="start", sp=0):
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{s}</text>')
def box(x, y, w, h, fill=PANEL, stroke=LINE, r=22, sw=2):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def arrow(x, y1, y2):
    o.append(f'<path d="M{x} {y1}V{y2-12}" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/><path d="M{x-12} {y2-18}L{x} {y2-4}L{x+12} {y2-18}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
def chips(x, y, items, w, gap=16, h=70):
    for i, (a, b) in enumerate(items):
        cx = x + i * (w + gap)
        box(cx, y, w, h, fill="#2a2a2a", r=16)
        t(cx + w / 2, y + 30, a, 22, TXT, 600, "middle")
        t(cx + w / 2, y + 55, b, 16, MUT, 400, "middle")
def layer(y, n, title, sub, h):
    box(60, y, 1080, h)
    o.append(f'<circle cx="112" cy="{y+52}" r="26" fill="{GOLD}"/>')
    t(112, y + 61, n, 26, "#1a1a1a", 700, "middle")
    t(156, y + 50, title, 34, TXT, 700)
    t(156, y + 82, sub, 21, MUT, 400)

GREEN = "#4ade80"
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ti"><title id="ti">Where VirtualPyTest uses AI, in one image</title>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
t(60, 100, "AI IN THE LAB", 20, GOLD, 500, sp=3)
t(60, 180, "Where VirtualPyTest uses AI", 62, TXT, 700)
t(60, 236, "Most of the lab needs no AI. A model is asked only when a check is not sure.", 27, MUT, 400)
t(60, 276, "Four use cases, mostly free. Numbers checked on 22 Nov 2026.", 24, MUT, 400)

def panel(y, n, title, sub, items, note, w=240, gap=18, last=False):
    layer(y, n, title, sub, 250)
    chips(90, y + 112, items, w, gap)
    t(600, y + 222, note, 19, MUT, 400, "middle")
    if not last:
        arrow(600, y + 250, y + 300)

panel(330, "•", "The use cases in one look", "Each one is detailed below",
      [("No AI", "0 · most of the lab"), ("False alarms", "1 · set aside"), ("Name screens", "2 · when unsure"), ("Write tests", "3 · plain words"), ("Help people", "4 · chat, voice, docs")],
      "Use cases 1 to 4 are the only places a model is asked.", w=190, gap=17)
panel(640, "0", "Most of it needs no AI", "A fingerprint or a clock is enough",
      [("Fingerprint", "which screen is this"), ("Clocks", "load and zap times"), ("Pixels", "freeze, black, silence"), ("Tree", "shortest path"), ("Repair", "fix after an update")],
      "Localize, KPIs, detection, navigation and repair use no model at all.", w=190, gap=17)
panel(950, "1", "Use case 1: throw away false alarms", "A person only looks at real problems",
      [("Alert triage", "real or noise"), ("Script analysis", "bug or lab noise"), ("Freeze words", "menu or stuck video"), ("Screen memory", "judged harmless before")],
      "A frozen menu, a sleeping phone, a network blink: set aside.")
panel(1260, "2", "Use case 2: name what is on screen", "When the fingerprint is not sure",
      [("Second opinion", "a doubtful match"), ("Channel banner", "read after a zap"), ("Unknown screens", "named in the background"), ("Reading words", "on the host, no cloud")],
      "The second opinion on a match is mostly logged: it changes nothing yet.")
panel(1570, "3", "Use case 3: write tests and scripts", "From plain words",
      [("Forge", "scripts, tests, trees"), ("Atlas", "tests in the chat"), ("Test plan", "steps from a goal"), ("Explore", "reads a new app")],
      "A person reviews what is written.")
panel(1880, "4", "Use case 4: help people", "Questions about the tool, a screen or a run",
      [("Atlas chat", "ask, drive, run"), ("Voice", "spoken commands"), ("Docs Ask", "the public question box"), ("Fleet report", "a daily summary")],
      "Plus showcases: game bots and the drone prove the same look-and-press loop.")
panel(2190, "•", "Where it runs", "Three places",
      [("Cloud models", "one per use case, plus a fallback"), ("The host CPU", "speech, OCR, titles"), ("Your own PC", "low-priority use cases")],
      "Every cloud call is logged and shown on the AI usage page.", w=320, gap=30)
panel(2500, "•", "What it costs", "The whole lab, the last 30 days",
      [("16.72 USD", "all AI calls"), ("0 USD", "flat plan and host models"), ("Paid calls", "fallback and hard cases"), ("Logged answers", "are only measured")],
      "Cheap on purpose: no AI first, small models next, strong models last.")
panel(2810, "•", "The newest: freeze alerts", "Menu or stuck video, without a language model",
      [("9,861", "alerts avoided in 7 days"), ("1.7 s", "the paid check today"), ("0.25 ms", "the word model, measured"), ("Learns", "every night, never alone")],
      "See the poster Freeze: menu or stuck video? The word model is measured, not wired yet.", last=True)

box(60, 3120, 1080, 120, "#2a2418", GOLD, 22, 2)
t(600, 3170, "AI only where nothing simpler can decide.", 32, GOLD, 700, "middle")
t(600, 3210, "Every answer is logged, so you can measure what AI really adds.", 21, TXT, 400, "middle")
t(600, 3286, "virtualpytest.com · open source, AGPLv3", 20, MUT, 400, "middle")
o.append('</svg>')
open("docs/img/ai-use-cases.svg", "w").write("\n".join(o))
