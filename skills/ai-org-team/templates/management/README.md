# {{MGMT_NAME}}

The coordination layer for the **{{ORG}} AI team**: the AI that sits above the departmental AIs
and handles what crosses between them.

{{TEAM_TREE}}

Each departmental AI owns its own domain, its own knowledge base and its own systems. This repo
owns four things nobody else does:

| | |
|---|---|
| **The registry** | Who owns what — departments, capabilities, systems (`knowledge/registry/`) |
| **The protocol** | How one department asks another, and what an answer must carry (`knowledge/protocol/`) |
| **The ledger** | One row per cross-department sub-session, written by every department (`exchange/REGISTER.md`) |
| **The group view** | Cross-department risks and decisions (`knowledge/group/`, `knowledge/open-items.md`) |

## The idea

A department should never have to dig through another department's raw material. If Operations
needs a contract term, it asks Legal, which has already read the agreements and knows which are
executed. If Sales needs a client's outstanding, it asks Finance, and carries Finance's caveats
with the number.

Departments talk to each other **directly, through sub-sessions**: the asking AI starts a session
in the owning department's repo, watches it and talks to it until the work is done. The Management
AI is not in the middle of ordinary traffic. It comes in when work spans three or more
departments, when two departments disagree, when something needs prioritising, or when nobody
owns the question.

## Start here

- [`CLAUDE.md`](CLAUDE.md) — the Management AI's charter
- [`knowledge/registry/department-directory.md`](knowledge/registry/department-directory.md) — the authoritative directory
- [`knowledge/protocol/interop-protocol.md`](knowledge/protocol/interop-protocol.md) — the rulebook
- [`exchange/README.md`](exchange/README.md) — how a cross-department request is recorded

## Rules that matter most

1. The department that owns a domain is the **only** source of truth for it. No AI recomputes
   another's numbers.
2. Provenance crosses the boundary or the answer does not: source, as-of date, basis, confidence,
   and what is missing.
3. No AI in this team approves anything, writes to a live system, or sends a communication
   without {{PRINCIPAL}}'s approval for that action.
4. Conflicts between departments are recorded, never averaged.
