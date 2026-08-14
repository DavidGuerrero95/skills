# 05 — Security and secrets

## Purpose

Define the non-negotiable security and supply-chain rules. Specific
shell-safety detection is implemented in
`scripts/agentic/pre_bash_safety_guard.py` (`pre-bash-safety-guard`
hook); secret-shaped-string detection in
`scripts/agentic/pre_write_secret_scan.py` (`pre-write-secret-scan`
hook). This policy is stack-agnostic.

## Secrets

- **Never hardcode** secrets, tokens, credentials, or private keys in
  source files, tests, comments, sample payloads, logs, or
  documentation.
- The canonical template is the repo-root `.env.example`. Operators copy
  it to `.env` / `.env.local` (never committed) and inject it into the
  runtime (Docker Compose, container secrets, CI secrets).
- Read secrets only via environment variables or a secret manager,
  documented in `.env.example` and the affected module README.
- When showing a sample value, use a clearly fake placeholder
  (`sk-REDACTED`, `xxxx-xxxx`, `your-token-here`).
- Do not include secret-shaped strings in commit messages, branch names,
  PR descriptions, or agent docs.

## Destructive command guardrails

The following require explicit operator confirmation, even when the
agent believes them safe:

- `rm -rf` against any path other than `/tmp/...` or a build output.
- `git push --force` (any target).
- `git reset --hard`, `git clean -fd`, `git checkout .` against tracked
  files with uncommitted state.
- `docker system prune`, `docker volume prune`, `docker network prune`.
- `terraform destroy`, `kubectl delete ns`, `kubectl delete -f`.
- `DROP DATABASE`, `DROP SCHEMA`, `TRUNCATE TABLE`, `db.dropDatabase()`
  against any datastore.
- Bulk file deletion via wildcards (`rm *`, `Remove-Item -Recurse`).
- Credential reset / rotation commands (broker, registry, cloud).

The pre-bash safety hook denies the worst of these and warns on the
rest. **Hook deny is not a substitute for judgment.** If a destructive
command is required, surface it to the user before running it.

## Supply-chain rules

- **Dependency versions are centralized** in the project's single source
  (root build manifest / lockfile). Child modules inherit; they do not
  declare their own versions.
- New dependencies require:
  - a one-line rationale in the PR description (why this lib?),
  - a check that the artifact is published from an official source,
  - confirmation that the licence is compatible with the project's
    distribution.
- Prefer pinning to a specific version over a range.
- Commit lockfiles (`package-lock.json`, `poetry.lock`, `uv.lock`,
  `gradle.lockfile`, `go.sum`) so builds are reproducible.
- Enable dependency and secret scanning in CI
  (`.github/workflows/ci.yml`).

## Network and external services

- Avoid introducing unreviewed outbound network calls. Every external
  call is owned by an outbound adapter, has a timeout, and surfaces a
  configurable URL via env var.
- Do not enable a new third-party SDK in tests by hitting the real
  endpoint. Use Testcontainers, a recorded fixture, or a local stub.

## Logging hygiene

- Never log secrets, full HTTP bodies that may contain PII, or broker
  passwords.
- Logs include canonical correlation keys (`requestId`, `correlationId`,
  domain ids) so an investigator can correlate. Levels: INFO for
  successful flows, WARN for retries / fallbacks, ERROR for failures.

## Forbidden patterns

- Shell commands that delete or rotate state without explicit operator
  confirmation.
- Hardcoded API keys in tests.
- New env vars added in code without updating `.env.example`.
- Logging request bodies in production.
- Disabling auth / TLS "to make local debugging easier" and forgetting
  to revert.
