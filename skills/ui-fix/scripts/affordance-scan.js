// ui-fix: affordance scan — "can a user tell this is clickable?". Run in the page (browser JS tool or Playwright page.evaluate). Read-only.
// Finds everything that acts as a control (button, link, summary, role=button, aria-expanded, cursor:pointer) and checks it
// carries a visible signal: a box (border/fill/shadow), an icon or chevron, link styling (underline/colour), a pill/arrow.
//   expanderNoIndicator   — opens/closes something (aria-expanded, summary, "card header") but has no chevron/plus/caret
//   looksLikeText         — clickable (pointer or role=button) but looks like plain text or a plain label
//   cardNoClickCue        — a big clickable card/row with no arrow, chevron, button or "open" word anywhere on it
//   linkLooksLikeText     — a link with no underline and the same colour as the text around it
//   ghostButtonLooksLikeText — a <button> with no border, fill or icon that reads as a label
// It cannot test hover feedback — walk it: hover each reported item and compare screenshots (walkthrough-and-stress.md).
// Set ROOT to the target's selector, or null.
(() => {
  const ROOT = null;   // e.g. '#settings', 'main'
  const root = (ROOT && document.querySelector(ROOT)) || document.body;
  const S = el => getComputedStyle(el);
  const vis = el => { const r = el.getBoundingClientRect(); const s = S(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0; };
  const px = v => parseFloat(v) || 0;
  const label = el => { const id = el.id ? '#' + el.id : ''; const cl = (typeof el.className === 'string' && el.className.trim()) ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return (el.tagName.toLowerCase() + id + cl).slice(0, 50); };
  const text = el => (el.innerText || '').trim().replace(/\s+/g, ' ');
  const color = c => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(parseFloat); return { r: p[0], g: p[1], b: p[2], a: p[3] == null ? 1 : p[3] }; };
  const sameColor = (a, b) => { const x = color(a), y = color(b); return x && y && Math.abs(x.r - y.r) + Math.abs(x.g - y.g) + Math.abs(x.b - y.b) < 24; };
  const GLYPH = /[▸▾▴▶▼▲›»→↗⌄⌃˅˄＋+−›>]\s*$|^\s*[▸▾▴▶▼▲‹«←＋+−]/;
  const all = [...root.querySelectorAll('*')].filter(el => !el.closest('svg,script,style,template') && vis(el));
  const out = { found: {}, examples: {}, checked: 0 };
  const flag = (k, el, note) => { out.found[k] = (out.found[k] || 0) + 1; (out.examples[k] = out.examples[k] || []); if (out.examples[k].length < 5) out.examples[k].push(label(el) + ' — "' + text(el).slice(0, 32) + '"' + (note ? ' — ' + note : '')); };

  const SEM = 'button,a[href],summary,[role=button],[role=link],[aria-expanded],[aria-haspopup],[onclick]';
  const cands = all.filter(el => {
    if (el.matches('[role=tab],[role=menuitem],[role=option],[role=treeitem],[role=switch],[role=checkbox],[role=radio]')) return false;   // list conventions carry these
    if (el.matches('input,select,textarea,label')) return false;
    if (el.matches(SEM)) return true;
    const s = S(el); return s.cursor === 'pointer' && !(el.parentElement && S(el.parentElement).cursor === 'pointer');
  });
  out.checked = cands.length;

  const pseudoContent = el => ['::before', '::after'].some(p => { const c = getComputedStyle(el, p).content; return c && c !== 'none' && c !== 'normal' && c !== '""' && c !== "''"; });
  const iconIn = el => (el.matches('summary') && S(el).display === 'list-item' && S(el).listStyleType !== 'none') || !!el.querySelector('svg, img, [class*=chevron], [class*=caret], [class*=arrow], [class*=icon], [data-icon]') || [el, ...el.querySelectorAll('*')].some(pseudoContent) || GLYPH.test(text(el));
  const iconNear = el => {   // an icon inside, or a sibling/neighbour inside the same header row
    if (iconIn(el)) return true;
    const p = el.parentElement; if (!p) return false;
    // neighbours only count when they sit on the same line as el (a chevron beside the label), not another card in a stack
    const er = el.getBoundingClientRect(); if (p.children.length > 6) return false;
    return [...p.children].filter(c => c !== el && vis(c)).some(c => { const cr = c.getBoundingClientRect(); const cy = cr.top + cr.height / 2; if (cy < er.top || cy > er.bottom || cr.height > 64) return false;
      return c.matches('svg,img,[class*=chevron],[class*=caret],[class*=arrow],[class*=icon]') || !!c.querySelector('svg,[class*=chevron],[class*=caret],[class*=arrow]') || (!text(c) && c.children.length === 0 && pseudoContent(c)); });
  };
  const bgOf = el => { let e = el; while (e) { const c = color(S(e).backgroundColor); if (c && c.a > 0.05) return S(e).backgroundColor; e = e.parentElement; } return 'rgb(255,255,255)'; };
  const hasBox = el => { const s = S(el); const bw = px(s.borderTopWidth) + px(s.borderBottomWidth) + px(s.borderLeftWidth) + px(s.borderRightWidth); const own = color(s.backgroundColor); const par = el.parentElement ? bgOf(el.parentElement) : 'rgb(255,255,255)';
    return (bw > 0 && color(s.borderTopColor)?.a > 0.1) || (own && own.a > 0.05 && !sameColor(s.backgroundColor, par)) || (s.boxShadow && s.boxShadow !== 'none' && el.matches('button,[role=button]')); };
  const underlined = el => /underline/.test(S(el).textDecorationLine);
  const parentTextColor = el => el.parentElement ? S(el.parentElement).color : S(el).color;

  cands.forEach(el => {
    const s = S(el); const r = el.getBoundingClientRect(); const t = text(el);
    const expander = el.matches('[aria-expanded],summary') || !!el.closest('summary');
    const isLink = el.matches('a[href]');
    const isButton = el.matches('button,[role=button],input[type=button],input[type=submit]');
    const box = hasBox(el) || (el.closest('button') && hasBox(el.closest('button')));
    const icon = iconNear(el);

    if (expander) { if (!icon) flag('expanderNoIndicator', el, 'opens/closes but shows no chevron, plus or caret'); return; }
    if (isLink) {
      const inline = !!el.closest('p,li,td,span,label,div') && S(el).display === 'inline' ;
      if (inline && !underlined(el) && sameColor(s.color, parentTextColor(el)) && !icon) flag('linkLooksLikeText', el, 'no underline, same colour as the text around it');
      return;
    }
    if (isButton) {
      if (!box && !icon && sameColor(s.color, parentTextColor(el)) && !underlined(el)) flag('ghostButtonLooksLikeText', el, 'no border, fill, icon or link colour');
      return;
    }
    // cursor:pointer containers and role=link
    const big = r.width > 280 && r.height > 36;
    if (big) { if (!icon && !/\b(open|view|edit|manage|details|more|show|expand)\b/i.test(t)) flag('cardNoClickCue', el, Math.round(r.width) + '×' + Math.round(r.height) + ' clickable area, no arrow/chevron/button'); }
    else if (!box && !icon && !underlined(el) && sameColor(s.color, parentTextColor(el))) flag('looksLikeText', el, 'pointer cursor but nothing else says "click me"');
  });

  const kinds = Object.keys(out.found);
  out.summary = { clickablesChecked: out.checked, problemKinds: kinds.length, problems: kinds.reduce((a, k) => a + out.found[k], 0),
    verdict: kinds.length ? 'some controls give no sign they are clickable — add the missing signal (chevron / button look / underline) and a hover + focus state' : 'every control checked carries a visible signal',
    note: 'Hover feedback is not measured here: hover each reported item and compare screenshots. Tabs, menu items and form fields are skipped (their conventions carry the signal).' };
  return out;
})();
