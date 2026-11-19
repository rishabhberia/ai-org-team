# ai-org-team

A Claude Code skill that builds and runs an **AI organization**: one AI per department, each in its
own repo with its own charter, knowledge base and memory, coordinated by a **Management AI** that
acts as chief of staff.

```
                Organization AI team
                        │
                 Management AI   ← routing, orchestration, conflicts, the ledger
                        │
   ┌──────────┬─────────┼──────────┬────────────┐
 Sales AI   Legal AI  Finance AI  Operations AI  …
```

## How it works

- **Each department owns its domain.** It is the only source of truth for it, and the only AI
  accountable for its numbers.
- **AIs talk through sub-sessions.** When one AI needs information from another, or wants it to do
  something, it starts a Claude Code session in that department's folder. It watches that
  session, talks to it while it works, and records the request in a shared ledger. No AI reads
  another department's knowledge base to answer from it.
- **Every answer carries provenance:** source, as-of date, basis, confidence, and what is missing.
  Missing is never written as zero.
- **No AI approves anything.** Sending, writing to live systems, merging, deploying and spending
  stop with a named human principal.
- **Confidentiality walls** hold in every direction, including toward the Management AI. These
  cover pay, personal data, privileged legal material, client-confidential terms and credentials.
- **Conflicts are recorded, never averaged.** When two departments disagree, both positions go to
  the principal.

The reasoning behind each rule is in
[`skills/ai-org-team/reference/architecture.md`](skills/ai-org-team/reference/architecture.md).

## Requirements

- **The Claude desktop app (Code tab)**, or any Claude Code harness that can start a session in
  another folder and message a running session. The protocol is built on sub-sessions.
- `git` and `python3` (standard library only).

## Install

**As a plugin:**

```
/plugin marketplace add <owner>/ai-org-team
/plugin install ai-org-team@ai-org-team
```

**Or as a plain skill:** copy `skills/ai-org-team/` into `~/.claude/skills/`.

## Use

Ask Claude something like:

> Set up an AI team for my company with Sales, Legal, Finance and Operations.

**You design the structure.** The skill asks what your organization does, proposes departments
from a menu of common ones, and lets you add, drop, rename, merge, or split a department into
several AIs (for example two Sales AIs, one per business line). It shows you the org chart
(`scaffold.py --preview`) and changes it until you approve. Then it interviews you on each AI's
scope, restrictions, systems and the confidentiality walls, and generates:

| Repo | Contents |
|---|---|
| Management AI | `CLAUDE.md` charter; `knowledge/registry/` (department directory, capability matrix, systems map); `knowledge/protocol/` (interop protocol, data-sharing walls, escalation and authority); `knowledge/group/` (decision register, business context); `exchange/REGISTER.md` (the ledger); `logs/` |
| Each department | `CLAUDE.md` charter with the team section; `knowledge/interop/ai-team.md` (team map and how to ask); `knowledge/00-INDEX.md`; `open-items.md`; `logs/` |

Each AI's name, folder and knowledge-base folder are yours to choose. Existing projects can join
as departments. Their `CLAUDE.md` is never overwritten. The skill
writes a charter section for you to merge.

It also covers adding, changing and retiring a department, changing the protocol across all
departments, and a read-only health check (`scripts/check.py`).

### Optional modules

- **Principal's office**: the Management AI also supports the principal directly. It handles
  briefs, follow-ups and drafts (never sent), and keeps personal matters walled off.
- **PIAF** (Process Implementation & Assurance Framework): every new process or feature states its
  Promise, Proof and Protection, and production releases are checked against assurance gates.

## Try the scaffold without Claude

```bash
python3 skills/ai-org-team/scripts/scaffold.py skills/ai-org-team/examples/example-config.json --preview
```

## License

MIT
