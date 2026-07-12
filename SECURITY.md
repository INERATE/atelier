# Security Policy

Atelier runs inside your coding agent with access to your filesystem, so we take
supply-chain and hook safety seriously.

## Reporting a vulnerability

Please do **not** open a public issue for security problems. Email the maintainers
(see repository profile) or use GitHub's private vulnerability reporting. Include
reproduction steps and impact. You'll get an acknowledgment within 72 hours.

## Scope

- Hooks executing unintended commands or escaping their purpose
- The store MCP reading/writing outside the workspace
- Bootstrap installing unpinned or tampered third-party components
- Any path that could exfiltrate API keys collected at bootstrap

## Principles we hold ourselves to

- Hooks are deterministic, auditable, single-purpose scripts.
- Third-party skills/MCPs are version-pinned in the registry; `/atelier:doctor`
  verifies them.
- API keys are stored via the host runtime's mechanism, never in the SQLite store
  or git-tracked files.
