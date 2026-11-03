# Think like a designer — the universal pass

The scans measure what we already thought of. A real screen will always have problems nobody listed. This pass makes the skill work on **any** screen, stack or platform: **look → think → measure → fix → learn.** Run it on every run; the scans are the measuring tape, not the eyes.

## 1. Look first, before any scan (open critique)

Take the screenshots, look at them, and write 5–10 lines in plain words, **in the order the eye lands**, with no jargon and no checklist:
- What do I notice first? Is that the right thing?
- What would a stranger click first? What would they misunderstand?
- What looks off, uneven, cramped, empty, loud, dead, or "a different project"?
- What looks clickable? What is clickable but doesn't look it?

Don't filter to what a scan can measure. This list is the ground truth the scans must confirm or miss.

## 2. The ten questions — ask them of every region and every element

| # | Question | Catches |
|---|---|---|
| 1 | **What is this for?** | purpose unclear, features nobody needs, wrong screen type |
| 2 | **Can I tell what to do / what's clickable?** | no affordance, hidden actions, unmarked expanders (`affordance.md`) |
| 3 | **Do things that look alike match?** | different heights/radii/sizes/colours/spacing for the same job (`consistency-scan.js`, `slop-scan.js`) |
| 4 | **Is related stuff close and unrelated stuff apart?** | title and description far apart, label far from its field, equal gaps everywhere |
| 5 | **Is the most important thing the most prominent — and is there one primary?** | flat hierarchy, competing buttons, wrong focal point |
| 6 | **Are the words plain, mine and short?** | jargon, codes, hype, vague buttons, same grey for label and help |
| 7 | **What happens at the edges?** | empty, one item, 1,000 items, long text, error, slow, offline |
| 8 | **Can everyone use it?** | keyboard, contrast, touch size, zoom, other languages, right-to-left |
| 9 | **Does it feel like this product — or any product?** | template look, AI tells (`anti-slop.md`) |
| 10 | **Do I know what will happen, and can I undo it?** | destructive actions with no count or confirm, silent saves |

## 3. Sweeps — so nothing is skipped

- **Region sweep.** Split the screen into regions (top bar, navigation, filter row, each card or section, table, modal, footer). Ask the ten questions of each region and write the findings.
- **Pair sweep.** For every set of things that sit together and look alike — a row, a column, a grid, a list — compare size, shape, colour, type, spacing, alignment. *If two things do the same job and differ, one is wrong.* This is the general rule behind "controls on one row", "cards in a row", "icons in a column".
- **State sweep.** For each interactive thing: hover, focus, pressed, disabled, loading, error, empty, long text.
- **Neighbour sweep.** Compare with two or three sibling screens: same job, same pattern, same names?

## 4. Measure every finding — write a probe if no scan covers it

Every finding needs a number or a screenshot. If a scan covers it, use it. If not, **write a probe**: 5–15 lines of JavaScript run with the browser tool / `page.evaluate`, reading `getBoundingClientRect()` and `getComputedStyle()`. Keep it read-only.

```js
// heights of everything on one row
[...document.querySelectorAll('.filters > *')].map(e => [e.tagName, Math.round(e.getBoundingClientRect().height)])
// every distinct value of a property across the page
[...new Set([...document.querySelectorAll('body *')].map(e => getComputedStyle(e).borderRadius))]
// text smaller than 13px
[...document.querySelectorAll('body *')].filter(e => e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(getComputedStyle(e).fontSize) < 13).map(e => e.textContent.trim().slice(0, 30))
// distance between a title and its description
(a => b => Math.round(b.getBoundingClientRect().left - a.getBoundingClientRect().right))(document.querySelector('h3'))(document.querySelector('h3 + p'))
```

## 5. Fix with the root cause, and say why in plain words

Per finding: **what the user sees** → **why it's a problem** → **the fix at component/token level** (one component, not one-off patches) → **how you verified** (number or screenshot, before → after). Use the project's components, then befui for React + Tailwind (`library/befui.md`).

## 6. Learn — the gap check

After measuring, compare the open critique (§1) with what the scans reported. **Any finding the scans missed is a gap.**
1. Turn the probe into a reusable check: save it as `.ui-fix/checks/<name>.js` (one-line header: what it finds and the threshold). Later runs execute every `.ui-fix/checks/*.js` in Phase 4 alongside the built-in scans.
2. Add a line to `.ui-fix/memory.md` → **Learned checks** (name, what it caught, date).
3. If the gap is general (not specific to this product), tell the user in one sentence — "this would be worth adding to ui-fix itself" — and offer a short description they can paste into an issue or hand to the skill's maintainer. Don't edit the installed skill yourself.

## 7. Any platform

| Target | How |
|---|---|
| **Web / Electron / webview** | DOM scans + probes (everything above) |
| **Screenshot only** (no code, no running app) | Work from the picture: sweeps and the ten questions; estimate sizes by pixel measurement (zoom, crop, count pixels) and say they're estimates ±2px; rebuild as static HTML if the user wants a fix demo |
| **Flutter / React Native / native iOS & Android** | Read the source for sizes, paddings, radii and colours of siblings (look for `height:`, `padding:`, `BorderRadius`, `TextStyle`); run on a simulator/emulator and screenshot; compare constants across like widgets; apply the ten questions and sweeps. Flutter web draws on a canvas — scans see nothing, use the source + screenshots |
| **Anything else** | Same method: look → think → measure what you can → state what you couldn't under **Not tested** |

Never claim a check passed that you couldn't run.
