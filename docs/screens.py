"""Twelve example screens, one per style in references/library/styles.md.

Each style is shown on a screen that fits its domain (a report, an orders console, a lesson, a PO table, a
meter, a machine board, a restaurant floor, a ward list, a sprint board, a portfolio, a reading app, an
approvals queue) — not the same dashboard re-skinned. They follow the skill's own anti-slop rules: 4px
spacing, text left-aligned, no gradients/glows/emoji, plain real-looking copy, quiet chrome, one rich moment.
"""

BASE = "*{box-sizing:border-box;margin:0;padding:0}body{width:720px;height:440px;overflow:hidden;-webkit-font-smoothing:antialiased}"

def spark(points, color, w=300, h=80, fill=None, thr=None, sw=2):
    xs = [i * (w / (len(points) - 1)) for i in range(len(points))]
    pts = ' '.join(f'{x:.1f},{h - p * h:.1f}' for x, p in zip(xs, points))
    area = f'<polygon points="0,{h} {pts} {w},{h}" fill="{fill}"/>' if fill else ''
    t = f'<line x1="0" x2="{w}" y1="{h - thr * h:.1f}" y2="{h - thr * h:.1f}" stroke="#F85149" stroke-width="1" stroke-dasharray="4 4"/>' if thr is not None else ''
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{area}{t}<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/></svg>'

SCREENS = []

# 1 ── Editorial · a quarterly review (type and rules do the work)
SCREENS.append(dict(slug='editorial', name='Editorial', domain='Quarterly review', html=f"""<style>{BASE}
body{{background:#FBFAF7;color:#1B1B1A;font:400 14px/1.55 Inter}} .p{{padding:36px 48px}}
.eb{{font-size:12px;color:#6B6A66;margin-bottom:12px}} h1{{font:600 30px/1.18 Fraunces,serif;letter-spacing:-.01em;max-width:560px;margin-bottom:24px}}
.cols{{display:grid;grid-template-columns:260px 1fr;gap:40px;border-top:1px solid #1B1B1A;padding-top:16px}}
p{{color:#3A3935;margin-bottom:16px}} .fig{{font:400 56px/1 Fraunces,serif;color:#7A1F2B}} .fig small{{display:block;font:400 12px Inter;color:#6B6A66;margin-top:8px}}
table{{width:100%;border-collapse:collapse;font-size:13px}} th{{font-weight:500;text-align:left;color:#6B6A66;padding:0 0 8px;font-size:12px}} th:not(:first-child),td:not(:first-child){{text-align:right}}
td{{padding:12px 0;border-top:1px solid rgba(27,27,26,.14);font-variant-numeric:tabular-nums}} .bad{{color:#7A1F2B;font-weight:600}}</style>
<div class="p"><div class="eb">Quarterly review · Q3 2026</div><h1>Dispatch times fell 18%, but the Pune depot is the exception</h1>
<div class="cols"><div><p>Median dispatch time dropped from 41 to 34 hours after the new picking route. Three of four depots improved; Pune slipped by six hours in September.</p><div class="fig">34 h<small>median dispatch time, Q3</small></div></div>
<table><tr><th>Depot</th><th>Q2</th><th>Q3</th><th>Change</th></tr><tr><td>Nashik</td><td>38 h</td><td>29 h</td><td>−9 h</td></tr><tr><td>Mumbai</td><td>44 h</td><td>36 h</td><td>−8 h</td></tr><tr><td>Nagpur</td><td>41 h</td><td>35 h</td><td>−6 h</td></tr><tr><td>Pune</td><td>39 h</td><td class="bad">45 h</td><td class="bad">+6 h</td></tr></table></div></div>"""))

# 2 ── Swiss functional · orders console (asymmetric grid, one signal colour)
SCREENS.append(dict(slug='swiss', name='Swiss functional', domain='Orders console', html=f"""<style>{BASE}
body{{background:#fff;color:#0A0A0A;font:400 14px/1.4 'Inter Tight'}} .p{{padding:32px 40px;display:grid;grid-template-columns:300px 1fr;gap:48px}}
.k{{font-size:13px;color:#6E6E6E;margin-bottom:8px}} .big{{font:800 96px/.95 'Inter Tight';letter-spacing:-.04em;font-variant-numeric:tabular-nums}} .sm{{margin-top:12px;color:#6E6E6E}}
.r{{display:flex;justify-content:space-between;align-items:baseline;border-top:2px solid #0A0A0A;padding:12px 0 12px}} .r b{{font:700 28px 'Inter Tight';font-variant-numeric:tabular-nums}} .sig{{display:inline-block;width:10px;height:10px;background:#E5322D;margin-right:8px}}
h2{{font:700 14px 'Inter Tight';margin:28px 0 8px}} table{{width:100%;border-collapse:collapse;font-size:13px}} td{{padding:8px 0;border-top:1px solid #D9D9D9}} td:last-child{{text-align:right;font-variant-numeric:tabular-nums}}</style>
<div class="p"><div><div class="k">Open orders</div><div class="big">1,284</div><div class="sm">12 more than yesterday at this time</div></div>
<div><div class="r"><span><span class="sig"></span>Delayed</span><b>37</b></div><div class="r"><span>Ready to ship</span><b>212</b></div><div class="r"><span>Waiting for payment</span><b>90</b></div>
<h2>Oldest delayed</h2><table><tr><td>#10412 · Shree Traders</td><td>6 days</td></tr><tr><td>#10418 · Kale Hardware</td><td>5 days</td></tr><tr><td>#10431 · Mehta &amp; Sons</td><td>4 days</td></tr></table></div></div>"""))

# 3 ── Soft & friendly · a lesson (warm accent, one radius, plain headline)
SCREENS.append(dict(slug='soft', name='Soft & friendly', domain='Learning app', html=f"""<style>{BASE}
body{{background:#FFF8F1;color:#33261D;font:400 15px/1.5 Nunito}} .p{{padding:32px 40px}}
.eb{{font-size:14px;color:#8A7466;margin-bottom:4px}} h1{{font:800 30px/1.15 Nunito;margin-bottom:20px}}
.main{{display:grid;grid-template-columns:1fr 240px;gap:20px}} .c{{background:#fff;border-radius:16px;padding:20px;box-shadow:0 1px 2px rgba(51,38,29,.08)}}
.bar{{height:8px;border-radius:99px;background:#F1E4D8;margin:12px 0 8px}} .bar i{{display:block;height:100%;width:60%;border-radius:99px;background:#E8553D}}
.btn{{display:inline-block;margin-top:16px;background:#E8553D;color:#fff;font-weight:700;padding:12px 24px;border-radius:12px}}
.s{{color:#8A7466;font-size:13px}} .l{{display:flex;gap:12px;align-items:center;padding:12px 0;border-top:1px solid #F1E4D8}} .l:first-of-type{{border:none}} .d{{width:20px;height:20px;border-radius:50%;border:2px solid #E8553D;flex:none}} .d.on{{background:#E8553D}} .d.off{{border-color:#D9C7B8}}</style>
<div class="p"><div class="eb">Spanish · Unit 2</div><h1>Lesson 4: Ordering food</h1>
<div class="main"><div class="c"><b>You're 3 of 5 exercises in</b><div class="bar"><i></i></div><div class="s">About 6 minutes left</div><span class="btn">Continue lesson</span></div>
<div class="c"><b style="font-size:14px">Up next</b><div style="margin-top:8px"><div class="l"><span class="d on"></span>Vocabulary</div><div class="l"><span class="d on"></span>Listening</div><div class="l"><span class="d"></span>Speaking</div><div class="l"><span class="d off"></span>Review</div></div></div></div></div>"""))

# 4 ── Dense pro · purchase orders (compact, aligned, no decoration)
rows = [('PO-24817','Sharma Steel Works','Raw material','12 Oct','₹4,82,000','Approved'),('PO-24818','Kale Fasteners','Consumables','12 Oct','₹38,400','Pending'),('PO-24819','Nashik Tooling Co.','Tooling','13 Oct','₹1,26,500','Pending'),('PO-24820','Mehta Packaging','Packaging','14 Oct','₹54,250','Approved'),('PO-24821','Deccan Lubricants','Consumables','14 Oct','₹21,900','Received'),('PO-24822','Sharma Steel Works','Raw material','15 Oct','₹3,10,000','Pending'),('PO-24823','Apex Bearings','Spares','16 Oct','₹67,800','Approved'),('PO-24824','Kale Fasteners','Consumables','16 Oct','₹12,300','Received')]
tr = ''.join(f"<tr class='{'sel' if i==2 else ''}'><td class='cb'><i></i></td><td class='m'>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td class='n'>{e}</td><td><span class='st {f.lower()}'></span>{f}</td></tr>" for i,(a,b,c,d,e,f) in enumerate(rows))
SCREENS.append(dict(slug='dense-pro', name='Dense pro', domain='Purchase orders', html=f"""<style>{BASE}
body{{background:#F4F5F7;color:#1D2430;font:400 13px/1.3 'IBM Plex Sans'}} .p{{padding:16px 20px}}
.h{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}} h1{{font:600 18px 'IBM Plex Sans'}} .btn{{background:#2557D6;color:#fff;font-weight:500;padding:0 12px;height:28px;display:flex;align-items:center;border-radius:4px}}
.f{{display:flex;gap:8px;margin-bottom:8px}} .f span{{border:1px solid #D9DDE3;background:#fff;border-radius:4px;height:28px;display:flex;align-items:center;padding:0 12px;color:#5E6876}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #D9DDE3}} th{{text-align:left;font-weight:600;font-size:12px;color:#5E6876;background:#EDEFF3;padding:0 12px;height:28px;border-bottom:1px solid #D9DDE3}}
td{{padding:0 12px;height:30px;border-bottom:1px solid #E6E9EE}} .m{{font:400 12px 'IBM Plex Mono'}} .n{{text-align:right;font-family:'IBM Plex Mono';font-size:12px}} th:nth-child(6){{text-align:right}}
.cb{{width:28px}} .cb i{{display:block;width:12px;height:12px;border:1px solid #9AA3B0;border-radius:2px;background:#fff}} .sel{{background:#E8EFFF}} .sel .cb i{{background:#2557D6;border-color:#2557D6}}
.st{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px}} .approved{{background:#1E7A3D}} .pending{{background:#C98A00}} .received{{background:#5E6876}}
.bulk{{margin-top:8px;color:#5E6876;font-size:12px}}</style>
<div class="p"><div class="h"><h1>Purchase orders</h1><span class="btn">New PO</span></div><div class="f"><span>Search PO or vendor</span><span>Status: all</span><span>Date: October</span></div>
<table><tr><th class="cb"></th><th>PO number</th><th>Vendor</th><th>Category</th><th>Date</th><th>Amount</th><th>Status</th></tr>{tr}</table><div class="bulk">1 selected · Approve · Export · 8 of 214 shown</div></div>"""))

# 5 ── Dark command center · energy meter (live value, threshold, alarm rail)
SCREENS.append(dict(slug='dark-command', name='Dark command center', domain='Energy monitoring', html=f"""<style>{BASE}
body{{background:#0E1116;color:#E6EDF3;font:400 13px/1.4 Inter}} .p{{padding:24px 28px;display:grid;grid-template-columns:minmax(0,1fr) 220px;gap:16px}}
.pn{{background:#161B22;border:1px solid #30363D;border-radius:6px;padding:16px}} .k{{color:#8B949E;font-size:12px}} .v{{font:600 52px/1.05 'JetBrains Mono';margin:8px 0 2px}} .v small{{font-size:18px;color:#8B949E;font-weight:400}}
.live{{display:flex;align-items:center;gap:8px;color:#8B949E;font-size:12px}} .live i{{width:8px;height:8px;border-radius:50%;background:#3FB950}}
.al{{border-left:3px solid #F85149;padding:4px 0 4px 12px;margin-bottom:12px}} .al b{{display:block;font-weight:600}} .ok{{color:#8B949E;padding:8px 0;border-top:1px solid #30363D;display:flex;justify-content:space-between}} .ok span:last-child{{color:#3FB950}}
.row{{display:flex;gap:24px;margin-top:12px;color:#8B949E;font-size:12px}} .row b{{display:block;color:#E6EDF3;font:600 16px 'JetBrains Mono'}}</style>
<div class="p"><div class="pn"><div class="live"><i></i>Plant 2 · main incomer · updated 10:42:08</div><div class="v">412<small> kW</small></div><div class="k">Demand now · limit 450 kW</div>
<div style="margin-top:12px">{spark([.48,.5,.46,.52,.58,.55,.6,.66,.7,.74,.8,.84,.82,.9,.92,.88], '#58A6FF', 392, 150, thr=.92, sw=2)}</div>
<div class="row"><div><b>0.96</b>power factor</div><div><b>1,284</b>kWh today</div><div><b>₹9.1k</b>cost today</div></div></div>
<div class="pn"><div class="k" style="margin-bottom:8px">Alarms</div><div class="al"><b>Feeder 3 over limit</b><span class="k">12 min · 468 kW</span></div><div class="k" style="margin:16px 0 4px">Normal</div><div class="ok"><span>Feeder 1</span><span>OK</span></div><div class="ok"><span>Feeder 2</span><span>OK</span></div><div class="ok"><span>Compressor room</span><span>OK</span></div></div></div>"""))

# 6 ── Industrial · machine board (big plates, gloves, glare)
SCREENS.append(dict(slug='industrial', name='Industrial', domain='Machine board', html=f"""<style>{BASE}
body{{background:#EDEDEA;color:#111;font:500 16px/1.25 Barlow}} .p{{padding:20px 24px}} h1{{font:700 26px 'Barlow Condensed';text-transform:uppercase;letter-spacing:.02em;margin-bottom:12px}}
.m{{display:grid;grid-template-columns:200px 1fr 200px;align-items:center;background:#fff;border:2px solid #111;margin-bottom:12px;min-height:88px}}
.m .n{{font:700 30px 'Barlow Condensed';padding:0 16px}} .m .i{{padding:0 8px;font-size:15px;color:#3D3D3D}} .m .i b{{display:block;color:#111;font-size:18px}}
.b{{height:100%;display:flex;align-items:center;padding:0 16px;font:700 24px 'Barlow Condensed';text-transform:uppercase}} .run{{background:#1F9D55;color:#fff}} .stop{{background:#D93025;color:#fff}} .wait{{background:#FFC400;color:#111}}
.go{{display:flex;align-items:center;justify-content:center;background:#111;color:#fff;font:700 24px 'Barlow Condensed';text-transform:uppercase;height:100%;min-height:88px;border-left:2px solid #111}}</style>
<div class="p"><h1>Line 2 · Machines</h1>
<div class="m"><div class="b run" style="min-height:88px">Running</div><div class="i"><b>CNC 4 · Job 2281</b>Bracket, 400 pcs · 62% done</div><div class="go">Pause</div></div>
<div class="m"><div class="b stop" style="min-height:88px">Stopped</div><div class="i"><b>Press 2</b>Die change since 09:40</div><div class="go">Start job</div></div>
<div class="m"><div class="b wait" style="min-height:88px">Waiting</div><div class="i"><b>Lathe 1</b>Material not at machine</div><div class="go">Call stores</div></div></div>"""))

# 7 ── Warm hospitality · restaurant floor (warmth from copy and colour of the content)
tbl = [('2','2 guests','Seated 18 min','Ordering',0),('3','4 guests','Seated 42 min','Main course',0),('4','6 guests','Seated 1 h 05','Dessert',0),('5','2 guests','Reserved 8:30','Not seated',0),('6','3 guests','Seated 1 h 20','Bill requested',1),('7','2 guests','Seated 6 min','Drinks served',0)]
tt = ''.join(f"<div class='t {'hot' if h else ''}'><div class='no'>{a}</div><div><b>{d}</b><div class='s'>{b} · {c}</div></div></div>" for a,b,c,d,h in tbl)
SCREENS.append(dict(slug='warm-hospitality', name='Warm hospitality', domain='Restaurant floor', html=f"""<style>{BASE}
body{{background:#FAF6F0;color:#2B2118;font:400 15px/1.4 'DM Sans'}} .p{{padding:28px 36px}} .eb{{color:#7B6A5B;font-size:13px}} h1{{font:400 32px/1.1 'DM Serif Display';margin:4px 0 20px}}
.g{{display:grid;grid-template-columns:1fr 1fr;gap:12px}} .t{{display:flex;gap:16px;align-items:center;background:#fff;border:1px solid #EADFD1;border-radius:12px;padding:12px 16px}} .t b{{font-weight:500}}
.no{{font:400 30px 'DM Serif Display';color:#C8553D;width:28px}} .s{{font-size:13px;color:#7B6A5B}} .hot{{border-color:#C8553D;background:#FFF3EE}} .hot b{{color:#A93F29}}</style>
<div class="p"><div class="eb">Saturday dinner · 7:30 service</div><h1>Tables on the floor</h1><div class="g">{tt}</div></div>"""))

# 8 ── Clinical calm · ward list (legibility, explicit words, one next action)
SCREENS.append(dict(slug='clinical', name='Clinical calm', domain='Ward list', html=f"""<style>{BASE}
body{{background:#F4F7F8;color:#14262B;font:400 15px/1.4 'Atkinson Hyperlegible'}} .p{{padding:28px 36px;display:grid;grid-template-columns:1fr 220px;gap:20px}} h1{{font:700 24px 'Atkinson Hyperlegible';margin-bottom:4px}} .s{{color:#4F6469;font-size:14px}}
.r{{display:grid;grid-template-columns:90px 1fr 150px;gap:12px;padding:12px 0;border-top:1px solid #D7E2E4;align-items:center}} .r b{{display:block}} .bed{{font-weight:700;color:#0F766E}}
.tag{{font-weight:700;font-size:14px}} .due{{color:#8A4B00}} .ok{{color:#14262B}} .c{{background:#fff;border:1px solid #D7E2E4;border-radius:8px;padding:16px}}
.btn{{display:block;background:#0F766E;color:#fff;font-weight:700;border-radius:8px;padding:12px 16px;margin-top:12px}}</style>
<div class="p"><div><h1>Ward 4 · Medical</h1><div class="s" style="margin-bottom:12px">12 patients · 3 need something in the next hour</div>
<div class="r"><span class="bed">Bed 1</span><span><b>Ramesh Patil, 67</b><span class="s">Pneumonia · day 3</span></span><span class="tag due">Medication due 11:00</span></div>
<div class="r"><span class="bed">Bed 2</span><span><b>Sunita Joshi, 54</b><span class="s">Post-op · day 1</span></span><span class="tag due">Dressing due 11:30</span></div>
<div class="r"><span class="bed">Bed 3</span><span><b>Aman Shaikh, 31</b><span class="s">Observation</span></span><span class="tag ok">Nothing due</span></div>
<div class="r"><span class="bed">Bed 4</span><span><b>Meera Kulkarni, 72</b><span class="s">Heart failure · day 5</span></span><span class="tag due">Vitals due 11:00</span></div></div>
<div class="c"><b>Next up</b><div class="s" style="margin-top:8px">11:00 · Bed 1<br>Give antibiotic, 500 mg</div><span class="btn">Open Bed 1</span></div></div>"""))

# 9 ── Neo-brutalist · sprint board (thick lines, one yellow, one pink)
cards = lambda items, bg: ''.join(f"<div class='k' style='background:{bg}'>{t}</div>" for t in items)
SCREENS.append(dict(slug='neo-brutalist', name='Neo-brutalist', domain='Sprint board', html=f"""<style>{BASE}
body{{background:#FFF8E7;color:#000;font:500 14px/1.35 'Space Grotesk'}} .p{{padding:24px 28px}} h1{{font:400 30px 'Archivo Black';margin-bottom:16px}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}} h2{{font:400 14px 'Archivo Black';text-transform:uppercase;border-bottom:3px solid #000;padding-bottom:8px;margin-bottom:12px}}
.k{{background:#fff;border:3px solid #000;box-shadow:4px 4px 0 #000;padding:12px;margin-bottom:12px;font-weight:500}} .k small{{display:block;margin-top:4px;font-weight:400;color:#2B2B2B}}</style>
<div class="p"><h1>Sprint 14</h1><div class="g"><div><h2>To do · 3</h2><div class='k'>Fix export to CSV<small>Asha</small></div><div class='k'>Invite emails bounce<small>Ravi</small></div><div class='k'>Dark mode contrast<small>Meera</small></div></div>
<div><h2>Doing · 2</h2><div class='k' style='background:#FFE14D'>New onboarding flow<small>Asha · 2 days left</small></div><div class='k' style='background:#FFE14D'>Billing page redesign<small>Ravi · 3 days left</small></div></div>
<div><h2>Done · 4</h2><div class='k' style='background:#FFD1E6'>Search is 3x faster<small>Meera · shipped Tuesday</small></div><div class='k'>Fix login redirect<small>Asha</small></div></div></div></div>"""))

# 10 ── Premium minimal · private portfolio (restraint, ledger lines, quiet numbers)
hold = [('Hindustan Unilever','Equity','₹1.24 Cr','+8.2%'),('HDFC Bank','Equity','₹86.4 L','+3.1%'),('Government of India 2034','Bonds','₹1.02 Cr','+0.9%'),('Embassy Office Parks','Real estate','₹74.0 L','+5.6%')]
hh = ''.join(f"<tr><td>{a}</td><td class='m'>{b}</td><td class='n'>{c}</td><td class='n'>{d}</td></tr>" for a,b,c,d in hold)
SCREENS.append(dict(slug='premium-minimal', name='Premium minimal', domain='Private portfolio', html=f"""<style>{BASE}
body{{background:#F7F4EE;color:#1C1B19;font:400 14px/1.5 Manrope}} .p{{padding:44px 56px}} .k{{font-size:13px;color:#7D776D}} .v{{font:400 64px/1 'Cormorant Garamond';margin:8px 0 4px;letter-spacing:-.01em}} .d{{color:#8A6A3F;font-size:13px;margin-bottom:28px}}
table{{width:100%;border-collapse:collapse}} td{{padding:12px 0;border-top:1px solid rgba(28,27,25,.16)}} .m{{color:#7D776D}} .n{{text-align:right;font-variant-numeric:tabular-nums}} tr:last-child td{{border-bottom:1px solid rgba(28,27,25,.16)}}</style>
<div class="p"><div class="k">Total portfolio value · 31 October 2026</div><div class="v">₹4.82 Cr</div><div class="d">+₹6.4 L this month</div><table>{hh}</table></div>"""))

# 11 ── Playful · reading app (one character with a job, calm elsewhere)
SCREENS.append(dict(slug='playful', name='Playful', domain='Reading app for kids', html=f"""<style>{BASE}
body{{background:#FFFDF6;color:#22223B;font:500 16px/1.4 Rubik}} .p{{padding:28px 36px;display:grid;grid-template-columns:150px 1fr;gap:28px;align-items:center;height:100%}}
.owl{{width:136px;height:150px;background:#FFD23F;border:3px solid #22223B;border-radius:60px 60px 48px 48px;position:relative}}
.owl .e{{position:absolute;top:44px;width:36px;height:36px;border-radius:50%;background:#fff;border:3px solid #22223B}} .owl .e:after{{content:'';position:absolute;left:12px;top:10px;width:10px;height:10px;border-radius:50%;background:#22223B}}
.owl .b{{position:absolute;left:54px;top:84px;width:24px;height:20px;background:#FF5D73;border:3px solid #22223B;border-radius:4px 4px 12px 12px}}
h1{{font:800 32px/1.1 'Baloo 2';margin-bottom:8px}} .s{{color:#5C5C7A;margin-bottom:16px}} .w{{display:flex;gap:8px;margin-bottom:20px}} .w i{{width:36px;height:36px;border-radius:50%;border:2px solid #22223B;display:flex;align-items:center;justify-content:center;font:700 13px Rubik;font-style:normal}} .w i.on{{background:#FFD23F}}
.btn{{display:inline-block;background:#FF5D73;color:#fff;font:700 20px 'Baloo 2';padding:12px 28px;border-radius:16px;border:2px solid #22223B;box-shadow:0 4px 0 #22223B}}</style>
<div class="p"><div class="owl"><span class="e" style="left:22px"></span><span class="e" style="left:72px"></span><span class="b"></span></div>
<div><h1>6 days in a row</h1><div class="s">Read one story today to keep your streak</div><div class="w"><i class="on">M</i><i class="on">T</i><i class="on">W</i><i class="on">T</i><i class="on">F</i><i class="on">S</i><i>S</i></div><span class="btn">Read today's story</span></div></div>"""))

# 12 ── Corporate trust · approvals queue (clear table + a decision panel)
inv = [('INV-2291','Kale Fasteners','₹1,18,400','Due 5 Nov','Needs you'),('INV-2288','Deccan Lubricants','₹36,900','Due 7 Nov','Needs you'),('INV-2284','Apex Bearings','₹2,41,000','Due 9 Nov','Approved'),('INV-2279','Mehta Packaging','₹58,250','Due 12 Nov','Approved')]
ii = ''.join(f"<tr class='{'sel' if i==0 else ''}'><td>{a}</td><td>{b}</td><td class='n'>{c}</td><td><span class='dot {'a' if e=='Approved' else 'n2'}'></span>{e}</td></tr>" for i,(a,b,c,d,e) in enumerate(inv))
SCREENS.append(dict(slug='corporate-trust', name='Corporate trust', domain='Approvals queue', html=f"""<style>{BASE}
body{{background:#F3F5F8;color:#14213D;font:400 14px/1.4 'Public Sans'}} .top{{background:#14213D;color:#fff;padding:12px 32px;display:flex;justify-content:space-between;font-weight:600;font-size:13px}} .top span:last-child{{font-weight:400;opacity:.8}}
.p{{padding:20px 32px;display:grid;grid-template-columns:minmax(0,1fr) 196px;gap:16px}} h1{{font:700 22px 'Public Sans';margin-bottom:4px;grid-column:1/3}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #D8DEE8;border-radius:6px}} th{{text-align:left;font-weight:600;color:#55607A;font-size:13px;padding:12px;border-bottom:1px solid #D8DEE8;white-space:nowrap}} td{{padding:16px 12px;border-bottom:1px solid #E6EAF1;white-space:nowrap}} .n{{text-align:right;font-variant-numeric:tabular-nums}} th:nth-child(3){{text-align:right}} .sel{{background:#EEF2FA}}
.dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px}} .a{{background:#1E7A3D}} .n2{{background:#B35C00}} .c{{background:#fff;border:1px solid #D8DEE8;border-radius:6px;padding:16px}} .s{{color:#55607A;font-size:13px}}
.b{{display:block;padding:12px 12px;border-radius:6px;font-weight:600;margin-top:8px}} .y{{background:#14213D;color:#fff}} .nn{{border:1px solid #14213D}}</style>
<div class="top"><span>Finance portal</span><span>Approvals · Payments · Vendors · Reports</span></div>
<div class="p"><h1>Invoices waiting for approval</h1><table><tr><th>Invoice</th><th>Vendor</th><th>Amount</th><th>Status</th></tr>{ii}</table>
<div class="c"><b>INV-2291</b><div class="s" style="margin:4px 0 8px">Kale Fasteners · matches PO-24818 and the goods receipt</div><span class="b y">Approve ₹1,18,400</span><span class="b nn">Reject</span></div></div>"""))
