# Formal Mechanism Registry v1

This registry activates the approved migration decisions. It is a routing index, not a requirement to run all mechanisms every task.

## Counts

- Total registered: 28
- `ACTIVE_DIRECT`: 16
- `ACTIVE_ADAPTED`: 8
- `DEFERRED`: 1
- `REJECTED_NOT_MIGRATED`: 3

The JSON registry is the field-complete machine-readable source for trigger, inputs, outputs, human gate, done criteria, blockers, validation, and review condition.

| ID | Name | Verdict | Activation | Canonical rule |
|---|---|---|---|---|
| M01 | ChatGPT/Codex/user authority separation | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/01_ROLES_AND_AUTHORITY.md` |
| M02 | Static rules/dynamic facts separation | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/02_SOURCE_OF_TRUTH_AND_CONFLICT.md` |
| M03 | Source authority/conflict | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/02_SOURCE_OF_TRUTH_AND_CONFLICT.md` |
| M04 | Cross-border task state routing | ADAPT | ACTIVE_ADAPTED | `rules/04_TASK_ROUTING_AND_STATE_MACHINE.md` |
| M05 | Six-layer requirement alignment | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md` |
| M06 | Ambiguous-goal clarification | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md` |
| M07 | Implementation design | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md` |
| M08 | Capability confirmation/probe separation | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md` |
| M09 | Primary/fallback/loss | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md` |
| M10 | Startup impact check | ADAPT | ACTIVE_ADAPTED | `rules/05_EXECUTION_SAFETY_AND_HUMAN_GATES.md` |
| M11 | Completion Relay | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/06_COMPLETION_TRUTH_AND_RELAY.md` |
| M12 | Completion truth | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/06_COMPLETION_TRUTH_AND_RELAY.md` |
| M13 | Four-state completion | ADAPT | ACTIVE_ADAPTED | `rules/06_COMPLETION_TRUTH_AND_RELAY.md` |
| M14 | Git decision/validation fields | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/08_GIT_AND_SYNC_TRUTH.md` |
| M15 | GPT Project sync truth | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/08_GIT_AND_SYNC_TRUTH.md` |
| M16 | Original-source readback | ADAPT | ACTIVE_ADAPTED | `rules/02_SOURCE_OF_TRUTH_AND_CONFLICT.md` |
| M17 | Dry-run and secret boundary | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/05_EXECUTION_SAFETY_AND_HUMAN_GATES.md` |
| M18 | Cross-border human/AI boundary | ADAPT | ACTIVE_ADAPTED | `rules/05_EXECUTION_SAFETY_AND_HUMAN_GATES.md` |
| M19 | L0-L3 engineering depth | DEFER | DEFERRED | `rules/09_ENGINEERING_DEPTH_AND_COLLABORATION_EFFECTIVENESS.md` |
| M20 | Execution budget | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/09_ENGINEERING_DEPTH_AND_COLLABORATION_EFFECTIVENESS.md` |
| M21 | Collaboration effectiveness | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/09_ENGINEERING_DEPTH_AND_COLLABORATION_EFFECTIVENESS.md` |
| M22 | Research Source-to-Action | ADAPT | ACTIVE_ADAPTED | `rules/07_RESEARCH_TO_ACTION_AND_EXPERIMENTS.md` |
| M23 | Single-primary-variable experiment | ADAPT | ACTIVE_ADAPTED | `rules/07_RESEARCH_TO_ACTION_AND_EXPERIMENTS.md` |
| M24 | Media-production workflows | DROP | REJECTED_NOT_MIGRATED | this registry |
| M25 | Fixed retrieval/external-AI dependency | DROP | REJECTED_NOT_MIGRATED | this registry |
| M26 | Legacy statuses, paths, conclusions | DROP | REJECTED_NOT_MIGRATED | this registry |
| M27 | Conditional Git closeout | ADAPT | ACTIVE_ADAPTED | `rules/08_GIT_AND_SYNC_TRUTH.md` |
| M28 | Latest/history separation | KEEP_DIRECTLY | ACTIVE_DIRECT | `rules/08_GIT_AND_SYNC_TRUTH.md` |

## Deferred condition

M19 does not run. Reconsider only after at least three comparable real tasks show repeated coordination cost, measurable automation value, and acceptable maintenance cost, followed by explicit user approval.

## Rejection boundary

M24-M26 are retained only as negative migration decisions. They must not enter runtime prompts, current facts, status names, required tools, or default paths.
