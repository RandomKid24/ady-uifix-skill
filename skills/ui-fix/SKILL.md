---
name: ui-fix
description: Audit and fix any page, form or UI component against the project's design.md, with real screenshots, automated checks, a usability score and a before/after demo. Use when the user says a screen, form, table, modal or component looks wrong, is confusing, or needs fixing, or runs /ui-fix.
---

# UI Fix

The user points at something that looks or works wrong. It can be anything: a full page, a form, a table, a dashboard, a modal, a single button, a mobile screen. Your job:
1. Check it against the project's design system (design.md).
2. See it for real (screenshots) and measure it (automated checks + score).
3. Tell them bluntly what's wrong.
4. Fix it at the right level (component vs page) in their stack.
5. Show a before/after demo with scores so they can SEE and compare the result.
6. Keep design.md growing so the next fix stays consistent.

The bar for every fix: **a first-time user with zero context knows what this screen is, what to click, and what happens next — without thinking.** If someone could hesitate, misclick, or get stuck, it's not fixed.

## Mindset — think like the best UI engineer on the team

- **Not broken ≠ good.** A screen that works but makes people think, scroll, guess or click twice is a screen to fix. Judge by how fast and confidently a new user gets the job done, not by whether anything throws an error.
- **Effort is the enemy.** Every field, click, decision and tab costs the user. Your best fixes remove work: derive it, default it, defer it, or delete it.
- **"Keep my look" means keep the design system** — colors, fonts, spacing, components, layout style. It never means keep usability problems. Fix 🔴 and 🟠 issues using the existing tokens and components.
- **Be opinionated, then let the user choose.** Fix what's required; propose the bigger upgrades clearly, show them in the demo, and let the user say yes or no.
- **Never present a weak run as a clean bill of health.** If the screen still has problems after your fix, say so plainly, with the score.

Bundled files (paths relative to this SKILL.md):
- `references/understand-the-screen.md` — **read this on every run**: purpose, users, data in/out, flow, element inventory, primary task path, Screen brief
- `references/hierarchy-and-naming.md` — **read this on every run**: section titles vs labels, squint test, label-only test, duplicate/similar/vague names, abbreviations, placeholders, fake values, choice states
- `scripts/hierarchy-scan.js` — run in the browser: measures heading vs label styles and spacing, finds duplicate/similar/truncated labels, generic placeholders, "NA" values, choice groups with no visible selection
- `references/dependencies-and-navigation.md` — **read for any form with dependent fields or 4+ sections**: parent→child links, hide vs disable, numbered sections, section index, icons
- `scripts/dependency-scan.js` — run in the browser (local/dev only): flips each Yes/No, radio, checkbox and small select, maps which fields get hidden/disabled/required/changed, checks the child sits next to its parent, finds greyed-out fields with no reason, restores original values
- `references/forms-and-data-entry.md` — **read this for any form, wizard, settings page, or data-entry screen** (input choice, dropdowns, effort table, flow, validation)
- `scripts/token-scan.mjs` — finds hardcoded colors/sizes/inline styles (design-token drift)
- `scripts/axe-run.js` — paste into the browser to run axe-core accessibility checks
- `references/design-md-template.md` — template for generating a missing design.md

## Modes

Pick from the user's wording; default to `fix`.
- `quick` — audit + score + report only. No code changes.
- `fix` — full flow below (default).
- `sweep` — audit every page/form/component in a folder or route group. Produce one ranked table (target, score, 🔴/🟠/🟡 counts, top issue), then fix the worst ones or the shared root causes first. Ask before editing more than ~5 files.

---

## Step 1 — Find design.md (always first)

design.md holds the system's current design decisions. Every fix must follow it.

Search case-insensitively: `design.md` at repo root, then `docs/`, `.design/`, `design/`, `src/`, `frontend/`, `client/`, then any `*design-system*.md` or `*style-guide*.md`.

Read the whole file. Note: tokens (colors, fonts, type scale, radius, spacing, shadows), component rules, layout rules, states, copy/voice rules, target users, anything deprecated.

**If not found — say so up front:**
> ⚠️ No design.md found in this project. I'll infer the system from the code for now. I can also generate a design.md so every future fix stays consistent — want that?

Fall back to `tailwind.config.*`, `:root` CSS variables, theme files (MUI/Chakra/shadcn/Flutter ThemeData), and the 2–3 most-used existing components. List what you inferred so the user can correct it.

If the user says yes (or in `sweep` mode), **generate design.md** from `references/design-md-template.md` (see Step 9).

If design.md contradicts the code, design.md wins — flag the contradiction.

## Step 2 — Understand the screen (before judging anything)

Read `references/understand-the-screen.md` and do all of it. You can't fix a screen you don't understand.

- Find and read the actual source, plus child components, shared styles, form schema/validation, **the API/endpoint it calls, the backend handler and the model/table it writes**.
- Classify the target: page / form / table-or-list / dashboard / modal / navigation / single component / mobile screen. Step 4 checks depend on this.
- Work out:
  - **Purpose** — one sentence: "<who> uses this to <do what> so that <outcome>", and the job type (Create / Edit / Review / Look up / Monitor / Configure / Bulk / Read / Convert). The job type decides what "good" means.
  - **Users** — roles, how often they use it, device/setting, domain knowledge, language.
  - **What it does** — data in, data out, business rules, side effects, field dependencies.
  - **Flow** — where users come from, where they go after, related screens.
  - **Element inventory** — every element with its purpose, data, required, frequency. Flag elements with no clear purpose, unclear labels, wrong prominence, duplicates.
  - **Primary task path** — the shortest real path to finish the main job, with step and click count.
  - **UI ↔ backend mismatches** — required on server but not marked, collected but ignored, backend-only validation, hardcoded options that should be master data. Report these as issues.
- Output the **Screen brief** (format in the reference) before the audit. If something in it is a guess that would change the fix, ask one short question; otherwise state the assumption and keep going.
- If it's ambiguous which file, ask one short question. Otherwise start.

Every finding later must tie back to the brief: why it hurts **this** user doing **this** job.

## Step 3 — See it for real

If any browser is available (built-in browser, Claude in Chrome, Playwright/Puppeteer via the shell), use it:

1. Get the app running. Use the existing dev server if one is up; otherwise start it with the project's own command (`npm run dev`, `python manage.py runserver`, `flutter run -d web-server`, etc.). Don't install new frameworks to do this.
2. Navigate to the target. If it needs login, use test credentials from the project's seed/fixture/env-example files, or ask the user. Only run against local/dev/staging — never production.
3. Screenshot at **desktop (~1440px)** and **mobile (375px)**. Also capture key states you can trigger: empty submit on forms, hover/focus on the primary button, empty and error states if reachable.
4. Save as `ui-fix/before-desktop.png`, `ui-fix/before-mobile.png`, etc.

If no browser is available or the target can't run (e.g. native app), say so in one line and work from the code and any screenshot the user gave.

## Step 4 — Audit

### 4a. Automated checks (facts, not vibes)

**Accessibility — axe-core.** In the browser, run the contents of `scripts/axe-run.js` (set `TARGET` to the target's CSS selector, or leave `null` for the whole page). It returns violations with impact, rule, node count, and a sample selector. Or use the CLI if available: `npx @axe-core/cli <url>`. Record actual numbers (e.g. "contrast 2.8:1, needs 4.5:1").

**Hierarchy & naming.** In the browser, run the contents of `scripts/hierarchy-scan.js` (set `ROOT` to the target's selector). It returns: section-title vs field-label size/weight ratios (flags anything under 1.25× without extra weight/color), gap above sections vs gap between fields, labels equal to their section name, duplicate and similar labels, abbreviations, vague labels, truncated labels, generic placeholders ("Select"), fake values ("NA", "-"), and choice groups with no visible selected state. Without a browser, check the same things from the code and screenshots.

**Dependencies.** On forms, also run `scripts/dependency-scan.js` (local/dev/staging only — it clicks choices, never Save/Submit, and restores them). Combine with a code search for conditions on other fields (`disabled={!x}`, `watch()`, `v-if`, `required_if`, effects that reset fields). Output the **Dependency map**: Parent · Value · Child · Effect · Visible link? · Layout.

**Design-token drift:**
```bash
node <skill-dir>/scripts/token-scan.mjs <target files or folders> [--json]
```
It reports hardcoded hex/rgb/hsl colors, raw px values, Tailwind arbitrary values (`p-[13px]`, `text-[#333]`), and inline visual styles, with file:line. Map each finding to the design.md token it should be. If Node isn't available, grep for the same patterns.

**Measure in the browser where possible:** tap targets under 44×44px, horizontal overflow at 375px (`document.documentElement.scrollWidth > innerWidth`), elements with no accessible name.

### 4b. Manual review

Use the screenshots plus the code. Only report real problems.

**A. Design-system drift** — wrong tokens, fonts, spacing, one-off components where a system component exists, deprecated patterns.

**H. Hierarchy & naming (check first — read `references/hierarchy-and-naming.md`)**
- **Squint test** on the screenshot: can you count the sections and see where each starts and ends? Section titles that look like field labels → 🔴.
- **Heading scan**: section titles alone read like a table of contents.
- **Label-only test**: read just the labels as a stranger. Section and field with the same name ("Packaging" → "Packaging"), near-identical names (Tray Type / Tray MOC / Tray Master), codes and abbreviations (MOC, Qty., HMI), vague labels ("Data Required" — required for what?), master-table names used as labels, truncated labels → fix each with a Rename table.
- Placeholders say what to pick ("Select tray type"); no fake values ("NA") in fields; list values typed as text → multi-select.
- Choice groups (Yes/No etc.) show a clear selected state and don't look like action buttons.

**I. Dependencies & way-finding (read `references/dependencies-and-navigation.md`)**
- Every child field sits right under its parent and looks attached (indent, connector, shared box). Child in another column → 🟠; in another section/tab → 🔴.
- Child that's meaningless when the parent is off → hide it and reveal on change. If kept disabled, it must say why ("Turn on Door Access System to choose a type"). Silent grey boxes → 🟠.
- Parent change clears/re-filters the child and says so; hidden values never get submitted; required follows visibility.
- Many Yes/No feature toggles in one section → a checklist of features, each expanding its own details.
- 4+ sections or long scroll → numbered, specific section titles (no "Other"/"Misc"), sticky section index with current section and completion, tabs showing missing-field counts, section icons from the project's icon set (icon + text, never icon-only).

**B. The zero-context user test (most important)**
- What is this screen? Clear title? Would someone know where they are?
- Exactly ONE obvious primary action, visually dominant. Secondary actions quieter. Destructive actions separated, styled as dangerous, with confirmation.
- Labels say what happens ("Save invoice", "Add employee") — not "Submit", "OK", "Click here", or unlabeled icons.
- Clickable things look clickable; non-clickable things don't.
- Clear visual hierarchy; no wall of equal-weight stuff.
- No jargon, internal codes, or unexplained abbreviations for these users.
- A way out: back, cancel, close, breadcrumbs. Leaving doesn't silently lose work.
- Every action gives visible feedback.

**C. Checks by target type** — run only what applies:
- **Forms & data entry:** read `references/forms-and-data-entry.md` and apply all of it. At minimum: measure the Effort table; check every field can't be derived/defaulted/deferred; right control type per field (radio/segmented for 2–4 options, searchable select for 10+, units as suffix, etc.); dropdown option order, readable labels (no bare codes), placeholder contrast, dependent dropdowns; required-first grouping and sections; tabs show where errors/missing fields are; keyboard flow; on-blur validation, error summary that jumps to the field; no lost work.
- **Tables / lists:** search; filters; sorting; sticky header on long tables; pagination or virtual scroll; row actions visible (not hover-only); bulk actions if users act on many rows; numbers right-aligned; usable mobile layout (cards or horizontal scroll with pinned first column); useful empty state.
- **Dashboards:** most important number first; every metric labelled with unit and period; charts have titles and legends; no decoration without data.
- **Modals / dialogs:** clear title; one primary action; Esc and a close button work; focus trapped and returned; not used for things that should be a page.
- **Navigation:** current location highlighted; labels match page titles; reachable on mobile.
- **Single components:** every state designed (default, hover, focus, active, disabled, loading, error); works at the sizes it's used at; matches the system component it duplicates.
- **Heavy data-entry / staff screens:** keyboard-only flow works; shortcuts for frequent actions; no mouse-only steps; large targets for touch or shop-floor use; labels in the users' language where design.md or the client calls for it.
- **Public / consumer screens:** value is obvious in seconds; one call to action; trust signals near it; fast on mobile.

**D. States** — loading, empty (with a next-step action, not just "No data"), error (with retry), disabled (with reason), success. Flag every missing one.

**E. Accessibility** — merge axe results with what you see: contrast, focus visibility, keyboard use, aria-labels on icon buttons, color never the only signal.

**F. Responsive** — from the 375px screenshot: cramped, overflowing, overlapping, tiny targets, unusable modals.

### Severity
- 🔴 **Broken / blocks users** — someone will get stuck, misclick, or lose data
- 🟠 **Confusing** — slows people down or makes them guess
- 🟡 **Off-system / polish** — design.md drift, inconsistency

### 4c. Root cause — component or page?

For each issue, check where it actually lives:
- If it comes from a **shared component** (Button, Input, Table, Modal, Layout, theme), mark it as root-cause. The fix goes in that component, not the page.
- Then **sweep**: search the codebase for other screens using the same component or repeating the same bad pattern (same hardcoded color, same "Submit" label, same placeholder-as-label). List them as "also affected".

## Step 5 — Score

Score the target 0–100. Each category starts at its max; subtract per issue in that category (🔴 −8, 🟠 −4, 🟡 −2), floor at 0.

| Category | Max |
|---|---|
| Clarity, hierarchy, naming & way-finding (H + I + B) | 25 |
| Type-specific usability (C) | 20 |
| States & feedback (D) | 15 |
| Accessibility (E + axe) | 15 |
| Design-system adherence (A + token scan) | 15 |
| Responsive (F) | 10 |

Show the per-category breakdown. After the fix, re-score honestly with the same rules — no points for things you didn't actually fix.

**Always show the score**, before and after, in every run — even when the changes are small. A small change with a low after-score is important information.

For forms with dependent fields, always include the **Dependency map**.

Always include the **Hierarchy table** (level · size · weight · spacing, from hierarchy-scan) and a **Rename table** (current label · new label · why) whenever any label changes.

For forms and data-entry screens, also show the **Effort table** (fields, required, dropdowns, decisions, clicks to complete, typing, tabs) before → after. See the forms reference.

## Step 6 — Report (blunt, short)

Talk like a straight-talking senior designer. Direct, some attitude is fine, no fluff. Each issue = what's wrong + why it hurts the user + where (file:line) + evidence (axe rule, measured value, or screenshot).

Start with the Screen brief (from Step 2), then the issues:

```
## <target> — score 48/100
Purpose: Sales coordinators create a manufacturing job for a confirmed order. Daily use, desktop.

🔴 1. Primary action is invisible — "Save" is a grey ghost button next to a bright red "Delete". Users will hit the wrong one. (EmployeeForm.tsx:142)
🔴 2. Placeholders used as labels — type one character and the field name is gone. axe: label ×6.
🟠 3. "Submit" tells nobody anything. It creates an employee — say "Add employee".
🟡 4. #1a73e8 hardcoded ×6 — design.md says --signal.

**Root cause:** 1 and 2 come from components/ui/Input.tsx and Button.tsx — also affected: LeaveForm, ExpenseForm, VendorForm.

**Verdict:** Usable if you built it. Anyone else is guessing.
```

In `quick` mode, stop here.

## Step 7 — The fix

Split the work into two tiers and say which is which:

- **Required fixes — always do these.** Every 🔴 and 🟠 issue. Using the existing design system, even if the user said "keep my look". The only acceptable reason to leave one is a real blocker (needs a backend/API change, needs a product decision, needs data you don't have) — state the blocker per issue.
- **Recommended upgrades — propose, show, ask.** Bigger improvements that change how the screen works: reordering or regrouping fields, swapping control types, splitting a long tab into sections or steps, deriving/defaulting fields, presets, "copy from previous". Show them in the demo (as a second "Upgraded" variant if needed) with the effort/score gain, and apply them only when the user says yes — unless they already asked for a full redesign.
- 🟡 polish items may be left out, but list them.

Then:
- Fix **root causes first**, in the shared component, then page-specific issues. Order: 🔴 → 🟠 → 🟡.
- When changing a shared component, check every place it's used still looks right; keep its props API backward compatible, or update all call sites.
- For "also affected" screens: if the component fix covers them, say so. If they need their own edits, list them and ask before editing more than ~5 files.
- Write in the project's actual stack and conventions. Use design.md tokens and system components only. If design.md has no answer, don't invent silently — see Step 9.
- Don't redesign what isn't broken. Keep business logic, API calls and data flow intact.
- With file access, apply edits directly (or as a diff if the user wants to review). Otherwise give complete, paste-ready code for every file touched.
- Add a change list: each change → which numbered issue it fixes.

## Step 8 — Verify + demo (required)

**Verify for real when you can:** after applying the fix, reload in the browser, take the same screenshots (`ui-fix/after-desktop.png`, `ui-fix/after-mobile.png`), re-run axe and the token scan, and re-score. If something still fails, fix it and check again before showing the user.

**Build a single self-contained HTML demo** (`ui-fix/demo-<target>.html`):
- **Before / After side by side** (stacked on mobile), each with its **score badge** and per-category bars. If you proposed recommended upgrades, add a third **Upgraded** view so the user can compare Before / Fixed / Upgraded.
- For forms: the Effort table under each view, and a live After that really behaves — searchable selects filter, dependent fields reveal under their parent when switched on, defaults pre-filled, error summary jumps to fields, section index highlights and jumps.
- If real screenshots exist, show them (embedded as data URIs) with a desktop/mobile toggle.
- A **live, interactive After** rebuilt in HTML with the real design.md tokens as CSS variables: hover/focus states, primary button shows loading → success, empty submit shows inline validation, toggles for empty/error/loading states.
- Numbered callout badges on the After side matching the issue numbers in the report.
- An "Automated checks" panel: axe violations before → after, hardcoded values before → after.
- Realistic sample data, no lorem ipsum. No dependencies except CDNs/fonts; must open by double-clicking.

Deliver it the best way the environment allows: a published artifact or inline preview if available; otherwise save the file and say where it is.

For native/Flutter/mobile targets, build the interactive After as a phone-width HTML mock.

## Step 9 — Keep design.md growing

**When design.md is missing**, generate it from what's in the code using `references/design-md-template.md`. Mark anything inferred rather than confirmed with `(inferred)` so the user can check it.

**When design.md exists but has no answer** for something the fix needed (a new state, a component variant, a table pattern):
- Propose the exact rule to add, in design.md's own format.
- With the user's OK (or if they asked for it up front), append it to the right section and add a dated Changelog line: `- YYYY-MM-DD: added <rule> (from ui-fix on <target>)`.
- Never rewrite or delete existing design.md rules on your own — propose, don't impose.

## Step 10 — Wrap up

End with:
- Score before → after, in one line (and Effort before → after for forms).
- Recommended upgrades not applied yet, each with its expected gain — ask which ones to do.
- What changed, in one line.
- Also-affected screens fixed vs still pending.
- Anything you couldn't fix and why (needs backend, needs a product decision).
- design.md additions made or proposed.

---

## Don'ts
- Don't skip the design.md check, ever.
- Don't judge a screen before you know what it's for and what it does — Screen brief first.
- Don't call a screen fine if section titles look like labels or two names can be confused — that's the first thing a new user hits.
- Don't invent a new visual style — follow the system.
- Don't give a fix without a demo.
- Don't inflate the after-score.
- Don't treat "keep my look" as "change nothing visible" — keep the system, fix the problems.
- Don't leave a 🔴 or 🟠 unfixed without naming the blocker.
- Don't run against production.
- Don't explain UX theory. Say what's wrong, prove it, fix it, show it.
- Don't touch unrelated files or logic.
