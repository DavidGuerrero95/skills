---
name: java-spring-implementation
description: Implement or refactor Java 21 + Spring services in this repository while respecting clean architecture, reactive constraints, validation, and project quality gates.
---


# Java Spring implementation

## When to use

Use this skill when creating or modifying:
- Spring controllers, handlers, routers, services, use cases
- Java domain or application classes
- DTOs, mappers, validators
- Gradle-backed Java modules in this repository

## Before coding

Read:
- `/memory/policies/01-engineering-baseline.md`
- `/memory/policies/02-clean-architecture.md`
- `/memory/policies/03-reactive-and-messaging.md`
- `/memory/rules/01-task-execution-flow.md`

## Workflow

1. Identify the impacted layer.
2. Preserve the current repository style unless the task is an explicit refactor.
3. Keep domain code framework-free.
4. Keep transport, persistence, and provider-specific logic at the edges.
5. Prefer constructor injection and explicit names.
6. Add or update targeted tests.
7. Validate compile + tests for the touched module.

## Output

Return:
- the change summary,
- the files touched,
- the validation run,
- any remaining risks.
