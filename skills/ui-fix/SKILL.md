---
name: ui-fix
description: Audit and fix any page, form, table or UI component like a senior UI engineer — understands what the screen is for, walks it as real users, measures it (accessibility, hierarchy, naming, dependencies, keyboard, stress), fixes it against the project's design.md, proves the fix with before/after scores and visual regression, and remembers decisions per project. Use when a screen looks wrong, is confusing, hard to use or needs fixing, or on /ui-fix.
---

# UI Fix

The user points at something: a page, a form, a table, a dashboard, a modal, one component, a mobile screen. You make it **obviously usable** — then prove it.

**The bar:** a first-time user with zero context knows what this screen is, what to click, and what happens next, without thinking. A daily user finishes the job in the fewest steps. Nobody loses work. If anyone could hesitate, misclick, get stuck, or repeat work, it isn't fixed.

## Mindset

- **Not broken ≠ good.** Judge by how fast and confidently real users get the job done, not by whether anything errors.
- **Understand before you judge.** Know what the screen is for, who uses it, and what it does to the data before calling anything wrong.
- **Evidence over opinion.** Every finding has proof: a measured number, a scan result, a screenshot, a walkthrough step. Tag it with the principle it breaks.
- **Effort is the enemy.** Remove work: derive, default, defer, delete.
- **"Keep my look" = keep the design system**, never keep the problems. Fix with existing tokens and components.
- **Fix the root.** Shared component first; then everything it touches is fixed too — and re-checked.
- **Prove it, lock it, remember it.** Re-measure after, guard against regressions, record decisions so the next run is smarter.
- **Opinionated, then the user chooses.** Required fixes get done; bigger upgrades get shown and approved.
- **Never call a weak result good.** Report the honest after-score.

## Bundled files (paths relative to this SKILL.md)

Read the reference before the phase that uses it. Load only what the target needs.

| File | When |
|---|---|
| `references/understand-the-screen.md` | Every run — Phase 1 |
| `references/hierarchy-and-naming.md` | Every run — Phase 4–5 |
| `references/walkthrough-and-stress.md` | Every run — Phase 3 (+ stress & consistency) |
| `references/prove-and-remember.md` | Every run — impact ranking, Phase 7–8, definition of done |
| `references/forms-and-data-entry.md` | Forms, wizards, settings, data entry |
| `references/dependencies-and-navigation.md` | Dependent fields, or 4+ sections / long scroll |
| `references/design-md-template.md` | When design.md is missing |
| `scripts/axe-run.js` | Browser — accessibility (axe-core) + tap targets + overflow |
| `scripts/hierarchy-scan.js` | Browser — heading vs label styles, spacing, confusing names, placeholders, fake values |
| `scripts/dependency-scan.js` | Browser, dev only — flips choices to map dependent fields |
| `scripts/focus-scan.js` | Browser — tab order vs visual order, focus visibility, keyboard-unreachable clickables |
| `scripts/stress-text.js` | Browser — pseudo-localization, Devanagari, long values; reversible |
| `scripts/token-scan.mjs` | Shell (Node) — hardcoded colors/sizes/inline styles |

Browser scripts: run the file's contents with the browser's JS tool (or Playwright `page.evaluate`). Each has a `ROOT`/`TARGET`/`MODE` constant at the top to set first.

## Modes

Pick from the user's wording; default `fix`.
- `quick` — Phases 0–5 (understand, see, walk, measure, judge) + report. No code changes.
- `fix` — everything.
- `sweep` — run Phases 0–5 on every screen in a folder/route group → one ranked table (screen, score, Impact-weighted issue count, top issue, shared root causes). Then fix shared root causes first, then the worst screens. Ask before editing more than ~5 files.
- `handoff` — like `quick`, then output a paste-ready implementation prompt for another coding agent (format in `prove-and-remember.md`).

## Safety

- Run the app and scripts on **local / dev / staging only**. Never production. Never submit real data. `dependency-scan.js` and walkthroughs click choices — never Save/Submit/Delete unless the data is disposable and you say so.
- Don't change business logic, API payloads, permissions or unrelated files.
- Never rewrite or delete existing design.md rules or memory decisions on your own.

---

## Phase 0 — Remember & ground

1. Read **`.ui-fix/memory.md`** if it exists (format in `prove-and-remember.md`). Follow its Decisions, don't re-propose its Rejected items, use its Glossary names. Create it at the end of the first run.
2. Find **design.md** — case-insensitive: repo root, `docs/`, `.design/`, `design/`, `src/`, `frontend/`, `client/`, then `*design-system*.md`, `*style-guide*.md`. Read it fully: tokens, type scale, spacing, components, states, copy rules, icons, users, deprecated.
   - **Missing →** say so up front:
     > ⚠️ No design.md found. I'll infer the system from the code for now (Tailwind config / CSS variables / theme / most-used components). I can generate a design.md so every future fix stays consistent — want that?
     List what you inferred. Generate from `references/design-md-template.md` if the user agrees (or in `sweep`), marking guesses `(inferred)`.
   - design.md vs code conflict → design.md wins; flag it.
3. Note the project's stack, component library, icon set, and test/lint setup — fixes and guards must use them.
4. Run artifacts go in `.ui-fix/runs/<YYYY-MM-DD>-<target-slug>/`.

## Phase 1 — Understand the screen

Do everything in `references/understand-the-screen.md`. Read the source, children, shared styles, form schema, **the API it calls, the backend handler and the model it writes**. Produce the **Screen brief**: purpose ("<who> uses this to <do what> so that <outcome>"), job type, users (role, frequency, device, domain knowledge, language), data in/out, business rules, side effects, flow (from → here → next), element inventory, primary task path (steps + clicks), UI↔backend mismatches, assumptions.

If a guess would change the fix, ask one short question; otherwise state the assumption and continue. Every later finding must tie back to the brief.

## Phase 2 — See it for real

If any browser is available (built-in browser, Claude in Chrome, Playwright via the shell):
1. Use the running dev server or start it with the project's own command. Don't install new frameworks for this.
2. Open the target. Log in with test credentials from seed/fixture/env-example files, or ask.
3. Screenshot desktop (~1440) and mobile (375), plus states you can trigger (empty submit, focus, hover, empty/error/loading if reachable). Save to the run folder as `before-*.png`.

No browser or not runnable (native app) → say so in one line; work from code + any screenshot given, and do the walkthroughs and stress tests mentally.

## Phase 3 — Walk it as real users

From `references/walkthrough-and-stress.md`:
- **Persona walkthroughs** on the primary task path — always **Newcomer** and **Keyboard-only** (run `focus-scan.js` first), plus whichever of Power user / Touch / Low vision (200% zoom) / Regional language / Interrupted match the brief. Include the 5-second test and first-click test. Log every friction point (hesitation, wrong click, dead end, backtrack, repeat work, surprise, lost work, can't tell state) and per persona: steps, clicks, friction count, completed?
- **Stress tests**: breakpoints 320→1440, 200% zoom, `stress-text.js` (`expand`, `devanagari` if users read Indic scripts or the UI is translated, `long-values`; then `restore`), data volume 0/1/many (local data only), missing data, slow network, errors, dark mode if supported.
- **Consistency**: compare with 2–3 sibling screens doing the same job.

## Phase 4 — Measure

Run what applies and keep the raw numbers for before → after:
- `axe-run.js` — accessibility violations with real values (e.g. contrast 2.8:1 vs 4.5:1), small tap targets, horizontal overflow.
- `hierarchy-scan.js` — section vs label size/weight ratio (flag < 1.25× without extra weight/colour/container), gap above sections vs between fields (needs ≥ 2×), label = section name, duplicate/similar/vague/abbreviated/truncated labels, generic placeholders, fake values ("NA"), choice groups with no visible selection.
- `dependency-scan.js` (forms, dev only) + code search for conditions on other fields (`disabled={!x}`, `watch()`, `v-if`, `required_if`, reset effects) → **Dependency map**.
- `focus-scan.js` — tab vs visual order, backward jumps, positive tabindex, no visible focus, clickable-but-unreachable.
- `token-scan.mjs` — `node <skill-dir>/scripts/token-scan.mjs <files/folders> [--json]` → hardcoded values mapped to design.md tokens. No Node → grep the same patterns.
- Forms: **Effort table** (fields, required, dropdowns, decisions, clicks to complete, typing, tabs) — see `forms-and-data-entry.md`.

## Phase 5 — Judge

Review screenshots + code + walkthrough log + measurements. Only real problems. Categories:

**H. Hierarchy & naming** (`hierarchy-and-naming.md`) — squint test (section titles that look like labels → 🔴), heading scan, label-only test, renames for same/similar/vague/abbreviated/master-table names, placeholders that say what to pick, no fake values, choices that look like choices.

**I. Dependencies & way-finding** (`dependencies-and-navigation.md`) — child right under its parent and visibly attached (other column 🟠, other section/tab 🔴); hide when meaningless, or disabled *with a reason*; parent change resets/re-filters child; required follows visibility; many Yes/No toggles → feature checklist that expands; 4+ sections → numbered specific titles (no "Other"/"Misc"), sticky section index with progress, tabs with missing-field counts, section icons from the project's icon set (icon + text).

**B. Zero-context clarity** — what is this screen; one obvious primary action, secondary quieter, destructive separated and confirmed; labels say what happens ("Add employee", not "Submit"); clickable looks clickable; no jargon; a way out; visible feedback for every action.

**C. By target type** — run what applies:
- **Forms & data entry** — all of `forms-and-data-entry.md`: derive/default/defer/delete; right control per field (2–4 options → radio/segmented, 10+ → searchable, units as suffix…); dropdown order, labels, dependent dropdowns, inline create; required-first sections; keyboard flow; on-blur validation; error summary that jumps; no lost work; review step for high-stakes saves.
- **Tables / lists** — search, filters, sorting, sticky header, pagination/virtualisation, visible row actions, bulk actions, right-aligned numbers, mobile layout, useful empty state.
- **Dashboards** — key number first, units and period on every metric, titled charts with legends, no decoration without data.
- **Modals** — clear title, one primary action, Esc + close, focus trapped and returned, not a page in disguise.
- **Navigation** — current location obvious, labels match page titles, works on mobile.
- **Single components** — every state (default, hover, focus, active, disabled, loading, error), all sizes it's used at, matches the system component it duplicates.
- **Staff / data-entry screens** — keyboard-only flow, shortcuts, no mouse-only steps, big targets for touch/shop floor, labels in the users' language where needed.
- **Public / consumer** — value obvious in seconds, one CTA, trust signals near it, fast on mobile.

**D. States** — loading, empty (with next step), error (with retry), disabled (with reason), success (what happened + what's next).

**E. Accessibility** — axe + focus-scan + what you see: contrast, focus, keyboard, names on icon buttons, colour never the only signal.

**F. Responsive & stress** — breakpoints, 200% zoom, long text, scripts, data volume.

**G. Consistency** — same job, same pattern, same names as sibling screens and the Glossary.

**A. Design-system adherence** — tokens, type scale, spacing, components, deprecated patterns.

For every issue: severity (🔴 blocks / loses data · 🟠 confuses / slows · 🟡 off-system / polish), **Impact = Severity × Frequency × Reach** (1–27, see `prove-and-remember.md`), a principle tag (e.g. [Proximity], [Match], [Hick], [Fitts], [Prevention], [A11y]), evidence, and file:line.

**Root cause:** if it comes from a shared component or theme, mark it; find every other screen using that component or repeating the pattern → "also affected".

### Score (0–100)

Each category starts at max; subtract per issue (🔴 −8, 🟠 −4, 🟡 −2), floor 0.

| Category | Max |
|---|---|
| Clarity, hierarchy, naming & way-finding (H + I + B) | 25 |
| Usability for this kind of UI (C) | 20 |
| States & feedback (D) | 15 |
| Accessibility & keyboard (E) | 15 |
| Design-system & consistency (A + G) | 15 |
| Responsive & stress (F) | 10 |

Always show the score with the per-category breakdown, before and after, in every run.

## Phase 6 — Report

Blunt, short, evidence-first. Talk like a senior designer who respects the user's time.

```
## <target> — 48/100
<Screen brief, 3–6 lines>

Walkthrough: Newcomer 14 steps · 5 friction · completed ✓ | Keyboard ✗ stuck at Door access type

🔴 [27] 1. Section titles look like labels — "Tray & Rack" 16px/500 vs labels 14px/500 (1.14×), 16px gap above vs 13px between fields. Newcomer couldn't tell where sections start. [Proximity] JobForm.tsx:212
🔴 [18] 2. Tab jumps from Capacity to Save, skipping Model No. (focus-scan: backward jump 320px). [A11y] JobForm.tsx:88
🟠 [18] 3. "Door access type" sits in the other column and greys out silently when Door Access is No. [Proximity][Visibility]
🟡 [4]  4. #1a73e8 ×6 — design.md says --signal.

Root cause: 1 comes from components/form/Section.tsx — also affected: LeaveForm, VendorForm.
Verdict: <one honest line>
```

Then the tables that apply: Hierarchy · Rename · Dependency map · Effort · Stress · Consistency · Walkthrough friction log (top items).

`quick` stops here. `handoff` outputs the hand-off prompt and stops.

## Phase 7 — Fix

**Required fixes — always:** every 🔴 and 🟠, using existing tokens/components even if the user said "keep my look". Only a real blocker (backend/API change, product decision, missing data) excuses one — name it per issue.

**Recommended upgrades — show, then ask:** regrouping, control swaps, sections → steps, derive/default, presets, copy-from-previous, feature checklists, section index. Build them as an **Upgraded** view in the demo with their score/effort gain. Apply only on a yes (unless the user asked for a redesign). Check memory's Rejected list first.

🟡 polish: fix if cheap, otherwise list.

How:
- Root causes first (shared component/theme), then page-specific, in Impact order.
- Shared component changes: keep the props API backward compatible or update every call site.
- Project's stack, conventions, component library, icon set, design.md tokens only. If design.md has no answer, propose a rule (Phase 8) instead of inventing silently.
- Keep business logic, payloads and data flow intact.
- With file access, edit directly (or as a diff if asked). Otherwise complete, paste-ready code for every file touched.
- Change list: each change → issue number.

## Phase 8 — Prove, lock in, remember

From `references/prove-and-remember.md`:
1. **Prove:** re-run every scan, re-walk the personas, re-screenshot (`after-*.png`), re-score. **Visual regression** on every screen using a shared component you changed (`npx -y pixelmatch before.png after.png diff.png 0.1`, or side-by-side by eye) — unexpected diffs get fixed before reporting. Same save payload, business validation intact, existing tests pass (run them if quick). Anything fails → fix and re-prove.
2. **Demo** — one self-contained HTML file in the run folder (published as an artifact or inline preview if the environment allows):
   - **Before / Fixed / Upgraded** views (stacked on mobile), each with score badge and per-category bars.
   - Real screenshots embedded (data URIs) with desktop/mobile toggle.
   - A **live, interactive Fixed view** built with the real design.md tokens as CSS variables: hover/focus, primary button loading → success, empty submit → inline errors + error summary, dependent fields revealing under their parent, section index highlighting and jumping, searchable selects filtering.
   - Numbered callouts matching issue numbers.
   - A **Proof panel**: scores, axe / focus / hierarchy / token numbers, walkthrough steps & friction, Effort table — before → after.
   - Realistic data (no lorem ipsum), no dependencies except CDNs/fonts, opens by double-click. Native/Flutter targets → phone-width HTML mock.
3. **Lock in:** add a focused test (primary path, dependent reveal, error summary, axe) if the project has a test setup; propose a lint rule against raw values if it has a linter. One line on what was added/proposed.
4. **design.md:** missing → generate (with approval). Gaps the fix needed → propose the exact rule in design.md's format; on approval append it + Changelog line `- YYYY-MM-DD: <rule> (from ui-fix on <target>)`.
5. **Memory:** update `.ui-fix/memory.md` — decisions approved/rejected, glossary, screen log row (score before → after, open items). Suggest `.ui-fix/runs/` in `.gitignore`.

## Phase 9 — Wrap up

Check the **Definition of done** in `prove-and-remember.md`, then end with:
- Score before → after (+ Effort and Newcomer steps/friction before → after).
- What changed, one line.
- Also-affected screens: fixed vs pending.
- Recommended upgrades not applied, each with expected gain — ask which to do.
- Blockers (needs backend / product decision).
- Guards added, design.md and memory updates.

---

## Don'ts

- Don't judge before the Screen brief, or before reading memory and design.md.
- Don't report opinions without evidence, or issues without Impact and file:line.
- Don't call a screen fine if section titles look like labels, names can be confused, dependent fields aren't visibly linked, or keyboard users get stuck.
- Don't treat "keep my look" as "change nothing visible".
- Don't leave a 🔴/🟠 unfixed without naming the blocker.
- Don't change a shared component without visual regression on the screens that use it.
- Don't inflate the after-score.
- Don't re-propose what memory says was rejected.
- Don't run against production, submit real data, or click destructive actions.
- Don't invent a new visual style, add new libraries, or touch unrelated logic.
- Don't explain UX theory. Show what's wrong, prove it, fix it, prove the fix.
