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
 'Fraunces': ('fraunces', [400, 600]), 'Inter Tight': ('inter-tight', [400, 700, 800]), 'Inter': ('inter', [400, 500, 600, 700]),
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
# Same content in every style: a small "Team today" home screen.
STYLES = [
 dict(slug='editorial', name='Editorial', head="'Fraunces', serif", body="'Inter', sans-serif", num="'Fraunces', serif",
      bg='#FBFAF7', surface='transparent', text='#1B1B1A', muted='#6B6A66', accent='#7A1F2B', accent_text='#fff', border='rgba(27,27,26,.14)',
      radius='0px', btn_radius='0px', card='border-top:1px solid rgba(27,27,26,.85); padding:14px 0 0;', label='font-variant:small-caps; letter-spacing:.06em; text-transform:lowercase;',
      chip='background:transparent; border:1px solid currentColor;', title_w=600, num_w=400, num_size='40px', pad='34px 40px'),
 dict(slug='swiss', name='Swiss functional', head="'Inter Tight', sans-serif", body="'Inter Tight', sans-serif", num="'Inter Tight', sans-serif",
      bg='#FFFFFF', surface='transparent', text='#0A0A0A', muted='#6E6E6E', accent='#E5322D', accent_text='#fff', border='#0A0A0A',
      radius='0px', btn_radius='0px', card='border-top:2px solid #0A0A0A; padding:10px 0 0;', label='text-transform:uppercase; letter-spacing:.04em; font-weight:700; font-size:11px;',
      chip='background:#0A0A0A; color:#fff;', title_w=800, num_w=800, num_size='48px', pad='32px 40px'),
 dict(slug='soft', name='Soft & friendly', head="'Nunito', sans-serif", body="'Nunito', sans-serif", num="'Nunito', sans-serif",
      bg='#F7F6FF', surface='#FFFFFF', text='#28264A', muted='#77749C', accent='#6C5CE7', accent_text='#fff', border='transparent',
      radius='20px', btn_radius='999px', card='box-shadow:0 10px 30px rgba(76,64,180,.10); padding:18px;', label='font-weight:700;',
      chip='background:#E9F9F1; color:#16794C;', tints=['#EAF7FF', '#FFF1E8', '#F1ECFF'], title_w=800, num_w=800, num_size='34px', pad='30px 34px'),
 dict(slug='dense-pro', name='Dense pro', head="'IBM Plex Sans', sans-serif", body="'IBM Plex Sans', sans-serif", num="'IBM Plex Mono', monospace",
      bg='#F4F5F7', surface='#FFFFFF', text='#1D2430', muted='#5E6876', accent='#2557D6', accent_text='#fff', border='#D9DDE3',
      radius='4px', btn_radius='4px', card='border:1px solid #D9DDE3; padding:10px 12px;', label='font-size:11px; font-weight:600; color:#5E6876;',
      chip='background:#E8F5EC; color:#1E7A3D; border:1px solid #BFE3CB;', title_w=600, num_w=500, num_size='26px', pad='18px 22px', dense=True),
 dict(slug='dark-command', name='Dark command center', head="'Inter', sans-serif", body="'Inter', sans-serif", num="'JetBrains Mono', monospace",
      bg='#0E1116', surface='#161B22', text='#E6EDF3', muted='#8B949E', accent='#58A6FF', accent_text='#0E1116', border='#30363D',
      radius='6px', btn_radius='6px', card='border:1px solid #30363D; padding:14px;', label='font-size:11px; text-transform:uppercase; letter-spacing:.08em; color:#8B949E;',
      chip='background:rgba(63,185,80,.15); color:#3FB950;', title_w=600, num_w=600, num_size='34px', pad='26px 30px', live=True),
 dict(slug='industrial', name='Industrial', head="'Barlow Condensed', sans-serif", body="'Barlow', sans-serif", num="'Barlow Condensed', sans-serif",
      bg='#EDEDEA', surface='#FFFFFF', text='#111111', muted='#3D3D3D', accent='#FFC400', accent_text='#111', border='#111111',
      radius='2px', btn_radius='2px', card='border:2px solid #111; padding:14px;', label='text-transform:uppercase; font-weight:700; letter-spacing:.04em; font-size:13px;',
      chip='background:#1F9D55; color:#fff;', title_w=700, num_w=700, num_size='46px', pad='26px 30px', big_btn=True),
 dict(slug='warm-hospitality', name='Warm hospitality', head="'DM Serif Display', serif", body="'DM Sans', sans-serif", num="'DM Serif Display', serif",
      bg='#FAF6F0', surface='#FFFFFF', text='#2B2118', muted='#7B6A5B', accent='#C8553D', accent_text='#fff', border='#EADFD1',
      radius='14px', btn_radius='12px', card='border:1px solid #EADFD1; box-shadow:0 6px 18px rgba(80,50,20,.06); padding:16px;', label='font-weight:500; color:#7B6A5B;',
      chip='background:#EEF2E3; color:#5A6B2E;', title_w=400, num_w=400, num_size='36px', pad='28px 34px'),
 dict(slug='clinical', name='Clinical calm', head="'Atkinson Hyperlegible', sans-serif", body="'Atkinson Hyperlegible', sans-serif", num="'Atkinson Hyperlegible', sans-serif",
      bg='#F4F7F8', surface='#FFFFFF', text='#14262B', muted='#4F6469', accent='#0F766E', accent_text='#fff', border='#D7E2E4',
      radius='8px', btn_radius='8px', card='border:1px solid #D7E2E4; padding:16px;', label='font-weight:700; font-size:13px; color:#4F6469;',
      chip='background:#E6F4F1; color:#0F766E;', title_w=700, num_w=700, num_size='32px', pad='28px 34px'),
 dict(slug='neo-brutalist', name='Neo-brutalist', head="'Archivo Black', sans-serif", body="'Space Grotesk', sans-serif", num="'Archivo Black', sans-serif",
      bg='#FFF8E7', surface='#FFFFFF', text='#000000', muted='#2B2B2B', accent='#FFE14D', accent_text='#000', border='#000000',
      radius='4px', btn_radius='4px', card='border:3px solid #000; box-shadow:5px 5px 0 #000; padding:14px;', label='font-weight:700; text-transform:uppercase; font-size:12px;',
      chip='background:#2BD47D; color:#000; border:2px solid #000;', tints=['#FF6FB5', '#3D5AFE', '#2BD47D'], title_w=400, num_w=400, num_size='38px', pad='28px 34px', brutal=True),
 dict(slug='premium-minimal', name='Premium minimal', head="'Cormorant Garamond', serif", body="'Manrope', sans-serif", num="'Cormorant Garamond', serif",
      bg='#F7F4EE', surface='transparent', text='#1C1B19', muted='#7D776D', accent='#1C1B19', accent_text='#F7F4EE', border='rgba(28,27,25,.18)',
      radius='0px', btn_radius='0px', card='border-bottom:1px solid rgba(28,27,25,.18); padding:0 0 16px;', label='font-size:11px; letter-spacing:.22em; text-transform:uppercase; color:#A27B4E;',
      chip='background:transparent; color:#A27B4E; border:1px solid #A27B4E;', title_w=500, num_w=400, num_size='52px', pad='40px 48px'),
 dict(slug='playful', name='Playful', head="'Baloo 2', sans-serif", body="'Rubik', sans-serif", num="'Baloo 2', sans-serif",
      bg='#FFFDF6', surface='#FFFFFF', text='#22223B', muted='#5C5C7A', accent='#FF5D73', accent_text='#fff', border='#22223B',
      radius='18px', btn_radius='999px', card='border:2px solid #22223B; padding:14px;', label='font-weight:500;',
      chip='background:#FFD23F; color:#22223B;', tints=['#5BC0EB', '#9BC53D', '#FFD23F'], title_w=800, num_w=800, num_size='38px', pad='26px 32px', mascot=True),
 dict(slug='corporate-trust', name='Corporate trust', head="'Public Sans', sans-serif", body="'Public Sans', sans-serif", num="'Public Sans', sans-serif",
      bg='#F3F5F8', surface='#FFFFFF', text='#14213D', muted='#55607A', accent='#14213D', accent_text='#fff', border='#D8DEE8',
      radius='6px', btn_radius='6px', card='border:1px solid #D8DEE8; padding:16px;', label='font-weight:600; font-size:13px; color:#55607A;',
      chip='background:#E7F0FF; color:#1D4ED8;', title_w=700, num_w=700, num_size='32px', pad='0 0 26px', topbar=True),
]

def style_html(s):
    tints = s.get('tints')
    kpis = [('Present today', '42', 'of 48'), ('On leave', '3', 'this week 7'), ('To approve', '5', 'oldest 2d')]
    tiles = ''
    for i, (l, v, sub) in enumerate(kpis):
        tint = f"background:{tints[i]};" if tints else f"background:{s['surface']};"
        if s.get('brutal') and tints: tint = f"background:{tints[i]};"
        color = '#fff' if s.get('brutal') and i == 1 else s['text']
        tiles += f"""<div class="tile" style="{tint}{s['card']}border-radius:{s['radius']};color:{color}">
          <div class="lbl" style="{s['label']}{'color:'+color+';' if s.get('brutal') else ''}">{l}</div>
          <div class="num">{v}{'<span class="live"></span>' if s.get('live') and i==0 else ''}</div>
          <div class="sub" style="{'color:'+color+';opacity:.85' if s.get('brutal') else ''}">{sub}</div></div>"""
    rows = [('Priya Sharma', 'Casual leave · 2 days', 'Pending'), ('Arjun Mehta', 'Sick leave · 1 day', 'Pending')]
    rowhtml = ''.join(f"""<div class="row"><div class="av">{n.split()[0][0]}{n.split()[1][0]}</div>
        <div class="who"><div class="nm">{n}</div><div class="sub">{d}</div></div><span class="chip">{st}</span></div>""" for n, d, st in rows)
    mascot = """<div class="mascot">◕‿◕</div>""" if s.get('mascot') else ''
    top = f"""<div class="topbar"><span>■ HR Portal</span><span>Home · People · Leave · Payroll</span></div>""" if s.get('topbar') else ''
    btn_h = '52px' if s.get('big_btn') else ('32px' if s.get('dense') else '40px')
    return f"""<!doctype html><html><head><meta charset="utf-8">{font_links()}<style>
* {{ box-sizing:border-box; margin:0 }}
body {{ width:720px; height:440px; background:{s['bg']}; color:{s['text']}; font-family:{s['body']}; font-size:{'13px' if s.get('dense') else '14px'}; overflow:hidden }}
.wrap {{ padding:{s['pad']}; }}
.topbar {{ background:#14213D; color:#fff; display:flex; justify-content:space-between; padding:12px 34px; font-weight:600; font-size:13px; margin-bottom:22px }}
.topbar span:last-child {{ font-weight:400; opacity:.8 }}
.cornertag {{ position:absolute; right:14px; bottom:10px; font:600 11px Inter, sans-serif; color:{s['muted']}; opacity:.75 }}
.head {{ display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:{'14px' if s.get('dense') else '22px'}; padding:{'0 34px' if s.get('topbar') else '0'} }}
.eyebrow {{ {s['label']} color:{s['muted']}; margin-bottom:4px }}
h1 {{ font-family:{s['head']}; font-weight:{s['title_w']}; font-size:{'22px' if s.get('dense') else '30px'}; line-height:1.1; letter-spacing:{'-.02em' if s['slug'] in ('swiss','editorial') else '0'} }}
.btn {{ background:{s['accent']}; color:{s['accent_text']}; border-radius:{s['btn_radius']}; height:{btn_h}; padding:0 {'26px' if s.get('big_btn') else '18px'};
        display:inline-flex; align-items:center; font-weight:{700 if s.get('big_btn') or s.get('brutal') else 600}; font-size:{'18px' if s.get('big_btn') else '14px'};
        {'border:3px solid #000; box-shadow:4px 4px 0 #000;' if s.get('brutal') else ''} {'text-transform:uppercase;' if s.get('big_btn') else ''}
        {'border:1px solid #1C1B19; letter-spacing:.14em; text-transform:uppercase; font-size:11px;' if s['slug']=='premium-minimal' else ''} }}
.tiles {{ display:grid; grid-template-columns:repeat(3,1fr); gap:{'10px' if s.get('dense') else '16px'}; margin-bottom:{'12px' if s.get('dense') else '20px'}; padding:{'0 34px' if s.get('topbar') else '0'} }}
.num {{ font-family:{s['num']}; font-weight:{s['num_w']}; font-size:{s['num_size']}; line-height:1.1; margin-top:6px; font-variant-numeric:tabular-nums; display:flex; align-items:center; gap:8px }}
.sub {{ color:{s['muted']}; font-size:12px; margin-top:2px }}
.live {{ width:9px; height:9px; border-radius:50%; background:#3FB950; box-shadow:0 0 0 4px rgba(63,185,80,.2) }}
.list {{ background:{s['surface'] if s['surface']!='transparent' else 'transparent'}; {s['card'] if s['slug'] not in ('editorial','swiss','premium-minimal') else ''} border-radius:{s['radius']}; margin:{'0 34px' if s.get('topbar') else '0'} }}
.listhead {{ {s['label']} color:{s['muted']}; margin-bottom:8px; {'border-top:1px solid '+s['border']+'; padding-top:12px;' if s['slug'] in ('editorial','swiss','premium-minimal') else ''} }}
.row {{ display:flex; align-items:center; gap:12px; padding:{'6px 0' if s.get('dense') else '9px 0'}; border-top:1px solid {s['border'] if s['border']!='transparent' else '#EEE'} }}
.row:first-of-type {{ border-top:none }}
.av {{ width:{'26px' if s.get('dense') else '32px'}; height:{'26px' if s.get('dense') else '32px'}; border-radius:{'50%' if s['radius'] not in ('0px','2px') else '0'}; background:{s['accent'] if s['slug']!='premium-minimal' else '#A27B4E'}; color:{s['accent_text'] if s['slug']!='premium-minimal' else '#fff'};
       display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; {'border:2px solid #000;' if s.get('brutal') else ''} }}
.who {{ flex:1 }} .nm {{ font-weight:600 }}
.chip {{ {s['chip']} padding:3px 10px; border-radius:{'999px' if s['radius'] not in ('0px','2px','4px') else s['radius']}; font-size:12px; font-weight:600 }}
.mascot {{ position:absolute; left:282px; top:28px; font:700 22px 'Baloo 2'; background:#5BC0EB; color:#22223B; border:2px solid #22223B; border-radius:16px; padding:4px 10px; transform:rotate(-6deg) }}
</style></head><body><div style="position:relative;height:100%">{top}<div class="wrap" style="{'padding:0' if s.get('topbar') else ''}">
{mascot}
<div class="head"><div><div class="eyebrow">Saturday, 31 October</div><h1>{'Good afternoon' if s['slug'] in ('soft','playful','warm-hospitality') else 'Team today'}</h1></div><span class="btn">{'Punch in' if s.get('big_btn') else 'New leave request'}</span></div>
<div class="tiles">{tiles}</div>
<div class="list"><div class="listhead">Waiting for you</div>{rowhtml}</div>
</div><div class="cornertag">{s['name']}</div></div></body></html>"""

# ---------------------------------------------------------------- patterns (wireframes)
WF = "font-family:Inter,sans-serif;"
def box(label, style='', cls='b'):
    return f'<div class="{cls}" style="{style}">{label}</div>'
DASH = [
 ('KPI strip + detail', f'<div class="g" style="grid-template-columns:repeat(4,1fr);grid-template-rows:56px 1fr">{"".join(box("KPI") for _ in range(4))}{box("Main chart / table","grid-column:1/4")}{box("Side list")}</div>'),
 ('My day', f'<div class="g" style="grid-template-columns:2fr 1fr;grid-template-rows:46px 1fr 1fr">{box("Greeting + next action","grid-column:1/3")}{box("My tasks","grid-row:2/4")}{box("Team")}{box("Balances")}</div>'),
 ('Command center', f'<div class="g" style="grid-template-columns:3fr 1fr;grid-template-rows:40px 1fr">{box("KPI · KPI · KPI · last updated","grid-column:1/3")}{box("Live map / status grid")}{box("Alarms","background:#FCE8E6;border-color:#E5534B")}</div>'),
 ('Bento grid', f'<div class="g" style="grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(3,1fr)">{box("Big","grid-column:1/3;grid-row:1/3")}{box("Tall","grid-row:1/4")}{box("")}{box("")}{box("Wide","grid-column:1/3")}{box("")}</div>'),
 ('Feed / inbox', f'<div class="g" style="grid-template-columns:1fr;grid-template-rows:36px repeat(4,1fr)">{box("Filters · All · Unread · Mine")}{"".join(box("● Item needing action — Approve / Reject","text-align:left;justify-content:flex-start;padding-left:12px") for _ in range(4))}</div>'),
 ('Split list-detail', f'<div class="g" style="grid-template-columns:1fr 2fr;grid-template-rows:repeat(5,1fr)">{"".join(box("Row") for _ in range(1))}{box("Selected item detail","grid-row:1/6;grid-column:2")}{"".join(box("Row") for _ in range(4))}</div>'),
 ('Report / narrative', f'<div class="g" style="grid-template-columns:1fr 1fr 1fr;grid-template-rows:40px 50px 1fr">{box("Headline sentence: sales 12% above target","grid-column:1/4;font-weight:600")}{box("Number")}{box("Number")}{box("Number")}{box("Chart that answers one question","grid-column:1/4")}</div>'),
 ('Role-based home', f'<div class="g" style="grid-template-columns:repeat(3,1fr);grid-template-rows:30px 1fr 1fr">{box("Admin","background:#E8EEFF")}{box("Manager","background:#E9F7EF")}{box("Staff","background:#FFF4E5")}{box("Approvals first","background:#E8EEFF")}{box("Team status","background:#E9F7EF")}{box("Punch in + my leave","background:#FFF4E5")}{box("Shared shell, different first section","grid-column:1/4")}</div>'),
]
LISTS = [
 ('Dense table', f'<div class="g" style="grid-template-rows:28px repeat(5,1fr);grid-template-columns:2fr 1fr 1fr 1fr">{"".join(box(h,"font-weight:700") for h in ["Name","Status","Qty","Amount"])}{"".join(box(c) for _ in range(5) for c in ["Item","● Open","12","₹4,200"])}</div>'),
 ('Card list', f'<div class="g" style="grid-template-columns:1fr 1fr 1fr;grid-template-rows:1fr 1fr">{"".join(box("▢ Image<br>Name · status") for _ in range(6))}</div>'),
 ('Kanban board', f'<div class="g" style="grid-template-columns:repeat(4,1fr);grid-template-rows:26px 1fr 1fr 1fr">{"".join(box(h,"font-weight:700") for h in ["New","Doing","Review","Done"])}{"".join(box("Card") for _ in range(8))}{box("")}{box("")}{box("")}{box("")}</div>'),
 ('Timeline', f'<div class="g" style="grid-template-columns:30px 1fr;grid-template-rows:repeat(5,1fr)">{"".join(box("●","border:none;background:none;color:#5B6CFF")+box("10:4"+str(i)+" — Event description","justify-content:flex-start;padding-left:10px") for i in range(5))}</div>'),
 ('Calendar / schedule', f'<div class="g" style="grid-template-columns:50px repeat(4,1fr);grid-template-rows:26px repeat(4,1fr)">{box("")}{"".join(box(d,"font-weight:700") for d in ["Riya","Sam","Neha","Om"])}{"".join(box(t,"font-weight:600")+box("")+box("Booking","background:#E8EEFF")+box("")+box("Booking","background:#E9F7EF") for t in ["10","11","12","1"])}</div>'),
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
<div class="c"><div class="bar"><div class="seg" style="width:46%;background:#6C5CE7"></div><div class="seg" style="width:22%;background:#2557D6"></div><div class="seg" style="width:10%;background:#F5A524"></div></div><div class="l" style="margin-top:8px">Casual · Sick · Unpaid</div><div class="cap">Segmented bar</div></div>
<div class="c"><div style="display:flex;gap:6px;align-items:center;font-size:12px"><span class="chip" style="background:#2557D6;color:#fff;margin:0">1 Draft</span>—<span class="chip" style="background:#2557D6;color:#fff;margin:0">2 Review</span>—<span class="chip" style="background:#ECEDF1;margin:0">3 Paid</span></div><div class="cap">Stepper</div></div></div>
</body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 720, 'height': 440}, device_scale_factor=2)
    tmp = OUT / '_tmp.html'
    for s in STYLES:
        tmp.write_text(style_html(s)); pg.goto(f'file://{tmp}'); pg.wait_for_timeout(250)
        pg.screenshot(path=str(OUT / f'style-{s["slug"]}.png'))
    pg2 = b.new_page(viewport={'width': 1200, 'height': 400}, device_scale_factor=2)
    for name, html in [('patterns-dashboards', wire_sheet('Dashboard & home layouts', DASH)), ('patterns-lists', wire_sheet('List & collection layouts', LISTS)), ('components', COMPONENTS)]:
        tmp.write_text(html); pg2.goto(f'file://{tmp}'); pg2.wait_for_timeout(250)
        pg2.screenshot(path=str(OUT / f'{name}.png'), full_page=True)
    tmp.unlink(); b.close()
print('done:', sorted(x.name for x in OUT.glob('*.png')))
