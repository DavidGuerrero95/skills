# Post edit code quality

## Purpose

After file edits, remind the main agent to run the smallest relevant validation and optionally trigger targeted review logic.

## Trigger

- After `Edit`, `Write`, or patch-based file changes.

## Responsibilities

- inspect changed file types,
- hint the next validation step,
- optionally run a lightweight smell/test command if configured.
