// ui-fix: consistency scan — "do things that look alike match?" Run in the page (browser JS tool or Playwright page.evaluate). Read-only.
// A general rule instead of one rule per component: group things that sit together and look alike, then compare what the eye compares.
//   iconSizeMismatch     — icons in one row/stack/column with different sizes
//   headingSizeMismatch  — headings of the same level with different size or weight on one screen
//   boxRowMismatch       — cards/panels/chips/rows side by side with different height, radius, border, fill or padding
//   labelStyleMismatch   — labels/captions/column headers of one kind styled differently
// (Controls — inputs, selects, buttons on one row — are covered by slop-scan.js → controlRowMismatch.)
// Set ROOT to the target's selector, or null.
(() => {
  const ROOT = null;   // e.g. '#settings', 'main'
  const root = (ROOT && document.querySelector(ROOT)) || document.body;
  const S = el => getComputedStyle(el);
  const px = v => parseFloat(v) || 0;
  const vis = el => { const r = el.getBoundingClientRect(); const s = S(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0; };
  const V = [...root.querySelectorAll('*')].filter(el => !el.closest('script,style,template,noscript') && vis(el));
  const label = el => { const id = el.id ? '#' + el.id : ''; const cl = (typeof el.className === 'string' && el.className.trim()) ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return (el.tagName.toLowerCase() + id + cl).slice(0, 50); };
  const own = el => [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' ').replace(/\s+/g, ' ').trim();
  const color = c => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(parseFloat); return { r: p[0], g: p[1], b: p[2], a: p[3] == null ? 1 : p[3] }; };
  const spread = a => Math.max(...a) - Math.min(...a);
  const out = { found: {}, examples: {} };
  const flag = (k, el, note) => { out.found[k] = (out.found[k] || 0) + 1; (out.examples[k] = out.examples[k] || []); if (out.examples[k].length < 5) out.examples[k].push(label(el) + ' — ' + note); };
  const CTL = 'input:not([type=hidden]):not([type=checkbox]):not([type=radio]), select, textarea, button, [role=combobox], [role=searchbox], [role=button]';

  // 1. icons: same parent (a row of icons) or same column (a nav/list with an icon per row)
  const icons = V.filter(el => el.matches('svg,img') && !el.parentElement.closest('svg') && el.getBoundingClientRect().width <= 48 && el.getBoundingClientRect().height <= 48 && el.getBoundingClientRect().width >= 8);
  const byParent = new Map(); icons.forEach(i => { const p = i.parentElement; (byParent.get(p) || byParent.set(p, []).get(p)).push(i); });
  byParent.forEach(g => { if (g.length >= 2) { const w = g.map(i => Math.round(i.getBoundingClientRect().width)); if (spread(w) > 2) flag('iconSizeMismatch', g[0], g.length + ' icons in one row: ' + w.join('/') + 'px'); } });
  const cols = []; icons.sort((a, b) => a.getBoundingClientRect().left - b.getBoundingClientRect().left).forEach(i => { const l = i.getBoundingClientRect().left; const c = cols.find(c => Math.abs(c.l - l) <= 4); c ? c.items.push(i) : cols.push({ l, items: [i] }); });
  cols.forEach(c => { if (c.items.length >= 3) { const w = c.items.map(i => Math.round(i.getBoundingClientRect().width)); if (spread(w) > 2) flag('iconSizeMismatch', c.items[0], c.items.length + ' icons in one column: ' + [...new Set(w)].join('/') + 'px'); } });

  // 2. headings of one level
  ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].forEach(t => {
    const hs = V.filter(el => el.tagName.toLowerCase() === t && own(el)); if (hs.length < 2) return;
    const fs = hs.map(h => Math.round(px(S(h).fontSize))), fw = hs.map(h => +S(h).fontWeight);
    if (spread(fs) > 1) flag('headingSizeMismatch', hs[0], hs.length + ' <' + t + '> with sizes ' + [...new Set(fs)].join('/') + 'px');
    else if (spread(fw) >= 100) flag('headingSizeMismatch', hs[0], hs.length + ' <' + t + '> with weights ' + [...new Set(fw)].join('/'));
  });

  // 3. boxes (cards, panels, chips, list rows) side by side
  const hasBox = el => { const s = S(el); const bg = color(s.backgroundColor); return (px(s.borderTopWidth) > 0 && color(s.borderTopColor)?.a > 0.1) || (bg && bg.a > 0.05) || (s.boxShadow && s.boxShadow !== 'none'); };
  let boxes = V.filter(el => { const r = el.getBoundingClientRect(); return hasBox(el) && r.width >= 64 && r.width <= 900 && r.height >= 28 && r.height <= 360 && el !== root && !el.matches(CTL) && !el.querySelector(CTL.replace(/, \[role=button\]/, '')) && own(el).length + el.querySelectorAll('*').length > 0 && el.parentElement !== document.body; });
  const br = boxes.map(el => ({ el, r: el.getBoundingClientRect() })).sort((a, b) => a.r.top - b.r.top); const seen = new Set();
  br.forEach(a => {
    if (seen.has(a)) return; seen.add(a); const row = [a];
    br.forEach(b => { if (!seen.has(b) && !a.el.contains(b.el) && !b.el.contains(a.el) && Math.abs((b.r.top + b.r.height / 2) - (a.r.top + a.r.height / 2)) < Math.max(a.r.height, b.r.height) / 2 && b.el.parentElement === a.el.parentElement) { row.push(b); seen.add(b); } });
    if (row.length < 2) return;
    const els = row.sort((x, y) => x.r.left - y.r.left).map(x => x.el);
    const hs = els.map(e => Math.round(e.getBoundingClientRect().height)), rad = els.map((e, i) => Math.round(Math.min(px(S(e).borderTopLeftRadius), hs[i] / 2)));
    const pad = els.map(e => Math.round((px(S(e).paddingLeft) + px(S(e).paddingTop)) / 2));
    const bw = els.map(e => px(S(e).borderTopWidth) + 'px ' + S(e).borderTopColor), fill = els.map(e => S(e).backgroundColor), shadow = els.map(e => S(e).boxShadow !== 'none');
    const probs = [];
    if (spread(hs) > 2 && els.length <= 6) probs.push('height ' + hs.join('/') + 'px');
    if (spread(rad) > 2) probs.push('corner radius ' + rad.join('/') + 'px');
    if (pad.every(x => x > 0) && spread(pad) > 2) probs.push('padding ' + pad.join('/') + 'px');   // boxes with 0 padding centre or delegate to children
    // fill / border / shadow often differ on purpose (a highlighted card, a status colour) — only report them next to a size/shape difference
    if (probs.length) {
      if (new Set(bw).size > 1) probs.push('border differs');
      if (new Set(fill).size > 1) probs.push('fill differs');
      if (new Set(shadow).size > 1) probs.push('shadow on some only');
    }
    if (probs.length) flag('boxRowMismatch', els[0], els.length + ' boxes side by side: ' + probs.join(' · '));
  });

  // 4. labels / captions / column headers of one kind
  const kinds = { 'table headers (th)': 'th', 'form labels': 'label', 'legends': 'legend' };
  Object.entries(kinds).forEach(([name, sel]) => {
    const ls = V.filter(el => el.matches(sel) && own(el)); if (ls.length < 2) return;
    const sig = ls.map(l => Math.round(px(S(l).fontSize)) + '/' + S(l).fontWeight + '/' + S(l).textTransform);
    if (new Set(sig).size > 1) flag('labelStyleMismatch', ls[0], ls.length + ' ' + name + ' styled ' + [...new Set(sig)].slice(0, 3).join(' | ') + ' (size/weight/case)');
  });

  const kindsFound = Object.keys(out.found);
  out.summary = { problemKinds: kindsFound.length, problems: kindsFound.reduce((a, k) => a + out.found[k], 0),
    verdict: kindsFound.length ? 'things that look alike do not match — make them one component/token' : 'things that look alike match',
    note: 'A difference with a reason (a primary card, an active state, a deliberate hero) is fine — state the reason. Controls on one row: slop-scan.js. Anything the scans miss: reference think-like-a-designer.md (sweeps + write-a-probe).' };
  return out;
})();
