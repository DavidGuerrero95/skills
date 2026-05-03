# Foundation analysis

## What was found in the current repository

The current INVEXA setup already has a strong Codex-oriented foundation:

- `AGENTS.md` centralizes working mode, mandatory policies, non-negotiable rules, local skills, and project context.
- `.codex/` already contains:
  - `policies/`
  - `skills/`
  - `knowledge/`
  - `archive/`
- `.cursor/rules/` contains project, engineering, architecture, reactive, Kafka, and idempotency rules.
- The repository domain is not generic: it is a **personal investment platform** with **five Java 21 reactive microservices**, shared infrastructure, Kafka choreography, reconciliation, idempotency, and strict testing/smoke workflows.

## Architectural issue in the current layout

The current structure is useful, but it mixes:
- long-lived policy,
- runtime-discovery artifacts,
- knowledge-base content,
- agent workflows,
- project context,
- and tool-specific folders.

That makes reuse harder when you want the same foundation to work for **Claude**, **Codex**, and **Cursor** without copying the same context repeatedly.

## What this scaffold changes

This scaffold introduces a **canonical `/memory` layer** and keeps tool-specific folders as adapters only.

### Before
- Tool folder often owned both the source content and the runtime integration.

### After
- `/memory` owns the intent and content.
- `.claude`, `.codex`, `.agents`, and `.cursor` are thin compatibility layers.
- The same skill/policy/agent can be exposed to multiple runtimes without re-authoring the full content.

## Result

You get:
- one reusable base for future repositories,
- lower instruction drift,
- cleaner SRP boundaries,
- clearer migration path from Cursor/Codex-centric setup to Claude + Codex parity,
- and room for automation through hooks and specialized agents.
