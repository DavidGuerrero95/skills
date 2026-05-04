# 02 — Clean architecture policy

## Purpose

Define the layer boundaries every service in this repository must
respect. This file is non-negotiable; specific implementation details
live in `skills/java-spring-implementation`.

## Layer responsibilities

| Layer                              | Owns                                                                       | Must not                                                                 |
| ---------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `domain/`                          | Entities, value objects, aggregates, domain services, **ports**, events    | Import Spring, persistence, HTTP, messaging SDKs, cloud clients          |
| `usecase/` (a.k.a. `application/`) | Use-case orchestration; calls domain and ports                             | Import concrete adapters, Spring infrastructure, transport DTOs          |
| `infrastructure/entry-points/*`    | HTTP routers/handlers, Kafka consumers, schedulers, listeners, CLI         | Contain business rules; manipulate domain entities directly              |
| `infrastructure/driven-adapters/*` | Persistence, brokers, external APIs, message producers, cache clients      | Be referenced from domain or use cases (only ports are referenced)       |
| `applications/app-service/`        | Spring `@Configuration`, wiring, profiles, `application.yaml`              | Hold business logic                                                      |

## Direction of dependencies

```
domain  <----  usecase  <----  entry-points
                  ^
                  |
            driven-adapters (implement domain ports)
                  ^
                  |
            applications/app-service (wires beans)
```

- `domain` depends on **nothing** outside the JDK and the project's own
  domain types.
- `usecase` depends on `domain` (and on ports declared in `domain`).
- `entry-points/*` depend on `usecase`. They translate transport into
  use-case input.
- `driven-adapters/*` depend on `domain` (to implement ports). They do
  **not** depend on `usecase`.
- `applications/app-service` is the only module allowed to depend on
  everything for wiring purposes.

## Concrete rules

- A new class belongs in the layer that matches its **reason to change**.
  An HTTP DTO changes when the API contract changes → `entry-points`.
  An event payload model changes when the topic contract changes →
  `domain` (it is a domain event) or a dedicated transport record in
  `entry-points`/`driven-adapters` if it is broker-specific framing.
- **Transactions** belong to use-case orchestration, not to domain
  entities. The transaction boundary equals the use case.
- **Mappers** live at the translation boundary. `entry-points` mappers
  go in `entry-points`. `driven-adapters` mappers go in
  `driven-adapters`. Never put a mapper in `domain`.
- Shared utilities are allowed only for **truly cross-cutting** concerns
  (clock, ids, JSON helpers). Default to local helpers.
- Dependency injection happens in `applications/app-service` via Spring
  configuration. Use cases and adapters are constructor-injected; they
  do not self-register.

## Review questions before merging

- Is the new class in the correct layer?
- Is infrastructure leaking inward (Spring, JDBC, Kafka, HTTP)?
- Is the mapper located on the boundary?
- Are ports defined in `domain` and implemented in `driven-adapters`?
- Is the proposed change smaller than a broad refactor? If not, can the
  refactor be split?

## Common violations to flag

- A `@Service` annotation inside `domain/`.
- A Jackson `@JsonProperty` on a domain entity.
- A use case importing from `infrastructure/driven-adapters/*`.
- A scheduler or HTTP handler holding business state across calls.
- A repository implementation referencing `usecase` types.
