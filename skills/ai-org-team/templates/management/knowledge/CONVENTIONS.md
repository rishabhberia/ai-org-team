---
title: Knowledge base conventions
updated: {{TODAY}}
sources: []
confidence: high
---
# Conventions

How every file in this repo is written. Read by the Management AI each session and by humans
reviewing how the AI team is wired. Keep this repo on a **private** git remote.

## Folder layout

| Folder | Holds |
|---|---|
| `knowledge/registry/` | Who owns what: departments, capabilities, systems |
| `knowledge/protocol/` | How departments interact: sessions, data sharing, authority |
| `knowledge/group/` | The organization layer: business context, decisions |
{{CONVENTIONS_OPTIONAL}}| `exchange/` | The ledger of cross-department sessions (written to by every department) |
| `logs/` | The dated management log |

## Rules for every file

1. **Front matter**, on every file in `knowledge/`:
   ```
   ---
   title: <title>
   updated: YYYY-MM-DD
   sources:
     - <absolute path, repo file, session, or MCP tool used>
   confidence: high | medium | low
   ---
   ```
2. **This repo holds no departmental data.** If a fact belongs to a department, link to that
   department's file — do not copy it. The one exception is a *quoted answer* in the decision
   register, which always carries its department, source and as-of date.
3. **Attribution on every borrowed fact**: department · file, system or session · as-of date ·
   confidence.
4. **Distinguish** true zero / missing / not applicable / not yet established. Never write a
   missing value as 0 or leave it blank.
5. **No secrets, no restricted content** — see
   [`protocol/data-sharing-rules.md`](protocol/data-sharing-rules.md). Write `[redacted — see <path>]`.
6. Dates absolute (`2026-01-31`), currency explicit, units explicit.
7. Link with relative markdown links so the repo reads on GitHub.
8. **Registers are append-and-close, never delete.** Open items, decisions and ledger rows are
   closed with a date and kept.
