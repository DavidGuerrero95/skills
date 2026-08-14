---
name: state-of-the-art-research
description: Research architecture, implementation, or platform decisions using local repository context and documented standards before proposing a new baseline. Use when selecting between patterns, comparing options for a shared foundation, or proposing a new module skeleton, ADR, or migration.
license: MIT
metadata:
  scope: research-tradeoffs
  version: "2.0"
---

# State-of-the-art research

## When to use

- Proposing a new baseline (module skeleton, build pattern, library).
- Comparing two or more architectural patterns for a specific need.
- Selecting between candidate libraries or frameworks.
- Evaluating a tradeoff before opening an ADR.

## When NOT to use

- A specific bug fix — `skills/implementation-bug-hunter`.
- A focused implementation — `skills/feature-implementation`.
- A pure cleanup — `skills/code-smell-remediator`.

## Read first

- `memory/policies/00-governance.md`
- `memory/policies/01-engineering-baseline.md`
- `memory/policies/02-clean-architecture.md`
- The active `memory/stacks/<stack>.md` (what is non-negotiable).
- The relevant module README and related ADRs under `docs/adr/`.

## Workflow

1. **State the constraint.** What the repo already does, what forced the
   question now, and what is non-negotiable (language/framework version,
   architecture, datastore, delivery model).

2. **List candidate options.** At least two; prefer three when the field
   is open. For each: what it does, where it is used in industry, what it
   changes here, what it costs.

3. **Show tradeoffs.** A small comparison table: option vs. axis
   (complexity, blast radius, ecosystem maturity, footprint, alignment
   with the existing repo). Flag any option that violates a policy.

4. **Recommend a baseline.** Choose one; explain why the alternatives
   were rejected; state the smallest first step (spike, ADR, prototype).

5. **Cite local sources.** Repository file paths, existing ADRs, and any
   reference material actually used.

## Output expected from this skill

```
Constraint:
 - <one paragraph>

Candidates:
 - <option A>: <one paragraph>
 - <option B>: <one paragraph>

Tradeoff table:
 | option | complexity | alignment | risk | cost |

Recommendation:
 - <option X> because ...

Rejected alternatives:
 - <option Y> because ...

Smallest first step:
 - <ADR / spike / prototype>

Sources:
 - <repo path>:<line>
 - docs/adr/<adr>.md
```

## Forbidden patterns

- Comparing options without grounding them in the repository.
- Recommending a tool the repo cannot adopt without violating a policy.
- A "research" output that is actually an implementation.
- Citing external blogs as load-bearing without local verification.
