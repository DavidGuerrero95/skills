---
name: dependency-management
description: Add, upgrade, or remove dependencies safely across any package manager (Gradle/Maven, uv/Poetry/pip, npm/pnpm, Go modules) while keeping versions centralized, supply-chain inputs reviewed, and licence posture intact. Use whenever an artifact is introduced, a version is bumped, a transitive conflict appears, or a licence concern is raised.
license: MIT
metadata:
  scope: dependencies-supply-chain
  version: "2.0"
---

# Dependency management

## When to use

- Adding a new third-party library.
- Bumping an existing version (security or feature).
- Removing an unused dependency.
- Resolving a transitive version conflict.
- Reviewing a supply-chain or licence concern flagged in CI.

## When NOT to use

- Pure code changes inside an existing dependency.
- Feature implementation — `skills/feature-implementation`.

## Read first

- `memory/policies/01-engineering-baseline.md` (centralization rule)
- `memory/policies/05-security-and-secrets.md` (supply-chain rules)
- The active `memory/stacks/<stack>.md` for the manifest/lockfile.

## Centralization rule (non-negotiable)

- **Versions live in the project's single source:** root `build.gradle`
  / `gradle/libs.versions.toml`, `pyproject.toml`, root `package.json`,
  `go.mod`.
- Child modules reference coordinates without versions and inherit them.
- Commit the **lockfile** so builds are reproducible.

## Workflow

1. **State the need.** Why this dependency; what the alternative is
   (in-tree code, stdlib, an existing dep).
2. **Pick a published artifact from a trusted source.** Official
   registry; pin an exact version, never a floating range.
3. **Check the licence.** Compatible with the project's distribution;
   note anything unusual in the PR.
4. **Add at the single source** and update the lockfile.
5. **Use in modules** by coordinate; confirm the correct scope
   (runtime vs. dev/test vs. compile-only).
6. **Resolve transitive conflicts** explicitly with the tool's
   inspection command; pin only for a real conflict.
7. **Validate.** Build + tests for impacted modules; quality gates green;
   the CI dependency/secret scan does not flag the change.

## Output expected from this skill

```
Dependency change:
 - added | bumped | removed: <coordinate> -> <version>

Reason:
 - <one-paragraph>

Supply-chain notes:
 - source registry, licence, transitive impact

Files touched:
 - <manifest> (single source), <lockfile>

Validation:
 - [ran]  <build/test command>
 - [ran]  <dependency inspection> (when conflicts suspected)
```

## Forbidden patterns

- Declaring a version per-module instead of centrally.
- Pulling a dependency from an unknown source.
- Pinning a floating range that changes across builds.
- Bumping a major version silently inside a feature change.
- Adding a dependency without recording the rationale.
- Committing without updating the lockfile.
