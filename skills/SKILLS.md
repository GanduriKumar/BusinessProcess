# Skills Catalog

Reusable capabilities live in subfolders under `skills/`.

## Standard Skill Layout

- `skills/<skill-name>/SKILL.md`: entry point for when and how to use the skill.
- `skills/<skill-name>/scripts/`: optional automation scripts.
- `skills/<skill-name>/templates/`: optional templates and snippets.
- `skills/<skill-name>/references/`: optional focused reference docs.
- `skills/<skill-name>/assets/`: optional examples or static files.

## How to Add a Skill

1. Copy `skills/_template` to `skills/<new-skill-name>`.
2. Update `SKILL.md` with trigger rules and workflow.
3. Add only the subfolders you actually need.
