# Stack — Python + FastAPI

Concrete conventions for Python services built with FastAPI. Universal
invariants stay in `policies/`; this profile adds the Python specifics.

## When to use

The module is a Python 3.11+ HTTP service or async worker using FastAPI
(and typically Pydantic v2, SQLAlchemy / Motor, and an ASGI server).

## Toolchain

- **Language:** Python 3.11+ (prefer 3.12). Full type hints on every
  public function; `from __future__ import annotations` where helpful.
- **Framework:** FastAPI + Starlette. Async by default (`async def`
  endpoints and adapters). Pydantic **v2** for request/response models
  and settings.
- **Server:** `uvicorn` (dev) / `gunicorn -k uvicorn.workers` or
  `uvicorn` behind a process manager (prod).
- **Packaging & env:** `pyproject.toml` with **uv** (preferred) or
  Poetry. Commit the lockfile (`uv.lock` / `poetry.lock`). One virtual
  env per repo.
- **Quality:** `ruff` (lint + format), `mypy --strict` (or `pyright`),
  `pytest` + `pytest-asyncio` + `httpx.AsyncClient`, `coverage`.
- **Config:** `pydantic-settings` `BaseSettings` reading env vars with
  documented defaults — never `os.environ[...]` scattered in code.

## Project layout (hexagonal)

```
app/
├── domain/            # entities, value objects, ports (Protocol), events
├── application/       # use cases / services orchestrating domain + ports
├── api/               # FastAPI routers, request/response schemas, deps
│   ├── routers/
│   └── schemas/
├── adapters/          # db (repositories), http clients, brokers, cache
├── core/              # settings, logging, lifespan, DI container
└── main.py            # ASGI app factory; wires routers + adapters
tests/
```

Domain stays free of FastAPI, Pydantic, ORM, and HTTP imports — use
plain classes / dataclasses and `typing.Protocol` for ports.

## Conventions

- **Async all the way.** Never call blocking IO inside `async def`. For
  unavoidable blocking work use `await anyio.to_thread.run_sync(...)` or
  `run_in_executor`; document why.
- **Pydantic at the boundary only.** API schemas live in `api/schemas`;
  map them to/from domain types in the router or an application mapper.
  Keep ORM models out of the domain.
- **Dependency injection via FastAPI `Depends`** for request-scoped
  wiring; a small container/factory in `core/` for app-scoped
  singletons. Inject ports, not concrete adapters, into use cases.
- **Routers are thin.** Validate input, call a use case, map the result.
  No business logic in routers.
- **Errors:** raise domain exceptions in the core; translate to
  `HTTPException` / RFC 9457 `problem+json` in an exception handler
  registered on the app, not inline in each route.
- **Settings:** one `Settings(BaseSettings)` object, loaded once, passed
  via DI. Secrets come from env, documented in `.env.example`.
- **Migrations:** Alembic for SQL (see `stacks/postgresql.md`); never
  auto-create schema in production.
- **Logging:** structured (JSON) with a correlation id from middleware;
  never log secrets or full PII payloads.

## Testing

- `pytest` with `pytest-asyncio`; use `httpx.AsyncClient` +
  `ASGITransport` against the app for endpoint tests.
- Testcontainers (`testcontainers-python`) for real DB/broker/cache in
  integration tests — do not mock the driver protocol.
- Fixtures/factories (`factory_boy` or plain builders) instead of
  inline setup. Deterministic; no real network.
- Regression test for every bug fix, failing first.

## Validation commands

```bash
uv sync                       # or: poetry install
ruff check . && ruff format --check .
mypy app                      # or: pyright
pytest -q --cov=app --cov-report=term-missing
uvicorn app.main:app --reload # local smoke
```

## Forbidden patterns

- Blocking IO (sync `requests`, sync DB driver, `time.sleep`) inside
  `async def`.
- Pydantic models or ORM entities used as domain types.
- Business logic inside routers.
- `os.environ` reads scattered across modules instead of `Settings`.
- Bare `except:` / `except Exception: pass` that swallows errors.
- Mutable default arguments (`def f(x=[])`).
- Committing without the lockfile updated.
