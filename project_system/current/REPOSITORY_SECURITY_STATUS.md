# Repository Security Status

repository_visibility: `Public`
business_sensitive_git_write_blocked_while_repo_public: `true`

## Scope

Public repository safety applies to:

- all branches, including `main` and `codex/*`
- all Commit history
- all Tag references
- all PR content and review artifacts
- the complete Git history reachable from this repository

Branch isolation is not privacy isolation. `codex/*` branches are not private storage and must not contain sensitive business, personal, authentication, certification, testing, contract, pricing, cost, or customer/supplier material.

## Allowed

- Static collaboration rules.
- Non-sensitive project state metadata.
- Empty templates and redacted audit evidence.

## Blocked from Git

- Customer or supplier records.
- Quotations, costs, contracts, bank or payment information.
- Certification or testing originals.
- Personal information and authentication material.
- Local private sources and business plans pending authority review.

If a task needs any blocked material, stop with `blocked_repo_visibility_for_sensitive_data` and keep it in an authorized ignored local location.
