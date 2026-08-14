---
name: database-design
description: Design or change database schema, migrations, indexes, and data-access patterns for PostgreSQL and MongoDB with integrity, performance, and safe migration discipline. Use whenever a schema/collection, migration, index, or hot query is added or changed.
license: MIT
metadata:
  scope: database-schema-migrations
  version: "1.0"
---

# Database design

## When to use

- Adding or changing a table / collection, column / field, or constraint.
- Writing a migration.
- Adding or revising an index.
- Diagnosing or optimizing a hot query.

## When NOT to use

- Pure application logic with no schema/index impact
  (`skills/feature-implementation`).
- Cache/lock design in Redis/Valkey (`stacks/redis.md`).

## Read first

- `memory/stacks/postgresql.md` (relational) and/or
  `memory/stacks/mongodb.md` (document) — the concrete rules.
- `memory/policies/02-clean-architecture.md` (persistence is an
  outbound adapter; keep it off the domain).
- `memory/policies/05-security-and-secrets.md` (destructive-migration
  guardrails).

## Workflow

1. **Start from access patterns.** List the queries/writes the
   application actually runs, their frequency, and their latency budget.
   Model the schema to serve them (especially for MongoDB).

2. **Design for integrity.**
   - Relational: `NOT NULL`, `CHECK`, `UNIQUE`, `FOREIGN KEY`;
     `numeric` for money; `timestamptz` UTC.
   - Document: `$jsonSchema` validators; `Decimal128` for money; bounded
     documents; a `schemaVersion` when the shape evolves.

3. **Choose keys and idempotency guards.**
   - Add the **unique index/constraint** that enforces identity and
     idempotency (`rules/04-idempotency-and-event-contracts.md`), not
     just an app-side check.

4. **Plan the migration as additive + safe.**
   - Add nullable → backfill → enforce constraint, so deploys avoid
     downtime.
   - One logical change per migration; ordered name; never edit an
     applied migration.
   - Guard destructive steps; back up first.

5. **Index deliberately.**
   - Add indexes for `WHERE`/`JOIN`/`ORDER BY` (SQL) or ESR-ordered
     compound indexes (Mongo). Verify with `EXPLAIN` /
     `explain("executionStats")`. Remove redundant indexes.

6. **Validate.**
   - Run the migration against a disposable database (Testcontainers) in
     a test.
   - Add/adjust integration tests using a **real** database, not an
     in-memory substitute.

## Output expected from this skill

```
Change:
 - <table/collection>: <what changed>

Access patterns served:
 - <query> -> <index used>

Integrity guards:
 - <constraints / validators / unique indexes>

Migration:
 - <file>  (additive? backfill? constraint step?)

Validation:
 - [ran]  migration applied on Testcontainers
 - [ran]  EXPLAIN / explain() reviewed for hot query
 - [ran]  <integration test command>
```

## Forbidden patterns

- Binary float for money (SQL `float`, Mongo `double`).
- Auto-generating/altering production schema at runtime.
- Editing an already-applied migration instead of adding a new one.
- App-side uniqueness without a DB unique index/constraint.
- Offset/`skip` pagination on large hot collections.
- Testing schema on an in-memory DB that differs from production.
