# Stack profiles

Stack profiles hold the **language-, framework-, and datastore-specific**
conventions that stack-agnostic `policies/` and `rules/` deliberately
leave out. Activate only the profiles the repository actually uses; the
others stay as reference for future work.

A stack profile answers: *"When working in this technology, what are the
concrete conventions, tools, commands, and forbidden patterns?"* It never
restates the universal invariants in `policies/` — it links to them and
adds the specifics.

## Available profiles

| Profile                     | Use when the repo uses…                       |
| --------------------------- | --------------------------------------------- |
| `java-spring.md`            | Java 21+ and Spring Boot (WebFlux or MVC)     |
| `python-fastapi.md`         | Python 3.11+ and FastAPI                      |
| `node-typescript.md`        | Node.js and TypeScript (NestJS / Express)     |
| `postgresql.md`             | PostgreSQL as a relational store              |
| `mongodb.md`                | MongoDB as a document store                   |
| `redis.md`                  | Redis / Valkey for cache, locks, rate limits  |
| `messaging-kafka.md`        | Apache Kafka (or a compatible broker)         |
| `rest-api-design.md`        | Any HTTP/REST API surface                     |
| `docker-compose.md`         | Docker + Docker Compose for local infra       |

## How profiles relate to policies

- **Invariants** (no blocking on async runtimes, layer purity, coverage
  gate) → `policies/`.
- **Execution flow** (inspect → change → validate → summarize) →
  `rules/`.
- **Concrete syntax, tools, commands, idioms** → `stacks/` (this folder).

## Adding a new profile

1. Confirm no existing profile already owns the technology.
2. Create `stacks/<slug>.md` with: when to use, toolchain, project
   layout, conventions, testing, validation commands, forbidden
   patterns.
3. Add a row to the table above and to `memory/MANIFEST.md`.
4. Link it from `policies/01-engineering-baseline.md` if it is a primary
   language/framework.
