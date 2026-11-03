# Anti-slop — make it look designed, not generated

"Slop" is UI that is technically fine and obviously machine-made: the same grey page, the same white cards, the same blue button, a gradient, a sparkle, a centred hero, copy that shouts. It is not an opinion about taste. It is a **set of measurable tells** plus a **lack of decisions** — every size, space and word is whatever came out first.

The fix is not decoration. It's the opposite: **make every value a decision, keep the chrome quiet, put richness in one or two moments that belong to this product.**

Run this on **every run** (Fix, Polish, Redesign). In Fix it limits itself to spacing, alignment and words. In Polish and Redesign it covers everything. Measure with `scripts/slop-scan.js` before and after.

---

## 1. The craft checks (what to fix first)

These matter more than any trend. Fix them in this order — each one changes how the next reads.

### 1.1 Spacing — one scale, one rhythm
- Every margin, padding and gap is a multiple of **4** (use design.md's scale; 2px nudges inside small controls are fine). No `13px`, `11px`, `mt-[22px]`.
- **Controls on one row are one family.** A search box, a dropdown and a button side by side share **one height** (design.md's control height; befui: `--control-h`, 36px, or `data-density`), **one corner radius, one border, one fill and one text size**. Different heights (a 64px search next to a 78px select) or a tinted search beside white dropdowns reads as three components from three projects. Fix by making all three use the same component tokens, not by nudging pixels. A primary button may differ in fill and weight, never in height or radius. `slop-scan.js` reports `controlRowMismatch` and says which of height / radius / border / fill / text size differs.
- **Same thing, same size.** Rows in a list share one height and one gap. Cards in a row share one padding and one height. Inputs on a row share one height. `slop-scan.js` flags siblings whose padding or height differ.
- **Space shows grouping.** Gap inside a group < gap between groups < gap between sections (e.g. 8 / 16 / 32). Equal gaps everywhere = no structure.
- A section label sits closer to its own content than to what's above it (e.g. 24 above, 8 below).
- Page edges and card padding follow density: compact panels 12–16, cards 20–24, page gutters 16 (mobile) / 24–32 (desktop).

### 1.2 Alignment — things line up, and not everything is centred
- Left-align reading content. Centred text is for **one or two short lines** (a title on an empty state, a single hero line). Never centre paragraphs, form labels, table cells with text, long headings or lists.
- **Don't centre the whole app.** An app or dashboard fills the window like an app: sidebar/rail 240–280 + fluid content (cap ~1440–1600). A narrow centred column with huge empty margins is only right for reading (article, a single form, a settings page ~640–720 wide) and still leaves its own text left-aligned inside.
- One left edge per column: labels, inputs, icons and numbers each line up. Numbers right-aligned in a column, with the same decimals.
- Prefer **asymmetric** composition for hero/overview screens — text on one side, the main object on the other — to the "everything stacked and centred" default.
- Centre-aligning is allowed to *centre an object in a free space* (a loader, an empty-state block, a modal), never as the default alignment of text.

### 1.3 Words — plain and short
- Say what it is or does, in the user's words (`hierarchy-and-naming.md`): "Save changes", not "Submit"; "Leave balance", not "LV BAL".
- Section titles name the content, labels name the field, buttons are verb + object.
- **No hype words** (supercharge, seamless, unlock, magic, revolutionary, game-changing, "AI-powered" on everything). **No exclamation marks** in interface text. No greeting headlines ("Welcome back, Sam! 👋") — name the context instead ("October overview").
- A change says what it compares to: "+12% vs last month", not "+12%".
- Short labels without trailing periods; only real paragraphs keep them. Sentence case, not UPPERCASE tracked labels everywhere.
- Mock/seed data looks real (plausible names, amounts, dates in the product's locale) — never `Lorem`, `John Doe`, `123,456`, `[X]`.
- Claims that can't be checked ("Loved by 10,000+ teams", "10x faster") come out unless the user confirms they're real — list them in the report.

### 1.4 Hierarchy — one thing is loudest
- One primary action per view; one headline value per screen. If everything is bold, nothing is.
- Hierarchy through **size and colour first, weight second.** Two weights (400/500, 600 for rare emphasis). Headings at 700–900 + tight tracking everywhere = tell.
- Text in 3 roles: primary, secondary, muted. Not ten greys.

### 1.5 Navigation — a stranger finds their way
- Current location is obvious (selected state, page title, breadcrumb where depth > 1).
- Group nav by task or noun; section labels closer to their own items; 32–36px rows, icons in one column.
- Every screen has one obvious next step and one obvious way out. Disabled things explain why. (See `dependencies-and-navigation.md`.)

---

## 2. The tells — detect → fix

`slop-scan.js` reports counts and the first examples of each. Treat a tell as a finding only when it has no reason tied to the product's identity.

| Area | Tell (what the scan looks for) | Why it reads as generated | Fix |
|---|---|---|---|
| **Colour** | Hue gradients (violet→blue, pink→orange) on surfaces, buttons or text; gradient text (`background-clip:text`) | The default "AI" palette; says nothing about the product | Flat colour from the palette. A gradient only as a tiny tone shift inside one neutral |
| | Coloured glows / halos (`box-shadow` or `text-shadow` with a saturated colour and blur ≥ 12) | Effects spread over the chrome | Neutral soft shadow, or a 1px border |
| | Purple/indigo as the only accent by default | The most common model default | Accent from the brand or the product's world |
| | Rainbow category colours with no meaning | Decoration | One accent; extra hues only where each means something |
| **Surfaces** | Everything is a card; cards inside cards; every card the same size | Template grid | Rules and spacing for grouping; vary the sizes; one card level |
| | Large radius (≥ 16) on everything, pill buttons everywhere | Trend default | One radius scale chosen for the personality; nested radius = outer − padding |
| **Type** | Weights 700–900 for headings; negative tracking on small text; italic for emphasis | Trendy-heavy | 400/500 (+600 rarely); tight tracking only on large display text |
| | UPPERCASE tracked micro-labels in 3+ places | Instant template | Sentence case; reserve small caps/uppercase for one deliberate role |
| | 7+ font sizes, 3+ families | No scale | 4–6 sizes, 1 family + at most 1 partner |
| **Icons** | Emoji used as icons or in labels/titles (🚀 ✨ 📊) | Emoji = placeholder | One line-icon set, one size and stroke (befui icons if the project uses befui) |
| | An icon in every card title / before every label | Noise | Icons only where they speed recognition |
| **Copy** | Exclamation marks, hype words, greeting headlines, "New ✨" badges | Marketing voice in a tool | Plain sentences (§1.3) |
| | Title Case Everywhere On Buttons | — | Sentence case |
| **Controls** | Search, dropdown and button on one row with different heights, radii, borders or fills | Parts from different components | One control height, radius, border, fill and text size per row (§1.1) |
| **Layout** | Hero/content blocks centred by default; text centred in multi-line blocks | Default flex centring | §1.2 |
| | Equal 3-up or 4-up cards with the same icon-title-text structure | "Features" template | Vary scale and structure; lead with the one that matters |
| | Dead empty bands, tiny content in a huge frame | Unfinished | Fill the viewport like the product it is |
| **Motion** | `animation: … infinite` on things that aren't live (pulse, float, shimmer on headings, gradient shifts) | Decoration | Remove. Keep loops only for real loading or live status |
| | `transition: all`, bouncy springs (overshoot easings), `hover:scale` on cards | Imprecise | Name the properties (colour, background, border, opacity, transform); one easing; ≤ 150–250ms |
| **Content** | Placeholder noise charts, `$123,456` figures, decorative sparklines in every stat card | Fake | Real shape of data or no chart; stat cards = label, figure, comparison |

If a tell has a **reason** (a playful product with a mascot; a gradient that is the real brand; a pulse on a live-status dot) it stays — write the reason in the report. Slop is unjustified, not forbidden.

---

## 3. Uniqueness — one quiet system, one rich moment

Removing slop is half the job. A clean screen that could belong to any product is **the next template**.

- **Quiet chrome.** Navigation, buttons, text, borders: tinted neutrals + one accent. Nothing glows, nothing competes.
- **One rich moment per screen** (two at most), chosen from what the product actually shows: a beautifully drawn main chart, a well-set key figure, a real object (a payment card, a receipt, a machine status plate, a floor plan), a photo from the product's world, a status that feels alive. Put the craft there.
- **One signature detail**, used consistently, that only this product would have (a live status dot for monitoring, keycaps for developer tools, a route line for delivery, a ruled ledger look for accounting).
- **Swap test.** Replace the product name with another product's. If the screen still fits, it's a template: push harder on the copy, the moment and the signature.
- Dashboards: one main chart clearly the biggest thing; anything else is a different kind of thing (ranked list with thin bars, short table), never a second chart of the same size. Stat cards are numbers — label, figure, comparison — not a sparkline in each.
- Don't swap one trend for another (glass, grain, neon, bento) — that's the same slop with a new coat.

Use `library/styles.md` and `visual-design.md` §3 for the direction itself; this file keeps any direction honest.

---

## 4. How much to change — be honest

Read the scan and the screenshots, then classify:
- **Heavy slop** (many tells across colour, type, icons, copy, spacing) → full pass, in Polish/Redesign. Write the identity first (`visual-design.md` §0), get the direction agreed (or default to Polish and say so), then fix in order.
- **Light slop** (mostly designed, a few tells) → fix only those, keep the palette, type and layout. Put bigger ideas in "Options to go further".
- **No slop** → say so plainly. Suggest ≤ 3 small refinements with exact values; apply only if the user agrees. **Never change a good screen just to make it different.**

## 5. Order of passes (for agents)

1. Screenshot + run `slop-scan.js`, `layout-scan.js`, `style-inventory.js` (before numbers).
2. **Spacing** (§1.1) → 3. **Alignment & centring** (§1.2) → 4. **Words** (§1.3) → 5. **Colour** (remove gradients/glows, one ramp, one accent, contrast ≥ 4.5:1) → 6. **Type** (scale, weights, case, tabular numbers) → 7. **Icons** (one set, one size) → 8. **Details** (nested radii, borders, hover/focus/disabled states, charts/stat cards) → 9. **Motion** (remove loops, name transitions) → 10. **The moment + signature** (only in Polish/Redesign).
3. Finish each pass across the whole screen before the next. Screenshot after each.
4. Re-run the scans; every tell without a stated reason should be 0 or explained. Put before → after counts in the report's Details.

Components: if the project is React + Tailwind, prefer befui for the controls (`library/befui.md`) — consistent states, one radius, one motion curve come for free, and the token levers make it look like this product.

---

*The "AI-tells" idea (audit the common signs of generated UI, fix in layered passes, "leave good screens alone") is in the spirit of **unslop** by Damir Sokolovsky (https://heydamir.design/unslop, CC BY 4.0). The rules, checks and scan here are written for ui-fix and extend it with measurable spacing/alignment checks.*
