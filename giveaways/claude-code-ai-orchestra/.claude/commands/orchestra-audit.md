---
description: Read-only multi-lens audit with the Night Ace orchestra — nothing gets modified
argument-hint: <area to audit, or empty for the whole project>
---

Run a read-only Night Ace orchestra audit on: **$ARGUMENTS** (if empty: the whole project,
scoped to what matters — skip vendored code, lockfiles, and generated files).

Hard rule for the entire run: **nothing is modified.** No edits, no fixes, no "while I'm
here." Every subagent works read-only; findings are reported, not repaired.

## Phase 1 — SCOUT (parallel)

Launch 2–4 `ace-scout` subagents in parallel, one per area of the audit target. Their maps
tell the reviewers where to dig.

## Phase 2 — REVIEW LENSES (parallel)

Launch one `ace-skeptic` subagent per lens, in parallel, each with the scout maps and one
mandate:

- **Correctness** — logic errors, broken edge cases, error paths that swallow failures
- **Security** — injection, authz gaps, secrets in code, unsafe input handling
- **Performance** — N+1 patterns, hot-path waste, unbounded growth
- **Maintainability** — dead code, duplication, tests that assert nothing

Each lens reports concrete findings with `file:line` and a plausible failure scenario — not
style opinions.

## Phase 3 — VERIFY (adversarial cross-check)

For each finding, launch a **fresh** `ace-skeptic` whose job is to refute that finding: is it
real, reachable, and consequential? A finding written by one lens is never confirmed by the
agent that wrote it. Findings that don't survive are dropped into a discard list, not
silently deleted.

## Phase 4 — MERGE

Launch one `ace-synthesizer` with all verdicts. Deliver its report ranked by consequence:
confirmed findings first with evidence, then unresolved disagreements, then the discard list
in one line each (so the user can see what was considered and rejected), then what the audit
did not cover.

No invented severity theater: if the audit found little, say the codebase held up well and
state exactly what was checked.
