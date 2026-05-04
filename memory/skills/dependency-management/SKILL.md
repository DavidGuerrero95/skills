---
name: dependency-management
description: Add, upgrade or remove Gradle dependencies safely while keeping versions centralized in the root build.gradle, supply chain inputs reviewed, and license posture intact. Use whenever a new artifact is introduced, a version is bumped, a transitive conflict appears, or a licence concern is raised.
license: Proprietary. Internal use only.
metadata:
  owner: invexa-platform
  scope: gradle-dependencies-supply-chain
  version: "1.0"
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
- Spring/Reactor implementation work — `skills/java-spring-implementation`.
- Static analysis configuration changes — separate, limited diff.

## Read first

- `memory/policies/01-engineering-baseline.md` (centralization rule)
- `memory/policies/05-security-and-secrets.md` (supply-chain rules)

## Centralization rule (non-negotiable)

- **All dependency versions are declared in the root `build.gradle`** (or
  the project's `versions.toml` / `gradle/libs.versions.toml`, when
  used).
- Child modules **must not** declare their own versions. They depend on
  named coordinates and inherit the version from the root.
- A new dependency lands in two diffs combined into one commit: root
  declaration + child usage.

## Workflow

1. **State the need.**
   - Why this dependency is required.
   - What the alternative is (in-tree code, JDK, an existing dep).

2. **Pick a published artifact from a trusted source.**
   - Maven Central or an explicitly approved internal registry.
   - Pin to a specific version (`1.2.3`), never a range (`1.+`).

3. **Check the licence.**
   - Compatible with this project's distribution model.
   - Document the licence in the PR description if it is unusual.

4. **Add at the root.**
   - Update root `build.gradle` (or `libs.versions.toml`).
   - Group with related deps.

5. **Use in child modules.**
   - Reference by coordinate (no version).
   - Confirm the dependency is in the correct configuration:
     `implementation` / `api` / `runtimeOnly` / `testImplementation`.

6. **Resolve transitive conflicts** explicitly.
   - Use `dependencyInsight` to inspect:

     ```powershell
     .\gradlew.bat :<service>:<module>:dependencyInsight --dependency <coord>
     ```

   - Pin via `resolutionStrategy` only when there is a real conflict.

7. **Validate.**
   - `./gradlew.bat clean test` for the impacted modules.
   - Spotless / Sonar / JaCoCo gates remain green.
   - The `.github/workflows/ci.yml` secret-scan does not flag the
     change.

## Output expected from this skill

```
Dependency change:
 - added | bumped | removed: <coord> -> <version>

Reason:
 - <one-paragraph>

Supply-chain notes:
 - source registry, licence, transitive impact

Files touched:
 - build.gradle (root)
 - <service>/<module>/build.gradle

Validation:
 - [ran]  ./gradlew :<service>:<module>:test
 - [ran]  ./gradlew :<service>:dependencies (when conflicts suspected)
```

## Forbidden patterns

- Declaring a version inside a child-module `build.gradle`.
- Pulling a dependency from an unknown source.
- Pinning a version range that floats across builds.
- Bumping a major version (`X.0.0`) silently inside a feature PR.
- Adding a dependency without recording the rationale in the PR.
