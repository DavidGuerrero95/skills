# Stack — PostgreSQL

Conventions for using PostgreSQL as a relational store. Applies across
languages (JDBC/R2DBC, SQLAlchemy, node-postgres/Prisma, etc.).

## When to use

The repository stores relational data in PostgreSQL 14+ and cares about
integrity, migrations, and query performance.

## Schema design

- **Model for integrity first.** Use `NOT NULL`, `CHECK`, `UNIQUE`, and
  `FOREIGN KEY` constraints — the database is the last line of defense,
  not just the app.
- **Primary keys:** prefer `bigint GENERATED ALWAYS AS IDENTITY` or
  `uuid` (v7 for time-ordered). Do not expose sequential ids externally
  if enumeration is a concern.
- **Money and exact quantities:** `numeric(precision, scale)`. Never
  `float`/`double` for currency.
- **Timestamps:** `timestamptz` (UTC), never naive `timestamp`. Store
  `created_at` / `updated_at`.
- **Enums:** a lookup table with an FK, or a `CHECK`ed text column;
  native `enum` only when values are truly stable (altering them is
  painful).
- **Naming:** `snake_case`; plural table names or a consistent
  convention; explicit schema namespaces (`billing.invoice`).
- **Soft delete** only when audit requires it; otherwise delete rows.

## Migrations

- **Every schema change is a migration** (Flyway, Liquibase, Alembic, or
  the ORM's migration tool). Never mutate production schema by hand or
  via `ddl-auto`/auto-sync.
- Migrations are **forward-only and reversible-in-intent**: additive
  first (add column nullable → backfill → add constraint), so deploys
  don't require downtime.
- One logical change per migration; name with an ordered prefix and a
  slug. Commit them; never edit an already-applied migration.
- Test migrations against a disposable database in CI (Testcontainers).

## Access & querying

- **Parameterized queries always.** Never string-concatenate user input
  (SQL injection).
- **Transactions own the use case.** Keep them short; do not hold a
  transaction open across an external network call.
- Use the **right isolation level**; rely on `SELECT … FOR UPDATE` /
  advisory locks for concurrency-sensitive updates, not app-side
  read-modify-write races.
- **Indexing:** add indexes for the columns in `WHERE`, `JOIN`, and
  `ORDER BY` of hot queries; use partial and composite indexes
  deliberately. Verify with `EXPLAIN (ANALYZE, BUFFERS)`. Avoid
  redundant indexes — they cost writes.
- **Connection pooling:** bound the pool (HikariCP, asyncpg pool,
  PgBouncer). Size it to the DB's `max_connections`, not arbitrarily
  high.
- Prefer set-based SQL over N+1 loops; page large reads with keyset
  pagination, not large `OFFSET`.

## Operations

- Migrations run as a discrete, gated deploy step — not on app startup in
  production unless explicitly designed to.
- Back up before destructive migrations; `DROP`/`TRUNCATE` are guarded
  (`policies/05-security-and-secrets.md`).
- Integration tests use a real PostgreSQL via Testcontainers, not an
  in-memory substitute (H2/SQLite) — dialect differences hide bugs.

## Forbidden patterns

- `float`/`double` for money.
- String-concatenated SQL with user input.
- Auto-generating/altering production schema from the ORM at runtime.
- Editing an already-applied migration instead of adding a new one.
- Unbounded connection pools.
- `OFFSET`-based pagination on large tables in hot paths.
- Holding a DB transaction open across a remote call.
