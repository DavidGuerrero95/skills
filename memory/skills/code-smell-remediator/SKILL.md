---
name: code-smell-remediator
description: Identify and reduce code smells, duplication, dead code, weak naming, oversized functions, and poor boundary placement without destabilizing behavior. Use after feature work, before merge, or when static analysis reports actionable smells. Focus is behavior-preserving cleanup, not redesign.
license: MIT
metadata:
  scope: refactoring-cleanup
  version: "2.0"
---

# Code-smell remediator

## When to use

- After feature work, as a focused cleanup pass.
- Before merging, in response to linter / static-analysis findings.
- When a function exceeds reasonable size and its responsibility blurs.
- When duplication has appeared in two or more places.
- When a unit has drifted across layers.

## When NOT to use

- A real architectural redesign — open an ADR and treat it as a feature.
- A bug fix — use `skills/implementation-bug-hunter`.
- A performance rewrite — out of scope.

## Read first

- `memory/policies/01-engineering-baseline.md`
- `memory/policies/02-clean-architecture.md`
- The active `memory/stacks/<stack>.md` for idiomatic replacements.

## Smells to look for

- **Duplication** of logic in two or more places.
- **Long functions** doing more than one thing.
- **Primitive obsession** where a value object / record / typed wrapper
  is missing.
- **Weak naming** that hides intent (`process`, `handle`, `data`,
  `manager`, `util`).
- **Misplaced units** (mappers in domain, framework imports in domain,
  business logic in handlers).
- **Dead code** — commented-out blocks, unused imports/params/privates.
- **Catch-and-rethrow** with no value added.
- **Optional/nullable misuse** — modeling required values as optional.
- **Magic numbers / strings** that deserve a named constant or enum.

## Workflow

1. **Bound the scope** to the diff or module under review. Do not sweep
   unrelated areas.
2. **Catalog the smells** before changing anything: `file:line` +
   one-sentence description.
3. **Order by safety:** behavior-preserving renames first, dead-code
   removals next, structural moves last.
4. **Apply the smallest fix** per smell; keep tests green at every step.
5. **Run the impacted module's tests** after each meaningful change.
6. **Surface deferred smells** explicitly with a reason.

## Output expected from this skill

```
Smells found:
 - <file:line>  duplication of X
 - <file:line>  long function (~70 LOC) mixing parsing + persistence

Smells fixed:
 - <file:line>  extracted ... ; tests still green
 - <file:line>  renamed ... for intent

Smells deferred:
 - <file:line>  requires moving X across a boundary — out of scope, see ADR

Validation:
 - [ran]  <test command>
```

## Behavior-preserving tactics

- Use IDE-driven safe refactors (extract, rename, inline) when available.
- Prefer adding a helper next to the original site over editing many
  call sites at once.
- Preserve signatures used by tests; if a signature must change, update
  tests in the same diff.
- If a smell is truly an architecture violation, **stop**, surface it,
  and let `agents/software-architect` decide.

## Forbidden patterns

- Sweeping unrelated cleanup into a feature change.
- Adding new behavior under cover of "refactor".
- Suppressing static-analysis issues with comments instead of fixing.
- Removing tests because they are inconvenient after the refactor.
