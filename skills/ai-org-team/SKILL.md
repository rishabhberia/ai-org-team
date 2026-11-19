---
name: ai-org-team
description: Set up and run an AI organization in Claude Code — one AI per department (each its own repo, charter, knowledge base and memory) coordinated by a Management AI acting as chief of staff. AIs ask each other for information and give each other tasks through sub-sessions that the asker monitors, every answer carries provenance, confidentiality walls hold, and no AI holds approval authority. Use when someone wants to build an AI team for their company or department structure, add, change or retire a department AI, wire an existing project in as a department, or check the team's health.
---

# AI organization team

Builds and maintains a team of departmental AIs under a Management AI:

```
                Organization AI team
                        │
                 Management AI  ← routing, orchestration, conflicts, the ledger
                        │
   ┌──────────┬─────────┼──────────┬────────────┐
 Sales AI   Legal AI  Finance AI  Operations AI  …   ← each: own repo, CLAUDE.md, KB, memory
```

- **Every department owns its domain.** It is the only source of truth for it. No AI recomputes
  another department's numbers from raw sources.
- **AIs talk through sub-sessions.** To get information from another AI, or give it a task, an AI
  starts a session in that department's folder, watches it, follows up in it, and records it in a
  ledger. Nobody reads another department's knowledge base to answer from it.
- **Provenance crosses the boundary or the answer does not:** source, as-of date, basis,
  confidence, and what is missing. Missing is never zero.
- **No AI approves anything.** Sends, live-system writes, merges, deploys and spend stop with the
  human principal.
- **Confidentiality walls** (pay, personal data, privileged legal material, client-confidential
  terms, credentials) hold in every direction, including towards Management.

Read [reference/architecture.md](reference/architecture.md) for the full model and why each rule
exists.

## Requirements

- **The Claude desktop app (Code tab)**, or another harness that can start a Claude Code session in
  another folder and send messages to a running session. The protocol depends on this; say so
  plainly if the user's environment cannot do it, and do not swap in a different channel unasked.
- `git`, and `python3` for the scripts (standard library only).
- One folder per department plus one for Management, all under a common root.

## Workflows

Pick the one that matches the request.

### A. Set up a new team

1. **Interview the user** with [reference/interview.md](reference/interview.md). Never invent a
   department's scope, its restricted material, a system's owner or the principal's name: ask.
   Offer the standard walls listed there as a starting point; the user confirms or edits them.
2. **Write the config** to a working file (format: [examples/example-config.json](examples/example-config.json)).
   Every department needs `slug`, `short`, `name`, `ai_name`, `dir`, `owns`, `ask_for`,
   `not_for`, `restricted`; `systems` and `matrix` are optional. Show the user the departments and
   walls in a short table and get a yes.
3. **Dry run:** `python3 scripts/scaffold.py <config> --dry-run`. Fix any config error it reports;
   do not work around it.
4. **Run it:** `python3 scripts/scaffold.py <config>`. It creates the Management repo and every new
   department repo. It never overwrites a file. For a department folder that already has a
   `CLAUDE.md` (an existing project) it leaves the charter alone and writes the charter section to
   a patch file.
5. **Existing projects:** merging the patch into an existing project's `CLAUDE.md` is that
   project's work. Start a session in that project to merge it under its own charter, after the
   user agrees.
6. **Git:** `git init` each new repo and make the first commit. Ask the user before creating any
   remote; recommend **private** remotes, since these repos will hold business knowledge.
7. **Check:** `python3 scripts/check.py <management repo>`. Report every problem it prints.
8. **First real request:** suggest the user try one cross-department question so the protocol gets
   exercised. Expect the first few to change the protocol, and record those changes in the
   decision register.

### B. Add a department

Follow [reference/operating.md](reference/operating.md#add-a-department): create the repo from
`templates/department/` (or wire in an existing project), add its section to the directory, its
rows to the capability matrix and systems map, a decision-register entry, then start a session in
every existing department to update its `knowledge/interop/ai-team.md` team table.

### C. Change a department's scope, path or name

[reference/operating.md](reference/operating.md#change-a-department). Routing is by **repo path**;
a renamed folder breaks every pointer, so the registry and every department's team table change in
the same session.

### D. Retire a department

[reference/operating.md](reference/operating.md#retire-a-department). Its domain is reassigned
first, its open ledger rows are closed or moved, and the decision is recorded. Its repo is kept,
not deleted.

### E. Health check

Run `scripts/check.py` and report each problem. It is read-only. For each problem, say which
department owns the fix. Fixes inside a department repo go to that department by session.

## Optional modules

Asked about during the interview:

- **Principal's office** — the Management AI also supports the principal (CEO/MD/founder) directly:
  one front door, briefs, follow-ups, drafts never sent, and personal matters kept walled off.
- **PIAF** — the Process Implementation & Assurance Framework: every new process or feature states
  its Promise, Proof and Protection, and production release is checked against Gates 1–3. Text in
  `templates/modules/piaf/PIAF.md`.

## Rules for you while running this skill

- Write only inside the root folder the user gave you. Never overwrite an existing file; the
  scaffold refuses to, and so do you.
- No secrets, credentials or real personal data in any generated file or config.
- Do not add fallback or "smart" behaviour to the protocol: no fuzzy matching of departments, no
  default owners, no guessed values. If something has no owner, it is Management's until the user
  assigns it.
- Creating remotes, pushing, and starting sessions in existing projects are outward actions: ask
  first.
