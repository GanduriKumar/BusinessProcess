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
- `leadership-storyteller`: repo-level internal solution-storytelling lead; pairs with `skills/internal-leadership-storytelling`.
- `action-item-reviewer`: repo-level Teams transcript and meeting follow-up reviewer; pairs with `skills/action-item-extractor`.
- `design-to-code-lead`: repo-level design-to-code solution lead; pairs with `skills/design-to-code-solution`.
- `cua-testing-lead`: repo-level CUA testing solution lead; pairs with `skills/cua-testing`.
- `geo-optiflow-lead`: repo-level GEO / OptiFlow solution lead; pairs with `skills/geo-optiflow`.
- `model-eval-watcher`: repo-level AI model-evaluation and agent-evaluation watch lead; uses repo scripts under `tools/one-off`.
- `career-positioning-strategist`: repo-level personal positioning and offer-design lead; pairs with `skills/career-positioning`.
- `career-content-writer`: repo-level personal content-pack writer; pairs with `skills/career-content-writer`.
- `search-discovery-researcher`: repo-level research lead for AI-native search / answer-engine changes and content-strategy implications; pairs with `skills/ai-search-discovery-research`.

Each active agent now includes:

- `workflows/`: short execution playbooks for repeated tasks
- `templates/`: starter structures for common outputs
