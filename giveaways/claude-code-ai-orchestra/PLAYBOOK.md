# The Orchestra Playbook

The one-sentence version: **an agent reviewing its own work is one opinion counted twice.**
Everything in this package exists to buy you independent opinions.

## Why a single context isn't enough

A single agent writes the code, then grades its own work. It anchors on its first idea and
defends it to the end of the context window — the same trap that makes authors bad reviewers
of their own code. No prompt fixes this, because it isn't a prompting problem. It's an
incentive-structure problem. The fix is separation of duties: the agent that verifies must not
be the agent that built.

## When to orchestrate

Run every task through four checks. If two or more are true, orchestrate.

1. **The work outgrows one context.** Nobody — human or model — holds a whole codebase in
   their head at once. Parallel scouts each hold a piece.
2. **Findings need independent checks.** Security reviews, data migrations, anything where
   "the model sounded confident" is not acceptable evidence.
3. **The task splits along clean seams.** One builder per endpoint, per module, per page.
   Clean seams mean builders don't trip over each other.
4. **Being wrong is expensive.** Cost of a mistake ≫ cost of a second opinion.

## When to stay solo

- One-file fixes
- Quick questions
- Exploration and prototyping, where you *want* momentum over rigor
- Anything cheap to redo

Orchestration has overhead. Spending it on a typo fix is theater, not engineering.

## The four roles

| Role | Mandate | May write files? |
|---|---|---|
| Scout | Map the territory; report facts with file:line evidence | No |
| Builder | Implement exactly one concern | Yes |
| Skeptic | Start from "this is wrong" and try to prove it | No |
| Synthesizer | Merge everything into one ranked, honest report | No |

The load-bearing rule: **the skeptic never verifies its own builder's work by intent — it is
a different agent with a different context and an adversarial mandate.** Disagreement between
agents is not noise to smooth over. It's the signal. When a skeptic refutes a builder, that
disagreement is the most valuable output of the whole run.

## Reading the final report

The synthesizer's report separates claims into three buckets:

- **Verified** — a skeptic tried to break it and failed. Trust these the most.
- **Refuted / reworked** — a skeptic found a real problem; the item was fixed and re-checked,
  or flagged.
- **Needs a human** — judgment calls, product decisions, anything the orchestra can't settle
  with evidence. This bucket is a feature, not a failure.

If a report ever arrives with an empty "needs a human" bucket on a non-trivial task, be
suspicious — that's usually overconfidence, not perfection.

---

Made by Night Ace — process over prompts.
