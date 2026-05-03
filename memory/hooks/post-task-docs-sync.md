# Post task docs sync

## Purpose

When implementation changes likely affect docs, generate a prompt-side reminder to update README, ADRs, runbooks, or diagrams.

## Trigger

- Stop / task completion,
- or after edit batches.

## Responsibilities

- inspect git diff,
- detect doc-impacting changes,
- emit precise follow-up guidance.
