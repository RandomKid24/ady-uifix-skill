# Prioritise by impact, prove the fix, lock it in, remember

---

## 1. Impact — what to fix first

Severity alone isn't priority. A 🔴 on a screen used once a year matters less than a 🟠 hit 200 times a day. For every issue:

**Impact = Severity × Frequency × Reach**

| Factor | 3 | 2 | 1 |
|---|---|---|---|
| Severity | 🔴 blocks / loses data | 🟠 confuses / slows | 🟡 off-system / polish |
| Frequency (from Screen brief) | many times a day | weekly | rarely |
| Reach | on the primary task path, or in a shared component | on a secondary path | edge case |

Impact ranges 1–27. Sort the issue list by Impact (ties → severity). Show the number in brackets: `🔴 [27]`. Fix in Impact order. Shared-component root causes usually win because their Reach multiplies across screens.

Tag each issue with the principle it breaks, one word, so the reasoning is checkable: **[Visibility]** (system status), **[Match]** (real-world language), **[Control]** (undo/exit), **[Consistency]**, **[Prevention]** (error prevention), **[Recognition]** (recognise vs recall), **[Efficiency]**, **[Minimal]** (noise), **[Recovery]** (error messages), **[Help]**, **[Proximity]** / **[Similarity]** (grouping), **[Hick]** (too many choices), **[Fitts]** (target size/distance), **[A11y]**.

---

## 2. Prove it

A fix isn't done until it's proven. After applying changes:

1. **Re-run every check** you ran before (axe-run, hierarchy-scan, dependency-scan, focus-scan, token-scan, stress tests). Before → after numbers go in the report.
2. **Re-walk the personas** on the primary task. Before → after: steps, clicks, friction points, completed yes/no.
3. **Visual regression on everything you touched.** If you changed a shared component (Button, Input, Select, Card, Layout, theme), screenshot **every screen that uses it** — at least the "also affected" list, max ~10 — before and after, at desktop and 375px. Compare:
   ```bash
   npx -y pixelmatch before.png after.png diff.png 0.1
   ```
   (prints "different pixels" and "error %"; exits non-zero when anything differs — that's not a failure. Open diff.png to see where). Expected differences = the fix. Unexpected differences on screens you didn't mean to change → investigate and fix before reporting. If pixelmatch isn't available, compare the screenshots side by side by eye and say so.
4. **Behaviour still intact**: the same payload is sent on save (compare the network request before/after if you can), business validation still fires, existing tests still pass (`npm test` / `pytest` / the project's command — run it if it exists and is quick).
5. If anything fails, fix it and re-prove. Only then build the demo.

---

## 3. Lock it in (regression guard)

So the same problem doesn't come back next month. Do what fits the project — don't add new frameworks unless the user agrees:

- **If the project has Playwright/Cypress/Testing Library tests**: add one focused test for the fixed screen — the primary path works, dependent field reveals under its parent, error summary appears on empty save, and (if `@axe-core/playwright` or `jest-axe` is present or the user agrees to add it) zero serious/critical axe violations.
- **If the project has a linter**: propose (don't silently enable) a rule against raw design values — e.g. Stylelint `color-no-hex` / `declaration-property-value-disallowed-list`, ESLint `no-restricted-syntax` for inline `style` colours, or Tailwind arbitrary-value restrictions — scoped to the folders you fixed.
- **design.md**: any new pattern you introduced (section index, dependent-field nesting, feature checklist, section icons) is written as a rule (Step 9 of SKILL.md), so the next screen follows it.
- Mention in one line what guard you added or proposed.

---

## 4. Remember (project memory)

Keep a project-level memory so ui-fix gets smarter with every run and never re-argues settled decisions.

File: **`.ui-fix/memory.md`** in the project root (commit it). Read it **first** on every run. Create it on the first run.

```markdown
# ui-fix memory — <project name>

## Users & context
- <stable facts from Screen briefs: who uses the app, devices, language, domain terms>

## Decisions (follow these)
- 2026-10-31: Labels spell out codes, code in brackets — "Tray material (MOC)". (approved)
- 2026-10-31: Dependent fields hide when parent is No, nested under parent with left border. (approved)

## Rejected (don't propose again unless asked)
- 2026-10-31: Splitting Job form into a 5-step wizard — user prefers one page with section index.

## Glossary (one name per concept)
- Job (not Order / Work order) · MOC = Material of Construction · FAT = Factory Acceptance Test

## Screens
| Screen | File | Last run | Score before → after | Open items |
|---|---|---|---|---|
| New Job form | src/pages/jobs/JobForm.tsx | 2026-10-31 | 52 → 86 | section icons (proposed) |
```

Rules:
- Record **decisions the user approved or rejected**, glossary terms, and the screen log — not the full reports.
- Before proposing an upgrade, check Rejected. Before renaming, check Glossary.
- Keep it short: roll old screen-log rows into one line per screen.
- Run artifacts (screenshots, demos, scan outputs) go in **`.ui-fix/runs/<YYYY-MM-DD>-<target-slug>/`**. Suggest adding `.ui-fix/runs/` to `.gitignore` (keep `memory.md` committed).

---

## 5. Hand-off prompt (when the user implements with another agent)

If the user says they'll implement with another coding agent, or asks for a hand-off, output a single paste-ready prompt:

```
Implement these UI fixes in <repo>. Follow design.md strictly; use only existing tokens/components.

Context: <one-line Screen brief>
Files: <list>

Changes (in order):
1. [<issue #>] <file>: <exact change> — acceptance: <how to verify>
2. ...

Don't change: business logic, API payloads, unrelated files.
Done when: <checks — axe 0 serious, primary path N clicks, dependent fields nested, tests pass>
```

---

## 6. Definition of done — check before you report

- [ ] `.ui-fix/memory.md` read; decisions/rejections respected
- [ ] design.md read (or absence stated)
- [ ] Screen brief written
- [ ] Screenshots before (desktop + mobile)
- [ ] Persona walkthrough before (Newcomer + Keyboard at minimum)
- [ ] Visual critique written; layout-scan run at desktop + 375px
- [ ] All other scans run (or stated why not)
- [ ] Stress tests run (or stated why not)
- [ ] Issues ranked by Impact, each with evidence and principle tag
- [ ] Layout blueprint + Why table produced for every section with layout issues
- [ ] Every 🔴/🟠 fixed or blocker named — including layout (not just markers/renames)
- [ ] Re-scanned, re-walked, re-scored after
- [ ] Visual regression on all touched shared components
- [ ] Demo built (Before / Fixed / Upgraded); Fixed view shows the new layout
- [ ] Regression guard added or proposed
- [ ] memory.md and design.md updated (with approval)
