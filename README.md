# ui-fix

**The UI fixer that thinks like a senior UI engineer — and proves it.**

Point it at a page, form, table, modal or single component. `ui-fix` works out what the screen is for, walks it as real users, measures everything, fixes it against your `design.md`, proves the fix with before/after numbers and visual regression, and remembers your decisions for next time.

Works with **Claude Code, OpenCode, Antigravity, Codex** — and any tool that reads skills.

The bar: **someone who has never seen your app knows what this screen is, what to click, and what happens next — without thinking. Daily users finish in the fewest steps. Nobody loses work.**

---

## Install

```bash
npx github:RandomKid24/ady-uifix-skill
```

Detects your AI tools and asks where to install. Press Enter for all detected. Restart your tool afterwards.

```bash
npx github:RandomKid24/ady-uifix-skill -y                    # no questions, all detected tools
npx github:RandomKid24/ady-uifix-skill --claude --opencode   # pick tools
npx github:RandomKid24/ady-uifix-skill --project             # this repo only (team gets it via git)
npx github:RandomKid24/ady-uifix-skill --dir <skills-folder> # any other tool
npx github:RandomKid24/ady-uifix-skill --list                # where it goes / what's detected
npx github:RandomKid24/ady-uifix-skill --uninstall           # remove
```

**Update:** run the install again. If npx serves an old copy: `rm -rf ~/.npm/_npx` first.

Needs Node 18+. No dependencies.

| Tool | Global | `--project` |
|---|---|---|
| Claude Code | `~/.claude/skills/ui-fix` | `.claude/skills/ui-fix` |
| OpenCode | `~/.config/opencode/skills/ui-fix` | `.opencode/skills/ui-fix` |
| Antigravity | `~/.gemini/antigravity/skills/ui-fix` | `.agent/skills/ui-fix` |
| Codex CLI | `~/.codex/skills/ui-fix` | `.codex/skills/ui-fix` |

Manual: copy `skills/ui-fix` into your tool's skills folder.

---

## Use

**Claude Code**
```
/ui-fix src/pages/jobs/JobForm.tsx
/ui-fix quick the vendor list
/ui-fix sweep src/pages/hr
/ui-fix handoff the add-invoice form
```

**OpenCode / Antigravity / Codex** — name it in plain words:
```
use ui-fix on src/pages/jobs/JobForm.tsx
use ui-fix sweep on src/pages/hr
```

Or just describe the problem: *"this form is confusing, fix it"*, *"the dashboard looks off"*.

Point it at a file, a folder, a local URL (`http://localhost:5173/jobs/new`), a screen by name, or a pasted screenshot.

| Mode | What you get |
|---|---|
| `fix` *(default)* | Everything: understand → see → walk → measure → judge → fix → prove → remember |
| `quick` | Full audit + score + report. No code touched |
| `sweep` | Audits every screen in a folder, ranks them, fixes shared root causes first |
| `handoff` | Audit + a paste-ready implementation prompt for another coding agent |

---

## How it works

| Phase | What happens |
|---|---|
| **0. Remember** | Reads `.ui-fix/memory.md` (past decisions, rejected ideas, glossary) and your `design.md`. No design.md? Says so and offers to generate one |
| **1. Understand** | Works out what the screen is for, who uses it and how often, what it loads and saves (reads the API and backend), the business rules, the flow, every element's purpose, and the shortest task path. Catches UI ↔ backend mismatches. Shows a short *Screen brief* |
| **2. See** | Runs your dev server, screenshots desktop + mobile and key states |
| **3. Walk** | Tries the task as real users — **Newcomer** and **Keyboard-only** always, plus Power user / Touch / 200% zoom / Regional language / Interrupted when they apply. 5-second test, first-click test, friction log. Then **stress tests**: breakpoints, zoom, pseudo-localization, Marathi/Devanagari, long values, 0/1/1000 rows, slow network, errors, dark mode. Compares with sibling screens for consistency |
| **4. Measure** | A designer's visual critique (grid, alignment, balance, rhythm, reading path), then seven scanners: **layout & spacing**, accessibility (axe), hierarchy & naming, dependent fields, keyboard & focus, text stress, design-token drift. Effort table for forms |
| **5. Judge** | Every issue gets severity, an **Impact score** (severity × frequency × reach), a principle tag, evidence, and file:line. Finds the shared root cause and every screen it affects. Scores 0–100 |
| **6. Report** | Blunt and short. A **layout blueprint** that says where every component goes, how wide, with what spacing — and why. Hierarchy, rename, dependency, effort, stress and consistency tables |
| **7. Fix** | Every 🔴 and 🟠 fixed (with your existing design system) or the blocker named. Bigger upgrades shown as an "Upgraded" view for you to approve |
| **8. Prove** | Re-scans, re-walks, re-scores. **Visual regression** on every screen using a changed shared component. Checks the save payload and tests still pass. Builds a before / fixed / upgraded demo with a proof panel. Adds a regression test or lint rule. Updates design.md and memory |

### What it catches

- **Layout & spacing** — forms stretched 1800px wide, Yes/No buttons floating in empty columns, a full-width dropdown next to a tiny button pair, number fields as wide as a paragraph, zig-zag 2-column grids of unrelated fields, near-miss alignment, random gaps (13px here, 22px there), ragged rows, children placed in the wrong column
- **Hierarchy & naming** — section titles that look like field labels, "Packaging" under "Packaging", Tray Type vs Tray MOC, codes like MOC/FAT/Qty., vague labels, truncated text, "Select" placeholders, "NA" typed into fields, Yes/No with no visible selection
- **Dependent fields** — clicks every choice to map which fields depend on which; flags children far from their parent or greyed out with no reason; checks reset-on-change and hidden values not being saved
- **Way-finding** — long forms without numbered sections, section index, progress, or icons; catch-all sections like "Other"
- **Forms & data entry** — fields that could be derived, defaulted or deferred; wrong controls (2-option dropdowns, 50-option plain selects); dropdown order and labels; validation and error summary; lost work
- **Keyboard** — tab order vs visual order, invisible focus, clickable divs keyboard users can't reach
- **Stress** — what breaks with long text, Indic scripts, 200% zoom, lots of data, slow network, errors
- **Accessibility** — real axe numbers ("contrast 2.8:1, needs 4.5:1"), tap targets, overflow
- **Design-system drift** — hardcoded colours, px, Tailwind arbitrary values, inline styles
- **Consistency** — same job, same pattern, same names across screens
- Plus tables, dashboards, modals, navigation, single components, states (loading / empty / error / disabled / success)

### Example report

```
## New Job form — 48/100
Purpose: Sales coordinators create a manufacturing job for a confirmed order. Daily, desktop.

Walkthrough: Newcomer 14 steps · 5 friction · completed ✓ | Keyboard ✗ stuck at Door access type

🔴 [27] 1. Section titles look like labels — 16px/500 vs labels 14px/500 (1.14×). Newcomer
          couldn't tell where sections start. [Proximity] JobForm.tsx:212
🔴 [18] 2. Tab jumps from Capacity to Save, skipping Model No. [A11y] JobForm.tsx:88
🟠 [18] 3. "Door access type" sits in the other column and greys out silently. [Proximity][Visibility]
🟡 [4]  4. #1a73e8 ×6 — design.md says --signal.

Root cause: 1 comes from components/form/Section.tsx — also affected: LeaveForm, VendorForm.
```

### Score

| Category | Points |
|---|---|
| Clarity, hierarchy, naming & way-finding | 20 |
| Layout, spacing & placement | 20 |
| Usability for this kind of UI | 15 |
| States & feedback | 10 |
| Accessibility & keyboard | 15 |
| Design-system & consistency | 10 |
| Responsive & stress | 10 |

🔴 −8 · 🟠 −4 · 🟡 −2 per issue in its category. Always shown before and after.

---

## Project files it creates

```
your-project/
├── design.md                  # your design system (generated if missing, with your OK)
└── .ui-fix/
    ├── memory.md              # decisions, rejected ideas, glossary, score history — commit this
    └── runs/<date>-<screen>/  # screenshots, scan results, demo.html — add to .gitignore
```

## Get the most out of it

- **Have a `design.md`.** No design.md? Let the first run generate one, then fix the `(inferred)` lines.
- **Keep your dev server runnable** with seed/test data. Real screenshots, walkthroughs and visual regression need it. Without a browser it still works from code — just with less proof.
- **Give it a browser** — Claude in Chrome, a built-in browser pane, or Playwright.
- **Say yes or no to upgrades.** It remembers both, so it never argues the same point twice.
- **Local / dev / staging only.** It clicks choices and fills fields while testing. Never point it at production.

---

## What's inside

```
skills/ui-fix/
├── SKILL.md                              # the pipeline
├── references/
│   ├── layout-and-spacing.md             # grid, alignment, balance, widths, spacing, placement, blueprint
│   ├── understand-the-screen.md          # purpose, data flow, element inventory, Screen brief
│   ├── walkthrough-and-stress.md         # personas, friction log, stress tests, consistency
│   ├── hierarchy-and-naming.md           # headings vs labels, confusing names, placeholders
│   ├── dependencies-and-navigation.md    # parent→child fields, section index, numbering, icons
│   ├── forms-and-data-entry.md           # effort, controls, dropdowns, validation
│   ├── prove-and-remember.md             # impact ranking, proof, regression guard, memory, hand-off
│   └── design-md-template.md             # starter design.md
└── scripts/
    ├── layout-scan.js                    # grid, balance, dead zones, widths, spacing rhythm, layout map (browser)
    ├── axe-run.js                        # accessibility + tap targets + overflow (browser)
    ├── hierarchy-scan.js                 # heading/label styles, spacing, naming problems (browser)
    ├── dependency-scan.js                # maps dependent fields by flipping choices (browser, dev only)
    ├── focus-scan.js                     # tab order, focus visibility, unreachable clickables (browser)
    ├── stress-text.js                    # pseudo-localization, Devanagari, long values (browser, reversible)
    └── token-scan.mjs                    # hardcoded colours/sizes/inline styles (Node)
```

Run the token scan on its own:
```bash
node ~/.claude/skills/ui-fix/scripts/token-scan.mjs src/pages
```

---

MIT · Made by [Aditya Badgujar](https://adityabadgujar.dev) at [BeForth](https://beforth.in)
