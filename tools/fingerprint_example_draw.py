import sys
from playwright.sync_api import sync_playwright
BARS=["Home","Movies","Guide","Apps","Settings"]
def page(active, tiles, title, body="tiles"):
    tabs="".join(f'<div class="tab{" on" if b==active else ""}">{b}</div>' for b in BARS)
    t="".join(f'<div class="tile" style="background:{c};left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>' for c,x,y,w,h in tiles)
    return f'''<body style="margin:0;width:1280px;height:720px;background:#10141c;font-family:DejaVu Sans;color:#eee;position:relative;overflow:hidden">
<style>.tab{{position:absolute;top:34px;font-size:26px;color:#9aa}}.tab.on{{color:#fff;border-bottom:5px solid #e0a96d;padding-bottom:6px}}.tile{{position:absolute;border-radius:12px}}</style>
<div style="position:absolute;left:60px;top:30px;font-size:30px;font-weight:700">{title}</div>
{"".join(f'<div class="tab{" on" if b==active else ""}" style="left:{300+i*170}px">{b}</div>' for i,b in enumerate(BARS))}{t}</body>'''
Cs=["#3d8bd1","#d1507a","#4fc38a","#e0a63a","#8a6bd1","#33c0c0"]
def rails(seed, hero):
    tl=[(hero,60,130,1160,260)]
    for r in range(2):
        for i in range(6):
            tl.append((Cs[(i+r*2+seed)%6],60+i*195,420+r*140,180,120))
    return tl
SCREENS={
 'home':page("Home",rails(0,"#d1507a"),"Home"),
 'home_live':page("Home",rails(2,"#3d8bd1"),"Home"),
 'movies':page("Movies",[(Cs[i%6],60+(i%5)*232,150+(i//5)*280,210,250) for i in range(10)],"Movies"),
 'guide':page("Guide",[("#e8edf5" if i%2==0 else "#5a6475",60,130+i*85,1160,70) for i in range(7)],"Guide"),
 'settings':page("Settings",[("#e8edf5",60,130+i*90,420,72) for i in range(6)]+[("#3d8bd1",560,130,660,520)],"Settings"),
}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720})
    for k,v in SCREENS.items():
        pg.set_content(v); pg.screenshot(path=f'{k}.png')
