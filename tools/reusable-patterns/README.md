# Reusable Patterns

This directory holds generator scripts that are more reusable than one-off scripts, but are not yet formalized as skill-local scripts.

Use this area for scripts that:

- demonstrate a reusable output pattern
- are still tied to a specific business case or data shape
- should remain available as reference implementations for future refactoring

Promote a script from here into `skills/<skill>/scripts/` when:

- the inputs are parameterized
- the workflow is broadly reusable
- the script is clearly owned by a single skill

Directory intent:

- `tools/one-off/`: artifact-specific utilities with low reuse
- `tools/reusable-patterns/`: scripts with reusable patterns that may later become skill automation
