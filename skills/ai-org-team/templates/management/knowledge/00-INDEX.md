---
title: Index — {{MGMT_NAME}} knowledge base
updated: {{TODAY}}
sources: []
confidence: high
---
# Index

Read this first, then [`../exchange/REGISTER.md`](../exchange/REGISTER.md), then
[`open-items.md`](open-items.md), then the last entries in
[`../logs/management-log.md`](../logs/management-log.md).

## Scope

The **organization layer only**: who owns what, how departments talk to each other, what crosses
departments, and what has been decided. No departmental data lives here. It lives in the
departmental repos and is obtained from them, through sub-sessions, with attribution.

## The registry — who owns what

| File | What it gives you |
|---|---|
| [registry/department-directory.md](registry/department-directory.md) | **Authoritative.** Every department: repo path, KB root, what to ask it, what not to, what is restricted |
| [registry/capability-matrix.md](registry/capability-matrix.md) | Question → department. Start here when routing |
| [registry/systems-map.md](registry/systems-map.md) | Which department owns which system, and the write rules |

## The protocol — how departments talk

| File | What it gives you |
|---|---|
| [protocol/interop-protocol.md](protocol/interop-protocol.md) | **The rulebook.** SESSION / ESCALATE, the session brief, monitoring, the ledger, the answer envelope, worked examples |
| [protocol/data-sharing-rules.md](protocol/data-sharing-rules.md) | The confidentiality walls and how they hold under orchestration |
| [protocol/escalation-and-authority.md](protocol/escalation-and-authority.md) | Who decides what; where approval stops; how conflicts are handled |

## The organization layer

| File | What it gives you |
|---|---|
| [group/business-context.md](group/business-context.md) | What the organization is, in one page, with pointers to the departments that own each part |
| [group/decision-register.md](group/decision-register.md) | Decisions taken across departments, and open conflicts between them |
| [open-items.md](open-items.md) | Organization-level risks and actions |
{{INDEX_OPTIONAL}}
## The ledger

[`../exchange/README.md`](../exchange/README.md) — the ledger of cross-department sessions. It
lives outside `knowledge/` because every department writes to it.

## Conventions

[CONVENTIONS.md](CONVENTIONS.md) — how every file here is written.
