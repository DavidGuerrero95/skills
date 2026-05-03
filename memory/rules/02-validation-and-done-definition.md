# Validation and done definition

A task is done only when all applicable items are satisfied.

## Done means

- code is in the correct layer,
- no obvious architectural regression was introduced,
- touched modules compile,
- relevant tests run or the omission is explained,
- contract-impacting changes are documented,
- docs and diagrams are updated when needed,
- no secret or unsafe command was introduced,
- and the summary states the exact validation performed.

## Validation ladder

- Single-class pure logic: unit tests
- Adapter/persistence/messaging changes: integration tests
- Multi-service workflow changes: smoke or E2E
- Contract changes: docs + schema/topic review
