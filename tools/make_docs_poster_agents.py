#!/usr/bin/env python3
"""Writes docs/img/ai-agents.svg, the Docs poster "Meet our AI agents". Run from the repo root:
    python3 tools/make_docs_poster_agents.py
It mirrors docs/ai/AI-AGENTS.md of the product repo (same sections, same words); no tool or agent totals.
Dark only (DOCS_POSTERS.md). Fails when a text is wider than its box in DejaVu Sans, headless Chromium's font.
"""
from PIL import ImageFont

THEMES = {
    'dark': dict(BG='#161616', PANEL='#212121', CHIP='#2a2a2a', LINE='#3a3a3a', TXT='#f2f2f2', MUT='#a8a8a8',
                 GOLD='#e0a96d', BAND='#2a2418', ON_GOLD='#1a1a1a'),
}
FONT = 'Geist,Inter,system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif'
MONO = 'ui-monospace,Menlo,DejaVu Sans Mono,monospace'
TTF = '/usr/share/fonts/truetype/dejavu/DejaVuSans{}.ttf'
W = 1200

# (name, one line, [(chip, caption)], what sets it apart)
AGENTS = [
    ('Atlas', 'Does the everyday jobs itself',
     [('Drive devices', 'keys, screens'), ('Run tests', 'and read results'), ('Search docs', 'answers, videos'),
      ('Open a page', 'beside the chat')], 'Dashboards too: it builds them from your data.'),
    ('Forge', 'Writes tests from plain words',
     [('Scripts', 'virtual scripts'), ('Test cases', 'build and run'), ('App maps', 'screens, keys'),
      ('Campaigns', 'groups of tests')], 'Atlas hands it the scripts to write.'),
    ('Sherlock', 'Why did the run fail?',
     [('Read the run', 'results, status'), ('Real bug', 'kept'), ('Lab problem', 'set aside'),
      ('Correct it', 'the verdict')], 'In the background too, when turned on.'),
    ('Nightwatch', 'What happened on this device?',
     [('Explain alerts', 'what and when'), ('Real', 'a true incident'), ('Expected', 'meant to happen'),
      ('False alarm', 'nothing wrong')], 'Sorts new alerts in the background, when turned on.'),
    ('Masterchief', 'Looks after the machines',
     [('Disk', 'what fills it'), ('Logs', 'what went wrong'), ('Services', 'state, restart'),
      ('Confirm card', 'before a change')], 'Changes machines only after your Confirm.'),
]
OVERVIEW = [('Atlas', 'the built-in chat'), ('Forge', 'writes tests'), ('Sherlock', 'failed runs'),
            ('Nightwatch', 'alerts'), ('Masterchief', 'machines')]


def draw(theme):
    c = THEMES[theme]
    o = []

    def fit(s, size, bold, room, mono=False):
        face = 'Mono' if mono else ('-Bold' if bold else '')
        font = ImageFont.truetype(TTF.format(face), size)
        if font.getlength(s) > room:
            raise SystemExit(f'too wide ({font.getlength(s):.0f} > {room}): {s}')

    def t(x, y, s, size, fill, weight=500, anchor='start', room=1060, family=FONT, sp=0):
        fit(s, size, weight >= 600, room, family == MONO)
        s = s.replace('&', '&amp;')
        o.append(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{sp}">{s}</text>')

    def box(x, y, w, h, fill=c['PANEL'], stroke=c['LINE'], r=22):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" '
                 f'stroke-width="2"/>')

    def chip(x, y, w, title, caption, size=21):
        box(x, y, w, 70, c['CHIP'], r=16)
        t(x + w / 2, y + 31, title, size, c['TXT'], 600, 'middle', w - 12)
        t(x + w / 2, y + 56, caption, 16, c['MUT'], 400, 'middle', w - 12)

    def chips(y, items):
        gap = 18
        w = (1020 - gap * (len(items) - 1)) / len(items)
        for i, (a, b) in enumerate(items):
            chip(90 + i * (w + gap), y, w, a, b)

    def panel(y, number, title, sub, h):
        box(60, y, 1080, h)
        o.append(f'<circle cx="112" cy="{y + 52}" r="26" fill="{c["GOLD"]}"/>')
        t(112, y + 61, number, 26, c['ON_GOLD'], 700, 'middle', 40)
        t(156, y + 50, title, 34, c['TXT'], 700, room=960)
        t(156, y + 82, sub, 21, c['MUT'], 400, room=960)

    def arrow(y):
        o.append(f'<path d="M600 {y}V{y + 34}" stroke="{c["GOLD"]}" stroke-width="4" stroke-linecap="round"/>'
                 f'<path d="M588 {y + 28}L600 {y + 42}L612 {y + 28}" fill="none" stroke="{c["GOLD"]}" '
                 f'stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')

    t(60, 100, 'AI IN THE LAB · AGENTS', 20, c['GOLD'], sp=3)
    t(60, 180, 'Meet our AI agents', 70, c['TXT'], 700)
    t(60, 236, 'We built them into VirtualPyTest. Each has one job.', 29, c['MUT'], 400)
    t(60, 278, 'Ask Atlas: it brings in a specialist when one is needed.', 25, c['GOLD'], 600)

    # overview: Atlas on top, a line to every agent it routes to (solid: hands over itself; dotted: its button)
    box(60, 320, 1080, 250)
    chip(450, 344, 300, *OVERVIEW[0])
    for i, (name, job) in enumerate(OVERVIEW[1:]):
        x, start = 90 + i * 258, 495 + i * 70
        dash = '' if name == 'Forge' else ' stroke-dasharray="2 11"'
        o.append(f'<path d="M{start} 416C{start} 452 {x + 123} 440 {x + 123} 476" fill="none" stroke="{c["GOLD"]}" '
                 f'stroke-width="4" stroke-linecap="round"{dash}/>')
        chip(x, 478, 246, name, job)
    arrow(578)

    y = 630
    for number, (name, line, items, apart) in enumerate(AGENTS, 1):
        panel(y, str(number), name, line, 252)
        chips(y + 112, items)
        t(600, y + 224, apart, 21, c['GOLD'], 600, 'middle')
        if number < len(AGENTS):
            arrow(y + 260)
        y += 312

    t(600, y + 22, 'virtualpytest.com · open source, AGPLv3', 20, c['MUT'], 400, 'middle')
    height = y + 56
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}" '
            f'role="img"><title>Meet our AI agents, in one image</title><rect width="{W}" height="{height}" '
            f'fill="{c["BG"]}"/>')
    return head + '\n' + '\n'.join(o) + '\n</svg>\n', height


def main():
    svg, height = draw('dark')
    with open('docs/img/ai-agents.svg', 'w', encoding='utf-8') as fh:
        fh.write(svg)
    print('docs/img/ai-agents.svg', W, height)


if __name__ == '__main__':
    main()
