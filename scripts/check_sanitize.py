#!/usr/bin/env python3
"""Sanitize guard for 7kolor repos.

Rules format (plain text, one per line):
    # comment
    ! <regex>   -> forbid: any hit fails the check
    ? <regex>   -> warn:   printed, does not fail

Rules source priority:
    1. --rules PATH
    2. env SANITIZE_RULES_B64 (base64 of the rules text, used in CI via repo secret)
    3. env SANITIZE_RULES_FILE

Usage:
    check_sanitize.py [--staged] [--all] [--history] [--rules PATH] [--strict]
"""
import argparse, base64, os, re, subprocess, sys, tempfile

ALLOWED_EMAIL_SUFFIXES = ("@users.noreply.github.com", "@7kolor.com")
EMAIL_RE = re.compile(r"[\w.+\-]+@[\w\-]+(?:\.[\w\-]+)+")
ID_RE = re.compile(rb"^[\w.+\-]+@[\w\-]+(?:\.[\w\-]+)+$")


def load_rules(args):
    text = None
    if args.rules and os.path.exists(args.rules):
        text = open(args.rules, encoding="utf-8").read()
    elif os.environ.get("SANITIZE_RULES_B64"):
        text = base64.b64decode(os.environ["SANITIZE_RULES_B64"]).decode("utf-8")
    elif os.environ.get("SANITIZE_RULES_FILE"):
        text = open(os.environ["SANITIZE_RULES_FILE"], encoding="utf-8").read()
    if text is None:
        print("FATAL: no sanitize rules provided (--rules / SANITIZE_RULES_B64)", file=sys.stderr)
        sys.exit(2)
    forbid, warn = [], []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("!"):
            forbid.append(line[1:].strip())
        elif line.startswith("?"):
            warn.append(line[1:].strip())
    return [re.compile(p) for p in forbid], [re.compile(p) for p in warn], forbid


def git(*argv):
    return subprocess.run(["git", *argv], capture_output=True, text=True).stdout


def target_files(staged):
    if staged:
        out = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    else:
        out = git("ls-files")
    return [f for f in out.splitlines() if f and os.path.isfile(f)]


def scan_text(name, content, forbid, warn, hits, warns):
    for m in EMAIL_RE.finditer(content):
        if not m.group(0).endswith(ALLOWED_EMAIL_SUFFIXES):
            hits.append(f"{name}: disallowed email: {m.group(0)}")
    for p in forbid:
        for m in p.finditer(content):
            hits.append(f"{name}: forbid pattern {p.pattern!r} -> ...{m.group(0)[:40]}...")
    for p in warn:
        for m in p.finditer(content):
            warns.append(f"{name}: warn pattern {p.pattern!r} -> ...{m.group(0)[:40]}...")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--staged", action="store_true", help="scan staged files only")
    ap.add_argument("--all", action="store_true", help="scan all tracked files (default)")
    ap.add_argument("--history", action="store_true", help="also scan full git history")
    ap.add_argument("--rules")
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    args = ap.parse_args()

    forbid, warn, forbid_raw = load_rules(args)
    hits, warns = [], []

    for f in target_files(args.staged):
        try:
            content = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        scan_text(f, content, forbid, warn, hits, warns)

    if args.history:
        # author/committer identities in history
        ids = set(git("log", "--all", "--format=%ae%n%ce").split())
        for e in ids:
            if e and not ID_RE.match(e.encode()):
                continue
            if e and not e.endswith(ALLOWED_EMAIL_SUFFIXES):
                hits.append(f"history: disallowed committer/author email: {e}")
        # commit messages
        scan_text("commit-messages", git("log", "--all", "--format=%B"), forbid, warn, hits, warns)
        # blob content across all revisions (fast C-side grep, forbid rules only)
        revs = git("rev-list", "--all").split()
        if revs:
            with tempfile.NamedTemporaryFile("w", suffix=".pat", delete=False) as tf:
                for p in forbid_raw:
                    tf.write(re.sub(r"\(\?i\)", "", p) + "\n")
                patfile = tf.name
            r = subprocess.run(["git", "grep", "-i", "-E", "-n", "-I", "-f", patfile, *revs],
                               capture_output=True, text=True)
            os.unlink(patfile)
            if r.returncode == 0:
                hits.append("history: forbid pattern found in blob content:\n" + r.stdout[:2000])
            elif r.returncode not in (0, 1):
                print(r.stderr, file=sys.stderr)

    for w in warns:
        print("WARN ", w)
    if hits:
        for h in hits:
            print("FAIL ", h, file=sys.stderr)
        sys.exit(1)
    if args.strict and warns:
        sys.exit(1)
    print(f"OK: {len(hits)} violations, {len(warns)} warnings")


if __name__ == "__main__":
    main()
