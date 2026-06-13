---
title: Animation Choreography — Easing, Duration, Scroll & Page Transitions
doc_id: 07-animation-choreography
version: 1.0
last_verified: 2026-06-12
applies_to_modes: [create, recreate, modify]
---

## Purpose & When To Read This

Open this doc whenever motion is being specified, implemented, or audited: choosing eases
and durations, wiring smooth scroll (Lenis), building scroll-driven storytelling
(pin / scrub / snap), page transitions (View Transitions API first, GSAP fallback), the
micro-interaction catalog (magnetic buttons, cursor followers, hover states), or the
mandatory `prefers-reduced-motion` handling. This doc OWNS the canonical easing table,
the four duration classes, the Lenis + ScrollTrigger setup recipe, the canonical
reduced-motion pattern, and page-transition guidance — all sibling docs reference these
from here and never redefine them.

## Core Principles

1. **Choreography, not decoration.** Every animation must answer "what changed, where did
   it come from, where is it going". Motion that answers nothing is removed.
2. **One easing vocabulary per project.** All eases come from the canonical table below
   (optionally re-published as named `CustomEase` tokens). Mixing ad-hoc curves is a defect.
3. **`out` for entrances, `inOut` for relocations, `in` only for exits.** `none`/`linear`
   is reserved for scrub-driven tweens, marquees, and spinners — never for UI movement.
4. **Compositor-only properties.** Animate `transform` and `opacity`. Animating
   `top/left/width/height/margin` triggers layout and is a performance defect
   (budgets: [doc 09](./09-tech-implementation.md#specifications--parameters)).
5. **Interruptible by default.** Pointer-driven motion uses `gsap.quickTo()` (or Motion
   springs), which restart toward new targets mid-flight. A user action must never wait
   for an animation to finish.
6. **Scroll belongs to the user.** Scrubbed timelines map progress to scroll position;
   smoothing softens input but never blocks, reverses, or hijacks it.
7. **Reduced motion is a build target, not a patch.** Every animation ships with its
   reduced variant on day one (canonical pattern in
   [Code Examples](#code-examples)).

## Decision Framework

**Engine selection**
- IF two-state UI feedback (hover, focus, open/close) with no sequencing → CSS
  `transition` using the cubic-bezier column of the canonical table.
- IF React component state / gesture animation inside a component tree →
  `motion/react` (`motion@12.40.0`).
- IF timelines, scroll choreography, text/SVG choreography, FLIP layout moves, or anything
  needing labels/stagger/scrub → GSAP 3.15.0 (+ plugins, all free).
- IF route/page change → View Transitions API first, GSAP fallback (see below).

**Smooth scroll**
- IF the page has scroll-driven storytelling or parallax → Lenis (`lenis@1.3.23`) is the
  default, wired to ScrollTrigger with the canonical recipe below.
- IF the build is already GSAP-everything AND attribute-driven parallax
  (`data-speed`/`data-lag`) is wanted → ScrollSmoother (ships free in `gsap@3.15.0`) is an
  acceptable alternative. Never run Lenis and ScrollSmoother together.
- IF content-utility site (docs, commerce checkout, dashboards) → native scroll. Smoothing
  adds nothing and hurts INP perception.
- IF `prefers-reduced-motion: reduce` → do not initialize smoothing at all (native scroll).

**Scroll animation pattern**
- IF element should animate once when entering viewport → ScrollTrigger with
  `toggleActions: "play none none none"` (the default), no scrub.
- IF the user should "own" the narrative (drive it back and forth) → `scrub: 0.5–1.5`.
- IF discrete full-screen scenes → pinned timeline + `snap: { snapTo: "labels" }`.
- IF continuous narrative (no scene boundaries) → scrub without snap.

**Page transitions**
- IF same-document (SPA / framework router) → `document.startViewTransition()` behind a
  feature check; un-animated DOM swap as the no-support path.
- IF cross-document (MPA) → `@view-transition { navigation: auto; }` on BOTH pages
  (same-origin only). Firefox has NO cross-document support (as of FF 150) — the design
  must read as intentional without the transition.
- IF the brief demands identical transitions in every browser → GSAP overlay/wipe
  transition driven by the router (recipe below).
- Barba.js (`@barba/core@2.10.3`) is DORMANT (last publish 2024-08-12) — never adopt for
  new builds; maintain only where it already exists (see Libraries section).

## Specifications & Parameters

### Duration classes (canonical — referenced by all docs)

| Class | Range | Typical use | Default ease |
|---|---|---|---|
| micro-interaction | 100–200 ms | hover, press, focus ring, icon nudge | `power2.out` |
| UI transition | 200–400 ms | menus, modals, tabs, accordions, tooltips | `power3.out` |
| content/section reveal | 400–700 ms | cards, images, headlines entering viewport | `expo.out` |
| hero / cinematic | 600–1200 ms | hero intros, page transitions, full-screen morphs | `power4.inOut` |

Rules: exits run at ~0.7× the entrance duration of the same class. Anything > 1200 ms
must be skippable or scrub-driven. Nothing UI-blocking may exceed 400 ms.

### Canonical easing table (canonical — others reference, never redefine)

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

Extensions (same vocabulary, for specific jobs):

| GSAP name | CSS approximation | Job |
|---|---|---|
| `power1.out` | `cubic-bezier(0.5, 1, 0.89, 1)` | subtle settles, opacity-only fades |
| `sine.inOut` | `cubic-bezier(0.37, 0, 0.63, 1)` | gentle loops, breathing/idle motion |
| `circ.out` | `cubic-bezier(0, 0.55, 0.45, 1)` | fast-arriving overlays, counters |
| `back.out(1.7)` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | playful pops, badges, toasts (~10% overshoot) |
| `elastic.out(1, 0.3)` | no CSS equivalent (multi-oscillation; JS only) | magnetic-button release, springy snaps |
| `none` | `linear` | scrubbed tweens, marquees, spinners ONLY |

Selection rules: entrances → `expo.out` / `power3.out`; exits → `power2.in`
(`cubic-bezier(0.55, 0.055, 0.675, 0.19)` — Penner easeInCubic, UNVERIFIED — confirm
before use) or simply reverse with `power2.out`; relocations / shared-element morphs →
`power2.inOut` or `power4.inOut`; attention accents → `back.out(1.7)`. GSAP's library
default is `power1.out` — always override per project via
`gsap.defaults({ ease: "power3.out" })`.

### Mapping to motion personalities (personalities owned by [doc 01](./01-visual-motion.md#specifications--parameters))

| Personality (doc 01) | Duration band | Eases from this table |
|---|---|---|
| `snappy` | 150–350 ms | `expo.out`, `power3.out`; accents `back.out(1.7)` |
| `fluid` | 400–800 ms | `power2.inOut`, `power3.out`; loops `sine.inOut` |
| `cinematic` | 600–1200 ms | `power4.inOut`, `expo.inOut`; reveals `expo.out` |

### Stagger standards (GSAP `stagger` — number = seconds between starts)

| Unit being staggered | `each` value | Notes |
|---|---|---|
| characters (SplitText) | 0.02–0.05 | recipe owned by [doc 04](./04-typography.md#code-examples) |
| words / lines | 0.06–0.10 | lines read best at 0.08 |
| cards / grid items | 0.08–0.15 | use `{ each: 0.1, from: "start" }`; grids: `grid: "auto"` |
| nav/menu items | 0.04–0.08 | overlay menus: `from: "edges"` or `"center"` |

Use `amount` (total time split across all items) instead of `each` when item count varies
— e.g. `stagger: { amount: 0.6 }` keeps a 50-item grid from taking 5 s.

### Scroll choreography parameters (ScrollTrigger)

| Parameter | Spec | Notes |
|---|---|---|
| `scrub` | `true` = locked to scrollbar; number = catch-up seconds. Default to `1`; use `0.5` for tight control, `1.5` for floaty | with Lenis active, `scrub: true` already feels smoothed |
| `pin` | `true` on the scene wrapper; `pinSpacing: true` (default) | `anticipatePin: 1` removes the jump on fast scrolls |
| `start` / `end` | `"top top"` / `"+=N"` where N = px of scroll driving the timeline; budget 600–1200 px per scene | defaults: start `"top bottom"` (`"top top"` when pinning), end `"bottom top"` |
| `snap` | `{ snapTo: "labels", duration: { min: 0.2, max: 0.6 }, delay: 0.1, ease: "power1.inOut", directional: true }` | `"labelsDirectional"` honors scroll direction; `inertia: true` respects velocity |
| `toggleActions` | default `"play none none none"`; reversible reveals: `"play none none reverse"` | onEnter / onLeave / onEnterBack / onLeaveBack |
| `invalidateOnRefresh` | `true` on any scrubbed/pinned trigger using function-based or responsive values | recalculates on resize |
| tween eases inside scrub | `ease: "none"` | scroll position IS the ease; curved eases fight the scrubber |

### Lenis parameters (`lenis@1.3.23` defaults → tuning)

| Option | Default | Tuning |
|---|---|---|
| `lerp` | `0.1` | 0.05 = heavy cinematic glide; 0.15–0.18 reads nearly native (snappy personality); stay within 0.05–0.18 — per-personality bands: [doc 01](./01-visual-motion.md#specifications--parameters) |
| `duration` | `1.2` (s) | applies to programmatic `lenis.scrollTo()` animation |
| `wheelMultiplier` / `touchMultiplier` | `1` / `1` | leave at 1; changing them breaks user expectations |
| `syncTouch` | `false` | keep `false` (iOS < 16 issues documented) |
| `autoRaf` | `false` | keep `false` with GSAP — the ticker drives `raf` (canonical recipe) |
| `anchors` | `false` | set `true` to smooth same-page anchor links |
| nested scrollers | — | mark with `data-lenis-prevent` (or `prevent: (node) => …`) |
| modals open | — | `lenis.stop()` on open, `lenis.start()` on close; `lenis.destroy()` on SPA route teardown |

ScrollSmoother alternative: `ScrollSmoother.create({ smooth: 1, effects: true })` —
`smooth` = catch-up seconds (lib default 0.8), requires the `#smooth-wrapper` >
`#smooth-content` structure, enables `data-speed="0.5"` / `data-lag="0.5"` attributes;
touch smoothing off by default (`smoothTouch: false`).

### Page-transition parameters

Support matrix (from `_facts.md`, verified 2026-06-12): same-document — Chrome/Edge ≥ 111,
Safari ≥ 18.0, Firefox ≥ 144. Cross-document — Chrome/Edge ≥ 126, Safari ≥ 18.2,
**Firefox: not supported** (as of FF 150).

| Spec | Value |
|---|---|
| full-page crossfade/slide | old out 200–300 ms `power2.out`-equivalent; new in 300–420 ms `expo.out`-equivalent |
| shared-element morph (`view-transition-name`) | 400–600 ms, `power4.inOut`-equivalent |
| total transition budget | ≤ 700 ms; navigation must complete fast — Chrome: *"more than four seconds … the view transition is skipped with a `TimeoutError` `DOMException`"* |
| `view-transition-name` | unique per rendered element; group shared styles with `view-transition-class` |
| reduced motion | disable via the canonical pattern below (pseudo-element `animation: none`) |

### Micro-interaction catalog (all in the micro / UI-transition classes)

| Pattern | Trigger | Spec |
|---|---|---|
| Hover lift | pointerenter | scale per the personality band owned by [doc 01](./01-visual-motion.md#specifications--parameters), `y: -2 to -4px`, 150–200 ms `power2.out`; reverse on leave at 200 ms |
| Press / tap | pointerdown | `scale: 0.96`, 100–120 ms `power2.out`; release springs back `back.out(1.7)` 200 ms |
| Link underline reveal | hover | `scaleX: 0 → 1`, `transform-origin: left` in / `right` out, 250–350 ms `power3.out` |
| Magnetic button | pointer inside hit area (button bounds + 20–40 px padding) | body follows pointer-offset × **0.3–0.4**; inner label × **0.5** (parallax layer); release: `elastic.out(1, 0.3)`, duration 1.0 s, via `gsap.quickTo` |
| Cursor follower | mousemove | dot/ring tweened with `gsap.quickTo(..., { duration: 0.4–0.6, ease: "power3" })`; disable on touch devices and under reduced motion; never remove the native cursor without an equal-affordance replacement |
| Image hover zoom | hover on media card | inner `<img>` `scale: 1 → 1.06`, 500–700 ms `expo.out`; container `overflow: hidden` |
| Icon nudge (arrow CTA) | hover | `x: 4–6px`, 150 ms `power2.out` |
| Toast / badge pop | mount | `scale: 0.8 → 1` + fade, 250–300 ms `back.out(1.7)` |

### Motion (`motion/react`) spring presets

Library defaults: tween `duration: 0.3` s; spring `bounce: 0.25`. Project presets:

| Preset | Config | Use |
|---|---|---|
| UI feedback | `{ type: "spring", stiffness: 300, damping: 20 }` | whileHover / whileTap |
| Magnetic | `{ type: "spring", stiffness: 150, damping: 15, mass: 0.1 }` | pointer-follow elements |
| Gentle settle | `{ type: "spring", bounce: 0.2, visualDuration: 0.4 }` | cards, list reordering |

Set project-wide defaults once via `<MotionConfig transition={{ duration: 0.3, ease: [0.19, 1, 0.22, 1] }}>`
(cubic-bezier arrays accepted — that array = `expo.out`).

## Recommended Libraries & Tools

Versions, installs, and imports per `_facts.md` (verified 2026-06-12):

| Use case | Library | Install / import |
|---|---|---|
| Timelines, scroll, FLIP, text, custom eases | GSAP **3.15.0** — 100% free incl. all former Club plugins (SplitText, MorphSVG, ScrollSmoother, DrawSVG, CustomEase…) | `npm install gsap` → `import gsap from "gsap"`; plugins: `import { ScrollTrigger } from "gsap/ScrollTrigger"` then `gsap.registerPlugin(ScrollTrigger)` |
| Smooth scroll (default) | Lenis **1.3.23** (MIT; package is `lenis` — NOT the deprecated `@studio-freight/lenis`) | `npm install lenis` → `import Lenis from "lenis"` + `import "lenis/dist/lenis.css"` |
| React component/gesture animation | Motion **12.40.0** (MIT; formerly Framer Motion) | `npm install motion` → `import { motion } from "motion/react"` |
| Page transitions | View Transitions API (platform, no install) | progressive enhancement; support matrix above |
| Legacy page transitions | Barba `@barba/core@2.10.3` — **DORMANT** (last publish 2024-08-12) | do not adopt; migrate existing Barba sites to View Transitions + GSAP fallback |

GSAP licensing caveat: free but proprietary (not MIT); cannot be embedded in no-code
animation-builder tools competing with Webflow.

## Code Examples

### 1. Canonical Lenis + ScrollTrigger setup (use everywhere, verbatim core)

```js
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";
import "lenis/dist/lenis.css"; // recommended base styles

gsap.registerPlugin(ScrollTrigger);

// — official integration, verbatim from the Lenis 1.3.23 README —
const lenis = new Lenis();
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => {
  lenis.raf(time * 1000); // Convert time from seconds to milliseconds
});
gsap.ticker.lagSmoothing(0);
// ————————————————————————————————————————————————————————————————
// lerp default 0.1 (0.05 = heavier glide; 0.15–0.18 = snappier, near-native).
// Outside GSAP contexts only: new Lenis({ autoRaf: true }).
// Modals: lenis.stop() / lenis.start(). SPA teardown: lenis.destroy().
```

### 2. Canonical `prefers-reduced-motion` pattern (MANDATORY in every build)

```js
const mm = gsap.matchMedia();
mm.add({
  motionOK:     "(prefers-reduced-motion: no-preference)",
  reduceMotion: "(prefers-reduced-motion: reduce)",
}, (context) => {
  const { reduceMotion } = context.conditions;
  if (reduceMotion) {
    gsap.set(".reveal", { opacity: 1, y: 0, clearProps: "transform" }); // end-state, instantly
    return; // also: skip new Lenis() entirely — native scroll
  }
  gsap.from(".reveal", {
    opacity: 0, y: 40,            // movement only for motion-OK users
    duration: 0.6, ease: "power3.out",
    stagger: { each: 0.08, from: "start" },
  });
  // everything created here is auto-reverted if the media condition flips
});
```

```css
@media (prefers-reduced-motion: reduce) {
  /* kill View Transition animations (official guidance) */
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) { animation: none !important; }
  /* replace movement with opacity-only, ≤ 200 ms — "reduced" ≠ "none":
     keep state-change feedback, drop parallax/scale/large translates */
}
```

Rules: reduced variant keeps opacity fades ≤ 200 ms and all state feedback; removes
parallax, pinning+scrub scenes (content must read fully without them), magnetic/cursor
effects, autoplaying loops, and smooth scrolling.

### 3. Scroll storytelling — pinned, scrubbed, snapped scene timeline

```js
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".story",
    start: "top top",
    end: "+=2400",          // 2400px of scroll drives the timeline (~800px per scene)
    pin: true,              // pinSpacing: true is the default
    scrub: 1,               // 1s catch-up; 0.5 tight, 1.5 floaty
    anticipatePin: 1,       // prevents pin-jump on fast scrolls
    snap: {
      snapTo: "labels",                  // settle on the nearest scene
      duration: { min: 0.2, max: 0.6 },
      delay: 0.1,
      ease: "power1.inOut",
      directional: true,
    },
    invalidateOnRefresh: true,
    // markers: true,       // dev only
  },
});

tl.addLabel("scene1")
  .from(".scene-1 .headline", { yPercent: 60, opacity: 0, ease: "none" }) // "none" under scrub
  .addLabel("scene2")
  .to(".scene-1", { opacity: 0, ease: "none" })
  .from(".scene-2", { xPercent: 100, ease: "none" }, "<")
  .addLabel("scene3")
  .from(".scene-3 figure", { scale: 0.8, opacity: 0, ease: "none", stagger: 0.1 });
```

### 4. Page transitions — View Transitions first, GSAP fallback

```js
// Same-document (SPA router hook) — progressive enhancement
async function transitionTo(updateDOM) {
  if (!document.startViewTransition ||
      window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    await updateDOM();                       // fallback: instant swap (or GSAP, below)
    return;
  }
  const t = document.startViewTransition(() => updateDOM());
  await t.finished;                          // also available: t.ready, t.updateCallbackDone
}
```

```css
/* Customize the default crossfade — old-out = UI-transition class; new-in = content/section-reveal class (page-transition table above) */
::view-transition-old(root) { animation-duration: 250ms; animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1); }
::view-transition-new(root) { animation-duration: 420ms; animation-timing-function: cubic-bezier(0.19, 1, 0.22, 1); }
.page-hero { view-transition-name: hero; }   /* shared-element morph, name unique per page */

/* Cross-document (MPA): opt in on BOTH pages, same-origin only. No Firefox support. */
@view-transition { navigation: auto; }
```

```js
// GSAP fallback wipe (Firefox cross-document / "identical everywhere" briefs)
async function gsapWipe(updateDOM) {
  const overlay = document.querySelector(".transition-overlay"); // fixed, inset:0, scaleY(0)
  await gsap.to(overlay, { scaleY: 1, transformOrigin: "bottom", duration: 0.5, ease: "power4.inOut" });
  await updateDOM();
  gsap.to(overlay, { scaleY: 0, transformOrigin: "top", duration: 0.5, ease: "power4.inOut" });
}
```

### 5. Magnetic button (gsap.quickTo — interruptible by design)

```js
const btn = document.querySelector(".magnetic");
const label = btn.querySelector(".magnetic__label");
const STRENGTH = 0.35;        // body follows 35% of pointer offset
const LABEL_STRENGTH = 0.5;   // inner label moves more -> parallax depth

const xTo = gsap.quickTo(btn, "x", { duration: 1, ease: "elastic.out(1, 0.3)" });
const yTo = gsap.quickTo(btn, "y", { duration: 1, ease: "elastic.out(1, 0.3)" });
const lxTo = gsap.quickTo(label, "x", { duration: 1, ease: "elastic.out(1, 0.3)" });
const lyTo = gsap.quickTo(label, "y", { duration: 1, ease: "elastic.out(1, 0.3)" });

btn.addEventListener("mousemove", (e) => {
  const { left, top, width, height } = btn.getBoundingClientRect();
  const x = e.clientX - (left + width / 2);   // offset from button center
  const y = e.clientY - (top + height / 2);
  xTo(x * STRENGTH);  yTo(y * STRENGTH);
  lxTo(x * LABEL_STRENGTH); lyTo(y * LABEL_STRENGTH);
});
btn.addEventListener("mouseleave", () => { xTo(0); yTo(0); lxTo(0); lyTo(0); });
// Gate behind: matchMedia("(pointer: fine)") AND motion-OK (pattern #2).
```

Cursor follower: identical mechanism — `gsap.quickTo(dot, "x", { duration: 0.5, ease: "power3" })`
fed from a document-level `mousemove`.

### 6. Motion micro-interaction (`motion/react`)

```jsx
import { motion } from "motion/react";

export function CTA({ children }) {
  return (
    <motion.button
      whileHover={{ scale: 1.04, transition: { type: "spring", stiffness: 300, damping: 20 } }}
      whileTap={{ scale: 0.96, transition: { duration: 0.12 } }}  // tween, 120ms press
    >
      {children}
    </motion.button>
  );
}
```

### 7. CustomEase as a brand motion token

```js
import { CustomEase } from "gsap/CustomEase";
gsap.registerPlugin(CustomEase);
CustomEase.create("brand-out", "0.19, 1, 0.22, 1");  // cubic-bezier data; = expo.out
gsap.to(".hero-title", { y: 0, opacity: 1, duration: 0.8, ease: "brand-out" });
// SVG-path data also accepted: CustomEase.create("hop", "M0,0 C0.25,0.1 0.25,1 1,1")
```

FLIP layout moves (filter grids, expanding cards): `const state = Flip.getState(".item")` →
mutate DOM/classes → `Flip.from(state, { duration: 0.6, ease: "power4.inOut", absolute: true, nested: true })`;
correlate elements across states with `data-flip-id`.

## Mode-Specific Guidance

### Create from scratch
Pick the motion personality with [doc 01](./01-visual-motion.md#specifications--parameters),
then lock: 2 primary eases + 1 accent from the canonical table, the four duration-class
values, and register them as `CustomEase`/CSS-variable tokens before building anything.
Wire the Lenis recipe and the reduced-motion pattern in the first commit, not the last.

### Re-create from existing site (reverse-engineering)
Read computed `transition-timing-function` / `transition-duration` in DevTools and snap
each curve to the NEAREST canonical ease (never copy odd beziers verbatim). Measure JS
animation durations with the Performance panel (record, read tween spans). Detect smooth
scroll: inertia after wheel stop + `transform` on a content wrapper ⇒ Lenis/ScrollSmoother
class; estimate `lerp` by feel against 0.05 / 0.1 / 0.15 references. Map scroll scenes to
pin + scrub + label structure; note snap behavior. Always re-spec into this doc's
vocabulary rather than cloning implementation details.

### Modify an existing system
Never introduce a second easing vocabulary — extend via the extension rows or one new
`CustomEase` token max. Audit existing durations into the four classes and normalize
outliers (±20% tolerance). New scroll scenes must reuse the existing Lenis instance
(one per page, ever). Verify the reduced-motion branch still covers every addition before
sign-off.

## Quality Checklist

- [ ] Every duration falls inside one of the four canonical classes (±0 ms tolerance on bounds).
- [ ] Every ease is from the canonical table (or a registered CustomEase token of one).
- [ ] Exactly one smooth-scroll instance; canonical Lenis recipe used verbatim; `lenis.destroy()` on teardown.
- [ ] All scrubbed tweens use `ease: "none"`; pinned scenes have `anticipatePin: 1`.
- [ ] `prefers-reduced-motion: reduce` path tested in-browser: no parallax, no pin+scrub traps, no smoothing, content fully readable.
- [ ] Page transitions: feature-checked `startViewTransition`, cross-document opt-in on both pages, Firefox (no cross-doc) reviewed and acceptable.
- [ ] Only `transform`/`opacity` animated; zero layout-property tweens.
- [ ] Pointer effects (magnetic, follower) gated behind `(pointer: fine)` and motion-OK.
- [ ] Hover/press feedback ≤ 200 ms; nothing UI-blocking > 400 ms; intros > 1200 ms skippable.
- [ ] INP stays < 200 ms with animations running ([doc 09](./09-tech-implementation.md#specifications--parameters)).

## Anti-Patterns

1. `linear` easing on UI movement — reads as broken; reserve for scrub/marquee/spinner.
2. Every animation at 300 ms — flat hierarchy; choreography needs class contrast.
3. Animating `width`/`height`/`top`/`left` — layout thrash; use FLIP for layout moves.
4. Scroll-hijacking: wheel events consumed, direction reversed, or snap fighting the user.
5. Two smoothing engines (Lenis + ScrollSmoother, or duplicate Lenis instances) at once.
6. Unskippable preloader/intro > 1200 ms — instant awards-jury and UX penalty.
7. Shipping without a reduced-motion branch, or treating it as "set durations to 0" only.
8. Adopting Barba.js in 2026 — dormant; use View Transitions + GSAP fallback.
9. Cross-document View Transitions as the only navigation affordance — Firefox gets nothing.
10. Magnetic/cursor effects on touch devices — dead listeners, broken affordances.
11. Curved eases inside scrubbed timelines — fights the scrubber, feels laggy.
12. Infinite attention-loops (pulsing CTAs, perpetual floaters) — vestibular triggers and noise.

## Sources & Verification

- https://www.npmjs.com/package/gsap — confirmed: gsap 3.15.0 is the latest release; 100% free incl. all former Club plugins (verified 2026-06-12)
- https://www.npmjs.com/package/lenis — confirmed: lenis 1.3.23 is the latest release of the `lenis` package (successor to the deprecated `@studio-freight/lenis`) (verified 2026-06-12)
- https://www.npmjs.com/package/motion — confirmed: motion 12.40.0 is the latest release; React import path `motion/react` (verified 2026-06-12)
- https://www.npmjs.com/package/@barba/core — confirmed: @barba/core 2.10.3 is the latest release, last published 2024-08-12 (dormant) (verified 2026-06-12)
- https://caniuse.com/view-transitions — confirmed: same-document View Transitions — Chrome/Edge ≥ 111, Safari ≥ 18.0, Firefox ≥ 144 (verified 2026-06-12)
- https://caniuse.com/cross-document-view-transitions — confirmed: cross-document View Transitions — Chrome/Edge ≥ 126, Safari ≥ 18.2, Firefox not supported (verified 2026-06-12)
- https://gsap.com/docs/v3/Plugins/ScrollTrigger/ — confirmed: `pin`/`pinSpacing`, `scrub` number = catch-up seconds, `snap` config (`snapTo` number/array/"labels"/"labelsDirectional", `duration {min,max}`, `delay`, `ease`, `directional`, `inertia`), start/end syntax + defaults (`"top bottom"`, `"top top"` when pinning, `"bottom top"`), `toggleActions` default `"play none none none"`, `anticipatePin`, `invalidateOnRefresh` (verified 2026-06-12)
- https://gsap.com/docs/v3/Eases/ — confirmed: ease families (power1–4, expo, circ, sine, back, elastic, bounce, none), config syntax `back.out(1.7)` / `elastic.out(1, 0.3)`, library default ease `power1.out` (verified 2026-06-12)
- https://gsap.com/resources/getting-started/Staggers — confirmed: `stagger` number = seconds between starts; object `{ each, amount, from: "start"|"center"|"edges"|"end"|"random", grid, axis, ease }`; each-vs-amount semantics (verified 2026-06-12)
- https://gsap.com/docs/v3/GSAP/gsap.quickTo()/ — confirmed: `gsap.quickTo(target, property, vars)` returns a setter function; documented mousemove-follower example with `duration`/`ease` (verified 2026-06-12)
- https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/ — confirmed: conditions-object syntax incl. `"(prefers-reduced-motion: reduce)"`, `context.conditions`, automatic revert/cleanup (verified 2026-06-12)
- https://gsap.com/docs/v3/Plugins/Flip/ — confirmed: `Flip.getState(targets)`, `Flip.from(state, vars)` options (`duration`, `ease`, `absolute`, `scale`, `nested`, `onEnter`, `onLeave`), `data-flip-id` (verified 2026-06-12)
- https://gsap.com/docs/v3/Eases/CustomEase/ — confirmed: `gsap.registerPlugin(CustomEase)`, `CustomEase.create("name", data)` with cubic-bezier string or SVG path data, then `ease: "name"` (verified 2026-06-12)
- https://gsap.com/docs/v3/Plugins/ScrollSmoother/ — confirmed: `ScrollSmoother.create({ smooth, effects, smoothTouch, normalizeScroll })`, `smooth` default 0.8 s, `#smooth-wrapper`/`#smooth-content` structure, `data-speed`/`data-lag` attributes, requires ScrollTrigger registration (verified 2026-06-12)
- https://github.com/darkroomengineering/lenis/blob/main/README.md — confirmed: option defaults (`lerp` 0.1, `duration` 1.2, `autoRaf` false, `syncTouch` false, `anchors` false), `lenis/dist/lenis.css`, `data-lenis-prevent` variants, `prevent` callback, `scrollTo` options, `stop()/start()/destroy()`, iOS < 16 syncTouch caveat (verified 2026-06-12)
- https://developer.chrome.com/docs/web-platform/view-transitions/same-document — confirmed: `document.startViewTransition(cb)`, `view-transition-name` uniqueness, `view-transition-class`, pseudo-element tree, default crossfade with `mix-blend-mode: plus-lighter`, `ready`/`finished`/`updateCallbackDone` promises, transition `types` + `:active-view-transition-type()` (verified 2026-06-12)
- https://developer.chrome.com/docs/web-platform/view-transitions/cross-document — confirmed: `@view-transition { navigation: auto; }` required on BOTH pages, same-origin only, `pageswap`/`pagereveal` events, 4 s `TimeoutError` skip quote, `<link rel="expect" blocking="render">` (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion — confirmed: `reduce`/`no-preference` values, `window.matchMedia('(prefers-reduced-motion: reduce)')`, vestibular-trigger guidance, replace-motion-with-opacity recommendation (verified 2026-06-12)
- https://motion.dev/docs/react-transitions — confirmed: `type: "spring"|"tween"`, spring options (`stiffness`, `damping`, `mass`, `bounce` default 0.25, `visualDuration`), tween `duration` default 0.3 s, cubic-bezier array eases, `MotionConfig` defaults, per-gesture `whileHover`/`whileTap` transitions (verified 2026-06-12)
- https://blog.olivierlarose.com/tutorials/magnetic-button — confirmed: center-offset math via `getBoundingClientRect`, `gsap.quickTo(el, "x", { duration: 1, ease: "elastic.out(1, 0.3)" })`, Motion spring `{ stiffness: 150, damping: 15, mass: 0.1 }` (verified 2026-06-12)
- https://tympanus.net/codrops/2020/08/05/magnetic-buttons/ — confirmed: magnetic pointer-follow concept with inner-element parallax (elements moving at different ratios) (verified 2026-06-12)
- https://easings.net/ — confirmed: extension cubic-bezier approximations — easeOutQuad `(0.5, 1, 0.89, 1)`, easeInOutSine `(0.37, 0, 0.63, 1)`, easeOutCirc `(0, 0.55, 0.45, 1)`, easeOutBack `(0.34, 1.56, 0.64, 1)` (verified 2026-06-12)
