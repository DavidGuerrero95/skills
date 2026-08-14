# Stack — Docker & Docker Compose

Conventions for containerizing services and running local infrastructure
with Docker Compose.

## When to use

The repository is containerized and/or provides a Compose file to run
dependencies (databases, brokers, caches) and services locally.

## Image / Dockerfile

- **Multi-stage builds:** a build stage (compile/install deps) and a slim
  runtime stage. Copy only artifacts into the runtime image.
- **Pin base images** by minor tag or digest (`python:3.12-slim`,
  `eclipse-temurin:21-jre`, `node:20-alpine`). Never `latest`.
- **Run as non-root:** create and `USER` a dedicated app user.
- **Order layers for caching:** copy the dependency manifest and install
  before copying source, so code changes don't rebuild dependencies.
- Add a **`HEALTHCHECK`** and a `.dockerignore` (exclude `.git`,
  `node_modules`, build output, `.env`).
- Keep images small; no build tools or secrets in the final layer.

## docker-compose.yml

- One `compose.yaml` for local infra; version-pinned service images.
- **Named volumes** for stateful services (Postgres, Mongo) so data
  survives restarts; document how to reset.
- **Healthchecks + `depends_on: condition: service_healthy`** so
  services start after their dependencies are ready.
- **Config via env / `.env`** (never committed real secrets); provide a
  committed `.env.example`.
- Expose only the ports needed; use an internal network for
  service-to-service traffic.
- Provide a smoke script (`scripts/smoke.sh`) that brings the stack up
  and asserts the critical paths.

## Operations

- Local secrets live in `.env` (gitignored), seeded from `.env.example`.
- `docker system prune` / `volume prune` are destructive — guarded by
  `policies/05-security-and-secrets.md`.
- CI builds the image and runs it (or Testcontainers) to catch
  packaging bugs, not just unit tests.

## Forbidden patterns

- `latest` base tags.
- Running the container as root.
- Baking secrets or `.env` into the image.
- Single-stage images that ship build tools to production.
- Stateful services without named volumes when data must persist.
- `depends_on` without healthchecks (racey startup).
