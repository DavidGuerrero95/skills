---
name: state-of-the-art-research
description: Research architecture, implementation, or platform decisions using local repository context and documented standards before proposing a new baseline. Use when selecting between patterns, comparing options for a shared foundation, or proposing a new service skeleton, ADR, or migration.
license: Proprietary. Internal use only.
metadata:
  owner: invexa-platform
  scope: research-tradeoffs
  version: "1.1"
---

# State-of-the-art research

## When to use

- Proposing a new baseline (service skeleton, build pattern, library).
- Comparing two or more architectural patterns for a specific need.
- Selecting between candidate libraries or frameworks.
- Evaluating a tradeoff before opening an ADR.

## When NOT to use

- A specific bug fix — use `skills/implementation-bug-hunter`.
- A focused implementation — use `skills/java-spring-implementation`.
- A pure cleanup — use `skills/code-smell-remediator`.

## Read first

- `memory/policies/00-governance.md`
- `memory/policies/01-engineering-baseline.md`
- `memory/policies/02-clean-architecture.md`
- The relevant service README and any related ADRs under `docs/adr/`.
- Any local knowledge under `.codex/knowledge/` (technical or
  functional).

## Workflow

1. **State the constraint.**
   - What the repository already does.
   - What forced this question now.
   - What is non-negotiable (Java 21, Spring 4.0.x, hex architecture,
     Kafka 4.x SCRAM, PostgreSQL/Mongo/Valkey, etc.).

2. **List candidate options.**
   - At least two. Prefer three when the field is open.
   - For each, capture: what it does, where it is used in industry,
     what it would change in this repo, what it would cost.

3. **Show tradeoffs.**
   - Use a small comparison table: option vs. axis (complexity,
     blast radius, ecosystem maturity, footprint, alignment with
     existing repo).
   - Flag any option that violates a policy.

4. **Recommend a baseline.**
   - Choose one.
   - Explain why the rejected alternatives were rejected.
   - State the smallest first step (often a spike, ADR or a single
     prototype module).

5. **Cite local sources.**
   - Repository file paths.
   - Existing ADRs.
   - Books or reference repos under `.codex/knowledge/` if used.

## Output expected from this skill

```
Constraint:
 - <one paragraph>

Candidates:
 - <option A>: <one paragraph>
 - <option B>: <one paragraph>
 - <option C>: <one paragraph>

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
 - .codex/knowledge/<topic>.md
```

## Forbidden patterns

- Comparing options without grounding them in the repository.
- Recommending a tool the repo cannot adopt without violating a
  policy.
- A "research" output that is actually an implementation.
- Citing external blogs as load-bearing without local verification.
