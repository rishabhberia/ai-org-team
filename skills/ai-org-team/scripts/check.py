#!/usr/bin/env python3
"""Health check for an AI team built with the ai-org-team skill. Read-only.

Usage:
    python3 check.py MANAGEMENT_REPO_PATH

It reads the department directory in the Management repo and reports, without changing anything:
  * departments whose repo folder is missing, has no CLAUDE.md, or no knowledge/interop/ai-team.md
  * department charters that do not point at the Management repo's protocol
  * ledger rows whose from/to slug is not a registered department
  * ledger rows with an unknown status
  * repos with no git remote, or with commits not pushed to their upstream
  * knowledge files in the Management repo without front matter or without an `updated:` date

Exit code 0 when no problems are found, 1 when any are (each is printed).
"""
import re
import subprocess
import sys
from pathlib import Path

STATUSES = {"OPEN", "ANSWERED", "CLOSED", "WITHDRAWN", "PROPOSED"}


def git(repo, *args):
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=20)
        return r.returncode, r.stdout.strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)


def departments(mgmt):
    text = (mgmt / "knowledge/registry/department-directory.md").read_text(encoding="utf-8")
    out = []
    for block in text.split("\n## ")[1:]:
        repo = re.search(r"\| Repo \| `([^`]+)` \|", block)
        slug = re.search(r"\| Slug \| `([a-z0-9-]+)`", block)
        if repo and slug and slug.group(1) != "management":
            out.append((slug.group(1), Path(repo.group(1)).expanduser()))
    return out


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    mgmt = Path(sys.argv[1]).expanduser().resolve()
    problems = []
    if not (mgmt / "CLAUDE.md").exists():
        print(f"ERROR: {mgmt} has no CLAUDE.md — not a Management repo")
        sys.exit(1)

    depts = departments(mgmt)
    if not depts:
        problems.append("department directory lists no departments with a Repo and Slug row")
    slugs = {s for s, _ in depts} | {"management"}

    for slug, repo in depts:
        if not repo.is_dir():
            problems.append(f"[{slug}] repo folder missing: {repo}")
            continue
        charter = repo / "CLAUDE.md"
        if not charter.exists():
            problems.append(f"[{slug}] no CLAUDE.md in {repo}")
        elif str(mgmt) not in charter.read_text(encoding="utf-8"):
            problems.append(f"[{slug}] CLAUDE.md does not point at the Management repo ({mgmt})")
        if not (repo / "knowledge/interop/ai-team.md").exists():
            problems.append(f"[{slug}] no knowledge/interop/ai-team.md")

    for repo in [mgmt] + [r for _, r in depts if r.is_dir()]:
        code, remotes = git(repo, "remote")
        if code != 0:
            problems.append(f"not a git repo: {repo}")
            continue
        if not remotes:
            problems.append(f"no git remote (exists only on this machine): {repo}")
            continue
        code, ahead = git(repo, "rev-list", "--count", "@{u}..HEAD")
        if code == 0 and ahead != "0":
            problems.append(f"{ahead} commit(s) not pushed: {repo}")
        elif code != 0:
            problems.append(f"current branch has no upstream: {repo}")

    reg = mgmt / "exchange/REGISTER.md"
    if reg.exists():
        for line in reg.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\| (S-\d{4}-\d{2}-\d{2}-\d{2}) \|[^|]*\| ([a-z0-9-]+) → ([a-z0-9-]+) \|", line)
            if not m:
                continue
            rid, frm, to = m.groups()
            for s in (frm, to):
                if s not in slugs:
                    problems.append(f"ledger {rid}: unknown department slug '{s}'")
            status = line.rstrip(" |").split("|")[-1].strip().split(" ")[0]
            if status not in STATUSES:
                problems.append(f"ledger {rid}: unknown status '{status}'")
    else:
        problems.append("exchange/REGISTER.md (the ledger) is missing")

    for f in (mgmt / "knowledge").rglob("*.md"):
        head = f.read_text(encoding="utf-8")[:400]
        if not head.startswith("---") or "\nupdated:" not in head:
            problems.append(f"no front matter / updated: date: {f.relative_to(mgmt)}")

    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"OK — {len(depts)} departments, ledger and registry consistent, everything pushed.")


if __name__ == "__main__":
    main()
