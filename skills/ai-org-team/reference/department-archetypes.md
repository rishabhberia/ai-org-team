# Department archetypes

A menu to help the user **design** their structure. Each archetype is only a starting suggestion:
show the ones that fit what the user described, and let them pick, rename, split, merge or drop
them. Nothing here goes into a config until the user has confirmed it for their organization.

## How to use this menu

1. Ask what the organization does and roughly how it is organized today (teams, business lines,
   who decides what).
2. Propose a structure: the archetypes that fit, plus any the user's business clearly needs that
   are not listed. Say why each is there, in one line.
3. Ask about **splits and groups**. One department may need several AIs when it covers separate
   business lines, e.g. *Sales → Equipment rentals* and *Sales → Service contracts*, or
   *Operations → Client delivery* and *Operations → Own fleet*. Each AI gets its own repo and
   charter; the shared `group` keeps them together in the org chart.
4. Ask about **merges**. A small organization may want one AI for *Finance & Legal* or
   *HR & Admin*. Fewer AIs is fine; every domain still needs exactly one owner.
5. Run `scaffold.py --preview` and show the tree and table. Iterate until the user says yes.

Rules while designing:
- **Every domain has exactly one owner.** If two departments would both own a thing (e.g.
  contract value: Sales or Legal?), ask the user to choose. Do not split ownership.
- **The Management AI is always there.** It owns the registry, the protocol and the ledger, and it
  is where conflicts and three-department work go. It owns no business data.
- **Keep the first version small.** Two to six departmental AIs is easier to get working; more can
  be added later (`reference/operating.md`).

## The archetypes

| Archetype | Typically owns | Others ask it for | Others should not ask it for | Typically restricted |
|---|---|---|---|---|
| **Sales** | Pipeline, quotes, pricing, account relationships | Pipeline and renewals; the rate card and how a quote is built; an account's state of play | Whether a contract is executed (→ Legal); outstanding (→ Finance); delivery status (→ Operations) | Pricing build-ups and margins; one client's terms in another's file |
| **Marketing** | Campaigns, brand, website, lead generation | Campaign status; lead sources; approved messaging | Pricing (→ Sales); product capability (→ Product) | Unreleased campaign plans; ad-account credentials |
| **Customer success / Support** | Onboarding, tickets, client health, renewals risk | A client's open issues; SLA performance; implementation state | Contract terms (→ Legal); invoices (→ Finance) | Client personal data in tickets |
| **Operations / Delivery** | Delivering the service or product; field work; delivery evidence | Delivery evidence behind an invoice; asset or job status; SOPs | Money figures (→ Finance); contract terms (→ Legal) | Staff pay rates in job reports |
| **Maintenance / Fleet** | Own assets: condition, servicing, spares | Asset condition and availability; service history; spares | Client deployments (→ Operations); spend approval (→ the principal) | Vendor pricing build-ups |
| **Finance** | Billing, receivables, payables, books, cash | Any money figure: billed, received, outstanding, with basis and as-of date | Whether work was delivered (→ Operations); contract terms (→ Legal) | Bank details; individual pay; unaudited figures presented as final |
| **Legal & Compliance** | Contracts, entities, registrations, disputes, regulatory | Contract status and terms; entity facts; disputes and notices; compliance obligations | Money figures (→ Finance); pricing (→ Sales) | Privileged material; litigation strategy |
| **HR / People** | Employment, roles, policies, recruitment | Whether a person is employed and in what role; who holds a function; policy with its date | Pay of a named person (never crosses); legal positions (→ Legal) | Individual pay; personal data |
| **Product / Engineering** | Product portfolio, roadmap, code, releases | What a product does; whether a capability is built; bug/feature status; release order | Business data inside the product (→ the data owner) | Unpatched security-defect detail |
| **Procurement / Purchasing** | Vendors, purchase orders, sourcing | PO status; approved vendors; lead times | Payment status (→ Finance); spec decisions (→ the requesting department) | Vendor quotes from competing bidders |
| **IT / Internal systems** | Accounts, devices, internal tools, access | Who has access to what; system status | Product code (→ Product); business data (→ its owner) | Credentials; security configuration |
| **Strategy / Business development** | Partnerships, new markets, M&A | Partnership status; market studies | Contract execution (→ Legal); valuations as fact (→ Finance) | Deal terms under NDA |

## Grouping examples

```
Sales                          Operations
├── Equipment rentals AI        ├── Client delivery AI
└── Service contracts AI        └── Own fleet maintenance AI
```

In the config, give each AI its own entry with the same `"group"`. Each needs its own `slug`,
`short` code, folder, and its own non-overlapping `owns` / `ask_for`.
