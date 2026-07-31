# Night Ace AI Orchestra for Claude Code

Stop prompting. Start orchestrating.

A single agent in a single context has a structural flaw: it grades its own work. This package
turns Claude Code into a small orchestra — parallel scouts map your codebase, one builder per
concern does the work, and independent skeptics try to refute every claim before anything
reaches you.

Built and used daily by **Night Ace**, a web design, development, and AI automation studio.

## What's inside

```
.claude/
├── agents/
│   ├── ace-scout.md        Read-only codebase mapper (runs in parallel)
│   ├── ace-builder.md      Implements exactly one concern, nothing more
│   ├── ace-skeptic.md      Adversarial verifier — its only job is to refute
│   └── ace-synthesizer.md  Merges everything into one ranked report
├── commands/
│   ├── orchestra.md        /orchestra — full pipeline for building or changing code
│   └── orchestra-audit.md  /orchestra-audit — read-only multi-lens code review
PLAYBOOK.md                 When to orchestrate, when to stay solo
LICENSE                     MIT — use it anywhere, including client work
```

## Install

1. Copy the `.claude/` folder into the root of your project (next to your `package.json`,
   `pyproject.toml`, etc.). If you already have a `.claude/` folder, merge the `agents/` and
   `commands/` directories into it — the `ace-` prefix keeps these files from colliding with
   your existing setup.
2. Open the project in Claude Code.
3. That's it. The agents and commands are picked up automatically.

## Use

**Build or change something, with verification built in:**

```
/orchestra add rate limiting to every public API endpoint
```

**Audit without changing anything:**

```
/orchestra-audit the checkout flow
/orchestra-audit          (whole project)
```

What happens under the hood, in order:

1. **SCOUT** — read-only scouts map the relevant parts of the codebase in parallel.
2. **FAN OUT** — the work is split into independent concerns; one builder takes each.
3. **VERIFY** — for every change or finding, a skeptic starts from "this is wrong" and tries
   to prove it. Only claims that survive make it through.
4. **MERGE** — a synthesizer assembles one ranked report: what was done, what was verified,
   what still needs a human.

## When to use it

Orchestration isn't speed. It's doubt. Reach for `/orchestra` when the work outgrows one
context, findings need independent checks, the task splits along clean seams, or being wrong is
expensive. For a one-file fix or a quick question, stay solo — plain Claude Code is the right
tool. The full decision guide is in `PLAYBOOK.md`.

## Uninstall

Delete the six `ace-*` / `orchestra*` files from `.claude/agents/` and `.claude/commands/`.
Nothing else is touched.

---

Made by Night Ace. If this saved you an afternoon, we're easy to find — #nightace.
