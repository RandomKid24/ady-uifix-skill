#!/usr/bin/env python3
"""Render the README preview images for the ui-fix design library.

Usage:
  npm i @fontsource/{fraunces,inter-tight,inter,ibm-plex-sans,ibm-plex-mono,nunito,barlow,barlow-condensed,\
dm-serif-display,dm-sans,atkinson-hyperlegible,cormorant-garamond,manrope,rubik,baloo-2,jetbrains-mono,\
public-sans,space-grotesk,archivo-black,source-sans-3}   # in some folder
  python3 docs/build-previews.py <that-folder>/node_modules/@fontsource docs/images

Needs: pip install playwright && playwright install chromium
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

FONTS = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(sys.argv[2]).resolve(); OUT.mkdir(parents=True, exist_ok=True)

FAMILIES = {  # css family -> (fontsource folder, weights)
 'Fraunces': ('fraunces', [400, 600]), 'Inter Tight': ('inter-tight', [400, 500, 700, 800]), 'Inter': ('inter', [400, 500, 600, 700]),
 'IBM Plex Sans': ('ibm-plex-sans', [400, 500, 600]), 'IBM Plex Mono': ('ibm-plex-mono', [400, 500]), 'Nunito': ('nunito', [400, 600, 700, 800]),
 'Barlow': ('barlow', [400, 600, 700]), 'Barlow Condensed': ('barlow-condensed', [600, 700]), 'DM Serif Display': ('dm-serif-display', [400]),
 'DM Sans': ('dm-sans', [400, 500, 700]), 'Atkinson Hyperlegible': ('atkinson-hyperlegible', [400, 700]),
 'Cormorant Garamond': ('cormorant-garamond', [400, 500, 600]), 'Manrope': ('manrope', [400, 500, 600]), 'Rubik': ('rubik', [400, 500, 700]),
 'Baloo 2': ('baloo-2', [600, 700, 800]), 'JetBrains Mono': ('jetbrains-mono', [400, 600]), 'Public Sans': ('public-sans', [400, 600, 700]),
 'Space Grotesk': ('space-grotesk', [400, 500, 700]), 'Archivo Black': ('archivo-black', [400]), 'Source Sans 3': ('source-sans-3', [400, 600]),
}
def font_links():
    out = []
    for fam, (folder, ws) in FAMILIES.items():
        for w in ws:
            f = FONTS / folder / f'{w}.css'
            if f.exists(): out.append(f'<link rel="stylesheet" href="file://{f}">')
    return '\n'.join(out)

# ---------------------------------------------------------------- styles
# One example screen per style, each on a screen that fits its domain: see screens.py
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from screens import SCREENS

def screen_html(sc):
    return f'<!doctype html><html><head><meta charset="utf-8">{font_links()}</head><body>{sc["html"]}</body></html>'

# ---------------------------------------------------------------- patterns (wireframes)
WF = "font-family:Inter,sans-serif;"
def box(label, style='', cls='b'):
    return f'<div class="{cls}" style="{style}">{label}</div>'
DASH = [
 ('KPI strip + detail', f'<div class="g" style="grid-template-columns:repeat(4,1fr);grid-template-rows:56px 1fr">{"".join(box("KPI") for _ in range(4))}{box("Main chart / table","grid-column:1/4")}{box("Side list")}</div>'),
 ('My day', f'<div class="g" style="grid-template-columns:2fr 1fr;grid-template-rows:46px 1fr 1fr">{box("Greeting + next action","grid-column:1/3")}{box("My tasks","grid-row:2/4")}{box("Team")}{box("Balances")}</div>'),
 ('Command center', f'<div class="g" style="grid-template-columns:3fr 1fr;grid-template-rows:40px 1fr">{box("KPI · KPI · KPI · last updated","grid-column:1/3")}{box("Live map / status grid")}{box("Alarms","background:#FBEAE8;border-color:#C9372C")}</div>'),
 ('Bento grid', f'<div class="g" style="grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(3,1fr)">{box("Big","grid-column:1/3;grid-row:1/3")}{box("Tall","grid-row:1/4")}{box("")}{box("")}{box("Wide","grid-column:1/3")}{box("")}</div>'),
 ('Feed / inbox', f'<div class="g" style="grid-template-columns:1fr;grid-template-rows:36px repeat(4,1fr)">{box("Filters · All · Unread · Mine")}{"".join(box("● Item needing action — Approve / Reject","text-align:left;justify-content:flex-start;padding-left:12px") for _ in range(4))}</div>'),
 ('Split list-detail', f'<div class="g" style="grid-template-columns:1fr 2fr;grid-template-rows:repeat(5,1fr)">{"".join(box("Row") for _ in range(1))}{box("Selected item detail","grid-row:1/6;grid-column:2")}{"".join(box("Row") for _ in range(4))}</div>'),
 ('Report / narrative', f'<div class="g" style="grid-template-columns:1fr 1fr 1fr;grid-template-rows:40px 50px 1fr">{box("Headline sentence: sales 12% above target","grid-column:1/4;font-weight:600")}{box("Number")}{box("Number")}{box("Number")}{box("Chart that answers one question","grid-column:1/4")}</div>'),
 ('Role-based home', f'<div class="g" style="grid-template-columns:repeat(3,1fr);grid-template-rows:30px 1fr 1fr">{box("Admin","background:#EDEDEA")}{box("Manager","background:#EDEDEA")}{box("Staff","background:#EDEDEA")}{box("Approvals first","background:#EDEDEA")}{box("Team status","background:#EDEDEA")}{box("Punch in + my leave","background:#EDEDEA")}{box("Shared shell, different first section","grid-column:1/4")}</div>'),
]
LISTS = [
 ('Dense table', f'<div class="g" style="grid-template-rows:28px repeat(5,1fr);grid-template-columns:2fr 1fr 1fr 1fr">{"".join(box(h,"font-weight:700") for h in ["Name","Status","Qty","Amount"])}{"".join(box(c) for _ in range(5) for c in ["Item","● Open","12","₹4,200"])}</div>'),
 ('Card list', f'<div class="g" style="grid-template-columns:1fr 1fr 1fr;grid-template-rows:1fr 1fr">{"".join(box("▢ Image<br>Name · status") for _ in range(6))}</div>'),
 ('Kanban board', f'<div class="g" style="grid-template-columns:repeat(4,1fr);grid-template-rows:26px 1fr 1fr 1fr">{"".join(box(h,"font-weight:700") for h in ["New","Doing","Review","Done"])}{"".join(box("Card") for _ in range(8))}{box("")}{box("")}{box("")}{box("")}</div>'),
 ('Timeline', f'<div class="g" style="grid-template-columns:30px 1fr;grid-template-rows:repeat(5,1fr)">{"".join(box("●","border:none;background:none;color:#5B6CFF")+box("10:4"+str(i)+" — Event description","justify-content:flex-start;padding-left:10px") for i in range(5))}</div>'),
 ('Calendar / schedule', f'<div class="g" style="grid-template-columns:50px repeat(4,1fr);grid-template-rows:26px repeat(4,1fr)">{box("")}{"".join(box(d,"font-weight:700") for d in ["Riya","Sam","Neha","Om"])}{"".join(box(t,"font-weight:600")+box("")+box("Booking","background:#EDEDEA")+box("")+box("Booking","background:#EDEDEA") for t in ["10","11","12","1"])}</div>'),
 ('Gallery / grid', f'<div class="g" style="grid-template-columns:repeat(4,1fr);grid-template-rows:1fr 1fr">{"".join(box("▢") for _ in range(8))}</div>'),
 ('Tree / nested', f'<div class="g" style="grid-template-columns:1fr;grid-template-rows:repeat(6,1fr)">{"".join(box(t,"justify-content:flex-start;padding-left:"+str(10+i*22)+"px") for t,i in [("▾ Assets",0),("▾ Current",1),("Cash",2),("Bank",2),("▸ Fixed",1),("▸ Liabilities",0)])}</div>'),
 ('Grouped list', f'<div class="g" style="grid-template-columns:1fr;grid-template-rows:24px 1fr 1fr 24px 1fr 1fr">{box("TODAY","font-weight:700;background:none;border:none;justify-content:flex-start")}{box("Item")}{box("Item")}{box("YESTERDAY","font-weight:700;background:none;border:none;justify-content:flex-start")}{box("Item")}{box("Item")}</div>'),
]
def wire_sheet(title, items):
    cards = ''.join(f'<div class="card"><div class="t">{n}</div>{g}</div>' for n, g in items)
    return f"""<!doctype html><html><head><meta charset="utf-8">{font_links()}<style>
*{{box-sizing:border-box;margin:0}} body{{width:1200px;background:#F6F6F4;{WF} padding:28px;color:#222}}
h2{{font-weight:700;font-size:20px;margin-bottom:16px}} .sheet{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
.card{{background:#fff;border:1px solid #E2E2DE;border-radius:10px;padding:12px}} .t{{font-weight:600;font-size:13px;margin-bottom:10px}}
.g{{display:grid;gap:5px;height:150px}} .b{{background:#F1F2F6;border:1px solid #D9DCE6;border-radius:4px;font-size:10px;color:#555;display:flex;align-items:center;justify-content:center;text-align:center;padding:2px;overflow:hidden}}
</style></head><body><h2>{title}</h2><div class="sheet">{cards}</div></body></html>"""

# ---------------------------------------------------------------- components
COMPONENTS = f"""<!doctype html><html><head><meta charset="utf-8">{font_links()}<style>
*{{box-sizing:border-box;margin:0}} body{{width:1200px;background:#F6F6F4;font-family:Inter,sans-serif;padding:28px;color:#1d1d1f}}
h2{{font-size:20px;margin-bottom:16px}} h3{{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#666;margin:18px 0 10px}}
.row{{display:grid;gap:14px}} .c{{background:#fff;border:1px solid #E2E2DE;border-radius:10px;padding:14px}} .cap{{font-size:11px;color:#777;margin-top:8px}}
.n{{font-size:28px;font-weight:700;font-variant-numeric:tabular-nums}} .l{{font-size:12px;color:#666}} .up{{color:#1E7A3D;font-size:12px;font-weight:600}}
.bar{{height:8px;border-radius:99px;background:#ECEDF1;overflow:hidden;display:flex}} .seg{{height:100%}}
.chip{{display:inline-block;padding:3px 10px;border-radius:99px;font-size:12px;font-weight:600;margin-right:6px}}
.seg-ctl{{display:inline-flex;border:1px solid #CFD3DC;border-radius:8px;overflow:hidden}} .seg-ctl span{{padding:7px 14px;font-size:13px;border-right:1px solid #CFD3DC}} .seg-ctl span:last-child{{border:none}} .on{{background:#2557D6;color:#fff}}
.rc{{border:1px solid #CFD3DC;border-radius:8px;padding:10px 12px;font-size:13px;margin-bottom:6px}} .rc.on{{border-color:#2557D6;background:#EEF3FF;color:#1d1d1f}}
.sw{{display:inline-block;width:36px;height:20px;border-radius:99px;background:#2557D6;position:relative;vertical-align:middle}} .sw:after{{content:'';position:absolute;right:3px;top:3px;width:14px;height:14px;border-radius:50%;background:#fff}}
</style></head><body><h2>Component variants (from the library)</h2>
<h3>Metric displays</h3><div class="row" style="grid-template-columns:repeat(4,1fr)">
<div class="c"><div class="l">Revenue · this month</div><div class="n">₹12.4L</div><div class="up">▲ 12% vs last month</div><div class="cap">Number + delta</div></div>
<div class="c"><div class="l">Tickets closed</div><div class="n">184</div><svg width="100%" height="30" viewBox="0 0 120 30"><polyline fill="none" stroke="#2557D6" stroke-width="2" points="0,24 15,20 30,22 45,14 60,16 75,9 90,11 105,5 120,7"/></svg><div class="cap">Number + sparkline</div></div>
<div class="c"><div class="l">Attendance goal</div><div style="display:flex;align-items:center;gap:12px"><svg width="54" height="54" viewBox="0 0 36 36"><circle cx="18" cy="18" r="15" fill="none" stroke="#ECEDF1" stroke-width="4"/><circle cx="18" cy="18" r="15" fill="none" stroke="#1E7A3D" stroke-width="4" stroke-dasharray="82 100" transform="rotate(-90 18 18)"/></svg><div class="n">87%</div></div><div class="cap">Progress to target</div></div>
<div class="c"><div style="font-size:15px;line-height:1.4"><b>3 leave requests</b> need your approval →</div><div class="cap">Sentence metric</div></div></div>
<h3>Choice controls — by number of options</h3><div class="row" style="grid-template-columns:repeat(4,1fr)">
<div class="c"><span class="sw"></span>&nbsp; Email alerts<div class="cap">2 · switch</div></div>
<div class="c"><span class="seg-ctl"><span class="on">Day</span><span>Week</span><span>Month</span></span><div class="cap">2–4 · segmented</div></div>
<div class="c"><div class="rc on"><b>Full day</b><br><span class="l">Counts as 1 leave day</span></div><div class="rc"><b>Half day</b></div><div class="cap">2–4 with explanation · radio cards</div></div>
<div class="c"><div class="rc" style="display:flex;justify-content:space-between">Search vendors… <span>⌕</span></div><div class="rc on">Acme Industrial Supplies</div><div class="cap">10+ · searchable select</div></div></div>
<h3>Status & progress</h3><div class="row" style="grid-template-columns:repeat(4,1fr)">
<div class="c"><span class="chip" style="background:#E8F5EC;color:#1E7A3D">Approved</span><span class="chip" style="background:#FFF4E0;color:#9A5B00">Pending</span><span class="chip" style="background:#FDECEC;color:#B42318">Rejected</span><div class="cap">Soft chips</div></div>
<div class="c"><span style="color:#1E7A3D">●</span> Online &nbsp; <span style="color:#9A5B00">●</span> Away &nbsp; <span style="color:#999">●</span> Offline<div class="cap">Dot + text</div></div>
<div class="c"><div class="bar"><div class="seg" style="width:46%;background:#1D2430"></div><div class="seg" style="width:22%;background:#2557D6"></div><div class="seg" style="width:10%;background:#8A94A3"></div></div><div class="l" style="margin-top:8px">Casual · Sick · Unpaid</div><div class="cap">Segmented bar</div></div>
<div class="c"><div style="display:flex;gap:6px;align-items:center;font-size:12px"><span class="chip" style="background:#2557D6;color:#fff;margin:0">1 Draft</span>—<span class="chip" style="background:#2557D6;color:#fff;margin:0">2 Review</span>—<span class="chip" style="background:#ECEDF1;margin:0">3 Paid</span></div><div class="cap">Stepper</div></div></div>
</body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 720, 'height': 440}, device_scale_factor=2)
    tmp = OUT / '_tmp.html'
    for sc in SCREENS:
        tmp.write_text(screen_html(sc)); pg.goto(f'file://{tmp}'); pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / f'style-{sc["slug"]}.png'))
    pg2 = b.new_page(viewport={'width': 1200, 'height': 400}, device_scale_factor=2)
    for name, html in [('patterns-dashboards', wire_sheet('Dashboard & home layouts', DASH)), ('patterns-lists', wire_sheet('List & collection layouts', LISTS)), ('components', COMPONENTS)]:
        tmp.write_text(html); pg2.goto(f'file://{tmp}'); pg2.wait_for_timeout(250)
        pg2.screenshot(path=str(OUT / f'{name}.png'), full_page=True)
    tmp.unlink(); b.close()
print('done:', sorted(x.name for x in OUT.glob('*.png')))
