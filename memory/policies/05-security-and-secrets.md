# Security and secrets policy

## Non-negotiable rules

- Never hardcode secrets, tokens, credentials, or private keys.
- Use existing environment-variable patterns and `.env.example` references.
- Prefer safe, minimal dependency changes.
- Avoid introducing unreviewed network calls or external services casually.
- Validate shell commands before execution if they are destructive or broad.

## Destructive command guardrails

Require extra scrutiny for:
- `rm -rf`
- `git push --force`
- `docker system prune`
- dropping databases or topics
- wildcard delete operations
- bulk permission changes

## Supply-chain rules

- Prefer official sources and pinned versions where appropriate.
- Keep dependency version ownership centralized.
- Document why a new dependency exists.
