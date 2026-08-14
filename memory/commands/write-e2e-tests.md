# /write-e2e-tests

Design or update smoke / E2E validation for a cross-module or
operator-visible workflow.

## Steps

1. State the workflow: trigger, path, expected observable outcome.
2. Reuse the repository's canonical smoke harness when possible
   (e.g. `scripts/smoke.sh`); extend it before adding a new script.
3. Document prerequisites (`.env` populated, `docker compose up -d`
   healthy — see `stacks/docker-compose.md`).
4. Author or extend the script: `[OK]/[FAIL]` lines, summary
   `N/N passed`, exit code reflects success.
5. Document failure signals (dead-letter destination, log line,
   dashboard).
6. Run end-to-end before declaring done; capture the pass count.

## Recommended delegates

- `e2e-test-engineer` (lead)
- `technical-writer` when the runbook is impacted
- `mermaid-architect` when a sequence diagram should accompany the smoke
