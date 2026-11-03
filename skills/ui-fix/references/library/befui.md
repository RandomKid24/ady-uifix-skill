# befui — the default component source for React + Tailwind

befui (https://github.com/RandomKid24/befui · docs https://befui.vercel.app) is a copy-paste component library: **273 React components, 38 full-page blocks, 389 icons, 10 palettes**, on Radix + Tailwind 4 + CSS variables. Every component is one file that ends up in the project and belongs to it. The same components also exist as **121 Flutter widgets** and as **`<bef-*>` HTML tags** (plain HTML, htmx, Django, Rails, PHP).

Why ui-fix leans on it: hand-built UI is where slop and inconsistency come from — one-off paddings, five button styles, a dropdown that works differently on every page. A befui component already has the real states (invalid, disabled, loading, empty, error), keyboard and focus handled by Radix, one radius scale, one motion curve, tabular numbers and RTL support. Using it removes whole classes of problems instead of patching them.

---

## 1. When to use it

Check in this order (stop at the first that fits):
1. **The project's own component** for the job — always first. Never duplicate it.
2. **befui — if the project is React + Tailwind (any version of Vite/Next/Remix), or the user says to use it.**
   Project already has befui? You'll see `src/components/ui/*`, `src/lib/utils.ts` with `cn`, an `AGENTS.md` block starting "## UI components (befui)", a `befui` entry in `.mcp.json`, and CSS variables like `--primary`, `--elev-1`, `--control-h` in `index.css`. Then befui is the project's kit — use it without asking.
   Project doesn't have it? **Recommend it, once, in the report** ("this screen would be built from befui `select`, `combobox`, `form-wizard` …") and **ask before running `init`/`add`** — it touches `index.css`, adds `AGENTS.md`/`.mcp.json` and installs packages.
3. The UI kit the project already uses (shadcn/ui, MUI, Chakra, Ant…) — keep it; take *ideas* from befui, not files.
4. Not React? **HTML/htmx/server templates →** `<bef-*>` tags (`public/llms-html.txt`). **Flutter →** `add <name> --flutter`. Anything else → build with the project's own stack and tokens.

If befui can't be reached (network allowlist, GitHub blocked), say so and build with the project's stack — never hand-copy a component from memory. The raw JSON for any component is `https://raw.githubusercontent.com/RandomKid24/befui/main/public/r/<name>.json` (blocks: `block-<name>.json`).

## 2. How to use it (the exact commands)

```bash
npx github:RandomKid24/befui init [--theme <name>] [--force]   # one time: theme CSS, cn helper, AGENTS.md rules, .mcp.json
npx github:RandomKid24/befui list                              # everything available (add --flutter for widgets)
npx github:RandomKid24/befui add button select combobox        # components; blocks are block:<name>; "all" for everything
npx github:RandomKid24/befui diff <name>                       # how the project's copy differs from the library's
npx github:RandomKid24/befui update [--check]                  # add missing animation keyframes to index.css
npx github:RandomKid24/befui mcp                               # MCP server: list_components, get_component, get_html_rules, add_components
```

- There is **no `befui` package on npm** — `npx befui` fails. Always the `github:` form.
- Needs Tailwind 4 and an `@` → `src` import alias (the setup guide in the befui README has the three config lines). Check both before running `add`.
- `add` also installs the npm packages and any befui files a component imports (usually `icons`). Existing local edits are kept unless `--force`.
- Icons come from `@/components/ui/icons` (389, own set, 24px grid). **Never mix in lucide or another icon package** next to befui icons.
- With the MCP server connected, call `get_component <name>` for the exact source, import path and example instead of guessing props.

## 3. Pick by job, not by name

Don't scan the whole catalogue. Map the screen's job (from the Screen brief) to this table, then confirm with `list` or `get_component`.

| The screen needs… | befui |
|---|---|
| App frame, navigation | `app-shell`, `sidebar`, `navbar`, `navigation-menu`, `breadcrumb`, `tabs`, `bottom-nav` (mobile), `org-switcher`, `user-menu`, `command` (⌘K) · block `admin-shell`, `top-nav-layout` |
| Settings | `settings-layout` (section list left, rows right) · block `settings-page`, `notifications-page` |
| Forms | `input`, `label` (+ `Field` for label/control/hint/error), `select`, `combobox`, `cascader` (country → state → city), `date-picker`, `currency-input`, `phone-input`, `tag-input`, `radio-group` (option cards), `switch`, `checkbox`, `segmented`, `number-stepper`, `form-wizard`, `schema-form`, `stepper` · blocks `new-hire-form` (ten dropdowns), `leave-request-form`, `checkout-page` |
| Dependent / many dropdowns | `cascader`, `combobox` with descriptions, `filter-builder`, `transfer-list` — and keep the dependent-field rules in `dependencies-and-navigation.md` |
| Tables & lists | `data-table` (sort, filter, paginate), `table` (dense parts), `tree-table`, `pivot-table`, `virtual-list`, `sortable-list`, `kanban`, `bar-list`, `saved-views`, `filter-bar` · blocks `reports-table`, `employee-directory`, `user-management` |
| Numbers & charts | `stat-card`, `kpi-strip`, `usage-meter`, `progress`, `progress-ring`, `gauge`, `bullet-chart`, `line-chart`, `area-chart`, `stacked-bar-chart`, `funnel-chart`, `heatmap`, `sparkline-table` … (84 in Data) · blocks `sales-dashboard`, `finance-dashboard`, `analytics-dashboard`, `hrms-overview` |
| Status & people | `badge`, `status-dot`, `avatar` (+ stacks, presence), `activity-feed`, `timeline`, `approval-flow`, `audit-log`, `profile-card` · blocks `leave-approvals`, `profile-page` |
| Show/hide & confirm | `accordion`, `collapsible` (chevron + animated height — use these for any expand/collapse), `popconfirm`, `alert-dialog` (confirm destructive actions) |
| Feedback | `alert`, `banner`, `toast`, `empty-state`, `error-state`, `skeleton`, `spinner`, `loader`, `popconfirm`, `alert-dialog` |
| Overlays | `dialog`, `drawer`, `bottom-sheet`, `popover`, `dropdown-menu`, `tooltip`, `hover-card`, `tour`, `coachmark` |
| Auth | blocks `sign-in`, `sign-up`, `reset-password`, `otp-verify` |
| Marketing | `landing-sections` (Hero, FeatureGrid, StatsStrip, Faq, CtaBanner, SiteFooter), `pricing-card`, `pricing-comparison`, `testimonial-card` · blocks `landing-page`, `pricing-page`, `contact-page`, `team-page` |
| AI products | `ai-chat`, `ai-message`, `prompt-input`, `thinking`, `tool-call`, `sources`, `model-picker`, `token-meter`, `artifact-panel` |
| Time | `time-picker`, `datetime-picker`, `week-strip`, `event-calendar`, `day-agenda`, `cron-builder`, `timezone-picker`, `relative-time` |

**Blocks are starting points, not finished screens.** Add one, then replace the mock data with the real API and cut what the screen doesn't need (the Screen brief decides). A block pasted whole into an unrelated product is exactly the template look this skill is trying to remove.

## 4. Make it look like *this* product (the part that stops it being slop)

befui's default is a calm, quiet system: neutral slate surfaces, hairline borders, one blue accent, Onest type, 8px radius, small shadows. That's a good **base**, not a finished identity. If every product ships the default, every product looks alike. After adding components, apply the product identity (`visual-design.md` §0) **through the tokens** — never by overriding component internals:

| Lever | Where | What to set |
|---|---|---|
| Accent | `--primary`, `--primary-foreground`, `--accent`, `--accent-foreground`, `--ring` | `init --theme <name>` gives ten palettes: blue, indigo, violet, rose, red, emerald, teal, amber, orange, slate. Better: the **brand colour** (derive the set with `type-and-colour.md`; check text on `--primary` ≥ 4.5:1) |
| Surfaces | `--background`, `--card`, `--secondary`, `--muted`, `--border` | Tint the neutrals toward the product's world (warm paper, cool graphite, green-grey) — keep them *neutral*; the world shows in the accent and the one rich moment |
| Shape | `--radius` (default 8px; small 6, large 10, cards 14) | Sharper for precise/industrial (2–4), rounder for friendly (12–14). One value for the whole product |
| Density | `data-density="compact"` or `"comfortable"` on any ancestor; `--control-h` (36px) | Compact for all-day data entry, comfortable for public/occasional users |
| Type | font stack in `index.css` (Onest + JetBrains Mono by default) | Keep the project's/brand font if there is one; otherwise pick from `type-and-colour.md` for the personality. One family for UI + at most one partner |
| Motion | `--dur-fast/base/spring/slow`, `--ease-out`, `--ease-spring` | Leave as is unless the personality needs calmer/snappier; never hard-code `duration-150` etc. |
| Elevation | `--elev-1..3` | Dark mode leans on borders; keep shadows neutral |

Rules when working with befui files:
- **Tokens only** (`bg-primary`, `text-muted-foreground`, `border`). No hard-coded hex, no gradients, no `shadow-[...]` one-offs.
- Merge classes with `cn` from `@/lib/utils`. Add a **variant** before adding a boolean prop (befui's own rule: `variant`, `size`, `shape`).
- Edit the copied files freely — they're the project's. `diff <name>` before re-adding with `--force` (which overwrites local edits).
- Components with fixed colours on purpose: `terminal` (always dark), `avatar` and `tag-manager` (name-stable tints — edit the `tones` list to match the brand). Don't "fix" those.
- Logical spacing (`ms-*`, `ps-*`, `start-*`) so right-to-left works — keep it.
- Animated components need keyframes in `index.css`; if one looks static, run `update`.
- Respect befui's own `DESIGN.md` (in its repo) when adding a new variant: tokens only, check light, dark, a custom palette and RTL, include empty/loading/error states.

## 5. What ui-fix does with befui in each phase

- **Phase 0:** detect whether the project already uses befui (see §1). Note it in the Screen brief's stack line and in memory.
- **Phase 4–5 (judge):** a hand-built control that befui already provides (custom dropdown, ad-hoc modal, DIY toast, one-off table) is a finding under **A. Design-system adherence** — "replace with `select`/`dialog`…" — especially when it caused a measurable issue (no keyboard, no focus ring, off-grid padding, no empty state).
- **Phase 7 (fix):** Fix → swap the broken control for the befui component, keep the payload and handlers. Polish → plus set the tokens above for this product. Redesign → pick components per direction (not one shared look), restyle through tokens, build each direction as a variant you can toggle.
- **Phase 8:** note which befui components were added or replaced (and that they're copied files, not a dependency) in the report's Files changed and in `.ui-fix/memory.md`; propose a befui line in design.md ("Components: befui; tokens in index.css; icons: befui icons only").
- **Not React / not reachable:** say what you'd have used and why you didn't; fall back to the project's own stack.

## 6. Honest limits

- befui covers the common parts well; domain-specific widgets (a factory floor machine board, a salon booking grid, a floor plan) are still built — from befui primitives and the project's tokens.
- Don't invent component names, props or CLI flags. If unsure, run `list` / `get_component` or read `https://raw.githubusercontent.com/RandomKid24/befui/main/public/llms-full.txt`.
- Adding befui is a **dependency-of-convenience decision for the user**: the files are copied (nothing to upgrade), but `index.css`, `AGENTS.md`, `.mcp.json` and npm packages change. Ask first.
