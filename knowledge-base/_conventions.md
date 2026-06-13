# _conventions.md — Shared Template, Glossary & Authoring Rules

> **BINDING for every document in this knowledge base.** Writers MUST read this file and
> `_facts.md` before writing a single line. Deviations are reviewer BLOCKERs.

---

## 1. Authoring Rules (non-negotiable)

1. **Numbers, not adjectives.** Every spec gives concrete values: exact easing curves,
   duration ranges in ms, ratios, px/rem scales, numeric budgets, parameter values.
   "Fast" is a defect; "150–250 ms" is a spec.
2. **Library versions come ONLY from `_facts.md`.** Never re-research or guess a version,
   package name, install command, or import path. If `_facts.md` lacks a library you need,
   write `UNVERIFIED — confirm before use` next to it and flag it in your completion report.
3. **UNVERIFIED flag syntax:** append the literal string `UNVERIFIED — confirm before use`
   immediately after any claim you could not confirm against a source.
4. **Line limit:** every spec doc (01–10) ≤ **500 lines**. The hub (00-agent.md) < **150 lines**.
   Templates have no hard limit but must stay skeletal.
5. **Write ONLY your assigned file(s).** Never touch another writer's file.
6. **Sources & Verification** section is mandatory. Entry format:
   `- https://example.com/page — confirmed: <specific fact> (verified 2026-06-12)`
7. **Code examples** must use current APIs per `_facts.md`, be copy-pasteable, and comment
   the key parameters.
8. **Reduced motion is not optional.** Any doc that specifies motion MUST include the
   `prefers-reduced-motion` handling for it (owner of the canonical pattern: doc 07).

---

## 2. Shared Document Template (docs 01–10)

Every spec document MUST follow this identical structure, in this order:

```markdown
---
title: <doc title>
doc_id: <e.g. 04-typography>
version: 1.0
last_verified: 2026-06-12
applies_to_modes: [create, recreate, modify]
---

## Purpose & When To Read This
(2–4 sentences: the exact situations in which the agent should open this doc — written as a routing selector.)

## Core Principles
(The non-negotiable rules / philosophy for this domain at award-winning level.)

## Decision Framework
(A decision tree or checklist the agent applies to choose an approach. Use IF/THEN logic.)

## Specifications & Parameters
(The detailist heart: exact values, scales, ranges, tokens, tables.)

## Recommended Libraries & Tools
(Mapped to use-cases, WITH VERIFIED current versions + install commands + import paths — sourced from _facts.md.)

## Code Examples
(Minimal, correct, copy-pasteable, current-API snippets. Comment the key params.)

## Mode-Specific Guidance
### Create from scratch
### Re-create from existing site (reverse-engineering)
### Modify an existing system

## Quality Checklist
(A pass/fail checklist the agent runs before declaring this domain "done".)

## Anti-Patterns
(Specific mistakes that get a site rejected from awards / hurt UX or performance.)

## Sources & Verification
(URLs + the fact each confirmed + date.)
```

Frontmatter is YAML, all five keys required. `applies_to_modes` lists only the modes the
doc serves (most docs serve all three).

---

## 3. Glossary & Canonical Values

### 3.1 The three agent modes (exact names, lowercase, everywhere)

| Mode | Meaning |
|---|---|
| `create` | Create a design system/spec from scratch from a brief |
| `recreate` | Reverse-engineer a design system/spec from an existing live website |
| `modify` | Modify/extend an existing design system while preserving consistency |

### 3.2 Motion personalities (owner: doc 01; easing detail: doc 07)

| Personality | Default duration band | Default eases (GSAP names) |
|---|---|---|
| `snappy` | 150–350 ms | `expo.out`, `power3.out` |
| `fluid` | 400–800 ms | `power2.inOut`, `power3.out` |
| `cinematic` | 600–1200 ms | `power4.inOut`, `expo.inOut` |

### 3.3 Duration classes (owner: doc 07)

| Class | Range |
|---|---|
| micro-interaction | 100–200 ms |
| UI transition | 200–400 ms |
| content/section reveal | 400–700 ms |
| hero / cinematic | 600–1200 ms |

### 3.4 Canonical easing vocabulary (owner: doc 07 — others reference, never redefine)

GSAP names are canonical; CSS `cubic-bezier()` values are the standard approximations:

| GSAP name | CSS approximation |
|---|---|
| `power2.out` | `cubic-bezier(0.215, 0.61, 0.355, 1)` |
| `power2.inOut` | `cubic-bezier(0.645, 0.045, 0.355, 1)` |
| `power3.out` | `cubic-bezier(0.165, 0.84, 0.44, 1)` |
| `power4.out` | `cubic-bezier(0.23, 1, 0.32, 1)` |
| `power4.inOut` | `cubic-bezier(0.86, 0, 0.07, 1)` |
| `expo.out` | `cubic-bezier(0.19, 1, 0.22, 1)` |
| `expo.inOut` | `cubic-bezier(1, 0, 0, 1)` |

### 3.5 Spacing scale (owner: doc 06 — 05/templates must use these exact tokens)

Base unit **8 px** with a 4 px half-step. Token name = `space.{n}` where `n = px ÷ 4`:

`space.1`=4, `space.2`=8, `space.3`=12, `space.4`=16, `space.6`=24, `space.8`=32,
`space.12`=48, `space.16`=64, `space.24`=96, `space.32`=128 (px).

### 3.6 Type scale (owner: doc 04)

Named ratios: Minor Third = **1.2**, Major Third = **1.25**, Perfect Fourth = **1.333**,
Golden = **1.618**. Default recommendation: 1.2–1.333 for UI; body floor **16 px**.

### 3.7 Design-token naming (owner: doc 05 for color; doc 06 for dimension)

- Format: W3C DTCG (`$type` / `$value`), file extension `.tokens.json`.
- **Canonical version string (use verbatim; do not re-phrase):** long form
  **"W3C Design Tokens (DTCG) Format Module 2025.10"**, short form **"DTCG 2025.10"**.
  Use the long form in artifact `$description` fields; the short form inline in prose
  (version facts: `_facts.md` §3).
- Three tiers: **primitive** (`color.blue.500`, `space.4`) → **semantic**
  (`color.bg.primary`, `color.text.primary`, `space.section`) → **component**
  (`button.bg`, `card.padding`).
- Alias syntax: `"{color.blue.500}"`. Multiword segments are kebab-case (`color.bg.on-brand`).

### 3.8 Performance budget anchors (owner: doc 09 — 08 references)

LCP < 2.5 s, INP < 200 ms, CLS < 0.1 (all at p75 of real-user loads); WebGL scenes
target < 100 draw calls (hard ceiling 150). Doc 09 owns the full budget table.

### 3.9 Accessibility anchors (owner: doc 05 for contrast; doc 09 for the rest)

WCAG 2.x AA: contrast ≥ 4.5:1 body text, ≥ 3:1 large text (≥ 24 px / 18.66 px bold) and
UI components/graphics.

---

## 4. Content Ownership (anti-duplication map)

A value lives in exactly ONE doc; everyone else cross-references it. Duplicating > 10
lines of another doc's content is a reviewer MAJOR.

| Canonical content | Owner |
|---|---|
| Library versions / install / import paths | `_facts.md` |
| Visual archetypes, motion-personality framework | `01-visual-motion.md` |
| AI image prompting, asset treatment & export specs | `02-image-generation.md` |
| Grid systems, breakpoints, composition rules | `03-layout.md` |
| Type scales, fluid type clamp() recipes, SplitText reveal recipe | `04-typography.md` |
| Color tokens, OKLCH palette, contrast verification, theming | `05-color.md` |
| Spacing scale, rhythm, fluid spacing | `06-spacing.md` |
| Easing table, duration classes, Lenis setup, reduced-motion pattern, page transitions | `07-animation-choreography.md` |
| WebGL decision framework, shader catalog, GPU perf rules | `08-webgl-effects.md` |
| Stack selection, perf budget table, asset pipeline commands, a11y practices, sound | `09-tech-implementation.md` |
| Mode playbooks, output artifact schemas | `10-modes-and-artifacts.md` |
| Artifact skeletons | `templates/` |

---

## 5. Cross-Reference Syntax

- Relative links from a spec doc: `[easing table](./07-animation-choreography.md#specifications--parameters)`
- From inside `templates/`: `[spacing scale](../06-spacing.md#specifications--parameters)`
- Anchors are GitHub-slugified headings: lowercase, spaces → `-`, `&` and other
  punctuation dropped (e.g. `## Purpose & When To Read This` → `#purpose--when-to-read-this`,
  `## Specifications & Parameters` → `#specifications--parameters`).
- Link only to files and headings that exist. The reviewer verifies every link.

---

## 6. Writer Completion Report (return this, nothing more)

```
file: <path>
lines: <count>
sources: <count>
unverified: <list or "none">
cross-doc assumptions: <list or "none">
```
