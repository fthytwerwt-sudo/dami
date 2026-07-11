# Project System History

This directory stores append-only historical state, decisions, task reports, experiments, failures, and superseded rules when future tasks create them.

## Rules

- `current/` remains the canonical present-tense entry.
- History never overrides a current formal fact or decision.
- Superseded records remain readable and point to their replacement.
- Sensitive business evidence must not enter this Public repository.
- `project_bootstrap/collaboration_mechanism_migration/` is protected migration evidence and remains outside the runtime read chain.
