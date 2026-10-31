# Visual hierarchy & naming

Read this on every run. If people can't tell a section title from a field label, or one field name from another, nothing else matters — they're lost before they start.

---

## 1. Levels must look different — at a glance

Every screen has levels. Each level needs its own look, and the difference must be obvious without reading:

| Level | Example | Must look like |
|---|---|---|
| Page title | "New Job" | Biggest, boldest text on the screen |
| Tab / step | "Specifications" | Clearly a navigation control, active one obvious |
| **Section title** | "Tray & Rack", "Documentation" | **Clearly a heading for a group** — not a field label |
| Sub-section (if any) | "Inner tray" | Between section and label |
| **Field label** | "Tray Type" | Small, attached to its field |
| Helper / hint | "Pick capacity first" | Smaller, muted, under the field |
| Value / placeholder | "Select tray type" | Inside the field, placeholder visibly lighter than a real value |

**Rules for section vs field label (the most common failure):**
- Size: section title at least **1.25× the label size** (e.g. label 14px → section 18px+), **and** a heavier weight, or a distinct style (uppercase eyebrow, color, icon).
- Size alone isn't enough if the difference is under ~25% — add weight, color, a divider, or a container.
- **Group the fields visually**: each section in a card/panel, or separated by a divider line, or a `<fieldset>` with a `<legend>`.
- **Spacing**: space above a section title ≥ **2×** the space between fields in a section. Fields inside a section sit close together; sections sit far apart (law of proximity).
- Optional but strong: a one-line description under the section title ("What the customer gets with the machine").

Use the design.md type scale. If design.md has no section-heading style, propose one (Step 9).

**Tests:**
- **Squint test** — look at the screenshot blurred/zoomed out. Can you count the sections? Can you tell where one ends and the next starts? If not → 🔴.
- **Heading scan** — read only the section titles top to bottom. Do they read like a table of contents for the form?

Measure it — run `scripts/hierarchy-scan.js` in the browser. It reports the computed font size/weight/color of headings vs labels and flags levels that are too close.

## 2. Names must be distinct and self-explanatory

**Label-only test:** read only the field labels, top to bottom, as someone who has never seen this app. For each one: do I know what to enter? Could I confuse it with another field?

Flag and fix:
- **Section and field with the same name** — "Packaging" → field "Packaging". The field must say *what about* packaging: "Packaging type", "Packing material", "Crate required". 🟠
- **Near-duplicate labels** — "Tray Type" / "Tray MOC" / "Tray Master" / "Tray Details": if a user can't instantly say how they differ, rename so the difference is the first word they read, or add a helper line. 🟠
- **Repeated prefix inside a section** — under "Tray & Rack", every label starting with "Tray" adds noise; keep the prefix only where needed to tell tray fields from rack fields. Under a "Tray" section, "Type" alone may be fine; under a mixed "Tray & Rack" section, keep "Tray type" / "Rack qty".
- **Abbreviations and codes** — MOC, Qty., DQ/IQ/OQ/PQ, HMI: spell out, code in brackets: "Tray material (MOC)", "Rack quantity", "Qualification documents (DQ, IQ, OQ, PQ)". Domain experts lose nothing; new staff stop guessing. 🟠
- **Vague labels** — "Details", "Info", "Data", "Type", "Other", "Remarks" with no subject. 🟠
- **Yes/No questions without a question** — "Data Required" + Yes/No: required for what? Rewrite as a question: "Include qualification data with the documents?" 🟠
- **Same thing, different names across screens** — list says "Job", form says "Order", PDF says "Work order". Pick one (check design.md / existing screens) and use it everywhere. 🟡
- **Masters vs records** — "Tray Master" (the list of tray types you manage) vs "Tray" (the one chosen on this job). In forms, label by what the user is choosing ("Tray type"), never by the master's table name. Where master data can be managed, link to it explicitly: "Manage tray types →". 🟠
- **Truncated labels** ("Third Party Senso…") — 🔴 if the user can't know the field; fix layout (wrap, wider column, shorter clear label), never rely on a tooltip.

Write a **Rename table** for every change: Current label · New label · Why.

## 3. Placeholders & values

- Placeholder says what to pick: **"Select tray type"**, not "Select" / "Choose" / "--". Placeholder never replaces the label.
- Placeholder colour is visibly lighter than real values but still readable (≥ 4.5:1 is ideal; ≥ 3:1 minimum).
- **No fake values**: "NA", "-", "0", "N/A" typed into fields as defaults. If a field doesn't apply, either hide it (conditional on another field), disable it with a reason, or leave it empty with an explicit "Not applicable" option. A number field must not hold text. 🟠
- List-type values typed as text ("DQ, IQ, OQ, PQ") → checkbox group or multi-select chips. 🟠

## 4. Choices must look like choices

- Yes/No (and other 2–4 option) button groups must show a **clearly selected state** (filled/colored, check icon) and an obvious unselected state, and look different from action buttons (Save, Add). If nothing is selected by default, it must be obvious nothing is selected yet. 🔴 if you can't tell the current value.
- Prefer a real radio group / segmented control (with `role="radiogroup"` and arrow-key support), or a toggle/checkbox for single on/off.
- Grouped choices sit next to their label, aligned with other fields in the section.

## 5. Layout consistency

- Fields in a row should be related (Tray type + Tray material is fine; Protocol + Third-party sensor is not).
- Consistent widths for similar fields; short inputs (qty, yes/no) shouldn't stretch full width while long ones are cramped.
- Columns align; labels line up; no field half off-screen at common widths (check 1280px and 375px).

---

## What to report

Add to the issue list, and include:
1. **Hierarchy table** — level · font size · weight · color · spacing above (from `hierarchy-scan.js`), with "too close" flags.
2. **Rename table** — current label · new label · why.
3. Squint-test result in one line.
