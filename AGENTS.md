# Low-GI Rice Cross-Border Project Instructions

project_id: `low_gi_rice_crossborder`
project_name: `大米低 GI 跨境`
repository: `fthytwerwt-sudo/dami`
formal_system_version: `v1`

This file is the only formal Codex entry for the project. Current stage and changing business facts are never stored here. Read the current stage from `project_system/current/CURRENT_PROJECT_STATE.md`.

## Mandatory startup order

1. User input for the current task.
2. Root `AGENTS.md`.
3. `project_system/current/CURRENT_PROJECT_STATE.md`.
4. `project_system/current/CURRENT_FORMAL_FACTS.md`.
5. `project_system/current/CURRENT_DECISIONS.md`.
6. `project_system/current/LATEST_TASK_STATUS.md`.
7. Rule files directly relevant to the task.
8. Original evidence directly relevant to the task.
9. `project_system/history/` and `project_bootstrap/` only for traceability.

If a mandatory entry is missing or unreadable, stop with `blocked_source_missing`. Candidate and history files never replace a missing current entry.

## Authority is three-dimensional

- `business_decision_authority`: The user decides whether to pursue a market, channel, offer, budget, external communication, contract, sample, or scale decision.
- `objective_fact_evidence_authority`: Current original regulatory, testing, certification, contract, platform, and other primary evidence determines what is objectively true. A business preference cannot rewrite evidence.
- `execution_authority`: ChatGPT frames and routes work; Codex may write or act only inside an authorized task scope. Neither may make an unapproved business commitment.

User input may temporarily change the current action. A durable change to project state, facts, or decisions must be written back to the canonical current files with evidence.

## Task pipeline

Complex, modifying, research, compliance, direction, automation, or external-action tasks use:

`task_classification -> requirement_alignment -> implementation_design -> impact_check -> source_of_truth_check -> human_gate_check -> execution -> validation -> completion_truth -> status_update -> Git closeout when authorized`

Only mechanisms relevant to the task are triggered; the registry is an index, not a requirement to run all mechanisms every turn.

## Codex task contract

Every executable task must define:

- Goal
- Context
- Source of truth
- Constraints
- Implementation design
- Impact check
- Allowed files
- Forbidden files
- External actions
- Human gates
- Execution steps
- Validation
- Rollback
- Done when
- Blocked if
- Output

## Write and permission boundaries

- Modify only task-authorized paths; never absorb unrelated dirty or untracked files.
- Never read, print, or commit secrets or authentication material.
- Never treat candidate research, plans, summaries, or search snippets as formal facts.
- Never present machine, repository, or technical validation as human, compliance, legal, commercial, or external-system approval.
- Never perform unapproved customer contact, publishing, advertising, payment, contract, sample, deletion, or account action.
- `business_sensitive_git_write_blocked_while_repo_public: true`.
- While the repository is Public, customer, supplier, quotation, cost, contract, certification original, test original, personal, and other business-sensitive data must remain outside Git.
- An ignored local private-source registry may be read only when authorized. Content marked `pending_authority_review` cannot enter formal facts.

## Git rules

Formal mechanism, fact, state, and decision changes require task authorization, path-limited staging, commit, push, and remote readback. Never use broad staging for a mixed worktree. Git synchronization is complete only when local `HEAD`, `origin/main`, and `ls-remote main` match and the remote files are readable.

Commit decisions use plain-language fields when relevant:

`Goal / Constraint / Rejected / Confidence / Scope-risk / Directive / Tested / Not-tested`

Read-only research and drafts do not require a commit unless the task explicitly requests one.

## Completion truth

Supported result states:

- `completed_verified`: all authorized deliverables and validation passed.
- `completed_pending_human_review`: machine-verifiable work passed, but a required human decision remains.
- `partial_completed`: only when the task allows a partial result and remaining work is explicit.
- `blocked`: a specific blocker prevents safe completion.

Every report states which statuses were promoted and which were not. Use specific blockers:

- `blocked_source_missing`
- `blocked_fact_conflict`
- `blocked_authorization_required`
- `blocked_compliance_evidence_missing`
- `blocked_capability_unverified`
- `blocked_write_scope_violation`
- `blocked_secret_access_required`
- `blocked_repo_visibility_for_sensitive_data`
- `blocked_remote_readback_failed`

## Canonical references

- System index: `project_system/00_PROJECT_SYSTEM_INDEX.md`
- Mechanism registry: `project_system/01_MECHANISM_REGISTRY.md` and `.json`
- Current truth: `project_system/current/`
- Formal rules: `project_system/rules/`
- Task templates: `project_system/templates/`
- History: `project_system/history/`
- GPT package: `gpt_project_sync/latest/`

The migration package remains historical evidence and is not a formal runtime entry.
