---
name: contract-change
description: Change an API or event contract safely — domain-safety review, backward-compatible implementation, E2E, contract docs.
trigger: A change to an HTTP endpoint, event topic, message schema, headers, or routing.
---

# Pipeline — Contract change

## When to run

Any change to a published contract (`stacks/rest-api-design.md`,
`stacks/messaging-kafka.md`, `rules/04-idempotency-and-event-contracts.md`).
Contracts are public APIs — treat every change as breaking until proven
additive.

## Preconditions

- The current contract and its consumers are identified.

## Stages

| # | agent / skill                | input                          | output                              | gate                                                        | on-fail                                       |
| - | ---------------------------- | ------------------------------ | ----------------------------------- | ----------------------------------------------------------- | --------------------------------------------- |
| 1 | `skills/domain-safety-review` | proposed change               | ownership + safety assessment       | no module publishes another's effect; guardrails intact     | stop, surface to user                          |
| 2 | `software-architect`         | change + consumers             | compatibility plan                  | change is **additive/optional**, or a **versioned** topic/endpoint with a migration | redesign as versioned at stage 2               |
| 3 | `implementation-engineer` / `skills/async-messaging-engineering` | compatibility plan | producer/consumer diff | idempotency keys per layer respected; consumers tolerate unknown fields | loop to stage 3                                 |
| 4 | `unit-test-engineer`         | diff                           | tests (incl. replay/duplicate)      | duplicate ⇒ no-op; same key+different payload ⇒ dead-letter  | loop to stage 3/4                               |
| 5 | `e2e-test-engineer`          | diff + workflow                | end-to-end run across producer+consumer | smoke passes                                             | loop to the owning stage                         |
| 6 | `technical-writer`           | contract delta                 | updated `docs/contracts/` (OpenAPI / AsyncAPI / JSON Schema / catalog) | schema + catalog updated in the same change     | loop to stage 6                                 |

## Output

```
Contract:     <endpoint/topic>:<version>
Compatibility: additive | versioned (migration: ...)
Idempotency:  <keys per layer>
Consumers:    <verified tolerant>
Docs:         docs/contracts/... updated
```
