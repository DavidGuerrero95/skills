---
name: database-change
description: Schema / migration / index change — design from access patterns, safe migration, adapter code, integration tests, review.
trigger: A change to a table/collection, column/field, constraint, index, or a hot query.
---

# Pipeline — Database change

## When to run

Any schema/migration/index change (`commands/design-database.md`). Read
`stacks/postgresql.md` and/or `stacks/mongodb.md` first.

## Preconditions

- The access patterns (queries/writes, frequency, latency budget) are
  known.

## Stages

| # | agent                     | input                          | output                              | gate                                                        | on-fail                                       |
| - | ------------------------- | ------------------------------ | ----------------------------------- | ----------------------------------------------------------- | --------------------------------------------- |
| 1 | `database-engineer`       | access patterns                | schema + integrity guards + indexes | constraints/validators + unique index enforce identity; decimal money; UTC time | revise design at stage 1                        |
| 2 | `database-engineer`       | schema delta                   | migration                           | **additive + safe** (nullable→backfill→constrain); one logical change; applies on Testcontainers | rewrite migration at stage 2                    |
| 3 | `implementation-engineer` | schema + migration             | repository/adapter code             | adapter stays out of the domain; ports respected            | loop to stage 3                                 |
| 4 | `unit-test-engineer` / integration | adapter code          | integration tests (real DB)         | tests green on a **real** DB (Testcontainers), not in-memory | loop to stage 3/4                               |
| 5 | `code-reviewer`           | diff + migration               | findings                            | no `blocker`; hot query has an index (verified via EXPLAIN) | loop to the owning stage                         |
| 6 | `technical-writer`        | schema + contract deltas       | doc update (`docs/contracts/`, README) | schema change documented                                  | loop to stage 6                                 |

## Gate: destructive migrations

A migration that drops/renames/truncates requires a backup step and
explicit confirmation (`policies/05-security-and-secrets.md`) before
stage 2 advances.

## Output

```
Change:      <table/collection>: <what>
Migration:   <file> (additive/backfill/constraint)
Indexes:     <index> for <hot query> (EXPLAIN verified)
Validation:  [ran] migration on Testcontainers; integration tests green
```
