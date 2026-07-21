# Latest Task Status

task: `single_repository_and_branch_governance_activation`
task_identity: `single_repository_and_branch_governance`
status: `governance_activation_recorded_pending_git_closeout`
target_repository: `fthytwerwt-sudo/dami`
target_branch: `main`
starting_main_sha: `95bb18bbdd34742dac3138508274e448d4713671`
execution_lane: `serial_only`
write_owner: `single_integrator`
integration_owner: `single_integrator`
single_repository_policy_active: `true`
multi_branch_governance_active: `true`
branch_aware_git_closeout_active: `true`
tool_branch_migration_approved: `false`
repository_visibility_change_approved: `false`
gpt_project_package_revision: `v2_20260712_r1`
gpt_project_synced: `false`
ui_uploaded: `false`
business_execution_started: `false`

## System deliverables

- Root `AGENTS.md` records the P0 single-repository and multi-branch governance rule.
- `main` is the formal branch for rules, decisions, current status, approved stable code, and approved formal deliverables.
- New `codex/*` task branches must start from current `origin/main` and must not be orphan branches.
- Existing `codex/dami-web-agent-toolkit` is a historical exception only; it is not approved for merge, rewrite, or use as a future branch template.
- Public repository safety applies to all branches, commits, tags, PRs, and full Git history.
- Branch push, PR created, PR merged, and `main` effective remain separate status claims.

## Status boundaries

- This task updates repository governance only.
- This task does not merge or modify the existing tool branch.
- GPT package generation is not ChatGPT Project UI upload or synchronization.
- Business execution, market/channel/B2B-B2C decisions, pricing, compliance approval and external actions remain unstarted or unapproved.
- This file cannot pre-record its own final commit SHA; final Git SHA evidence must come from the completion report after commit, push, fetch, three-way SHA verification, and remote readback.

## Next safe action

Finish this task only after precise staging, `git diff --cached --check`, staged secret and sensitive scans, commit, normal push to `origin/main`, fetch, three-way SHA match, and remote readback for `AGENTS.md` plus current files. After that, the next safe project task remains a read-only product fact gap inventory or a separate formal migration task for historical tool-branch contents.
