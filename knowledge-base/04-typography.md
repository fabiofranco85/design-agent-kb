---
title: Typography — Scales, Fluid Type, Variable Fonts & Kinetic Text
doc_id: 04-typography
version: 1.0
last_verified: 2026-06-12
applies_to_modes: [create, recreate, modify]
---

## Purpose & When To Read This

Open this doc whenever the task involves choosing or auditing typefaces, building a type
scale (static or fluid), configuring variable-font axes, specifying line-height / measure /
tracking, loading fonts performantly, or animating text (split reveals, kinetic type).
This doc owns the modular-scale table, the fluid `clamp()` recipes, and the SplitText
reveal recipe; easing curves and the global reduced-motion pattern live in
[doc 07](./07-animation-choreography.md#specifications--parameters).

## Core Principles

1. **One scale, one ratio.** Every font size on the site is a step on a single modular
   scale (ratios pinned in `_conventions.md` §3.6). Ad-hoc sizes are defects.
2. **16 px body floor, always.** Body text never renders below 16 px (1 rem) at any
   viewport width or zoom level. Fluid minimums clamp at ≥ 1 rem.
3. **Fluid by default.** Type interpolates between viewports with `clamp()` using
   rem + vw sums — never bare viewport units (they ignore browser zoom and fail
   WCAG 1.4.4 Resize Text).
4. **Hierarchy is multi-channel.** Differentiate levels with size + weight + tracking +
   case + color, not size alone. Two adjacent levels must differ in ≥ 2 channels.
5. **Maximum 2 families** (1 display + 1 text), plus an optional monospace for code.
   Award-level sites win with restraint and precision, not font variety.
6. **Performance is typography.** WOFF2 only, subset to the languages served,
   `font-display` declared on every `@font-face`, swap-induced CLS engineered to ≈ 0.
7. **Animated text must degrade.** Every split/kinetic effect ships with a
   `prefers-reduced-motion` fallback and keeps the accessibility tree intact
   (SplitText `aria: "auto"`). Canonical reduced-motion pattern:
   [doc 07](./07-animation-choreography.md#specifications--parameters).

## Decision Framework

**Ratio selection**
- IF text-heavy product UI, dashboard, docs → **Minor Third 1.2**.
- IF general marketing / brand site with mixed content → **Major Third 1.25**.
- IF editorial / portfolio with hero-driven hierarchy → **Perfect Fourth 1.333**.
- IF campaign / display-led one-pager AND fluid scaling is implemented → **Golden 1.618
  at max viewport only**, compressed to ≤ 1.333 at min viewport (see §4.1 — Golden
  produces a 110 px h1 from a 16 px base at 4 steps and breaks 320–390 px screens
  if applied statically).
- Default when unsure: 1.2–1.333 band (per `_conventions.md` §3.6).

**Static vs fluid**
- IF the design system serves responsive web (it does) → fluid `clamp()` scale (§4.2).
- IF a step's max/min ratio would exceed 2.5× → split it into two steps; 200 % zoom
  compliance is no longer guaranteed beyond 2.5× (§4.2 zoom-safety rule).

**Variable vs static fonts**
- IF the design uses ≥ 3 weights of a family, OR animates weight/width/optical size,
  OR needs optical sizing across display→caption → one variable-font file.
- IF exactly 1–2 fixed weights and no axis animation → 1–2 static WOFF2 files
  (smaller total payload).

**Text animation**
- IF hero/section headline reveal at award level → SplitText recipe (§4.7, Code Examples).
- IF simple appearance of body copy → CSS opacity/transform only; never split paragraphs.
- IF scroll-scrubbed kinetic type → pair with ScrollTrigger per
  [doc 07](./07-animation-choreography.md#specifications--parameters); keep axis
  animation off long body copy (§4.7 performance note).

## Specifications & Parameters

### 4.1 Modular scale (ratios per `_conventions.md` §3.6 — exact names/values)

Sizes from base 16 px, rounded to 0.1 px; steps = base × ratio^n.

| Ratio | Name | +1 | +2 | +3 | +4 | +5 | Character / trade-off |
|---|---|---|---|---|---|---|---|
| 1.2 | Minor Third | 19.2 | 23.0 | 27.6 | 33.2 | 39.8 | Dense, calm; ideal for UI/text-heavy. Weak hero drama — compensate with weight. |
| 1.25 | Major Third | 20.0 | 25.0 | 31.3 | 39.1 | 48.8 | Versatile marketing default; clear hierarchy without mobile overflow. |
| 1.333 | Perfect Fourth | 21.3 | 28.4 | 37.9 | 50.5 | 67.3 | Editorial drama; long headlines wrap badly < 480 px — shorten copy or go fluid. |
| 1.618 | Golden | 25.9 | 41.9 | 67.8 | 109.7 | 177.4 | Display-only. Step +4 = **109.7 px** ≈ 5 chars/line at 320 px. **Falls apart on mobile without fluid scaling** — never use statically. |

**Recommendation:** 1.2–1.333 for UI (per §3.6). Use the fluid scale below to run a
smaller ratio at the min viewport and a larger one at the max viewport.

### 4.2 Fluid type with clamp() — the canonical recipe

Formula for a step interpolating `min`px → `max`px between viewports `vwMin`=320 px and
`vwMax`=1280 px (960 px range):

```
slope     = (max − min) / (vwMax − vwMin)        // px per viewport px
vw-coef   = slope × 100                           // the Nvw term
intercept = min − slope × vwMin                   // px → ÷16 = rem
font-size: clamp(min/16 rem, intercept/16 rem + vw-coef vw, max/16 rem);
```

Canonical fluid scale — Minor Third (1.2) at 320 px → Major Third (1.25) at 1280 px,
rounded to whole px (Utopia-style dual-ratio interpolation):

| Token | 320 px | 1280 px | CSS value |
|---|---|---|---|
| `type.step.0` (body) | 16 | 18 | `clamp(1rem, 0.958rem + 0.208vw, 1.125rem)` |
| `type.step.1` | 19 | 22 | `clamp(1.188rem, 1.125rem + 0.313vw, 1.375rem)` |
| `type.step.2` | 23 | 28 | `clamp(1.438rem, 1.333rem + 0.521vw, 1.75rem)` |
| `type.step.3` | 28 | 35 | `clamp(1.75rem, 1.604rem + 0.729vw, 2.188rem)` |
| `type.step.4` | 33 | 44 | `clamp(2.063rem, 1.833rem + 1.146vw, 2.75rem)` |
| `type.step.5` | 40 | 55 | `clamp(2.5rem, 2.188rem + 1.563vw, 3.438rem)` |
| `type.step.6` (display) | 48 | 69 | `clamp(3rem, 2.563rem + 2.188vw, 4.313rem)` |

Rules:
- **Body floor:** `type.step.0` minimum is exactly 1 rem (16 px) — accessibility floor.
- **Zoom-safety rule:** keep each step's max ≤ **2.5×** its min and the text passes
  WCAG 1.4.4 (200 % resize) on modern browsers (Smashing Magazine / Barvian). The table
  above peaks at 1.44× — well inside.
- **Always rem + vw**, never vw alone: viewport units do not respond to browser zoom.
- **A "fluid Golden" hero:** min 40 px (1.333-ish from 16 base) → max 70 px (≈ 16 × 1.618²
  display step) = `clamp(2.5rem, 1.875rem + 3.125vw, 4.375rem)`; ratio 1.75× ≤ 2.5× ✓.

### 4.3 Line-height, measure, tracking (per role)

| Role | Size band | line-height (unitless) | letter-spacing | Measure / width |
|---|---|---|---|---|
| Display | ≥ 48 px | 0.95–1.1 | −0.02 to −0.03 em | ≤ 14ch |
| Headline | 28–48 px | 1.1–1.2 | −0.01 to −0.02 em | ≤ 22ch |
| Subhead | 20–28 px | 1.25–1.35 | 0 to −0.01 em | ≤ 36ch |
| Body | 16–18 px | 1.5–1.6 | 0 | 45–75 CPL, target 66 (`max-width: 65ch`) |
| Caption / small | 13–14 px | 1.4–1.5 | +0.01 em | ≤ 50ch |
| All-caps label | 11–14 px | 1.0–1.2 | +0.05 to +0.10 em | n/a |
| Button | 14–16 px | 1.0 | 0 to +0.02 em | n/a |

- Line-height is always **unitless** (multiplier), letter-spacing always in **em**
  (scales with size). 45–75 characters per line is the comfortable screen measure.
- **Tracking tokens are static per role, not fluidly recomputed.** Store each role's
  tracking once as the em amount (a DTCG `number` token, `tracking.{role}`) and apply it
  as `letter-spacing: <n>em`. Because `em` scales with the role's own `font-size`, the
  single stored value is correct at every viewport — there is no per-breakpoint px
  recompute and no build step involved. `typography.*` composites alias `{tracking.role}`;
  never store tracking as a px value derived from a step's max size.
- **WCAG 1.4.12 Text Spacing (AA):** the layout must not break when a user overrides to
  line-height 1.5×, paragraph spacing 2×, letter-spacing 0.12 em, word-spacing 0.16 em.
  Never use fixed-height text containers; test with a text-spacing bookmarklet.
- Contrast minimums (4.5:1 body / 3:1 large) are owned by
  [doc 05](./05-color.md#specifications--parameters); vertical rhythm aligns to the
  spacing scale in [doc 06](./06-spacing.md#specifications--parameters).

### 4.4 Variable fonts — axis usage

Five registered axes (lowercase tags) map to standard CSS properties (MDN):

| Axis | Tag | CSS property | Range |
|---|---|---|---|
| Weight | `wght` | `font-weight` | 1–1000 (vs 100–900 static) |
| Width | `wdth` | `font-stretch` | % , typically 75–125 % |
| Slant | `slnt` | `font-style: oblique Xdeg` | −90° to 90° |
| Italic | `ital` | `font-style: italic` | 0–1 |
| Optical size | `opsz` | `font-optical-sizing: auto \| none` | font-defined, e.g. 9–144 |

Rules (per MDN):
- **Prefer the standard property** for registered axes; use `font-variation-settings`
  only for custom axes or unexposed values.
- Tags are **case-sensitive**: registered = lowercase (`"wght"`), custom = UPPERCASE
  (`"SOFT"`, `"GRAD"`).
- `font-variation-settings` is **all-or-nothing**: changing one axis requires
  redeclaring all — route each axis through a CSS custom property (Code Examples).
- Reference fonts: **Inter** (wght 100–900, opsz 14–32 — UI workhorse);
  **Fraunces** (wght 100–900, opsz 9–144, SOFT 0–100, WONK 0–1 — expressive display;
  WONK is disabled by the font at small optical sizes ≤ 18 px).
- Directory for sourcing: v-fonts.com; specimen pages on fonts.google.com list each
  font's axes and ranges.

### 4.5 Font pairing heuristics

1. **2 families max:** expressive display + neutral text workhorse. Third family only as
   monospace for code.
2. **Contrast the classification, match the proportions:** serif display + sans text
   (or inverse). Check x-heights side-by-side at identical font-size — they should
   align within ≈ 5 %; mismatched x-heights make the smaller-x face look shrunken.
3. **Superfamilies are a guaranteed pass** (shared skeleton/metrics): e.g. Source Serif +
   Source Sans, Roboto + Roboto Slab, Merriweather + Merriweather Sans.
4. **Never pair near-identical voices:** two geometric sans, or two old-style serifs,
   read as a mistake, not a choice.
5. **Same-family hierarchy needs ≥ 200 weight delta** (e.g. 400 body / 700 headings)
   plus a size step ≥ 1 scale step.
6. **Audition at production sizes:** display face at ≥ 48 px against body at 16 px,
   on both light and dark surfaces, before committing.

### 4.6 Font loading & performance

| Decision | Spec |
|---|---|
| Format | **WOFF2 only** (Brotli; ~30 % smaller than WOFF — web.dev: "use only WOFF2 and forget about everything else") |
| Subsetting | Subset per script via `unicode-range`; a western-language subset lands ≈ 20–30 KB vs up to 300 KB full |
| Files | ≤ 4 static files or 1–2 variable files; typography-local payload target ≤ 200 KB total (global budget table: [doc 09](./09-tech-implementation.md#specifications--parameters)) |
| `font-display` | Body/UI text → `swap` (FOUT, text always visible). Perf-critical + decorative → `optional` (≤ 100 ms block, no late swap, zero CLS). Brand-critical display where fallback is unacceptable → `block`, only with preload. Never default (`auto`) silently. |
| Preload | `<link rel="preload" as="font" type="font/woff2" crossorigin>` for the 1–2 critical files only; preload **ignores `unicode-range`** so never preload more than the subset you will certainly use |
| Discovery | Inline the `@font-face` declarations in `<head>` (not the font binaries) |
| CLS | Metric-matched fallback via `size-adjust` / `ascent-override` / `descent-override` / `line-gap-override` (next/font generates these automatically); target swap-shift ≈ 0, CLS budget owned by [doc 09](./09-tech-implementation.md#specifications--parameters) |
| Tooling | `pyftsubset` (fontTools) or `subfont` for subsetting — versions not in `_facts.md`: UNVERIFIED — confirm before use |

### 4.7 Kinetic typography parameters

| Technique | Parameters | Guardrails |
|---|---|---|
| Split reveal (SplitText) | stagger: chars **0.02–0.05 s**, words/lines **0.06–0.10 s** — stagger standards owned by [doc 07](./07-animation-choreography.md#specifications--parameters); duration 0.6–0.8 s; ease `expo.out` / `power3.out` (curves: same doc 07 table) | Total = stagger × (count − 1) + duration ≤ **1.2 s** (hero class cap, §3.3). 30 chars × 0.03 + 0.8 = 1.67 s → too slow: drop to word-level or 0.02 s. |
| Masked line reveal | `mask: "lines"` + `yPercent: 110 → 0` | Use for headlines ≤ 3 lines; beyond that reveal by line groups. |
| Variable-axis hover | `wght` 400 → 700, `transition: font-weight 150–250 ms` | Interactive elements only; weight change reflows — keep the element's box width fixed or accept ≤ 2 px shift. |
| Scroll-scrubbed axis | `wght` or `wdth` scrubbed via ScrollTrigger | Display text only, ≤ 1 instance per viewport; text re-rasterizes every frame. Choreography: [doc 07](./07-animation-choreography.md#specifications--parameters). |
| Marquee / ticker | 20–40 s per loop, linear, pause on hover/focus | Duplicate strip gets `aria-hidden="true"`; stops entirely under reduced motion. |

Accessibility, non-negotiable: SplitText `aria: "auto"` (default — `aria-label` on the
target, `aria-hidden` on the pieces) so screen readers get intact text; every recipe has
the reduced-motion branch shown in Code Examples.

## Recommended Libraries & Tools

| Use case | Tool | Version / install (from `_facts.md`) |
|---|---|---|
| Split-text reveals, kinetic type | GSAP + SplitText plugin | `gsap@3.15.0` — `npm install gsap`. 100 % free incl. commercial use since v3.13 (Webflow-sponsored); SplitText rewritten in 3.13: **50 % smaller**, autoSplit, masking, onSplit, screen-reader aria handling |
| Scroll-linked text choreography | GSAP ScrollTrigger (same package) | `import { ScrollTrigger } from "gsap/ScrollTrigger"` — setup owned by [doc 07](./07-animation-choreography.md#specifications--parameters) |
| Fluid scale generation | Utopia type calculator (utopia.fyi) | Web tool — emits `--step-N` clamp() variables from min/max viewport + ratio pairs |
| Variable font sourcing | v-fonts.com directory; fonts.google.com specimen pages | Web references |
| Subsetting | `pyftsubset` (fontTools), `subfont` | Versions not in `_facts.md`: UNVERIFIED — confirm before use |

Imports (per `_facts.md`):

```js
import gsap from "gsap";
import { SplitText } from "gsap/SplitText";
gsap.registerPlugin(SplitText);
```

## Code Examples

### Fluid type tokens (drop-in)

```css
:root {
  /* 320→1280px viewport; Minor Third → Major Third; body floor 16px */
  --step-0: clamp(1rem, 0.958rem + 0.208vw, 1.125rem);     /* 16 → 18 */
  --step-1: clamp(1.188rem, 1.125rem + 0.313vw, 1.375rem); /* 19 → 22 */
  --step-2: clamp(1.438rem, 1.333rem + 0.521vw, 1.75rem);  /* 23 → 28 */
  --step-3: clamp(1.75rem, 1.604rem + 0.729vw, 2.188rem);  /* 28 → 35 */
  --step-4: clamp(2.063rem, 1.833rem + 1.146vw, 2.75rem);  /* 33 → 44 */
  --step-5: clamp(2.5rem, 2.188rem + 1.563vw, 3.438rem);   /* 40 → 55 */
  --step-6: clamp(3rem, 2.563rem + 2.188vw, 4.313rem);     /* 48 → 69 */
}
body { font-size: var(--step-0); line-height: 1.5; }
h1   { font-size: var(--step-6); line-height: 1.05; letter-spacing: -0.02em; }
p    { max-width: 65ch; } /* 45–75 CPL measure */
```

### @font-face with subsetting + zero-CLS fallback

```css
@font-face {
  font-family: "InterVariable";
  src: url("/fonts/inter-var-latin.woff2") format("woff2");
  font-weight: 100 900;        /* variable wght range */
  font-display: swap;          /* FOUT, never invisible text */
  unicode-range: U+0000-00FF;  /* Basic Latin + Latin-1; use your subsetter's full emitted range */
}
/* Metric-matched local fallback so the swap doesn't shift layout */
@font-face {
  font-family: "Inter-fallback";
  src: local("Arial");
  size-adjust: 107%;       /* EXAMPLE values — generate per font pair */
  ascent-override: 90%;    /* (next/font emits these automatically)   */
  descent-override: 22%;
  line-gap-override: 0%;
}
html { font-family: "InterVariable", "Inter-fallback", sans-serif; }
```

```html
<!-- Preload ONLY the critical subset; preload ignores unicode-range -->
<link rel="preload" href="/fonts/inter-var-latin.woff2"
      as="font" type="font/woff2" crossorigin>
```

### Variable-font axes (registered via standard props; custom via CSS vars)

```css
.headline {
  font-weight: 640;                 /* registered axis → standard property */
  font-optical-sizing: auto;        /* let opsz track font-size */
  transition: font-weight 200ms ease-out; /* 150–250ms hover band */
}
.headline:hover { font-weight: 760; }

.display-fraunces {
  /* font-variation-settings is all-or-nothing → one var per axis */
  --soft: 0; --wonk: 1;
  font-variation-settings: "SOFT" var(--soft), "WONK" var(--wonk); /* custom = UPPERCASE */
}
.display-fraunces:hover { --soft: 60; } /* changes one axis without resetting the rest */
```

### SplitText reveal recipe (gsap@3.15.0, post-3.13 API)

```js
import gsap from "gsap";
import { SplitText } from "gsap/SplitText";
gsap.registerPlugin(SplitText);

const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {
  const split = SplitText.create(".hero-title", {
    type: "lines,words", // what to split into (chars also available)
    mask: "lines",       // extra clipping wrapper per line → clean edge reveal
    autoSplit: true,     // re-split + re-run onSplit on font load / width change
    aria: "auto",        // default: aria-label on target, aria-hidden on pieces
    onSplit(self) {
      // RETURN the animation so autoSplit can kill/re-sync it on re-split
      return gsap.from(self.words, {
        yPercent: 110,   // start fully below the line mask
        duration: 0.8,   // content-reveal band 400–700ms; hero cap 1200ms (§3.3)
        ease: "expo.out",// canonical name — curve table in doc 07
        stagger: 0.06,   // words/lines 0.06–0.10s; chars 0.02–0.05s (doc 07 stagger standards)
      });
    },
  });
  return () => split.revert(); // cleanup restores original DOM + a11y tree
});

mm.add("(prefers-reduced-motion: reduce)", () => {
  // Recipe-specific fallback: no splitting, no movement — opacity only, ≤ 200 ms.
  // Global reduced-motion policy: doc 07.
  gsap.from(".hero-title", { opacity: 0, duration: 0.2, ease: "none" });
});
```

Key API facts (gsap.com docs, current): `type` default `"chars,words,lines"`; `aria`
default `"auto"` (also `"hidden"`, `"none"`); `autoSplit` default `false` — set `true`
whenever splitting lines; `mask` accepts `"lines" | "words" | "chars"`; `deepSlice`
default `true` handles nested elements spanning lines; `smartWrap` prevents awkward
char-split wraps; `reduceWhiteSpace` default `true`.

## Mode-Specific Guidance

### Create from scratch
1. Pick ratio via the Decision Framework; generate the fluid scale with the §4.2 formula
   (or Utopia) at 320/1280 px anchors; emit as `type.step.N` tokens
   (format per [doc 05](./05-color.md#specifications--parameters) /
   [doc 06](./06-spacing.md#specifications--parameters) token conventions).
2. Choose families with §4.5 heuristics; prefer one variable font when ≥ 3 weights.
3. Write the loading plan (§4.6) before any layout work — fonts are render-critical.
4. Spec line-height/tracking per role from the §4.3 table into the tokens — tracking as
   static `tracking.{role}` em `number` tokens (per the §4.3 static-tracking rule), aliased
   by the `typography.*` composites; never a build-recomputed px value.

### Re-create from existing site (reverse-engineering)
1. In DevTools, read `getComputedStyle(el).fontSize` for h1…h6/body at 320, 768, 1440 px
   widths. Divide adjacent sizes: the median quotient is the ratio — snap to the nearest
   §3.6 named value (1.2 / 1.25 / 1.333 / 1.618).
2. If sizes drift continuously while resizing → fluid type; solve §4.2's formula
   backwards from two viewport samples to recover min/max anchors.
3. Identify families from the Network panel (woff2 names) + computed `font-family`;
   detect variable fonts via `font-variation-settings` in computed styles or the
   Fonts inspector (Firefox shows axes/instances).
4. Record line-height, letter-spacing, measure per role into the §4.3 table format;
   note `font-display` from the source CSS.

### Modify an existing system
1. Never add an off-scale size; if a new level is needed, add a half-step
   (geometric mean of neighbors: √(a×b)) and document it.
2. Changing ratio or base re-flows everything — re-run the Quality Checklist plus the
   layout checks in [doc 03](./03-layout.md#quality-checklist).
3. Swapping a family: match x-height within ≈ 5 % and regenerate fallback metric
   overrides (§4.6), or accept a CLS regression.

## Quality Checklist

- [ ] Single ratio from §3.6; every rendered size is a scale step (audit computed styles).
- [ ] Body ≥ 16 px at every viewport; all clamp() minimums ≥ 1 rem.
- [ ] All sizes in rem; every clamp() preferred term is rem + vw; max/min per step ≤ 2.5×.
- [ ] Page zoom 200 %: no clipped, overlapped, or fixed-size text (WCAG 1.4.4).
- [ ] WCAG 1.4.12 override (lh 1.5 / para 2× / letter 0.12 em / word 0.16 em): no loss.
- [ ] Body measure 45–75 CPL; body line-height ≥ 1.5; display ≤ 1.1 with −0.02 em tracking.
- [ ] WOFF2 only, subset, ≤ 200 KB total, ≤ 2 families; `font-display` on every face.
- [ ] No FOIT > 100 ms; swap CLS ≈ 0 via metric-matched fallback.
- [ ] SplitText: `aria: "auto"` intact, `autoSplit: true` for line splits, animation
      returned from `onSplit`, `revert()` on cleanup, reduced-motion branch present.
- [ ] Total split-reveal time ≤ 1.2 s; staggers within doc 07 bands (chars 0.02–0.05 s,
      words/lines 0.06–0.10 s).
- [ ] Registered axes set via standard properties, not `font-variation-settings`.

## Anti-Patterns

- `font-size: 5vw` (bare viewport units) — immune to zoom, WCAG 1.4.4 failure.
- Static Golden (1.618) scale — 110 px h1 from a 16 px base wrecks 320 px screens.
- px-based font sizes / letter-spacing — ignore user font-size preference and don't scale.
- Fixed pixel line-height (`line-height: 24px`) — breaks at 1.4.12 spacing overrides;
  use unitless.
- `font-display: block` on body text, or no `font-display` at all — multi-second FOIT.
- Preloading 4+ font files "to be safe" — starves LCP-critical resources and bypasses
  `unicode-range` negotiation.
- Splitting whole paragraphs into chars — DOM bloat, screen-reader noise, sluggish reveal.
- SplitText with `aria: "none"` and no fallback — text becomes unreadable to AT.
- Char stagger ≥ 0.1 s on long headlines — 3–4 s reveals read as broken, not cinematic.
- Animating `wght` on body copy or > 1 display element per viewport — continuous
  re-rasterization jank.
- Three or more typefaces, or two same-classification faces with clashing skeletons.
- All-caps labels without +0.05 em tracking; justified text without hyphenation.

## Sources & Verification

- https://gsap.com/docs/v3/Plugins/SplitText/ — confirmed: current SplitText options and
  defaults (`type` default `"chars,words,lines"`; `aria` default `"auto"` with
  aria-label/aria-hidden behavior; `autoSplit` default `false`; `mask:
  "lines"|"words"|"chars"`; `onSplit` return-animation re-sync; `deepSlice` default
  `true`; `smartWrap`; `reduceWhiteSpace` default `true`) (verified 2026-06-12)
- https://gsap.com/blog/3-13/ — confirmed: SplitText rewritten in 3.13, 50 % smaller,
  free for everyone, 14 new features incl. screen-reader aria handling, masking,
  autoSplit/onSplit (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_fonts/Variable_fonts_guide —
  confirmed: 5 registered axes + property mappings; wght 1–1000; slnt −90°–90°;
  lowercase registered / UPPERCASE custom tags; font-variation-settings redeclare-all
  gotcha + custom-property workaround; prefer standard properties (verified 2026-06-12)
- https://web.dev/articles/font-best-practices — confirmed: "use only WOFF2"; preload
  caveats (ignores unicode-range, use sparingly); font-display scenario guidance
  (optional ≤ 100 ms block / swap / block); inline font declarations in head;
  unicode-range subsetting; size-adjust fallback matching (verified 2026-06-12)
- https://www.smashingmagazine.com/2023/11/addressing-accessibility-concerns-fluid-type/
  — confirmed: viewport units don't scale with zoom; max ≤ 2.5× min keeps clamp() fluid
  type passing WCAG 1.4.4 on modern browsers (Barvian) (verified 2026-06-12)
- https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html — confirmed: 1.4.12 AA
  override values — line-height 1.5×, paragraph 2×, letter 0.12 em, word 0.16 em, no
  loss of content/function (verified 2026-06-12)
- https://utopia.fyi/type/calculator/ — confirmed: clamp()-based fluid scale generator
  interpolating min/max viewport + ratio pairs into `--step-N` variables
  (verified 2026-06-12)
- https://fonts.google.com/specimen/Fraunces — confirmed: Fraunces variable axes
  wght, opsz 9–144, SOFT 0–100, WONK 0–1; WONK disabled at small optical sizes
  (verified 2026-06-12)
- https://fontsource.org/fonts/inter — confirmed: Inter variable axes wght 100–900,
  opsz 14–32 (verified 2026-06-12)
- https://pimpmytype.com/line-length-line-height/ — confirmed: 45–75 characters per
  line comfortable measure; heading line-height 1.1–1.4, body ~1.4–1.7 bands
  (verified 2026-06-12)
- https://pangrampangram.com/blogs/journal/how-to-pair-fonts — confirmed: pairing
  heuristics — similar x-heights pair well; serif/sans structural contrast; superfamily
  shared-skeleton pairing (verified 2026-06-12)
- https://walterebert.com/blog/subsetting-web-fonts/ — confirmed: pyftsubset
  (fontTools) / subfont tooling; western-language subsets ≈ 20–30 KB vs up to 300 KB
  full fonts (verified 2026-06-12)
