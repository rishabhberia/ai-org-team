# Setup interview

Do the structure design first (see [department-archetypes.md](department-archetypes.md)): which
departments, which are split into several AIs, which are merged. Then ask these in a few rounds,
not all at once. Write the answers into the config file
(`examples/example-config.json` shows the format). Never fill a gap with a guess: an unanswered
item stays unanswered and setup waits for it.

## Round 1 — the organization

1. **Organization name** (`org`).
2. **The principal** (`principal`): the human who approves sends, spend, writes to live systems,
   merges and deploys. Use a role if they prefer ("the Managing Director"), not a guess at a name.
3. **Root folder** (`root`): where all the AI repos will live, e.g. `~/ai-team`.
4. **Management AI name and folder** (`management.name`, `management.dir`).
5. **Optional modules** (`modules`):
   - `principal_office`: should the Management AI also support the principal directly (briefs,
     follow-ups, drafts, personal matters kept walled off)?
   - `piaf`: should every AI apply the Process Implementation & Assurance Framework when designing
     and releasing processes and features?

## Round 2 — the departments

For each department (at least two):

| Field | Question to ask |
|---|---|
| `name` | What is the department called? |
| `slug` | Short id for the ledger: lowercase, hyphens (suggest one; let them change it) |
| `short` | 2–5 capital letters for the capability matrix (e.g. FIN) |
| `ai_name` | What should its AI be called? |
| `dir` | Its folder under the root. If a project already exists for it, give that folder: the skill wires it in without touching its charter |
| `group` | *(optional)* The department it belongs to, when one department has several AIs (e.g. two Sales AIs, one per business line). Same `group` on each |
| `kb_root` | *(optional)* Its knowledge folder, if not `knowledge` (e.g. an existing project that uses `docs` or `kb`) |
| `owns` | What does it own? One sentence |
| `ask_for` | What should other departments ask it for? A list |
| `not_for` | What should they **not** ask it for, and who owns that instead? A list, "→ Dept" at the end |
| `restricted` | What must never leave it? A list |
| `systems` | Which systems or connectors does it own? For each: what others may do, and what nobody else may ever do (optional) |

After this round, run `scaffold.py --preview` and show the user the org chart before going on.

Check the answers against each other: every "→ Dept" in `not_for` must name a department that
exists. If two departments both claim the same thing, ask which one owns it. Do not split it.

## Round 3 — the confidentiality walls

Offer this standard set and ask the user to confirm, edit, or drop each, and to say which
department holds it (`held_by` is a slug, or `nobody` for things that belong in no repo):

| Wall | Usually held by | What may cross instead |
|---|---|---|
| Individual pay — salary, pay rates, increments | HR (or Finance) | The rule or an aggregate; never a named person's number |
| Personal data — ID numbers, bank details, home addresses, personal phones | HR | Role, entity and employment status, by employee id |
| Privileged legal material and litigation strategy | Legal | Legal's conclusion, only as far as the asker needs |
| Client confidentiality undertakings, NDAs | Sales / Legal | That a constraint exists; never one client's terms in another's file |
| Internal pricing build-ups, margins | Sales | The approved price |
| Credentials and secrets — passwords, tokens, API keys, account numbers | nobody | `[redacted — see <path>]` |
| Unpatched security-defect detail | Product / Engineering | That the defect exists, the product, its priority |
| Raw source files — contracts, HR records, financial workbooks | nobody | A summary with the path cited; never the file |

## Round 4 — standing authorisations (optional)

Has the principal given any standing written approvals (e.g. "a deploy agent may deploy repo X
after review")? Record them verbatim in `standing_authorisations`, with the date. If none, leave
the field out. Never infer one.
