# Operating the team

All of these are Management's own work on the registry, plus a session in each department whose
own files must change. Management never edits a department's repo itself.

## Add a department

1. Interview for the new department (Round 2 of [interview.md](interview.md)).
2. **New repo:** copy `templates/department/` into the new folder and fill the placeholders by
   hand, or run `scaffold.py` with a config that lists only the new department and a throwaway
   `management.dir`, then move the department folder into place. **Existing project:** write
   `knowledge/interop/ai-team.md`, and start a session in that project to merge the charter
   section into its `CLAUDE.md`.
3. In the Management repo:
   - add its section to `knowledge/registry/department-directory.md`;
   - add its rows to `capability-matrix.md` and `systems-map.md`, and re-route any rows it now owns;
   - add any walls it holds to `protocol/data-sharing-rules.md`;
   - add a decision to `group/decision-register.md` (date, scope, decided by the principal);
   - add its slug to `exchange/README.md`.
4. Start one session in **every existing department** to update the team table in its
   `knowledge/interop/ai-team.md`, and record each in the ledger.
5. Run `scripts/check.py`.

## Change a department

Scope, path or name changes:

1. Record the decision first (decision register).
2. Update the directory, capability matrix, systems map and, if it moved, every place the old path
   appears in the Management repo.
3. Start a session in every department to update its team table, and in the changed department
   to update its own charter.
4. **Never rename a folder silently.** Routing is by path, and every pointer breaks.
5. Run `scripts/check.py`.

## Retire a department

1. Decide who owns each part of its domain afterwards, and record the decision.
2. Close or reassign its open ledger rows (`WITHDRAWN` with the reason, or a new session to the
   new owner).
3. Move its directory section to a "Retired" heading with the date. Do not delete it.
4. Re-route its capability-matrix and systems-map rows.
5. Start a session in every remaining department to update its team table.
6. Keep the repo. Its history is the record.

## Change the protocol itself

1. Record the decision, quoting the principal's words and the date.
2. Update `knowledge/protocol/*`, the Management `CLAUDE.md`, and `exchange/README.md`.
3. Commit and push the Management repo **before** rolling out, so departments read the new text.
4. Start one session per department to update its own copy (`knowledge/interop/ai-team.md` and its
   charter section), and record each in the ledger. Check each department's diff when it reports
   back; a session's report is not proof.
5. Track the rollout as an open item until every department has pushed.

## Session hygiene

- One question or task per session; follow up in the same session.
- Before a session ends its work, the asker checks the result against its sources.
- Close every ledger row with a date and a one-line outcome. Nothing is deleted.
- Every repo is pushed at the end of every session. `scripts/check.py` flags anything that exists
  only on one machine.
