# 01 — Task execution flow

## Default sequence

Apply this sequence for every non-trivial change. Skip a step only when
the task is genuinely smaller than the step.

1. **Frame the smallest correct scope.**
   - Restate the task in one sentence.
   - Identify the impacted layer(s) and service(s).
   - Decide whether this is a fix, a refactor, a feature, or research.

2. **Read the applicable canonical files.**
   - `memory/policies/*` for invariants relevant to the change.
   - `memory/rules/*` for the specific rule that governs the change
     (idempotency, validation, diagrams).
   - `memory/skills/<skill>/SKILL.md` if a named workflow applies.
   - The relevant service's `README.md` and immediate neighbors of the
     impacted file.

3. **Inspect the codepath.**
   - Trace from the entry point to the side effect.
   - Check tests that already cover the area.
   - Note the canonical idempotency keys per layer.

4. **Decide on delegation.**
   - Use a sub-agent (`memory/agents/*`) when the task is test-heavy,
     debug-heavy, doc-heavy, architecture-heavy, or cross-service.
   - Stay direct when the task is contained, mechanical, or already
     scoped.

5. **Make the smallest safe change.**
   - Match the local style.
   - Keep the diff inside the right layer.
   - Update or add the targeted tests in the same change.

6. **Validate at the right level.**
   - Apply the ladder in `02-validation-and-done-definition.md`.

7. **Update documentation.**
   - Use `policies/07-documentation-and-traceability.md` to decide
     which surfaces are affected.
   - Diagrams: `rules/05-diagrams-and-docs.md`.

8. **Summarize.**
   - State files touched, validation run, validation skipped (with
     reason), follow-ups left open.

## Definition of ready

Before starting, you should be able to answer:

- What is the user-visible outcome of this change?
- Which service(s) and layer(s) does it affect?
- Which contract(s) does it touch (Kafka topic, REST, schema, env var)?
- Which tests will prove it works?
- Is there a domain-safety concern (paper trading, idempotency,
  notification ownership)?

If any answer is "I don't know", inspect first.

## Escalation triggers

Stop and surface to the user when:

- The minimal fix requires a domain rule change
  (`policies/06-investment-domain-guardrails.md`).
- The change requires a destructive operation listed in
  `policies/05-security-and-secrets.md`.
- The change requires lowering a quality gate (Sonar, JaCoCo, Spotless).
- The cleanest fix violates a layer boundary
  (`policies/02-clean-architecture.md`).

## Forbidden patterns

- Skipping the inspection step "because the change is obvious".
- Bundling unrelated cleanup into a focused fix PR.
- Marking a task done with skipped validation and no explanation.
- Adding new env vars without updating both `.env.example` files.
- Editing a runtime adapter (`.claude/`, `.codex/`, `.cursor/`,
  `.agents/`) instead of the canonical `/memory` source.
