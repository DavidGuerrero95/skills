---
name: implementation-bug-hunter
description: Investigate failing behavior, trace root cause, propose the smallest safe fix, and add regression validation.
---


# Implementation bug hunter

## Use for

- production-like defects
- failing tests
- wrong event mapping
- broken contracts
- scheduler/reconciliation bugs
- subtle reactive behavior issues

## Workflow

1. Reproduce or restate the failure clearly.
2. Narrow the failing boundary.
3. Identify the smallest plausible root cause.
4. Fix with minimal blast radius.
5. Add regression coverage.
6. Summarize cause, fix, and validation.

## Read first

- `/memory/rules/01-task-execution-flow.md`
- `/memory/policies/04-testing-and-quality-gates.md`
- `/memory/policies/03-reactive-and-messaging.md`
