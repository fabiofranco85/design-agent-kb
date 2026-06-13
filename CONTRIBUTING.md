# Contributing

Thanks for your interest. This repo is a hub-and-spoke **knowledge base** (`knowledge-base/`)
plus a Claude Code **skill** (`.claude/skills/design-systems-agent/`) for building award-winning
website design systems. A few conventions keep it coherent — please follow them.

## Ground rules

- **Versions are facts, not guesses.** Every library version, package name, and import path lives
  ONLY in `knowledge-base/_facts.md`, verified against the npm registry / official docs with a
  date. Never hardcode a version anywhere else — reference `_facts.md`. Flag anything you can't
  confirm as `UNVERIFIED — confirm before use`.
- **One owner per value.** Each canonical value (spacing scale, easing table, color tiers,
  performance budget…) lives in exactly one doc — see the ownership map in
  `knowledge-base/_conventions.md` §4. Cross-reference instead of duplicating (>10 duplicated
  lines is a review blocker).
- **Numbers, not adjectives.** Specs give concrete values (ms, ratios, px/rem, budgets), not
  vague guidance.
- **Stay within limits.** Spec docs ≤ 500 lines; the hub (`00-agent.md`) < 150 lines; the shared
  document template in `_conventions.md` §2 is mandatory for docs 01–10.

## Making a change

1. Branch off `main`.
2. Edit the relevant doc(s). If you touch a version, re-verify it live and update `_facts.md`
   (and its `last_verified`).
3. Run a consistency pass over the files you changed: internal link/anchor sweep, line-limit
   check, `python3 -m json.tool` on any `.tokens.json`, and check values against the canonical
   ones in `_conventions.md`. Append findings to `_review-report.md`.
4. Open a pull request describing what changed and why. Keep the working tree clean (no scratch
   files or editor folders).

## Re-verification cadence

Re-verify the moving targets quarterly, and before any new project — see the "most likely to go
stale" list at the bottom of the [README](README.md). Bump each touched doc's `last_verified`.

By contributing, you agree your contributions are licensed under the repo's
[MIT License](LICENSE).
