# Project Collaboration System v1

status: `active_in_repository`
project_id: `low_gi_rice_crossborder`
formal_system_version: `v1`

## Four layers

1. **Static rules**: root `AGENTS.md`, this index, mechanism registry, and `rules/`.
2. **Dynamic project truth**: `current/` for current state, formal facts, decisions, latest task status, and repository security.
3. **Task execution**: `templates/` plus task-specific requests, impact checks, validation, and completion reports.
4. **Evidence and history**: original evidence, `history/`, `audit/`, and the protected migration package.

## Canonical read chain

Use root `AGENTS.md` first, then the four current files, then task-relevant rules. `project_bootstrap/` is traceability evidence only. There is no second formal entry.

## Rule routing

- Roles and authority: `rules/01_ROLES_AND_AUTHORITY.md`
- Source truth and conflict: `rules/02_SOURCE_OF_TRUTH_AND_CONFLICT.md`
- Requirements and implementation design: `rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md`
- Task routing and state machine: `rules/04_TASK_ROUTING_AND_STATE_MACHINE.md`
- Safety and human gates: `rules/05_EXECUTION_SAFETY_AND_HUMAN_GATES.md`
- Completion truth and relay: `rules/06_COMPLETION_TRUTH_AND_RELAY.md`
- Research and experiments: `rules/07_RESEARCH_TO_ACTION_AND_EXPERIMENTS.md`
- Git and sync truth: `rules/08_GIT_AND_SYNC_TRUTH.md`
- Engineering budget and review: `rules/09_ENGINEERING_DEPTH_AND_COLLABORATION_EFFECTIVENESS.md`

## Activation scope

- 16 mechanisms: `ACTIVE_DIRECT`
- 8 mechanisms: `ACTIVE_ADAPTED`
- M19: `DEFERRED`
- M24-M26: `REJECTED_NOT_MIGRATED`

The registry is the formal mapping for all 28 mechanisms. Only task-relevant mechanisms run.

## Status boundary

The collaboration system is active in the repository. GPT Project upload remains a user action. Business facts, market, channel, offer, compliance, and execution do not advance merely because this system exists.
