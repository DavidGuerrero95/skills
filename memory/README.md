# Memory source of truth

This directory is the canonical, reviewable, version-controlled source for agent behavior in this repository.

## Core principles

1. **Single responsibility**  
   Every instruction belongs in exactly one canonical place.

2. **Canonical over duplicated**  
   Runtime folders should reference or adapt memory content, not become independent sources of truth.

3. **Stable defaults, task-specific expansion**  
   Put invariants in `policies/`, execution flow in `rules/`, repeatable workflows in `skills/`, and specialized role behavior in `agents/`.

4. **Least surprise**  
   Hooks may automate validation and reminders, but they must not hide major behavior changes from the user.

5. **Token discipline**  
   Keep high-level guidance short. Move large procedures into skills. Use hooks and subagents selectively.

## Folder contract

- `policies/`: non-negotiable constraints
- `rules/`: project operating mode
- `skills/`: reusable workflows
- `agents/`: specialized delegates
- `hooks/`: lifecycle automation contracts
- `commands/`: explicit entrypoints
- `output-styles/`: communication layer only

## Precedence

1. Applicable runtime safety / platform rules
2. `memory/policies/*`
3. `memory/rules/*`
4. Active skill or agent instructions
5. Active output style
6. Ad hoc task prompt
