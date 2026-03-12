# Agents

This folder contains agent definitions.

## Standard Layout

- `agents/<agent-name>/AGENT.md`: role, scope, constraints, and trigger conditions.
- `agents/<agent-name>/PROMPT.md`: optional prompt template.
- `agents/<agent-name>/workflows/`: optional execution playbooks.
- `agents/<agent-name>/templates/`: optional output templates.
- `agents/<agent-name>/examples/`: optional sample I/O.
- `agents/<agent-name>/config/`: optional runtime/tool config.

## Quick Start

1. Copy `agents/_template` to `agents/<new-agent-name>`.
2. Update `AGENT.md` for behavior and boundaries.
3. Add only subfolders you need.

## Repo Agents

- `proposal-manager`: repo-level proposal and RFP response lead; pairs with `skills/rfp-response`.
- `deck-strategist`: repo-level executive deck and PPTX lead; pairs with `skills/slide-deck-creation`.
- `finance-reviewer`: repo-level finance and business-case reviewer; pairs with `skills/business-financial-analysis`.
- `ops-reviewer`: repo-level operational analysis and delivery-review agent; pairs with `skills/operational-data-analysis`.

Each active agent now includes:

- `workflows/`: short execution playbooks for repeated tasks
- `templates/`: starter structures for common outputs
