---
project: <project-name>
artifact: motion-spec
version: 1.0.0             # semver — create/recreate emit 1.0.0; modify bumps per ../10-modes-and-artifacts.md §3
date: <YYYY-MM-DD>
mode: <create | recreate | modify>
personality: <snappy | fluid | cinematic>
intensity: <ambient | responsive | showcase>
---

<!--
TEMPLATE — motion-spec.md
Section schema owner: ../10-modes-and-artifacts.md#specifications--parameters (§4 — exact
section names and order; this skeleton implements that schema, never the reverse).
The agent fills this skeleton for every project. Rules:
  • Every duration must land in one of the four canonical classes
    (../07-animation-choreography.md#specifications--parameters) AND in the personality
    slice matrix (../01-visual-motion.md#specifications--parameters).
  • Every ease is a GSAP name from the canonical table (or a registered CustomEase token
    of one) — never an ad-hoc cubic-bezier.
  • §6 maps EVERY §3/§4/§5 row to a reduced-motion variant. "—" is not a value; write
    the explicit fallback or "inherits GLOBAL".
  • Scrubbed tweens use ease "none"; only transform/opacity are ever animated.
  • Rows marked EXAMPLE are illustrations of the expected precision — replace them.
-->

# Motion Spec — <project-name>

## 1. Motion Identity

<!-- One personality, one easing vocabulary, one smooth-scroll instance per site.
     Personality + intensity MUST equal the design-system-spec.md §1 values. -->

| Setting | Value | Notes |
|---|---|---|
| Personality | `<snappy \| fluid \| cinematic>` | = design-system-spec.md §1 |
| Intensity tier | `<ambient \| responsive \| showcase>` | = design-system-spec.md §1 |
| Duration-class values (micro/ui/reveal/hero) | <ms> / <ms> / <ms> / <ms> | chosen from the personality slices, ../01-visual-motion.md#specifications--parameters |
| Stagger default | <ms/item> | bands: ../07-animation-choreography.md#specifications--parameters |
| Engines | CSS transitions: <scope> · GSAP 3.15.0: <scope> · motion 12.40.0: <scope> | versions per ../_facts.md — re-verify at project start |

## 2. Easing & Duration Tokens

<!-- 2 primary eases + max 1 accent from the canonical table
     (../07-animation-choreography.md#specifications--parameters), with GSAP names AND
     cubic-bezier() values. Token names exactly as registered in
     design-tokens.tokens.json `motion.*`. -->

| Ease token (`motion.ease.*`) | GSAP name | cubic-bezier() | Role |
|---|---|---|---|
| `motion.ease.out` | <e.g. `power3.out`> | <e.g. cubic-bezier(0.165, 0.84, 0.44, 1)> | primary entrance |
| `motion.ease.in-out` | <e.g. `power2.inOut`> | <e.g. cubic-bezier(0.645, 0.045, 0.355, 1)> | relocations / morphs |
| `motion.ease.accent` | <e.g. `back.out(1.7)` \| none> | <value \| —> | accent pops only (~10% of tweens) |

| Duration token (`motion.duration.*`) | Value (ms) | Canonical class |
|---|---|---|
| `motion.duration.micro` | <ms> | micro-interaction 100–200 ms |
| `motion.duration.ui` | <ms> | UI transition 200–400 ms |
| `motion.duration.reveal` | <ms> | content/section reveal 400–700 ms |
| `motion.duration.hero` | <ms> | hero/cinematic 600–1200 ms |

- **`gsap.defaults` ease:** `<e.g. power3.out>` — overrides GSAP's library default `power1.out`
- **Custom eases registered:** `<CustomEase name → bezier data> | none` — max one new token in modify mode

## 3. Choreography Inventory

<!-- One row per animated pattern. ID is referenced from design-system-spec.md §7 and
     mapped to a reduced-motion variant in §6. Targets: element/selector. From → To:
     numeric transform/opacity start/end states only. Ease token: from §2. Overlap: % of
     the previous tween elapsed when this one starts ("—" = sequential/none). -->

| ID | Trigger | Targets | From → To | Duration (ms) | Ease token | Stagger (ms/item) | Overlap (% of previous tween) |
|---|---|---|---|---|---|---|---|
| M-01 | <EXAMPLE: scroll into view, `start: "top 80%"`, once> | <`.hero [data-reveal]`> | <`y: 40px → 0`, `opacity: 0 → 1`> | <600> | <`motion.ease.out`> | <70> | <—> |
| M-02 | <EXAMPLE: pointerdown / release> | <`.button`> | <`scale: 1 → 0.96` / `0.96 → 1`> | <120 / 200> | <`motion.ease.out`> / <`motion.ease.accent`> | — | — |
| M-03 | <load \| scroll \| hover \| click \| route> | <selector> | <from → to> | <ms> | <`motion.ease.*`> | <ms/item \| —> | <% \| —> |
| M-04 | <trigger> | <targets> | <from → to> | <ms> | <ease token> | <ms/item \| —> | <% \| —> |

<!-- Add rows until every animated element on every page template has an ID. -->

## 4. Scroll Behavior

<!-- Native vs Lenis is a per-site decision; ONE Lenis instance max, destroyed on SPA
     teardown, never initialized under `reduce` (one-instance rule:
     ../07-animation-choreography.md#mode-specific-guidance). Scenes only for pin/scrub
     storytelling (responsive/showcase tiers); budget 600–1200 px of scroll per scene;
     tween eases inside scrub are always "none". -->

- **Smooth scroll:** <Lenis, lerp <0.05–0.18> | native> — canonical recipe: ../07-animation-choreography.md#code-examples
- **Lenis options (if used):** <full options object — lerp, wheelMultiplier, touch behavior, …>

| Scene ID | Trigger element | start / end | pin | scrub | snap | Labels / beats |
|---|---|---|---|---|---|---|
| S-01 | <`.story`> | <`"top top"` / `"+=2400"`> | <true> | <1> | <`labels` \| none> | <scene1 → scene2 → scene3> |
| S-02 | <…> | <…> | <…> | <…> | <…> | <…> |

## 5. Page Transitions

<!-- View Transitions API first, GSAP fallback — decision + support matrix:
     ../07-animation-choreography.md#decision-framework. Total budget ≤ 700 ms.
     Firefox has no cross-document support — design must read as intentional without it. -->

| Route change | Mechanism | Spec |
|---|---|---|
| <all routes> | <same-doc `startViewTransition` \| cross-doc `@view-transition` \| GSAP wipe> | <old out <ms> `<ease>`; new in <ms> `<ease>`; shared element: <name, ms, ease> \| none> |

## 6. Reduced-Motion Variants

<!-- MANDATORY: one mapping per §3 / §4 / §5 row. The canonical collapse pattern
     (gsap.matchMedia + View-Transition pseudo-element kill) is owned by
     ../07-animation-choreography.md#code-examples — apply it verbatim, then map each
     row below. -->

GLOBAL policy — under `prefers-reduced-motion: reduce`, site-wide and non-negotiable:

- No smooth scrolling (Lenis never initialized), no parallax, no pin+scrub scenes
  (content must read fully without them), no magnetic/cursor effects, no marquees,
  glitch loops, or ambient drift.
- Movement collapses to **opacity-only fades ≤ 200 ms, `ease: "none"`**; all state-change
  feedback is kept ("reduced" ≠ "none").
- View Transitions killed via the pseudo-element `animation: none` block.
- Project-specific additions: <e.g. autoplaying hero video swaps to poster frame | none>

| Row (ID from §3/§4/§5) | Reduced-motion variant |
|---|---|
| M-01 | <EXAMPLE: opacity 0 → 1, 200 ms, `none`, no stagger> |
| M-02 | <EXAMPLE: inherits GLOBAL — keep instant state feedback, no spring> |
| S-01 | <EXAMPLE: static stacked sections, all content visible, no pin> |
| <route change> | <instant swap (pseudo-element kill above)> |
| <every remaining ID> | <explicit fallback \| inherits GLOBAL> |

## 7. Performance Notes

<!-- transform/opacity-only = zero CLS from motion; input feedback ≤ 200 ms = INP guard
     (_conventions.md §3.8). Confirm every line before sign-off (pass/fail). -->

- [ ] Only `transform`/`opacity` animated anywhere (zero layout/paint properties; zero CLS from motion).
- [ ] Input feedback ≤ 200 ms on every pointer/keyboard interaction; INP < 200 ms with animations running.
- [ ] Every §3 duration sits inside its canonical class AND personality slice; nothing UI-blocking > 400 ms; > 1200 ms items skippable or scrub-driven.
- [ ] Every ease resolves to a §2 token (canonical table or registered CustomEase); scrubbed tweens use `ease: "none"`.
- [ ] One smooth-scroll instance max; destroyed on SPA teardown.
- [ ] Pointer effects gated behind `(pointer: fine)` + motion-OK.
- [ ] §6 mapping covers 100% of §3/§4/§5 rows; `reduce` path tested in-browser.
