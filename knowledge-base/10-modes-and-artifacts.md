---
title: Mode Playbooks & Output Artifacts
doc_id: 10-modes-and-artifacts
version: 1.0
last_verified: 2026-06-12
applies_to_modes: [create, recreate, modify]
---

## Purpose & When To Read This

Open this doc at the START of every engagement (immediately after
[01-visual-motion](./01-visual-motion.md#purpose--when-to-read-this)) to select the
operating mode and load its playbook, and again at DELIVERY to emit the four output
artifacts. This doc is the canonical owner of the artifact schemas — the skeletons in
`./templates/` implement the schemas defined here, never the reverse. In `recreate`
mode, also use the runtime-detection table and extraction checklist below before opening
any domain doc.

## Core Principles

1. **Exactly one mode per engagement.** The three modes are `create`, `recreate`,
   `modify` (lowercase tokens, `_conventions.md` §3.1). Switching mode mid-engagement is
   an explicit, logged decision (see Decision Framework escalations), never a drift.
2. **Artifacts are the contract.** Every design decision lands in one of the four
   artifacts (§1 inventory). A decision that is not in an artifact does not exist:
   downstream agents and humans rebuild ONLY from artifacts, never from chat history.
3. **`recreate` is clean-room.** Infer the SYSTEM (scales, tokens, choreography
   vocabulary) from observation; never copy code, shaders, fonts files, or imagery —
   license risk (shader rule: [doc 08](./08-webgl-effects.md#mode-specific-guidance);
   imagery rule: [doc 02](./02-image-generation.md#mode-specific-guidance)).
4. **Every recorded value carries provenance.** Tag values `measured` (read from
   computed styles / runtime), `inferred` (derived from ≥2 consistent observations), or
   `assumed`. Every `assumed` value carries `UNVERIFIED — confirm before use`.
5. **The token file is semver-versioned.** Per semver.org: MAJOR = incompatible change,
   MINOR = backward-compatible addition, PATCH = backward-compatible fix. Mapping to
   token operations: §3 table. `create` and `recreate` emit `1.0.0`; `modify` always
   bumps.
6. **One quality bar, three modes.** A recreated or modified system must pass the same
   per-doc Quality Checklists as a from-scratch build. "The source site did it" is not
   a justification — flag source defects (e.g. failing contrast pairs per
   [doc 05](./05-color.md#mode-specific-guidance)), do not inherit them.

## Decision Framework

Select the mode from the INPUTS, not from preference:

- IF input = brief/requirements only (no existing site, no token file) → **`create`**.
- IF input = live URL (or screenshots/recordings of a site) AND goal = rebuild or
  extract its design system → **`recreate`**.
- IF input includes an existing `design-tokens.tokens.json` and/or `design-system-spec.md`
  (or a codebase embodying them) AND goal = extend/adjust while keeping identity →
  **`modify`**.

Escalations and edge cases:

- IF existing site + brief demands a NEW direction (redesign) → run the `recreate`
  extraction first (audit only, no artifact polish), then switch to `create`; record the
  old system in the spec's Provenance section as the migration baseline.
- IF `modify` is requested but no token file or spec exists → run the `recreate`
  playbook against the live build to reconstruct artifacts at `1.0.0`, then proceed
  with `modify` on top.
- IF a `modify` request changes the archetype token or motion-personality token →
  escalate to `create` with a migration note
  ([doc 01 rule](./01-visual-motion.md#mode-specific-guidance)).
- IF a `modify` diff would touch > 50% of semantic tokens or ≥ 2 of: type ratio, spacing
  base, color ramps, grid columns → treat as a redesign; escalate as above.

## Specifications & Parameters

### 1. Artifact inventory (canonical)

| Artifact | Template (skeleton) | Format | Primary content owners |
|---|---|---|---|
| `design-system-spec.md` | [./templates/design-system-spec.md](./templates/design-system-spec.md) | Markdown | docs 01–06, 08 |
| `design-tokens.tokens.json` | [./templates/design-tokens.tokens.json](./templates/design-tokens.tokens.json) | W3C DTCG 2025.10 (first stable version; `.tokens.json`; media type `application/design-tokens+json` — `_facts.md` §3) | docs 04–07 |
| `motion-spec.md` | [./templates/motion-spec.md](./templates/motion-spec.md) | Markdown | docs 01, 07 |
| `implementation-plan.md` | [./templates/implementation-plan.md](./templates/implementation-plan.md) | Markdown | docs 08, 09 |

Companion file (when theming): `design-tokens.dark.tokens.json` — semantic tier only,
same token names ([doc 05](./05-color.md#specifications--parameters) owns its rules).
All four artifacts are emitted in EVERY mode; in `modify`, unchanged artifacts are
re-emitted with an unchanged version and a changelog entry "no change".

### 2. `design-system-spec.md` — section schema (exact, ordered)

1. **Identity & Direction** — REQUIRED fields:
   - `archetype`: exactly one archetype token from the
     [doc 01 taxonomy](./01-visual-motion.md#specifications--parameters)
     (`brutalist-editorial` | `immersive-3d` | `kinetic-minimal` | `retro-futurist` |
     `soft-organic` | `luxe-cinematic`).
   - `personality`: exactly one of `snappy` | `fluid` | `cinematic`
     (`_conventions.md` §3.2), plus the override justification if it deviates from the
     archetype default.
   - `intensity`: exactly one of `ambient` | `responsive` | `showcase` (doc 01 tiers).
   - `signals`: 5–8 measurable archetype signals committed to, with numbers (palette
     stance, display ceiling, border/radius/texture values, stagger/travel values).
   - `signature-interaction`: the ONE memorable move, described with its parameters.
2. **Typography** — ratio, fluid anchors (320/1280 px), families + fallback metrics,
   loading plan ([doc 04](./04-typography.md#specifications--parameters)).
3. **Color** — OKLCH ramps, semantic map (light + dark), verified contrast pairs with
   ratios ([doc 05](./05-color.md#specifications--parameters)).
4. **Layout & Grid** — column count, `--content-max`, breakpoints (exact px), editorial
   presets used ([doc 03](./03-layout.md#specifications--parameters)).
5. **Spacing & Rhythm** — scale adoption (canonical §3.5 or documented deviation),
   fluid recipes, planned grid-breaks ([doc 06](./06-spacing.md#specifications--parameters)).
6. **Imagery & Asset Direction** — style anchor, consistency kit, treatment recipes,
   output matrix ([doc 02](./02-image-generation.md#specifications--parameters)).
7. **Components** — inventory; per component: token bindings (semantic/component tier
   names only — no raw values).
8. **Motion Language** — summary only: personality + intensity restated from §1, pinned
   eases (GSAP names), duration-class values, smooth-scroll + page-transition decisions;
   the full choreography contract lives in `motion-spec.md` (§4 schema below) — this
   section points there, never duplicates its tables.
9. **Accessibility Notes** — contrast results, reduced-motion policy reference, focus
   and keyboard expectations.
10. **Performance Budget** — the project's budget numbers against the canonical table in
    [doc 09](./09-tech-implementation.md#specifications--parameters) (anchors:
    `_conventions.md` §3.8); measurement method + gates live in `implementation-plan.md`
    §2 (§5 schema below).
11. **Provenance & Confidence** — REQUIRED in `recreate` (this is the "recreate report"
    referenced by [doc 03](./03-layout.md#mode-specific-guidance)); in `modify` it holds
    the drift-audit result; in `create` it lists `assumed` items only.
    - Per-dimension confidence table — one row per dimension:
      `archetype`, `typography`, `color`, `layout`, `spacing`, `imagery`, `motion`,
      `webgl-stack`. Columns: confidence (`high` | `medium` | `low`), provenance
      (`measured` | `inferred` | `assumed`), evidence (1 line), snap deltas (e.g.
      "gutter measured 22 px → snapped `space.6` (24), Δ +2 px").
    - `low` confidence ⇒ the affected values carry `UNVERIFIED — confirm before use`.
12. **Changelog** — one entry per version: semver, date, diffs summary, rationale.

### 3. `design-tokens.tokens.json` — schema rules

- DTCG 2025.10 syntax (`_facts.md` §3): token = object with required `$value`, plus
  `$type`, optional `$description` / `$extensions`; alias syntax `"{group.token}"`.
- Three tiers per `_conventions.md` §3.7: primitive → semantic → component. Semantic and
  component tokens alias, never restate, primitive values.
- Top-level groups: `color` (format owned by [doc 05](./05-color.md#specifications--parameters)),
  `font` ([doc 04](./04-typography.md#specifications--parameters)), `type` (primitive
  fluid scale steps `type.step.{N}`, owned by
  [doc 04](./04-typography.md#specifications--parameters); `$value` = clamp max, fluid
  min + viewport range in `$extensions["agent.fluid"]`), `typography` (DTCG composite
  role tokens, e.g. `typography.h1` — their `fontSize` MUST alias `{type.step.N}`,
  never restate sizes), `space` (dimension
  `$value` objects `{"value": n, "unit": "px"}` —
  [doc 06](./06-spacing.md#code-examples)), `motion` (durations + eases; canonical
  values from [doc 07](./07-animation-choreography.md#specifications--parameters)),
  plus component groups (`button`, `card`, …).
- Motion token types (DTCG 2025.10): `$type: "duration"` with `$value`
  `{"value": 350, "unit": "ms"}` (units `ms` | `s`); `$type: "cubicBezier"` with
  `$value` `[P1x, P1y, P2x, P2y]` (x in [0,1]).
- **Root metadata block** (DTCG defines NO root version field — metadata goes in
  `$extensions`): root-group `$extensions["agent.meta"]` with REQUIRED keys
  `version` (semver string), `mode`, `archetype`, `personality`, `intensity`,
  `generated` (ISO date), and — in `recreate` — `confidence` (the §2.11 per-dimension
  map). The spec recommends reverse-domain extension keys; this KB standardizes on the
  `agent.*` namespace already used by doc 06 (`agent.fluid`).

Semver mapping for token-file changes (Principle 5):

| Change | Bump |
|---|---|
| Remove or rename a token; change a primitive that ≥1 semantic alias depends on; change scale base, type ratio, grid columns, archetype or personality | MAJOR |
| Add tokens/groups; add a theme file; add aliases; deprecate-by-alias (never delete — [doc 06 rule](./06-spacing.md#mode-specific-guidance)) | MINOR |
| Value nudge that keeps all references and bands intact (e.g. OKLCH L +0.02 to pass a contrast gate); `$description` / `$extensions` edits | PATCH |

### 4. `motion-spec.md` — section schema (exact, ordered)

1. **Motion Identity** — personality token + intensity tier (must equal the spec §2.1
   values), four duration-class values chosen from the personality slices
   ([doc 01](./01-visual-motion.md#specifications--parameters)).
2. **Easing & Duration Tokens** — 2 primary eases + max 1 accent from the canonical
   table ([doc 07](./07-animation-choreography.md#specifications--parameters)), with
   GSAP names AND `cubic-bezier()` values; token names as registered in
   `design-tokens.tokens.json` `motion.*`.
3. **Choreography Inventory** — one row per pattern: id, trigger (load / scroll /
   hover / click / route), targets, from → to (numeric transform/opacity start/end
   states), duration (ms), ease token, stagger (ms/item), overlap (% of previous tween).
4. **Scroll Behavior** — native vs Lenis; if Lenis: `lerp` value + full options;
   scroll scenes (pin / scrub / snap / labels); one-Lenis-instance rule
   ([doc 07](./07-animation-choreography.md#mode-specific-guidance)).
5. **Page Transitions** — View Transitions API usage (support matrix: `_facts.md` §3)
   + non-supporting-browser fallback behavior.
6. **Reduced-Motion Variants** — REQUIRED: one mapping per Choreography Inventory row
   (canonical collapse pattern:
   [doc 07](./07-animation-choreography.md#specifications--parameters)).
7. **Performance Notes** — transform/opacity-only confirmation (zero CLS), input
   feedback ≤ 200 ms (INP guard, `_conventions.md` §3.8).

### 5. `implementation-plan.md` — section schema (exact, ordered)

1. **Stack Decision** — framework + libraries with versions from `_facts.md` ONLY;
   WebGL rung chosen + ruled-out lighter rungs
   ([doc 08](./08-webgl-effects.md#decision-framework)); rationale per
   [doc 09](./09-tech-implementation.md#decision-framework).
2. **Performance Budgets** — the project's numbers against the canonical table in
   [doc 09](./09-tech-implementation.md#specifications--parameters) (anchors: LCP
   ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 at p75; WebGL < 100 draw calls).
3. **Build Phases** — ordered phases with exit criteria: tokens → layout shell →
   typography/color application → components → motion pass → WebGL layer (if any) →
   polish/QA. Each phase exits only when its owner doc's Quality Checklist passes.
4. **Asset Pipeline** — fonts, images, 3D assets: formats, budgets, commands
   ([doc 02](./02-image-generation.md#specifications--parameters) +
   [doc 09](./09-tech-implementation.md#specifications--parameters)).
5. **Accessibility Plan** — reduced-motion coverage, contrast gate, keyboard/focus,
   per [doc 09](./09-tech-implementation.md#specifications--parameters) practices.
6. **Testing & Verification Gates** — which checklists run when; CWV measurement
   method; device tiers.
7. **Risks & Open Questions** — every `UNVERIFIED — confirm before use` item carried
   forward, with the verification step that would resolve it.

### 6. Runtime detection signatures (`recreate` mode — all verified 2026-06-12)

Run AFTER full load + one scroll/interaction pass (code-split libraries load lazily;
re-run after navigation). Versions named below are current per `_facts.md`.

| Target | Runtime signal | Caveats |
|---|---|---|
| GSAP core (3.15.0 current) | `window.gsap.version`; `window.gsapVersions` (array of every loaded instance) | Installs onto `window` even from ESM imports — UNLESS the site defines `window.GreenSockGlobals` (rare opt-out) |
| GSAP plugins | `window.ScrollTrigger?.version`, `window.SplitText`, etc. | Registered plugins are exposed on the same install scope; ScrollTrigger self-registers when it finds a window gsap |
| Lenis (1.3.23 current) | `window.lenisVersion`; `window.lenis.version`; root-element classes `lenis`, `lenis-smooth`, `lenis-scrolling`, `lenis-stopped`, `lenis-locked`, `lenis-autoToggle`; `[data-lenis-prevent]` attributes | Classes sit on `<html>` for window scroll, on the wrapper for nested scroll |
| three.js (r184 current) | `window.__THREE__` = revision string (e.g. `"184"`) | Set even in bundled apps. Absent + `<canvas>` present → search bundles (DevTools Sources) for the literal `"Multiple instances of Three.js"`, else suspect OGL/PixiJS (no verified global — bundle-string search only) |
| Next.js (Pages Router) | `window.__NEXT_DATA__` + inline `<script id="__NEXT_DATA__">`; `window.next`; `/_next/static/` asset paths | |
| Next.js (App Router) | Inline `self.__next_f.push()` scripts (serialized RSC payload); `window.next` without `__NEXT_DATA__` | |
| Nuxt | `<div id="__nuxt">` (default `app.rootId`); `window.__NUXT__` | Since Nuxt 3.4, `window.__NUXT__` is not populated until app init — check after hydration |
| Astro | `<meta name="generator" content="Astro vX.Y.Z">` (via `Astro.generator`) | Template-supplied; absence does not rule Astro out |
| View Transitions usage | `::view-transition*` / `@view-transition` rules in stylesheets | Audit in Chrome ≥ 126: Firefox has no cross-document support (`_facts.md` §3) |

Negative results are evidence of absence of the SIGNAL, not of the library. Record
detection output verbatim in spec §11 (Provenance & Confidence).

## Recommended Libraries & Tools

No new runtime dependencies — this doc consumes versions already pinned in `_facts.md`
(GSAP 3.15.0, Lenis 1.3.23, three 0.184.0/r184) as detection targets. Audit tooling:

| Task | Tool | Where its method is specified |
|---|---|---|
| Library/framework fingerprinting | DevTools console + Code Example A below | §6 table |
| Grid/spacing/type extraction | DevTools computed styles, grid overlay | [doc 03](./03-layout.md#mode-specific-guidance), [doc 04](./04-typography.md#mode-specific-guidance), [doc 06](./06-spacing.md#mode-specific-guidance) |
| Motion timing/easing capture | DevTools Performance panel + computed `transition-*` | [doc 07](./07-animation-choreography.md#mode-specific-guidance) |
| WebGL frame capture, draw-call count, shader read | Spector.js | [doc 08](./08-webgl-effects.md#mode-specific-guidance) |
| Token file conventions | DTCG 2025.10: `.tokens.json`, media type `application/design-tokens+json` | `_facts.md` §3 |

## Code Examples

**A — detection script** (paste into the DevTools console on the target site; signals
verified against the published packages, see Sources):

```js
// recreate-mode fingerprint. Run after full load + one scroll pass; re-run after a
// client-side navigation (code-split bundles register late).
const sig = {
  gsap: window.gsap?.version,                 // gsap self-installs on window even from ESM
  gsapAll: window.gsapVersions,               // every gsap instance loaded (array)
  scrollTrigger: window.ScrollTrigger?.version, // registered plugins land on the install scope
  splitText: !!window.SplitText,
  lenis: window.lenisVersion ?? window.lenis?.version, // lenis@1.x writes both
  lenisActive: document.documentElement.classList.contains('lenis'), // html.lenis = window-scroll instance
  three: window.__THREE__,                    // revision string, e.g. "184" (= r184)
  nextPages: !!window.__NEXT_DATA__,          // Pages Router payload
  nextApp: !!window.next && !window.__NEXT_DATA__, // App Router: also see self.__next_f inline scripts
  nuxt: !!document.getElementById('__nuxt'),  // default app.rootId; window.__NUXT__ only after init (≥3.4)
  astro: document.querySelector('meta[name="generator"]')?.content ?? null, // "Astro vX.Y.Z" if kept
  canvases: [...document.querySelectorAll('canvas')].map(c => `${c.width}x${c.height}`),
};
console.table(sig); // paste the verbatim output into spec §11 (Provenance & Confidence)
```

**B — token-file root metadata + motion group** (DTCG 2025.10; full skeleton:
[./templates/design-tokens.tokens.json](./templates/design-tokens.tokens.json)):

```json
{
  "$description": "Project design tokens. Schema: doc 10 §3. Color: doc 05. Space: doc 06.",
  "$extensions": {
    "agent.meta": {
      "version": "1.1.0",
      "mode": "recreate",
      "archetype": "kinetic-minimal",
      "personality": "fluid",
      "intensity": "responsive",
      "generated": "2026-06-12",
      "confidence": {
        "archetype": "high", "typography": "high", "color": "high", "layout": "high",
        "spacing": "medium", "imagery": "medium", "motion": "medium", "webgl-stack": "high"
      }
    }
  },
  "motion": {
    "duration": {
      "$type": "duration",
      "ui":     { "$value": { "value": 350, "unit": "ms" } },
      "reveal": { "$value": { "value": 600, "unit": "ms" } }
    },
    "ease": {
      "$type": "cubicBezier",
      "out":   { "$value": [0.165, 0.84, 0.44, 1],  "$description": "power3.out — canonical table: doc 07" },
      "in-out": { "$value": [0.645, 0.045, 0.355, 1], "$description": "power2.inOut" }
    }
  }
}
```

Durations above sit in the `fluid` slices (UI 300–400 ms, reveal 450–650 ms) per
[doc 01 §2](./01-visual-motion.md#specifications--parameters).

## Mode-Specific Guidance

### Create from scratch

1. **Brief intake.** Extract: 3–5 brand adjectives, audience + device profile, content
   ratio (long-form % vs visual %), conversion criticality, asset/3D budget, a11y
   regime. Missing answers are recorded as `assumed` (Principle 4).
2. **Direction.** Run the [doc 01 Decision Framework](./01-visual-motion.md#decision-framework)
   → one archetype + one personality + one intensity tier + 5–8 signals + the signature
   interaction. Write spec §1 immediately.
3. **Tokens first.** Initialize `design-tokens.tokens.json` at `1.0.0` with the §3
   metadata block; adopt the canonical spacing scale
   ([doc 06](./06-spacing.md#mode-specific-guidance)) before any visual work.
4. **Type / color / spacing.** In this order: type scale + loading plan
   ([doc 04](./04-typography.md#mode-specific-guidance)) → OKLCH ramps + semantic map +
   contrast gate ([doc 05](./05-color.md#mode-specific-guidance)) → rhythm + fluid
   recipes ([doc 06](./06-spacing.md#mode-specific-guidance)). Emit spec §§2–5 and the
   corresponding token groups as you go.
5. **Layout.** Grid, breakpoints, editorial presets
   ([doc 03](./03-layout.md#mode-specific-guidance)); spec §4.
6. **Motion language.** Lock eases + duration-class values + Lenis decision + the
   reduced-motion pattern in the FIRST motion commit
   ([doc 07](./07-animation-choreography.md#mode-specific-guidance)); emit
   `motion-spec.md` (§4 schema) + the spec §8 summary, fill the Choreography Inventory
   as patterns are designed.
7. **Optional WebGL.** Only via the [doc 08 Decision Framework](./08-webgl-effects.md#decision-framework);
   record the rung + ruled-out lighter rungs in `implementation-plan.md` §1; imagery
   direction per [doc 02](./02-image-generation.md#mode-specific-guidance) (spec §6).
8. **Implementation plan.** Stack, budgets, phases, pipeline, gates per
   [doc 09](./09-tech-implementation.md#mode-specific-guidance) → emit
   `implementation-plan.md` (§5 schema). Engagement is done when the §Quality Checklist
   below passes.

### Re-create from existing site (reverse-engineering)

Order: fingerprint → measure → classify → reconstruct. Never reconstruct from memory of
"sites like this" — only from recorded measurements.

1. **Scope.** Pick 3–5 representative pages (home, one content page, one index/listing,
   one interactive showpiece). All sampling below runs on these.
2. **Fingerprint the stack.** Run Code Example A + the §6 table; record verbatim output
   in spec §11. Check `/_next/static/`-style asset paths and bundle-string searches for
   negatives.
3. **Extract per domain** (each domain doc's audit recipe lives under its
   `## Mode-Specific Guidance` heading):
   - Layout/grid dump + breakpoints + clamp reconstruction —
     [doc 03](./03-layout.md#mode-specific-guidance).
   - Computed type scale at 320/768/1440, families, variable axes —
     [doc 04](./04-typography.md#mode-specific-guidance).
   - Computed colors → OKLCH clustering → ramp fit; flag (never copy) failing contrast
     pairs — [doc 05](./05-color.md#mode-specific-guidance).
   - Spacing samples at 375/768/1440 → cluster → snap to `space.{n}` (±2 px), log
     deltas — [doc 06](./06-spacing.md#mode-specific-guidance).
   - Imagery slots, ratios, treatments — [doc 02](./02-image-generation.md#mode-specific-guidance).
   - Motion timings/eases: computed `transition-*`, Performance-panel tween spans, snap
     to nearest canonical ease; Lenis lerp estimate; scroll scenes —
     [doc 07](./07-animation-choreography.md#mode-specific-guidance).
   - WebGL: Spector.js capture → effect catalog mapping —
     [doc 08](./08-webgl-effects.md#mode-specific-guidance).
4. **Classify.** Score archetype signals (≥4 = classification) and derive personality
   from the median measured duration per
   [doc 01](./01-visual-motion.md#mode-specific-guidance).
5. **Reconstruct.** Emit all four artifacts at version `1.0.0`: clean tokens (snapped,
   not raw measurements), spec with §11 fully populated (confidence + provenance + snap
   deltas), motion-spec re-specified in canonical vocabulary, implementation plan for
   the REBUILD stack (chosen per [doc 09](./09-tech-implementation.md#decision-framework) —
   not necessarily the source stack).
6. **Gap policy.** Unobservable values (e.g. hover states behind auth, font licensing)
   → `assumed` + `UNVERIFIED — confirm before use`; never present a guess as a measurement.

**Extraction checklist** (all boxes before reconstruction starts):

- [ ] 3–5 pages scoped; viewport sample widths fixed (320/375/768/1440)
- [ ] Detection script output recorded verbatim (Code Example A) + §6 caveats checked
- [ ] Grid: columns, gutters, margins, `--content-max`, breakpoints (exact px) — [doc 03](./03-layout.md#mode-specific-guidance)
- [ ] Type: sizes per role at 3 widths, ratio, families, weights, line-heights, `font-display` — [doc 04](./04-typography.md#mode-specific-guidance)
- [ ] Color: full computed-color harvest → OKLCH clusters → ramp fit + contrast audit — [doc 05](./05-color.md#mode-specific-guidance)
- [ ] Spacing: clusters snapped, off-scale repeats (≥3×) recorded as project tokens, fluid clamps solved — [doc 06](./06-spacing.md#mode-specific-guidance)
- [ ] Imagery: slot inventory, aspect ratios, formats, treatment parameters — [doc 02](./02-image-generation.md#mode-specific-guidance)
- [ ] Motion: ≥5 interactions measured (duration + ease + stagger), smooth-scroll lerp estimate, scroll scenes mapped, page-transition mechanism identified — [doc 07](./07-animation-choreography.md#mode-specific-guidance)
- [ ] WebGL: canvas inventory, draw calls, effects mapped to catalog rows with parameters — [doc 08](./08-webgl-effects.md#mode-specific-guidance)
- [ ] Archetype scored (≥4 signals) + personality from median duration — [doc 01](./01-visual-motion.md#mode-specific-guidance)
- [ ] Every dimension has confidence + provenance; every `assumed` value flagged

### Modify an existing system

1. **Ingest.** Load all four artifacts. Missing artifacts → reconstruct via `recreate`
   first (Decision Framework). Note the current token-file version.
2. **Drift audit.** Verify artifacts against the live build with `recreate` spot-checks
   (one per dimension). Document drift in spec §11 — never modify on top of stale docs.
3. **Assess against the quality bar.** Run the Quality Checklist of every domain doc
   the change touches. Pre-existing failures: list in spec §11; fixing them is a
   separate, explicitly-scoped diff (no silent scope creep).
4. **Propose diffs before applying.** One row per change:
   `path` (token or spec section) · `current` → `proposed` (numbers) · rationale ·
   semver class (§3 table) · blast radius (count of aliasing tokens + affected
   components) · checks to re-run. Diffs must preserve consistency per each doc's
   modify rules: derive from existing bands ([doc 01](./01-visual-motion.md#mode-specific-guidance)),
   no second easing vocabulary ([doc 07](./07-animation-choreography.md#mode-specific-guidance)),
   alias-don't-delete ([doc 06](./06-spacing.md#mode-specific-guidance)), re-run contrast
   on transitively affected pairs ([doc 05](./05-color.md#mode-specific-guidance)),
   no second WebGL context ([doc 08](./08-webgl-effects.md#mode-specific-guidance)).
5. **Version + document.** Apply diffs; bump `$extensions["agent.meta"].version` by the
   HIGHEST semver class among applied diffs; append a spec §12 changelog entry (version,
   date, diff table reference, rationale).
6. **Regression gates.** Re-run the touched docs' Quality Checklists + the affected
   measurements (e.g. grid dumps before/after per
   [doc 03](./03-layout.md#mode-specific-guidance); draw calls/frame time per
   [doc 08](./08-webgl-effects.md#mode-specific-guidance) — >10% regression needs
   sign-off).

## Quality Checklist

- [ ] Mode selected via the Decision Framework and recorded in every artifact's
      metadata; any mid-engagement escalation logged with its trigger rule.
- [ ] All four artifacts emitted, matching the §§2–5 schemas section-for-section and
      the `./templates/` skeletons.
- [ ] Spec §1 carries exactly one archetype token, one personality token, one intensity
      tier, 5–8 numeric signals, and one signature interaction.
- [ ] Token file: valid DTCG 2025.10 ([gate rules](./05-color.md#quality-checklist),
      [doc 06](./06-spacing.md#quality-checklist)); `.tokens.json` extension; root
      `agent.meta` block complete; semantic/component tiers alias primitives only.
- [ ] Token-file version is correct semver: `1.0.0` for `create`/`recreate`; `modify`
      bump equals the highest diff class in the changelog.
- [ ] motion-spec: every Choreography Inventory row has a Reduced-Motion variant; all
      durations sit inside the personality slices.
- [ ] `recreate`: spec §11 has all 8 confidence rows with provenance + evidence; every
      `assumed`/`low` value carries `UNVERIFIED — confirm before use`; zero copied
      code/shaders/assets.
- [ ] `modify`: drift audit documented; diff table present with blast radius; changelog
      appended (no history rewritten).
- [ ] implementation-plan budgets match `_conventions.md` §3.8 anchors or document a
      stricter project value.
- [ ] Every cross-reference in the artifacts points at an existing doc/anchor.

## Anti-Patterns

1. **Pixel-cloning instead of system inference** (`recreate`) — shipping raw measured
   values (22 px gutters, 17.3 px font sizes) instead of snapped tokens + logged
   deltas. The deliverable is the SYSTEM, not a screenshot diff.
2. **Copying implementation** (`recreate`) — lifting shader code, minified JS, font
   files, or imagery from the source site. License exposure; clean-room only.
3. **Guesses presented as measurements** — a value without provenance, or a `low`
   confidence dimension without the `UNVERIFIED` flag, poisons every downstream mode.
4. **Unversioned modification** — editing `design-tokens.tokens.json` without a semver
   bump + changelog entry. Consumers cannot detect the change class; treat as a build
   breaker.
5. **MAJOR smuggled as PATCH** — renaming a token or shifting a primitive with aliases
   and calling it a fix. Use the §3 table; blast radius decides, not intent.
6. **Mode drift** — a `modify` that quietly re-decides archetype/personality, or a
   `recreate` that "improves" the direction mid-extraction. Escalate explicitly per the
   Decision Framework.
7. **Artifact rot** — building features the spec doesn't describe, or leaving the spec
   describing things the build no longer does. Drift audit (modify step 2) exists
   because this is the default failure mode.
8. **Detection-script blind faith** — concluding "no GSAP" from a missing global on a
   `GreenSockGlobals`-scoped or pre-interaction page. Negatives require the §6 caveat
   checks + bundle-string search.
9. **Inheriting source defects** (`recreate`) — copying contrast failures, scroll-jack,
   or missing reduced-motion because "the original does it". The quality bar is
   mode-independent (Principle 6).
10. **Adjective specs in artifacts** — "generous spacing", "smooth easing". Artifacts
    accept numbers and token references only.

## Sources & Verification

- https://unpkg.com/gsap@3.15.0/gsap-core.js — confirmed: `_install(_installScope || _win.GreenSockGlobals || !_win.gsap && _win || {})` installs GSAP globals onto `window` unless `GreenSockGlobals` is defined; every instance pushes to `window.gsapVersions` (verified 2026-06-12)
- https://unpkg.com/gsap@3.15.0/ScrollTrigger.js — confirmed: `ScrollTrigger.version = "3.15.0"`; auto-registration via `_getGSAP() && gsap.registerPlugin(ScrollTrigger)`, exposing the plugin on the window install scope (verified 2026-06-12)
- https://unpkg.com/lenis@1.3.23/dist/lenis.mjs — confirmed: `window.lenisVersion = version` and `window.lenis.version`; root-element classes `lenis`, `lenis-autoToggle`, `lenis-stopped`, `lenis-locked`, `lenis-scrolling`, `lenis-smooth` (verified 2026-06-12)
- https://github.com/darkroomengineering/lenis/blob/main/README.md — confirmed: `data-lenis-prevent` attribute family; recommended stylesheet `lenis/dist/lenis.css` (verified 2026-06-12)
- https://github.com/darkroomengineering/lenis/blob/main/packages/core/lenis.css — confirmed: stylesheet targets `html.lenis`, `.lenis-stopped`, `.lenis-smooth iframe` (verified 2026-06-12)
- https://unpkg.com/three@0.184.0/build/three.core.js — confirmed: sets `window.__THREE__ = REVISION` and warns `"Multiple instances of Three.js being imported."` (verified 2026-06-12)
- https://unpkg.com/three@0.184.0/src/constants.js — confirmed: `REVISION = '184'` for three 0.184.0 (verified 2026-06-12)
- https://webreveal.io/blog/how-to-tell-if-a-website-uses-nextjs.html — confirmed: `window.__NEXT_DATA__` (Pages Router), `window.next` runtime object, `/_next/static/` asset paths as Next.js fingerprints (verified 2026-06-12)
- https://github.com/vercel/next.js/discussions/42170 — confirmed: App Router pages embed inline `self.__next_f.push()` scripts carrying the serialized RSC payload (verified 2026-06-12)
- https://nuxt.com/docs/api/nuxt-config — confirmed: Nuxt `app.rootId` default is `"__nuxt"` (root `<div id="__nuxt">`) (verified 2026-06-12)
- https://nuxt.com/blog/v3-4 — confirmed: since Nuxt 3.4 the payload is no longer available on `window.__NUXT__` immediately; it is parsed during app initialization (verified 2026-06-12)
- https://docs.astro.build/en/reference/api-reference/ — confirmed: `Astro.generator` renders `<meta name="generator" content="Astro vX.Y.Z">` with the running Astro version (verified 2026-06-12)
- https://www.designtokens.org/TR/2025.10/format/ — confirmed: `duration` `$value` = `{value, unit}` with units `ms`/`s`; `cubicBezier` `$value` = `[P1x, P1y, P2x, P2y]`; no root-level version field (metadata via `$extensions`); reverse-domain notation recommended for `$extensions` keys (verified 2026-06-12)
- https://semver.org/ — confirmed: increment MAJOR for incompatible API changes, MINOR for backward-compatible functionality, PATCH for backward-compatible bug fixes (verified 2026-06-12)
