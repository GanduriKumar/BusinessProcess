# One-Off Generators

This directory holds artifact-specific generator scripts that are not yet generalized enough to live under a skill.

Use these when:

- the script is tied to one topic, customer, or deliverable
- the input and output structure is highly specific
- the script serves as an example or historical generator pattern

Promote a script into `skills/<skill>/scripts/` only after:

- hardcoded paths are removed or parameterized
- the script works across multiple similar tasks
- the expected inputs and outputs are clear

Repo convention:

- read business input files from `docs/input/` where practical
- write generated artifacts to `docs/output/`
