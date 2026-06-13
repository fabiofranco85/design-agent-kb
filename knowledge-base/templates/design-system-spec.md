---
project: <project-name>
artifact: design-system-spec
version: 1.0.0             # semver — create/recreate emit 1.0.0; modify bumps per ../10-modes-and-artifacts.md §3
date: <YYYY-MM-DD>
mode: <create | recreate | modify>
source_url: <https://existing-site.example | none>   # recreate/modify only; none in create
archetype: <brutalist-editorial | immersive-3d | kinetic-minimal | retro-futurist | soft-organic | luxe-cinematic>
personality: <snappy | fluid | cinematic>
intensity: <ambient | responsive | showcase>
confidence:                # summary of the §11 table — recreate mode ONLY; delete this block in create mode
  archetype: <high | medium | low>
  typography: <high | medium | low>
  color: <high | medium | low>
  layout: <high | medium | low>
  spacing: <high | medium | low>
  imagery: <high | medium | low>
  motion: <high | medium | low>
  webgl-stack: <high | medium | low>
---

<!--
TEMPLATE — design-system-spec.md
Section schema owner: ../10-modes-and-artifacts.md#specifications--parameters (§2 — exact
section names and order; this skeleton implements that schema, never the reverse).
The agent fills this skeleton for every project. Rules:
  • Replace every <angle-bracket placeholder>. Delete every guidance comment when done.
  • Numbers, not adjectives (_conventions.md §1). "Bold" is a defect; "display ≥ 8vw" is a spec.
  • Versions/installs come ONLY from ../_facts.md. Flag anything unconfirmed with the literal
    string: UNVERIFIED — confirm before use.
  • Frontmatter tokens (archetype / personality / intensity) are the top-level decisions
    every other doc consumes — pick them via ../01-visual-motion.md#decision-framework
    BEFORE filling any section below.
  • In recreate mode, keep the frontmatter confidence block (the canonical 8 dimensions,
    summarizing the §11 table). In create mode, delete it.
-->

# Design System Spec — <project-name>

## 1. Identity & Direction

<!-- Owner of the taxonomy + measurable signals: ../01-visual-motion.md#specifications--parameters
     Exactly ONE archetype, ONE personality, ONE intensity tier per site. Record the 5–8
     measurable signals you commit to — recreate mode needs ≥4 matching signals to classify. -->

- **Brief adjectives (3–5):** <adjective-1>, <adjective-2>, <adjective-3>
- **Archetype:** `<archetype-token>` — justification: <1–2 sentences mapping brief → Step 1/2 of the decision framework>
- **Personality:** `<snappy | fluid | cinematic>` (archetype default ± max one step; justify any override: <justification | none>)
- **Intensity:** `<ambient | responsive | showcase>` <!-- showcase requires the perf budget in §10 to hold -->
- **Committed measurable signals (5–8, each verifiable in the build):**
  | # | Signal | Value |
  |---|---|---|
  | 1 | <e.g. display type size> | <e.g. clamp ceiling 12vw> |
  | 2 | <e.g. border treatment> | <e.g. 1px hairlines, radius 0> |
  | 3 | <e.g. palette stance> | <e.g. near-black on off-white, 1 accent> |
  | 4 | <signal> | <value> |
  | 5 | <signal> | <value> |
- **Signature interaction (exactly one):** <the single memorable move — element, trigger, behavior>

## 2. Typography

<!-- Owner: ../04-typography.md#specifications--parameters (scale ratios, fluid clamp recipes,
     SplitText reveal recipe). Ratios pinned in _conventions.md §3.6: Minor Third 1.2,
     Major Third 1.25, Perfect Fourth 1.333, Golden 1.618; UI default 1.2–1.333; body floor 16px.
     Token contract (../10-modes-and-artifacts.md §3): primitives are `type.step.N` (doc 04);
     role composites `typography.*` alias them — fontSize MUST be `{type.step.N}`. -->

- **Display face:** <family> — <weights used> — license: <license/source>
- **Body face:** <family> — <weights used> — license: <license/source>
- **Pairing rationale:** <1 sentence>
- **Scale ratio:** <1.2 | 1.25 | 1.333 | 1.618> · **Body floor:** 16px · **Body line-height:** <1.5–1.75, unitless>
- **Scale steps (rem/px at base 16):**
  | Role token | fontSize alias | Size | Use |
  |---|---|---|---|
  | `typography.display` | `{type.step.6}` | <clamp(min, vw-formula, max)> | hero display |
  | `typography.h1` | `{type.step.<n>}` | <value> | page titles |
  | `typography.h2` | `{type.step.<n>}` | <value> | section titles |
  | `typography.h3` | `{type.step.<n>}` | <value> | block titles |
  | `typography.body` | `{type.step.0}` | 16px / 1rem | prose, UI |
  | `typography.small` | <`{type.step.<n>}` \| fixed ≥ 12px> | <value ≥ 12px> | captions, labels |
- **Tracking / case rules:** <e.g. small-caps labels 0.08–0.16em; display -0.02em — em values per ../04-typography.md#specifications--parameters>
- **Loading strategy:** <woff2 subsets, font-display value, preload list — pipeline detail in implementation-plan.md>

## 3. Color

<!-- Owner: ../05-color.md#specifications--parameters. OKLCH is the working space; hex is
     fallback only. Three tiers, aliases only above primitive; themes swap SEMANTICS, never
     primitives. Full values live in design-tokens.tokens.json — list ramps + the semantic
     map + verified contrast here, not every step. -->

- **Brand hue H:** <0–360> · **Neutral hue:** <same H, C 0.003–0.015> · **Accent hues (≤2):** <H values | none>
- **Ramps emitted (11 steps on the doc-05 L anchors):** `color.<brand-name>.50–950`, `color.neutral.0–950`<, color.<accent>.…>
- **Themes:** <light + dark | light only | dark only> — dark override file re-targets semantic tier only (`design-tokens.dark.tokens.json`)
- **Semantic map (alias targets per theme):**
  | Semantic token | Light alias | Dark alias |
  |---|---|---|
  | `color.bg.primary` | `{color.neutral.<step>}` | `{color.neutral.<step>}` |
  | `color.bg.brand` | `{color.<brand>.<step>}` | `{color.<brand>.<step>}` |
  | `color.text.primary` | `{color.neutral.<step>}` | `{color.neutral.<step>}` |
  | `color.text.on-brand` | `{color.neutral.<step>}` | `{color.neutral.<step>}` |
  | `color.border.focus` | `{color.<brand>.<step>}` | `{color.<brand>.<step>}` |
  | <…complete per the doc-05 semantic map> | | |
- **Verified contrast pairs** <!-- compute on hex fallbacks with the canonical gate:
  ../05-color.md#code-examples — no rounding up; record EVERY text + UI pair, both themes -->
  | Pair | Light ratio | Dark ratio | Target | Status |
  |---|---|---|---|---|
  | `text.primary` on `bg.primary` | <n.nn:1> | <n.nn:1> | 4.5:1 | <pass/fail> |
  | `text.on-brand` on `bg.brand` | <n.nn:1> | <n.nn:1> | 4.5:1 | <pass/fail> |
  | `border.focus` on `bg.primary` | <n.nn:1> | <n.nn:1> | 3:1 | <pass/fail> |
- **P3 policy:** <`color.<hue>.vivid` accents with sRGB base + `@media (color-gamut: p3)` chroma-only boost | none>

## 4. Layout & Grid

<!-- Owner: ../03-layout.md#specifications--parameters (grid, breakpoints, composition).
     The grid consumes the exact --space-{n} custom properties — never rename them. -->

- **Grid:** <12-col | other> · **Max content width:** <px> · **Prose measure:** <≤720px>
- **Breakpoints:** <list px values + names>
- **Gutter:** `space.gutter` (fluid, §5) · **Outer margin:** `space.margin`
- **Container queries:** <where used | none>
- **Hero composition:** <full-bleed | contained | canvas-dominant ≥60% (immersive-3d)> — negative-space minimums per ../03-layout.md#specifications--parameters
- **Section map (per page template):**
  | Page | Section | Layout pattern | Full-bleed? |
  |---|---|---|---|
  | <home> | <hero> | <pattern> | <y/n> |

## 5. Spacing & Rhythm

<!-- Owner: ../06-spacing.md#specifications--parameters. The canonical space.{n} scale
     (n = px ÷ 4, base 8px) is pinned in _conventions.md §3.5 — adopt verbatim unless the
     brief demands otherwise; document any deviation with its math. -->

- **Scale:** canonical `space.1/2/3/4/6/8/12/16/24/32` (4–128px) — deviations: <none | list with justification>
- **Rhythm unit:** <24px = `space.6` (16px body × 1.5) | recomputed: <math>>
- **Fluid semantic recipes (token endpoints + verified clamp math, per doc 06):**
  | Token | Endpoints | Viewport range | clamp() |
  |---|---|---|---|
  | `space.gutter` | `space.<n>`→`space.<n>` | <v1>→<v2> | <clamp(var(--space-n), …vw ± …px, var(--space-n))> |
  | `space.margin` | `space.<n>`→`space.<n>` | <v1>→<v2> | <…> |
  | `space.section` | `space.<n>`→`space.<n>` | <v1>→<v2> | <…> |
- **Density stance:** <default | data-dense (micro/meso −1 step) | editorial (macro +1 step)>
- **Planned grid-breaks (≤1 per viewport-height, 3–5 per page max):**
  | Section | Move (exaggeration / compression / asymmetric / overlap) | Values | Recovery section |
  |---|---|---|---|
  | <section> | <move> | <token values> | <next section, on-scale> |

## 6. Imagery & Asset Direction

<!-- Owner: ../02-image-generation.md#specifications--parameters (prompt vocabulary, texture,
     treatment + export specs). Archetype dictates the style vocabulary (cascade table in
     ../01-visual-motion.md#specifications--parameters). -->

- **Image classes:** <photography | 3D renders | illustration | generative> — ratio across site: <e.g. 70/30>
- **Prompt style vocabulary (for generated assets):** <subject treatment, lighting, lens, palette anchors>
- **Texture/treatment:** <grain % | gloss | duotone | none> · **Color grading:** <toward palette tokens>
- **Aspect ratios used:** <list> · **Focal-point rules:** <e.g. golden-section anchors>
- **Export specs:** per ../02-image-generation.md#specifications--parameters — formats <AVIF/WebP + fallback>, hero budget <KB>, alt-text policy: <required for all informative images>

## 7. Components

<!-- Inventory + per-component token bindings. Component tokens alias SEMANTICS only
     (_conventions.md §3.7). States must include hover, focus-visible, active, disabled;
     focus indicators ≥3:1 contrast (../05-color.md#specifications--parameters). -->

| Component | Variants | Key tokens (component tier) | States specced | Motion ref (motion-spec.md ID) |
|---|---|---|---|---|
| Button | <primary / secondary / ghost> | `button.bg`, `button.text`, `button.padding-x/y` | <hover/focus/active/disabled> | <M-##> |
| Card | <variants> | `card.bg`, `card.border`, `card.padding` | <…> | <M-##> |
| Nav / header | <variants> | <tokens> | <…> | <M-##> |
| <component> | <…> | <…> | <…> | <M-##> |

<!-- Add one row per component. Every visual value in a component must resolve to a token. -->

## 8. Motion Language

<!-- Summary only — the full choreography contract lives in motion-spec.md (same folder;
     schema: ../10-modes-and-artifacts.md#specifications--parameters §4). Easing names +
     duration classes are owned by ../07-animation-choreography.md#specifications--parameters;
     personality slices by ../01-visual-motion.md#specifications--parameters. -->

- **Personality:** `<token>` · **Workhorse band:** <150–350 | 400–800 | 600–1200> ms
- **Pinned eases (2 primary + 1 accent, GSAP names):** `<ease-1>`, `<ease-2>`, accent `<ease-3>`
- **Duration-class slices in use:** micro <ms> · ui <ms> · reveal <ms> · hero <ms>
- **Stagger default:** <ms/item> · **Entrance travel:** <px> · **Hover scale:** <value | 1.00>
- **Smooth scroll:** <Lenis lerp <0.05–0.18> | native> · **Page transitions:** <View Transitions + fallback | GSAP wipe | none>
- **Reduced motion:** canonical pattern mandatory — ../07-animation-choreography.md#code-examples

## 9. Accessibility Notes

<!-- Anchors pinned in _conventions.md §3.9; contrast owner ../05-color.md; reduced motion
     owner ../07-animation-choreography.md. This section records project-level commitments. -->

- **Target:** WCAG 2.2 AA
- **Contrast:** body ≥ 4.5:1, large text (≥24px / ≥18.66px bold) ≥ 3:1, UI/focus ≥ 3:1 — full verified table in §3
- **Reduced motion:** every motion item has a fallback (motion-spec.md §6 mapping); smoothing/parallax/marquees disabled under `reduce`
- **Keyboard:** all interactive elements reachable; visible focus (`color.border.focus`); skip link <y/n>
- **Zoom & text spacing:** layout survives 200% zoom and WCAG 1.4.12 overrides (../04-typography.md#quality-checklist)
- **Flashing:** nothing above 3 flashes/s (WCAG 2.3.1); <retro-futurist only: glitch loops ≤2Hz, dead under reduce>
- **Semantics:** <landmarks, heading order, form labels — project-specific notes>

## 10. Performance Budget

<!-- Anchors pinned in _conventions.md §3.8; canonical budget table:
     ../09-tech-implementation.md#specifications--parameters. Budgets are pass/fail at p75
     of real-user loads; the intensity tier (§1) must fit inside them or drop one tier
     (conflict rule: ../01-visual-motion.md#specifications--parameters). Measurement
     method + gates: implementation-plan.md §2. -->

| Metric | Budget | Measured (fill at QA) |
|---|---|---|
| LCP (p75) | < 2.5 s | <value> |
| INP (p75) | < 200 ms | <value> |
| CLS (p75) | < 0.1 | <value> |
| WebGL draw calls | < 100 (hard ceiling 150) | <value | n/a> |
| JS bundle (initial, gzip) | <KB target> | <value> |
| Hero image/video weight | <KB target> | <value> |
| Font payload (woff2, subset) | <KB target> | <value> |
| 3D assets (per device tier) | <desktop KB / mobile KB ≈ ¼ desktop> | <value | n/a> |

- **Device tiers:** <desktop / mid-tier mobile asset plan — required for `showcase` intensity>
- **WebGL constraints (if any canvas):** ../08-webgl-effects.md#decision-framework governs base-vs-accent and GPU rules

## 11. Provenance & Confidence

<!-- REQUIRED in recreate (this is the "recreate report"); in modify it holds the
     drift-audit result; in create it lists assumed items only. Canonical 8 dimensions:
     ../10-modes-and-artifacts.md#specifications--parameters (§2.11). low confidence ⇒
     the affected values carry the literal flag: UNVERIFIED — confirm before use. -->

- **Detection-script output (recreate):** <verbatim console.table output from doc 10 Code Example A | n/a>

| Dimension | Confidence | Provenance | Evidence (1 line) | Snap deltas |
|---|---|---|---|---|
| archetype | <high \| medium \| low> | <measured \| inferred \| assumed> | <e.g. 5/8 signals matched on home + work pages> | <— \| delta> |
| typography | <high \| medium \| low> | <measured \| inferred \| assumed> | <evidence> | <e.g. h1 measured 67px → `type.step.6` (69), Δ +2px> |
| color | <high \| medium \| low> | <measured \| inferred \| assumed> | <evidence> | <— \| delta> |
| layout | <high \| medium \| low> | <measured \| inferred \| assumed> | <evidence> | <— \| delta> |
| spacing | <high \| medium \| low> | <measured \| inferred \| assumed> | <evidence> | <e.g. gutter measured 22px → `space.6` (24), Δ +2px> |
| imagery | <high \| medium \| low> | <measured \| inferred \| assumed> | <evidence> | <— \| delta> |
| motion | <high \| medium \| low> | <measured \| inferred \| assumed> | <evidence> | <e.g. reveal 580ms → `motion.duration.reveal` (600), Δ +20ms> |
| webgl-stack | <high \| medium \| low> | <measured \| inferred \| assumed> | <evidence> | <— \| delta> |

- **Assumed / unverified items (carry the literal flag; empty list = write "none"):**
  - <item — UNVERIFIED — confirm before use | none>

## 12. Changelog

<!-- One entry per version: semver, date, diffs summary, rationale. create/recreate start
     at 1.0.0; modify appends an entry and bumps per the semver table in
     ../10-modes-and-artifacts.md#specifications--parameters (§3). Never rewrite history. -->

| Version | Date | Diff summary | Rationale |
|---|---|---|---|
| 1.0.0 | <YYYY-MM-DD> | initial emission (<mode>) | <brief intake | source-site reconstruction> |
