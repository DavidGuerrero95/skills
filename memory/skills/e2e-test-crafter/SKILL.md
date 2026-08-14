---
name: e2e-test-crafter
description: Create or refine end-to-end and smoke validation for multi-module/multi-service flows, operator scripts, messaging pipelines, and API workflows. Use whenever a workflow crosses module boundaries, an operator runbook needs a smoke check, or a contract change must be validated end-to-end.
license: MIT
metadata:
  scope: smoke-e2e
  version: "2.0"
---

# E2E + smoke test crafter

## When to use

- Multi-module / multi-service workflows.
- Smoke scripts operators run to verify a deploy.
- Messaging pipelines where multiple topics/queues participate.
- API workflows spanning several endpoints and side effects.

## When NOT to use

- Single-unit behavior — `skills/unit-test-crafter`.
- Adapter-only behavior — a Testcontainers integration test inside the
  module.
- Documentation-only changes — `skills/technical-doc-writer`.

## Read first

- `memory/policies/04-testing-and-quality-gates.md`
- `memory/policies/06-domain-guardrails.md`
- `memory/rules/02-validation-and-done-definition.md`
- `memory/rules/04-idempotency-and-event-contracts.md`
- `memory/stacks/docker-compose.md` (for local infra)

## Workflow

1. **State the workflow under test.**
   - Trigger (HTTP call, scheduler tick, operator command).
   - Path (modules, topics, side effects).
   - Expected observable outcome (DB row, message, notification, log
     line, HTTP response).

2. **Reuse existing scripts/harnesses** before adding a new one. Extend
   `scripts/smoke.sh` (or the repo's equivalent) where possible.

3. **Document prerequisites.**
   - `.env` populated from `.env.example`.
   - Local infra up (`docker compose up -d`) and healthy.

4. **Author or extend the script.**
   - Bash scripts use `set -euo pipefail`.
   - Each assertion prints `[OK] ...` / `[FAIL] ...`.
   - Exit code reflects success/failure; print a final count
     (`17/17 passed`).

5. **Make assertions operator-readable** using canonical
   topic/endpoint/entity names.

6. **Document failure signals.**
   - Which dead-letter destination to inspect, which log line to grep,
     which dashboard panel to open.

7. **Run the script end-to-end** before declaring done; capture the pass
   count in the summary.

## Output expected from this skill

```
Workflow: <one-line description>
Trigger:  <HTTP / message / scheduler / operator>
Modules involved: <list>
Topics/endpoints: <list>

Prerequisites:
 - .env populated
 - docker compose up -d (healthy)

Commands:
 - bash scripts/smoke.sh

Assertions performed:
 - <bullet>

Failure signals:
 - dead-letter   ⇒ <name>
 - log line      ⇒ <pattern>
 - dashboard     ⇒ <panel>

Validation run:
 - [ran]  bash scripts/smoke.sh  (N/N passed)
```

## Forbidden patterns

- A smoke script that exits 0 on partial failure.
- An E2E run depending on cached fixtures from a previous run without an
  explicit reset.
- Hardcoding secrets, chat ids, or environment URLs into the script.
- Writing a brand-new script when a canonical one could be extended.
