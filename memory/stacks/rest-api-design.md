# Stack — REST / HTTP API design

Conventions for any HTTP/REST surface, independent of framework. For the
correctness of async handlers see
`policies/03-async-and-messaging.md`; for contracts and versioning see
`rules/04-idempotency-and-event-contracts.md`.

## Resource & URL design

- **Nouns, not verbs**, in plural: `/orders`, `/orders/{id}`,
  `/orders/{id}/items`. Actions that don't fit CRUD use a sub-resource
  or a documented POST verb (`/orders/{id}/cancel`).
- Lowercase, hyphenated path segments; `snake_case` or `camelCase` JSON
  fields — pick one and keep it consistent repo-wide.
- Filtering, sorting, pagination via query params
  (`?status=open&sort=-created_at&limit=50&cursor=…`). Prefer **cursor
  (keyset) pagination** over offset for large collections.

## Methods & status codes

- `GET` (safe, cacheable), `POST` (create/action), `PUT` (full replace),
  `PATCH` (partial), `DELETE` (remove). `GET`/`PUT`/`DELETE` are
  idempotent; `POST` is not (see idempotency keys below).
- Use accurate status codes: `200/201/204`, `400/401/403/404/409/422`,
  `429`, `500/503`. Do not return `200` with an error body.
- **Errors follow RFC 9457** (`application/problem+json`): `type`,
  `title`, `status`, `detail`, `instance`. One consistent error shape
  across the API.

## Contracts & versioning

- **OpenAPI is the source of truth** for the surface; keep it under
  `docs/contracts/` and generate/validate it in CI.
- Version the API (`/v1/...` or a header). Additive changes are
  backward-compatible; breaking changes bump the version.
- Validate every request body at the boundary; never trust client input.

## Reliability & safety

- **Idempotency:** unsafe non-idempotent writes accept an
  `Idempotency-Key` header; store the first response and replay it on
  retry.
- **Pagination, rate limiting, and timeouts** on every collection and
  outbound call. Advertise limits via `429` + `Retry-After`.
- **Auth** on every non-public route (OAuth2/JWT/session); enforce
  authorization per resource, not just authentication.
- **CORS, security headers, and payload size limits** configured
  centrally.
- Correlation id (`X-Request-Id` / `traceparent`) accepted and
  propagated; returned in responses and logs.

## Observability

- Structured request logs with method, route template (not raw path),
  status, latency, correlation id — never log bodies with secrets/PII.
- Health (`/health`, `/ready`) and metrics endpoints.

## Forbidden patterns

- Verbs in resource URLs for standard CRUD.
- `200 OK` wrapping an error.
- Inconsistent error shapes across endpoints.
- Offset pagination on large hot collections.
- Non-idempotent write endpoints with no idempotency strategy.
- Trusting request input without validation at the boundary.
- Breaking a published contract without a version bump.
