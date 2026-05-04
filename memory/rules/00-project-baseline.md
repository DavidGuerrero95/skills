# 00 — Project baseline rule

## Working mode

The default working order for any non-trivial task is:

1. **Inspect.** Read the relevant policy, the impacted module, neighbors,
   and recent commits. Form a hypothesis before changing anything.
2. **Change.** Make the smallest correct diff. Stay inside the layer
   that owns the responsibility.
3. **Validate.** Run the smallest meaningful validation per the
   ladder in `02-validation-and-done-definition.md`.
4. **Summarize.** Report what changed, what was validated, and what
   remains. Be specific about skipped checks.

## Default posture

- **Minimal diffs over sweeping rewrites.** Surrounding cleanup is not
  required and is often noise.
- **Flag architecture violations** rather than silently extending them.
  If the cleanest fix forces a violation, surface it and stop for
  guidance.
- **Output is copy-paste ready.** Code blocks are syntactically
  correct, paths are absolute or repository-relative, commands run
  unmodified on the documented shell.
- **Adapt to the existing shape.** This is not a blank-slate project.
  Conform to the repository conventions defined in `policies/01-*`
  and the per-service layout under `policies/02-*`.
- **Trust the policy file** over chat history. If chat says one thing
  and `memory/policies/*` says another, the policy wins.

## What "task" means here

A task is a unit of work small enough to keep open from inspection to
summary in one focused session. If a task expands beyond that, split
it and re-plan; don't grow a single diff to cover unrelated areas.

## When in doubt

- Prefer asking for guidance over committing a risky decision.
- Prefer a smaller, working change over a larger, speculative one.
- Prefer linking to a policy file over re-arguing the rule in chat.
