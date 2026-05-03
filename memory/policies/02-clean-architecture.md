# Clean architecture policy

## Target boundaries

- `domain`: entities, value objects, aggregates, domain services, ports, domain events
- `application` / `usecases`: orchestration and application flow
- `entry-points`: HTTP, messaging, schedulers, listeners, CLI, transport concerns
- `driven-adapters`: persistence, external APIs, producers, infrastructure gateways
- `config`: framework wiring and cross-cutting configuration

## Rules

- Domain must not depend on Spring, persistence frameworks, HTTP, messaging SDKs, or cloud clients.
- Application depends on domain and ports, not concrete adapters.
- Entry points translate transport only and delegate to use cases.
- Driven adapters own provider-specific details and keep them local.
- Transactions belong in application/service orchestration, not domain models.
- Shared utilities are allowed only for truly cross-cutting concerns.

## Review questions

- Is a new class in the right layer?
- Is infrastructure leaking inward?
- Is a mapper located at the translation boundary?
- Is the proposed change smaller than a broad refactor?
