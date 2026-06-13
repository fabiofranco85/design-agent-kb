---
title: Visual Direction & Motion Personality
doc_id: 01-visual-motion
version: 1.0
last_verified: 2026-06-12
applies_to_modes: [create, recreate, modify]
---

## Purpose & When To Read This

Open this doc FIRST in every engagement, before any other spec doc. It owns the two
top-level decisions that every other document consumes: (1) the **visual archetype** (the
site's aesthetic family) and (2) the **motion personality** (`snappy` / `fluid` /
`cinematic`). In `create` mode it turns a brief into a numeric visual direction; in
`recreate` mode it classifies an existing site; in `modify` mode it protects an existing
direction from drift. If archetype + personality are already declared in the project
artifact ([schema](./10-modes-and-artifacts.md#specifications--parameters)), skip to the
cascade table in Specifications & Parameters.

## Core Principles

1. **Controlled creativity wins awards.** The Awwwards jury weights **Design 40% +
   Usability 30% + Creativity 20% + Content 10%**. Design and usability together are 70%
   of the score — a spectacular site that scroll-jacks, lags, or hides its navigation
   loses more points than a restrained one gains from novelty. Submissions go to ≥18
   jurors and the 3 most extreme scores are discarded, so polarizing chaos is
   structurally penalized. Aim for the precision of Lusion or Locomotive, never "more
   effects".
2. **One archetype, one personality, per site.** Every page, component, and interaction
   inherits the same archetype token and the same personality token. Mixing two
   archetypes is a redesign decision, not a styling choice.
3. **Motion is identity, not decoration.** Pick the personality before specifying a
   single animation. Identical layouts with `expo.out` at 200 ms vs `power4.inOut` at
   1000 ms are different brands. All durations and eases below use the canonical bands
   from `_conventions.md` §3.2; curve definitions live in the
   [easing table](./07-animation-choreography.md#specifications--parameters).
4. **Numbers, not adjectives.** "Bold" is a defect; "display type ≥ 8 vw, contrast
   ≥ 12:1, borders 2 px" is a direction. Every archetype below resolves to measurable
   signals so `recreate` mode can classify and `modify` mode can verify.
5. **Performance is part of the aesthetic.** Lusion's SOTM-winning site pre-bakes
   simulations offline (a 220 KB gzip cloth sim; 983 KB of vertex-animation textures on
   desktop, 246 KB on mobile) — their stated principle: "You don't need to do everything
   real-time." Spectacle that breaks the budgets in
   [doc 09](./09-tech-implementation.md#specifications--parameters) is a defect, not a style.
6. **Reduced motion is a first-class variant.** Motion can trigger vestibular disorders
   (dizziness, nausea, migraine). Every motion spec in this KB ships with a
   `prefers-reduced-motion` fallback — canonical pattern owned by
   [doc 07](./07-animation-choreography.md#specifications--parameters).

## Decision Framework

Apply in order; stop at the first decisive rule.

**Step 1 — Candidate archetypes from the brief.**
- IF brief keywords include *raw, honest, editorial, independent, manifesto, type-driven*
  → `brutalist-editorial`.
- IF the product IS the experience (game, launch, flagship campaign, tech demo) AND
  WebGL budget exists → `immersive-3d`.
- IF *premium SaaS, studio portfolio, refined, understated, crafted* → `kinetic-minimal`.
- IF *nostalgia, Y2K, gaming, music, streetwear, Gen-Z* → `retro-futurist`.
- IF *wellness, food, sustainability, community, human, warm* → `soft-organic`.
- IF *fashion, automotive, fragrance, film, hospitality at luxury tier* → `luxe-cinematic`.

**Step 2 — Eliminate by constraints.**
- IF >60% of content is long-form text → eliminate `immersive-3d` as the base (a WebGL
  accent layer may remain; see [doc 08](./08-webgl-effects.md#decision-framework)).
- IF mobile-majority audience on mid-tier devices OR no 3D asset budget → downgrade
  `immersive-3d` to "hybrid": DOM-first with one canvas accent.
- IF accessibility requirements are strict (public sector, health) → eliminate
  `retro-futurist` glitch/flicker treatments; keep its palette/type only.
- IF conversion-critical e-commerce funnel → cap personality at `fluid`; `cinematic`
  is reserved for narrative sections, never for checkout UI.

**Step 3 — Personality.** Take the archetype's default from the mapping table below.
Override only one step in either direction (e.g. `immersive-3d` from `fluid` to
`cinematic` for a narrative piece) and record the justification in the artifact.

**Step 4 — Intensity tier.** Choose exactly one:
- `ambient` — motion only on scroll-reveals and hovers; no persistent animation.
- `responsive` — adds scroll-linked progress (parallax ≤ 12% of element height,
  scrubbed timelines) and cursor-reactive accents.
- `showcase` — adds persistent real-time layers (shader/canvas, generative type).
  Allowed only if the [doc 09 budgets](./09-tech-implementation.md#specifications--parameters)
  hold (LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 at p75).

**Step 5 — Sanity check.** IF the chosen combination cannot keep text readable, nav
discoverable within one viewport, and scroll always user-controlled → reduce intensity
one tier before touching the archetype.

## Specifications & Parameters

### 1. Visual archetype taxonomy (owner: this doc)

Archetype IDs are canonical tokens — use them verbatim in artifacts and prompts.

| Archetype | Core idea | Default personality | Reference studios / evidence |
|---|---|---|---|
| `brutalist-editorial` | Exposed grid, oversized type, raw honesty | `snappy` | Obys (32 SOTD, Awwwards Studio of the Year 2023) |
| `immersive-3d` | Real-time 3D scene IS the interface | `fluid` (narrative: `cinematic`) | Lusion, Active Theory, Resn, Dogstudio |
| `kinetic-minimal` | Restraint everywhere, motion carries identity | `fluid` | 14islands (20 SOTD), Locomotive (1 SOTY, 90 SOTD), Unseen Studio, OFF+BRAND |
| `retro-futurist` | Y2K/chrome nostalgia with modern engineering | `snappy` | Y2K revival trend (chrome gradients, pixel type, glitch) |
| `soft-organic` | Warm, tactile, grain + curves, human | `fluid` | 2025 grain/texture trend (Codrops-documented) |
| `luxe-cinematic` | Dark, full-bleed, slow, editorial luxury | `cinematic` | Dogstudio, Active Theory campaign work |

Measurable signals per archetype (use ≥4 matching signals to classify in `recreate`):

**`brutalist-editorial`**
- Color: ≤3 colors; near-black (#0A0A0A–#111) on off-white (#F0EEE9–#FAFAF7) or
  inverted; one saturated accent. Display contrast ≥ 12:1
  (floors in [doc 05](./05-color.md#specifications--parameters)).
- Type: display at 8–16 vw via clamp; grotesque or monospace; uppercase headers;
  body-to-display jump ≥ 4 steps on the scale
  ([doc 04](./04-typography.md#specifications--parameters)).
- Layout: visible structure — 1 px hairline rules, 1–2 px solid borders, exposed 12-col
  grid, dense asymmetric blocks ([doc 03](./03-layout.md#specifications--parameters)).
- Surface: flat, zero shadows, zero border-radius (0–2 px max), no gradients.
- Motion signatures: SplitText line/word reveals, instant hover inversions (≤120 ms),
  marquee strips at 40–80 px/s, hard timeline cuts (no crossfades).

**`immersive-3d`**
- A `<canvas>` is the primary visual surface (≥60% of hero viewport).
- Color: scene-lit; UI overlays at 80–95% white/black opacity for legibility.
- Type: minimal UI type layer; 2 sizes often suffice (nav ~14–16 px, display via clamp).
- Motion signatures: camera dolly/orbit eased over 800–1200 ms, scroll-scrubbed
  timelines, cursor parallax ≤ 3° rotation / ≤ 24 px translation, shader transitions.
- Budget signals: pre-baked > real-time wherever possible (Lusion method: keyframe
  subsampling — 11 of 66 frames + runtime interpolation; per-device asset tiers,
  desktop ~4× mobile vertex counts). Hard caps in
  [doc 08](./08-webgl-effects.md#decision-framework) and
  [doc 09](./09-tech-implementation.md#specifications--parameters).

**`kinetic-minimal`**
- Color: 1–2 hues + neutrals; backgrounds within 5% lightness of pure white or near-black.
- Type: ratio 1.2–1.25 (`_conventions.md` §3.6); weight contrast over size contrast.
- Layout: whitespace-dominant — section padding ≥ `space.24` (96 px), content width
  ≤ 720 px for prose ([doc 06](./06-spacing.md#specifications--parameters)).
- Surface: flat or 1-step elevation; radius 4–12 px; no texture.
- Motion signatures: smooth scroll (Lenis), staggered mask reveals (60–90 ms/item),
  hover scale 1.02–1.04, image parallax 6–12%; motion IS the brand layer.

**`retro-futurist`**
- Color: chrome/metallic gradients, neon accents (electric blue, acid green, hot pink)
  on dark or silver bases.
- Type: pixel/bitmap or techno display faces paired with a neutral grotesque for body
  (body stays ≥ 16 px and high-legibility — nostalgia never applies to paragraphs).
- Surface: gloss, bevels, scanlines at 2–4 px pitch and ≤ 8% opacity, sticker/badge
  elements, visible cursors.
- Motion signatures: `steps()` glitch reveals (4–8 steps), blinking elements at ≤ 2 Hz,
  instant state swaps. HARD RULE: no flashing above 3 flashes/s (WCAG 2.3.1) and all
  glitch loops disabled under reduced motion.

**`soft-organic`**
- Color: warm off-whites (#FAF6F0 family), earth/pastel hues; low global contrast with
  AA-compliant text ([doc 05](./05-color.md#specifications--parameters)).
- Type: humanist sans or sans+serif pairing; generous line-height (1.6–1.75 body).
- Surface: grain/noise overlay at 3–8% opacity, blob/superellipse shapes, border-radius
  16–32 px+, gradient meshes, soft shadows (blur ≥ 24 px, opacity ≤ 12%).
- Motion signatures: opacity+blur reveals (blur 8 px → 0), hover scale 1.02–1.05,
  slow ambient drift (≥ 20 s loops, ≤ 8 px amplitude), spring-flavored eases.

**`luxe-cinematic`**
- Color: dark base (#0A0A0A–#141414), 1 metallic or muted accent; full-bleed
  photography/video as the color carrier.
- Type: high-contrast serif or didone display; wide tracking on small caps labels
  (0.08–0.16 em); display ratio up to 1.618.
- Layout: full-viewport scenes, centered or golden-section focal points, minimal chrome.
- Motion signatures: slow image scale 1.05 → 1.0 over 900–1200 ms on entry,
  letterbox wipes, crossfades ≥ 600 ms, scroll-driven scene changes, generous
  timeline overlaps (40–60% of previous tween).

### 2. Motion-personality framework (owner: this doc; values pinned in `_conventions.md` §3.2)

| Personality | Default duration band | Default eases (GSAP names) |
|---|---|---|
| `snappy` | 150–350 ms | `expo.out`, `power3.out` |
| `fluid` | 400–800 ms | `power2.inOut`, `power3.out` |
| `cinematic` | 600–1200 ms | `power4.inOut`, `expo.inOut` |

The band governs the site's workhorse motion (UI transitions and standard reveals). For
role-specific timing, the [duration classes](./07-animation-choreography.md#specifications--parameters)
(`_conventions.md` §3.3) take precedence; the personality selects WHERE inside each
class range you sit:

| Duration class (doc 07 owns ranges) | `snappy` slice | `fluid` slice | `cinematic` slice |
|---|---|---|---|
| micro-interaction (100–200 ms) | 100–140 ms | 140–180 ms | 160–200 ms |
| UI transition (200–400 ms) | 200–280 ms | 300–400 ms | 350–400 ms |
| content/section reveal (400–700 ms) | 400–480 ms | 450–650 ms | 550–700 ms |
| hero / cinematic (600–1200 ms) | 600–750 ms | 700–900 ms | 900–1200 ms |

Personality-level parameters (extensions owned by this doc):

| Parameter | `snappy` | `fluid` | `cinematic` |
|---|---|---|---|
| Stagger per item | 30–50 ms | 60–90 ms | 90–140 ms |
| Max total stagger sequence | 600 ms | 1000 ms | 1600 ms |
| Entrance travel (translateY) | 16–24 px | 32–48 px | 48–80 px |
| Hover scale | 1.00 (use color/invert) | 1.02–1.04 | 1.04–1.06 |
| Timeline overlap (of prev tween) | 0–10% | 20–40% | 40–60% |
| Smooth-scroll intent (Lenis lerp) | 0.14–0.18 | 0.09–0.12 | 0.05–0.08 |

Lenis integration itself is owned by [doc 07](./07-animation-choreography.md#code-examples) —
the lerp row above only expresses personality intent. `snappy` may also skip smooth
scroll entirely (native scroll is a legitimate snappy choice).

Selection heuristics:
- `snappy` = confidence, utility, wit. Risk: feels cheap if eases are linear — always
  use the pinned decelerating eases.
- `fluid` = craft, premium calm. The safest award-grade default; 14islands/Locomotive
  territory.
- `cinematic` = drama, luxury, narrative. Risk: INP and perceived sluggishness — never
  apply the band to input feedback; micro-interactions stay in their class slice above.

Reduced-motion collapse (all personalities): replace transform/scale/parallax motion
with opacity-only fades of 150–200 ms, `ease: "none"`; disable marquees, glitch loops,
ambient drift, smooth scroll. Canonical pattern + full policy:
[doc 07](./07-animation-choreography.md#specifications--parameters).

### 3. Cascade: how this doc's decision flows into the other specs

Record archetype + personality + intensity in the project artifact
([doc 10](./10-modes-and-artifacts.md#specifications--parameters)), then read across:

| Downstream doc | What the archetype/personality dictates there |
|---|---|
| [02-image-generation](./02-image-generation.md#specifications--parameters) | Prompt style vocabulary, texture (grain %, gloss), photography vs 3D renders |
| [03-layout](./03-layout.md#specifications--parameters) | Grid visibility, density, whitespace tier, full-bleed vs contained scenes |
| [04-typography](./04-typography.md#specifications--parameters) | Scale ratio tendency, display size ceilings, face pairing class |
| [05-color](./05-color.md#specifications--parameters) | Palette temperature, contrast stance, dark/light base, accent count |
| [06-spacing](./06-spacing.md#specifications--parameters) | Section padding tier (dense ↔ whitespace-dominant) on the §3.5 scale |
| [07-animation-choreography](./07-animation-choreography.md#specifications--parameters) | Personality → concrete easing/duration/stagger choreography recipes |
| [08-webgl-effects](./08-webgl-effects.md#decision-framework) | Whether canvas is base layer (`immersive-3d`), accent, or absent |
| [09-tech-implementation](./09-tech-implementation.md#specifications--parameters) | Stack weight class and perf budget pressure of the chosen intensity tier |

Conflict rule: if a downstream spec cannot satisfy both its own constraints (a11y,
performance) and the archetype direction, the downstream constraint wins and the
intensity tier drops one level — the archetype itself never silently changes.

## Recommended Libraries & Tools

All versions from `_facts.md` (single source of truth — do not re-research).

| Use-case | Library | Install | Import |
|---|---|---|---|
| Personality engine: tweens, timelines, scroll triggers, type reveals | `gsap@3.15.0` (all plugins free since 3.13, incl. SplitText/ScrollTrigger/CustomEase) | `npm install gsap` | `import gsap from "gsap"`; `import { ScrollTrigger } from "gsap/ScrollTrigger"` + `gsap.registerPlugin(ScrollTrigger)` |
| Smooth-scroll feel for `fluid`/`cinematic` | `lenis@1.3.23` (NOT `@studio-freight/lenis` — deprecated name) | `npm install lenis` | `import Lenis from "lenis"` + `import "lenis/dist/lenis.css"` — setup recipe in [doc 07](./07-animation-choreography.md#code-examples) |
| React-component UI transitions | `motion@12.40.0` (formerly framer-motion) | `npm install motion` | `import { motion } from "motion/react"` |
| `immersive-3d` base layer | `three@0.184.0` (r184) | `npm install three` | `import * as THREE from "three"` — full decision framework in [doc 08](./08-webgl-effects.md#decision-framework) |

Page transitions: prefer the View Transitions API with a GSAP fallback;
`@barba/core@2.10.3` is dormant (last publish 2024-08) — use-at-own-risk per `_facts.md`.
Choreography ownership: [doc 07](./07-animation-choreography.md#specifications--parameters).

## Code Examples

Declare the personality ONCE as tokens; every animation reads from it.

```js
// motion.tokens.js — single source of motion truth for the build.
// Values must sit inside the pinned bands (_conventions.md §3.2 / this doc §2).
export const MOTION = {
  personality: "fluid",          // "snappy" | "fluid" | "cinematic" — exactly ONE per site
  dur: {                         // seconds; fluid slices of each duration class
    micro: 0.16,                 // 140–180 ms slice
    ui: 0.35,                    // 300–400 ms slice
    reveal: 0.6,                 // 450–650 ms slice
    hero: 0.8,                   // 700–900 ms slice
  },
  ease: { out: "power3.out", inOut: "power2.inOut" }, // pinned fluid eases (defs: doc 07)
  stagger: 0.07,                 // 60–90 ms band
  travel: 40,                    // px entrance offset, 32–48 px band
  hoverScale: 1.03,              // 1.02–1.04 band
};
```

```js
// reveal.js — personality-driven section reveal with the mandatory reduced-motion variant.
// gsap@3.15.0 (_facts.md). Canonical reduced-motion policy: doc 07.
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { MOTION } from "./motion.tokens.js";

gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.from(".section [data-reveal]", {
    y: MOTION.travel,            // transform-only: never animates layout → zero CLS
    opacity: 0,
    duration: MOTION.dur.reveal, // 0.6 s — fluid slice of the reveal class
    ease: MOTION.ease.out,       // power3.out
    stagger: MOTION.stagger,     // 70 ms per item
    scrollTrigger: { trigger: ".section", start: "top 80%" }, // fires once in view
  });
});

mm.add("(prefers-reduced-motion: reduce)", () => {
  // Collapse to opacity-only, ≤200 ms, no easing personality, no stagger choreography.
  gsap.from(".section [data-reveal]", { opacity: 0, duration: 0.2, ease: "none" });
});
```

## Mode-Specific Guidance

### Create from scratch

1. Extract 3–5 brand adjectives from the brief; run the Decision Framework to land on
   one archetype + one personality + one intensity tier.
2. Write the numeric direction into the artifact
   ([doc 10](./10-modes-and-artifacts.md#specifications--parameters)): archetype token,
   personality token, intensity tier, plus the 5–8 measurable signals you committed to
   (palette stance, display ceiling, border/radius/texture values, stagger/travel values).
3. Walk the cascade table top-to-bottom, opening each downstream doc with the direction
   already fixed. Never let a downstream doc re-decide the archetype.
4. Differentiate within the archetype, not by mixing archetypes: vary the accent hue,
   type pairing, and one signature interaction. Award-level distinctiveness comes from
   one memorable, perfectly executed signature move (Awwwards Creativity = 20%), not
   from effect count.

### Re-create from existing site (reverse-engineering)

1. **Detect the base layer:** presence of a dominant `<canvas>` (≥60% of hero viewport)
   → `immersive-3d` candidate. Check bundles for `three`/shader code.
2. **Measure motion:** record 5+ interactions (hover, nav open, section reveal, page
   transition) with DevTools Performance; read CSS `transition-duration` /
   `animation-duration` computed values. Median duration → personality band; map
   captured `cubic-bezier()` values to the nearest canonical GSAP name via the
   [doc 07 easing table](./07-animation-choreography.md#specifications--parameters).
3. **Detect smooth scroll:** translated wrapper + `html.lenis` class or `data-lenis`
   attributes → Lenis; estimate lerp from scroll settle time (≈300 ms settle ≈ 0.15;
   ≥800 ms ≈ 0.06).
4. **Score archetype signals:** check the measurable signal lists in §1; ≥4 matching
   signals = classification. Tie-break with the measured personality (e.g. snappy
   timing breaks a brutalist/kinetic-minimal tie toward `brutalist-editorial`).
5. Record per-dimension confidence (high/medium/low) in the artifact; any guessed value
   gets `UNVERIFIED — confirm before use`.

### Modify an existing system

1. Classify the existing system first (run the `recreate` diagnostic above) even when
   docs exist — verify the docs against the live behavior.
2. New components inherit the existing motion tokens verbatim. Introducing a second
   personality or archetype is forbidden inside `modify`; if the brief truly demands a
   new direction, escalate to `create` with a migration note.
3. Drift check before shipping: every new element must match ≥4 of the archetype's
   measurable signals, and every new duration must fall in the established personality
   slices (§2 matrix).
4. When extending tokens (new duration role, new stagger), derive from the existing
   band — never import values from another personality column.

## Quality Checklist

- [ ] Exactly one archetype token and one personality token declared in the artifact,
      with intensity tier.
- [ ] Every specified duration falls inside the correct personality slice of its
      duration class (§2 matrix); micro-interactions never exceed 200 ms.
- [ ] Every ease used is one of the personality's pinned GSAP names (or a documented,
      justified addition referencing the [doc 07 table](./07-animation-choreography.md#specifications--parameters)).
- [ ] ≥4 measurable archetype signals (§1) are specified with numbers and verifiable in
      the build.
- [ ] Reduced-motion variant specified for EVERY motion item (opacity-only ≤200 ms
      collapse; marquees/glitch/ambient loops disabled).
- [ ] Entrance animations use transform/opacity only — zero CLS contribution.
- [ ] Text contrast meets the §3.9 anchors (≥4.5:1 body) within the chosen palette
      stance ([doc 05](./05-color.md#specifications--parameters)).
- [ ] Navigation reachable and legible in the first viewport without waiting for any
      animation or asset.
- [ ] Scroll is never blocked or hijacked; any scrubbed sequence remains
      user-interruptible.
- [ ] Intensity tier respects the perf budgets
      ([doc 09](./09-tech-implementation.md#specifications--parameters)); `showcase`
      tier has a per-device asset plan (Lusion pattern: mobile assets ≈ ¼ desktop).
- [ ] One signature interaction documented (the memorable move) — and only one.

## Anti-Patterns

1. **Personality mixing** — snappy 150 ms buttons next to 1000 ms cinematic reveals
   reads as unfinished, not eclectic. One personality column, site-wide.
2. **Uniform 300 ms `ease-in-out` everywhere** — the opposite failure: no personality
   at all. Jurors score this as template work (Design 40% suffers).
3. **Scroll-jacking** — overriding scroll distance/direction or trapping the wheel in a
   scene with no escape. Usability is 30% of the Awwwards score; this is the most
   common spectacle-induced rejection.
4. **Spectacle-first loading** — a WebGL hero that pushes LCP past 2.5 s or a 5 s
   unskippable preloader. Pre-bake, tier assets per device, or drop intensity.
5. **Entrance animations that move layout** — animating `top/height/margin` causes CLS;
   transform/opacity only.
6. **Ignoring `prefers-reduced-motion`** — vestibular harm and an automatic
   accessibility failure. The collapse variant is mandatory (principle 6).
7. **Flashing/glitch loops above 3 flashes per second** — seizure risk (WCAG 2.3.1);
   `retro-futurist` treatments must stay ≤ 2 Hz and die under reduced motion.
8. **Archetype cosplay** — brutalism as an excuse for no grid, or "organic" as an
   excuse for AA-failing contrast. Every archetype above carries discipline numbers;
   chaos without measurable structure scores as broken, not bold.
9. **Trend-stacking** — grain + chrome + 3D + glitch + serif luxury in one build.
   ≥2 archetype signal-sets mixed = no identity. Pick one, execute deeply.
10. **Decorative cursor replacement that hides affordances** — custom cursors may add,
    never remove, state feedback (links/buttons must still signal interactivity within
    100–140 ms).

## Sources & Verification

- https://www.awwwards.com/about-evaluation/ — confirmed: jury weighting Design 40% /
  Usability 30% / Creativity 20% / Content 10%; ≥18 jurors with the 3 scores furthest
  from average discarded; 6.5+ qualifies for Honorable Mention (verified 2026-06-12)
- https://tympanus.net/codrops/2025/12/29/2025-a-very-special-year-in-review/ —
  confirmed: GSAP as the key expressive-motion tool of 2025; dominance of scroll-driven
  effects, kinetic typography, dithering/dissolve shaders, Three.js + TSL and WebGPU
  experimentation (verified 2026-06-12)
- https://www.awwwards.com/case-study-for-lusion-by-lusion-winner-of-site-of-the-month-may.html
  — confirmed: Lusion's pre-baked simulation approach ("You don't need to do everything
  real-time"); 220 KB gzip Houdini cloth sim; 11-of-66 keyframe vertex-animation
  textures with runtime interpolation; 983 KB desktop (4,096 vertices) vs 246 KB mobile
  (1,024 vertices) asset tiers (verified 2026-06-12)
- https://www.awwwards.com/obys/ — confirmed: Obys (Ukraine), 32 SOTD, 2 SOTM, 41
  Honorable Mentions; concept-driven studio (verified 2026-06-12)
- https://www.behance.net/obys_agency — confirmed: Obys named Awwwards Studio of the
  Year 2023; approach rooted in typography, grid systems, motion, and modernist
  principles (verified 2026-06-12)
- https://www.awwwards.com/14islands/ — confirmed: 14islands (Sweden, est. 2011), 20
  SOTD incl. "365 — A Year of Cartier" (SOTD Feb 2025) (verified 2026-06-12)
- https://www.awwwards.com/locomotive/ — confirmed: Locomotive (Montréal), 1 Site of
  the Year, 4 SOTM, 90 SOTD, 130 Honorable Mentions (verified 2026-06-12)
- https://lusion.co/ — confirmed: Lusion's positioning as an award-winning 3D and
  interactive studio building real-time immersive experiences (verified 2026-06-12)
- https://activetheory.net/ — confirmed: Active Theory's positioning, "Creative Digital
  Experiences" (verified 2026-06-12)
- https://unseen.co/ — confirmed: Unseen Studio's positioning as a brand, digital &
  motion studio (verified 2026-06-12)
- https://www.itsoffbrand.com/ — confirmed: OFF+BRAND is a Scottish-born global
  creative & technology studio working across branding, web design and WebGL
  (verified 2026-06-12)
- https://www.utsubo.com/blog/top-threejs-agencies — confirmed: studio
  characterizations — Resn (NZ/NL, large-scale interactive/multi-user builds),
  Dogstudio (EU, bold creative + technical signatures), Active Theory (refined
  motion + solid engineering) (verified 2026-06-12)
- https://web.dev/articles/prefers-reduced-motion — confirmed: implementation guidance
  for the `prefers-reduced-motion` media query and reduced-but-not-zero motion
  philosophy (verified 2026-06-12)
- https://web.dev/learn/accessibility/motion — confirmed: motion can trigger vestibular
  disorders (dizziness, nausea, migraine); WCAG 2.3.3 "Animation from Interactions"
  guidance to reduce/replace non-essential motion (verified 2026-06-12)
- https://webflow.com/blog/y2k-aesthetic — confirmed: Y2K visual vocabulary — glossy
  UI elements, chunky/pixelated typography, metallic-chrome gradients, bubble shapes
  (verified 2026-06-12)
