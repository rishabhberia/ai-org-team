---
title: Decision register and open conflicts
updated: {{TODAY}}
sources:
  - Setup by the ai-org-team skill, {{TODAY}}
confidence: high
---
# Decision register

Two things live here: **decisions** taken across departments (so a department can find out why
something is the way it is), and **open conflicts** where two departments hold contradictory facts.

Nothing is deleted. A conflict is closed by the owning department establishing the fact — never by
averaging, by taking the newer file, or by quietly dropping one side.

## Decisions

| # | Date | Decision | Departments affected | Decided by | Recorded where |
|---|---|---|---|---|---|
| D1 | {{TODAY}} | {{ORG}} runs an AI team of {{DEPT_COUNT}} departmental AIs plus a Management AI. AIs ask each other for information and tasks through **sub-sessions** in the owning department's repo, recorded in a ledger. Departments talk directly; Management is not a checkpoint for ordinary two-department traffic | All | {{PRINCIPAL}} | [`../protocol/interop-protocol.md`](../protocol/interop-protocol.md) |
| D2 | {{TODAY}} | Routing is by **repo path**, not by display name | All | {{PRINCIPAL}} | [`../registry/department-directory.md`](../registry/department-directory.md) |
| D3 | {{TODAY}} | No AI holds approval authority. Orchestration lends none: a sub-session has exactly the authority of the department it works under | All | {{PRINCIPAL}} | [`../protocol/escalation-and-authority.md`](../protocol/escalation-and-authority.md) |
{{DECISIONS_OPTIONAL}}
## Open conflicts

| # | Raised | The conflict | Position A (dept · source · date) | Position B (dept · source · date) | Owner of the fact | Status |
|---|---|---|---|---|---|---|
| — | — | *None recorded yet.* | — | — | — | — |

**How to raise one:** both positions, both sources, both dates, and the department that owns the
domain the fact belongs to. Then a sub-session with that owner, and a line here. A conflict with
only one side written down is not a conflict, it is an assertion.
