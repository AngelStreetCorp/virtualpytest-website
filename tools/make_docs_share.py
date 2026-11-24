#!/usr/bin/env python3
"""Share assets of the Docs posters. Run from the repo root after a poster changes:

    python3 tools/make_docs_share.py

For each poster id in POSTERS: docs/img/<id>-share.png (1200x630, the top of the poster; X and LinkedIn show PNG or JPG,
never SVG) and docs/view/<id>/index.html (a static page with the Open Graph / Twitter card tags, then it opens the
viewer). A link needs no `#`: social crawlers ignore the part after `#`, so the share link is /docs/view/<id>/.
Add a poster: add its row to POSTERS here (and to docs/index.html and docs/view/index.html), run this script, commit the output.
"""
import http.server, os, socketserver, threading
from playwright.sync_api import sync_playwright

POSTERS = [
    ("what-is", "What is VirtualPyTest?", "img/what-is-virtualpytest.svg", "Any device with a screen, tested and monitored 24/7 by AI, in one image."),
    ("profiles", "A profile is a set of services", "img/profiles.svg", "What a host runs for each device: three host shapes, a profile per device and a table of what each profile switches on."),
    ("services", "Services are background jobs", "img/services.svg", "Every VirtualPyTest service, grouped in server and host, and how each one shows on the Status page."),
    ("fingerprint", "Fingerprint", "img/fingerprint.svg", "Which node is on screen right now? The blob stored on a node, the sibling check at save, the refresh script and the six abstain doors of identify_screen."),
    ("ai-use-cases", "Where VirtualPyTest uses AI", "img/ai-use-cases.svg", "Where VirtualPyTest uses AI: six use cases, from discarding incidents to the live TV companion, and what is not AI."),
    ("small-models", "Our own small models", "img/small-models.svg", "How we trained three small models of our own, taught by the cloud models, answering only when sure, 0 USD a call."),
    ("freeze-discard", "Freeze: menu or stuck video?", "img/freeze-discard.svg", "How a freeze alert is decided in 0.25 ms: read the words, weigh the pieces, decide with a safety band."),
]
PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · VirtualPyTest</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:site_name" content="VirtualPyTest">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="https://virtualpytest.com/docs/view/{id}/">
<meta property="og:image" content="https://virtualpytest.com/docs/img/{id}-share.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://virtualpytest.com/docs/img/{id}-share.png">
<link rel="canonical" href="https://virtualpytest.com/docs/view/{id}/">
<meta http-equiv="refresh" content="0; url=../#{id}">
<script>location.replace('../#{id}');</script>
</head><body><p><a href="../#{id}">{title}</a></p></body></html>
"""

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def main():
    srv = socketserver.TCPServer(("127.0.0.1", 0), Q); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
        for id_, title, src, desc in POSTERS:
            pg.set_content(f'<body style="margin:0;background:#161616"><img src="http://127.0.0.1:{port}/docs/{src}" width=1200 style="display:block">')
            pg.wait_for_timeout(1200)
            pg.screenshot(path=f"docs/img/{id_}-share.png", clip={"x": 0, "y": 0, "width": 1200, "height": 630})
            os.makedirs(f"docs/view/{id_}", exist_ok=True)
            open(f"docs/view/{id_}/index.html", "w").write(PAGE.format(id=id_, title=title, desc=desc))
            print(id_, "ok")
        b.close()
    srv.shutdown()

main()
