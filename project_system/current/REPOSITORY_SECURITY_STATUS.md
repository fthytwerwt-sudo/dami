# Repository Security Status

repository_visibility: `Public`
business_sensitive_git_write_blocked_while_repo_public: `true`

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
