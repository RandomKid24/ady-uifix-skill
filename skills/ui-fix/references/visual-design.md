# Visual design — how it looks, and how it could look better

Read this on **every run**. Usability and layout make a screen work; visual design makes it feel clear, trustworthy and current. A screen can be usable and still look dated, flat, noisy or cheap. Judge that too — and **always come back with concrete visual design suggestions**.

Two kinds of output, never confuse them:
1. **Polish within the system** — required. Use existing tokens and components better: consistent sizes, colours used for the right roles, one radius, clean surfaces. No approval needed.
2. **Design suggestions** — always proposed, applied only on approval. Changes that go beyond the current system: new surface treatment, refined type scale, new component style, new accent use, a different density. Shown as options in the demo; approved ones are written into design.md.

"Follow the design system" means don't change the look *silently*. It never means "have no opinion about the look".

---

## 1. Visual critique — judge these every time

Use the screenshots plus `scripts/style-inventory.js` (counts every distinct font, size, weight, colour, radius, shadow, border and button style on the screen).

| Area | Good looks like | Common problems |
|---|---|---|
| **Typography** | 1 font family (2 max), a clear scale of 4–6 sizes, 2–3 weights, comfortable line-height (1.4–1.6 body), readable body size (≥14px dense UI, ≥16px content) | 8+ sizes in use, sizes 1–2px apart, everything the same weight, cramped line-height, all-caps paragraphs |
| **Colour roles** | Neutral base; **one** brand/accent colour for primary actions and active states; semantic colours (success/warning/danger/info) only for meaning; text in 2–3 greys by importance | Brand colour on everything (every Yes button filled blue), many unrelated colours, colour used decoratively, grey-on-grey low contrast, pure #000 on pure #fff glare |
| **Surfaces & depth** | Page background vs card/panel background clearly separated (subtle tint or border or soft shadow — pick one approach); consistent elevation levels (0/1/2) | Everything white on white with no grouping; heavy borders everywhere; mixed shadows; boxes inside boxes inside boxes |
| **Shape** | One radius scale (e.g. 6 inputs/buttons, 10–12 cards, full for pills), applied consistently | 4–5 different radii; sharp inputs next to rounded buttons |
| **Components** | Buttons: clear primary / secondary / ghost / danger variants, same height as inputs; inputs: one style, clear focus; choice controls look like choices; cards share padding | 3 different button styles doing the same job; filled buttons used for options; inputs and buttons of different heights on one row |
| **Visual weight & emphasis** | The eye lands on the page title, then the primary action; filled/strong styles reserved for what matters | Many equally loud elements (lots of filled buttons, bold text, colour) → nothing stands out |
| **Iconography** | One icon set, one stroke weight, one size per context, aligned to text | Mixed icon styles, emoji next to line icons, icons at random sizes |
| **Density** | Matches the users (compact for daily data entry, comfortable for occasional/public) and consistent across the app | Same screen both cramped and empty; inconsistent padding |
| **Polish** | Pixel-aligned edges, consistent padding inside controls, hover/focus/active states designed, smooth small transitions (150–200ms), no layout jump on load | Off-by-few-pixels alignment, no hover state, abrupt state changes, spinners that shift the layout |
| **Modern & trustworthy** | Current conventions: clear hierarchy, generous but purposeful whitespace, subtle surfaces, readable type, restrained colour | Dated look: heavy gradients, bevels, tiny dense text, harsh borders, default browser controls mixed with styled ones |

Severity: visual problems that hide meaning (can't tell selected state, can't find primary action, low contrast) → 🔴/🟠 under their usability category. Pure aesthetics (looks dated, too many sizes, inconsistent radii) → 🟡 and must still appear in Design suggestions.

## 2. Style inventory targets

From `style-inventory.js`, flag when the screen uses more than:
- font families: 2 · font sizes: 6 · font weights: 3
- text colours: 4 · background colours: 5 (excluding images) · accent/brand colours: 1–2
- border radii: 3 · shadows: 3 · border colours: 3
- button visual styles: 4 (primary, secondary, ghost, danger)

Too many = visual noise and inconsistency. Map each extra value to the design.md token it should be, or propose a token.

## 3. Design suggestions — always include

Every run (including `quick`) ends its report with a **Design suggestions** section. Give **2–3 directions**, each concrete enough to build, each staying recognisably the same product (keep brand colour, logo, overall personality unless the user asks for a rebrand):

```
### Design suggestions

A. Clean & calm (closest to current)
   - Page bg #F7F8FA, sections as white cards, 1px #E6E8EC border, radius 12, padding 24
   - Type: 24/600 page title · 18/600 section · 14/500 label · 14/400 body · 12/400 helper
   - Brand blue only on primary button + selected states; options become outlined segmented controls
   - Why: separates sections without heavy lines; one loud colour so Save stands out

B. Compact pro (for daily data-entry users)
   - 36px controls, 16px field gap, 2-column for short pairs, sticky section index left
   - Subtle zebra on long checklists, keyboard hints on primary actions
   - Why: fits 40% more on screen; fewer scrolls for power users

C. Guided (for occasional / new users)
   - Numbered step headers with icons and one-line descriptions, progress bar on top
   - Larger 44px controls, inline help text under complex fields
   - Why: lowers first-time errors; clearer where you are
```

For each direction: what changes (tokens, components, layout), what stays, who it suits (tie to the Screen brief), and the expected effect. Build each as a view in the demo (**Before / Fixed / Direction A / B / C**) so the user can compare visually, not just read about it. Mark which direction you recommend and why.

If design.md exists, directions should evolve it, not ignore it — say which tokens change. On approval, write the chosen tokens/components into design.md (with a Changelog line) and implement.

## 4. Within-system polish — always apply

Without asking, using existing tokens:
- Collapse near-duplicate font sizes, colours, radii, shadows to the nearest design.md token.
- Give the primary action the primary style and demote everything else that's competing.
- Make choice controls look like choices (selected vs unselected), not like action buttons.
- Equal heights for inputs, selects and buttons on the same row.
- Consistent padding inside cards/sections and inside controls.
- Designed hover / focus / active / disabled states where missing.
- Pick one surface approach (tint vs border vs shadow) per level and apply it everywhere on the screen.
