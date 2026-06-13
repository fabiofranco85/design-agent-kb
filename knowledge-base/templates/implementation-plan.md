---
project: <project-name>
artifact: implementation-plan
version: 1.0.0             # semver — create/recreate emit 1.0.0; modify bumps per ../10-modes-and-artifacts.md §3
date: <YYYY-MM-DD>
mode: <create | recreate | modify>
stack: <e.g. next | astro | nuxt | vanilla-vite>
intensity: <ambient | responsive | showcase>
---

<!--
TEMPLATE — implementation-plan.md
Section schema owner: ../10-modes-and-artifacts.md#specifications--parameters (§5 — exact
section names and order; this skeleton implements that schema, never the reverse).
The agent fills this skeleton for every project. Rules:
  • Versions below are pre-filled from ../_facts.md (all verified 2026-06-12).
    RE-VERIFY EVERY VERSION AT PROJECT START against the npm registry; update this table
    and ../_facts.md together. NEVER add a version that is not in ../_facts.md without
    flagging it: UNVERIFIED — confirm before use.
  • Keep only the library rows the project actually uses; delete the rest.
  • Budgets are pass/fail gates, not aspirations (_conventions.md §3.8 anchors).
-->

# Implementation Plan — <project-name>

## 1. Stack Decision

<!-- Justify against content type, team, hosting, and the intensity tier from
     design-system-spec.md — selection rules: ../09-tech-implementation.md#decision-framework.
     Framework versions from ../_facts.md §4. The WebGL rung row is REQUIRED: record the
     rung chosen AND the ruled-out lighter rungs (../08-webgl-effects.md#decision-framework). -->

| Layer | Choice | Version (verified 2026-06-12 — re-verify at project start) | Rationale |
|---|---|---|---|
| Framework | <`next` 16.2.9 \| `astro` 6.4.6 \| `nuxt` 4.4.8 \| vanilla + bundler> | <version> | <1 sentence> |
| UI runtime | <`react` 19.2.7 \| none \| other> | <version> | <note: @react-three/fiber 9.6.1 requires react >=19 <19.3> |
| CMS | <`@sanity/client` 7.22.1 \| `storyblok-js-client` 7.6.1 \| `contentful` 11.12.4 \| `@prismicio/client` 7.21.8 \| none> | <version> | <1 sentence> |
| WebGL rung | <rung per ../08-webgl-effects.md#decision-framework \| none> | — | <ruled-out lighter rungs + why each is insufficient> |
| Hosting / CDN | <choice> | — | <edge caching, image CDN notes> |
| Rendering strategy | <SSG \| SSR \| hybrid> | — | <per-route notes> |

### Libraries & verified versions

> All versions verified 2026-06-12 in ../_facts.md — **re-verify at project start**
> (`npm view <pkg> version`). Install commands and import paths are binding; do not
> re-derive them. Delete unused rows.

#### Animation & scroll (specs: ../07-animation-choreography.md#recommended-libraries--tools)

| Library | Version | Install | Import | Notes |
|---|---|---|---|---|
| GSAP | **3.15.0** | `npm install gsap` | `import gsap from "gsap"`; plugins e.g. `import { ScrollTrigger } from "gsap/ScrollTrigger"` + `gsap.registerPlugin(ScrollTrigger)` | 100% free incl. all former Club plugins (SplitText, MorphSVG, ScrollSmoother, DrawSVG, CustomEase). Proprietary no-charge license, not MIT; no embedding in no-code animation builders competing with Webflow |
| Lenis | **1.3.23** | `npm install lenis` | `import Lenis from "lenis"` + `import "lenis/dist/lenis.css"` | Package is `lenis` — NOT deprecated `@studio-freight/lenis`. Canonical ScrollTrigger wiring: ../07-animation-choreography.md#code-examples |
| Motion | **12.40.0** | `npm install motion` | `import { motion } from "motion/react"` (vanilla: `import { animate } from "motion"`) | Formerly Framer Motion; migrate imports `"framer-motion"` → `"motion/react"` |
| Barba.js | 2.10.3 | — | — | **DORMANT (last publish 2024-08-12) — do not adopt.** Use View Transitions API + GSAP fallback |

#### WebGL / 3D (only if intensity/archetype requires a canvas — ../08-webgl-effects.md#decision-framework)

| Library | Version | Install | Import | Notes |
|---|---|---|---|---|
| three.js | **0.184.0 (r184)** | `npm install three` | `"three"`, `"three/webgpu"`, `"three/tsl"`, `"three/addons/*"` | WebGPURenderer still officially experimental; automatic WebGL2 fallback |
| @react-three/fiber | **9.6.1** | `npm install three @react-three/fiber` | `"@react-three/fiber"` | Requires react >=19 <19.3; v10 is alpha-only — do not adopt |
| @react-three/drei | **10.7.7** | `npm install @react-three/drei` | `"@react-three/drei"` | peerDeps react ^19, fiber ^9; v11-alpha ↔ fiber v10 pairing UNVERIFIED — confirm before use |
| postprocessing | **6.39.1** | `npm install postprocessing` | `"postprocessing"` | Zlib; peer `three >= 0.168 < 0.185` (covers r184). v7-beta WebGPU details UNVERIFIED — confirm before use |
| PixiJS | **8.19.0** | `npm install pixi.js` | `"pixi.js"` | 2D GPU canvas; WebGL renderer recommended, WebGPU experimental |
| OGL | **1.0.11** | `npm install ogl` | `"ogl"` | Minimal WebGL alternative for single-effect accents (slow release cadence) |

#### Asset pipeline

| Tool | Version | Install | Notes |
|---|---|---|---|
| @gltf-transform/cli | **4.4.0** | `npm install -D @gltf-transform/cli` | glTF optimization (see §4) |
| <image pipeline: framework-native / CDN> | <version \| n/a> | <install \| —> | <AVIF/WebP encodes — specs: ../02-image-generation.md#specifications--parameters> |

## 2. Performance Budgets

<!-- Anchors pinned in _conventions.md §3.8; canonical budget table (per-metric rows incl.
     3D/transfer budgets): ../09-tech-implementation.md#specifications--parameters.
     Core Web Vitals "good" at p75 per ../_facts.md §3. Measure in the field (CrUX/RUM)
     plus lab (Lighthouse, 4× CPU throttle, mid-tier mobile). -->

| Metric | Budget | Gate | Measured |
|---|---|---|---|
| LCP (p75) | < 2.5 s | hard | <value> |
| INP (p75) | < 200 ms | hard | <value> |
| CLS (p75) | < 0.1 | hard | <value> |
| WebGL draw calls | < 100 | hard ceiling 150 | <value \| n/a> |
| Initial JS (gzip) | <KB — set per stack> | project | <value> |
| Font payload (subset woff2) | <KB> | project | <value> |
| Hero media weight | <KB> | project | <value> |
| 3D assets desktop / mobile | <KB / KB ≈ ¼ desktop> | project | <value \| n/a> |
| Total page weight (landing) | <KB> | project | <value> |

Breach protocol: a hard-gate breach drops the intensity tier one level before any
archetype change (conflict rule: ../01-visual-motion.md#specifications--parameters).

## 3. Build Phases

<!-- Phase order is binding (../10-modes-and-artifacts.md §5): tokens → layout shell →
     typography/color application → components → motion pass → WebGL layer (if any) →
     polish/QA. Each phase exits ONLY when its owner doc's Quality Checklist passes.
     Tokens and the reduced-motion branch land in P1, not at the end
     (../07-animation-choreography.md#mode-specific-guidance). Add dates/owners. -->

| # | Phase | Contents | Exit criteria | Target date |
|---|---|---|---|---|
| P0 | Direction lock | archetype + personality + intensity in design-system-spec.md; version re-verification of §1 | frontmatter tokens signed off; versions re-verified | <date> |
| P1 | Foundations | `design-tokens.tokens.json` (+ dark override) emitted → CSS custom properties; grid; type scale; Lenis recipe + canonical reduced-motion pattern wired | tokens parse + contrast gate passes both themes; `reduce` path renders | <date> |
| P2 | Components | design-system-spec.md §7 component inventory built on tokens; states + focus styles | every visual value resolves to a token; focus ≥ 3:1 | <date> |
| P3 | Pages & choreography | page templates; motion-spec.md rows M-xx implemented; scroll scenes S-xx; page transitions | motion-spec.md §7 Performance Notes all pass | <date> |
| P4 | <WebGL layer \| delete if none> | canvas scenes, per-device asset tiers (mobile ≈ ¼ desktop) | draw calls < 100; §2 budgets hold on mid-tier mobile | <date> |
| P5 | Hardening & launch | §6 gates, perf passes, a11y audit (§5), content load | all §2 budgets green at p75; zero UNVERIFIED items open | <date> |

## 4. Asset Pipeline

<!-- Commands become package.json scripts. Export/format specs are owned by
     ../02-image-generation.md#specifications--parameters; type loading by
     ../04-typography.md#specifications--parameters; model/texture compression commands by
     ../09-tech-implementation.md#specifications--parameters (§3 — CANONICAL). -->

- **Fonts:** subset to <unicode ranges> → woff2; `font-display: <swap | optional>`; preload <list>.
- **Images:** source <format> → AVIF + WebP (+ fallback) at <breakpoint widths>; LCP image preloaded, explicit `width`/`height` (CLS).
- **Video:** <codec/ladder, poster frames, autoplay policy | none>.
- **3D (if used):** one-shot: `gltf-transform optimize <in.glb> <out.glb> --compress draco --texture-compress ktx2 --texture-size 2048` (CLI 4.4.0); two-pass UASTC/ETC1S codec-rule variant + full script: ../09-tech-implementation.md#specifications--parameters. Per-device tiers <desktop/mobile targets>; pre-bake over real-time wherever possible (Lusion pattern, ../01-visual-motion.md#core-principles).
- **Tokens:** `design-tokens.tokens.json` → CSS custom properties build step (dots → hyphens transform, fluid clamp composition from `$extensions` — ../06-spacing.md#code-examples). Validate JSON in CI: `python3 -m json.tool design-tokens.tokens.json`.
- **CI checks:** <lint, type-check, token validation, Lighthouse CI budget file, link check>.

## 5. Accessibility Plan

<!-- Canonical practice list: ../09-tech-implementation.md#specifications--parameters (§4);
     contrast owner ../05-color.md; reduced-motion pattern owner
     ../07-animation-choreography.md. Commitments here are verified at the §6 gates. -->

- **Reduced-motion coverage:** canonical pattern wired in P1 (../07-animation-choreography.md#code-examples); every motion-spec.md §3/§4/§5 row mapped in its §6; Lenis/parallax/pin+scrub never initialized under `reduce`.
- **Contrast gate:** every text + UI pair, both themes — body ≥ 4.5:1, large text/UI/focus ≥ 3:1 (_conventions.md §3.9); method ../05-color.md#code-examples; results recorded in design-system-spec.md §3.
- **Keyboard & focus:** all interactive elements reachable; `:focus-visible` restyled, never `outline: none` without replacement; roving tabindex in composite widgets; skip link <y/n>; route-change focus management per ../09-tech-implementation.md#code-examples.
- **Canvas/WebGL fallbacks:** fallback content inside every `<canvas>`; <DOM-mirrored content plan \| n/a>.
- **Zoom & text spacing:** layout survives 200% zoom + WCAG 1.4.12 overrides (../04-typography.md#quality-checklist).
- **Semantics:** <landmarks, heading order, form labels — project-specific notes>.

## 6. Testing & Verification Gates

<!-- Which checklists run when (phase exits, §3), CWV measurement method, device tiers.
     All pass/fail; run before launch. -->

- **CWV measurement method:** field (CrUX/RUM) at p75 where available; lab otherwise (Lighthouse, 4× CPU throttle, mid-tier mobile).
- **Device tiers:** <desktop spec / mid-tier mobile spec — must match the §2 asset tiers>.

- [ ] All §2 hard gates green at p75 (field data where available; lab on mid-tier mobile otherwise).
- [ ] Domain checklists pass: ../01-visual-motion.md#quality-checklist · ../03-layout.md#quality-checklist · ../04-typography.md#quality-checklist · ../05-color.md#quality-checklist · ../06-spacing.md#quality-checklist · ../07-animation-choreography.md#quality-checklist <· ../08-webgl-effects.md#quality-checklist if canvas>.
- [ ] Contrast gate re-run on final rendered colors, both themes (../05-color.md#code-examples).
- [ ] `prefers-reduced-motion: reduce` walked end-to-end in-browser: native scroll, no parallax/pins, content fully readable.
- [ ] Keyboard-only pass: every interactive element reachable, visible focus, no traps.
- [ ] 200% zoom + WCAG 1.4.12 text-spacing overrides: no overlap/clipping.
- [ ] Page transitions verified per browser incl. Firefox no-cross-document path (support matrix: ../_facts.md §3).
- [ ] `design-tokens.tokens.json` parses; uses `.tokens.json` extension; served/committed with `application/design-tokens+json` noted.
- [ ] Cross-artifact consistency: spec ↔ tokens ↔ motion-spec IDs ↔ build output (spot-check 10 values).
- [ ] Zero raw px spacing / raw hex colors in authored CSS (grep per ../06-spacing.md#quality-checklist).
- [ ] All UNVERIFIED items (§7) resolved or explicitly accepted by the client.

## 7. Risks & Open Questions

<!-- Carry forward EVERY "UNVERIFIED — confirm before use" item the project touches
     (from ../_facts.md and the other artifacts), each with the verification step that
     would resolve it, plus project risks. -->

| Item | Status | Action / verification step |
|---|---|---|
| <e.g. drei v11-alpha ↔ fiber v10 pairing> | UNVERIFIED — confirm before use | <pin to drei 10.7.7 / fiber 9.6.1> |
| <e.g. postprocessing v7-beta WebGPU support> | UNVERIFIED — confirm before use | <stay on 6.39.1> |
| <project-specific risk> | <status> | <mitigation> |
