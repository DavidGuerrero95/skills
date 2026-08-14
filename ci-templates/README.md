# CI templates

Ready-to-copy GitHub Actions workflows for projects that adopt this
agentic baseline. They mirror the quality gates in
`memory/policies/04-testing-and-quality-gates.md` and the validation
commands in each `memory/stacks/*.md` profile.

## How to use

1. Copy the workflow(s) for your stack into `.github/workflows/`.
2. Adjust paths, module names, and the coverage threshold.
3. Keep `.github/workflows/ci.yml` (baseline validation + hook smoke) as
   well — it protects the agentic scaffold itself.

| Template                 | Stack                          | Gates                                            |
| ------------------------ | ------------------------------ | ------------------------------------------------ |
| `python-fastapi.yml`     | Python + FastAPI               | ruff, mypy, pytest + coverage                    |
| `java-spring.yml`        | Java + Spring Boot (Gradle)    | spotless, test, jacoco coverage verification     |
| `node-typescript.yml`    | Node + TypeScript              | eslint, tsc, test + coverage                     |
| `docker-build.yml`       | Any containerized service      | build image, trivy scan                          |

All templates pin action versions, use least-privilege `permissions`, and
run on `push` + `pull_request`.
