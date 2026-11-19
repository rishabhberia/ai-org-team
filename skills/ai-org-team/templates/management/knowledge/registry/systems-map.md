---
title: Systems map — which department owns which system
updated: {{TODAY}}
sources:
  - Setup by the ai-org-team skill, {{TODAY}}
confidence: medium
---
# Systems map

MCP servers and connectors are usually configured **per user, not per project**: any
department's session can technically reach all of them. Access is therefore not the control.
**Ownership is.** The owning department holds the rules, the caveats and the accountability for
what a system's data means.

**A department may not publish a figure from a system it does not own.** It asks the owner in a
sub-session, and the answer carries the owner's caveats.

| System | Connector / MCP | Owner | Others may | Never |
|---|---|---|---|---|
{{SYSTEMS_ROWS}}
| Email | Email connector | Shared | Read own threads; create **drafts** | Send without {{PRINCIPAL}}'s approval for that message |
