#!/usr/bin/env python3
"""Validate the design-agent-kb knowledge base, skill, and templates.

Run from anywhere: python3 scripts/validate_kb.py
Exits non-zero if any check fails. Pure standard library (no third-party deps),
so CI needs only the python3 preinstalled on the runner.

Checks:
  1. Internal markdown links/images resolve (file exists + anchor exists, GitHub slug rules).
  2. Line limits: hub 00-agent.md < 150; spec docs 01-10 <= 500.
  3. Template compliance: docs 01-10 carry all 10 required H2 sections + 3 mode H3s.
  4. design-tokens.tokens.json parses and every {alias} resolves to an in-file token.
  5. SKILL.md frontmatter is valid (allowed keys, kebab name, description <= 1024, no < >).
"""
import re, os, sys, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

failures = []
def check(name, ok, detail=""):
    print(("PASS" if ok else "FAIL") + " - " + name + ("" if ok else "  -> " + detail))
    if not ok:
        failures.append(name)

def slug(h):
    # GitHub heading anchor: lowercase, strip punctuation, spaces -> hyphens (NOT collapsed).
    s = h.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return s.replace(" ", "-")

md_files = sorted(
    f for f in glob.glob("**/*.md", recursive=True)
    if not f.startswith(".git") and "node_modules" not in f
)

heads = {}
for f in md_files:
    hs = set()
    for line in open(f, encoding="utf-8"):
        m = re.match(r"^#{1,6}\s+(.*)", line)
        if m:
            hs.add(slug(m.group(1)))
    heads[os.path.abspath(f)] = hs

# 1. link / anchor sweep (markdown links and images), skipping code fences + inline code spans
link_re = re.compile(r"\]\(([^)\s]+)\)")
broken, checked = [], 0
for f in md_files:
    base = os.path.dirname(os.path.abspath(f))
    fence = False
    for ln, line in enumerate(open(f, encoding="utf-8"), 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        clean = re.sub(r"`[^`]*`", "", line)
        for m in link_re.finditer(clean):
            t = m.group(1)
            if t.startswith(("http://", "https://", "#", "mailto:")):
                continue
            checked += 1
            path, _, anchor = t.partition("#")
            tgt = os.path.normpath(os.path.join(base, path)) if path else os.path.abspath(f)
            if path and not os.path.exists(tgt):
                broken.append(f"{f}:{ln} -> {t} (missing file)")
                continue
            if os.path.isdir(tgt):
                # A bare directory link is valid (GitHub renders the folder listing).
                # An anchored directory link must resolve to a README.md containing the anchor.
                if not anchor:
                    continue
                readme = os.path.join(tgt, "README.md")
                if not os.path.exists(readme):
                    broken.append(f"{f}:{ln} -> {t} (anchored dir without README.md)")
                    continue
                tgt = readme
            if anchor and tgt.endswith(".md") and anchor not in heads.get(os.path.abspath(tgt), set()):
                broken.append(f"{f}:{ln} -> {t} (missing anchor)")
check(f"internal links resolve ({checked} checked)", not broken, "; ".join(broken[:10]))

# 2. line limits
over = []
for f in sorted(glob.glob("knowledge-base/[0-9][0-9]-*.md")):
    n = sum(1 for _ in open(f, encoding="utf-8"))
    lim = 150 if os.path.basename(f) == "00-agent.md" else 500
    if n > lim:
        over.append(f"{f}={n}>{lim}")
check("line limits (hub<150, specs<=500)", not over, "; ".join(over))

# 3. template compliance for docs 01-10
REQUIRED_H2 = [
    "## Purpose & When To Read This", "## Core Principles", "## Decision Framework",
    "## Specifications & Parameters", "## Recommended Libraries & Tools", "## Code Examples",
    "## Mode-Specific Guidance", "## Quality Checklist", "## Anti-Patterns",
    "## Sources & Verification",
]
REQUIRED_H3 = ["### Create from scratch", "### Re-create from existing site", "### Modify an existing system"]
bad = []
for f in sorted(glob.glob("knowledge-base/*.md")):
    if not re.match(r"(0[1-9]|10)-", os.path.basename(f)):
        continue
    txt = open(f, encoding="utf-8").read()
    miss = [s for s in REQUIRED_H2 if s not in txt] + [h for h in REQUIRED_H3 if h not in txt]
    if miss:
        bad.append(f"{os.path.basename(f)}: {miss}")
check("template compliance (docs 01-10)", not bad, "; ".join(bad))

# 4. tokens JSON parses + aliases resolve
TJ = "knowledge-base/templates/design-tokens.tokens.json"
try:
    tj = json.load(open(TJ, encoding="utf-8"))
    defined, aliases = set(), []
    def walk(node, path):
        if isinstance(node, dict):
            if "$value" in node:
                defined.add(".".join(path))
            for k, v in node.items():
                if not k.startswith("$"):
                    walk(v, path + [k])
    walk(tj, [])
    def find_aliases(node):
        if isinstance(node, dict):
            for v in node.values():
                if isinstance(v, str) and v.startswith("{") and v.endswith("}"):
                    aliases.append(v.strip("{}"))
                else:
                    find_aliases(v)
        elif isinstance(node, list):
            for x in node:
                find_aliases(x)
    find_aliases(tj)
    unresolved = [a for a in aliases if a not in defined]
    check(f"tokens JSON valid + aliases resolve ({len(aliases)} aliases)", not unresolved, "; ".join(unresolved[:10]))
except Exception as e:
    check("tokens JSON valid", False, repr(e))

# 5. skill frontmatter
SK = ".claude/skills/design-systems-agent/SKILL.md"
ALLOWED = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
try:
    txt = open(SK, encoding="utf-8").read()
    fm = re.match(r"^---\n(.*?)\n---", txt, re.S)
    errs = []
    if not fm:
        errs.append("no frontmatter")
    else:
        lines = fm.group(1).split("\n")
        keys, name, desc, i = [], "", "", 0
        while i < len(lines):
            l = lines[i]
            m = re.match(r"^([A-Za-z0-9_-]+):(.*)$", l)
            if m and not l.startswith(("  ", "\t")):
                k = m.group(1); keys.append(k); v = m.group(2).strip()
                if k == "name":
                    name = v.strip('"').strip("'")
                if k == "description" and v in (">", "|", ">-", "|-"):
                    cont = []; i += 1
                    while i < len(lines) and (lines[i].startswith("  ") or lines[i].startswith("\t")):
                        cont.append(lines[i].strip()); i += 1
                    desc = " ".join(cont); continue
                elif k == "description":
                    desc = v.strip('"').strip("'")
            i += 1
        if set(keys) - ALLOWED:
            errs.append(f"disallowed keys {set(keys) - ALLOWED}")
        if not re.match(r"^[a-z0-9-]+$", name) or name.startswith("-") or name.endswith("-") or "--" in name:
            errs.append(f"bad name {name!r}")
        if not desc:
            errs.append("empty description")
        if "<" in desc or ">" in desc:
            errs.append("description has angle brackets")
        if len(desc) > 1024:
            errs.append(f"description too long ({len(desc)})")
    check("skill frontmatter valid", not errs, "; ".join(errs))
except FileNotFoundError:
    check("skill frontmatter valid", False, f"{SK} not found")

print("\n" + ("ALL CHECKS PASSED" if not failures else f"{len(failures)} CHECK(S) FAILED: {failures}"))
sys.exit(1 if failures else 0)
