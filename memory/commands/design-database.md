# /design-database

Design or change database schema, migrations, and indexes for PostgreSQL
or MongoDB with integrity, performance, and safe-migration discipline.

**Pipeline:** `memory/pipelines/database-change.md` (ordered stages +
gates).

## When to use

- Adding or changing a table / collection, column / field, or constraint.
- Writing or reviewing a migration.
- Adding or revising an index, or optimizing a hot query.

## When NOT to use

- Pure application logic with no schema/index impact — `/implement-feature`.
- Cache/lock design in Redis/Valkey — see `stacks/redis.md`.

## Steps

1. Start from access patterns (queries/writes, frequency, latency
   budget).
2. Design for integrity — read `stacks/postgresql.md` and/or
   `stacks/mongodb.md`.
3. Add the unique constraint/index that enforces identity and
   idempotency (`rules/04-idempotency-and-event-contracts.md`).
4. Plan the migration as additive + safe (nullable → backfill →
   constrain); one logical change per migration.
5. Index deliberately; verify with `EXPLAIN` / `explain()`.
6. Validate the migration and hot queries against a real DB
   (Testcontainers).

## Recommended delegates

- `database-engineer` (lead)
- `implementation-engineer` for the repository/adapter code
- `code-reviewer` for an independent pass before merge
