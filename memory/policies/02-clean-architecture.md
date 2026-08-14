# 02 — Clean / hexagonal architecture policy

## Purpose

Define the layer boundaries every module in this repository must respect.
This file is non-negotiable and stack-agnostic. Concrete package/module
naming for a given stack lives in the matching `stacks/*.md` profile;
implementation workflow lives in `skills/feature-implementation`.

## Layer responsibilities

| Layer                              | Owns                                                                       | Must not                                                                 |
| ---------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `domain` (core)                    | Entities, value objects, aggregates, domain services, **ports**, events    | Import framework, persistence, HTTP, messaging, or cloud SDKs            |
| `application` (use cases)          | Use-case orchestration; calls domain and ports                             | Import concrete adapters, framework infrastructure, transport DTOs       |
| `entry-points` (inbound adapters)  | HTTP routers/handlers, message consumers, schedulers, CLI, GraphQL         | Contain business rules; manipulate domain entities directly             |
| `driven-adapters` (outbound)       | Persistence, brokers, external APIs, producers, cache clients              | Be referenced from domain or use cases (only ports are referenced)      |
| `app` (composition root)           | Wiring, configuration, profiles, dependency injection setup               | Hold business logic                                                      |

The names are conceptual. Each stack profile maps them to real folders:
e.g. Java uses `domain/`, `usecase/`, `infrastructure/entry-points/*`,
`infrastructure/driven-adapters/*`, `applications/app-service/`; a Python
FastAPI service uses `domain/`, `application/`, `api/` (routers),
`adapters/`, and `main.py` / `container.py` as the composition root.

## Direction of dependencies

```
domain  <----  application  <----  entry-points
                   ^
                   |
             driven-adapters (implement domain ports)
                   ^
                   |
             app / composition root (wires everything)
```

- `domain` depends on **nothing** outside the language standard library
  and the project's own domain types.
- `application` depends on `domain` (and on ports declared in `domain`).
- `entry-points` depend on `application`. They translate transport into
  use-case input.
- `driven-adapters` depend on `domain` (to implement ports). They do
  **not** depend on `application`.
- The composition root is the only place allowed to depend on everything
  for wiring purposes.

## Concrete rules

- A new unit belongs in the layer that matches its **reason to change**.
  An HTTP DTO changes when the API contract changes → `entry-points`.
  A persistence row model changes when the storage schema changes →
  `driven-adapters`. A business invariant changes → `domain`.
- **Transactions** belong to use-case orchestration, not to domain
  entities. The transaction boundary equals the use case.
- **Mappers / serializers** live at the translation boundary.
  Inbound mappers go in `entry-points`; outbound mappers go in
  `driven-adapters`. Never put a mapper in `domain`.
- Shared utilities are allowed only for **truly cross-cutting** concerns
  (clock, ids, JSON helpers). Default to local helpers.
- Dependency injection happens at the composition root. Use cases and
  adapters are constructor/parameter-injected; they do not self-register.

## Review questions before merging

- Is the new unit in the correct layer?
- Is infrastructure leaking inward (framework, DB driver, HTTP, broker)?
- Is the mapper located on the boundary?
- Are ports defined in `domain` and implemented in `driven-adapters`?
- Is the proposed change smaller than a broad refactor? If not, can the
  refactor be split?

## Common violations to flag

- A framework annotation (`@Service`, `@Component`, FastAPI `Depends`,
  ORM decorator) inside `domain`.
- A serialization annotation on a domain entity.
- A use case importing a concrete adapter instead of a port.
- A scheduler or HTTP handler holding business state across calls.
- A repository implementation referencing use-case types.
