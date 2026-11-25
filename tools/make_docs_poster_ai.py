#!/usr/bin/env python3
"""Writes docs/img/ai-use-cases.svg (Docs poster "Where VirtualPyTest uses AI").

Layout agreed with the owner (2026-11-25): title, three numbers, the 9 use-case names as an overview, "How we keep AI
calls low" (algorithms, our small models, how we train them), then one card per use case: a real screenshot from our
platform (docs/img/ai-use-cases-real-*.jpg, names of customers hidden), the model badge top right (route and fallback
that really answered; an AI agent is named with an "AI Agent" pill), 3 or 4 one-line steps, one gold result line. Words: the "Step by step" section of
docs/ai/AI-USE-CASES.md in the product repo. Every card is the same height; no text may wrap.
The page is drawn in HTML, rendered by headless Chromium (Playwright) and stored as one JPEG inside the SVG, so the
poster looks the same everywhere. Run from the repo root: python3 tools/make_docs_poster_ai.py
"""
import base64, re
from playwright.sync_api import sync_playwright
def img(n):
    p = 'docs/img/fingerprint-real-report.jpg' if n == 'localize.jpg' else 'docs/img/ai-use-cases-real-' + n
    return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
AI='<span class="ai">AI</span>'; OWN='<span class="own">our model</span>'; AG='<span class="ag">AI Agent</span>'
cards=[
("Zap detection","Channel change time",'zap.jpg',"MiniMax Flash · fallback: Haiku",["Picture cuts: zap time measured","Banner text read by OCR","Known logo: name, no AI",f"New logo: {AI} reads it once"],"70 AI calls per wall before, 1 now"),
("Freeze detection","Is the picture stuck?",'freeze.jpg',"Our word classifier · no cloud",["Pixels stop moving","4 frames, diff under 0.5: freeze",f"Menu words? {OWN} says menu"],"0.25 ms, free, no cloud AI"),
("Discard Test Result","App bug or lab problem?",'test-result.jpg',"Sherlock: MiniMax M2.7 · fallback: Haiku",["Same failure: same verdict",f"{AG} Sherlock reads the logs","Lab problem: result set aside"],"Only real bugs count"),
("Discard Incident","Real problem or noise?",'discard-incident.jpg',"Nightwatch: MiniMax VLM · fallback: Haiku",["Screen seen before: ignored",f"Menu words: {OWN} ignores it",f"Unsure: {AG} Nightwatch looks"],"You only see real problems"),
("Classify unknown screens","A screen with no name",'unknown.jpg',"Our SmolVLM · fallback: MiniMax VLM",["Seen 5 times, no name yet",f"{OWN} or {AI} proposes a name","A person accepts it"],"Nothing named without a person"),
("Create script","Virtual script or test case",'create-script.jpg',"Forge: Claude Sonnet 5.5",["You describe the test in plain words",f"{AG} Forge writes script or test","A person reviews, then runs it"],"No code, no Python"),
("Chat Bot","Ask in plain words",'atlas.jpg',"Atlas: Claude Sonnet 5.5 · fallback: MiniMax M3",["You ask in plain words",f"{AG} Atlas picks the tools","It answers or acts on a device"],"About 2 s per model step"),
("Companion","Atlas beside the page",'companion.jpg',"Atlas: Claude Sonnet 5.5 · fallback: MiniMax M3",["Atlas sees your page","You ask: filter stb31+",f"{AG} Atlas runs the action"],"The page updates for you"),
("Localize Screen","Which screen is this?",'localize.jpg',"Our Qwen3 0.6B · fallback: MiniMax M3",["Fingerprint vs stored screens","Sure: done, no AI",f"Doubtful: {AI} confirms"],"AI on about 3 in 100"),
]
ov=''.join(f'<div class="ov"><b>{"Classify screens" if c[0].startswith("Classify") else c[0]}</b><span>{c[1]}</span></div>' for c in cards)

def tile(t,lines,to):
    return '<div class="tl"><b>'+t+'</b>'+''.join('<span>'+l+'</span>' for l in lines)+'<i>→ '+to+'</i></div>'
algos=[("Fingerprint",["Picture hash per screen"],"Localize Screen"),("Screen memory",["Judged once, never again"],"Discard Incident"),("Logo table",["OCR + logos learned once"],"Zap detection"),("Signature table",["Same failure, same verdict"],"Discard Test Result")]
models=[("Word classifier",["Base: none (word weights)","2 MB · 0.25 ms","95.6 % right"],"Freeze detection"),("Localize model",["Base: Qwen3 0.6B + LoRA","640 MB · 1.3 s","98.9 % right"],"Localize Screen"),("Screen namer",["Base: SmolVLM 256M + LoRA","365 MB · 2.6 s","98.3 % right when sure"],"Classify screens")]
train=["Take the lab's own AI answers","Keep a test set two strong models agree on","Teach the small model: 15 to 30 min, under 2 USD","Serve it: sure answers only, cloud AI as fallback"]
how='<section class="how"><h2>How we keep AI calls low</h2><p class="hs">Repetitive tasks get an algorithm or a small model of our own. The cloud AI is only the fallback.</p>'
how+='<div class="gl">ALGORITHMS: NO MODEL, NO COST</div><div class="tg4">'+''.join(tile(*a) for a in algos)+'</div>'
how+='<div class="gl">OUR SMALL MODELS: TRAINED BY US, RUN ON OUR BOXES</div><div class="tg3">'+''.join(tile(*m) for m in models)+'</div>'
how+='<div class="gl">HOW WE TRAIN THEM</div><ol class="tr">'+''.join(f'<li><span class="n">{i}</span><span>{t}</span></li>' for i,t in enumerate(train,1))+'</ol><p class="res">→ Answering only when sure turns 94 % into 98 %</p></section>'
cs=''
for t,sub,im,model,steps,res in cards:
    th=f'<img src="{img(im)}">' if im else '<div class="ph">image to come</div>'
    li=''.join(f'<li><span class="n">{j}</span><span>{s}</span></li>' for j,s in enumerate(steps,1))
    cs+=f'<section class="card"><div class="hd"><h2>{t}</h2><span class="mb">{model}</span></div><div class="row"><div class="th">{th}</div><div><ol>{li}</ol><p class="res">→ {res}</p></div></div></section>'
html=f'''<html><head><meta charset="utf-8"><style>
body{{margin:0;background:#161616;color:#f2f2f2;font-family:Geist,Inter,system-ui,sans-serif;width:1200px}}
.w{{padding:60px}} .eb{{color:#e0a96d;letter-spacing:3px;font-size:20px}} h1{{font-size:62px;margin:14px 0 10px}}
.sub{{color:#a8a8a8;font-size:26px;line-height:1.4}}
.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:30px 0 12px}}
.st{{background:#212121;border:2px solid #3a3a3a;border-radius:18px;padding:18px 22px}} .st b{{font-size:44px;color:#e0a96d;display:block}} .st span{{color:#a8a8a8;font-size:20px}}
.kinds{{color:#a8a8a8;font-size:19px;margin-bottom:30px}}
.ovg{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:40px}}
.ov{{background:#212121;border:2px solid #3a3a3a;border-radius:16px;padding:18px 14px;text-align:center;display:flex;flex-direction:column;gap:6px;justify-content:center;min-height:92px}}
.ov b{{font-size:19px;white-space:nowrap}} .ov span{{color:#a8a8a8;font-size:17px}}
.card{{background:#212121;border:2px solid #3a3a3a;border-radius:22px;padding:24px 30px;margin-bottom:26px;height:340px;box-sizing:border-box}}
h2{{margin:0;font-size:34px}} .hd{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;gap:16px}} .mb{{border:1.5px solid #e0a96d;color:#e0a96d;border-radius:999px;padding:5px 14px;font-size:16px;white-space:nowrap}} .row{{display:grid;grid-template-columns:440px 1fr;gap:30px;align-items:center}}
.th{{width:440px;height:240px;background:#0f0f0f;border-radius:12px;overflow:hidden;display:flex;align-items:center;justify-content:center}}
.th img{{max-width:440px;max-height:240px;object-fit:contain;display:block}}
.ph{{width:436px;height:236px;border:2px dashed #e0a96d;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#e0a96d;font-size:20px}}
ol{{list-style:none;padding:0;margin:0;font-size:22px;line-height:1.35}} li{{display:flex;gap:12px;align-items:center;margin-bottom:12px;white-space:nowrap}}
.n{{background:#3a3a3a;border-radius:50%;width:32px;height:32px;display:inline-flex;align-items:center;justify-content:center;font-size:17px;flex:none}}
.ai{{background:#e0a96d;color:#1a1a1a;font-weight:700;border-radius:8px;padding:1px 9px;font-size:18px}}
.ag{{background:#e0a96d;color:#1a1a1a;font-weight:700;border-radius:8px;padding:1px 9px;font-size:18px;white-space:nowrap;box-shadow:inset 0 0 0 2px #1a1a1a55}} .own{{background:#6dc5c9;color:#10201f;font-weight:700;border-radius:8px;padding:1px 9px;font-size:18px;white-space:nowrap}}
.res{{color:#e0a96d;font-size:21px;margin:10px 0 0;font-weight:600}}
.how{{background:#212121;border:2px solid #3a3a3a;border-radius:22px;padding:26px 30px;margin-bottom:26px}} .hs{{color:#a8a8a8;font-size:21px;margin:8px 0 18px}}
.gl{{color:#e0a96d;letter-spacing:2px;font-size:16px;font-weight:700;margin:18px 0 12px}}
.tg4{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}} .tg3{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}}
.tl{{background:#2a2a2a;border:1.5px solid #3a3a3a;border-radius:14px;padding:14px 16px;display:flex;flex-direction:column;gap:5px}}
.tl b{{font-size:20px;white-space:nowrap}} .tl span{{color:#c8c8c8;font-size:15px;white-space:nowrap}} .tl i{{color:#e0a96d;font-style:normal;font-size:16px;font-weight:600;margin-top:4px;white-space:nowrap}}
ol.tr{{font-size:21px}}
.end{{border:2px solid #e0a96d;background:#2a2418;border-radius:22px;text-align:center;padding:30px;font-size:32px;color:#e0a96d;font-weight:700;margin-top:10px}}
</style></head><body><div class="w">
<div class="eb">AI IN THE LAB</div><h1>Where VirtualPyTest uses AI</h1>
<div class="sub">Most of the recurrent tasks do not require AI. Here is an overview of the split.</div>
<div class="stats"><div class="st"><b>120+</b><span>devices watched</span></div><div class="st"><b>350,000</b><span>AI answers in 30 days</span></div><div class="st"><b>14.90 USD</b><span>for all AI in 30 days</span></div></div>
<div class="kinds">Set-top boxes · Mobile · Streams · Consoles · Web · Android TV · Apple TV</div>
<div class="ovg">{ov}</div>{how}{cs}
<div class="end">AI only when nothing simpler can decide.</div></div></body></html>'''

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 1000}, device_scale_factor=1.5)
    pg.set_content(html); pg.wait_for_timeout(500)
    bad = pg.evaluate("""[...document.querySelectorAll('.tl b,.tl span,.tl i,li,.ov b,.mb,h2,.res')].filter(e => {
        const c = e.closest('.tl,.card,.how,.ov,.w').getBoundingClientRect(), r = e.getBoundingClientRect();
        return e.scrollWidth > e.clientWidth + 1 || r.right > c.right - 8 || (e.matches('li,.ov b,.res,.mb,h2') && e.getClientRects().length > 1);
    }).map(e => e.textContent)""")
    if bad:
        raise SystemExit("text wraps or overflows: " + "; ".join(bad))
    H = pg.evaluate("document.body.scrollHeight")
    jpg = pg.screenshot(full_page=True, type="jpeg", quality=72)
    b.close()
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 {H}" width="1200" height="{H}" role="img" aria-labelledby="ti">'
       f'<title id="ti">Where VirtualPyTest uses AI, in one image</title>'
       f'<image width="1200" height="{H}" href="data:image/jpeg;base64,{base64.b64encode(jpg).decode()}"/></svg>')
open("docs/img/ai-use-cases.svg", "w").write(svg)
print(f"docs/img/ai-use-cases.svg written, 1200x{H}, {len(svg)//1024} KB")
