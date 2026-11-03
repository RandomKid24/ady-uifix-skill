# Affordance — can a user tell what is clickable, and what will happen?

If a user has to guess what they can click, the screen is broken, however good it looks. Quiet, minimal styling (no borders, no fills, grey text) removes the signals that say "this is a control". Check every interactive thing for a **visible signal**, a **hover/focus/pressed state**, and a **result they can predict**.

Measure with `scripts/affordance-scan.js` (what's clickable but gives no sign), then **walk it**: hover and tab to each reported item and compare screenshots — the scan can't see hover.

## 1. The signals (a control needs at least one visible one)

| Signal | Use for |
|---|---|
| **A box** — fill and/or border, radius that matches the product's other controls | Buttons, selects, inputs. Primary = filled, secondary = outlined, tertiary = text **with an icon or underline** |
| **An icon or glyph that says what it does** — chevron (opens/closes), plus (adds), arrow (goes somewhere), external-link mark | Expanders, menus, rows that open something, "add" actions |
| **Link styling** — underline or a link colour that differs from body text (and ≥ 3:1 against the text around it) | Links, especially inside sentences |
| **A verb in the label** — "Open", "Edit", "Show advanced options", "Delete oldest logs" | When there's no room for an icon |
| **Cursor + hover** — `cursor: pointer`, and a visible change on hover (fill, border, underline) | All of them. Hover is a bonus, never the only signal — touch screens have none |
| **Focus ring** — visible keyboard focus | All of them (`focus-scan.js`) |

Something that looks like plain text but is clickable is the #1 finding. The reverse is also a finding: a chip or label *styled like a button* that does nothing.

## 2. Expand / collapse (the most-missed case)

A card, row or section that opens and closes **must** show it:
- A **chevron** (▸ closed / ▾ open, or ⌄/⌃) beside the title, at a consistent spot (right edge or left of the title) — it **rotates** with the state so the user can see how to close it again.
- The **whole header row is the button** (`<button aria-expanded aria-controls>`), with hover fill, focus ring, `cursor: pointer`.
- Closed state shows enough to decide: title + one line of what's inside, placed **together** (not a title far left and its description 1,500px away on the right).
- Use a real component: befui `accordion` / `collapsible` (chevron, smooth height, keyboard handled), or the project's own. Never a bare `div` with an `onClick`.
- Ask whether it should be collapsed at all. A single important action ("Delete old logs") hidden behind an unmarked card is worse than showing the field and the button.

## 3. Rows and cards that navigate or open a panel
A big clickable row needs a trailing arrow/chevron (or an "Open"/"View" button), hover fill, and the same treatment on every row of the list. Don't make only the title text the target and leave the rest looking clickable.

## 4. Predictable result
- The label says what happens (verb + object); destructive actions say what is lost and how much ("Delete 500 oldest logs"), and ask for confirmation (befui `alert-dialog` / `popconfirm`) or offer undo.
- Disabled controls look disabled **and** say why (helper text or tooltip).
- Toggles show their state in words or position, not colour alone.

## 5. Fixing it
1. Pick the signal from §1 that matches the job (chevron for expanders, button styling for actions, underline for inline links).
2. Do it in the **component/token**, so every instance changes: one `Collapsible` header, one `Button` ghost variant with an icon, one link style.
3. Add hover, focus-visible and pressed states from the tokens (`--ring`, `bg-secondary`, `bg-primary-soft`).
4. Re-run `affordance-scan.js`; then hover/tab through and screenshot.

## 6. Also check when you see a screen like "Delete old logs"
- Title and description far apart on a wide card → group them (title above description, or `settings-layout`: text left, control right at a sensible width). `layout-and-spacing.md`.
- Field label and help text in the same grey and weight → label darker/heavier than help. `hierarchy-and-naming.md`.
- Input and button on one row with different heights or radii → one control height and radius (`slop-scan.js` → `controlRowMismatch`).
- A destructive red button with no confirmation or count → §4.
