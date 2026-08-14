# Stack — MongoDB

Conventions for using MongoDB as a document store. Applies across
drivers (Spring Data Mongo, Motor/PyMongo, mongoose, official drivers).

## When to use

The repository stores document-shaped data in MongoDB 6+ where flexible
schema, denormalization, or high write throughput fit the domain better
than a relational model.

## Document modeling

- **Model around access patterns, not entities.** Design the document
  shape from the queries the application actually runs, not from a
  normalized ER diagram.
- **Embed vs. reference:**
  - *Embed* data that is read together and bounded in size
    (one-to-few, owned lifecycle).
  - *Reference* when data is large, shared, unbounded, or independently
    updated (one-to-many/many-to-many, high-churn).
- **Avoid unbounded arrays.** A field that grows without limit
  (event log, comments) belongs in its own collection with a reference,
  not an ever-growing embedded array (16 MB document cap).
- **Ids:** use `ObjectId` (time-ordered) unless a natural business key
  is stable and useful as `_id`.
- **Money/exact numbers:** `Decimal128`, never binary `double`.
- **Dates:** store UTC `Date`. Keep `createdAt` / `updatedAt`.

## Schema governance

- Apply **JSON Schema validation** (`$jsonSchema` validators) on
  collections even though Mongo is "schemaless" — it catches shape drift.
- Keep a **schema version field** (`schemaVersion`) on documents that
  evolve, and migrate lazily on read or via a batch job.
- Model changes are documented like any contract change
  (`policies/07-documentation-and-traceability.md`).

## Indexing & querying

- **Create indexes for every hot query**, including the sort key;
  follow the ESR rule (Equality, Sort, Range) for compound indexes.
- Add a **unique index** to enforce identity/idempotency constraints
  (e.g. `{ orderId: 1 }` unique) — the app-side check is not enough.
- Use **TTL indexes** for expiring data (sessions, dedupe memory,
  cooldowns) instead of manual cleanup.
- Verify plans with `explain("executionStats")`; watch for `COLLSCAN`
  on hot paths.
- Prefer projection to return only needed fields; paginate with a
  range/keyset filter, not large `skip`.
- Keep aggregation pipelines readable; push `$match`/`$project` early to
  reduce the working set.

## Consistency & operations

- **Transactions** exist (replica set / sharded) but are costly; prefer
  single-document atomicity and idempotent upserts where possible. Use
  multi-document transactions only when the invariant truly spans
  documents.
- Use `findOneAndUpdate` with upsert + `$setOnInsert` for idempotent
  writes; combine with a unique index.
- Choose an explicit **write concern** (`w: "majority"` for durable
  writes) and **read concern/preference** appropriate to the use case.
- Integration tests run against a real MongoDB (Testcontainers), not an
  in-memory fake.

## Forbidden patterns

- Binary `double` for money.
- Unbounded embedded arrays.
- Relying on app-side uniqueness checks without a unique index.
- `skip`-based pagination on large collections in hot paths.
- Collections with no indexes on their hot query fields.
- Storing schemaless documents with no validator and no `schemaVersion`
  when the shape evolves.
