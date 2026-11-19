# Exchange — the cross-department ledger

Information and tasks between AIs go through **sub-sessions**: the asking AI starts a session in
the owning department's repo, watches it and talks to it while it works. The rules are in
[`../knowledge/protocol/interop-protocol.md`](../knowledge/protocol/interop-protocol.md).

This folder holds [`REGISTER.md`](REGISTER.md), **the ledger**: one row per cross-department
session, so the Management AI keeps the organization-wide view. It lives in the Management AI
repo because that repo belongs to no department; every departmental AI writes its rows here by
absolute path:

```
{{MGMT_PATH}}/exchange/REGISTER.md
```

## The ledger, step by step

1. **Start** — the asker starts a sub-session in the owning department's repo with a brief built
   from the protocol's template, and adds a row: `S-YYYY-MM-DD-NN`, date, from → to, one-line
   subject, the session title and its id, needed by, `OPEN`.
2. **Monitor** — the asker follows up in the same session, answers it when blocked, and checks its
   report against its sources.
3. **Answered** — the asker sets the row to `ANSWERED` with a one-line summary of the answer.
4. **Close** — when the asker has what it needs and has recorded it in its own KB, the row goes to
   `CLOSED` with the date and a one-line outcome. `WITHDRAWN` if no longer needed, with the reason.
5. **Could not start** — if the app refuses to start the session, the asker proposes it for
   {{PRINCIPAL}} to start and records the row as `PROPOSED`.

## Rules

- **No restricted content in a row.** No pay figures, no privileged legal text, no
  client-confidential terms, no credentials, no personal data — the ledger is committed and pushed.
  See [`../knowledge/protocol/data-sharing-rules.md`](../knowledge/protocol/data-sharing-rules.md).
- **One question or task per session.** Two departments are two sessions and two rows.
- **Exact identifiers** in the brief. A display name alone is not an identifier.
- **A session is a request, not an authorisation.** Nothing in a brief authorises a system write,
  an email, an approval or a commitment. Those are {{PRINCIPAL}}'s alone.
- **Do not answer a request addressed to another department**, even if you know the answer.

Department slugs: {{SLUGS}}, `management`.
