---
title: Spacing — Scale, Rhythm, Fluid Space & Whitespace Systems
doc_id: 06-spacing
version: 1.0
last_verified: 2026-06-12
applies_to_modes: [create, recreate, modify]
---

## Purpose & When To Read This

Open this doc whenever you set, audit, or reverse-engineer ANY margin, padding, or gap:
defining the spacing token scale, computing fluid spacing `clamp()` values, establishing
vertical rhythm between text blocks, choosing whitespace density, or deciding when and how
to break the grid for editorial impact. This doc OWNS the canonical `space.{n}` scale, the
`dimension` token definitions, and the rhythm-break rules referenced by
[03-layout](./03-layout.md#specifications--parameters).

## Core Principles

1. **One scale, zero exceptions.** Every margin, padding, and gap is a `space.{n}` token,
   a token-endpoint `clamp()`, or an `em` multiple of the rhythm unit. A raw `17px` is a defect.
2. **Spacing IS hierarchy.** Gestalt proximity quantified: space *between* groups ≥ 2×
   space *within* groups. If section gap == card gap, the page has no structure.
3. **Generosity reads as quality.** When a measured value falls between tokens, snap UP.
   Award-level sites are whitespace-rich (hero negative-space minimums are owned by
   [03-layout](./03-layout.md#specifications--parameters)).
4. **Rhythm derives from type.** The rhythm unit = the body line box: 16 px × 1.5
   line-height = **24 px = `space.6`**. Block spacing in prose is a multiple of it
   (0.5 / 1 / 2 / 4 units = 12 / 24 / 48 / 96 px = `space.3/6/12/24`). Type scale itself is
   owned by [04-typography](./04-typography.md#specifications--parameters).
5. **Fluid between breakpoints, never stepped.** Macro spacing (sections, margins,
   gutters) interpolates with `clamp()`; micro spacing (inside components) stays static.
   Never let spacing grow unbounded with bare `vw`.
6. **Break the grid deliberately, recover immediately.** A spacing break is an editorial
   accent with preconditions and a frequency cap — never a default, never an accident.

## Decision Framework

Apply top-down to every spacing decision:

1. **IF** spacing is *inside* a component (icon↔label, input padding, chip gap)
   **THEN** use `space.1`–`space.4` (4–16 px), static (no clamp).
2. **IF** spacing separates *related elements within a block* (form rows, card internals,
   list items) **THEN** use `space.4`–`space.6` (16–24 px), static.
3. **IF** spacing separates *blocks within a section* (heading↔body, card grid gaps,
   figure margins) **THEN** use `space.6`–`space.12` (24–48 px); fluid only if the block
   is a full-width editorial unit.
4. **IF** spacing separates *sections* or sets page margins/gutters **THEN** use
   `space.16`–`space.32` (64–128 px) as fluid `clamp()` with token endpoints (§ fluid spacing).
5. **IF** the element scales with its *container*, not the viewport **THEN** use `cqi`
   units inside clamp — container-query strategy owned by
   [03-layout](./03-layout.md#specifications--parameters).
6. **IF** spacing sits between text blocks in long-form prose **THEN** use the rhythm
   system (`em`-based flow spacing) instead of fixed tokens (§ vertical rhythm).
7. **IF** a measured/desired value is off-scale **THEN** snap to the nearest token
   (ties snap up). Only break the scale when ALL preconditions in § breaking the grid hold.
8. **IF** in `recreate` mode and an off-scale value repeats ≥ 3 times across the source
   site **THEN** it is an intentional scale step — record it as a project-specific token,
   do not "correct" it.

## Specifications & Parameters

### The canonical spacing scale (owner: this doc — pinned in `_conventions.md` §3.5)

Base unit **8 px**, half-step **4 px**. Token name `space.{n}` where **n = px ÷ 4**.

| Token | px | rem (÷16) | Step logic | Primary use |
|---|---|---|---|---|
| `space.1` | 4 | 0.25 | linear +4 | hairline gaps, icon↔text |
| `space.2` | 8 | 0.5 | linear +4 | tight padding, chip/badge internals |
| `space.3` | 12 | 0.75 | linear +4 | input padding, heading→content (½ rhythm) |
| `space.4` | 16 | 1 | linear +4 (last) | default component padding, min gutter |
| `space.6` | 24 | 1.5 | ×1.5 | rhythm unit, card padding, paragraph gap |
| `space.8` | 32 | 2 | ×1.333 | block gaps, max gutter |
| `space.12` | 48 | 3 | ×1.5 | sub-section gaps, heading isolation (2 rhythm) |
| `space.16` | 64 | 4 | ×1.333 | min section padding |
| `space.24` | 96 | 6 | ×1.5 | large section padding, outer margins (4 rhythm) |
| `space.32` | 128 | 8 | ×1.333 | max section padding, hero breathing room |

**Step logic, documented:** below 16 px the scale is linear (+4) because component-internal
spacing needs fine control; from 16 px up it is two interleaved doubling series —
{16, 32, 64, 128} and {24, 48, 96} — so consecutive ratios alternate ×1.5 / ×1.333 and
every value doubles two steps later. This matches the field-tested Utopia finding: more
nuance near the base size, fewer options at the large end. Deliberately ABSENT: 20, 28,
40, 56, 72, 80, 112 px — gaps force visible contrast between steps. `0` is written
literally, never tokenized. Comparative grounding: Primer uses the same 4 px base and
2–128 px range; Polaris names tokens as percentage multiples of a 4 px base
(`space-100` = 4 px); Material's spacing follows an 8 dp scale with type/iconography on a
4 dp grid — the industry consensus this scale formalizes.

### Token → CSS custom property transform (BINDING — doc 03's grid code depends on it)

Join token path segments with hyphens and prefix `--` (dots → hyphens):

| Token path | CSS custom property |
|---|---|
| `space.4` | `--space-4` |
| `space.32` | `--space-32` |
| `space.section` (semantic) | `--space-section` |
| `card.padding` (component) | `--card-padding` |

Primitives are authored and emitted in **px** (the clamp math below assumes px). The
12-column grid in [03-layout](./03-layout.md#code-examples) consumes exactly these
`--space-{n}` names — never rename or re-derive them.

### Three token tiers (naming pinned in `_conventions.md` §3.7)

- **Primitive:** `space.1` … `space.32` — the table above. Never used directly in
  component CSS; always routed through a semantic or component token.
- **Semantic:** `space.rhythm` = `{space.6}` · `space.gutter` (fluid, 16→32 px) ·
  `space.section` (fluid, 64→128 px) · `space.margin` (fluid, 24→96 px).
- **Component:** `card.padding` = `{space.6}` · `button.padding-x` = `{space.4}` ·
  `button.padding-y` = `{space.2}` · `input.padding` = `{space.3}`.

### Vertical rhythm (ties spacing to the type scale)

The type scale (ratios 1.2–1.333, body floor 16 px) is owned by
[04-typography](./04-typography.md#specifications--parameters); rhythm is owned here.

- **Rhythm unit** = body line box = 16 px × 1.5 = **24 px** (`space.6`). The rhythm
  sub-series inside the scale is `space.3 / 6 / 12 / 24` = 0.5 / 1 / 2 / 4 units.
- **Web-pragmatic, not print-strict:** do NOT force every baseline onto a grid with fixed
  px line-heights — doc 04 bans `line-height: 24px` (breaks WCAG 1.4.12 text-spacing
  overrides). Rhythm lives in the *margins between blocks*, set in whole/half units.
- **Prose block spacing table (at the 16 px body floor):**

| Boundary | Value | Units |
|---|---|---|
| paragraph → paragraph | `space.6` (24 px) | 1 |
| any block → heading | `space.12` (48 px) | 2 |
| heading → its content | `space.3` (12 px) | 0.5 |
| figure / blockquote isolation | `space.12` (48 px) | 2 |
| prose end → next section | `space.16+` (fluid) | macro |

  The 48/12 split around headings yields a 4:1 above:below ratio — the heading visibly
  belongs to what follows (proximity rule from Core Principle 2).
- **Fluid type caveat:** when body size is fluid (doc 04), px tokens stop tracking the
  line box. In long-form prose use `em` flow spacing instead — `1.5em` = 1 rhythm unit at
  any font size (Code Example C). Token-based rhythm is for UI surfaces; `em`-based
  rhythm is for articles/editorial copy.
- **Single-direction margins only:** space flows downward via `margin-block-start` on the
  *following* element (owl selector). Never set both block margins on prose elements —
  collapsing margins make rhythm unpredictable.

### Fluid spacing with clamp() (the formula — show your math)

A value scaling linearly from `s1` px at viewport `v1` px to `s2` px at viewport `v2` px:

```
slope     = (s2 − s1) / (v2 − v1)            → preferred-value vw coefficient = slope × 100
intercept = s1 − slope × v1                  → px offset (may be negative or 0)
result    = clamp(s1px, {slope×100}vw + {intercept}px, s2px)
```

`clamp(MIN, VAL, MAX)` resolves as `max(MIN, min(VAL, MAX))`; arithmetic is allowed
directly inside without `calc()` (spaces required around `+`/`−`). Baseline: widely
available since July 2020 — no fallback needed.

**Rules:** both endpoints MUST be `space.{n}` tokens (as `var(--space-{n})`); verify the
math at BOTH endpoints; pick the fluid range per property (it need not equal the
breakpoint range — doc 03's canonical recipes use 640→1920 for gutters, 800→2000 for
margins, 800→1600 for sections).

**Canonical worked recipes** (consumed by [03-layout](./03-layout.md#specifications--parameters)):

| Property | Endpoints | Range | Math | Result |
|---|---|---|---|---|
| gutter | `space.4`→`space.8` (16→32) | 640→1920 | slope 16/1280 = 0.0125 → 1.25vw; intercept 16 − 8 = 8px | `clamp(var(--space-4), 1.25vw + 8px, var(--space-8))` |
| outer margin | `space.6`→`space.24` (24→96) | 800→2000 | slope 72/1200 = 0.06 → 6vw; intercept 24 − 48 = −24px | `clamp(var(--space-6), 6vw - 24px, var(--space-24))` |
| section padding | `space.16`→`space.32` (64→128) | 800→1600 | slope 64/800 = 0.08 → 8vw; intercept 64 − 64 = 0 | `clamp(var(--space-16), 8vw, var(--space-32))` |
| block gap | `space.8`→`space.12` (32→48) | 640→1920 | slope 16/1280 → 1.25vw; intercept 32 − 8 = 24px | `clamp(var(--space-8), 1.25vw + 24px, var(--space-12))` |

Utopia-style rem alternative (their generator output, 18→40 px across a 360→1240 viewport):
`--space-s-l: clamp(1.125rem, 0.5625rem + 2.5vw, 2.5rem)` — Utopia's "one-up pairs" jump
one t-shirt size (s→m); steeper custom pairs (s→l above) suit hero slats. Use the Utopia
space calculator to cross-check any hand-derived clamp.

### Whitespace density bands

| Band | Scope | Tokens | Behavior |
|---|---|---|---|
| micro | inside components | `space.1`–`space.4` | static |
| meso | blocks within a section | `space.6`–`space.12` | static or gently fluid |
| macro | between sections, page margins | `space.16`–`space.32` | always fluid |

- **Proximity ratio:** adjacent bands separated by ≥ 2× (e.g. within-card `space.4` →
  between-cards ≥ `space.8`). Adjacent steps used together should differ by ≥ 1.5×.
- **Density modes:** data-dense UI (dashboards) may shift micro/meso one step DOWN;
  editorial/portfolio pages shift macro one step UP. Shift bands, never single values —
  hierarchy ratios must survive the shift.

### Breaking the grid for editorial impact (owner: this doc — doc 03 links here)

Award-level sites violate their own spacing system on purpose. The deviation only reads
as intentional when the system is established first.

**WHEN (all preconditions must hold):**
1. The base rhythm is visible first: ≥ 2 consecutive on-scale sections before the first break.
2. Frequency cap: **≤ 1 compositional break per viewport-height** (cap shared with
   [03-layout](./03-layout.md#specifications--parameters)) and **3–5 breaks per page max**.
3. The break marks genuine editorial emphasis: hero, pull quote, featured work,
   section transition, final CTA — nothing else.
4. NEVER inside functional UI: forms, navigation, card collections, tables, checkout.
5. Never two consecutive broken sections — the section after a break returns to scale.

**HOW (pick exactly one move per break):**
- **Exaggeration:** jump ≥ 2 scale steps beyond context, or exceed the scale with a
  simple multiple of `space.32` — 192 px (×1.5) or 256 px (×2). Off-scale values must
  still sit on the 4 px sub-grid.
- **Compression shock:** collapse a normally `space.16+` section boundary to `space.1`
  or 0 (full-bleed image butted against the next section), then over-recover with
  ≥ `space.24` after.
- **Asymmetric block padding:** `padding-block-start: var(--space-32)` with
  `padding-block-end: var(--space-12)` (ratio ≥ 2.5:1) creates forward pull into the
  next section.
- **Overlap via negative tokens:** `margin-block-start: calc(-1 * var(--space-16))` to
  `calc(-1 * var(--space-24))` — exact overlap composition values and counterweight
  rules are owned by [03-layout](./03-layout.md#specifications--parameters).
- **Inside a broken section, internal spacing stays canonical.** Only the section's
  outer relationship breaks; headings/body within keep token rhythm.

## Recommended Libraries & Tools

Spacing needs **no runtime library** — it ships as pure CSS custom properties generated
from the token file.

| Use case | Tool | Version / install |
|---|---|---|
| Token format | W3C DTCG Format Module **2025.10** (first stable version; a Final Community Group Report, not a W3C Standard) — per `_facts.md`. Files: `.tokens` / `.tokens.json`; MIME `application/design-tokens+json` | spec, no install |
| Fluid clamp generation & cross-check | Utopia fluid space calculator — https://utopia.fyi/space/calculator/ | web tool, no install |
| DTCG → CSS variable build | Style Dictionary (token transform pipeline) | version UNVERIFIED — confirm before use (not in `_facts.md`) |

## Code Examples

### A — `space.tokens.json` (DTCG 2025.10, `$type: dimension`)

```json
{
  "space": {
    "$type": "dimension",
    "$description": "Primitive spacing. n = px / 4. Base-8, 4px half-steps below 16px.",
    "1":  { "$value": { "value": 4,   "unit": "px" } },
    "2":  { "$value": { "value": 8,   "unit": "px" } },
    "3":  { "$value": { "value": 12,  "unit": "px" } },
    "4":  { "$value": { "value": 16,  "unit": "px" } },
    "6":  { "$value": { "value": 24,  "unit": "px" } },
    "8":  { "$value": { "value": 32,  "unit": "px" } },
    "12": { "$value": { "value": 48,  "unit": "px" } },
    "16": { "$value": { "value": 64,  "unit": "px" } },
    "24": { "$value": { "value": 96,  "unit": "px" } },
    "32": { "$value": { "value": 128, "unit": "px" } },

    "rhythm":  { "$value": "{space.6}",  "$description": "1 rhythm unit = body line box (16px x 1.5)." },
    "section": {
      "$value": "{space.16}",
      "$description": "Min section padding; fluid max via $extensions, built into clamp() at compile time.",
      "$extensions": {
        "agent.fluid": { "max": "{space.32}", "viewportRange": [800, 1600] }
      }
    }
  },
  "card":   { "$type": "dimension", "padding":   { "$value": "{space.6}" } },
  "button": {
    "$type": "dimension",
    "padding-x": { "$value": "{space.4}" },
    "padding-y": { "$value": "{space.2}" }
  }
}
```

Key DTCG rules applied: `$value` is an object `{ value, unit }`; only `"px"` and `"rem"`
units exist; the unit is required even when value is 0; `$type` on a group is inherited
by all child tokens; names must not contain `.`, `{`, `}` or start with `$` (which is why
`space.6` is group `space` → token `6`); alias syntax `"{space.6}"`. `clamp()` is NOT
representable as a `dimension` — store endpoints as tokens and fluid metadata in
`$extensions`; the build step composes the clamp. Color tokens live in
[05-color](./05-color.md#specifications--parameters), never in this file.

### B — Generated CSS custom properties (the dots → hyphens transform)

```css
/* GENERATED from space.tokens.json — token path "space.4" → --space-4 */
:root {
  --space-1: 4px;   --space-2: 8px;    --space-3: 12px;  --space-4: 16px;
  --space-6: 24px;  --space-8: 32px;   --space-12: 48px; --space-16: 64px;
  --space-24: 96px; --space-32: 128px;

  /* semantic — fluid values composed at build time, endpoints are tokens */
  --space-rhythm:  var(--space-6);
  --space-gutter:  clamp(var(--space-4), 1.25vw + 8px, var(--space-8));  /* 16px@640 → 32px@1920 */
  --space-margin:  clamp(var(--space-6), 6vw - 24px, var(--space-24));   /* 24px@800 → 96px@2000 */
  --space-section: clamp(var(--space-16), 8vw, var(--space-32));         /* 64px@800 → 128px@1600 */

  /* component */
  --card-padding: var(--space-6);
  --button-padding-x: var(--space-4);
  --button-padding-y: var(--space-2);
}

section { padding-block: var(--space-section); }
```

### C — Rhythm: single-direction flow spacing (owl selector)

```css
/* UI surfaces: token-based rhythm (body locked at 16px floor) */
.flow > * + * { margin-block-start: var(--flow-space, var(--space-6)); } /* 1 unit */
.flow :is(h2, h3) { --flow-space: var(--space-12); }       /* 2 units before a heading */
.flow :is(h2, h3) + * { --flow-space: var(--space-3); }    /* 0.5 unit after — 4:1 ratio */

/* Long-form prose with FLUID type: em-based so rhythm tracks the local font size */
.prose { line-height: 1.5; }                  /* unitless — never px (see doc 04) */
.prose > * + * { margin-block-start: 1.5em; } /* 1.5em = exactly 1 line box at any size */
.prose :is(h2, h3) { margin-block-start: 2em; margin-block-end: 0; }
.prose :is(h2, h3) + * { margin-block-start: 0.75em; }
```

### D — Deriving a new fluid value (the math, inline)

```css
/* Goal: hero top padding space.16 → space.32 (64 → 128px) across 360 → 1440px.
   slope     = (128 − 64) / (1440 − 360) = 64 / 1080 = 0.059259  → 5.9259vw
   intercept = 64 − 0.059259 × 360      = 64 − 21.333 = 42.667px → 2.6667rem
   check: @360 → 21.33 + 42.67 = 64 ✓   @1440 → 85.33 + 42.67 = 128 ✓        */
.hero { padding-block-start: clamp(var(--space-16), 5.9259vw + 42.667px, var(--space-32)); }
```

## Mode-Specific Guidance

### Create from scratch
1. Adopt the canonical scale verbatim unless the brief demands otherwise; if the type
   scale changes the body line box (e.g. 18 px body), recompute the rhythm unit
   (18 × 1.5 = 27 → snap line-height to 1.556 so the line box lands on 28 px, the 4 px
   sub-grid) and document the deviation.
2. Emit Code Examples A + B before any component work — doc 03's grid consumes
   `--space-{n}` on day one.
3. Define the three fluid semantic recipes (gutter / margin / section) with ranges chosen
   from the project's min/max breakpoints
   ([03-layout](./03-layout.md#specifications--parameters)).
4. Mark planned grid-breaks in the page spec (which section, which move, recovery section).

### Re-create from existing site (reverse-engineering)
1. Sample computed `margin`/`padding`/`gap` (DevTools, not authored CSS) at 375 / 768 /
   1440 — the widths doc 03 uses for layout sampling.
2. Cluster the values. Snap each cluster to the nearest token (±2 px tolerance, ties up).
   Off-scale values repeating ≥ 3× = intentional steps — record as project tokens.
3. Values that *change continuously* across the three widths are fluid. Reconstruct the
   clamp from two samples: `slope = (b − a) / (v2 − v1)`, `intercept = a − slope × v1`,
   then express endpoints as the snapped tokens.
4. Log every section boundary larger/smaller than its neighbors by ≥ 2 steps as a
   deliberate grid-break; reproduce it with the matching move from § breaking the grid.

### Modify an existing system
1. NEVER renumber or re-value existing `space.{n}` tokens — doc 03's grid code and every
   component reference them. Extend only with new `n` where `n = px ÷ 4` is an integer.
2. Deprecate by aliasing the old token to a new one (DTCG alias), not by deletion.
3. Changing the emission unit (px → rem) is a breaking change to every clamp intercept —
   recompute all fluid recipes or do not do it.
4. Adding a density mode = shifting whole bands (§ whitespace density), never editing
   individual component values.

## Quality Checklist

- [ ] Every margin/padding/gap is a token, a token-endpoint clamp, or an `em` rhythm
      multiple — zero raw px values in authored CSS (grep for `[0-9]px` outside the
      generated `:root` block and clamp offsets).
- [ ] All clamp() values verified at BOTH endpoints with the slope/intercept math shown
      in a comment.
- [ ] Computed spacing at min and max viewport lands on the 4 px sub-grid.
- [ ] Proximity ratio ≥ 2:1 between every group boundary vs its within-group spacing.
- [ ] Prose rhythm: block margins are 0.5/1/2/4-unit multiples (or `em` equivalents);
      line-height unitless; no fixed-px line-height anywhere.
- [ ] Layout survives 200% zoom and WCAG 1.4.12 text-spacing overrides (line-height 1.5×,
      paragraph 2×) without overlap — overrides owned by
      [04-typography](./04-typography.md#quality-checklist).
- [ ] Grid-breaks: ≤ 1 per viewport-height, 3–5 per page, all preconditions logged,
      recovery section on-scale.
- [ ] `space.tokens.json` validates against DTCG 2025.10: `dimension` type, `{value, unit}`
      objects, px/rem only, unit present at 0, no `.`/`{`/`}` in names.
- [ ] CSS variables match the transform exactly: `space.{n}` → `--space-{n}`.

## Anti-Patterns

- **Off-grid noise:** 17 px, 23 px, 35 px values scattered per-component — the #1 sign of
  an unsystematized site; reviewers and award juries read it as sloppiness.
- **A 13-step scale with 2 px deltas.** No perceptible contrast between steps means no
  hierarchy; the deliberate gaps in the canonical scale are the feature.
- **Equal spacing everywhere** (section gap == card gap == paragraph gap): proximity
  ratio 1:1 destroys grouping; the page becomes a uniform gray of boxes.
- **Bare `vw` spacing without clamp** — unbounded growth on ultrawide screens; also
  banned by doc 03 for layout dimensions.
- **Fixed px line-height to chase a print baseline grid** — breaks WCAG 1.4.12 overrides
  and fluid type; rhythm belongs in block margins, not the line box.
- **Both block margins set on prose elements** — margin collapse makes rhythm
  unpredictable; use single-direction flow (Code Example C).
- **Spacer `<div>`s or stacked `<br>`** instead of margin/gap tokens.
- **Hardcoding `clamp()` strings inside `.tokens.json`** — `dimension` cannot hold a CSS
  function; store endpoints + `$extensions` metadata, compose at build time.
- **Breaking the grid in functional UI** or more than once per viewport-height — chaos,
  not editorial confidence; juries can tell an unestablished grid from a broken one.
- **Renaming `--space-{n}` variables** in a modify pass — silently severs doc 03's grid
  code and every component token.

## Sources & Verification

- https://www.designtokens.org/TR/2025.10/format/ — confirmed: `dimension` `$value` is an
  object `{value, unit}` with units limited to `px`/`rem`; unit required even when value
  is 0; group-level `$type` is inherited by child tokens; token/group names must not
  contain `.`, `{`, `}` or begin with `$`; alias syntax `"{group.token}"` (verified 2026-06-12)
- https://utopia.fyi/space/calculator/ — confirmed: t-shirt-size fluid space scale
  (3xs–3xl), one-up "space value pairs", and generator output format
  `--space-s-l: clamp(1.125rem, 0.5625rem + 2.5vw, 2.5rem)` (verified 2026-06-12)
- https://utopia.fyi/blog/designing-with-a-fluid-space-palette/ — confirmed: multipliers
  derived from a type-scale base with 0.25 increments near the base and whole-number
  increments at the large end ("more nuanced space options nearer the base font size,
  fewer options at the larger end"); custom and reverse pairs (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/CSS/clamp — confirmed: `clamp(MIN, VAL, MAX)`
  resolves as `max(MIN, min(VAL, MAX))`; direct `+ − × ÷` allowed inside without `calc()`;
  Baseline widely available since July 2020 (verified 2026-06-12)
- https://primer.style/foundations/primitives/size — confirmed: Primer base unit 4 px
  (0.25 rem), scale 2–128 px via `--base-size-{px}` tokens, incl. 4/8/16/24/32/48/128
  (verified 2026-06-12)
- https://polaris-react.shopify.com/tokens/space — confirmed: Polaris spacing tokens named
  as percentage multipliers of a 4 px base (`space-100` = 4 px, `space-400` = 16 px), with
  primitive + semantic tiers (verified 2026-06-12)
- https://m3.material.io/foundations/layout/understanding-layout/spacing — confirmed:
  Material 3 spacing units follow an 8 dp scale; components align to an 8 dp grid while
  type and iconography align to a 4 dp grid (page is JS-rendered; facts cross-checked via
  search excerpts of the same page) (verified 2026-06-12)
- https://zellwk.com/blog/why-vertical-rhythms/ — confirmed: vertical-rhythm rules — set
  inter-block whitespace and text line-heights to multiples of one baseline unit (24 px
  example for 16 px body) (verified 2026-06-12)
- https://usabilitygeek.com/when-how-break-grid-layout/ — confirmed: establish a solid
  grid before breaking it; effective broken-grid work keeps the grid as the reference
  that makes deviation read as intentional (verified 2026-06-12)
- https://www.awwwards.com/inspiration/breaking-the-grid — confirmed: broken-grid
  composition is a curated, award-recognized technique on Awwwards (verified 2026-06-12)
