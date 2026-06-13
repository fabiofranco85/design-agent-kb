---
title: WebGL & Shader Effects
doc_id: 08-webgl-effects
version: 1.0
last_verified: 2026-06-12
applies_to_modes: [create, recreate, modify]
---

## Purpose & When To Read This

Open this doc whenever a design direction calls for a `<canvas>` layer: the
`immersive-3d` archetype, any `showcase` intensity tier, or any single effect (hover
distortion, particles, fluid trails, raymarched visuals) that CSS/SVG cannot produce
([archetype decision: doc 01](./01-visual-motion.md#decision-framework)). It owns the
canvas-vs-DOM decision, the GLSL technique catalog, and GPU performance rules. It does
NOT own the full performance-budget table or asset-pipeline commands — those live in
[doc 09](./09-tech-implementation.md#specifications--parameters).

## Core Principles

1. **Lightest tool that achieves the effect.** The escalation ladder is
   CSS/SVG → OGL → PixiJS → three.js → WebGPU/TSL. Every step up costs bundle weight,
   GPU memory, and maintenance. A hover distortion does not justify a 3D engine.
2. **One canvas, one context.** A page gets at most one WebGL context. Effects on
   multiple DOM images are rendered as planes inside the single canvas, position-synced
   to their DOM rects — never one context per element.
3. **GPU memory is borrowed, never owned.** Everything you allocate you must free:
   `geometry.dispose()`, `material.dispose()`, `texture.dispose()`,
   `renderTarget.dispose()`. The three.js manual is explicit: geometries "are only
   deleted if you call `BufferGeometry.dispose()`". Verify with `renderer.info`.
4. **Pre-baked beats real-time.** Bake simulations, light, and AO offline whenever the
   result is deterministic (the Lusion method —
   [doc 01](./01-visual-motion.md#core-principles)). Spend real-time GPU only on
   pointer/scroll-reactive work.
5. **Effects serve content.** Award-level shader work distorts the actual images, type,
   and scenes of the site — it is not a free-floating ornament layer. If removing the
   effect changes nothing about comprehension or brand, cut it.
6. **Budgets are pinned.** WebGL scenes target **< 100 draw calls, hard ceiling 150**
   (`_conventions.md` §3.8). LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 still apply with a
   canvas on screen — full table in
   [doc 09](./09-tech-implementation.md#specifications--parameters).
7. **Degrade in tiers, not cliffs.** Quality falls in steps (dpr → sim resolution →
   effect off → static poster); never "works on M-series, slideshow on Android".
8. **Reduced motion is a first-class variant.** Persistent shader loops pause and render
   one static frame under `prefers-reduced-motion` — canonical pattern owned by
   [doc 07](./07-animation-choreography.md#specifications--parameters).

## Decision Framework

This section is the canonical **canvas-vs-DOM decision** (docs 01 and 02 link here).
Apply in order; stop at the first match. Bias every tie toward the lighter tool.

**Step 0 — Gate by direction.** IF archetype/intensity from
[doc 01](./01-visual-motion.md#decision-framework) is `ambient` → no persistent canvas;
only event-driven effects (hover/scroll) are allowed, and only if Step 1 fails.
IF > 60% of content is long-form text → canvas may only be an accent layer, never the base.

**Step 1 — Can CSS/SVG do it? THEN no WebGL.**
- Blurs, color shifts, blend modes → CSS `filter` / `mix-blend-mode`.
- Masked reveals, shape morphs → `clip-path`, SVG masks.
- Static turbulence/displacement on a still image → SVG `feTurbulence` +
  `feDisplacementMap`.
- Page transitions → View Transitions API
  ([doc 07](./07-animation-choreography.md#specifications--parameters)).
- Grain → a tiled 128–256 px noise PNG at 3–6% opacity costs 0 GPU programs.

**Step 2 — 2D texture distortion on DOM media → OGL (`ogl@1.0.11`).**
Hover displacement, flowmap trails, scroll bend, bulge lenses on images/video need only
planes + fragment shaders. OGL delivers this without three.js's scene-graph weight.
gpu-curtains 0.16.3 is the WebGPU-era option for DOM-synced planes by the curtains.js
author ("official successor" status: UNVERIFIED — confirm before use).

**Step 3 — 2D-heavy scenes (thousands of sprites, 2D filters, canvas typography) →
PixiJS (`pixi.js@8.19.0`).** Its WebGL renderer is the official default ("Default
renderer using WebGL/WebGL2. Well supported and stable."); its WebGPU renderer is
official-experimental ("More performant, still maturing.").

**Step 4 — True 3D (models, depth, lights, camera moves, 3D particles) →
three.js (`three@0.184.0` / r184).**
- Vanilla JS / Astro / minimal-framework site → plain three.js.
- React app where scene state and UI state interleave → `@react-three/fiber@9.6.1`
  + `@react-three/drei@10.7.7`.

**Step 5 — Compute-first or WebGPU-targeted work → `three/webgpu` + TSL.**
Ship only with the automatic WebGL 2 fallback path tested (see Specifications §5).
Treat as progressive enhancement, not baseline, while the renderer is official-experimental.

**Step 6 — Always-DOM rule.** Body text, navigation, and form controls stay DOM,
regardless of steps above. Canvas never owns interactive text (accessibility, SEO,
selection). WebGL type is for display/hero moments only.

## Specifications & Parameters

### 1. Runtime budgets (numbers the agent enforces)

| Parameter | Target | Hard limit | Measure with |
|---|---|---|---|
| Draw calls per frame | < 100 | 150 (`_conventions.md` §3.8) | `renderer.info.render.calls` |
| Device pixel ratio | `min(devicePixelRatio, 2)` | 1.5 when a fullscreen fragment shader (raymarch/fluid) runs | renderer `setPixelRatio` / R3F `dpr={[1, 2]}` |
| Frame rate | 60 fps desktop & flagship mobile | ≥ 30 fps mid-tier mobile, else drop a degradation tier | DevTools performance trace |
| Texture dimensions | ≤ 1024 px per plane texture | 2048 px (hero only) | asset pipeline, [doc 09](./09-tech-implementation.md#specifications--parameters) |
| Displacement maps | 512–1024 px grayscale, ≤ 256 KB | 2048 px | export spec owned by [doc 02](./02-image-generation.md#specifications--parameters) |
| CPU particles (`THREE.Points`) | ≤ 30,000 | 50,000 — above this go GPGPU | vertex count |
| GPGPU sim texture | 128² = 16,384 (mobile) / 256² = 65,536 (desktop) | 512² = 262,144 (`showcase` desktop only) | `GPUComputationRenderer(sizeX, sizeY, renderer)` |
| Raymarch steps | ≤ 64 | 100; render at 0.5× resolution if fullscreen | shader `MAX_STEPS` |
| Post-processing | 1 composer, effects merged into 1 `EffectPass` | 2 passes (e.g. + SMAA) | pass count |
| Fluid sim resolution | 0.25× canvas (sim) / 0.5× (dye) | 0.5× / 1.0× | FBO sizes |

Instancing context: pmndrs docs state plainly that instancing allows "hundreds of
thousands of objects in a single draw call" — repeated geometry is never N meshes.
`InstancedMesh` = same geometry + same material, 1 draw call. `BatchedMesh` = *different*
geometries, same material: "Use this class if you have to render a large number of
objects with the same material but with different geometries or world transformations."
Constructor: `new BatchedMesh(maxInstanceCount, maxVertexCount, maxIndexCount, material)`.

### 2. GLSL technique catalog (effect → approach → reference)

| Effect | Approach + key parameters | Primary reference |
|---|---|---|
| Hover displacement transition | Sample grayscale disp map; `mix(texA, texB, p)` with UV offset `disp.r * p * 0.05–0.2`; tween `p` 600–900 ms `power3.out` | Codrops "WebGL Distortion Hover Effects" (2018) |
| Velocity RGB shift | Offset R-channel UV by pointer/scroll velocity; magnitude 0.002–0.01 UV; lerp back at 0.08–0.12/frame | Codrops "Motion Hover Effects with Image Distortions" (2019) |
| Mouse flowmap | Ping-pong flowmap FBO ~128 px: RG = velocity xy, B = speed; falloff ≈ 0.3, dissipation ≈ 0.98; bend UVs by flow | Codrops "Mouse Flowmap Deformation with OGL" (2019) |
| Scroll distortion + grain | Bend plane vertices ∝ scroll velocity (clamp 0.2–0.4 units); hash-noise grain at 0.03–0.08; sync planes to DOM rects | Codrops "Distortion and Grain Effects on Scroll" (2024) |
| Grid/pixel displacement | Data texture grid (~34×34) accumulates pointer offsets, relaxes ×0.9/frame; sample for UV + RGB shift | Codrops "Grid Displacement Texture with RGB Shift" (2024); "Pixel Distortion" (2022) |
| Bulge / lens | Radial UV warp: `uv − dir * strength * smoothstep(radius, 0., dist)`; strength 0.3–1.0, radius 0.2–0.4 UV | Codrops "Bulge Distortion Effect with WebGL" (2023) |
| Fluid simulation | Navier-Stokes ping-pong FBOs: advection → divergence → pressure (Jacobi 20–40 iterations) → gradient subtract; sim at 0.25× res | Codrops "WebGPU Fluid Simulations" (2025); Pavel Dobryakov's WebGL fluid sim |
| Noise reveal / dissolve | `step/smoothstep(p − 0.05, p + 0.05, fbm(uv * 3–6))` against progress `p`; optional emissive edge band 0.02–0.08 wide | Codrops "Shader-Based Reveal Effect with R3F & GLSL" (2024); Book of Shaders ch. 11 |
| Chromatic aberration | `ChromaticAberrationEffect`, offset 0.0005–0.002, modulated radially toward frame edges | pmndrs/postprocessing |
| Bloom | `BloomEffect` with mipmap blur; luminanceThreshold 0.7–0.9, intensity 0.5–1.5 | pmndrs/postprocessing; Three.js Journey "Post-processing" |
| Film grain | `NoiseEffect` (OVERLAY/SOFT_LIGHT blend) at 0.03–0.08, or hash grain in the final pass | pmndrs/postprocessing; Codrops scroll-grain (2024) |
| Dithering / retro shading | Ordered dithering with 4×4 or 8×8 Bayer matrix, 2–8 luminance levels; single pass (Codrops demo: < 0.2 ms at 4K, ~3 KB) | Codrops "Bayer Dithering" (2025); "Real-Time Dithering Shader" (2025) |
| Vertex-noise surfaces (sea, blobs, terrain) | fbm 3–5 octaves in vertex shader; amplitude ≤ 0.15× object scale; recompute normals (neighbour or analytic) | Three.js Journey "Raging Sea" (L29), "Shader Patterns" (L28) |
| GPGPU particles | `GPUComputationRenderer` sim 128²–512²; curl-noise/flow-field velocity; point size 1–4 px × dpr | Three.js Journey "GPGPU Flow Field Particles"; Codrops "Dreamy Particle Effect" (2024) |
| Raymarched SDF scene | `sdSphere/sdBox/sdTorus` + `opSmoothUnion` (k 0.1–0.5); ≤ 64 steps, surface ε 0.001, max dist 100 | iquilezles.org "distfunctions" + "raymarchingdf" |

### 3. Noise functions (shared by half the catalog)

Per The Book of Shaders ch. 11 (Gonzalez Vivo & Lowe): **value noise** (interpolated
random values, blocky), **gradient/Perlin** (interpolated gradients, smoother), **simplex**
(triangular grid, fewer corner samples, cheapest per quality). Defaults: fbm with
3–5 octaves, lacunarity 2.0, gain 0.5, base frequency 2–6 over UV space. Use a
precomputed 256 px noise texture instead of in-shader simplex when > 2 octaves are
needed per fragment on mobile.

### 4. Raymarching / SDF rules

- Distance functions and operator names come from Inigo Quilez's catalog (`sdSphere`,
  `sdBox`, `sdRoundBox`, `sdTorus`, `sdCapsule`, `sdOctahedron`, …; `opUnion`,
  `opSubtraction`, `opIntersection` and their `opSmooth*` variants).
- Loop budget: 64 steps default, ε = 0.001, max distance 100, early-exit on both.
- Normals: central differences with eps 0.0005–0.001 (4-tap tetrahedron variant saves
  2 taps).
- Fullscreen raymarch renders to a 0.5× render target, upscaled — never at native dpr.
- Use for: hero blobs, smooth-blended metaballs, abstract brand objects. Do not
  raymarch what a 5,000-triangle mesh can show.

### 5. WebGPU / TSL guidance (status per `_facts.md`)

- Official status, quoted verbatim from the three.js manual: *"The renderer itself is
  still in an experimental state although its maturity level has been greatly improved
  in the last years."*
- Fallback is automatic, quoted: *"If a device/browser doesn't support WebGPU, the
  renderer can automatically fall back to using a WebGL 2 backend."* Caveat, quoted:
  *"Still, depending on your application and scene setup, you will encounter missing
  features or a better performance with WebGLRenderer."*
- **Write once → WGSL + GLSL:** *"With TSL, developers can write shader code with
  JavaScript in a platform-independent manner. Shader code written in TSL can be
  transpiled to WGSL or GLSL depending on the available backend."* Author new
  WebGPU-path materials in TSL, not raw WGSL, so the WebGL 2 fallback stays free.
- Imports: `import * as THREE from "three/webgpu"` and nodes from `"three/tsl"`.
  Init is async: use `renderer.setAnimationLoop()` (auto-inits) or `await renderer.init()`.
- Post-processing on the WebGPU path uses three's node-based **`RenderPipeline`**
  (renamed from `PostProcessing` in r183; works only with `WebGPURenderer`):
  `pipeline.outputNode = pass(scene, camera)`. pmndrs `postprocessing@6.39.1` is
  WebGL-only (peer `three >= 0.168 < 0.185`); its v7 beta's WebGPU support details are
  UNVERIFIED — confirm before use.
- R3F: stable `9.6.1` is the production WebGL path. v10 (`10.0.0-alpha.2`, alpha only)
  release notes state: *"R3F now supports the WebGLRenderer and WebGPURenderer"* and
  *"WebGPU and TSL is first-class, with new built-ins just for working with TSL:
  useUniforms, useNodes, useLocalNodes and usePostProcessing."* Do not ship the alpha.

### 6. Degradation ladder (apply top-down until ≥ 30 fps)

1. dpr 2 → 1.5 → 1.25.
2. Sim/FBO resolution one tier down (256² → 128²; fluid 0.5× → 0.25×).
3. Post-processing: drop bloom mip levels, then drop the whole `EffectPass`.
4. Persistent loop → render-on-demand (pointer/scroll events only).
5. Canvas off → static poster `<img>` (same art, exported per
   [doc 02](./02-image-generation.md#specifications--parameters)).
Tier selection: capability check (WebGL2 support, `devicePixelRatio`,
`navigator.hardwareConcurrency` ≤ 4 → start at tier 2) plus a 2 s rolling fps probe.

### 7. Reference studios (WebGL craft benchmarks)

Lusion (Awwwards SOTM; Cannes Lions, FWA), Active Theory, Unseen Studio, OFF+BRAND
(Awwwards Site of the Year 2025), Resn, Dogstudio — archetype mapping owned by
[doc 01](./01-visual-motion.md#specifications--parameters). Browse
awwwards.com/websites/webgl/ for current jury-validated work; study *restraint*
(one signature effect per site), not effect count.

## Recommended Libraries & Tools

Versions are pinned by `_facts.md` — never re-resolve them.

| Use case | Library | Install / import |
|---|---|---|
| True 3D scenes (baseline) | `three@0.184.0` (r184, MIT) | `npm install three` → `import * as THREE from "three"`; addons from `"three/addons/*"` |
| WebGPU + TSL path | same package | `import * as THREE from "three/webgpu"`, nodes from `"three/tsl"` |
| React 3D | `@react-three/fiber@9.6.1` (MIT; requires React 19) | `npm install three @react-three/fiber` |
| R3F helpers (loaders, `shaderMaterial`, controls) | `@react-three/drei@10.7.7` (MIT) | `npm install @react-three/drei` (v11-alpha ↔ fiber v10 pairing: UNVERIFIED — confirm before use) |
| Post-processing (WebGL) | `postprocessing@6.39.1` (Zlib; peer `three >=0.168 <0.185`) | `npm install postprocessing` |
| Lightweight 2D/DOM distortion | `ogl@1.0.11` (Unlicense) | `npm install ogl` → `import { Renderer, Program, Flowmap } from "ogl"` |
| 2D sprite/filter scenes | `pixi.js@8.19.0` (MIT) | `npm install pixi.js` → `import { Application } from "pixi.js"` |
| DOM-synced WebGPU planes | `gpu-curtains@0.16.3` (MIT) | successor status UNVERIFIED — confirm before use |
| Legacy DOM-synced WebGL | `curtainsjs@8.1.6` — dormant (last publish 2024-05); avoid for new builds ("officially legacy": UNVERIFIED — confirm before use) | — |
| GPGPU | `GPUComputationRenderer` (ships with three) | `import { GPUComputationRenderer } from "three/addons/misc/GPUComputationRenderer.js"` |

Diagnostic tools: `renderer.info` (the manual: it "tells you how many textures,
geometries and shader programs are internally stored"); Spector.js browser extension for
per-frame draw-call capture; Chrome DevTools Performance panel for GPU-time traces.

## Code Examples

### R3F + drei `shaderMaterial` — displacement hover with RGB shift (current API)

```jsx
import * as THREE from 'three'
import { useRef } from 'react'
import { Canvas, extend, useFrame } from '@react-three/fiber'
import { shaderMaterial, useTexture } from '@react-three/drei'

// Uniforms become props/setters automatically (drei shaderMaterial contract).
const DistortMaterial = shaderMaterial(
  { uHover: 0, uTexture: null, uDisp: null }, // uHover: 0→1
  /* glsl */ `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }`,
  /* glsl */ `
    uniform float uHover;
    uniform sampler2D uTexture;
    uniform sampler2D uDisp;   // grayscale map — export spec: doc 02
    varying vec2 vUv;
    void main() {
      float d = texture2D(uDisp, vUv).r;
      vec2 off = vec2(d * 0.08 * uHover, 0.0);   // max 0.08 UV displacement
      float r  = texture2D(uTexture, vUv + off * 1.5).r; // R leads = RGB shift
      vec2  gb = texture2D(uTexture, vUv + off).gb;
      gl_FragColor = vec4(r, gb, 1.0);
    }`
)
extend({ DistortMaterial })

function Card({ url }) {
  const mat = useRef()
  const target = useRef(0)
  const [tex, disp] = useTexture([url, '/disp/clouds-1024.png'])
  useFrame((_, delta) => {
    // Mutate in the loop — never setState per frame (transient updates).
    // Exponential approach ≈ 300 ms settle:
    mat.current.uHover += (target.current - mat.current.uHover) * (1 - Math.exp(-10 * delta))
  })
  return (
    <mesh
      onPointerOver={() => (target.current = 1)}
      onPointerOut={() => (target.current = 0)}>
      <planeGeometry args={[1, 1.33]} />
      {/* key={...key} enables shader hot-reload (documented drei pattern) */}
      <distortMaterial key={DistortMaterial.key} ref={mat} uTexture={tex} uDisp={disp} transparent />
    </mesh>
  )
}

export default function Scene() {
  return (
    <Canvas
      dpr={[1, 2]}                                  // hard dpr cap: 2
      gl={{ antialias: true, powerPreference: 'high-performance' }}
      camera={{ position: [0, 0, 2], fov: 45 }}>
      <Card url="/img/work-01-1024.jpg" />
    </Canvas>
  )
}
// Static scenes: add frameloop="demand" and call invalidate() from event
// handlers — R3F then renders only when something actually changed.
```

### Vanilla three.js — lifecycle, on-demand render, context loss

```js
import * as THREE from 'three'

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true })
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)) // dpr cap: 2

let dirty = true
const invalidate = () => { dirty = true }
renderer.setAnimationLoop(() => {           // rAF-driven; pauses in hidden tabs
  if (!dirty) return                        // on-demand: skip identical frames
  dirty = false
  renderer.render(scene, camera)
})
window.addEventListener('resize', invalidate)        // + tween/scroll callbacks

function teardown() {                       // SPA route change / unmount
  geometry.dispose(); material.dispose(); texture.dispose()
  renderTarget?.dispose(); renderer.dispose()
  console.log(renderer.info.memory)         // expect counts back at baseline
}

canvas.addEventListener('webglcontextlost', (e) => {
  e.preventDefault()
  canvas.replaceWith(posterImg)             // same fallback as no-WebGL path
})
```

## Mode-Specific Guidance

### Create from scratch
Run the Decision Framework before writing any code and record the chosen rung + the
ruled-out lighter options in the project artifact
([doc 10](./10-modes-and-artifacts.md#specifications--parameters)). Instrument
`renderer.info.render.calls` from day one. Define desktop/mobile tiers up front
(sim texture 256² vs 128², textures 1024 vs 512 px). Build the static-poster fallback
first — it is also the reduced-motion and no-WebGL variant.

### Re-create from existing site (reverse-engineering)
Detect: inspect for `<canvas>`, then capture a frame with Spector.js to count draw
calls and read shader source. Classify each observed effect against the catalog in
Specifications §2 (e.g. "UVs bend with pointer velocity, trail decays ≈ 1 s" →
flowmap, dissipation ≈ 0.98). Estimate magnitudes by frame-stepping a screen recording
(offset in UV ≈ pixel shift ÷ canvas width). Record effect → catalog row → parameters
in the artifact; re-implement from the catalog reference, never by copying shader code
(license risk).

### Modify an existing system
Never add a second WebGL context — extend the existing scene/composer. Before upgrading
`three`, check the `postprocessing` peer range (`>= 0.168 < 0.185` at 6.39.1). Match
the codebase's uniform naming (`u`-prefix) and effect vocabulary; one new effect must
not introduce a second noise implementation if one exists. Re-measure draw calls and
frame time after the change: > 10% regression requires explicit sign-off.

## Quality Checklist

- [ ] Lighter-tool options explicitly ruled out (CSS/SVG → OGL → PixiJS) and recorded.
- [ ] Exactly one WebGL context on the page.
- [ ] `renderer.info.render.calls` < 100 (ceiling 150) on the heaviest view.
- [ ] dpr capped at 2 (1.5 with fullscreen fragment shaders).
- [ ] 60 fps desktop, ≥ 30 fps mid-tier mobile — or degradation ladder engaged.
- [ ] Repeated geometry uses `InstancedMesh` / `BatchedMesh`, not N meshes.
- [ ] Teardown verified: `renderer.info.memory` returns to baseline after route change.
- [ ] `webglcontextlost` handled → poster fallback renders.
- [ ] No-WebGL and `prefers-reduced-motion` paths show the static variant
      ([doc 07 pattern](./07-animation-choreography.md#specifications--parameters)).
- [ ] All post effects merged into one `EffectPass`; ≤ 2 passes total.
- [ ] Textures ≤ 2048 px and compressed per
      [doc 09](./09-tech-implementation.md#specifications--parameters).
- [ ] CWV budgets (doc 09) still green with the canvas live at p75.

## Anti-Patterns

- **A context per card.** A gallery of 12 images = 12 WebGL contexts ⇒ context-limit
  evictions and 12× overhead. One canvas, planes synced to DOM rects.
- **three.js for a 2D hover effect.** OGL does flowmaps/displacement at a fraction of
  the engine surface; shipping a 3D engine for one plane fails the lightest-tool rule.
- **Fullscreen raymarch at native dpr.** dpr 3 = 9× the fragments of dpr 1; retina
  phones melt. Half-res target + upscale, always.
- **rAF loop spinning while idle.** A static hero re-rendering 60 fps drains batteries
  and INP headroom. Use `frameloop="demand"` / dirty-flag rendering.
- **Resize without dispose.** Re-creating render targets/FBOs on every resize without
  `renderTarget.dispose()` leaks VRAM until the tab dies.
- **`setState` inside `useFrame`.** Per-frame React re-renders; mutate refs instead.
- **Pass stacking.** Bloom + CA + grain + vignette as 4 separate passes; postprocessing
  exists precisely to merge them — quoted rationale: it "minimizes the amount of render
  operations and makes it possible to combine many effects without the performance
  penalties of traditional pass chaining."
- **Effect soup.** More than one signature distortion technique per page reads as a
  demo reel, not a brand (jury weighting: doc 01 — usability is 30%).
- **WebGPU-only shipping.** No tested WebGL 2 fallback while WebGPURenderer is
  officially experimental = blank canvas for a chunk of real users.
- **No reduced-motion variant.** Persistent fluid/particle motion with no static
  fallback is an accessibility failure, not a style choice.

## Sources & Verification

- https://threejs.org/manual/en/webgpurenderer.html — confirmed: WebGPURenderer "experimental state" wording, automatic WebGL 2 fallback quote, TSL transpile-to-WGSL-or-GLSL quote, `three/webgpu` import, async `renderer.init()` / `setAnimationLoop()` requirement (verified 2026-06-12)
- https://threejs.org/manual/en/how-to-dispose-of-objects.html — confirmed: `dispose()` required for geometries/materials/textures/render targets; `renderer.info` tracks stored textures/geometries/programs (verified 2026-06-12)
- https://threejs.org/docs/pages/BatchedMesh.html — confirmed: BatchedMesh purpose quote and constructor `(maxInstanceCount, maxVertexCount, maxIndexCount, material)` (verified 2026-06-12)
- https://threejs.org/docs/pages/GPUComputationRenderer.html — confirmed: variables are RGBA float textures, two render targets per variable (ping-pong), import path `three/addons/misc/GPUComputationRenderer.js`, constructor `(sizeX, sizeY, renderer)` (verified 2026-06-12)
- https://threejs.org/docs/pages/PostProcessing.html and https://threejs.org/docs/pages/RenderPipeline.html — confirmed: `PostProcessing` renamed to `RenderPipeline` in r183; `RenderPipeline` is WebGPURenderer-only, `outputNode` + `pass(scene, camera)` usage (verified 2026-06-12)
- https://drei.docs.pmnd.rs/shaders/shader-material — confirmed: current `shaderMaterial` API, uniforms as auto setter/getter props, `key={Material.key}` HMR pattern, `extend` registration (verified 2026-06-12)
- https://r3f.docs.pmnd.rs/advanced/scaling-performance — confirmed: `frameloop="demand"` + `invalidate()`, dpr scaling, instancing "hundreds of thousands of objects in a single draw call", `regress()` quality scaling (verified 2026-06-12)
- https://r3f.docs.pmnd.rs/tutorials/basic-animations — confirmed: `useFrame` ref-mutation pattern; transient updates instead of setState (verified 2026-06-12)
- https://github.com/pmndrs/postprocessing — confirmed: EffectComposer/RenderPass/EffectPass classes; built-in Bloom, Chromatic Aberration, Noise, Vignette, Glitch, LUT, SSAO, DoF effects; pass-merging performance quote; fullscreen-triangle rendering (verified 2026-06-12)
- https://iquilezles.org/articles/distfunctions/ — confirmed: canonical SDF names (`sdSphere`, `sdBox`, `sdRoundBox`, `sdTorus`, `sdCapsule`, `sdOctahedron`, …) and `opUnion`/`opSmoothUnion` operator set, author Inigo Quilez (verified 2026-06-12)
- https://iquilezles.org/articles/raymarchingdf/ — confirmed: raymarching distance fields reference article exists at this path (verified 2026-06-12)
- https://thebookofshaders.com/11/ — confirmed: noise chapter covers value, gradient/Perlin (1985) and simplex (2001) noise; authors Patricio Gonzalez Vivo & Jen Lowe (verified 2026-06-12)
- https://tympanus.net/codrops/2018/04/10/webgl-distortion-hover-effects/ — confirmed: displacement-image hover transition technique (verified 2026-06-12)
- https://tympanus.net/codrops/2019/10/21/how-to-create-motion-hover-effects-with-image-distortions-using-three-js/ — confirmed: velocity-driven RGB-shift hover technique (R channel offset) (verified 2026-06-12)
- https://tympanus.net/codrops/2019/09/25/mouse-flowmap-deformation-with-ogl/ — confirmed: OGL flowmap technique; RG = velocity, B = velocity length (verified 2026-06-12)
- https://tympanus.net/codrops/2024/07/18/how-to-create-distortion-and-grain-effects-on-scroll-with-shaders-in-three-js/ — confirmed: scroll-velocity distortion + grain, DOM-image-to-WebGL position sync (verified 2026-06-12)
- https://tympanus.net/codrops/2024/08/27/grid-displacement-texture-with-rgb-shift-using-three-js-gpgpu-and-shaders/ — confirmed: GPGPU grid-displacement + RGB shift technique (verified 2026-06-12)
- https://tympanus.net/codrops/2023/06/28/creating-a-bulge-distortion-effect-with-webgl/ and https://tympanus.net/codrops/2022/01/12/pixel-distortion-effect-with-three-js/ — confirmed: bulge and pixel-distortion tutorials exist (verified 2026-06-12)
- https://tympanus.net/codrops/2024/12/02/how-to-code-a-shader-based-reveal-effect-with-react-three-fiber-glsl/ — confirmed: noise-threshold reveal with R3F + GLSL (verified 2026-06-12)
- https://tympanus.net/codrops/2024/12/19/crafting-a-dreamy-particle-effect-with-three-js-and-gpgpu/ — confirmed: GPGPU particle tutorial (verified 2026-06-12)
- https://tympanus.net/codrops/2025/02/26/webgpu-fluid-simulations-high-performance-real-time-rendering/ — confirmed: Navier-Stokes fluid-sim pipeline tutorial (verified 2026-06-12)
- https://tympanus.net/codrops/2025/07/30/interactive-webgl-backgrounds-a-quick-guide-to-bayer-dithering/ and https://tympanus.net/codrops/2025/06/04/building-a-real-time-dithering-shader/ — confirmed: Bayer-matrix ordered dithering technique; single-pass < 0.2 ms @ 4K / ~3 KB demo figures (verified 2026-06-12)
- https://threejs-journey.com/ — confirmed: Bruno Simon's course; lessons "Shader Patterns" (L28), "Raging Sea" (L29), "Post-processing" (L32), "GPGPU Flow Field Particles Shaders" (verified 2026-06-12)
- https://lusion.co/ and https://www.awwwards.com/websites/webgl/ — confirmed: Lusion's award record (Cannes Lions, Webby, Awwwards, FWA); Awwwards-curated WebGL collection; OFF+BRAND Site of the Year 2025 (verified 2026-06-12)
- All versions, install commands, import paths, licenses, and status quotes (three r184, fiber 9.6.1 / v10-alpha, drei 10.7.7, postprocessing 6.39.1, ogl 1.0.11, pixi.js 8.19.0, curtainsjs 8.1.6, gpu-curtains 0.16.3) — sourced exclusively from `_facts.md` (verified 2026-06-12)
