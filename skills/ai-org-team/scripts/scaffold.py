#!/usr/bin/env python3
"""Scaffold an AI team (one Management AI repo + one repo per department) from a config file.

Usage:
    python3 scaffold.py CONFIG.json [--dry-run] [--patch-dir DIR] [--today YYYY-MM-DD]

What it does:
  * Creates the Management AI repo from templates/management (refuses if it already has a CLAUDE.md).
  * For each department:
      - folder missing or empty      -> creates it from templates/department
      - folder exists with CLAUDE.md -> an existing project: CLAUDE.md is NOT touched. It writes
        knowledge/interop/ai-team.md only if that file is absent, and writes the charter section
        to PATCH_DIR/<slug>-charter-section.md for a human or agent to merge in by hand.
  * Never overwrites an existing file. Never runs git. Standard library only.

It fails loudly on a bad config or on any placeholder left unrendered. It never invents values:
every field it needs must be in the config.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "templates"
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{1,30}$")
SHORT_RE = re.compile(r"^[A-Z]{2,5}$")
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")

DEPT_REQUIRED = ["slug", "short", "name", "ai_name", "dir", "owns", "ask_for", "not_for", "restricted"]


class ConfigError(Exception):
    pass


# ---------------------------------------------------------------- config

def load_config(path):
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    errors = []

    for key in ("org", "principal", "root", "management", "departments", "walls"):
        if key not in cfg or cfg[key] in ("", None, []):
            errors.append(f"missing or empty top-level field: {key}")
    mgmt = cfg.get("management") or {}
    for key in ("name", "dir"):
        if not mgmt.get(key):
            errors.append(f"missing management.{key}")

    depts = cfg.get("departments") or []
    seen_slug, seen_short, seen_dir = set(), set(), set()
    for i, d in enumerate(depts):
        where = f"departments[{i}]"
        for key in DEPT_REQUIRED:
            if key not in d or d[key] in ("", None, []):
                errors.append(f"{where}: missing or empty field '{key}'")
        slug = d.get("slug", "")
        if slug and not SLUG_RE.match(slug):
            errors.append(f"{where}: slug '{slug}' must be lowercase letters, digits and hyphens")
        if slug == "management":
            errors.append(f"{where}: slug 'management' is reserved")
        if slug in seen_slug:
            errors.append(f"{where}: duplicate slug '{slug}'")
        seen_slug.add(slug)
        short = d.get("short", "")
        if short and not SHORT_RE.match(short):
            errors.append(f"{where}: short code '{short}' must be 2-5 capital letters")
        if short == "MGT" or short in seen_short:
            errors.append(f"{where}: short code '{short}' is reserved or duplicated")
        seen_short.add(short)
        ddir = d.get("dir", "")
        if ddir in seen_dir or ddir == mgmt.get("dir"):
            errors.append(f"{where}: folder '{ddir}' is used twice")
        seen_dir.add(ddir)
        for listkey in ("ask_for", "not_for", "restricted"):
            if listkey in d and not isinstance(d[listkey], list):
                errors.append(f"{where}: '{listkey}' must be a list of strings")
        for j, s in enumerate(d.get("systems", [])):
            for key in ("system", "connector", "others_may", "never"):
                if not s.get(key):
                    errors.append(f"{where}.systems[{j}]: missing '{key}'")
        for j, q in enumerate(d.get("matrix", [])):
            if not q.get("question"):
                errors.append(f"{where}.matrix[{j}]: missing 'question'")

    for i, w in enumerate(cfg.get("walls") or []):
        for key in ("wall", "held_by", "may_cross"):
            if not w.get(key):
                errors.append(f"walls[{i}]: missing '{key}'")
        held = w.get("held_by")
        if held and held not in seen_slug and held != "nobody":
            errors.append(f"walls[{i}]: held_by '{held}' is not a department slug (or 'nobody')")

    if len(depts) < 2:
        errors.append("an AI team needs at least two departments")
    if errors:
        raise ConfigError("\n".join(errors))
    return cfg


# ---------------------------------------------------------------- rendering helpers

def md_list(items):
    return "\n".join(f"- {x}" for x in items)


def team_table(cfg, mgmt_path):
    rows = ["| Department | AI | Repo | Ask it for |", "|---|---|---|---|"]
    for d in cfg["departments"]:
        path = str(Path(cfg["_root"]) / d["dir"])
        rows.append(f"| {d['name']} | {d['ai_name']} | `{path}` | {'; '.join(d['ask_for'])} |")
    rows.append(f"| **Management** | {cfg['management']['name']} | `{mgmt_path}` | Routing, "
                "cross-department orchestration, conflicts, the organization view. It lends no authority |")
    return "\n".join(rows)


def team_tree(cfg):
    lines = ["```", f"{cfg['org']} AI team", f"└── {cfg['management']['name']}"]
    depts = cfg["departments"]
    for i, d in enumerate(depts):
        branch = "└──" if i == len(depts) - 1 else "├──"
        lines.append(f"    {branch} {d['name']} — {d['ai_name']}")
    lines.append("```")
    return "\n".join(lines)


def directory_sections(cfg):
    out = []
    for d in cfg["departments"]:
        path = str(Path(cfg["_root"]) / d["dir"])
        out.append(f"""---

## {d['name']} · **{d['ai_name']}**

| | |
|---|---|
| Repo | `{path}` |
| KB root | `knowledge/` (start at `knowledge/00-INDEX.md`) |
| Slug | `{d['slug']}` (shorthand {d['short']}) |
| Owns | {d['owns']} |

**Ask it for:**
{md_list(d['ask_for'])}

**Do not ask it for:**
{md_list(d['not_for'])}

**Restricted — never leaves {d['name']}:**
{md_list(d['restricted'])}
""")
    return "\n".join(out)


def matrix_rows(cfg):
    rows = []
    for d in cfg["departments"]:
        entries = d.get("matrix") or [{"question": q} for q in d["ask_for"]]
        for q in entries:
            rows.append(f"| {q['question']} | {d['short']} | {q.get('note', '')} |")
    return "\n".join(rows)


def systems_rows(cfg):
    rows = []
    for d in cfg["departments"]:
        for s in d.get("systems", []):
            rows.append(f"| {s['system']} | {s['connector']} | **{d['short']}** | {s['others_may']} | {s['never']} |")
    return "\n".join(rows) if rows else "| *None recorded yet* | — | — | — | — |"


def walls_table(cfg):
    names = {d["slug"]: d["name"] for d in cfg["departments"]}
    rows = ["| Wall | Held by | What may cross instead |", "|---|---|---|"]
    for w in cfg["walls"]:
        held = "Nobody. It does not belong in any repo" if w["held_by"] == "nobody" else names[w["held_by"]]
        rows.append(f"| **{w['wall']}** | {held} | {w['may_cross']} |")
    return "\n".join(rows)


def render(text, values):
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    left = sorted(set(PLACEHOLDER_RE.findall(text)))
    if left:
        raise ConfigError(f"unrendered placeholders: {', '.join(left)}")
    return text


# ---------------------------------------------------------------- writer

class Writer:
    def __init__(self, dry_run):
        self.dry_run = dry_run
        self.created, self.skipped = [], []

    def write(self, path, text):
        path = Path(path)
        if path.exists():
            self.skipped.append(str(path))
            return False
        if not self.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        self.created.append(str(path))
        return True


def read_t(rel):
    return (TEMPLATES / rel).read_text(encoding="utf-8")


# ---------------------------------------------------------------- main build

def build(cfg, today, patch_dir, dry_run):
    root = Path(os.path.expanduser(cfg["root"])).resolve()
    cfg["_root"] = str(root)
    mgmt_path = str(root / cfg["management"]["dir"])
    mods = cfg.get("modules", {})
    po, piaf = bool(mods.get("principal_office")), bool(mods.get("piaf"))
    principal = cfg["principal"]

    base = {
        "ORG": cfg["org"],
        "PRINCIPAL": principal,
        "TODAY": today,
        "MGMT_NAME": cfg["management"]["name"],
        "MGMT_PATH": mgmt_path,
        "DEPT_COUNT": str(len(cfg["departments"])),
        "DEPT_LIST": ", ".join(d["name"] for d in cfg["departments"]),
        "TEAM_TABLE": team_table(cfg, mgmt_path),
    }

    # --- Management repo
    mgmt_dir = Path(mgmt_path)
    if (mgmt_dir / "CLAUDE.md").exists():
        raise ConfigError(f"{mgmt_dir} already has a CLAUDE.md — the Management repo exists. "
                          "Change the registry by hand (see reference/operating.md), not with this script.")
    po_section = render(read_t("modules/principal-office/_charter-section.md"), base) if po else ""
    piaf_section = render(read_t("modules/piaf/_charter-section.md"), base) if piaf else ""
    index_opt = ""
    conv_opt = ""
    dec_opt = ""
    if po:
        index_opt += ("\n## The principal's office\n\n| File | What it gives you |\n|---|---|\n"
                      "| [principal-office/README.md](principal-office/README.md) | What the support to "
                      f"{principal}'s office covers, and the rules for personal matters |\n")
        conv_opt += f"| `knowledge/principal-office/` | {principal}'s office: work and personal matters |\n"
        dec_opt += (f"| D4 | {today} | The Management AI also supports {principal}'s office, for work and "
                    "personal matters. No authority is added (D3) | Management | " + principal +
                    " | [`../principal-office/README.md`](../principal-office/README.md) |\n")
    if piaf:
        index_opt += ("\n## PIAF\n\n| File | What it gives you |\n|---|---|\n"
                      "| [group/piaf/PIAF.md](group/piaf/PIAF.md) | The Process Implementation & Assurance "
                      "Framework every AI applies when designing and releasing a process |\n")
        n = "D5" if po else "D4"
        dec_opt += (f"| {n} | {today} | PIAF applies in every AI and project: designs state Promise, Proof and "
                    "Protection; Gate 1–3 evidence is checked before production. No authority is added (D3) | All | "
                    + principal + " | [`piaf/PIAF.md`](piaf/PIAF.md) |\n")

    mvals = dict(base)
    mvals.update({
        "PRINCIPAL_OFFICE_CLAUSE": f", and **support to {principal}'s office**" if po else "",
        "PRINCIPAL_OFFICE_JOB": (f"5. **Support {principal}'s office** — see below.\n" if po else ""),
        "OPTIONAL_CHARTER_SECTIONS": ("\n" + po_section + piaf_section) if (po or piaf) else "",
        "TEAM_TREE": team_tree(cfg),
        "INDEX_OPTIONAL": index_opt,
        "CONVENTIONS_OPTIONAL": conv_opt,
        "DECISIONS_OPTIONAL": dec_opt,
        "DIRECTORY_SECTIONS": directory_sections(cfg),
        "MATRIX_ROWS": matrix_rows(cfg),
        "SHORTHAND": ", ".join(f"{d['short']} = {d['name']}" for d in cfg["departments"]) + ", MGT = Management",
        "SYSTEMS_ROWS": systems_rows(cfg),
        "WALLS_TABLE": walls_table(cfg),
        "STANDING_AUTHORISATIONS": cfg.get("standing_authorisations", "") and
            ("## Standing authorisations\n\n" + cfg["standing_authorisations"]),
        "SLUGS": ", ".join(f"`{d['slug']}`" for d in cfg["departments"]),
        "BUSINESS_ROWS": "\n".join(f"| {d['name']} | {d['owns']} | {d['name']} |" for d in cfg["departments"]),
    })

    w = Writer(dry_run)
    for tpl in sorted((TEMPLATES / "management").rglob("*")):
        if tpl.is_file():
            rel = tpl.relative_to(TEMPLATES / "management")
            w.write(mgmt_dir / rel, render(tpl.read_text(encoding="utf-8"), mvals))
    w.write(mgmt_dir / "exchange/.gitkeep", "")
    if po:
        w.write(mgmt_dir / "knowledge/principal-office/README.md",
                render(read_t("modules/principal-office/README.md"), mvals))
    if piaf:
        w.write(mgmt_dir / "knowledge/group/piaf/PIAF.md", render(read_t("modules/piaf/PIAF.md"), mvals))
    w.write(mgmt_dir / ".gitignore", ".DS_Store\n.claude/settings.local.json\n")

    # --- Departments
    patches = []
    for d in cfg["departments"]:
        dvals = dict(base)
        restricted_rule = "6. **Restricted — never leaves this department:** " + "; ".join(d["restricted"]) + "."
        dvals.update({
            "DEPT_NAME": d["name"], "AI_NAME": d["ai_name"], "DEPT_SLUG": d["slug"], "OWNS": d["owns"],
            "OWNS_SENTENCE": f"You own {d['owns']}; every other domain is asked of its owner.",
            "ASK_FOR": md_list(d["ask_for"]), "RESTRICTED": md_list(d["restricted"]),
            "RESTRICTED_RULE": restricted_rule,
            "DEPT_OPTIONAL_RULES": (f"- **PIAF** applies to every process or feature you design or release: "
                                    f"`{mgmt_path}/knowledge/group/piaf/PIAF.md`.\n" if piaf else ""),
        })
        section = render(read_t("department/_charter-section.md"), dvals)
        dvals["CHARTER_SECTION"] = section
        ddir = root / d["dir"]
        existing = (ddir / "CLAUDE.md").exists()
        if existing:
            w.write(ddir / "knowledge/interop/ai-team.md", render(read_t("department/knowledge/interop/ai-team.md"), dvals))
            ppath = Path(patch_dir) / f"{d['slug']}-charter-section.md"
            w.write(ppath, section)
            patches.append((d["slug"], str(ddir), str(ppath)))
            continue
        for tpl in sorted((TEMPLATES / "department").rglob("*")):
            if not tpl.is_file() or tpl.name == "_charter-section.md":
                continue
            rel = tpl.relative_to(TEMPLATES / "department")
            if str(rel) == "logs/log.md":
                rel = Path("logs") / f"{d['slug']}-log.md"
            w.write(ddir / rel, render(tpl.read_text(encoding="utf-8"), dvals))
        w.write(ddir / ".gitignore", ".DS_Store\n.claude/settings.local.json\n")
    return w, patches, mgmt_path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config")
    ap.add_argument("--dry-run", action="store_true", help="show what would be written; write nothing")
    ap.add_argument("--patch-dir", help="where charter sections for existing repos go "
                    "(default: <root>/_ai-org-setup-patches)")
    ap.add_argument("--today", help="date stamp for front matter (default: today)")
    a = ap.parse_args()
    try:
        cfg = load_config(a.config)
        today = a.today or dt.date.today().isoformat()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", today):
            raise ConfigError("--today must be YYYY-MM-DD")
        patch_dir = a.patch_dir or str(Path(os.path.expanduser(cfg["root"])).resolve() / "_ai-org-setup-patches")
        w, patches, mgmt_path = build(cfg, today, patch_dir, a.dry_run)
    except (ConfigError, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    verb = "would create" if a.dry_run else "created"
    print(f"{verb} {len(w.created)} files; skipped {len(w.skipped)} that already exist")
    for p in w.skipped:
        print(f"  skipped (exists): {p}")
    print(f"Management repo: {mgmt_path}")
    for slug, ddir, ppath in patches:
        print(f"EXISTING PROJECT {slug}: {ddir} — CLAUDE.md untouched; merge {ppath} into it")


if __name__ == "__main__":
    main()
