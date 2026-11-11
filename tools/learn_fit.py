#!/usr/bin/env python3
"""Phone-fit check for the Learn player: every lesson fits one phone screen, every title stays on one line, no card
throws a page error (a WAAPI "Offsets must be monotonically non-decreasing" error stops a card).

    python3 tools/learn_fit.py [site-dir, default: the repo root] [viewport height, default 740] [--lang de]

What "fits" means: the lesson block (`main.lx`: picker, animation stage, text, sticky Prev/Next) is at most the
viewport height. The site navbar, device strip and footer around it are page chrome that scrolls away; counting them
(`document.scrollHeight - innerHeight`, the check before 2026-11-11) made all 50 lessons fail by a constant ~400 px.
Fonts are awaited before measuring. Exit code: 0 all good, 1 a lesson too tall / title wraps / card broken.
"""
import socket, subprocess, sys, time
from playwright.sync_api import sync_playwright

LESSON_H = "Math.round(document.querySelector('main.lx').getBoundingClientRect().height)"
TITLE_WRAPS = "(e => e.offsetHeight > parseFloat(getComputedStyle(e).fontSize) * 1.5)(document.getElementById('title'))"
CARD_BROKEN = "(f => !(f.contentWindow && typeof f.contentWindow.__seek === 'function'))(document.getElementById('card'))"


def check(site, vh=740, lang='', width=390):
    """-> (ids, tall {id: px over}, wrap [ids], broken [ids], page errors)"""
    with socket.socket() as s:      # a free port: other sessions run http servers on the usual ones
        s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
    srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=site,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={'width': width, 'height': vh})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(f'http://127.0.0.1:{port}/learn/{"?lang=" + lang if lang else ""}#1.1'); pg.wait_for_timeout(1500)
            pg.evaluate('document.fonts.ready')
            ids = pg.evaluate("TOPICS.filter(t => t.cards).flatMap(t => t.cards.map((c, i) => t.id + '.' + (i + 1)))")
            tall, wrap, broken = {}, [], []
            for h in ids:
                pg.evaluate(f"location.hash = '#{h}'"); pg.wait_for_timeout(400)
                over = pg.evaluate(LESSON_H) - vh
                if over > 0:
                    tall[h] = over
                if pg.evaluate(TITLE_WRAPS):
                    wrap.append(h)
                if pg.evaluate(CARD_BROKEN):
                    broken.append(h)
            b.close()
        return ids, tall, wrap, broken, errs
    finally:
        srv.terminate()


def main(argv):
    args = list(argv)
    lang = ''
    if '--lang' in args:
        i = args.index('--lang'); lang = args[i + 1]; del args[i:i + 2]
    site = args[0] if args else '.'
    vh = int(args[1]) if len(args) > 1 else 740
    ids, tall, wrap, broken, errs = check(site, vh, lang)
    print(f'{lang or "en"}: {len(ids) - len(tall)}/{len(ids)} lessons fit 390x{vh}' + (f'; too tall (px over): {tall}' if tall else ''))
    print('titles on one line' if not wrap else f'titles on two lines: {wrap}')
    print('every card loads' if not broken and not errs else f'card errors: {broken} {errs}')
    return 1 if (tall or wrap or broken or errs or not ids) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
