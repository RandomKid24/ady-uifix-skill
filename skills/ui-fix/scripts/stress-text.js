// ui-fix: text stress test. Run in the page (browser JS tool or devtools console). Reversible.
// MODE:
//   'expand'      pseudo-localize visible text (+~40% length, accented) — finds truncation/overflow from translation
//   'devanagari'  swap visible labels/buttons for Marathi-length text — finds font/line-height/wrap issues
//   'long-values' fill empty/short text inputs with long realistic values (never submits)
//   'restore'     put everything back
// After expand/devanagari/long-values, take screenshots, then read the returned overflow report.
(() => {
  const MODE = 'expand'; // 'expand' | 'devanagari' | 'long-values' | 'restore'
  const ROOT = null;     // e.g. 'form'
  const root = (ROOT && document.querySelector(ROOT)) || document.body;
  const store = window.__uifixStress = window.__uifixStress || { text: new Map(), values: new Map(), ph: new Map() };

  const setNativeValue = (el, v) => {
    const proto = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, v);
    el.dispatchEvent(new Event('input', { bubbles: true }));
  };

  if (MODE === 'restore') {
    store.text.forEach((v, node) => { if (node.isConnected) node.nodeValue = v; });
    store.values.forEach((v, el) => { if (el.isConnected) setNativeValue(el, v); });
    store.ph.forEach((v, el) => { if (el.isConnected) el.setAttribute('placeholder', v); });
    const n = store.text.size + store.values.size + store.ph.size;
    window.__uifixStress = null;
    console.log(`ui-fix stress: restored ${n} items`);
    return { restored: n };
  }

  const ACCENT = { a: 'á', e: 'é', i: 'í', o: 'ö', u: 'ü', c: 'ç', n: 'ñ', A: 'Å', E: 'É', I: 'Î', O: 'Ø', U: 'Û', C: 'Ç', N: 'Ñ', s: 'š', y: 'ý' };
  const pseudo = s => {
    const core = s.replace(/[aeioucnAEIOUCNsy]/g, ch => ACCENT[ch] || ch);
    const pad = Math.max(2, Math.round(s.trim().length * 0.4));
    return `[${core} ${'·'.repeat(pad)}]`;
  };
  const MR = ['क्षमता निवडा', 'दरवाजा प्रवेश प्रणाली', 'ट्रे सामग्री (एमओसी)', 'कारखाना स्वीकृती चाचणी', 'पॅकेजिंग प्रकार', 'जतन करा', 'होय', 'नाही', 'आवश्यक माहिती भरा'];
  const devanagari = (s, i) => { const base = MR[i % MR.length]; return s.trim().length > 18 ? `${base} — ${MR[(i + 3) % MR.length]}` : base; };

  if (MODE === 'expand' || MODE === 'devanagari') {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: n => {
        const p = n.parentElement;
        if (!p || !n.nodeValue.trim() || /^(SCRIPT|STYLE|NOSCRIPT|OPTION|TEXTAREA)$/.test(p.tagName)) return NodeFilter.FILTER_REJECT;
        if (MODE === 'devanagari' && !p.closest('label, button, legend, h1, h2, h3, h4, h5, h6, th, [role=tab], [class*=label], [class*=title]')) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    let n, i = 0;
    while ((n = walker.nextNode())) {
      if (!store.text.has(n)) store.text.set(n, n.nodeValue);
      const orig = store.text.get(n);
      n.nodeValue = MODE === 'expand' ? pseudo(orig) : devanagari(orig, i++);
    }
    root.querySelectorAll('[placeholder]').forEach((el, k) => {
      if (!store.ph.has(el)) store.ph.set(el, el.getAttribute('placeholder'));
      const o = store.ph.get(el);
      el.setAttribute('placeholder', MODE === 'expand' ? pseudo(o) : devanagari(o, k));
    });
  }

  if (MODE === 'long-values') {
    const LONG = {
      email: 'procurement.department.head@aureole-pharmatech-industries.co.in',
      tel: '+91 98765 43210 ext. 4521',
      url: 'https://vendor-portal.example-industries.co.in/orders/2026/10/very-long-path',
      text: 'Shree Ganesh Precision Engineering & Fabrication Works Private Limited, Unit 2',
      search: 'stainless steel perforated tray 316L electropolished',
    };
    root.querySelectorAll('input[type=text], input:not([type]), input[type=email], input[type=tel], input[type=url], input[type=search], textarea').forEach(el => {
      if (el.disabled || el.readOnly) return;
      if (!store.values.has(el)) store.values.set(el, el.value);
      const kind = el.tagName === 'TEXTAREA' ? 'text' : (el.type || 'text');
      setNativeValue(el, el.tagName === 'TEXTAREA' ? Array(4).fill(LONG.text).join('. ') : (LONG[kind] || LONG.text));
    });
  }

  // overflow report
  const vis = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const clipped = [...root.querySelectorAll('label, button, a, h1, h2, h3, h4, h5, h6, legend, th, td, [role=tab], span, p, div')]
    .filter(el => vis(el) && !el.children.length && (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 4) && /hidden|clip|ellipsis/.test(getComputedStyle(el).overflow + getComputedStyle(el).textOverflow))
    .slice(0, 25).map(el => (el.innerText || '').trim().slice(0, 50));
  const offscreen = [...root.querySelectorAll('*')].filter(el => { const r = el.getBoundingClientRect(); return vis(el) && r.right > innerWidth + 2; }).slice(0, 15).map(el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + ' ' + ((el.innerText || '').trim().slice(0, 30)));
  const result = { mode: MODE, horizontalScroll: document.documentElement.scrollWidth > innerWidth, clippedText: clipped, pastRightEdge: offscreen, next: "Screenshot now, then run with MODE = 'restore'." };
  console.log(JSON.stringify(result, null, 2));
  return result;
})();
