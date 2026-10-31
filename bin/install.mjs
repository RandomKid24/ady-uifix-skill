#!/usr/bin/env node
// ui-fix skill installer — detects your AI coding tools and copies the skill into each.
// Zero dependencies. Node 18+.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';

const SKILL = 'ui-fix';
const here = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.resolve(here, '..', 'skills', SKILL);
const HOME = os.homedir();
const CWD = process.cwd();
const isWin = process.platform === 'win32';

const c = process.stdout.isTTY && !process.env.NO_COLOR
  ? { b: s => `\x1b[1m${s}\x1b[0m`, g: s => `\x1b[32m${s}\x1b[0m`, y: s => `\x1b[33m${s}\x1b[0m`, r: s => `\x1b[31m${s}\x1b[0m`, d: s => `\x1b[2m${s}\x1b[0m` }
  : { b: s => s, g: s => s, y: s => s, r: s => s, d: s => s };

// Where each tool looks for skills. global = for every project, project = this repo only.
const TOOLS = [
  {
    id: 'claude', name: 'Claude Code',
    global: path.join(HOME, '.claude', 'skills'),
    project: path.join(CWD, '.claude', 'skills'),
    detect: [path.join(HOME, '.claude')], bins: ['claude'],
  },
  {
    id: 'opencode', name: 'OpenCode',
    global: path.join(HOME, '.config', 'opencode', 'skills'),
    project: path.join(CWD, '.opencode', 'skills'),
    detect: [path.join(HOME, '.config', 'opencode'), path.join(HOME, '.opencode')], bins: ['opencode'],
  },
  {
    id: 'antigravity', name: 'Antigravity',
    global: path.join(HOME, '.gemini', 'antigravity', 'skills'),
    project: path.join(CWD, '.agent', 'skills'),
    detect: [path.join(HOME, '.gemini', 'antigravity')], bins: ['antigravity'],
  },
  {
    id: 'codex', name: 'Codex CLI',
    global: path.join(HOME, '.codex', 'skills'),
    project: path.join(CWD, '.codex', 'skills'),
    detect: [path.join(HOME, '.codex')], bins: ['codex'],
  },
];

// ---------- args ----------
const argv = process.argv.slice(2);
const has = (...f) => f.some(x => argv.includes(x));
const valueOf = flag => { const i = argv.indexOf(flag); return i >= 0 ? argv[i + 1] : undefined; };

if (has('-h', '--help')) {
  console.log(`
${c.b('ui-fix skill installer')}

  npx github:RandomKid24/ady-uifix-skill [options]

Options:
  (none)            Detect installed AI tools and ask where to install
  --claude          Install for Claude Code
  --opencode        Install for OpenCode
  --antigravity     Install for Antigravity
  --codex           Install for Codex CLI
  --all             Install for every supported tool, detected or not
  --project         Install into the current project instead of globally
  --dir <path>      Install into a custom skills folder (any other tool)
  -y, --yes         Don't ask, install to all detected tools
  --uninstall       Remove ui-fix from the selected tools
  --list            Show supported tools, paths and what's detected
  -h, --help        Show this help
`);
  process.exit(0);
}

const scope = has('--project') ? 'project' : 'global';
const uninstall = has('--uninstall');

// ---------- detection ----------
function onPath(bin) {
  const dirs = (process.env.PATH || '').split(path.delimiter);
  const exts = isWin ? (process.env.PATHEXT || '.EXE;.CMD;.BAT').split(';').concat(['']) : [''];
  return dirs.some(d => exts.some(e => { try { return fs.statSync(path.join(d, bin + e)).isFile(); } catch { return false; } }));
}
const detected = t => t.detect.some(p => fs.existsSync(p)) || t.bins.some(onPath);

if (has('--list')) {
  console.log(`\n${c.b('Supported tools')}  ${c.d(`(scope: ${scope})`)}\n`);
  for (const t of TOOLS) {
    console.log(`  ${detected(t) ? c.g('✔') : c.d('·')} ${t.name.padEnd(12)} ${c.d(path.join(t[scope], SKILL))}`);
  }
  console.log('');
  process.exit(0);
}

if (!fs.existsSync(path.join(SRC, 'SKILL.md'))) {
  console.error(c.r(`Skill files not found at ${SRC}`));
  process.exit(1);
}

// ---------- pick targets ----------
async function ask(q) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(res => rl.question(q, a => { rl.close(); res(a.trim()); }));
}

async function pickTargets() {
  const custom = valueOf('--dir');
  if (custom) return [{ name: 'Custom folder', dir: path.resolve(custom) }];

  const explicit = TOOLS.filter(t => has(`--${t.id}`));
  if (has('--all')) return TOOLS.map(t => ({ name: t.name, dir: t[scope] }));
  if (explicit.length) return explicit.map(t => ({ name: t.name, dir: t[scope] }));

  const found = TOOLS.filter(detected);
  const interactive = process.stdin.isTTY && !has('-y', '--yes');

  if (!interactive) {
    const use = found.length ? found : [TOOLS[0]];
    if (!found.length) console.log(c.y('No AI tools detected — defaulting to Claude Code.'));
    return use.map(t => ({ name: t.name, dir: t[scope] }));
  }

  console.log(`\n${c.b(uninstall ? 'Remove ui-fix from:' : 'Install ui-fix for:')}  ${c.d(`(${scope})`)}\n`);
  TOOLS.forEach((t, i) => {
    console.log(`  ${c.b(String(i + 1))}. ${t.name.padEnd(12)} ${detected(t) ? c.g('detected') : c.d('not found')}  ${c.d(path.join(t[scope], SKILL))}`);
  });
  const def = found.length ? found.map(t => TOOLS.indexOf(t) + 1).join(',') : '1';
  const a = await ask(`\nPick numbers (comma separated) or "a" for all ${c.d(`[${def}]`)}: `);
  const raw = (a || def).toLowerCase();
  const idx = raw === 'a' || raw === 'all'
    ? TOOLS.map((_, i) => i)
    : raw.split(/[\s,]+/).map(n => parseInt(n, 10) - 1).filter(i => i >= 0 && i < TOOLS.length);
  if (!idx.length) { console.log(c.y('Nothing selected.')); process.exit(0); }
  return [...new Set(idx)].map(i => ({ name: TOOLS[i].name, dir: TOOLS[i][scope] }));
}

// ---------- do it ----------
const targets = await pickTargets();
console.log('');
let ok = 0;
for (const t of targets) {
  const dest = path.join(t.dir, SKILL);
  try {
    if (uninstall) {
      if (fs.existsSync(dest)) { fs.rmSync(dest, { recursive: true, force: true }); console.log(`  ${c.g('✔')} removed from ${t.name}  ${c.d(dest)}`); }
      else console.log(`  ${c.d('·')} not installed in ${t.name}`);
    } else {
      const existed = fs.existsSync(dest);
      fs.mkdirSync(t.dir, { recursive: true });
      if (existed) fs.rmSync(dest, { recursive: true, force: true });
      fs.cpSync(SRC, dest, { recursive: true });
      console.log(`  ${c.g('✔')} ${existed ? 'updated' : 'installed'} for ${t.name}  ${c.d(dest)}`);
    }
    ok++;
  } catch (e) {
    console.log(`  ${c.r('✖')} ${t.name}: ${e.message}`);
  }
}

if (!uninstall && ok) {
  console.log(`
${c.b('Done.')} Restart your AI tool, then try:

  /ui-fix src/pages/Employees.tsx
  /ui-fix quick the login form
  /ui-fix sweep src/pages/hr

Tip: put a ${c.b('design.md')} in your project root so every fix follows your design system.
`);
}
process.exit(ok ? 0 : 1);
