# Session end orphan check

## Purpose

Best-effort detection of lingering local agent/tool processes so the operator can clean up explicit long-running work.

## Trigger

- Stop or SessionEnd

## Important note

This is only a best-effort local hygiene check. It is not a guaranteed token-leak prevention mechanism.
