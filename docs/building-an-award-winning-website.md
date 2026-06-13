# Building an Award-Winning Website with the Design-Systems Agent

An end-to-end playbook for taking a brief all the way to a shipped, Awwwards / FWA /
CSS-Design-Awards-caliber site — using the `design-systems-agent` skill for the design system,
then building, verifying, and shipping the rest.

> **The skill is stage 1 of 8.** It produces the *spec and tokens* — the system behind the
> site. This document is the bridge from that spec to a finished, award-grade site.

---

## The workflow in one screen

```
0. BRIEF ──► 1. DESIGN SYSTEM ──► 2. SCAFFOLD + ──► 3. BUILD UI ──► 4. MOTION ──► 5. WEBGL ──► 6. ASSETS ──► 7. VERIFY ──► 8. SHIP
   (decide)     (the skill →         TOKEN BRIDGE     (frontend-       (motion-      (only if      (pipeline)    (vs the       (deploy +
                 4 artifacts)         (tokens→CSS)      design skill)    spec.md)      spec needs)                 budget)       submit)
```

**Three rules make this efficient and award-grade — internalize them before you start:**

1. **Spec before pixels.** Get the *system* right first (it's cheap to iterate a token file;
   it's expensive to refactor colors/spacing/motion across a built site). Stage 1 is your
   highest-leverage hour.
2. **Tokens, never hardcoded values.** Every hex, px, duration, and easing in the build traces
   back to a token from `./design/design-tokens.tokens.json`. The moment you hardcode `#1a1a1a`
   or `24px`, the design system becomes a document instead of the source of truth, and drift
   begins. This single discipline is what keeps a complex site coherent.
3. **Verify against numbers, not vibes.** "Award-winning" is measured: Core Web Vitals,
   contrast ratios, reduced-motion behavior. Check them *at every phase*, not at the end.

---

## What "award-winning" actually requires

Awwwards juries score **Design 40 / Usability 30 / Creativity 20 / Content 10** — so usability
and performance together outweigh raw creativity. The bar is *"controlled creativity"*: bold
direction that still hits these non-negotiable gates (they sink the score regardless of how
beautiful the site is):

| Gate | Target | Owner doc |
|---|---|---|
| Largest Contentful Paint | ≤ **2.5 s** (p75) | `09-tech-implementation.md` |
| Interaction to Next Paint | ≤ **200 ms** (p75) | `09` |
| Cumulative Layout Shift | ≤ **0.1** (p75) | `09` |
| `prefers-reduced-motion` | every animation has a fallback | `07-animation-choreography.md` |
| WCAG AA contrast | ≥ 4.5:1 text, ≥ 3:1 large/UI | `05-color.md` |
| WebGL (if used) | < 100 draw calls, resources disposed | `08-webgl-effects.md` |

All of these are already baked into the four artifacts the skill produces — your job in the
build is to *honor* them, then *prove* you did.

---

## Phase 0 — Brief (≈5 min)

Decide these before you invoke anything. The skill will ask for what's missing, but having them
ready makes stage 1 one-shot:

- **Mode:** `create` (from scratch) · `recreate` (reverse-engineer a reference site) · `modify`
  (evolve an existing system).
- **Archetype leaning** (or let it recommend): brutalist-editorial, immersive-3D,
  kinetic-minimal, retro-futurist, soft-organic, luxe-cinematic. *(See rendered examples of each
  in [archetypes/](archetypes/) to pick one.)*
- **Motion personality:** `snappy` (150–350 ms) · `fluid` (400–800 ms) · `cinematic` (600–1200 ms).
- **WebGL:** yes (and where) / no.
- **Audience & tone**, **brand constraints** (existing colors/fonts/logo, or "none"),
  **content types**, **performance context** (markets, devices), **deadline**.

---

## Phase 1 — Generate the design system (the skill)

In a **new project directory**, start a fresh Claude Code session and paste:

```
Use the design-systems-agent skill. Mode: create.

Brief:
- Project: <one line — what the site is>
- Archetype leaning: <name, or "recommend from doc 01">
- Motion personality: <snappy | fluid | cinematic>
- WebGL: <yes, where | no>
- Audience & tone: <...>
- Brand constraints: <existing colors/fonts/logo, or "none">
- Constraints: <perf context, target browsers, deadline>

Produce the four artifacts into ./design/. Run every consulted doc's Quality
Checklist and flag any UNVERIFIED items.
```

**You get four artifacts in `./design/`:**

| Artifact | What it pins |
|---|---|
| `design-system-spec.md` | archetype, type/color/spacing scales, grid, components, motion language, imagery, a11y, perf budget |
| `design-tokens.tokens.json` | DTCG tokens (primitive→semantic→component); plus `design-tokens.dark.tokens.json` if themed |
| `motion-spec.md` | per-element motion table with reduced-motion fallbacks |
| `implementation-plan.md` | chosen stack + **verified versions**, asset pipeline, perf budget, QA checklist |

**REVIEW GATE (do not skip).** Read the spec and tokens. Adjust archetype, personality, palette,
type scale — and re-run the skill if the direction is off. Iterating here costs minutes;
iterating after you've built costs days. Only proceed when the system feels right.

> Have a reference site you love? Use `recreate` mode instead — point it at the URL and it
> reverse-engineers a clean system (tokens + confidence scores) without copying code. Evolving
> an existing site? Use `modify` mode (it versions the token file with semver).

---

## Phase 2 — Scaffold + the token bridge (the make-or-break step)

```
Read ./design/implementation-plan.md and scaffold the project using the stack and
the exact pinned versions it specifies (use non-interactive / --yes flags).

Then build the TOKEN BRIDGE: compile ./design/design-tokens.tokens.json into CSS
custom properties — dot→hyphen naming (color.bg.primary → --color-bg-primary),
resolving aliases — wire them into the global stylesheet, and load
design-tokens.dark.tokens.json as the [data-theme="dark"] semantic override.
From here, the app consumes tokens ONLY via var(--…). No hardcoded hex/px.
```

The token bridge is where most builds quietly fail. Two viable approaches:

- **Generate a static CSS variables file** from the DTCG JSON (simplest; ask Claude to write the
  generator once). Re-run it whenever tokens change.
- **A token build tool** (e.g. Style Dictionary — *verify its current version first; it's not in
  `_facts.md`*) for richer multi-platform output.

Either way, the output is `var(--token)` everywhere. The implementation plan already chose the
stack — typically **Astro** for content/marketing sites (best Core Web Vitals + cross-document
View Transitions), **Next/Nuxt** for app-like state.

---

## Phase 3 — Build the UI from the spec

Use the **`frontend-design`** skill (built for distinctive, production-grade UI that avoids
generic AI aesthetics) and feed it the spec + tokens as the brief:

```
Use the frontend-design skill. Build <page/section>, implementing
./design/design-system-spec.md — its layout/grid, typography, color, spacing, and
component sections. Consume the CSS token variables only; if you need a value with
no token, ADD a token rather than hardcoding. Mobile-first, per the spec's breakpoints.
```

Build section by section. After each, sanity-check against the spec's grid, type scale, and
spacing rhythm. Keep the component inventory in the spec as your checklist.

---

## Phase 4 — Motion & interaction

```
Implement ./design/motion-spec.md row by row (trigger, property, from→to, duration,
easing, stagger). Use the verified libraries from ./design/implementation-plan.md
(GSAP + the canonical Lenis ScrollTrigger integration; Motion; View Transitions API
first with a GSAP fallback). EVERY animation must have its prefers-reduced-motion
fallback exactly as the motion-spec defines. Stay within the duration classes.
```

Award-grade motion is *choreographed and respectful*: it reads as intentional, never blocks
interaction (watch INP), and collapses cleanly under reduced-motion. The motion-spec already
encodes all of this — implement it faithfully rather than improvising.

---

## Phase 5 — WebGL (only if the spec calls for it)

Follow `08-webgl-effects.md`'s decision framework: **the lightest tool that achieves the
effect.** If you do go 3D, honor the budget (< 100 draw calls, dispose GPU resources, cap DPR,
on-demand rendering) and **always ship a non-WebGL fallback** for unsupported devices and
reduced-motion. For a full bespoke 3D scene, the `3d-web-forge` skill builds the scene — your
design system supplies the *direction*, it supplies the implementation.

---

## Phase 6 — Asset pipeline

From `implementation-plan.md` / `09-tech-implementation.md`:

- **Images:** AVIF/WebP, responsive `srcset` bracketing your breakpoints at 1× and 2×, correct
  color profile (sRGB / P3). Hero image budget ≈ **200 KB**.
- **3D models:** optimize with the pinned `gltf-transform` —
  `gltf-transform optimize in.glb out.glb --compress draco --texture-compress ktx2 --texture-size 2048`
  (UASTC for normal maps, ETC1S for diffuse).
- **Fonts:** subset + `font-display: swap`; budget ≈ **200 KB** total.
- **JS:** content-site budget ≈ **170 KB**.

---

## Phase 7 — Verify against the bar (this is what wins)

The gap between "done" and "award-winning" is *measured*. Run these gates and iterate until they
pass:

```
Run the site and verify against the budget:
- Core Web Vitals at p75 (mobile + desktop): LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1.
- WCAG AA contrast on every text/UI pair.
- prefers-reduced-motion path, full keyboard nav, focus management, canvas fallback.
- Run each consulted KB doc's Quality Checklist + the implementation-plan QA checklist.
If a budget breaks, drop the design's intensity tier first (per the spec's breach protocol).
```

**Use the real tools, not guesswork:**

- **`chrome-devtools`** skill (`debug-optimize-lcp`, `a11y-debugging`, `memory-leak-debugging`)
  and Lighthouse for CWV, performance traces, and accessibility.
- **`verify`** skill to actually run the app and confirm behavior.
- **`playwright`** for cross-browser checks — note **Firefox has no cross-document View
  Transitions**, so confirm your transition fallback there.

---

## Phase 8 — Ship & submit

- **Deploy:** the `vercel:deploy` skill (preview → production). Astro/Next deploy with zero
  config; ISR/edge as the plan specifies.
- **Final QA** on real devices (not just emulation) — especially scroll feel and INP on
  mid-range mobile.
- **Award submission:** lead with the *controlled-creativity* story, but make sure usability and
  performance are bulletproof (30 + 40 of the score). Polish the **loading experience** — it's
  the juror's first impression and a common, cheap place to lose points.

---

## The copy-paste sequence (the efficient path)

One prompt per phase, run in order, reviewing the artifacts/output between each:

1. *(Phase 1)* `Use the design-systems-agent skill. Mode: create. Brief: …` → review `./design/`.
2. *(Phase 2)* `Read ./design/implementation-plan.md, scaffold the pinned stack, build the token bridge (DTCG → CSS vars).`
3. *(Phase 3)* `Use frontend-design. Build <section> from ./design/design-system-spec.md, tokens only.` *(repeat per section)*
4. *(Phase 4)* `Implement ./design/motion-spec.md row by row, with every reduced-motion fallback.`
5. *(Phase 5, if needed)* `Add the WebGL from the spec per doc 08's budget, with a non-WebGL fallback.`
6. *(Phase 6)* `Run the asset pipeline from the implementation plan (AVIF/WebP + gltf-transform).`
7. *(Phase 7)* `Verify against the budget: CWV, contrast, reduced-motion, keyboard. Use chrome-devtools + verify.`
8. *(Phase 8)* `Deploy with the vercel skill; run final cross-device QA.`

---

## Pitfalls that cost awards

| Pitfall | Fix |
|---|---|
| Hardcoded values drift from the tokens | Consume `var(--token)` only; add a token before hardcoding |
| Animation with no reduced-motion fallback | Instant a11y fail — the motion-spec already defines every fallback; implement it |
| Hero image / JS bundle blows the budget | AVIF + responsive srcset; budget-check in Phase 7, not at launch |
| WebGL with no fallback or > 100 draw calls | Provide a fallback; instance/batch; dispose resources |
| Ignoring INP (jank on interaction) | Keep main-thread work off the interaction path; measure with chrome-devtools |
| Shipping unverified library versions | Use only what `./design/implementation-plan.md` pins (sourced from `_facts.md`) |
| Building before the system is right | Use the Phase 1 review gate; iterate the spec, not the built site |

---

## Why this is efficient

You design the *system* once (Phase 1), wire it in once (the token bridge), then every page you
build inherits consistent type, color, spacing, and motion for free — and stays consistent
because there's a single source of truth. You verify against numbers continuously, so you never
discover at launch that the hero blew the LCP budget. The skill front-loads the hard, expensive
decisions into a one-hour spec, and the rest of the build becomes execution against a plan that
already knows the answer.

**See also:** [`../README.md`](../README.md) (skill install + the spec→build two-stage model) ·
[`../knowledge-base/00-agent.md`](../knowledge-base/00-agent.md) (the agent's routing hub) ·
[`../knowledge-base/09-tech-implementation.md`](../knowledge-base/09-tech-implementation.md)
(the full performance-budget table and asset-pipeline commands).
