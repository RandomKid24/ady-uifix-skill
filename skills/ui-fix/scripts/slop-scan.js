// ui-fix: slop scan. Run in the page (browser JS tool or Playwright page.evaluate). Read-only.
// Counts the measurable "generated UI" tells and the craft problems behind them:
//   spacing off the grid · sibling padding/height mismatch · controls on one row that differ (height, radius, border, fill, text size) · centred text · narrow centred app column ·
//   hue gradients · gradient text · coloured glows · emoji · UPPERCASE tracked labels · heavy weights ·
//   hype words · exclamation marks · greeting headlines · trailing periods on short labels ·
//   infinite animations · transition: all · bouncy easing.
// Set ROOT to the target's selector (or null for the whole page), GRID to design.md's spacing base.
(() => {
  const ROOT = null;   // e.g. '#checkout', 'main'
  const GRID = 4;      // spacing base (4 or 8)
  const root = (ROOT && document.querySelector(ROOT)) || document.body;
  const vw = innerWidth;
  const all = [root, ...root.querySelectorAll('*')].filter(el => !el.closest('script,style,svg,noscript,template'));
  const cs = new Map();
  const S = el => cs.get(el) || (cs.set(el, getComputedStyle(el)), cs.get(el));
  const vis = el => { const r = el.getBoundingClientRect(); const s = S(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0; };
  const V = all.filter(vis);
  const ownText = el => [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' ').replace(/\s+/g, ' ').trim();
  const label = el => { const id = el.id ? '#' + el.id : ''; const cl = (typeof el.className === 'string' && el.className.trim()) ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return (el.tagName.toLowerCase() + id + cl).slice(0, 60); };
  const px = v => parseFloat(v) || 0;
  const out = { tells: {}, craft: {}, examples: {} };
  const add = (k, el, note) => { (out.examples[k] = out.examples[k] || []); out.tells[k] = (out.tells[k] || 0) + 1; if (out.examples[k].length < 4) out.examples[k].push(label(el) + (note ? ' — ' + note : '')); };
  const addCraft = (k, el, note) => { (out.examples[k] = out.examples[k] || []); out.craft[k] = (out.craft[k] || 0) + 1; if (out.examples[k].length < 4) out.examples[k].push(label(el) + (note ? ' — ' + note : '')); };

  // ---- colour helpers ----
  const parseColor = c => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(parseFloat); return { r: p[0], g: p[1], b: p[2], a: p[3] == null ? 1 : p[3] }; };
  const hsl = ({ r, g, b }) => { r /= 255; g /= 255; b /= 255; const mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn; let h = 0; const l = (mx + mn) / 2; const s = d === 0 ? 0 : d / (1 - Math.abs(2 * l - 1)); if (d) { if (mx === r) h = ((g - b) / d) % 6; else if (mx === g) h = (b - r) / d + 2; else h = (r - g) / d + 4; } return { h: ((h * 60) + 360) % 360, s, l }; };
  const saturated = c => { const p = parseColor(c); return p && p.a > 0.05 && hsl(p).s > 0.35 && hsl(p).l > 0.12 && hsl(p).l < 0.92 ? p : null; };
  const hueDist = (a, b) => { const d = Math.abs(a - b) % 360; return d > 180 ? 360 - d : d; };

  // ---- 1. gradients (hue-shifting) and gradient text ----
  V.forEach(el => {
    const s = S(el); const bi = s.backgroundImage || '';
    if (/gradient/.test(bi)) {
      const cols = (bi.match(/rgba?\([^)]+\)/g) || []).map(parseColor).filter(c => c && c.a > 0.1);
      const sat = cols.filter(c => hsl(c).s > 0.25);
      let shift = false; for (let i = 0; i < sat.length; i++) for (let j = i + 1; j < sat.length; j++) if (hueDist(hsl(sat[i]).h, hsl(sat[j]).h) > 35) shift = true;
      const clip = (s.webkitBackgroundClip || s.backgroundClip) === 'text';
      if (clip) add('gradientText', el, ownText(el).slice(0, 30));
      else if (shift) add('hueGradient', el, 'hue shift');
      else if (sat.length >= 2 && el.getBoundingClientRect().width > 200 && el.getBoundingClientRect().height > 120) add('colourWash', el, 'large coloured gradient');
    }
    // coloured glow: saturated shadow with real blur
    const bs = s.boxShadow; if (bs && bs !== 'none') {
      (bs.match(/rgba?\([^)]+\)\s+-?\d+px\s+-?\d+px\s+(\d+)px/g) || []).forEach(sh => { const col = saturated(sh.match(/rgba?\([^)]+\)/)[0]); const blur = +sh.match(/(\d+)px$/)[1]; if (col && blur >= 12) add('colouredGlow', el, sh.slice(0, 50)); });
    }
    const ts = s.textShadow; if (ts && ts !== 'none') { const col = saturated(ts.match(/rgba?\([^)]+\)/)?.[0]); const blur = +(ts.match(/(\d+)px(?=\s*$)/) || [0, 0])[1]; if (col && blur >= 6) add('textGlow', el, ts.slice(0, 40)); }
  });

  // ---- 2. text tells ----
  const HYPE = /\b(supercharge[sd]?|seamless(ly)?|unlock(s|ed|ing)?|magic(al)?|revolutionary|revolutionize[sd]?|game[- ]chang(er|ing)|next[- ]gen(eration)?|cutting[- ]edge|10x|effortless(ly)?|blazing[- ]fast|ai[- ]powered|reimagine[sd]?|elevate[sd]?)\b/i;
  const EMOJI = /\p{Extended_Pictographic}/u;
  const GREETING = /^(welcome( back)?|hey|hi|hello|good (morning|afternoon|evening))\b.*[,!]/i;
  const UNVERIFIED = /(\d[\d,.]*\s*[kKmM]?\+?\s*(teams|companies|customers|users|businesses)\b|loved by|trusted by|#1\b|best[- ]in[- ]class)/i;
  let upperLabels = 0, heavyHeads = 0, headings = 0, centredText = 0, textBlocks = 0, tightSmall = 0, italics = 0;
  V.forEach(el => {
    const t = ownText(el); if (!t) return;
    const s = S(el); const fs = px(s.fontSize); const words = t.split(' ').length;
    textBlocks++;
    if (EMOJI.test(t)) add('emoji', el, t.slice(0, 30));
    if (HYPE.test(t) && words <= 40) add('hypeWords', el, t.slice(0, 40));
    if (/!/.test(t) && words <= 14) add('exclamation', el, t.slice(0, 40));
    if (GREETING.test(t) && (/^h[1-6]$/i.test(el.tagName) || fs >= 20)) add('greetingHeadline', el, t.slice(0, 40));
    if (UNVERIFIED.test(t) && words <= 14) add('unverifiedClaim', el, t.slice(0, 40));
    if (/^(lorem|john doe|jane doe|123,456|\[x\])/i.test(t) || /lorem ipsum/i.test(t)) add('placeholderData', el, t.slice(0, 30));
    if (words <= 6 && /\.$/.test(t) && /^(h[1-6]|button|label|th|a|span|legend|summary)$/i.test(el.tagName) && !/\.\.\.?$|etc\.$/.test(t)) add('trailingPeriodOnLabel', el, t);
    if (s.textTransform === 'uppercase' && px(s.letterSpacing) / fs > 0.05 && fs <= 13 && words <= 5) upperLabels++, add('uppercaseTrackedLabel', el, t.slice(0, 24));
    if (/^h[1-6]$/i.test(el.tagName) || fs >= 24) { headings++; if (+s.fontWeight >= 700) { heavyHeads++; } }
    if (px(s.letterSpacing) < 0 && fs < 20 && Math.abs(px(s.letterSpacing) / fs) > 0.015) add('negativeTrackingSmall', el, s.letterSpacing);
    if (s.fontStyle === 'italic' && words <= 8) italics++;
    if (s.textAlign === 'center' && words >= 12) { centredText++; add('centredParagraph', el, t.slice(0, 36)); }
  });
  if (heavyHeads >= 2 && headings && heavyHeads / headings > 0.6) { out.tells.heavyHeadingWeights = heavyHeads; out.examples.heavyHeadingWeights = ['weight ≥ 700 on ' + heavyHeads + ' of ' + headings + ' headings']; }
  const allCapsFam = (n) => n >= 3;
  if (allCapsFam(upperLabels)) out.tells.uppercaseLabelsRepeated = upperLabels;

  // ---- 3. motion ----
  V.forEach(el => {
    const s = S(el);
    if (s.animationName && s.animationName !== 'none' && s.animationIterationCount === 'infinite') {
      const spinnerLike = /spin|rotate|loader|load|skeleton|shimmer-load/i.test(s.animationName + ' ' + el.className) || el.matches('[role=progressbar],[aria-busy=true],[data-loading],svg') ;
      add(spinnerLike ? 'infiniteAnimation_maybeLoader' : 'infiniteAnimation', el, s.animationName);
    }
    if ((s.transitionProperty || '') === 'all' && px(s.transitionDuration) > 0) add('transitionAll', el, s.transitionDuration);
    const tf = s.transitionTimingFunction + ' ' + s.animationTimingFunction;
    const bz = tf.match(/cubic-bezier\(([^)]+)\)/g) || []; bz.forEach(b => { const p = b.replace(/cubic-bezier\(|\)/g, '').split(',').map(parseFloat); if (p[1] > 1.1 || p[3] > 1.1 || p[1] < -0.1) add('bouncyEasing', el, b); });
  });

  // ---- 4. spacing on the grid + sibling consistency ----
  const offGrid = {}; let spacingValues = 0;
  V.forEach(el => {
    const s = S(el);
    ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'marginTop', 'marginRight', 'marginBottom', 'marginLeft', 'rowGap', 'columnGap'].forEach(p => {
      const v = px(s[p]); if (!v || v <= 2 || v > 200 || s[p] === 'auto' || s[p] === 'normal') return; spacingValues++;
      const r = Math.round(v * 10) / 10;
      if (r % GRID !== 0) { offGrid[r] = (offGrid[r] || 0) + 1; if (!out.examples.offGrid) out.examples.offGrid = []; if (out.examples.offGrid.length < 6 && !out.examples.offGrid.some(x => x.includes(' ' + r + 'px'))) out.examples.offGrid.push(label(el) + ' ' + p + ' ' + r + 'px'); }
    });
  });
  const offTop = Object.entries(offGrid).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k, n]) => k + 'px×' + n);
  out.craft.offGridSpacing = Object.values(offGrid).reduce((a, b) => a + b, 0);
  out.craft.spacingValuesChecked = spacingValues;

  // siblings that should match (same tag + class list, ≥3 in a row) but differ in padding/height
  const sigOf = el => el.tagName + '|' + (typeof el.className === 'string' ? el.className.trim().split(/\s+/).sort().join(' ') : '');
  let mismatchGroups = 0;
  V.forEach(parent => {
    if (parent.matches('table,thead,tbody,tfoot,tr')) return;   // table cells have no gap to compare
    const kids = [...parent.children].filter(vis); if (kids.length < 3) return;
    const groups = {}; kids.forEach(k => { const g = sigOf(k); (groups[g] = groups[g] || []).push(k); });
    Object.values(groups).forEach(g => {
      if (g.length < 3) return;
      const pads = new Set(g.map(k => ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft'].map(p => Math.round(px(S(k)[p]))).join('/')));
      const rects = g.map(k => k.getBoundingClientRect());
      const rowAligned = Math.max(...rects.map(r => r.top)) - Math.min(...rects.map(r => r.top)) < 4;
      const hs = new Set(rects.map(r => Math.round(r.height))); const gapsY = [], gapsX = [];
      for (let i = 1; i < rects.length; i++) { gapsY.push(Math.round(rects[i].top - rects[i - 1].bottom)); gapsX.push(Math.round(rects[i].left - rects[i - 1].right)); }
      const gapSet = new Set((rowAligned ? gapsX : gapsY).filter(x => x >= 0));
      if (pads.size > 1) { mismatchGroups++; addCraft('siblingPaddingMismatch', g[0], g.length + ' siblings, paddings ' + [...pads].slice(0, 3).join(' | ')); }
      if (rowAligned && hs.size > 1 && Math.max(...hs) - Math.min(...hs) > 2 && g.every(k => !k.matches('p,span,a,li'))) addCraft('siblingHeightMismatch', g[0], g.length + ' side by side, heights ' + [...hs].slice(0, 4).join('/'));
      if (gapSet.size > 1 && Math.max(...gapSet) - Math.min(...gapSet) > 2) addCraft('uneven gaps between siblings', g[0], 'gaps ' + [...gapSet].join('/') + 'px');
    });
  });

  // ---- 4b. controls on one row: same height, radius, border, fill, text size ----
  // A search box, a dropdown and a button sitting side by side are different elements — the sibling check above
  // can't see them. Group every control by the line it sits on and compare what the eye compares.
  const CTL = 'input:not([type=hidden]):not([type=checkbox]):not([type=radio]):not([type=range]):not([type=file]), select, button, [role=combobox], [role=searchbox], [role=spinbutton]';
  const hasBox = el => { const x = S(el); const bg = parseColor(x.backgroundColor); return px(x.borderTopWidth) > 0 || (bg && bg.a > 0.05) || (x.boxShadow && x.boxShadow !== 'none'); };
  const boxOf = el => { let b = el; for (let i = 0; i < 3 && !hasBox(b) && b.parentElement && b.parentElement !== root; i++) b = b.parentElement; return hasBox(b) ? b : el; };
  let ctls = [...new Set(V.filter(el => el.matches(CTL)).map(boxOf))].filter(vis).filter(el => { const r = el.getBoundingClientRect(); return r.height >= 24 && r.height <= 140 && r.width >= 40; });
  ctls = ctls.filter(c => !ctls.some(o => o !== c && o.contains(c)));
  const cr = ctls.map(el => ({ el, r: el.getBoundingClientRect() })).sort((a, b) => a.r.top - b.r.top);
  const taken = new Set();
  cr.forEach(a => {
    if (taken.has(a)) return; taken.add(a); const row = [a];
    cr.forEach(b => { if (!taken.has(b) && Math.abs((b.r.top + b.r.height / 2) - (a.r.top + a.r.height / 2)) < Math.max(a.r.height, b.r.height) / 2) { row.push(b); taken.add(b); } });
    if (row.length < 2) return;
    const els = row.sort((x, y) => x.r.left - y.r.left).map(x => x.el);
    const inner = e => e.matches(CTL) ? e : (e.querySelector(CTL) || e);
    const isField = e => { const i = inner(e); return !i.matches('button,[type=submit],[type=button]') && i.getAttribute('role') !== 'button'; };
    const hs = els.map(e => Math.round(e.getBoundingClientRect().height));
    const rad = els.map((e, i) => Math.round(Math.min(px(S(e).borderTopLeftRadius), hs[i] / 2)));
    const fs = els.map(e => Math.round(px(S(inner(e)).fontSize)));
    const fields = els.filter(isField);
    const bor = fields.map(e => px(S(e).borderTopWidth) + 'px ' + S(e).borderTopColor);
    const fill = fields.map(e => S(e).backgroundColor);
    const spread = a => Math.max(...a) - Math.min(...a);
    const probs = [];
    if (spread(hs) > 2) probs.push('height ' + hs.join('/') + 'px');
    if (spread(rad) > 2) probs.push('corner radius ' + rad.join('/') + 'px');
    if (fields.length >= 2 && new Set(bor).size > 1) probs.push('border differs');
    if (fields.length >= 2 && new Set(fill).size > 1) probs.push('fill differs');
    if (spread(fs) > 1) probs.push('text size ' + fs.join('/') + 'px');
    if (probs.length) addCraft('controlRowMismatch', els[0], els.length + ' controls on one row: ' + probs.join(' · '));
  });

  // ---- 5. centring ----
  const cs2 = V.filter(el => S(el).textAlign === 'center' && ownText(el)).length;
  out.craft.centredTextShare = textBlocks ? Math.round(100 * cs2 / textBlocks) + '%' : '0%';
  // narrow centred column on a wide window
  const main = document.querySelector('main, [role=main]') || root;
  const mr = main.getBoundingClientRect();
  const kids = [...main.children].filter(vis);
  const w = kids.length ? Math.max(...kids.map(k => k.getBoundingClientRect().width)) : mr.width;
  const lm = (kids[0] ? kids[0].getBoundingClientRect().left : mr.left), rm = vw - (kids[0] ? kids[0].getBoundingClientRect().right : mr.right);
  const appLike = !!document.querySelector('nav, aside, [role=navigation]');
  if (vw >= 1100 && w / vw < 0.55 && lm > 120 && Math.abs(lm - rm) < 40) addCraft('narrowCentredColumn', main, Math.round(w) + 'px wide in a ' + vw + 'px window (margins ' + Math.round(lm) + '/' + Math.round(rm) + ')' + (appLike ? ' — app with navigation: should fill the window' : ' — fine only for reading or a single form'));
  // flex/grid centred hero blocks: block whose children all centred and which has ≥2 text children
  V.forEach(el => { const s = S(el); if (/^(flex|inline-flex)$/.test(s.display) && s.flexDirection.startsWith('column') && s.alignItems === 'center' && el.querySelectorAll('h1,h2,h3').length && el.querySelectorAll('p,button,a').length >= 2 && el.getBoundingClientRect().width > vw * 0.5) addCraft('centredStack', el, 'column stack with everything centred'); });

  // ---- 6. identity helpers ----
  const fams = new Set(), sizes = new Set(), weights = new Set();
  V.forEach(el => { if (!ownText(el)) return; const s = S(el); fams.add(s.fontFamily.split(',')[0].replace(/["']/g, '').trim()); sizes.add(Math.round(px(s.fontSize))); weights.add(s.fontWeight); });
  out.craft.fontFamilies = fams.size; out.craft.fontSizes = sizes.size; out.craft.fontWeights = [...weights].sort().join(',');
  const cardish = V.filter(el => { const s = S(el); const r = el.getBoundingClientRect(); return r.width > 140 && r.height > 60 && (px(s.borderTopWidth) > 0 || (s.boxShadow && s.boxShadow !== 'none')) && px(s.borderTopLeftRadius) >= 8 && !!s.backgroundColor && parseColor(s.backgroundColor)?.a > 0.9; });
  const nested = cardish.filter(c => cardish.some(p => p !== c && p.contains(c))).length;
  if (nested >= 2) addCraft('cardsInsideCards', cardish.find(c => cardish.some(p => p !== c && p.contains(c))), nested + ' nested');
  const bigRadius = cardish.filter(c => px(S(c).borderTopLeftRadius) >= 16).length;
  if (cardish.length >= 4 && bigRadius / cardish.length > 0.8) addCraft('allRoundedCards', cardish[0], bigRadius + ' of ' + cardish.length + ' cards radius ≥ 16');

  // ---- summary ----
  const tellKeys = Object.keys(out.tells).filter(k => !/maybeLoader/.test(k));
  out.summary = {
    tellKinds: tellKeys.length,
    tellCount: tellKeys.reduce((a, k) => a + out.tells[k], 0),
    offGridSpacingTop: offTop,
    verdict: tellKeys.length >= 6 ? 'heavy slop — full pass' : tellKeys.length >= 2 || out.craft.offGridSpacing > 8 ? 'light slop — fix what is listed' : 'little or no slop — leave the look alone, fix craft items only',
    note: 'A tell with a reason tied to the product (a mascot, a real brand gradient, a live-status pulse) stays — state the reason. infiniteAnimation_maybeLoader = probably a spinner: check.'
  };
  return out;
})();
