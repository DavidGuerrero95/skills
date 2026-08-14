# Stack — Node.js + TypeScript

Concrete conventions for Node.js services written in TypeScript.
Universal invariants stay in `policies/`; this profile adds the specifics.

## When to use

The module is a Node.js 20+ service in TypeScript, typically NestJS
(opinionated, DI-friendly) or Express/Fastify (minimal).

## Toolchain

- **Language:** TypeScript in `strict` mode (`"strict": true`,
  `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`). No `any`
  without a written reason.
- **Runtime:** Node.js 20+ LTS. ES modules (`"type": "module"`).
- **Package manager:** pnpm (preferred) or npm; commit the lockfile.
  Versions centralized in root `package.json`; workspaces for monorepos.
- **Quality:** ESLint (`@typescript-eslint`) + Prettier; `tsc --noEmit`
  for type-check; Vitest or Jest for tests; `zod` for runtime validation
  at boundaries.
- **Config:** a typed config module that parses `process.env` once
  (e.g. with `zod`), with documented defaults — never scatter
  `process.env` reads.

## Project layout (hexagonal)

```
src/
├── domain/            # entities, value objects, ports (interfaces), events
├── application/       # use cases / services
├── api/               # controllers/routers, DTOs, validation schemas
├── adapters/          # repositories, http clients, brokers, cache
├── config/            # typed env config, logging, DI wiring
└── main.ts            # composition root / bootstrap
test/
```

Domain stays free of framework, ORM, and HTTP imports.

## Conventions

- **DI:** NestJS providers, or manual constructor injection in
  Express/Fastify. Inject interfaces (ports), not concrete adapters.
- **Validation at the edge** with `zod` / `class-validator`; map to
  domain types. Do not pass raw request bodies inward.
- **Errors:** a typed error hierarchy in the core; a single error
  middleware/filter maps them to HTTP responses (RFC 9457).
- **Async:** always `await` promises; never leave floating promises
  (`@typescript-eslint/no-floating-promises`). Bound concurrency with a
  pool/semaphore on hot paths.
- **Immutability:** `readonly` fields, `as const`, avoid mutating shared
  objects.

## Testing

- Vitest/Jest for unit; supertest / app injection for endpoint tests.
- Testcontainers for real DB/broker/cache in integration tests.
- Deterministic, no real network; factories over inline setup.
- Regression test for every bug fix, failing first.

## Validation commands

```bash
pnpm install
pnpm run lint          # eslint
pnpm run typecheck     # tsc --noEmit
pnpm test -- --coverage
pnpm run build
```

## Forbidden patterns

- `any` without justification; `@ts-ignore` instead of fixing types.
- Floating promises / unhandled rejections.
- `process.env` reads scattered across modules.
- Business logic inside controllers/routers.
- Framework/ORM types leaking into `domain/`.
- Committing without the lockfile updated.
