#!/usr/bin/env python3
"""PET-A-MON keeper toolbox.

Commands (run from anywhere; app clones live in $PETAMON_WORK, default: parent of this repo):
  sync                      clone missing app repos, fetch + fast-forward existing ones
  status                    HEAD of each app vs. last reviewed SHA in state/sync-state.json
  news [APP]                commits since last reviewed SHA, with each touched file classified
  drift [--all] [PATH...]   theme-normalised comparison of shared files across the apps
  classify PATH...          tell whether a path is core / themed / app-specific / lovable-managed
  translate FROM TO         read a patch on stdin, rewrite FROM's theme tokens into TO's, print it
  mark APP [SHA]            record APP as reviewed up to SHA (default: its current HEAD)

Nothing here pushes or edits app repos: the keeper does that itself, following CLAUDE.md.
"""
from __future__ import annotations

import difflib
import fnmatch
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "apps.json").read_text())
STATE_FILE = ROOT / "state" / "sync-state.json"
WORK = Path(os.environ.get("PETAMON_WORK", ROOT.parent))
APPS = {a["id"]: a for a in CFG["apps"]}
BRANCH = CFG.get("branch", "main")

# ---- path classification ---------------------------------------------------
# Order matters: first match wins.
CLASSES: list[tuple[str, list[str]]] = [
    ("lovable-managed", [
        "supabase/migrations/*", "drizzle/*", "src/integrations/supabase/types.ts",
        "src/integrations/supabase/client*.ts", "src/integrations/supabase/auth-*.ts",
        "src/routeTree.gen.ts", ".lovable/*", ".env", "bun.lock", "supabase/config.toml",
    ]),
    ("app-specific", [
        "src/game/catalog.ts", "src/game/milano.ts", "src/components/cat/art.ts",
        "src/components/cat/fantasy.ts", "public/*", "doc/STORMO.md",
        "doc/sql/02_species_seed.sql", "doc/lovable-prompts/02_species_seed.txt",
        "src/lib/email-templates/brand.ts", "src/test/milano.test.ts",
        "src/routes/colonia.tsx", "src/routes/branco.tsx", "src/routes/stormo.tsx",
        "scripts/make-icons.mjs", "roadmap.md",
    ]),
    ("themed", [
        "src/i18n/*", "src/styles/*", "src/server/lib/prompts.ts", "src/game/vision-schema.ts",
        "src/lib/email-templates/*", "src/routes/privacy.tsx", "src/routes/regole.tsx",
        "doc/*", "README.md", "AGENTS.md", "tests/*", "src/test/*",
    ]),
]


def classify(path: str) -> str:
    for name, pats in CLASSES:
        if any(fnmatch.fnmatch(path, p) for p in pats):
            return name
    return "core"


# ---- helpers ----------------------------------------------------------------
def git(app: str, *args: str, check: bool = True) -> str:
    r = subprocess.run(["git", "-C", str(WORK / app), *args], capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"git {' '.join(args)} failed in {app}: {r.stderr.strip()}")
    return r.stdout


def load_state() -> dict:
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {"reviewed": {}}


def save_state(s: dict) -> None:
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(s, indent=2) + "\n")


def tokens(app: str) -> list[tuple[str, int, str]]:
    """(kind, index, word) for every theme token of an app, longest word first."""
    out = []
    for kind, words in APPS[app]["theme"]["tokens"].items():
        for i, w in enumerate(words):
            out.append((kind, i, w))
    return sorted(out, key=lambda t: -len(t[2]))


def _sub(text: str, app: str, repl) -> str:
    for kind, i, w in tokens(app):
        text = re.sub(rf"(?<![\w-]){re.escape(w)}(?![\w])", lambda _m: repl(kind, i), text)
    return text


def normalise(text: str, app: str) -> str:
    return _sub(text, app, lambda k, i: f"«{k}{i}»")


def translate(text: str, src: str, dst: str) -> str:
    dt = APPS[dst]["theme"]["tokens"]
    marked = normalise(text, src)
    def back(m):
        kind, i = m.group(1), int(m.group(2))
        words = dt[kind]
        return words[min(i, len(words) - 1)]
    return re.sub(r"«([a-z_]+?)(\d+)»", back, marked)


def read(app: str, path: str) -> str | None:
    p = WORK / app / path
    return p.read_text(errors="replace") if p.is_file() else None


def tracked(app: str) -> set[str]:
    return set(git(app, "ls-files").split("\n")) - {""}


# ---- commands ---------------------------------------------------------------
def cmd_sync(_args):
    owner = CFG["github_owner"]
    for app in APPS:
        d = WORK / app
        if not (d / ".git").exists():
            subprocess.run(["git", "clone", "--depth", "100", f"https://github.com/{owner}/{app}", str(d)], check=True)
        else:
            git(app, "fetch", "--depth", "100", "origin", BRANCH)
            dirty = git(app, "status", "--porcelain").strip()
            if dirty:
                print(f"!! {app}: working tree dirty, not fast-forwarding")
                continue
            git(app, "checkout", "-q", BRANCH)
            git(app, "merge", "--ff-only", "-q", f"origin/{BRANCH}")
        print(f"{app}: {git(app, 'log', '-1', '--format=%h %ci %s').strip()}")


def cmd_status(_args):
    st = load_state()["reviewed"]
    for app in APPS:
        head = git(app, "rev-parse", "HEAD").strip()
        rev = st.get(app, {}).get("sha")
        n = git(app, "rev-list", "--count", f"{rev}..HEAD", check=False).strip() if rev else "?"
        print(f"{app:14} HEAD {head[:9]}  reviewed {str(rev)[:9]}  new commits: {n or '?'}")


def cmd_news(args):
    st = load_state()["reviewed"]
    for app in (args or APPS):
        rev = st.get(app, {}).get("sha")
        rng = f"{rev}..HEAD" if rev else "HEAD~10..HEAD"
        log = git(app, "log", "--no-merges", "--format=@@%h|%ci|%s", "--name-status", rng, check=False)
        print(f"===== {app}  ({rng})")
        if not log.strip():
            print("  (nothing new)")
            continue
        for line in log.splitlines():
            if line.startswith("@@"):
                h, d, s = line[2:].split("|", 2)
                print(f"\n  {h} {d[:16]}  {s}")
            elif line.strip():
                parts = line.split("\t")
                path = parts[-1]
                print(f"      {parts[0]:4} [{classify(path):15}] {' -> '.join(parts[1:])}")


def cmd_drift(args):
    show_all = "--all" in args
    paths = [a for a in args if not a.startswith("--")]
    ids = list(APPS)
    files = {a: tracked(a) for a in ids}
    universe = sorted(set(paths) if paths else set().union(*files.values()))
    rows = []
    for p in universe:
        cls = classify(p)
        if not paths and cls in ("lovable-managed", "app-specific"):
            continue
        present = [a for a in ids if p in files[a]]
        if len(present) < len(ids):
            rows.append((p, cls, "only in " + ",".join(present), None))
            continue
        norm = {a: normalise(read(a, p) or "", a).splitlines() for a in ids}
        pair = {}
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                d = [l for l in difflib.unified_diff(norm[a], norm[b], lineterm="", n=0)
                     if l[:1] in "+-" and not l.startswith(("+++", "---"))]
                pair[f"{a[:4]}/{b[:4]}"] = len(d)
        if show_all or paths or any(pair.values()):
            rows.append((p, cls, pair, norm if paths else None))
    for p, cls, info, norm in rows:
        if isinstance(info, str):
            print(f"{cls:15} {p}  ({info})")
        else:
            print(f"{cls:15} {p}  " + "  ".join(f"{k}:{v}" for k, v in info.items()))
            if norm and any(info.values()):
                a, b = ids[0], ids[-1]
                for x, y in ((ids[0], ids[1]), (ids[1], ids[2])):
                    d = list(difflib.unified_diff(norm[x], norm[y], x, y, lineterm="", n=1))
                    if d:
                        print("\n".join(d[:200]))
    print(f"\n{len(rows)} paths listed (theme tokens normalised; lovable-managed/app-specific hidden unless named).")


def cmd_classify(args):
    for p in args:
        print(f"{classify(p):15} {p}")


def cmd_translate(args):
    if len(args) != 2 or args[0] not in APPS or args[1] not in APPS:
        sys.exit("usage: translate FROM_APP TO_APP < patch")
    sys.stdout.write(translate(sys.stdin.read(), args[0], args[1]))


def cmd_mark(args):
    if not args or args[0] not in APPS:
        sys.exit("usage: mark APP [SHA]")
    app = args[0]
    sha = git(app, "rev-parse", args[1] if len(args) > 1 else "HEAD").strip()
    s = load_state()
    s["reviewed"][app] = {"sha": sha, "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    save_state(s)
    print(f"{app} reviewed up to {sha[:9]}")


CMDS = {"sync": cmd_sync, "status": cmd_status, "news": cmd_news, "drift": cmd_drift,
        "classify": cmd_classify, "translate": cmd_translate, "mark": cmd_mark}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        sys.exit(__doc__)
    CMDS[sys.argv[1]](sys.argv[2:])
