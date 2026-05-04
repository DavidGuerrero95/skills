---
name: code-smell-remediator
description: Identify and reduce code smells, duplication, dead code, weak naming, oversized methods, and poor boundary placement without destabilizing behavior. Use after feature work, before merge, or when Sonar reports actionable smells. Focus is behavior-preserving cleanup, not redesign.
license: Proprietary. Internal use only.
metadata:
  owner: invexa-platform
  scope: refactoring-cleanup
  version: "1.1"
---

# Code-smell remediator

## When to use

- After feature work, as a focused cleanup pass.
- Before merging, in response to Sonar findings.
- When a method exceeds reasonable size and the responsibility is
  blurred.
- When duplication has appeared in two or more places.
- When a class has been quietly drifting across layers.

## When NOT to use

- A real architectural redesign — open an ADR and treat it as a
  feature.
- A bug fix — use `skills/implementation-bug-hunter`.
- A perf rewrite — out of scope for this skill.

## Read first

- `memory/policies/01-engineering-baseline.md`
- `memory/policies/02-clean-architecture.md`

## Smells to look for

- **Duplication** of logic in two or more places.
- **Long methods** doing more than one thing.
- **Primitive obsession** where a value object or `record` is missing.
- **Weak naming** that hides intent (`process`, `handle`, `data`,
  `manager`).
- **Misplaced classes** (mappers in `domain`, framework imports in
  `domain`, business logic in handlers).
- **Dead code** — commented-out blocks, unused imports, unused
  parameters, unused private methods.
- **Catch-and-rethrow** with no value added.
- **Optional misuse** — Optional fields, Optional in signatures used
  to model required values.
- **Magic numbers / strings** that deserve a named constant or enum.

## Workflow

1. **Bound the scope** to the diff or the module under review. Do not
   sweep unrelated areas.
2. **Catalog the smells** before changing anything. Output: a short
   list with file:line and a one-sentence description.
3. **Order by safety:** behavior-preserving renames first, dead code
   removals next, structural moves last.
4. **Apply the smallest fix** for each smell. Keep tests green at every
   step.
5. **Run the impacted module's tests** after each meaningful change.
6. **Surface deferred smells** explicitly with a reason
   ("requires architecture change", "outside scope").

## Output expected from this skill

```
Smells found:
 - <file:line>  duplication of X
 - <file:line>  long method (~70 LOC) mixing parsing + persistence

Smells fixed:
 - <file:line>  extracted ... ; tests still green
 - <file:line>  renamed ... for intent

Smells deferred:
 - <file:line>  requires moving X into driven-adapter — out of scope, see ADR-0XX

Validation:
 - [ran]  ./gradlew :<service>:<module>:test
```

## Behavior-preserving tactics

- Use IDE-driven safe refactors when available (extract method, rename
  symbol, inline).
- Prefer adding a new helper next to the original site over editing
  many call sites at once.
- Preserve method signatures used by tests; if a signature must
  change, update tests in the same diff.
- If a smell is truly an architecture violation, **stop**, surface it,
  and let `agents/java-architect` decide.

## Forbidden patterns

- Sweeping unrelated cleanup into a feature PR.
- Adding new behavior under cover of "refactor".
- Suppressing Sonar issues with comments instead of fixing them.
- Removing tests because they are inconvenient after the refactor.
