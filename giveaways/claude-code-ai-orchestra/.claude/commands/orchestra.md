---
description: Run the Night Ace AI orchestra — scout, fan out, verify, merge — on a build task
argument-hint: <what to build or change>
---

Run the Night Ace orchestra on this task: **$ARGUMENTS**

You are the conductor. You coordinate; the subagents do the work. Follow the four phases in
order and do not skip the verification phase, whatever the builders claim.

## Phase 1 — SCOUT (parallel, read-only)

Break the codebase territory relevant to the task into 2–4 areas. Launch one `ace-scout`
subagent per area, **in parallel**, each with a clearly bounded assignment. Wait for all maps.

If the task is trivially small after scouting (one file, one obvious change), say so, skip the
orchestra, and just do it — orchestration on a typo fix is theater. Otherwise continue.

## Phase 2 — FAN OUT (one builder per concern)

Split the task into independent concerns along the seams the scouts found — one endpoint, one
module, one migration each. For every concern, launch an `ace-builder` subagent whose prompt
contains: the concern (exactly one), the relevant scout map, and the conventions it must match.

Run builders whose files don't overlap in parallel; run overlapping ones sequentially. Never
give two builders the same file.

## Phase 3 — VERIFY (adversarial, one skeptic per claim)

For **every** builder change, launch an `ace-skeptic` subagent with the builder's handoff
report and the mandate to refute it. Never let a builder's own "it works" stand as
verification — that is one opinion counted twice.

Where a skeptic REFUTES a change: send the concern back to a **fresh** `ace-builder` with the
skeptic's evidence, then have a skeptic re-check the rework. Maximum two rework rounds; after
that, the item goes in the report as unresolved rather than looping forever.

## Phase 4 — MERGE

Launch one `ace-synthesizer` subagent with every builder report and every skeptic verdict.
Relay its ranked report to the user, then add one short conductor's note of your own: anything
you saw across phases that the reports individually miss.

## Conductor's rules

- Keep phase boundaries honest: no building during scouting, no verifying by the builder.
- Disagreement between agents is signal — surface it, never smooth it over.
- If the user's task is ambiguous enough that the fan-out could go two very different ways,
  ask before Phase 2, not after.
