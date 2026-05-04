# /refactor-module

Run a bounded, behavior-preserving refactor on a single module. Use
when the change is too large for `/audit-code-smells` but smaller
than a redesign.

## When to use

- Repeated duplication across two or more files in the module.
- A class with mixed responsibilities that needs to split.
- Long methods that obscure intent.
- A boundary violation contained inside one module.

## When NOT to use

- A redesign that crosses modules — open an ADR first.
- A bug fix — `/root-cause-analysis`.
- A simple cleanup pass — `/audit-code-smells`.

## Steps

1. **Bound the scope** to a single module. State entry/exit invariants
   in writing.
2. **Capture the behavior** with characterization tests if missing.
3. **Plan the smallest sequence** of behavior-preserving steps:
   rename → extract → move → inline.
4. **Apply each step** as its own commit. Run the module's tests
   between steps.
5. **Update neighbors** only when truly required.
6. **Document the outcome** if the change is significant
   (`docs/wiki/architecture-overview.md`, an ADR if the placement
   choice was deliberate).

## Recommended delegates

- `java-architect` (placement decisions)
- `code-smell-auditor` (cleanup pass after structural moves)
- `unit-test-engineer` (characterization tests)
- `code-reviewer` (independent pass before merge)
