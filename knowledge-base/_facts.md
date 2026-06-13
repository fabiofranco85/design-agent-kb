# _facts.md — Verified Library Versions & Platform Facts (Single Source of Truth)

> **All verified live on 2026-06-12** against the npm registry and official sources, via a
> deep-research pass (25 claims, 3-0 adversarial votes, 0 killed) plus three targeted
> verification agents. **Writers MUST source every version, package name, install command,
> and import path from this file.** Re-verify quarterly. Anything marked
> `UNVERIFIED — confirm before use` must carry that flag wherever it is cited.

---

## 1. Animation & Scroll

### GSAP — `gsap@3.15.0`
- **Version:** 3.15.0 (published 2026-04-13). Install: `npm install gsap`
- **License:** Standard "No Charge" GSAP License — proprietary, **100% free including
  commercial use**, since v3.13 (released 2025-04-29/30, after Webflow acquired GreenSock
  Oct 2024). Official wording: *"GSAP is now 100% FREE including ALL of the bonus plugins
  like SplitText, MorphSVG, and all the others that were exclusively available to Club GSAP
  members... even for commercial use!"* No paid tier exists; Club GSAP discontinued.
- **All former Club plugins ship in the public npm package** (verified in the 3.15.0
  tarball): SplitText, MorphSVGPlugin, ScrollSmoother, DrawSVGPlugin, CustomEase — plus
  ScrollTrigger, Flip, etc.
- **Caveats:** (a) "free" ≠ OSI open source — it is a proprietary no-charge license, not
  MIT; (b) Prohibited Uses clause: may not be embedded in no-code animation-builder tools
  competing with Webflow without written consent.
- **Imports:** `import gsap from "gsap"`; plugins from subpaths, e.g.
  `import { ScrollTrigger } from "gsap/ScrollTrigger"`,
  `import { SplitText } from "gsap/SplitText"` — then `gsap.registerPlugin(ScrollTrigger, SplitText)`.
  (Plugin file presence verified in tarball; subpath syntax is the gsap.com-documented pattern.)
- Sources: https://registry.npmjs.org/gsap · https://gsap.com/blog/3-13/ ·
  https://gsap.com/community/standard-license/ · https://gsap.com/pricing/ ·
  https://webflow.com/blog/gsap-becomes-free

### Lenis — `lenis@1.3.23`
- **Version:** 1.3.23 (published 2026-04-15). **License:** MIT. Install: `npm install lenis`
- **Package name is `lenis`.** The old `@studio-freight/lenis` is deprecated/frozen at
  1.0.42 (every version carries the registry notice "has been renamed to 'lenis'").
- **Import:** `import Lenis from "lenis"` (+ `import "lenis/dist/lenis.css"` for recommended styles).
- **Official GSAP ScrollTrigger integration** (verbatim from the v1.3.23 README):
  ```js
  const lenis = new Lenis();
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => {
    lenis.raf(time * 1000); // Convert time from seconds to milliseconds
  });
  gsap.ticker.lagSmoothing(0);
  ```
  Alternative outside GSAP contexts: `new Lenis({ autoRaf: true })`.
- Sources: https://registry.npmjs.org/lenis ·
  https://github.com/darkroomengineering/lenis/blob/main/README.md

### Motion (formerly Framer Motion) — `motion@12.40.0`
- **Version:** 12.40.0 (published 2026-05-21), major line **12.x** (no v13 even as prerelease).
  **License:** MIT. Install: `npm install motion`
- **React import:** `import { motion } from "motion/react"` (exports map confirms `./react`).
  Vanilla JS: `import { animate } from "motion"`.
- **Upgrade path:** `npm uninstall framer-motion && npm install motion`, swap imports
  `"framer-motion"` → `"motion/react"`. Note: `framer-motion` is still published in lockstep
  (12.40.0, not deprecated) as a legacy mirror.
- Sources: https://registry.npmjs.org/motion · https://motion.dev/docs/react-upgrade-guide ·
  https://motion.dev/docs/react-installation

### Barba.js — `@barba/core@2.10.3` — DORMANT
- **Version:** 2.10.3 (published **2024-08-12** — ~22 months before verification). MIT.
- **Maintenance verdict: dormant.** Last commit to main 2024-08-12; last repo push
  2024-12-02; not archived, no deprecation notice. Treat as use-at-own-risk for new
  projects; prefer the View Transitions API with a GSAP fallback.
- Sources: https://registry.npmjs.org/@barba/core · https://github.com/barbajs/barba

---

## 2. WebGL / 3D

### three.js — `three@0.184.0` (= r184)
- **Version:** 0.184.0 = **r184** (published 2026-04-16). **License:** MIT.
  Install: `npm install three`
- **Imports:** `"three"`, `"three/webgpu"`, `"three/tsl"`, `"three/addons/*"` (exports map
  verified: `[".", "./addons", "./addons/*", "./examples/jsm/*", "./src/*", "./tsl", "./webgpu"]`).
- **WebGPURenderer official status** (threejs.org manual, quoted verbatim): *"The renderer
  itself is still in an experimental state although its maturity level has been greatly
  improved in the last years."*
- **WebGL2 fallback is automatic** (quoted): *"If a device/browser doesn't support WebGPU,
  the renderer can automatically fall back to using a WebGL 2 backend."* Also: *"Still,
  depending on your application and scene setup, you will encounter missing features or a
  better performance with WebGLRenderer."*
- **TSL:** documented at threejs.org/docs/pages/TSL.html; the "experimental" label appears
  only on the WebGPURenderer manual page, not in the TSL reference.
- Sources: https://registry.npmjs.org/three · https://threejs.org/manual/en/webgpurenderer.html ·
  https://threejs.org/docs/pages/TSL.html

### @react-three/fiber — `9.6.1` (v10 in alpha)
- **Version:** 9.6.1 (published 2026-04-28). MIT. Install: `npm install three @react-three/fiber`
- **React 19 required:** peerDeps `react >=19 <19.3`, `react-dom >=19 <19.3`, `three >=0.156`.
- **v10 status:** `10.0.0-alpha.2` published 2026-01-20 (alpha only — no beta/rc/stable).
  v10.0.0-alpha.1 release notes (verbatim): *"R3F now supports the WebGLRenderer and
  WebGPURenderer."* and *"WebGPU and TSL is first-class, with new built-ins just for working
  with TSL: useUniforms, useNodes, useLocalNodes and usePostProcessing."*
- Sources: https://registry.npmjs.org/@react-three/fiber ·
  https://github.com/pmndrs/react-three-fiber/releases/tag/v10.0.0-alpha.1

### @react-three/drei — `10.7.7`
- **Version:** 10.7.7 (published 2025-11-13). MIT. Install: `npm install @react-three/drei`
- peerDeps: `react ^19`, `react-dom ^19`, `three >=0.159`, `@react-three/fiber ^9.0.0`.
- v11 alpha exists (`11.0.0-alpha.5`); whether it pairs with fiber v10:
  UNVERIFIED — confirm before use.
- Source: https://registry.npmjs.org/@react-three/drei

### postprocessing (pmndrs) — `6.39.1`
- **Version:** 6.39.1 (published 2026-04-17). **License:** Zlib. Install: `npm install postprocessing`
- peerDeps: `three >= 0.168.0 < 0.185.0` (supports current r184). v7 is in beta
  (`7.0.0-beta.16`); v7/WebGPU support details: UNVERIFIED — confirm before use.
- Source: https://registry.npmjs.org/postprocessing

### OGL — `ogl@1.0.11`
- **Version:** 1.0.11 (published 2025-01-27 — slow cadence, not deprecated).
  **License:** Unlicense. Install: `npm install ogl`. Import: `"ogl"`.
- Source: https://registry.npmjs.org/ogl

### PixiJS — `pixi.js@8.19.0`
- **Version:** 8.19.0 (published 2026-06-04), major **v8**, actively maintained. MIT.
  Install: `npm install pixi.js`. Import: `"pixi.js"`.
- **Renderers (official guide, quoted):** WebGL — *"Default renderer using WebGL/WebGL2.
  Well supported and stable."* (✅ Recommended). WebGPU — *"Modern GPU renderer using
  WebGPU. More performant, still maturing."* (🚧 Experimental; *"feature complete, however,
  inconsistencies in browser implementations may lead to unexpected behavior"*).
- Sources: https://registry.npmjs.org/pixi.js · https://pixijs.com/8.x/guides/components/renderers

### curtains.js → gpu-curtains
- **curtainsjs 8.1.6** (published 2024-05-02 — no release in >2 years; repo not archived,
  **no official legacy notice**; calling it "officially legacy" is
  UNVERIFIED — confirm before use). MIT.
- **gpu-curtains 0.16.3** (published 2026-03-24, actively maintained). MIT. WebGPU-based
  library by the same author (Martin Laxenaire). "Official successor" is implied, not
  formally declared: UNVERIFIED — confirm before use.
- Sources: https://registry.npmjs.org/curtainsjs · https://registry.npmjs.org/gpu-curtains

---

## 3. Web Platform Standards

### View Transitions API — browser support (as of 2026-06-12)
| Mode | Chrome | Edge | Safari | Firefox |
|---|---|---|---|---|
| Same-document | ≥ 111 (2023-03) | ≥ 111 | ≥ 18.0 (2024-09) | **≥ 144** (2025-10-14) |
| Cross-document | ≥ 126 (2024-06) | ≥ 126 | ≥ 18.2 (2024-12) | **Not supported** (as of FF 150; impl bug open) |

- **Cross-document timeout** (Chrome docs, verbatim): *"If a navigation takes too long —
  more than four seconds in Chrome's case — then the view transition is skipped with a
  `TimeoutError` `DOMException`."*
- **Reduced motion**: official guidance — disable or soften transitions under
  `@media (prefers-reduced-motion)`, e.g.
  `::view-transition-group(*), ::view-transition-old(*), ::view-transition-new(*) { animation: none !important; }`;
  caveat (quoted): *"a preference for 'reduced motion' doesn't mean the user wants no motion."*
- **Pseudo-element tree** (MDN): `::view-transition` → `::view-transition-group()` →
  `::view-transition-image-pair()` → `::view-transition-old()` / `::view-transition-new()`.
- Sources: https://caniuse.com/view-transitions · https://caniuse.com/cross-document-view-transitions ·
  https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API ·
  https://developer.chrome.com/docs/web-platform/view-transitions/cross-document

### W3C Design Tokens (DTCG) Format Module — 2025.10 (stable)
- **2025.10 is the first stable version** — *"Final Community Group Report, 28 October
  2025"*, *"considered stable"*, *"not a W3C Standard"*. **No newer TR as of 2026-06-12.**
- **Syntax:** a token is an object with required `$value`; `$type` = *"a predefined
  categorization applied to the token's value"*; optional `$description`, `$extensions`.
  Alias syntax: `"{group.token}"`.
- **File extensions** (spec, verbatim): *"The following file extensions are recommended by
  this spec: `.tokens` and `.tokens.json`"*.
- **Media type** (spec, verbatim): *"the following MIME type SHOULD be used:
  `application/design-tokens+json`"*.
- Sources: https://www.designtokens.org/TR/2025.10/format/ ·
  https://www.designtokens.org/technical-reports/ ·
  https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/

### Core Web Vitals — current "good" thresholds (p75, mobile & desktop segmented)
- **LCP ≤ 2.5 s** · **INP ≤ 200 ms** (200–500 needs improvement, >500 poor) · **CLS ≤ 0.1**
- INP replaced FID in 2024. No new metric replaces INP; no 2025/2026 threshold changes on
  web.dev. (SEO-blog rumor of "LCP tightened to 2.0 s in March 2026": contradicted by live
  web.dev — treat as false.)
- Sources: https://web.dev/articles/vitals · https://web.dev/articles/lcp · https://web.dev/articles/inp

---

## 4. Frameworks, CMS & Asset Pipeline

| Package | Latest stable | Published | Major | Notes |
|---|---|---|---|---|
| `next` | 16.2.9 | 2026-06-09 | 16 | 15.x still maintained (15.3.9) |
| `astro` | 6.4.6 | 2026-06-10 | 6 | v7 in beta (7.0.0-beta.3) |
| `nuxt` | 4.4.8 | 2026-06-08 | 4 | 3.x maintained (3.21.8) |
| `react` | 19.2.7 | 2026-06-01 | 19 | 19.3 in canary |
| `@sanity/client` | 7.22.1 | 2026-05-28 | 7 | `sanity` studio at 6.0.0 (2026-06-11) |
| `storyblok-js-client` | 7.6.1 | 2026-06-09 | 7 | `@storyblok/js` at 5.1.10 |
| `contentful` | 11.12.4 | 2026-06-01 | 11 | |
| `@prismicio/client` | 7.21.8 | 2026-04-04 | 7 | |
| `@gltf-transform/cli` | 4.4.0 | 2026-06-06 | 4 | `@gltf-transform/core` same line; flags verified by executing the 4.4.0 binary |
| `howler` | 2.2.4 | 2023-09-19 | 2 | MIT; dormant (~33 months) but stable de-facto standard; verified live by doc-09 writer |

All sourced from https://registry.npmjs.org/<package> (dist-tags + time), verified 2026-06-12.

---

## 5. Consolidated UNVERIFIED list (carry the flag wherever cited)

1. `@react-three/drei` v11-alpha ↔ fiber v10 pairing — UNVERIFIED — confirm before use.
2. `postprocessing` v7 (beta) WebGPU support details — UNVERIFIED — confirm before use.
3. curtains.js "officially legacy" designation — UNVERIFIED (dormancy is verified; no official notice exists).
4. gpu-curtains as the formally declared "official successor" to curtains.js — UNVERIFIED (same author, implied only).
5. Exact GSAP plugin import subpath syntax — verified by tarball file presence; quoted-docs confirmation pending (standard documented pattern `gsap/SplitText` assumed).
