#!/usr/bin/env python3
"""Drawn generic screens for the `localize` Docs poster, run through the REAL Localize code.

Draws generic screens (no brand, no app screenshot) with headless Playwright, fingerprints the wall with
ImageHelpers.compute_fingerprint and names each live frame with ImageHelpers.identify_screen (which also calls
classify_special_state). Writes docs/img/localize-real-<name>.jpg (320x180) and tools/localize_example_values.json,
which tools/make_docs_poster_localize.py reads: no number on the poster is typed by hand.

Run from the website repo root:  python3 tools/localize_example_draw.py [path to the virtualpytest product repo]
"""
import json, os, sys, tempfile
REPO = os.path.abspath(os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/virtualpytest"))
os.environ.setdefault("VPT_MT_DOWNLOAD", "0")
from playwright.sync_api import sync_playwright
TABS = ["Home", "Movies", "Guide", "Apps", "Search"]
Cs = ["#3d8bd1", "#d1507a", "#4fc38a", "#e0a63a", "#8a6bd1", "#33c0c0"]
def page(title, body, active=None):
    tabs = "" if active is None else "".join(
        f'<div class="tab{" on" if b == active else ""}" style="left:{330+i*170}px">{b}</div>' for i, b in enumerate(TABS))
    tiles = "".join(f'<div class="tile" style="background:{c};left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>' for c, x, y, w, h in body)
    return f'''<body style="margin:0;width:1280px;height:720px;background:#10141c;font-family:DejaVu Sans;color:#eee;position:relative;overflow:hidden">
<style>.tab{{position:absolute;top:56px;font-size:26px;color:#9aa}}.tab.on{{color:#fff;border-bottom:6px solid #ff1010;padding-bottom:8px}}.tile{{position:absolute;border-radius:12px}}</style>
<div style="position:absolute;left:60px;top:28px;font-size:32px;font-weight:700">{title}</div>{tabs}{tiles}</body>'''
def rails(seed, hero):
    tl = [(hero, 60, 150, 1160, 250)]
    for r in range(2):
        for i in range(6):
            tl.append((Cs[(i + r * 2 + seed) % 6], 60 + i * 195, 430 + r * 140, 180, 120))
    return tl
def posters(seed):
    return [(Cs[(i + seed) % 6], 60 + (i % 5) * 232, 150 + (i // 5) * 280, 210, 250) for i in range(10)]
def guide():
    return [("#e8edf5" if i % 2 == 0 else "#5a6475", 60, 150 + i * 80, 1160, 64) for i in range(7)]
def listing(n, panel):
    return [("#2c3546", 60, 140 + i * 92, 640, 76) for i in range(n)] + [(panel, 740, 140, 480, 520)]
def settings():
    return [("#e8edf5", 60, 140 + i * 90, 420, 72) for i in range(6)] + [("#3d8bd1", 560, 140, 660, 520)]
def search():
    return [("#e8edf5", 60, 140, 700, 70)] + [("#2c3546", 60 + (i % 9) * 78, 240 + (i // 9) * 78, 70, 70) for i in range(36)] + [(Cs[i % 6], 820, 140 + i * 130, 400, 110) for i in range(4)]
SCREENS = {
    # the wall: screens saved in the navigation tree
    "home": page("Home", rails(0, "#d1507a"), "Home"),
    "home_movies": page("Home", posters(0), "Movies"),
    "home_guide": page("Home", guide(), "Guide"),
    "recordings": page("Recordings", listing(6, "#4fc38a")),
    "favourites": page("Favourites", listing(6, "#4fc38a")),
    "settings": page("Settings", settings()),
    # live frames
    "live_movies": page("Home", posters(3), "Movies"),
    "live_favourites": page("Favourites", listing(6, "#e0a63a")),
    "live_search": page("Search", search()),
    "live_black": '<body style="margin:0;width:1280px;height:720px;background:#000"></body>',
    "live_bars": '<body style="margin:0;width:1280px;height:720px;display:flex">' + "".join(
        f'<div style="flex:1;background:{c}"></div>' for c in ["#c0c0c0", "#c0c000", "#00c0c0", "#00c000", "#c000c0", "#c00000", "#0000c0"]) + "</body>",
}
WALL = ["home", "home_movies", "home_guide", "recordings", "favourites", "settings"]
LIVE = ["live_movies", "live_favourites", "live_search", "live_black", "live_bars"]

tmp = tempfile.mkdtemp()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 720})
    for k, v in SCREENS.items():
        pg.set_content(v); pg.screenshot(path=f"{tmp}/{k}.png")
    b.close()

sys.path[:0] = [REPO, os.path.join(REPO, "backend_host/src/controllers/verification")]
cwd = os.getcwd(); os.chdir(REPO)
import cv2
from backend_host.src.controllers.verification.image_helpers import ImageHelpers
h = ImageHelpers(None, None)
os.chdir(cwd)
img = {k: cv2.imread(f"{tmp}/{k}.png") for k in SCREENS}
for k, im in img.items():
    cv2.imwrite(f"docs/img/localize-real-{k}.jpg", cv2.resize(im, (320, 180), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 85])
fps = [{"node_id": n, "label": n, "fingerprint": h.compute_fingerprint(img[n])} for n in WALL]
out = {"FINGERPRINT_VERSION": h.FINGERPRINT_VERSION, "FP_SELF_DRIFT_FLOOR": h.FP_SELF_DRIFT_FLOOR,
       "wall": {f["node_id"]: {k: f["fingerprint"].get(k) for k in ("focus", "title")} for f in fps}, "live": {}}
for k in LIVE:
    r = h.identify_screen(img[k], fps)
    lf = h.compute_fingerprint(img[k])
    out["live"][k] = {"dhash": lf["dhash"], "title": lf.get("title"),
                      "title_scores": {f["node_id"]: round(h.title_score(lf.get("title") or "", f["fingerprint"].get("title") or ""), 2) for f in fps},
                      "candidates": [{x: c.get(x) for x in ("node_id", "confidence", "title_score")} for c in r.get("candidates") or []],
                      "ranked": [{x: c.get(x) for x in ("node_id", "dist")} for c in r.get("ranked") or []],
                      **{x: r.get(x) for x in ("reason", "state", "state_label", "live_focus")}}
json.dump(out, open("tools/localize_example_values.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
