---
title: Tech Stack, Performance Budgets & Implementation Architecture
doc_id: 09-tech-implementation
version: 1.0
last_verified: 2026-06-12
applies_to_modes: [create, recreate, modify]
---

## Purpose & When To Read This

Open this doc when selecting or auditing the technical stack (framework, headless CMS,
rendering mode), when enforcing performance budgets — this doc OWNS the canonical budget
table (`_conventions.md` §3.8) that docs 01/02/03/04/08 reference — when compressing 3D
models and textures for delivery (gltf-transform / Draco / Meshopt / KTX2; doc 02 *creates*
assets, this doc *compresses* them), and when implementing the accessibility practice list
(§3.9), sound design, or persistent-canvas code architecture. Not for: runtime shader and
scene budgets ([doc 08](./08-webgl-effects.md#specifications--parameters)) or animation
choreography ([doc 07](./07-animation-choreography.md#specifications--parameters)).

## Core Principles

1. **Budgets are field-measured law.** Every target in §Specifications is evaluated at the
   **75th percentile of real-user loads** (CrUX / RUM), mobile and desktop segmented — not
   on the dev machine. A lab pass with a field fail is a fail.
2. **Lightest stack that satisfies the brief.** Render HTML on the server or at build
   time; ship JavaScript only for actual interactivity. Award-level visual ambition is an
   asset-and-shader problem, not a framework-weight problem.
3. **Everything above the baseline is progressive enhancement.** View Transitions, WebGL,
   audio, and smooth scroll all degrade to a complete, intentional-looking experience
   (Firefox gets no cross-document View Transitions — per `_facts.md` — and must never
   look broken).
4. **Assets are compressed in the build pipeline, never at runtime.** No raw PNG inside a
   GLB, no full-resolution textures resized by the GPU, no client-side image scaling.
5. **Accessibility is structural, not a retrofit.** Semantic HTML, keyboard paths, focus
   management, and canvas fallbacks are part of the architecture (§3.9 list below).
6. **Sound is opt-in.** Mute by default, explicit persistent toggle, autoplay policies
   respected. A site that plays unrequested audio is an instant award/UX rejection.
7. **One canvas, one WebGL context, persistent across routes** (doc 08 rule). The router
   must never destroy and recreate the GPU world on navigation.

## Decision Framework

### Stack selection (apply in order, stop at first match)

1. **IF** the site is content-led (marketing, portfolio, editorial, campaign), navigation
   is page-to-page, and SEO matters → **Astro 6** (`astro@6.4.6`). Islands architecture:
   "Astro will automatically render every UI component to just HTML & CSS, stripping out
   all client-side JavaScript automatically"; hydrate only islands via `client:load` /
   `client:visible`. Page transitions: browser-native **cross-document View Transitions**
   (`@view-transition { navigation: auto; }`, recipe owned by
   [doc 07](./07-animation-choreography.md#specifications--parameters)). Caveat from
   `_facts.md`: Firefox (as of FF 150) does not support cross-document View Transitions —
   the un-transitioned experience must read as intentional. Use Astro's `<ClientRouter />`
   (`import { ClientRouter } from "astro:transitions"`) only when you need SPA behaviors:
   persistent islands (`transition:persist`, e.g. a WebGL canvas or audio player that must
   survive navigation) or identical transitions in every browser. Astro's own docs note
   that as browser APIs evolve, the ClientRouter "will increasingly become unnecessary".
2. **IF** the product is app-like — authenticated state, dashboards, carts, complex
   filtering, realtime data — and the team is React → **Next.js 16** (`next@16.2.9`,
   `react@19.2.7`), App Router. Server Components ship no client JS and "are automatically
   code split"; lazy-load client islands with `next/dynamic` (`ssr: false` is only allowed
   inside Client Components).
3. **IF** the same app-like profile but the team is Vue → **Nuxt 4** (`nuxt@4.4.8`).
   Universal rendering by default; use hybrid `routeRules` per route:
   `'/': { prerender: true }`, `'/products/**': { swr: 3600 }`, `'/admin/**': { ssr: false }`.
4. **IF** a persistent WebGL world *is* the site (one canvas alive across all routes) →
   any SPA-routed option: Next/Nuxt, or Astro + `<ClientRouter />` with the canvas island
   marked `transition:persist`. Never a hard-reload MPA — reloading destroys the context.
5. **WHEN to add R3F** (`@react-three/fiber@9.6.1` + `@react-three/drei@10.7.7`): only if
   the framework is already React AND the scene is component-shaped (many objects, shared
   state, per-route scene content). Otherwise vanilla `three@0.184.0` in a single island.
   Full canvas-vs-DOM decision: [doc 08](./08-webgl-effects.md#decision-framework).

### Headless CMS selection

| IF the priority is… | THEN | Client (versions: `_facts.md`) |
|---|---|---|
| Marketing team edits visually in-context, component "bloks" | Storyblok — "make changes in the editor and view the updated content in real-time" | `storyblok-js-client@7.6.1` |
| Developer-defined structured content + expressive queries | Sanity (GROQ query language, spec at spec.groq.dev) | `@sanity/client@7.22.1` |
| Enterprise governance, many spaces/locales | Contentful | `contentful@11.12.4` |
| Slice-based landing-page assembly | Prismic (Slice Machine) | `@prismicio/client@7.21.8` |

All four are API-first: content is fetched at build time (preferred) or server-side; CMS
clients never run in the browser bundle of a content site.

### Rendering-mode rules

- Prerender (SSG) every page whose content is the same for all visitors. SSR only for
  personalization. Client-render only true islands (canvas, audio, configurators).
- The canvas is always client-only: in Next, `dynamic(() => import("./Scene"), { ssr: false })`
  from inside a Client Component (Server Components reject `ssr: false`).
- Platform feature policy (referenced by [doc 05](./05-color.md#specifications--parameters)):
  Baseline *Widely available* → use freely; Baseline *Newly available* → use behind a
  fallback; anything less (e.g. cross-document View Transitions, missing in Firefox per
  `_facts.md`) → strictly progressive enhancement.

## Specifications & Parameters

### 1. Performance budget table (CANONICAL — `_conventions.md` §3.8; docs 01–08 reference this)

All Core Web Vitals at **p75 of real-user loads**, mobile and desktop segmented (web.dev).

| Budget | Target | Hard ceiling | Notes / measured with |
|---|---|---|---|
| LCP | ≤ 2.5 s | 2.5 s (no award-tier excuse) | CrUX, RUM, `web-vitals` lib |
| INP | ≤ 200 ms | 500 ms = "poor" (200–500 needs improvement) | field RUM; long interactions |
| CLS | ≤ 0.1 | 0.1 | `aspect-ratio` on all media ([doc 03](./03-layout.md#specifications--parameters)); font fallback metrics ([doc 04](./04-typography.md#specifications--parameters)) |
| JS, initial route (compressed) — content site | ≤ 170 KB | 250 KB | web.dev baseline: "less than 170 KB of JavaScript on mobile" |
| JS, total with 3D experience | ≤ 300 KB | 450 KB | `three`/R3F in a lazy chunk loaded after first paint, never in the entry bundle |
| CSS, initial route (compressed) | ≤ 50 KB | 75 KB | purge unused; no UI framework CSS dumps |
| Web fonts | ≤ 200 KB total | 200 KB | owner: [doc 04](./04-typography.md#specifications--parameters) |
| Hero image | ≤ 200 KB AVIF | 300 KB | per-slot budgets owner: [doc 02](./02-image-generation.md#specifications--parameters) |
| Images in initial viewport | ≤ 500 KB total | 800 KB | lazy-load everything below the fold |
| Total transfer, first view — content site | ≤ 1.5 MB | 2.5 MB | network panel, throttled Fast 4G |
| Total transfer, first view — 3D experience | ≤ 3.0 MB | 5.0 MB | includes models + KTX2 textures |
| Single 3D model (.glb, compressed) | ≤ 2.0 MB | 4.0 MB | after gltf-transform pipeline (§3) |
| Hero model polycount | ≤ 100 k triangles | 250 k | use `--simplify` (§3); LODs beyond ceiling |
| GPU textures per scene (KTX2 transfer) | ≤ 1.5 MB | 3.0 MB | dimensions ≤ 1024 px, 2048 px hero only ([doc 08](./08-webgl-effects.md#specifications--parameters)) |
| Audio payload per page | ≤ 1.0 MB | 2.0 MB | lazy-loaded after first interaction (§5) |
| Draw calls per frame | < 100 | 150 | §3.8 anchor; runtime owner: [doc 08](./08-webgl-effects.md#specifications--parameters) |
| Frame rate | 60 fps desktop & flagship mobile | ≥ 30 fps mid-tier | degradation tiers: doc 08 |

**LCP decomposition (arithmetic, not a separate source):** within the 2.5 s budget plan
≤ 0.8 s TTFB + ≤ 1.0 s LCP-resource load + ≤ 0.7 s render. If TTFB eats more, the hero
asset budget shrinks — fix the server first.

### 2. Feature → library map (versions pinned in `_facts.md` unless noted)

| Feature | Use | Owner doc |
|---|---|---|
| Smooth scroll | `lenis@1.3.23` | 07 |
| Timelines, scroll choreography | `gsap@3.15.0` (+ free plugins) | 07 |
| React component/gesture animation | `motion@12.40.0` | 07 |
| Page transitions | View Transitions API (no install) | 07 |
| 3D scene, vanilla | `three@0.184.0` | 08 |
| 3D scene in React | `@react-three/fiber@9.6.1` + `@react-three/drei@10.7.7` | 08 |
| 2D texture distortion on DOM media | `ogl@1.0.11` | 08 |
| Heavy 2D canvas | `pixi.js@8.19.0` | 08 |
| Post-processing | `postprocessing@6.39.1` | 08 |
| Audio | `howler@2.2.4` (MIT; version per `_facts.md` §4 — dormant ~33 months but stable) or raw Web Audio API | 09 (§5) |
| Model/texture compression | `@gltf-transform/cli@4.4.0` | 09 (§3) |
| CMS clients | table above | 09 |

### 3. Asset pipeline — model & texture compression (CANONICAL; doc 02 links here)

Install: `npm install --save-dev @gltf-transform/cli` (4.4.0). The `etc1s`/`uastc`
commands additionally require **KTX-Software** (`toktx`) installed on the machine
(stated in the CLI's own help output).

**One-shot optimize** (flags verified by executing the published 4.4.0 binary):

```bash
gltf-transform optimize model.glb out.glb --compress draco --texture-compress ktx2 --texture-size 2048
```

Verified 4.4.0 defaults if you omit flags: `--compress meshopt` (choices
`draco|meshopt|quantize|false`), `--texture-compress auto` (choices
`ktx2|webp|avif|auto|false`), `--texture-size 2048`, `--simplify true`
(`--simplify-error 0.0001`), `--instance true` (`--instance-min 5`), `--join true`,
`--palette true` (`--palette-min 5`), `--weld true`, `--prune true`, `--flatten true`.

- **Draco vs Meshopt** (per the CLI help): "Draco compresses geometry; Meshopt and
  quantization compress geometry and animation." Choose `meshopt` (default) for animated
  models and fast decode; `draco` for maximum geometry compression on static models.
- Register the matching decoder in the loader at runtime (three.js `GLTFLoader` +
  `DRACOLoader` or `MeshoptDecoder`, and `KTX2Loader` for KTX2 textures — addons paths
  per the `three` exports map in `_facts.md`).
- `--join` exists specifically to "Join meshes and reduce draw calls" — it directly
  serves the < 100 draw-call budget.

**Two-pass KTX2 — the codec rule (Khronos guidance):** color data → **ETC1S**; non-color
data (normal, occlusion-roughness-metalness) → **UASTC**. ETC1S is smallest but artifacts
on packed/high-detail channels break lighting; UASTC is larger and higher quality.

```bash
# Pass 1 — UASTC for non-color maps (normals, ORM). 4.4.0 syntax:
gltf-transform uastc in.glb tmp.glb \
  --slots "{normalTexture,occlusionTexture,metallicRoughnessTexture}" \
  --level 2 --rdo --rdo-lambda 0.5 --zstd 18
# Pass 2 — ETC1S for the remaining color maps (baseColor, emissive):
gltf-transform etc1s tmp.glb out.glb --quality 255
```

Verified parameter semantics (4.4.0 `--help`): `uastc --level` 0–4 (default 2; 4 = "Very
slow", 48.24 dB); `--rdo` is boolean, quality scalar is `--rdo-lambda` — "A good range to
try is [.25, 10]. For normal maps, try [.25, .75]" (default 1); `--zstd` 1–22 Zstandard
supercompression (0 = off; levels > 20 need decode memory caution — 18 ⇒ 8 MB window);
`etc1s --quality` 1–255 (default 128), `--compression` 0–5 (default 1), `--rdo-threshold`
"try 1.0-3.0" (default 1.25); both commands take `--slots <glob>` and `--mipmaps true`
by default. Note: the Khronos artist guide shows the older `--rdo 4` syntax; in CLI 4.4.0
use `--rdo --rdo-lambda <n>`.

**Texture sizing for KTX2:** author power-of-two dimensions (256/512/1024/2048) so
mipmaps generate cleanly; keep ≤ 1024 px per texture, 2048 px hero-only (doc 08 budget).
Standalone resizing: `gltf-transform resize` (PNG/JPEG only).

**2D image encoding (settings owned by [doc 02](./02-image-generation.md#specifications--parameters)),** assembled command:

```bash
avifenc --min 0 --max 63 -a end-usage=q -a cq-level=18 -a tune=ssim -s 6 in.png out.avif
```

### 4. Accessibility practices (CANONICAL list — `_conventions.md` §3.9)

Contrast ratios are owned by [doc 05](./05-color.md#specifications--parameters); the
reduced-motion pattern by [doc 07](./07-animation-choreography.md#code-examples). The
rest lives here:

1. **Semantic structure.** Native elements first (`button`, `a`, `nav`, `main`,
   `header`, `footer`, `dialog`); exactly one `h1`; no skipped heading levels; DOM order
   = visual order at every breakpoint (doc 03 checklist).
2. **Keyboard.** Every interactive element reachable by Tab; composite widgets use
   roving `tabindex` (active item `tabindex="0"`, rest `-1`, arrow keys move focus) per
   WAI-ARIA APG; never a positive `tabindex`; "the visual focus indicator must always be
   visible" (APG) — restyle `:focus-visible`, never `outline: none` without replacement.
3. **Focus management on SPA navigation.** After route change, call `.focus()` on the new
   view's `<main tabindex="-1">` (programmatic focus via `tabindex="-1"`, APG pattern);
   announce the new page title in an `aria-live="polite"` region. First tab stop on every
   page: a skip link to `#main`.
4. **Target size.** WCAG 2.2 SC 2.5.8 (AA): pointer targets ≥ **24 × 24 CSS px** (with
   spacing/inline exceptions). This KB's standard for primary controls: **44 × 44 px**.
5. **Canvas/WebGL fallbacks.** Canvas "is just a bitmap… not exposed to accessibility
   tools as semantic HTML is" (MDN). Therefore: meaningful fallback content *inside*
   `<canvas>…</canvas>`; mirror any narrative the scene carries as real DOM text
   (visually-hidden allowed); purely decorative scenes get `role="img"` + `aria-label`
   on a wrapper, or `aria-hidden="true"` if genuinely decorative; all interaction the
   canvas offers must have a DOM-parallel control. Body text and navigation never render
   in canvas (doc 08 Always-DOM rule).
6. **Forms & ARIA.** Every control labelled (`<label>`, not placeholder); ARIA only where
   no native semantic exists; async status changes announced via `aria-live="polite"`.
7. **Reduced motion / transparency.** Apply doc 07's canonical
   `prefers-reduced-motion` pattern to every animation, View Transition, smooth-scroll,
   and audio-reactive visual this doc's stack ships.

### 5. Sound design parameters

| Parameter | Spec |
|---|---|
| Default state | **Muted** — zero audio until the user opts in via an explicit toggle |
| Toggle | Persistent header control, ≥ 44 × 44 px, `aria-pressed`, state saved to `localStorage`; restore on next visit |
| Autoplay policy (Chrome, verified) | "Muted autoplay is always allowed"; audible playback requires a user gesture, a crossed Media Engagement Index, or an installed PWA |
| Web Audio rule (verified) | An `AudioContext` created before a user gesture starts `"suspended"` — call `context.resume()` inside the gesture handler |
| Howler specifics | `Howler.autoUnlock` defaults `true` (silent unlock on first interaction); `html5: true` streams large files instead of full download+decode; sprites define `[offset, duration]` in ms; ship `webm` + `mp3` for full coverage; ~7 KB gzipped (README; 9.7 KB measured on bundlephobia) |
| Howler maintenance | Last publish 2023-09-19 (dormant but stable, MIT). For new builds needing only 2–3 sounds, raw Web Audio API avoids the dependency |
| Mix levels | master 0.7; ambient loop 0.08–0.20; UI sfx 0.20–0.40, each ≤ 250 ms; hover sfx debounce ≥ 80 ms; duck ambient ×0.5 under voice/video |
| Crossfades | 300–800 ms between ambient states (eases: [doc 07](./07-animation-choreography.md#specifications--parameters)) |
| Loading | Lazy-load all audio after first interaction; never in the critical path; budget §1 |

### 6. Code architecture

- **Single persistent canvas.** Mount the canvas (or R3F `<Canvas>`) in the app shell
  *above* the route boundary — Next root `layout.tsx` via a Client Component, Nuxt
  `app.vue`, Astro island with `transition:persist` under `<ClientRouter />`. Routes
  publish scene intent (which content, camera state) through a small store/event bus;
  the canvas component never unmounts on navigation.
- **Three layers, one-way data flow.** `interface/` (DOM, forms, nav) → events →
  `experience/` (scene, materials, postprocessing) ← `data/` (CMS client calls at
  build/server time). The scene never drives DOM layout.
- **Web workers for heavy compute.** Anything that would block the main thread > 50 ms
  (physics, particle sims, geometry generation, large JSON parsing) runs in a Worker —
  this is an INP budget defense. For rendering itself:
  `canvas.transferControlToOffscreen()` → `worker.postMessage({ canvas }, [canvas])`;
  OffscreenCanvas supports `2d`/`webgl`/`webgl2` contexts and is Baseline Widely
  available since March 2023 (MDN).
- **Code splitting discipline.** Entry bundle = layout + first interaction only. Heavy
  libs load on intent: `next/dynamic` for client islands (`ssr: false` only inside
  Client Components), bare `import()` on user action for libraries (verified Next 16
  pattern). Server Components are code-split by default and ship no client JS.

## Recommended Libraries & Tools

| Use case | Package & version (`_facts.md`) | Install / import |
|---|---|---|
| Content/marketing framework | `astro@6.4.6` | `npm create astro@latest`; `import { ClientRouter } from "astro:transitions"` |
| React app framework | `next@16.2.9` + `react@19.2.7` | `npx create-next-app@latest`; `import dynamic from "next/dynamic"` |
| Vue app framework | `nuxt@4.4.8` | `npm create nuxt@latest` UNVERIFIED — confirm before use (scaffolder name) |
| CMS clients | `@sanity/client@7.22.1` · `storyblok-js-client@7.6.1` · `contentful@11.12.4` · `@prismicio/client@7.21.8` | `npm install <package>` |
| Asset pipeline | `@gltf-transform/cli@4.4.0` (+ KTX-Software/`toktx` for KTX2) | `npm i -D @gltf-transform/cli` |
| Audio | `howler@2.2.4` (MIT; version per `_facts.md` §4 — dormant ~33 months but stable) | `npm install howler`; `import { Howl, Howler } from "howler"` |
| Field metrics | `web-vitals` library — version not in `_facts.md`: UNVERIFIED — confirm before use | reports LCP/INP/CLS from real users |

3D/animation libraries: see the feature map in §2 and docs 07/08.

## Code Examples

### 1. Full asset-pipeline script (verified 4.4.0 flags)

```bash
#!/usr/bin/env bash
set -euo pipefail
IN="$1"; OUT="$2"
# Geometry: meshopt (animated-safe) + simplify + join (draw-call budget) + 2048px cap
gltf-transform optimize "$IN" /tmp/_o.glb --compress meshopt --texture-compress false
# Textures, pass 1: UASTC for non-color data (normals/ORM)
gltf-transform uastc /tmp/_o.glb /tmp/_u.glb \
  --slots "{normalTexture,occlusionTexture,metallicRoughnessTexture}" \
  --level 2 --rdo --rdo-lambda 0.5 --zstd 18
# Textures, pass 2: ETC1S for color data (baseColor, emissive)
gltf-transform etc1s /tmp/_u.glb "$OUT" --quality 255
# Budget gate (§1): single model ≤ 2.0 MB target / 4.0 MB ceiling
SIZE=$(wc -c < "$OUT")
[ "$SIZE" -le 4194304 ] || { echo "FAIL: $SIZE bytes > 4 MB ceiling"; exit 1; }
[ "$SIZE" -le 2097152 ] || echo "WARN: $SIZE bytes > 2 MB target"
```

### 2. Persistent canvas in Next 16 App Router (single context across routes)

```tsx
// app/_components/ExperienceShell.tsx — Client Component wrapper
"use client";
import dynamic from "next/dynamic";
// ssr:false is valid here ONLY because this file is a Client Component
const Scene = dynamic(() => import("./Scene"), { ssr: false });
export default function ExperienceShell() {
  return <Scene />; // mounts ONE <Canvas>; routes message it via a store
}
// app/layout.tsx (Server Component) renders <ExperienceShell /> OUTSIDE
// {children}, so route changes swap DOM content but never unmount the canvas.
```

### 3. Sound manager — mute by default, gesture-unlocked (howler@2.2.4)

```js
import { Howl, Howler } from "howler";
const KEY = "sound-enabled";                       // persisted opt-in
Howler.mute(true);                                  // muted until user opts in
Howler.volume(0.7);                                 // master (§5 mix levels)
const ambient = new Howl({
  src: ["/audio/ambient.webm", "/audio/ambient.mp3"],
  html5: true,                                      // stream large file (no full decode)
  loop: true, volume: 0.15,                         // ambient band 0.08–0.20
});
const ui = new Howl({
  src: ["/audio/ui.webm", "/audio/ui.mp3"],
  sprite: { click: [0, 120], hover: [200, 90] },    // [offset, duration] in ms
  volume: 0.3,
});
export function setSound(on, toggleEl) {
  Howler.mute(!on);                                 // AudioContext unlock is handled by
  localStorage.setItem(KEY, String(on));            // Howler.autoUnlock (default true) on
  toggleEl.setAttribute("aria-pressed", String(on));// the same user gesture
  if (on && !ambient.playing()) ambient.play();
}
// Restore: only re-enable on a returning user's explicit prior opt-in.
if (localStorage.getItem(KEY) === "true") { /* show toggle as ON, unmute on first gesture */ }
```

### 4. Route-change focus management (works with any SPA router)

```js
// After the router commits new DOM (e.g. inside startViewTransition's update callback):
function onRouteChange(pageTitle) {
  const main = document.querySelector("main");      // <main tabindex="-1">
  main.focus({ preventScroll: true });              // programmatic focus (APG tabindex=-1)
  document.getElementById("route-announcer")        // <div aria-live="polite" class="sr-only">
    .textContent = `${pageTitle} loaded`;
}
```

## Mode-Specific Guidance

### Create from scratch
Run the stack decision tree first and record the verdict (framework, CMS, rendering mode
per route type) in the spec artifact (schemas:
[doc 10](./10-modes-and-artifacts.md#specifications--parameters)). Copy the §1 budget table into
the project README as the contract; wire a CI gate that fails the build on bundle-size or
Lighthouse regression. Set up the §3 asset pipeline as an npm script before the first
model lands.

### Re-create from existing site (reverse-engineering)
Detect the stack from signals: `/_next/` assets + `__NEXT_DATA__`/RSC payload → Next;
`__NUXT__` state → Nuxt; `astro-island` custom elements → Astro. Pull the site's real
CWV from public p75 field data (CrUX) before deciding what to match or beat. In the
network panel, inspect GLB payloads for `KHR_draco_mesh_compression` /
`EXT_meshopt_compression` / `KHR_texture_basisu` to reverse the asset pipeline; record
model sizes, texture formats, and draw calls against the §1 table. Re-create the budget,
not just the look.

### Modify an existing system
Measure p75 baselines before touching anything; after the change, no §1 budget may
regress (> 10% regression on any row requires explicit sign-off — mirrors doc 08's rule).
Keep the existing framework unless it fails a budget gate that islands/code-splitting
cannot fix; a stack migration is a separate project, never a side effect. When adding
sound or 3D to a site that had none, the *combined* page must still pass §1.

## Quality Checklist

- [ ] Stack decision recorded with the IF/THEN path that selected it.
- [ ] All §1 budgets green at p75 in field data (or lab + throttled Fast 4G pre-launch).
- [ ] CI fails on JS-budget or Lighthouse regression; budgets in the README.
- [ ] Every GLB ran through the §3 pipeline; ETC1S on color maps, UASTC on normal/ORM;
      no PNG/JPEG textures inside shipped GLBs.
- [ ] Keyboard-only walkthrough passes: skip link, visible focus, roving tabindex in
      composites, focus moved on every route change.
- [ ] Canvas has DOM fallback content; no text or nav rendered in canvas.
- [ ] Sound: muted by default, ≥ 44 px persistent toggle, `AudioContext.resume()` only
      on gesture, audio lazy-loaded.
- [ ] Exactly one WebGL context; canvas survives navigation; heavy compute (> 50 ms)
      in workers.
- [ ] Firefox checked: no cross-document View Transitions — page still reads intentional.
- [ ] `prefers-reduced-motion` honored everywhere (doc 07 pattern).

## Anti-Patterns

- **Three.js in the entry bundle.** The 3D chunk loads after first paint, on intent or
  visibility — never blocking LCP/INP.
- **SPA framework for a brochure site.** Shipping a router, hydration, and client state
  for five static pages burns the 170 KB JS budget on nothing.
- **ETC1S normal maps.** Block artifacts in non-color data corrupt lighting; the
  Khronos rule is UASTC for normal/ORM, ETC1S for color.
- **Uncompressed GLBs** (raw PNG textures, no Draco/Meshopt): 10–20× the §1 model budget.
- **Autoplaying audio** or auto-unmuting on load — blocked by Chrome policy and an
  instant UX rejection; sound is opt-in (§5).
- **`outline: none` without a `:focus-visible` replacement** — fails APG's "always
  visible" rule.
- **Text or navigation inside canvas** — invisible to assistive tech, SEO, and selection
  (MDN: canvas is "just a bitmap").
- **Recreating the WebGL context per route** — multi-second navigation jank and GPU
  memory churn; one persistent canvas (§6).
- **Dev-machine-only performance sign-off** — budgets hold at p75 of real users on
  mid-tier mobile, not on an M-series laptop on fiber.
- **Adopting dormant dependencies blind** — Barba (dormant, `_facts.md`) and Howler
  (last publish 2023-09-19) need a maintenance check before new adoption.

## Sources & Verification

- https://registry.npmjs.org/howler — confirmed: `howler` latest = 2.2.4, published 2023-09-19, MIT (verified live via registry JSON, 2026-06-12)
- https://registry.npmjs.org/@gltf-transform/cli — confirmed: 4.4.0 binary fetched from npm; all `optimize`/`uastc`/`etc1s` flags, defaults, and allowed values in §3 taken verbatim from the executed 4.4.0 `--help` output, including `--compress` default `meshopt`, `--texture-compress` default `auto`, `--texture-size` default 2048, `--rdo-lambda` normal-map range [.25, .75], `etc1s --quality` default 128, KTX-Software dependency note, and `--join` "reduce draw calls" (verified 2026-06-12)
- https://gltf-transform.dev/cli — confirmed: command roster (draco, meshopt, quantize, weld, simplify, resize, etc1s, uastc, webp, avif) and the documented `optimize … --compress draco --texture-compress webp` example pattern (verified 2026-06-12)
- https://github.com/KhronosGroup/3D-Formats-Guidelines/blob/main/KTXArtistGuide.md — confirmed: "textures with color data should use ETC1S while textures with non-color data (such as roughness-metallic or normal maps) should use UASTC"; ETC1S suits solid/monochromatic areas; UASTC suits packed ORM/normal channels (verified 2026-06-12)
- https://raw.githubusercontent.com/KhronosGroup/3D-Formats-Guidelines/main/subpages/KTXArtistGuide_glTF-Transform.md — confirmed: recommended two-pass workflow (UASTC `--slots "{normalTexture,occlusionTexture,metallicRoughnessTexture}"` + `--zstd 18` first, ETC1S `--quality 255` second); guide shows older `--rdo 4` syntax (verified 2026-06-12)
- https://docs.astro.build/en/guides/view-transitions/ — confirmed: `<ClientRouter />` from `"astro:transitions"`, `transition:name`, `transition:persist`, `fallback` = `animate|swap|none`, and the statement that the ClientRouter "will increasingly become unnecessary" as browser APIs evolve (verified 2026-06-12)
- https://docs.astro.build/en/concepts/islands/ — confirmed: zero client-side JS by default; `client:load` / `client:visible` selective hydration (verified 2026-06-12)
- https://nextjs.org/docs/app/guides/lazy-loading — confirmed: `next/dynamic`; Server Components "automatically code split"; `ssr: false` only valid inside Client Components, errors in Server Components (page version tag 16.2.9; verified 2026-06-12)
- https://nuxt.com/docs/guide/concepts/rendering — confirmed: universal rendering default; hybrid `routeRules` with `prerender`, `swr`, `isr`, `ssr: false` examples (verified 2026-06-12)
- https://developer.chrome.com/blog/autoplay — confirmed: "Muted autoplay is always allowed"; audible autoplay requires gesture / MEI / installed PWA; pre-gesture `AudioContext` starts `"suspended"` and needs `resume()` after the gesture (verified 2026-06-12)
- https://raw.githubusercontent.com/goldfire/howler.js/master/README.md — confirmed: `Howler.autoUnlock` default true; `html5: true` for streaming large files; sprites in ms; `Howler.mute()`/`Howler.volume()`; webm+mp3 coverage; "as light as 7kb gzipped"; MIT (verified 2026-06-12)
- https://bundlephobia.com/api/size?package=howler@2.2.4 — confirmed: howler 2.2.4 measures 9,705 B gzipped (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/canvas — confirmed: provide fallback content inside `<canvas>`; "Canvas content is not exposed to accessibility tools as semantic HTML is" (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas — confirmed: `transferControlToOffscreen()`, worker rendering pattern, 2d/webgl/webgl2 contexts, Baseline Widely available since March 2023 (verified 2026-06-12)
- https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/ — confirmed: roving tabindex pattern, `tabindex="-1"` for programmatic focus, "The visual focus indicator must always be visible" (verified 2026-06-12)
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — confirmed: SC 2.5.8 (AA) "at least 24 by 24 CSS pixels" with spacing/equivalent/inline/user-agent/essential exceptions (verified 2026-06-12)
- https://web.dev/articles/performance-budgets-101 — confirmed: budget methodology (quantity/milestone/rule metrics); "under 170 KB of critical-path resources (compressed/minified)"; example budget "less than 170 KB of JavaScript on mobile" (verified 2026-06-12)
- https://www.storyblok.com/docs/concepts/visual-editor — confirmed: "Make changes in the editor and view the updated content in real-time" (verified 2026-06-12)
- https://spec.groq.dev/ — confirmed: GROQ has a maintained public specification (version list); Sanity's query language (verified 2026-06-12)
- Core Web Vitals thresholds, View Transitions support matrix (incl. Firefox cross-document gap), and every package version cited above: `_facts.md` (its own sources, verified 2026-06-12)
