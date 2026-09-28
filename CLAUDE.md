# CLAUDE.md

How to work in this repo. What is being built and why lives in the `PLAN*.md` docs,
not here.

## How to work with me

- **Restate concepts back.** When I describe a concept or design, repeat it back
  simply and briefly before acting.
- **Don't assume. Check, or ask.** If something can be checked (a file, running the
  code, git history), check it. If it can't, or you're still unsure, ask. Also flag
  requests whose risk or consequences might not have been thought through.
- **Keep it simple.** Keep asking whether the solution is the simplest one that works.
- **Check MCP tools first.** A connected MCP tool may already do the job better than
  doing it by hand.
- **Refer to steps by name**, e.g. "Step 15 — Keyword-expansion pass", not just
  "Step 15".

## Progress over perfection

Lesson learned: getting stuck on early details cost the most time. Most of those
issues later went away on their own, because the scope changed or because fixing a
bigger issue fixed them too.

- **Does it block the next milestone?** Yes: fix it. No: add it to "Open / deferred"
  in `PLAN.md` and move on.
- **Good enough to move forward beats perfect.** Get the whole thing working roughly
  first, then improve the parts that turn out to matter.
- **Stop when stuck.** If an issue is still unsolved after ~2 attempts, stop and ask
  me whether it's worth more time before trying again.
- **Keep the goal in view.** Even deep in a detail, ask whether this still serves the
  end goal in `PLAN.md`.

## Checkpoint: pivot or double down?

Run this at every milestone, and whenever work has stalled. Keep it to a few lines
in chat:

1. Are we closer to the end goal? Is the end goal itself still right?
2. Did anything we learned change the plan? Update the milestones.
3. Are any deferred items solved or no longer relevant? Remove them.
4. Is anything costing more than it's worth? Recommend one of: **continue**,
   **simplify**, **pivot**, or **drop**.

## Plans: fixed ends, growing middle

At the start you don't know enough to plan every step. So:

- **Fix the ends.** `PLAN.md` opens with the **Start** (what exists now), the **Goal**
  (what done looks like, in a few lines), and **Done when** (how we'll know it's
  done). Change these only on purpose, at a checkpoint.
- **Grow the middle.** Milestones start as one-liners and get filled in as we learn.
  Only the next milestone needs detailed steps.
- **Detail grows with depth.** The top-level `PLAN.md` stays short: goal, milestones,
  status. Detailed steps go in the subfolder plan for that part. Too much detail at
  the top distracts from the current issue. Too little at the bottom loses precision.

## Docs

Each initiative keeps its docs in one place. Once there are enough of them to
clutter the code, move them into a `plans_verifications_models/` subfolder.

| Doc | Job |
|---|---|
| `PLAN.md`, `PLAN2.md`, ... | Start, Goal, and Done when, then milestones, then Open / deferred. One file per arc of work, numbered in the order the arcs start. Shared goals go in `PLAN.md` only. |
| `PLAN_INDEX.md` (optional) | One line: which arc is active now. |
| `VERIFICATION_INDEX.md` + `VERIFICATION_PHASE_A.md`, `_B.md`, ... | Evidence: what was run, the results, the bugs found and fixed. Letters keep counting across all arcs. Split a phase once it passes ~300 lines. |
| `MODEL.md` (optional) | The mental model: how to reason about the domain. No thresholds or code. |

Read them in this order: this file → `PLAN_INDEX.md`/`PLAN.md` → the verification
docs.

**Verification docs:** give each specific finding its own header, and put searchable
terms in it (ticker, exact phrase, concept).

**New truth replaces old.** Once a phase is written, don't rewrite it. When a new
finding overrides an old one:
- the new finding says `Supersedes: <old header>`
- the old one gets a single line added: `Superseded by: <new header>`
- `VERIFICATION_INDEX.md` has a **Current truths** list at the top: one line per
  conclusion that holds now, each pointing to its latest finding. Edit this list;
  never edit the history.

**Drafts:** name them `DRAFT_<topic>.md` and don't give them a number yet. They get
one when they become the active arc.

## Keeping docs accurate

Accuracy matters more than being short or complete. Out-of-date guidance is worse
than none, because people still trust it.

- Point to docs that stay current anyway instead of copying facts that go stale.
  Current-state facts belong in `PLAN.md`.
- If a fix is obvious, just make it. If the staleness points to a real design
  question, ask.
- Don't write dates by hand. `git log`/`git blame` already has them.

## Before investigating a question or issue

1. Check **Current truths** in `VERIFICATION_INDEX.md`, then the phase docs.
2. Then check the code. Past lessons can be built into it without being written
   down anywhere.
3. A match is a lead, not the answer. Check it still holds.

## Code comments

Short and plain: one or two lines on what the code does. No history, step numbers,
or doc references. Skip the comment if the names already make it clear.

## Git

- **Commit automatically** only when a `PLAN*.md` checklist item goes from `- [ ]` to
  `- [x]`, and name the step in the message. Ask before any other commit.
- **Never push** without an explicit ask, every time.
