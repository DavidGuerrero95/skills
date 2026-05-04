# 05 — Security and secrets

## Purpose

Define the non-negotiable security and supply-chain rules. Specific
shell-safety detection is implemented in
`scripts/agentic/pre_bash_safety_guard.py` and registered as the
`pre-bash-safety-guard` hook.

## Secrets

- **Never hardcode** secrets, tokens, credentials, or private keys in
  source files, tests, comments, sample payloads, logs, or
  documentation.
- The canonical templates are `infrastructure/.env.example` and the
  repo-root `.env.example`. Operators copy these to `.env.local` (not
  committed) and inject into Docker Compose / Spring profiles.
- Read secrets only via environment variables documented in the
  templates. Document any new variable in both `.env.example` files
  and in the affected service README.
- When showing a sample value, use a clearly fake placeholder
  (`sk-REDACTED`, `xxxx-xxxx`).
- Do not include secret-shaped strings in commit messages, branch
  names, PR descriptions or AGENTS.md.

## Destructive command guardrails

The following commands require explicit operator confirmation, even
when the agent believes them safe:

- `rm -rf` against any path other than `/tmp/...` or a build output.
- `git push --force` (any target).
- `git reset --hard`, `git clean -fd`, `git checkout .` against tracked
  files with uncommitted state.
- `docker system prune`, `docker volume prune`, `docker network prune`.
- `terraform destroy`, `kubectl delete ns`, `kubectl delete -f`.
- `DROP DATABASE`, `DROP SCHEMA`, `TRUNCATE TABLE` against any DB.
- Bulk file deletion via wildcards (`rm *`, `Remove-Item -Recurse`).
- Credential reset / rotation commands (broker, registry, cloud).

The pre-bash safety hook denies the worst of these and warns on the
rest. **Hook deny is not a substitute for judgment.** If a destructive
command is required, surface it to the user before running it.

## Supply-chain rules

- **Dependency versions are centralized** in the root `build.gradle`
  (or root `versions.toml` if used). Child modules inherit; they do
  not declare their own versions.
- New dependencies require:
  - a one-line rationale in the PR description (why this lib?),
  - a check that the artifact is published from an official source,
  - confirmation that the licence is compatible with the project's
    distribution.
- Prefer pinning to a specific version (`1.2.3`) over a range (`1.+`).
- Avoid pulling transitive plugin behavior change (e.g. Gradle plugin
  `apply false` patterns) without a corresponding ADR if it changes
  build semantics.

## Network and external services

- Avoid introducing unreviewed outbound network calls. Every external
  call is owned by a `driven-adapter`, has a timeout, and surfaces a
  configurable URL via env var.
- Do not enable a new third-party SDK in tests by hitting the real
  endpoint. Use Testcontainers, a recorded fixture, or a local stub.

## Logging hygiene

- Never log secrets, full HTTP bodies that may contain PII, or broker
  passwords.
- Logs include canonical keys (`eventId`, `clientOrderId`,
  `portfolioId`) so an investigator can correlate. Levels: INFO for
  successful flows, WARN for retries / fallbacks, ERROR for failures
  that route to DLQ or alerting.

## Forbidden patterns

- Shell commands that delete or rotate state without explicit
  operator confirmation.
- Hardcoded API keys in tests.
- New env vars added in code without `.env.example` updates.
- Logging request bodies in production.
- Disabling SCRAM, TLS, or auth "to make local debugging easier" and
  forgetting to revert.
