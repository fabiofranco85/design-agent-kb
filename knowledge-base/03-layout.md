---
title: Layout, Grid Systems & Composition
doc_id: 03-layout
version: 1.0
last_verified: 2026-06-12
applies_to_modes: [create, recreate, modify]
---

## Purpose & When To Read This

Open this doc whenever you must define or change the structural skeleton of a site: page
grids, column systems, breakpoints, container-query strategy, fluid layout dimensions
(margins, gutters, section padding), or compositional moves (asymmetry, overlap, negative
space, diagonal framing). Also open it in `recreate` mode before inferring a grid from a
live site or screenshots. Spacing-scale values themselves are owned by
[06-spacing](./06-spacing.md#specifications--parameters); fluid *type* sizing is owned by
[04-typography](./04-typography.md#specifications--parameters) — this doc owns everything
between the viewport edge and the content box.

## Core Principles

1. **Grid first, break second.** Build a strict Swiss/modernist column system (the
   Müller-Brockmann lineage: single-column, multi-column, modular, hierarchical grids),
   then deviate deliberately. A break only reads as intentional against visible order.
   The when/how rules for breaking rhythm live in
   [06-spacing](./06-spacing.md#specifications--parameters).
2. **One structural grid per page.** All sections place onto the same 12-column system
   (or a named-area editorial preset mapped onto it). Nested components inherit tracks
   via `subgrid` — never re-derive track math by hand.
3. **Mobile-first, container-aware.** Page structure responds to the *viewport*
   (media queries); components respond to *their container* (`@container`). A card must
   not know which breakpoint the page is at.
4. **Fluid between anchors, stepped at structure.** Dimensions (margins, gutters,
   section padding) interpolate continuously via `clamp()`; column *count* changes only
   at the canonical breakpoints. Never let a layout dimension grow unbounded with `vw`
   alone.
5. **Negative space is a material, not leftover.** Award-level layouts reserve empty
   columns on purpose (see Composition Parameters). Symmetric, fully-filled,
   center-everything pages read as templates and lose juries.
6. **Source order = reading order.** Grid placement rearranges visuals, never meaning.
   Tab order and screen-reader order must match the DOM, at every breakpoint.
7. **Numbers, not vibes.** Every offset, overlap, ratio, and angle in this doc is exact.
   When you invent a new compositional move, write its numbers down in the same way.

## Decision Framework

- IF the page is content-led (editorial, portfolio, agency) → 12-column fluid grid +
  one named-area editorial preset per hero/feature section.
- IF the page is app-like (dashboard, tool) → 12-column grid, symmetric placement,
  skip compositional breaks; density rules come from
  [06-spacing](./06-spacing.md#specifications--parameters).
- IF a component appears in containers of unknown width (card, media object, teaser)
  → drive its internal layout with `@container` queries, not media queries.
- IF a nested element must align to page columns (captions, hanging numbers, card rows
  with shared baselines) → `subgrid` on that axis + `@supports` fallback.
- IF a section needs full-bleed media but aligned text → breakout grid (Code Example A):
  named lines `full` and `content`, opt-in `grid-column: full`.
- IF the brief demands "energy/tension" → apply at most ONE compositional move per
  viewport-height: asymmetric split, overlap, or diagonal — never all three stacked.
- IF reverse-engineering (`recreate`) → start from computed styles, not pixels:
  `getComputedStyle()` returns used track sizes in px (see Mode-Specific Guidance).
- IF subgrid support below the project's browser floor matters (Safari < 16, Chrome
  < 117) → ship the `@supports not (...)` fallback in Code Example B; never block
  layout on JS polyfills.

## Specifications & Parameters

### Canonical breakpoints (mobile-first, `min-width`)

Breakpoints step the column *count* only. Gutters and outer margins are ALWAYS the
fluid `clamp()` recipes below (the single source — Code Example A applies them at every
width); they are never stepped per breakpoint. The Gutter / Outer-margin columns show
what each canonical recipe resolves to at that breakpoint's min-width:

| Token | Min-width | Design columns | Gutter (fluid value at this width) | Outer margin (fluid value at this width) |
|---|---|---|---|---|
| `bp.base` | 0 | 4 | 16px (clamp min = `space.4`) | 24px (clamp min = `space.6`) |
| `bp.sm` | 480px | 4 | 16px (clamp min) | 24px (clamp min) |
| `bp.md` | 768px | 6 | 17.6px | 24px (clamp min) |
| `bp.lg` | 1024px | 12 | 20.8px | 37.44px |
| `bp.xl` | 1280px | 12 | 24px | 52.8px |
| `bp.2xl` | 1440px | 12 | 26px | 62.4px |

- Gutter math (`1.25vw + 8px`): @768 → 9.6 + 8 = 17.6px; @1024 → 12.8 + 8 = 20.8px;
  @1280 → 16 + 8 = 24px; @1440 → 18 + 8 = 26px; reaches the 32px (`space.8`) max at 1920.
- Margin math (`6vw − 24px`): at ≤ 800 the preferred value ≤ 24px, so the 24px
  (`space.6`) min holds; @1024 → 61.44 − 24 = 37.44px; @1280 → 76.8 − 24 = 52.8px;
  @1440 → 86.4 − 24 = 62.4px; reaches the 96px (`space.24`) max at 2000. Both
  sequences grow monotonically with viewport width.
- Beyond `--content-max` (1440px) the scaffold's `1fr` margin tracks absorb surplus
  width, so real margins exceed the clamp value (auto-centering).
- All clamp endpoints are `space.{n}` tokens pinned in `_conventions.md` §3.5 and owned
  by [06-spacing](./06-spacing.md#specifications--parameters). CSS custom-property
  mapping assumed: `space.4` → `var(--space-4)`.
- Write media queries with these exact min-widths only. Never invent per-component
  breakpoints — that is what container queries are for.
- Test widths (fixed set): **320, 375, 480, 768, 1024, 1280, 1440, 1920**.

### The 12-column primary grid

| Parameter | Value |
|---|---|
| Columns (desktop ≥1024) | 12, equal `1fr`, `minmax(0, 1fr)` to prevent blowout |
| Content max-width | **1440px** default; `wide` variant 1680px; `full` = 100% |
| Column gutter | fluid `clamp(var(--space-4), 1.25vw + 8px, var(--space-8))` → 16px at 640px viewport, 32px at 1920px |
| Outer margin (≥1024) | fluid `clamp(var(--space-6), 6vw - 24px, var(--space-24))` → 24px at 800px, 96px at 2000px |
| Named lines | `full-start/full-end`, `content-start/content-end`, per-column `col-start` repeats |
| Default placement | children span `content`; full-bleed is opt-in via `grid-column: full` |

Standard span vocabulary on 12 columns: `span 12` (full), `span 8` + `span 4`
(primary/secondary), `span 7` + `span 5` (editorial asymmetric), `span 6` + `span 6`
(split), `span 4` ×3 (cards), `span 3` ×4 (dense cards).

### Named-area editorial grid presets (on a 6-track macro grid; each macro column = 2 base columns at ≥1024)

Preset `editorial-feature` (kicker/title/media/body, media-dominant 4/2 split):

```text
"kicker kicker .      .      .      ."
"title  title  title  title  .      ."
"media  media  media  media  body   body"
".      .      .      .      body   body"
```

Preset `editorial-split` (50/50 with offset rows — text leads, media trails one row):

```text
"title  title  title  .      .      ."
"body   body   body   media  media  media"
".      .      .      media  media  media"
```

Preset `editorial-stack` (mobile/base; all presets collapse to this below 40rem
container width): every area spans all 6 tracks, order `kicker → title → media → body`.

Rules: every area must be rectangular (non-rectangular `grid-template-areas` are
invalid per MDN); `.` marks deliberate negative space — keep at least 2 empty macro
cells per preset at ≥1024.

### Container-query strategy

| Parameter | Value |
|---|---|
| Container type | `container-type: inline-size` (default). Use `size` only when block-size is externally fixed — it adds size containment and collapses height-auto elements |
| Naming | `container: <component> / inline-size`, kebab-case, one name per component family (`card-row`, `feature`, `sidebar`) |
| Query thresholds | component-intrinsic, in rem: `24rem`, `40rem`, `64rem` (NOT the page breakpoints) |
| Units | `cqi` (1% of container inline size) for fluid internals; `cqw/cqh/cqb/cqmin/cqmax` available; fall back to small-viewport units when no container exists |

### Fluid layout dimension recipes (clamp endpoints MUST be `space.{n}` tokens)

The gutter/margin/section recipe values are owned by
[06-spacing](./06-spacing.md#specifications--parameters) (canonical worked recipes,
with full slope/intercept derivations) — do not edit them here. Only the
container-relative card-gap row is layout-specific to this doc.

| Dimension | Recipe | Resolves |
|---|---|---|
| Column gutter | `clamp(var(--space-4), 1.25vw + 8px, var(--space-8))` | 16 → 32px (640 → 1920 vp) |
| Outer margin | `clamp(var(--space-6), 6vw - 24px, var(--space-24))` | 24 → 96px (800 → 2000 vp) |
| Section padding-block | `clamp(var(--space-16), 8vw, var(--space-32))` | 64 → 128px (800 → 1600 vp) |
| Card internal gap (container-relative) | `clamp(var(--space-4), 2cqi, var(--space-8))` | 16 → 32px (800 → 1600 cq) |

Deriving a new recipe (the slope/intercept formula and general fluid-spacing
methodology) is owned by [06-spacing](./06-spacing.md#specifications--parameters).
Fluid *font* recipes are owned by
[04-typography](./04-typography.md#specifications--parameters) — never write them here.

### Composition parameters (the award-level moves, quantified)

| Move | Parameter | Spec |
|---|---|---|
| Asymmetric split | column ratio | 7/5 or 8/4 on 12 cols (≈ golden 7.4/4.6 — use 7/5) |
| Off-center focal | placement | focal mass starts at col 2–3 or ends at col 9–10; never centered on col 6/7 boundary in hero sections |
| Negative space | hero | ≥ 30% of the hero area empty; ≥ 1 fully empty column (of 12) flanking the focal element |
| Negative space | sections | ≥ 2 empty macro cells per editorial preset (see above) |
| Overlap (horizontal) | depth | element shifts 1–2 columns into its neighbor's span |
| Overlap (vertical) | pull | `margin-block-start: calc(-1 * var(--space-16))` to `calc(-1 * var(--space-24))` (−64 to −96px), or shared grid rows |
| Layer scale | z-index tokens | `--layer-base: 0`, `--layer-media: 1`, `--layer-overlap: 2`, `--layer-content: 3`, `--layer-chrome: 10`; nothing else |
| Diagonal framing | section edges | `clip-path: polygon(...)` at 3–8° (e.g. 100% edge offset = `tan(angle) × width`); text never clipped |
| Rotation accents | decorative only | −2° to 2° (`transform: rotate()`); body text always 0° |
| Break frequency | per viewport-height | ≤ 1 compositional break; rhythm-break rules in [06-spacing](./06-spacing.md#specifications--parameters) |
| Tension | counterweight | every off-grid element is balanced by negative space or a small anchored element in the opposing third |

### Browser support floor (verified 2026-06-12, caniuse)

| Feature | Chrome | Edge | Firefox | Safari | Global |
|---|---|---|---|---|---|
| `subgrid` | ≥ 117 | ≥ 117 | ≥ 71 | ≥ 16.0 | 88.39% |
| Container size queries | ≥ 106 | ≥ 106 | ≥ 110 | ≥ 16.0 | 92.22% |

Both are safe as progressive enhancements with the fallbacks in Code Examples; treat
them as baseline for new award-tier builds, but always ship the `@supports` path.

## Recommended Libraries & Tools

- **Layout requires zero npm dependencies.** Native CSS Grid Level 2 (subgrid) +
  CSS Containment (container queries) cover everything in this doc. Do NOT add
  Bootstrap/Foundation-style grid frameworks — they fight token-driven gutters.
- **Chrome DevTools grid inspector** (`recreate` + QA): grid badge in the Elements
  panel toggles a per-grid overlay showing lines, track sizes, and area names; the
  Layout pane lists all grids, supports multiple simultaneous overlays, line-number/
  name labels, and extending lines to viewport edges. Firefox has an equivalent grid
  inspector.
- **Framework context** (versions from `_facts.md`, verified 2026-06-12): layout CSS in
  this doc is framework-agnostic and drops into `next@16.2.9`, `astro@6.4.6`,
  `nuxt@4.4.8`, or plain `react@19.2.7` projects unchanged.

## Code Examples

### A — Page scaffold: fluid breakout grid (the one structural grid)

```css
:root {
  /* space.{n} tokens are emitted by 06-spacing as --space-{n}; endpoints below are tokens */
  --gutter: clamp(var(--space-4), 1.25vw + 8px, var(--space-8)); /* 16px@640 → 32px@1920 */
  --margin: clamp(var(--space-6), 6vw - 24px, var(--space-24));  /* 24px@800 → 96px@2000 */
  --content-max: 1440px;
}

.page-grid {
  --cols: 4;                                   /* design columns, mobile-first */
  display: grid;
  column-gap: var(--gutter);
  /* margin tracks subtract one gutter: column-gap also separates them from col 1/N */
  grid-template-columns:
    [full-start] minmax(calc(var(--margin) - var(--gutter)), 1fr)
    [content-start] repeat(
      var(--cols),
      minmax(0, calc((var(--content-max) - (var(--cols) - 1) * var(--gutter)) / var(--cols)))
    )
    [content-end] minmax(calc(var(--margin) - var(--gutter)), 1fr)
    [full-end];
}
@media (min-width: 768px)  { .page-grid { --cols: 6; } }
@media (min-width: 1024px) { .page-grid { --cols: 12; } }

.page-grid > *          { grid-column: content; } /* default: aligned content width */
.page-grid > .full-bleed { grid-column: full; }   /* opt-in edge-to-edge media */
```

### B — Fluid editorial feature: named areas + container queries + subgrid

```css
.feature { container: feature / inline-size; }   /* responds to ITS width, not viewport */

.feature__grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr)); /* 6-track macro grid */
  column-gap: var(--gutter);
  row-gap: var(--space-8);
  grid-template-areas:        /* base = editorial-stack */
    "kicker kicker kicker kicker kicker kicker"
    "title  title  title  title  title  title"
    "media  media  media  media  media  media"
    "body   body   body   body   body   body";
}

/* ≥40rem container: editorial-feature preset — asymmetric 4/2, deliberate empty cells */
@container feature (inline-size >= 40rem) {
  .feature__grid {
    grid-template-areas:
      "kicker kicker .      .      .      ."
      "title  title  title  title  .      ."
      "media  media  media  media  body   body"
      ".      .      .      .      body   body";
  }
}

.feature__kicker { grid-area: kicker; }
.feature__title  { grid-area: title; }
.feature__body   { grid-area: body; }

/* Media block: caption hangs on the macro columns via subgrid, not arbitrary offsets */
.feature__media {
  grid-area: media;
  display: grid;
  grid-template-columns: subgrid;  /* inherits the 4 spanned tracks + gutter from parent */
  row-gap: var(--space-2);         /* row-gap override; column-gap stays inherited */
}
.feature__media img {
  grid-column: 1 / -1;
  aspect-ratio: 16 / 9;            /* reserves space — protects CLS budget (doc 09) */
  object-fit: cover;
  width: 100%;
}
.feature__media figcaption { grid-column: 1 / 3; } /* first 2 inherited tracks */

/* Fallback: engines without subgrid (Safari <16, Chrome/Edge <117, Firefox <71) */
@supports not (grid-template-columns: subgrid) {
  .feature__media { grid-template-columns: repeat(4, minmax(0, 1fr)); } /* ≈ drift ok */
}
```

### C — Card row with cross-card row alignment (subgrid rows)

```css
.card-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr));
  gap: var(--gutter);
}
.card {
  display: grid;
  grid-row: span 4;             /* eyebrow / title / body / cta */
  grid-template-rows: subgrid;  /* all 4 rows align across every card in the row */
  row-gap: var(--space-3);
}
@supports not (grid-template-rows: subgrid) {
  .card { grid-template-rows: auto auto 1fr auto; } /* per-card approximation */
}
```

## Mode-Specific Guidance

### Create from scratch

1. Pick the structural grid: always Code Example A. Set `--content-max` (1440px unless
   the brief's archetype from
   [01-visual-motion](./01-visual-motion.md#specifications--parameters) demands `wide`
   1680px).
2. Choose one editorial preset per hero/feature section; symmetric spans elsewhere.
3. Quantify every compositional move against the Composition Parameters table before
   writing CSS; record the chosen numbers in the project spec artifact (doc 10).
4. Define container names for every reusable component family up front.

### Re-create from existing site (reverse-engineering)

1. **Computed DOM beats pixel-measuring.** For a grid container, `getComputedStyle()`
   serializes `grid-template-columns/rows` as the **used values**: "every track size
   given as a length in pixels" and "every track listed individually, whether
   implicitly or explicitly created" (CSSWG css-grid-1 §7.2.6). Dump all grids:

   ```js
   for (const el of document.querySelectorAll('*')) {
     const cs = getComputedStyle(el);
     if (cs.display.includes('grid')) console.log(el.tagName, el.className, {
       cols: cs.gridTemplateColumns, rows: cs.gridTemplateRows,   // used px tracks
       colGap: cs.columnGap, rowGap: cs.rowGap, areas: cs.gridTemplateAreas,
     });
   }
   ```

2. Infer the system: count equal-width tracks → column count; `columnGap` → gutter;
   outer margin = `(innerWidth − Σtracks − Σgaps) / 2` (also: `width`, `padding-*`,
   `margin-*` resolve to used px values via `getComputedStyle`, per MDN).
3. Sample at 3+ widths (375 / 768 / 1440): values that change continuously are fluid —
   solve `slope = (m2 − m1)/(v2 − v1)` and reconstruct the `clamp()`; values that jump
   mark a breakpoint — record its exact px.
4. Use the Chrome DevTools grid overlay (grid badge → Layout pane) to read line
   numbers, named areas, and track sizes visually; enable multiple overlays to check
   whether nested grids share tracks (subgrid candidates).
5. **Screenshots only** (no DOM): align a vertical-line overlay to repeated left/right
   text and image edges; distinct alignment lines ≈ column lines. Work in ratios
   (gutter ÷ column width), then map to the nearest 12-column interpretation. Validate
   by re-rendering your inferred grid at 50% opacity over the screenshot at the same
   width — every major edge must land on a line. Flag unmatched edges as deliberate
   breaks, not grid errors.
6. Snap every recovered gutter/margin to the nearest `space.{n}` token and note the
   delta in the recreate report (schema in doc 10).

### Modify an existing system

1. Never change column count, `--content-max`, or breakpoint values inside an existing
   system — additions must place onto the incumbent grid.
2. New gutters/margins: reuse the existing clamp recipes; if a new dimension is needed,
   derive it with the slope formula and token endpoints, then register it in the
   token file (DTCG, `.tokens.json` per `_conventions.md` §3.7).
3. Adding a compositional break: check the per-viewport break budget (≤1) against
   neighboring sections before and after the insertion point.
4. Regression pass: re-run the Quality Checklist at all 8 test widths; diff
   `getComputedStyle` grid dumps (step 1 above) before/after.

## Quality Checklist

- [ ] Every gutter/margin/section-padding is a `space.{n}` token or a `clamp()` whose
      min/max are `space.{n}` tokens — zero loose px values.
- [ ] No horizontal overflow at 320, 375, 480, 768, 1024, 1280, 1440, 1920.
- [ ] One structural grid per page; nested alignment uses `subgrid`, with `@supports`
      fallback present and visually acceptable.
- [ ] Container queries used for all reusable components; thresholds in rem; no
      component-level viewport media queries.
- [ ] All `grid-template-areas` rectangular; every preset collapses to
      `editorial-stack` below 40rem container width.
- [ ] DOM order = visual reading order at every breakpoint (tab through the page).
- [ ] All media slots declare `aspect-ratio` (CLS ≤ 0.1 budget — owner:
      [09-tech-implementation](./09-tech-implementation.md#specifications--parameters)).
- [ ] Content max-width 1440px enforced; `full-bleed` only where specified.
- [ ] ≤ 1 compositional break per viewport-height; every break has a counterweight
      (negative space or anchored element) per the Composition Parameters table.
- [ ] Hero negative-space minimum met (≥ 30% empty, ≥ 1 empty column).
- [ ] z-index values come only from the 5-token layer scale.

## Anti-Patterns

- **Centered-symmetric everything.** Title centered, content centered, three equal
  cards — reads as a template; juries reject it. Apply the asymmetry specs.
- **Breaking the grid everywhere.** More than one break per viewport-height reads as
  chaos, not tension. Order first, deviation second.
- **`position: absolute` for overlaps.** Kills reflow and accessibility; use grid
  placement into shared rows/columns or the negative `margin-block-start` token range.
- **`width: 100vw` full-bleeds.** Includes the scrollbar width on most desktop
  platforms → horizontal overflow. Use the breakout grid's `grid-column: full`.
- **Re-deriving nested track math** (`calc((100% - 11*gutter)/12)` inside components)
  instead of `subgrid` — drifts the moment a gutter token changes.
- **Per-component viewport breakpoints.** A card styled by `@media` breaks the moment
  it's placed in a sidebar. Container queries only.
- **`container-type: size` on auto-height sections** — size containment collapses them
  to 0 height. Default to `inline-size`.
- **`vw`-only fluid dimensions** (no `clamp()`): margins balloon on 3440px ultrawides
  and crush at 320px.
- **Grid-placement reordering against DOM order** to "fix" a layout — breaks tab order
  and screen-reader flow; fix the DOM instead.
- **Phantom breakpoints** (e.g. 991px, 1199px copied from old frameworks) instead of
  the canonical set — multiplies QA surface with zero design payoff.

## Sources & Verification

- https://caniuse.com/css-subgrid — confirmed: subgrid first shipped Chrome/Edge 117, Firefox 71, Safari 16.0; global support 88.39% (verified 2026-06-12)
- https://caniuse.com/css-container-queries — confirmed: container size queries first shipped Chrome/Edge 106, Firefox 110, Safari 16.0; global support 92.22% (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid — confirmed: subgrid syntax, gap inheritance + per-axis override, parent named lines passing into subgrids, line numbering restarting at 1, no implicit tracks in subgridded dimensions (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries — confirmed: `container-type` values (`size`/`inline-size`/`normal`), `container: name / type` shorthand, `@container` syntax, cq unit definitions (`cqw/cqh/cqi/cqb/cqmin/cqmax`), fallback to small-viewport units without a container (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/CSS/clamp — confirmed: `clamp(MIN, VAL, MAX)` resolves as `max(MIN, min(VAL, MAX))`; mixed units and math expressions allowed; valid for width/padding/margin (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/CSS/grid-template-areas — confirmed: string-row syntax, rectangular-area requirement (non-rectangular = invalid), `.` null-cell tokens, placement via `grid-area` (verified 2026-06-12)
- https://drafts.csswg.org/css-grid-1/#resolved-track-list — confirmed: resolved value of `grid-template-columns/rows` on a grid container serializes "every track size given as a length in pixels" and lists every track individually including implicit tracks (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/CSS/resolved_value — confirmed: `getComputedStyle()` returns used values for `width`, `height`, `margin-*`, `padding-*`, `top/right/bottom/left` (verified 2026-06-12)
- https://developer.chrome.com/docs/devtools/css/grid — confirmed: grid badge toggles per-grid overlay; Layout pane offers line numbers/names, track sizes, area names, multiple simultaneous overlays, extend-lines option (verified 2026-06-12)
- https://www.artlebedev.com/izdal/modulnye-sistemy-2021/ — confirmed: Müller-Brockmann "Grid Systems in Graphic Design" taxonomy (single-column, multi-column, modular, hierarchical grids) and the "grid system is an aid, not a guarantee" framing (verified 2026-06-12)
- https://blog.hubspot.com/website/broken-grid-layouts — confirmed: broken-grid practice = build within a grid system first, then offset/overlap via CSS; whitespace required to keep broken grids readable (verified 2026-06-12)
