# Architecture and the reasons behind it

This structure came out of running a real multi-department AI team in Claude Code. Each rule below
exists because something went wrong, or nearly did, without it.

## The shape

| Part | Lives in | Holds |
|---|---|---|
| **Management AI** | its own repo | The registry (who owns what), the protocol, the ledger, cross-department decisions and risks. **No departmental data** |
| **Departmental AI** | one repo per department | Its charter (`CLAUDE.md`), knowledge base, log, open items, memory. Its own systems |
| **Ledger** | `exchange/REGISTER.md` in the Management repo | One row per cross-department session request |
| **Principal** | a human | All approvals |

The Management AI is **above the departments in routing, not in authority**.

## Why each rule exists

**The owner is the only source of truth.** A department that rebuilds another's number from raw
files produces a figure that looks complete and is not, and nobody is accountable for it. Finance
knows which invoices are disputed; Legal knows which contract version was signed. The caveats are
the value.

**Ask by sub-session, not by reading the other KB.** A knowledge base is as of its `updated:` date,
and it is written for its own department. Reading it from outside loses the caveats and the
freshness. A session runs under the owner's charter and memory, so the owner answers in its own
way. The asker can watch it and talk to it, so problems surface at once rather than days later in
a file.

**Earlier versions used request files and in-session sub-agents.** Request files (CDRs) went
unanswered until the other department happened to open a session. In-session sub-agents ran
without the target project's memory, and nobody could watch them. Sub-sessions fix both.

**The ledger.** Sessions are many and short-lived. One row per request gives Management (and the
principal) the organization-wide view: what is open, between whom, since when, with what outcome.

**One hop.** Without it a question ricochets: A asks B, B asks C, C asks A. The answering session
says "needs <Dept>" and the asker decides. Management, handling an escalation, is the only one
that fans out.

**Coordinate, don't do.** A coordinating AI that edits another project directly works without that
project's context and mixes contexts. The work is done by an agent inside the project, under its
own charter, and checked by a separate agent.

**Missing is never zero.** A missing meter reading written as 0 becomes a real-looking consumption
figure in a report. Every answer names what is missing; any calculation that needs it stops.

**Conflicts are recorded, not resolved by convenience.** When the contract says one rate and the
invoices show another, that is a finding: money is lost in exactly these gaps. Both positions go
into the decision register, and the owner of the fact decides.

**Walls hold toward Management.** Management routes questions; it does not unlock records. A
department that refuses to pass pay data to Management is behaving correctly.

**No AI approves.** Orchestration lends no authority. A child session gets an approval only when
the parent relays the principal's own words, with the date and the exact target.

**Route by repo path.** Display names drift. A folder path is unambiguous, so every pointer uses it.

**Everything pushed.** A registry or ledger that exists on one laptop is lost with it. Every repo
gets a private remote, and every session ends pushed.

## What the structure deliberately does not do

- It does not give Management a copy of departmental data "for convenience".
- It does not average two departments' numbers or pick the newer one.
- It does not let a department act on another's behalf, in either direction.
- It does not fall back to a different channel when a session cannot be started: the request is
  proposed to the principal instead.
