# ui-fix

**Point at an ugly or confusing screen. Get told what's wrong, a real fix, and a before/after demo.**

`ui-fix` is a skill for AI coding tools (Claude Code, OpenCode, Antigravity, Codex). It checks any page, form, table, modal or single component against your project's `design.md`, measures it, scores it, fixes it in your stack, and shows you the result before you commit.

The bar it holds every screen to: **someone who has never seen your app knows what this screen is, what to click, and what happens next — without thinking.**

---

## Install

```bash
npx github:RandomKid24/ady-uifix-skill
```

That's it. The installer finds the AI tools on your machine and asks which ones to install into.

```
Install ui-fix for:  (global)

  1. Claude Code  detected   ~/.claude/skills/ui-fix
  2. OpenCode     detected   ~/.config/opencode/skills/ui-fix
  3. Antigravity  not found  ~/.gemini/antigravity/skills/ui-fix
  4. Codex CLI    not found  ~/.codex/skills/ui-fix

Pick numbers (comma separated) or "a" for all [1,2]:
```

Press Enter to install into everything detected. Restart your AI tool afterwards.

### Other ways

```bash
# No questions, install into all detected tools
npx github:RandomKid24/ady-uifix-skill -y

# Pick tools directly
npx github:RandomKid24/ady-uifix-skill --claude --opencode

# Only for the project you're in (commits with the repo, whole team gets it)
npx github:RandomKid24/ady-uifix-skill --project

# Any other tool — point at its skills folder
npx github:RandomKid24/ady-uifix-skill --dir ~/.some-tool/skills

# See where it goes and what's detected
npx github:RandomKid24/ady-uifix-skill --list

# Update: just run the install again (it overwrites the old copy)
# Remove:
npx github:RandomKid24/ady-uifix-skill --uninstall
```

Needs **Node 18+**. No dependencies.

### Where it installs

| Tool | Global | `--project` |
|---|---|---|
| Claude Code | `~/.claude/skills/ui-fix` | `.claude/skills/ui-fix` |
| OpenCode | `~/.config/opencode/skills/ui-fix` | `.opencode/skills/ui-fix` |
| Antigravity | `~/.gemini/antigravity/skills/ui-fix` | `.agent/skills/ui-fix` |
| Codex CLI | `~/.codex/skills/ui-fix` | `.codex/skills/ui-fix` |

If your tool reads skills from somewhere else, use `--dir <path>`.

### Manual install

Copy the `skills/ui-fix` folder into your tool's skills folder (table above). Done.

---

## Use

```
/ui-fix src/pages/Employees.tsx
/ui-fix the add-invoice form
/ui-fix components/ui/Button.tsx
/ui-fix http://localhost:5173/leaves
```

Or just say it in plain words — "this vendor form is confusing, fix it", "the dashboard looks off" — and the skill kicks in.

### Modes

| Mode | Example | What you get |
|---|---|---|
| `fix` *(default)* | `/ui-fix src/pages/Employees.tsx` | Audit → score → fix → verify → demo |
| `quick` | `/ui-fix quick the login page` | Audit + score + report only. No code touched |
| `sweep` | `/ui-fix sweep src/pages/hr` | Audits every screen in the folder, ranks them by score, fixes shared root causes first |

---

## What it does

1. **Reads your `design.md` first.** Colors, fonts, spacing, components, rules — every fix follows it. No `design.md`? It tells you, works from your Tailwind config / CSS variables / theme for now, and offers to generate one.
2. **Looks at the real thing.** Runs your dev server, screenshots the target at desktop and 375px mobile, and triggers states like empty submit and focus. *(Local / dev / staging only — never production.)*
3. **Measures it.**
   - **axe-core** accessibility check with real numbers ("contrast 2.8:1, needs 4.5:1")
   - **Token scan** for hardcoded colors, px values, Tailwind arbitrary values and inline styles that should be design tokens
   - Tap targets under 44px, horizontal overflow on mobile
4. **Checks it like a first-time user would.** One obvious main button? Labels that say what happens? A way out? Feedback after every click? Plus checks for the kind of UI it is — forms, tables, dashboards, modals, navigation, single components, data-entry screens, public pages.
5. **Scores it 0–100** across 6 categories, before and after.
6. **Tells you bluntly what's wrong**, with file:line and evidence, tagged 🔴 broken · 🟠 confusing · 🟡 off-system.
7. **Fixes the root, not just the page.** If the problem lives in a shared `Button` or `Input`, it fixes that component and lists every other screen it also fixes.
8. **Shows you the result.** A self-contained HTML demo: before vs after side by side, real screenshots, a live clickable "after" built with your real tokens, numbered callouts, scores, and the axe/token numbers before → after.
9. **Grows your `design.md`.** When a fix needs a rule your design system doesn't have yet, it proposes the exact line and adds it (with a changelog entry) once you OK it. It never rewrites your existing rules on its own.

### Example report

```
## EmployeeForm — score 48/100

🔴 1. Primary action is invisible — "Save" is a grey ghost button next to a
      bright red "Delete". Users will hit the wrong one. (EmployeeForm.tsx:142)
🔴 2. Placeholders used as labels — type one character and the field name is gone. axe: label ×6.
🟠 3. "Submit" tells nobody anything. It creates an employee — say "Add employee".
🟡 4. #1a73e8 hardcoded ×6 — design.md says --signal.

Root cause: 1 and 2 come from components/ui/Input.tsx and Button.tsx
— also affected: LeaveForm, ExpenseForm, VendorForm.

Verdict: Usable if you built it. Anyone else is guessing.
```

### Score

| Category | Points |
|---|---|
| Clarity & primary action | 25 |
| Usability for this kind of UI | 20 |
| States & feedback | 15 |
| Accessibility | 15 |
| Design-system adherence | 15 |
| Responsive | 10 |

Each issue costs 🔴 8 · 🟠 4 · 🟡 2 points in its category.

---

## Get the most out of it

- **Add a `design.md`** to your project root. That's what keeps fixes consistent with your system. Don't have one? Run `/ui-fix` once and let it generate a starter from your code, then clean up the lines marked `(inferred)`.
- **Have your dev server runnable** so it can take real screenshots and verify the fix. Without a browser it still works from code, just without the real before/after.
- **Give it a browser.** Claude in Chrome, a built-in browser pane, or Playwright all work.

## What's inside

```
skills/ui-fix/
├── SKILL.md                         # the skill
├── references/
│   └── design-md-template.md         # template for generating a missing design.md
└── scripts/
    ├── token-scan.mjs               # finds hardcoded colors/sizes/inline styles
    └── axe-run.js                   # runs axe-core + tap-target/overflow checks in the browser
```

You can run the token scan on its own too:

```bash
node ~/.claude/skills/ui-fix/scripts/token-scan.mjs src/pages
```

---

MIT · Made by [Aditya Badgujar](https://adityabadgujar.dev) at [BeForth](https://beforth.in)
