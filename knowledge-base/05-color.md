---
title: Color — OKLCH Palettes, Design Tokens, Contrast & Theming
doc_id: 05-color
version: 1.0
last_verified: 2026-06-12
applies_to_modes: [create, recreate, modify]
---

## Purpose & When To Read This

Open this doc whenever you define, extract, or change any color in a design system: building
a palette from a brief, reverse-engineering colors from a live site, adding a dark theme, or
emitting the token file. It owns the canonical color-token architecture (primitive →
semantic → component), the DTCG color format, the full WCAG contrast spec and verification
method, and P3/sRGB gamut policy. Dimension/spacing tokens are owned by
[06-spacing](./06-spacing.md#specifications--parameters); type sizes that determine the
"large text" contrast threshold are owned by
[04-typography](./04-typography.md#specifications--parameters).

## Core Principles

1. **OKLCH is the working color space.** All palette design, ramps, and reasoning happen in
   OKLCH (CSS Color 4). Its `L` is perceptually uniform: a 0.1 lightness change reads the
   same at every hue, which HSL cannot guarantee. Hex values exist only as computed sRGB
   fallbacks, never as the source of truth.
2. **Three tiers, aliases only.** Raw color values live exclusively in primitive tokens.
   Semantic tokens alias primitives; component tokens alias semantics. A raw value in a
   semantic or component token is a defect.
3. **Themes swap semantics, never primitives.** Light/dark (and any brand theme) re-target
   the semantic tier only. Token names are identical across themes.
4. **Contrast is computed, not eyeballed.** Every text/background and UI pair ships with a
   computed WCAG 2.x ratio: ≥ 4.5:1 body text, ≥ 3:1 large text and UI components
   (anchors pinned in `_conventions.md` §3.9; full spec below). Thresholds are hard —
   4.49:1 fails.
5. **P3 is an enhancement, never a dependency.** Every wide-gamut color has an sRGB-safe
   base declaration. Award-level vibrancy comes from controlled chroma on capable displays,
   not from colors that fall apart on sRGB screens.
6. **Restraint reads as craft.** 1 brand hue + 1 neutral ramp + ≤ 2 accent hues covers
   almost every award-winning site. Mood and archetype selection feed in from
   [01-visual-motion](./01-visual-motion.md#core-principles).

## Decision Framework

- **IF mode = create with no given brand color** → pick brand hue H (0–360) from the
  archetype; build the 11-step ramp on the L anchors in §Specifications; set step-500
  chroma to ≤ 0.9 × the sRGB gamut maximum at that L/H; derive neutrals at the same hue
  with C 0.003–0.015; map semantics per the table; run the contrast gate.
- **IF a brand color is given as hex/RGB** → convert to OKLCH (oklch.com); snap its L to
  the nearest ramp anchor (it becomes that step); rebuild the remaining steps around it at
  constant H.
- **IF mode = recreate** → sample computed styles from the live site, convert every color
  to OKLCH, cluster by hue (±8°) into ramps, then re-normalize L to the ramp anchors and
  document deviations. Never copy hex values into semantic tokens directly.
- **IF mode = modify (e.g. "add dark mode")** → do not touch primitives. Add/re-target the
  dark semantic alias set, then re-run the full contrast gate for the new theme.
- **IF a pair fails 4.5:1** → first move the text token's L (±0.05 steps along the ramp),
  then reduce background C; change hue only as a last resort.
- **IF an accent must "pop" on modern screens** → use the P3 override pattern (§P3 Gamut):
  sRGB-safe base + `@media (color-gamut: p3)` chroma boost at identical L.
- **IF the user requests pure black (#000) backgrounds** → counter-propose `neutral.950`
  (L 0.15); reserve `oklch(0 0 0)` for OLED-targeted "true black" mode only, as an explicit
  additional theme.

## Specifications & Parameters

### OKLCH component spec (CSS Color 4)

Syntax: `oklch(L C H / A)` — Baseline Widely available since May 2023 (MDN).

| Component | Range | Notes |
|---|---|---|
| `L` lightness | `0`–`1` (or `0%`–`100%`) | Perceptual; 0 = black, 1 = white |
| `C` chroma | `0`–theoretical < `0.5` | `100%` = `0.4`; real displayable colors stay below ≈ `0.37` |
| `H` hue | `0`–`360` deg | Angle; sRGB blue primary ≈ 264, red ≈ 29, green ≈ 142 |
| `A` alpha | `0`–`1` after `/` | Optional, default 1 |

Out-of-gamut `oklch()` values are gamut-mapped by the browser to the closest displayable
color — convenient, but **never rely on it for brand colors**: author in-gamut values
(§P3 Gamut).

### Token architecture (canonical — `templates/design-tokens.tokens.json` follows this)

Format: W3C DTCG Format Module **2025.10** (first stable version, "Final Community Group
Report, 28 October 2025"; not a W3C Standard). File extensions `.tokens` / `.tokens.json`;
media type `application/design-tokens+json`. A token is an object with required `$value`,
plus `$type`, optional `$description` / `$extensions`. Alias syntax: `"{group.token}"`.
(All per `_facts.md` §3.)

| Tier | Holds | Examples | May alias |
|---|---|---|---|
| primitive | raw `$value` objects only | `color.blue.500`, `color.neutral.900` | nothing |
| semantic | role-named aliases | `color.bg.primary`, `color.text.on-brand` | primitives only |
| component | part-named aliases | `button.bg`, `card.border` | semantics only |

Naming rules (pinned in `_conventions.md` §3.7): dot-separated paths; multiword segments
kebab-case (`color.bg.on-brand`); ramp steps are numeric strings `50`–`950` plus `0` for
pure white. Set `$type: "color"` explicitly on every color token (no reliance on group
inheritance — keeps each token self-describing).

**Token → CSS custom property transform (binding for all sibling docs):** prefix `--`,
replace every `.` with `-`, segments stay lowercase/kebab-case.
`color.bg.primary` → `--color-bg-primary` · `color.blue.500` → `--color-blue-500` ·
`color.bg.on-brand` → `--color-bg-on-brand` · `button.bg` → `--button-bg`.
The transform is collision-free because token segments never contain `-`-adjacent dots;
it is reversible only via the token file — treat the `.tokens.json` as source of truth.

DTCG color `$value` is an **object** (2025.10 color module): `colorSpace` (required;
includes `"oklch"`, `"srgb"`, `"display-p3"` among 14 spaces), `components` (required;
for oklch: `[L, C, H]` with L 0–1, C ≥ 0, H 0–360), optional `alpha` (0–1, default 1) and
`hex` (6-digit sRGB **fallback** string). Author primitives in `"oklch"` and always emit
the computed `hex` fallback.

### Sample palette (brand hue H = 250, neutral hue H = 250)

L anchors per step (brand ramp): 50→0.97, 100→0.94, 200→0.89, 300→0.81, 400→0.70,
500→0.58, 600→0.50, 700→0.43, 800→0.36, 900→0.29, 950→0.22.
Chroma policy: neutrals 0.003–0.015 (hue-tinted toward brand for cohesion); UI tints
≤ 0.06; brand/interactive 0.09–0.155; vivid accents up to P3 gamut max with sRGB base.
All values below verified in-gamut for sRGB **and** Display P3 (computed 2026-06-12 with
the OKLab reference matrices; spot-check any edit at oklch.com).

| Step | `color.blue.*` (oklch L C H) | hex fallback | `color.neutral.*` (oklch L C H) | hex fallback |
|---|---|---|---|---|
| 0 | — | — | `1 0 0` | `#ffffff` |
| 50 | `0.97 0.013 250` | `#eff6fe` | `0.985 0.003 250` | `#f9fafc` |
| 100 | `0.94 0.028 250` | `#deedfe` | `0.96 0.004 250` | `#f0f2f4` |
| 200 | `0.89 0.05 250` | `#c3defb` | `0.92 0.006 250` | `#e2e5e8` |
| 300 | `0.81 0.095 250` | `#92c6fc` | `0.86 0.008 250` | `#cdd1d6` |
| 400 | `0.70 0.13 250` | `#5aa3ec` | `0.72 0.012 250` | `#9fa5ac` |
| 500 | `0.58 0.15 250` | `#1f7dcf` | `0.62 0.014 250` | `#80878e` |
| 600 | `0.50 0.135 250` | `#0f66ac` | `0.50 0.014 250` | `#5d646b` |
| 700 | `0.43 0.115 250` | `#0c528c` | `0.42 0.012 250` | `#484e54` |
| 800 | `0.36 0.095 250` | `#083f6c` | `0.31 0.010 250` | `#2d3135` |
| 900 | `0.29 0.075 250` | `#062d4f` | `0.23 0.008 250` | `#1a1d21` |
| 950 | `0.22 0.055 250` | `#031c33` | `0.15 0.006 250` | `#090b0e` |

Secondary hues: reuse the same L anchors, rotate H, then re-check gamut per hue — max
displayable chroma varies strongly by hue (see headroom table in §P3 Gamut). Keep hue
constant within a ramp (drift ≤ ±4° per step only as a deliberate, documented choice).

### Semantic token map (light ↔ dark swap)

| Semantic token | Light alias | Dark alias | Role |
|---|---|---|---|
| `color.bg.primary` | `{color.neutral.0}` | `{color.neutral.950}` | Page background |
| `color.bg.secondary` | `{color.neutral.50}` | `{color.neutral.900}` | Sections, wells |
| `color.bg.elevated` | `{color.neutral.0}` | `{color.neutral.900}` | Cards, popovers |
| `color.bg.brand` | `{color.blue.600}` | `{color.blue.400}` | Primary CTA fill |
| `color.bg.brand-hover` | `{color.blue.700}` | `{color.blue.300}` | CTA hover |
| `color.text.primary` | `{color.neutral.900}` | `{color.neutral.50}` | Body text |
| `color.text.secondary` | `{color.neutral.600}` | `{color.neutral.400}` | Muted text |
| `color.text.on-brand` | `{color.neutral.0}` | `{color.neutral.950}` | Text on CTA |
| `color.text.link` | `{color.blue.600}` | `{color.blue.400}` | Links |
| `color.border.default` | `{color.neutral.200}` | `{color.neutral.800}` | Decorative dividers (contrast-exempt) |
| `color.border.strong` | `{color.neutral.500}` | `{color.neutral.500}` | Input/control boundaries (≥ 3:1) |
| `color.border.focus` | `{color.blue.500}` | `{color.blue.400}` | Focus ring (≥ 3:1) |

Component tier (theme-invariant — inherits swaps through semantics):
`button.bg` → `{color.bg.brand}` · `button.bg-hover` → `{color.bg.brand-hover}` ·
`button.text` → `{color.text.on-brand}` · `button.border-focus` → `{color.border.focus}` ·
`card.bg` → `{color.bg.elevated}` · `card.border` → `{color.border.default}`.

### Contrast spec & verification method (this doc owns the full spec)

Targets — WCAG 2.2 AA (WCAG 3 is an incomplete draft; WCAG 2 remains the compliance
standard and "will not be deprecated for at least several years"):

| Content | Minimum ratio | Source SC |
|---|---|---|
| Body text (< 24 px, or < 18.66 px bold) | **4.5:1** | 1.4.3 |
| Large text: ≥ 18 pt = 24 px, or ≥ 14 pt bold = 18.66 px (WAI rounds to ≈ 18.5 px) | **3:1** | 1.4.3 |
| UI components, states, focus indicators, meaningful graphics | **3:1** vs adjacent colors | 1.4.11 |
| Exempt | inactive/disabled controls, logotypes, purely decorative, unmodified user-agent default styles | 1.4.3 / 1.4.11 |

Verification method (binding):
1. **Compute on rendered sRGB values** — the `hex` fallback of each token. WCAG 2.x
   relative luminance is defined for sRGB only; OKLCH `L` is *not* WCAG luminance and must
   never be substituted for it.
2. Formula: linearize each channel (`c ≤ 0.04045 ? c/12.92 : ((c+0.055)/1.055)^2.4`), then
   `Lum = 0.2126R + 0.7152G + 0.0722B`, then `ratio = (Lum_lighter + 0.05) / (Lum_darker + 0.05)`.
3. **No rounding up.** Per the WAI Understanding doc for 1.4.11, ratios are thresholds:
   2.999:1 fails 3:1. Apply the same discipline to 4.5:1.
4. P3 policy: a P3 override may only change `C` (never `L`) relative to its sRGB base, so
   the verified ratio of the base remains representative.
5. Record every verified pair + ratio in the design-system artifact (see
   [10-modes-and-artifacts](./10-modes-and-artifacts.md#purpose--when-to-read-this)).
6. Tools: the JS snippet in §Code Examples (canonical), WebAIM Contrast Checker, or the
   browser DevTools color picker. Results must agree to 2 decimals.

Verified ratios for the sample palette (computed 2026-06-12 via the formula above):

| Pair (semantic) | Light | Dark | Target | Status |
|---|---|---|---|---|
| `text.primary` on `bg.primary` | 16.91:1 | 18.87:1 | 4.5:1 | pass |
| `text.secondary` on `bg.primary` | 6.00:1 | 7.93:1 | 4.5:1 | pass |
| `text.secondary` on `bg.secondary` | 5.74:1 | 6.81:1 | 4.5:1 | pass |
| `text.on-brand` on `bg.brand` | 5.97:1 | 7.40:1 | 4.5:1 | pass |
| `text.on-brand` on `bg.brand-hover` | 8.07:1 | 10.98:1 | 4.5:1 | pass |
| `text.link` on `bg.primary` | 5.97:1 | 7.40:1 | 4.5:1 | pass |
| `border.focus` on `bg.primary` | 4.29:1 | 7.40:1 | 3:1 | pass |
| `border.strong` on `bg.primary` | 3.64:1 | 5.42:1 | 3:1 | pass |

Note the dark-mode CTA: white on `blue.500` is only 4.29:1, which is why dark
`bg.brand` swaps to `blue.400` with `neutral.950` text (7.40:1) — a textbook example of
why themes swap semantics instead of recoloring primitives.

### P3 wide gamut + sRGB fallback

- Detection: `@media (color-gamut: p3)` (values `srgb` | `p3` | `rec2020`; Baseline since
  February 2023). Explicit P3 literals: `color(display-p3 r g b / a)` with channels 0–1
  (Baseline since May 2023) — but prefer authoring the override in `oklch()` so `L` stays
  comparable to the base.
- Measured chroma headroom (max in-gamut C, computed 2026-06-12; varies by L and H):

| Hue (at L) | sRGB max C | P3 max C | Headroom |
|---|---|---|---|
| Blue H 250 (L 0.65) | 0.184 | 0.210 | +14% |
| Red H 25 (L 0.65) | 0.236 | 0.297 | +26% |
| Green H 145 (L 0.80) | 0.252 | 0.341 | +35% |
| Magenta H 330 (L 0.70) | 0.314 | 0.350 | +11% |

- Policy: primitives `50`–`950` must be sRGB-in-gamut (they are the brand). Optional
  `color.{hue}.vivid` accent primitives may exceed sRGB into P3; they MUST declare the
  in-spec `hex` sRGB fallback and be delivered via the override pattern in §Code Examples.
  Greens and reds gain the most from P3; blues gain least — set expectations accordingly.

### Theming strategy

Canonical mechanism: semantic CSS custom properties swapped by `[data-theme]`, with
`prefers-color-scheme` as the default when the user has not chosen. Always set
`color-scheme: light dark` on `:root` so form controls, scrollbars, and system UI follow.
Alternative for simple sites: `light-dark(<light>, <dark>)` (requires `color-scheme`;
Baseline Newly available May 2024 — acceptable when the support matrix in
[09-tech-implementation](./09-tech-implementation.md#specifications--parameters) allows).
Token storage: the main `design-tokens.tokens.json` holds primitives + light semantic
aliases + component aliases; `design-tokens.dark.tokens.json` re-targets **only** the
semantic tier (identical token names, different alias targets). IF the system defines
both light and dark themes, `design-tokens.dark.tokens.json` is a **REQUIRED** companion
artifact; IF it is single-theme, the dark file is **omitted**
([doc 10 §1](./10-modes-and-artifacts.md#specifications--parameters)).

## Recommended Libraries & Tools

No npm dependency is required for color: `oklch()`, `color()`, `color-gamut`, and
`light-dark()` are native CSS (support status above; versions/spec status per `_facts.md`).

| Use case | Tool |
|---|---|
| Pick/convert colors, see sRGB & P3 gamut limits, get chroma-clipped fallbacks | oklch.com (Evil Martians; shows both gamut boundaries and "closest fallback by chroma") |
| Spot-check a contrast pair | WebAIM Contrast Checker (webaim.org/resources/contrastchecker/) |
| In-browser pair checking | Chrome/Firefox DevTools color picker (shows WCAG ratio against rendered background) |
| Batch-verify the token file | JS snippet in §Code Examples (canonical gate) |
| Token build (tokens → CSS vars) | Style Dictionary — version/package UNVERIFIED — confirm before use; the §Code Examples CSS shows the required output shape regardless of tool |

## Code Examples

DTCG 2025.10 token file excerpt (all three tiers; goes in `design-tokens.tokens.json`):

```json
{
  "color": {
    "blue": {
      "500": {
        "$type": "color",
        "$value": {
          "colorSpace": "oklch",
          "components": [0.58, 0.15, 250],
          "alpha": 1,
          "hex": "#1f7dcf"
        },
        "$description": "Brand anchor. sRGB-safe: max C at L 0.58 / H 250 is 0.164."
      },
      "vivid": {
        "$type": "color",
        "$value": {
          "colorSpace": "oklch",
          "components": [0.65, 0.2, 250],
          "alpha": 1,
          "hex": "#0f92f7"
        },
        "$description": "P3-only accent (sRGB max C here is 0.184); hex is the sRGB-safe fallback at C 0.18."
      }
    },
    "bg": {
      "brand": { "$type": "color", "$value": "{color.blue.600}" }
    },
    "text": {
      "on-brand": { "$type": "color", "$value": "{color.neutral.0}" }
    }
  },
  "button": {
    "bg": { "$type": "color", "$value": "{color.bg.brand}" },
    "text": { "$type": "color", "$value": "{color.text.on-brand}" }
  }
}
```

Dark override file (`design-tokens.dark.tokens.json` — semantic tier only, same names):

```json
{
  "color": {
    "bg": {
      "brand": { "$type": "color", "$value": "{color.blue.400}" }
    },
    "text": {
      "on-brand": { "$type": "color", "$value": "{color.neutral.950}" }
    }
  }
}
```

CSS build output (token → custom property: prefix `--`, dots → hyphens):

```css
:root {
  color-scheme: light dark; /* required for light-dark() and native form controls */
  /* primitive tier — theme-invariant */
  --color-blue-400: oklch(0.7 0.13 250);      /* #5aa3ec */
  --color-blue-600: oklch(0.5 0.135 250);     /* #0f66ac */
  --color-neutral-0: oklch(1 0 0);            /* #ffffff */
  --color-neutral-950: oklch(0.15 0.006 250); /* #090b0e */
  /* semantic tier — light defaults */
  --color-bg-brand: var(--color-blue-600);    /* white text: 5.97:1 */
  --color-text-on-brand: var(--color-neutral-0);
}
[data-theme="dark"] {
  --color-bg-brand: var(--color-blue-400);    /* n950 text: 7.40:1 */
  --color-text-on-brand: var(--color-neutral-950);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {           /* system default when user hasn't chosen */
    --color-bg-brand: var(--color-blue-400);
    --color-text-on-brand: var(--color-neutral-950);
  }
}
/* component tier */
.button {
  background: var(--button-bg, var(--color-bg-brand));
  color: var(--button-text, var(--color-text-on-brand));
}
.button:focus-visible {
  outline: 2px solid var(--color-border-focus); /* 4.29:1 light / 7.40:1 dark vs bg */
  outline-offset: 2px;
}
```

P3 progressive enhancement (sRGB-safe base, chroma-only boost — `L` never changes):

```css
:root {
  --color-accent-vivid: oklch(0.65 0.18 250); /* in sRGB gamut → #0f92f7 */
}
@media (color-gamut: p3) {
  :root {
    --color-accent-vivid: oklch(0.65 0.2 250); /* +11% chroma, P3-only; same L */
  }
}
```

Contrast gate (canonical verification; run against every pair in the semantic map):

```js
// WCAG 2.x contrast — input: the sRGB hex fallbacks from the token file.
const lum = (hex) => {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map((c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4)); // linearize
  return 0.2126 * r + 0.7152 * g + 0.0722 * b; // relative luminance
};
const ratio = (a, b) => {
  const [hi, lo] = [lum(a), lum(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
};
// ratio('#1a1d21', '#ffffff') → 16.91  (text.primary on bg.primary, light)
// Gate: text pairs >= 4.5, large-text/UI pairs >= 3 — no rounding up.
```

## Mode-Specific Guidance

### Create from scratch
Derive brand hue from the brief/archetype → build both ramps on the L anchors → write
primitives (`colorSpace: "oklch"` + computed `hex`) → map semantics for light AND dark in
the same pass (retrofitting dark later forces re-verification anyway) → run the contrast
gate → emit `design-tokens.tokens.json` + dark override + CSS variables.

### Re-create from existing site (reverse-engineering)
Harvest `getComputedStyle` colors from representative pages; convert all to OKLCH; cluster
by hue (±8°) and dedupe by ΔL < 0.02 within a cluster; fit clusters to the ramp anchors and
record any anchor deviations in `$description`. Then verify contrast of the *reconstructed*
pairs — the source site may itself fail WCAG; flag (do not silently copy) every failing
pair, and propose the nearest passing L adjustment.

### Modify an existing system
Read the existing token file first; respect its hue and chroma envelope. New tokens must
alias existing primitives where possible; add primitives only when no step is within
ΔL 0.04 / ΔC 0.02 / ΔH 4°. Any change to a primitive requires re-running the contrast gate
for every semantic pair that transitively aliases it (both themes).

## Quality Checklist

- [ ] All primitives authored in OKLCH with `colorSpace`, `components`, `alpha`, `hex`.
- [ ] Every `50`–`950` primitive in sRGB gamut; only `*.vivid` tokens exceed it (with fallback).
- [ ] Semantic tokens are 100% aliases; component tokens alias semantics only.
- [ ] All text pairs ≥ 4.5:1 (≥ 3:1 only where 04-typography classifies the text as large).
- [ ] All UI/focus/border-strong pairs ≥ 3:1 — verified separately in light AND dark.
- [ ] Ratios computed on hex fallbacks via the canonical formula; recorded in the artifact.
- [ ] `color-scheme: light dark` set on `:root`; theme swap touches semantic vars only.
- [ ] Every `@media (color-gamut: p3)` override has an sRGB-safe base at identical `L`.
- [ ] CSS variables follow the `--` + dots→hyphens transform exactly.
- [ ] Token file parses as valid JSON and uses `.tokens.json` extension.

## Anti-Patterns

- **HSL-generated ramps.** HSL lightness is not perceptual — the same `L%` is a different
  real lightness per hue, so ramps drift and contrast becomes unpredictable.
- **Checking contrast with OKLCH `L` arithmetic.** OKLCH L ≠ WCAG luminance; only the
  computed ratio counts. (OKLCH L is a design heuristic, the formula is the law.)
- **Hex as source of truth.** Hex cannot encode P3; storing only hex forfeits wide gamut
  and breaks round-tripping. Hex is the fallback field, nothing more.
- **Theming by editing primitives** (or worse, a parallel `color.blue-dark.*` ramp) —
  doubles maintenance and guarantees drift. Swap semantic aliases.
- **Raw values inside components** (`button.bg: "#1f7dcf"`) — orphans the component from
  theme swaps; a top award-jury tell of an unsystematic build.
- **Pure `#000` page backgrounds with pure `#fff` body text** (16+:1 halation glare on
  OLED); use `neutral.950`/`neutral.50` (18.87:1 — still far above target, without glare).
- **Rounding ratios up** — 2.999:1 fails 3:1 per WAI; 4.49:1 fails 4.5:1.
- **Unbounded chroma everywhere.** C > 0.15 on large surfaces fatigues; reserve max-chroma
  for accents ≤ 10% of viewport area.
- **Relying on browser gamut-mapping** for brand colors — the mapped result differs across
  engines' clip strategies; author in-gamut values explicitly.
- **`@media (color-gamut: p3)` without an sRGB base** — most external monitors are still
  sRGB; the unenhanced experience is the default experience.

## Sources & Verification

- https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch — confirmed: `oklch(L C H / A)` syntax; L 0–1/0–100%; C min 0, 100% = 0.4, practical < 0.5; H 0–360; Baseline Widely available since May 2023 (verified 2026-06-12)
- https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl — confirmed: OKLCH perceptual-lightness advantage over HSL; palette generation via fixed L/C with rotated H; real-color chroma stays below ≈ 0.37; browsers gamut-map out-of-gamut values to closest supported color (verified 2026-06-12)
- https://www.designtokens.org/TR/2025.10/color/ — confirmed: color `$value` object = `colorSpace` (req.), `components` (req.), `alpha` (opt., default 1), `hex` (opt. sRGB fallback string); 14 color spaces incl. `oklch` (L 0–1, C 0–∞, H 0–360), `srgb`, `display-p3`; `"none"` component keyword (verified 2026-06-12)
- https://www.designtokens.org/TR/2025.10/format/ — confirmed (via `_facts.md` §3, verified there 2026-06-12): 2025.10 first stable version, Final Community Group Report 28 Oct 2025, not a W3C Standard; `$value` required, `$type`, alias `"{group.token}"`; extensions `.tokens`/`.tokens.json`; media type `application/design-tokens+json`
- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — confirmed: 4.5:1 normal / 3:1 large text; large = ≥ 18 pt or ≥ 14 pt bold (≈ 24 px / 18.5 px); exemptions (incidental, logotypes, inactive); ratio = (L1+0.05)/(L2+0.05) with sRGB relative luminance 0.2126R+0.7152G+0.0722B (verified 2026-06-12)
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — confirmed: 3:1 for UI components, states, focus indicators, meaningful graphics; exemptions (inactive, unmodified user-agent styles, essential); thresholds not rounded — 2.999:1 fails (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/color-gamut — confirmed: values `srgb`/`p3`/`rec2020`, hierarchy srgb ⊂ p3 ⊂ rec2020; Baseline Widely available since February 2023 (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color — confirmed: `color(display-p3 r g b / a)` syntax, channels 0–1, out-of-gamut permitted; Baseline Widely available since May 2023 (verified 2026-06-12)
- https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark — confirmed: `light-dark(light, dark)` requires `color-scheme: light dark` on `:root`; Baseline Newly available May 2024 (verified 2026-06-12)
- https://oklch.com — confirmed: OKLCH picker/converter by Evil Martians (Sitnik/Shamin); displays sRGB and Display P3 gamut boundaries; provides closest-by-chroma sRGB fallback (verified 2026-06-12)
- https://www.w3.org/WAI/standards-guidelines/wcag/wcag3-intro/ — confirmed: WCAG 3 is an incomplete draft; WCAG 2 will not be deprecated for at least several years after WCAG 3 is finalized — WCAG 2.x AA remains the compliance target (verified 2026-06-12)
- Palette hex fallbacks, gamut checks, P3 headroom table, and all contrast ratios — computed 2026-06-12 from the OKLab reference conversion matrices (Björn Ottosson) + the WCAG 2.x formula above; reproducible via the §Code Examples gate; spot-check conversions at oklch.com
