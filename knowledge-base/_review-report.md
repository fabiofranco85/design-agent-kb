# Knowledge-Base Review Report

- **Review date:** 2026-06-12
- **Reviewer:** consistency reviewer (automated structural checks + full manual read)
- **Files reviewed (16):** `_facts.md`, `_conventions.md`, `01-visual-motion.md`, `02-image-generation.md`, `03-layout.md`, `04-typography.md`, `05-color.md`, `06-spacing.md`, `07-animation-choreography.md`, `08-webgl-effects.md`, `09-tech-implementation.md`, `10-modes-and-artifacts.md`, `templates/design-system-spec.md`, `templates/design-tokens.tokens.json`, `templates/motion-spec.md`, `templates/implementation-plan.md`. (`00-agent.md` and `README.md` intentionally not yet written — not findings.)
- **Totals:** 1 BLOCKER · 13 MAJOR · 8 MINOR · 20 consolidated UNVERIFIED items

## Checks performed (results)

1. **Template compliance (docs 01–10):** all 10 docs have all 5 frontmatter keys (`title`, `doc_id`, `version`, `last_verified`, `applies_to_modes`), all 10 required H2 sections in the exact §2 order, all three Mode-Specific H3s, zero extra H2s, and all are ≤ 500 lines (max: 07 at 487). **PASS.**
2. **Cross-references:** 199 internal links extracted and verified against actual files + GitHub-slugified anchors. **All resolve.** (The one mechanical hit — `_conventions.md:179` → `../06-spacing.md` — is the syntax *example* inside an inline code span, not a real link; not a finding.)
3. **Library versions:** every version string, install command, and import path in docs 01–10 and templates was grepped and compared against `_facts.md`. All version *numbers* match (`gsap@3.15.0`, `lenis@1.3.23`, `motion@12.40.0`, `@barba/core@2.10.3`, `three@0.184.0`/r184, fiber 9.6.1, drei 10.7.7, postprocessing 6.39.1, ogl 1.0.11, pixi.js 8.19.0, curtainsjs 8.1.6, gpu-curtains 0.16.3, next 16.2.9, astro 6.4.6, nuxt 4.4.8, react 19.2.7, @sanity/client 7.22.1, storyblok-js-client 7.6.1, contentful 11.12.4, @prismicio/client 7.21.8, @gltf-transform/cli 4.4.0, howler 2.2.4). One *claim about* `_facts.md` is false → BLOCKER-1.
4. **Canonical values:** spacing scale (§3.5) + `--space-{n}` transform, easing table (§3.4), motion personalities (§3.2), duration classes (§3.3), type ratios (§3.6), CWV + draw-call budgets (§3.8), contrast anchors (§3.9), mode names (§3.1, lowercase everywhere) — consistent across all files except the specific mismatches below.
5. **JSON:** `templates/design-tokens.tokens.json` parses as valid JSON.
6. **Sources & Verification:** present in all 10 docs with URL + confirmed-fact + date entries. **PASS** (one format nit → MINOR-8).
7. **Efficiency:** no doc exceeds 500 lines; no >10-line cross-doc duplication found (one borderline ~8-line table duplication → MINOR-7); no "adjectives where a number should be" violations found — the corpus is consistently numeric.

---

## BLOCKER findings

### BLOCKER-1 — Doc 09 contradicts `_facts.md` about howler ownership
- **File:** `09-tech-implementation.md`, lines 140 and 279 (§2 feature map; Recommended Libraries table)
- **Problem:** Both rows state `howler@2.2.4` is "**not in `_facts.md`**". This is false: `_facts.md` §4 lists `howler` 2.2.4 (2023-09-19, MIT, "verified live by doc-09 writer"). The claim contradicts the single source of truth and instructs maintainers to treat the version as un-owned, violating `_conventions.md` §1.2 ("Library versions come ONLY from `_facts.md`"). The likely cause is that `_facts.md` was updated after doc 09 was written, but as shipped the statement is a factual contradiction.
- **Fix:** In both rows, replace "(… not in `_facts.md`)" with "(version per `_facts.md` §4)". No version change needed (2.2.4 matches).

---

## MAJOR findings

### MAJOR-1 — Doc 09 claims doc 10 "not yet present in this KB"
- **File:** `09-tech-implementation.md`, lines 364–365 (Mode-Specific Guidance → Create from scratch)
- **Problem:** "(schemas owned by doc 10-modes-and-artifacts — not yet present in this KB at time of writing, so referenced without a link)". `10-modes-and-artifacts.md` now exists; the claim is stale and the required cross-reference is missing.
- **Fix:** Replace the parenthetical with `(schemas: [doc 10](./10-modes-and-artifacts.md#specifications--parameters))`.

### MAJOR-2 — Tokens template missing the REQUIRED root `$extensions["agent.meta"]` block
- **File:** `templates/design-tokens.tokens.json`, root `$extensions` (lines 3–18)
- **Problem:** Doc 10 §3 defines a REQUIRED root-group `$extensions["agent.meta"]` with keys `version` (semver), `mode`, `archetype`, `personality`, `intensity`, `generated`, and (recreate) `confidence` (8-dimension map). The template root has only `agent.guidance` — no `agent.meta` at all, so a skeleton filled as-is fails doc 10's Quality Checklist ("root `agent.meta` block complete").
- **Fix:** Add to root `$extensions`, alongside `agent.guidance`:
  ```json
  "agent.meta": {
    "version": "1.0.0", "mode": "<create|recreate|modify>",
    "archetype": "<token>", "personality": "<snappy|fluid|cinematic>",
    "intensity": "<ambient|responsive|showcase>", "generated": "<YYYY-MM-DD>",
    "confidence": { "archetype": "", "typography": "", "color": "", "layout": "",
                    "spacing": "", "imagery": "", "motion": "", "webgl-stack": "" }
  }
  ```
  with a note that `confidence` is recreate-only (per doc 10 Code Example B).

### MAJOR-3 — Confidence-map dimensions/shape mismatch (template vs doc 10 §2.9)
- **File:** `templates/design-system-spec.md`, frontmatter lines 11–19
- **Problem:** Doc 10 §2.9 defines the canonical 8 dimensions as `archetype, typography, color, layout, spacing, imagery, motion, webgl-stack`, recorded as a **table in spec §9** with columns confidence + provenance (`measured|inferred|assumed`) + evidence + snap deltas. The template instead has a YAML frontmatter block whose keys are `archetype, typography, color, spacing, layout, components, motion, imagery` — it contains `components` (not a canonical dimension), omits `webgl-stack`, and has no provenance/evidence/snap-delta columns anywhere. Doc 10 Code Example B (`agent.meta.confidence`) confirms the canonical key set.
- **Fix:** Replace `components:` with `webgl-stack:` in the frontmatter block, and add a §9 "Provenance & Confidence" section with the 4-column per-dimension table (see MAJOR-4); the frontmatter block can stay as a summary but must use the canonical 8 keys.

### MAJOR-4 — `design-system-spec.md` template does not match doc 10 §2 section schema
- **File:** `templates/design-system-spec.md` (whole-file structure) vs `10-modes-and-artifacts.md` §2 ("exact, ordered")
- **Problem (full diff):**
  | # | Doc 10 §2 schema | Template | Mismatch |
  |---|---|---|---|
  | 1 | Identity & Direction | Brand & Archetype | name |
  | 2 | Typography | Typography | OK |
  | 3 | Color | Color | OK |
  | 4 | Layout & Grid | **Spacing** | order swapped |
  | 5 | Spacing & Rhythm | **Layout & Grid** | order swapped + name |
  | 6 | Imagery & Asset Direction | Components | position; schema §6 appears as template §8 named "Imagery & **Art** Direction" |
  | 7 | Components | Motion Language | position; "Motion Language" is not in the schema (motion belongs to `motion-spec.md`) |
  | 8 | Accessibility Notes | Imagery & Art Direction | name + position |
  | 9 | **Provenance & Confidence** | Accessibility | **schema §9 missing from template** |
  | 10 | **Changelog** | Performance Budget | **schema §10 missing from template**; "Performance Budget" is not in the schema (budgets belong to `implementation-plan.md` §2) |
  Additionally, frontmatter keys `motion_personality` / `intensity_tier` differ from the canonical field names `personality` / `intensity` used by doc 10 §2.1 and `agent.meta`.
- **Fix:** Doc 10 is the canonical owner ("the skeletons in `./templates/` implement the schemas defined here, never the reverse"): rename/reorder the template sections to the doc 10 §2 sequence, add **§9 Provenance & Confidence** (per-dimension table: confidence | provenance | evidence | snap deltas) and **§10 Changelog** (semver, date, diffs, rationale), and either delete Motion Language / Performance Budget or move them into doc 10 §2 as explicit schema additions (one edit, not two divergent truths). Rename frontmatter keys to `personality` / `intensity` (or add the mapping note to doc 10).

### MAJOR-5 — `motion-spec.md` template does not match doc 10 §4 section schema
- **File:** `templates/motion-spec.md` vs `10-modes-and-artifacts.md` §4 ("exact, ordered")
- **Problem:** Schema: 1 Motion Identity · 2 Easing & Duration Tokens · 3 Choreography Inventory · 4 Scroll Behavior · 5 Page Transitions · 6 Reduced-Motion Variants · 7 Performance Notes. Template: 1 Global Motion Settings · 2 Global Reduced-Motion Policy · 3 Per-Element Motion Table · 4 Scroll Choreography Scenes · 5 Page Transitions · 6 Quality Gate. Mismatches: every section name except §5; reduced motion at §2 vs schema §6; schema §2 (easing/duration **tokens with names as registered in `design-tokens.tokens.json` `motion.*`**) is folded into a settings table without token names; the Choreography Inventory lacks the schema-required **overlap (% of previous tween)** column; schema §7 Performance Notes has no counterpart (partially absorbed by a Quality Gate that is not in the schema).
- **Fix:** Rename/reorder template sections 1–7 to match doc 10 §4; add an `overlap` column to the per-element table; add a Performance Notes section (transform/opacity-only confirmation, input feedback ≤ 200 ms); keep the Quality Gate as an optional trailing section only if doc 10 §4 is amended to include it.

### MAJOR-6 — `implementation-plan.md` template does not match doc 10 §5 schema; Accessibility Plan section missing
- **File:** `templates/implementation-plan.md` vs `10-modes-and-artifacts.md` §5 ("exact, ordered")
- **Problem:** Schema: 1 Stack Decision · 2 Performance Budgets · 3 Build Phases · 4 Asset Pipeline · 5 **Accessibility Plan** · 6 Testing & Verification Gates · 7 Risks & Open Questions. Template: 1 Chosen Stack · 2 Libraries & Verified Versions (not in schema) · 3 Milestones · 4 Performance Budget · 5 Asset Pipeline · 6 QA Checklist · 7 Risks & Unverified Items. The schema-required **Accessibility Plan** section (reduced-motion coverage, contrast gate, keyboard/focus per doc 09 §4) is entirely absent (only scattered QA checkboxes); budgets sit at §4 instead of §2; names differ on §§1/3/6/7. Also the schema requires "WebGL rung chosen + ruled-out lighter rungs" in §1 — the template's Chosen Stack table has no row/field for it.
- **Fix:** Insert a dedicated "## 5. Accessibility Plan" section; reorder budgets to §2 (or amend doc 10 §5); rename sections to the schema names; add a "WebGL rung + ruled-out rungs" row to §1; keep "Libraries & Verified Versions" only if added to doc 10 §5.

### MAJOR-7 — Template artifact versions `0.1` violate doc 10's semver rule
- **Files:** `templates/design-system-spec.md`:4, `templates/motion-spec.md`:4, `templates/implementation-plan.md`:4 (frontmatter `version: 0.1`)
- **Problem:** Doc 10 Principle 5 + Quality Checklist: artifacts are semver-versioned; `create`/`recreate` emit **`1.0.0`**. `0.1` is not valid semver and contradicts the checklist gate.
- **Fix:** Change to `version: 1.0.0` (or placeholder `<semver — 1.0.0 for create/recreate>`).

### MAJOR-8 — Doc 10 token name `motion.ease.inOut` violates the kebab-case convention
- **File:** `10-modes-and-artifacts.md`, Code Example B (line ~285): `"inOut"` key
- **Problem:** `_conventions.md` §3.7: multiword token segments are kebab-case. The tokens template correctly uses `motion.ease.in-out`; doc 10's canonical example uses `inOut`, which would emit a different CSS variable (`--motion-ease-inout` vs `--motion-ease-in-out`) and diverges from the skeleton it claims to define.
- **Fix:** Change doc 10 Code Example B key to `"in-out"`.

### MAJOR-9 — Type-scale token naming differs three ways across 04 / tokens template / spec template
- **Files:** `04-typography.md` §4.2 + Code Examples (`type.step.0–6`, `--step-N`); `templates/design-tokens.tokens.json` (`typography.display`, `typography.body` composites + `font.*`); `templates/design-system-spec.md` §2 (`typography.display/h1/h2/h3/body/small`); `10-modes-and-artifacts.md` §3 (top-level groups listed as `color`, `font`, `space`, `motion` + components — neither `type` nor `typography` defined).
- **Problem:** The same design dimension (the type scale) has three incompatible token vocabularies, and the tokens template introduces a top-level `typography` group that doc 10's canonical group list doesn't include. An agent emitting tokens from doc 04 produces `type.step.N`; one filling the templates produces `typography.*` — the artifacts won't line up, and the spec template's `typography.h1` names exist nowhere else.
- **Fix:** Pick one vocabulary and propagate: recommend keeping doc 04's `type.step.N` for primitive scale steps, adding `typography.*` composites as role tokens that alias them, and amending doc 10 §3's group list to `color`, `font`, `type`/`typography`, `space`, `motion` + components. Update the spec template §2 step tokens to match.

### MAJOR-10 — Doc 03's breakpoints table contradicts its own fluid clamp recipes
- **File:** `03-layout.md` — "Canonical breakpoints" table (lines 70–77) vs "The 12-column primary grid" / "Fluid layout dimension recipes" (lines 90–148)
- **Problem:** The breakpoints table specifies stepped gutters/margins per breakpoint (gutter: 24 px at `bp.md`/768 and `bp.lg`/1024, 32 px at `bp.xl`/1280; outer margin: 48 px at `bp.md`), while the same doc's canonical fluid recipes — also consumed by doc 06 and Code Example A — yield different values at those widths: gutter `clamp(16px, 1.25vw + 8px, 32px)` = **17.6 px @768, 20.8 px @1024, 24 px @1280**; margin `clamp(24px, 6vw − 24px, 96px)` = **24 px @800, 37.4 px @1024** — i.e. the margin would *shrink* from the table's 48 px at 768 to 37.4 px when crossing 1024. Two conflicting specs for the same dimensions.
- **Fix:** Make the fluid recipes the single source: replace the table's Gutter/Outer-margin columns with the clamp-resolved values at each breakpoint (16/16/18/21/24/27 px gutter etc.), or explicitly label the table values as the *non-fluid fallback tier* and recompute the margin recipe so it is monotonic across 768→1024 (e.g. fluid range 768→2000 with min `space.12`).

### MAJOR-11 — Word/line stagger bands contradict between doc 04 and doc 07
- **Files:** `04-typography.md` §4.7 (line 197: words **0.03–0.05 s**, lines **0.05 s**; recipe uses 0.04) vs `07-animation-choreography.md` Stagger standards (line 138: words/lines **0.06–0.10**, "lines read best at 0.08")
- **Problem:** Doc 04's words band tops out below doc 07's floor; doc 04's canonical SplitText recipe (`stagger: 0.04`) violates doc 07's table outright. Ownership is split (doc 04 owns the SplitText recipe; doc 07 owns stagger standards), so an agent gets contradictory instructions for the same reveal.
- **Fix:** In doc 07's table, split the row: "words (SplitText) 0.03–0.05 — recipe owned by doc 04" and "lines 0.05–0.10, best 0.08", or align both docs on a single band (recommend 0.03–0.06 words / 0.05–0.08 lines) — one edit in each table.

### MAJOR-12 — Doc 04 reduced-motion fallback exceeds the ≤ 200 ms canonical collapse
- **File:** `04-typography.md`, SplitText recipe reduced branch (line 322): `gsap.from(".hero-title", { opacity: 0, duration: 0.3, ease: "none" })`
- **Problem:** The canonical reduced-motion collapse — doc 07 (owner): "opacity fades ≤ 200 ms"; doc 01 §2: "opacity-only fades of 150–200 ms"; motion-spec template §2: "≤ 200 ms" — caps at 200 ms. Doc 04's example uses 300 ms.
- **Fix:** Change `duration: 0.3` → `duration: 0.2` in the example.

### MAJOR-13 — Lenis `lerp` range: doc 07 caps at 0.15, doc 01 and both templates allow 0.18
- **Files:** `07-animation-choreography.md`:161 ("stay within **0.05–0.15**") vs `01-visual-motion.md`:200 (snappy intent **0.14–0.18**), `templates/design-system-spec.md`:168 and `templates/motion-spec.md`:38 ("lerp <**0.05–0.18**>")
- **Problem:** Doc 07 owns the Lenis setup and forbids lerp > 0.15; doc 01's snappy band and both artifact templates permit up to 0.18. A snappy build following doc 01 violates doc 07's tuning rule.
- **Fix:** Harmonize: either doc 07 widens to "stay within 0.05–0.18 (snappy may also use native scroll)" or doc 01/templates cap at 0.15 (change doc 01 snappy band to 0.12–0.15 and templates to `<0.05–0.15>`). One value, three files.

---

## MINOR findings

### MINOR-1 — Hover-scale band in doc 07 ignores doc 01's personality bands
- **File:** `07-animation-choreography.md` micro-interaction catalog, "Hover lift" row (line 193): `scale: 1.03–1.05`.
- **Problem:** Doc 01 §2 pins hover scale per personality: snappy **1.00**, fluid 1.02–1.04, cinematic 1.04–1.06. Doc 07's generic 1.03–1.05 straddles fluid/cinematic and contradicts snappy.
- **Fix:** Replace with "scale per the doc 01 personality band ([doc 01 §2](./01-visual-motion.md#specifications--parameters)); y: −2 to −4 px, 150–200 ms `power2.out`".

### MINOR-2 — Doc 07 View-Transitions CSS comment mislabels the duration class
- **File:** `07-animation-choreography.md`, Code Example 4 (line 340): "durations map to the hero/cinematic class" above 250 ms / 420 ms values.
- **Problem:** 250 ms is the UI-transition class and 420 ms the content-reveal class, not hero/cinematic (600–1200 ms). The values themselves match the doc's own page-transition table — only the comment is wrong.
- **Fix:** Change comment to "old-out = UI-transition class; new-in = content-reveal class (page-transition table above)".

### MINOR-3 — Doc 02 claims its srcset ladder aligns with doc 03 breakpoints
- **File:** `02-image-generation.md` §4.4 (line 173): widths 640/960/1280/1600/1920/2560 "(align breakpoints with [03-layout])".
- **Problem:** Doc 03's canonical breakpoints are 480/768/1024/1280/1440 — only 1280 coincides. srcset widths legitimately differ from layout breakpoints, but the parenthetical asserts an alignment that does not exist.
- **Fix:** Reword to "(srcset widths are delivery sizes, independent of the layout breakpoints in [03-layout](./03-layout.md#specifications--parameters))" or adjust the ladder.

### MINOR-4 — Implementation-plan template's glTF command diverges from doc 09's canonical pipeline
- **File:** `templates/implementation-plan.md` §5 (line 113): `gltf-transform optimize … --compress draco --texture-compress webp`.
- **Problem:** Doc 09 §3 (canonical owner) specifies `--texture-compress ktx2` (or the two-pass UASTC/ETC1S flow), and the §1 budget row assumes "GPU textures per scene (KTX2 transfer)". WebP textures inside GLBs bypass the KTX2 codec rule.
- **Fix:** Replace with the doc 09 §3 one-shot (`--compress draco --texture-compress ktx2 --texture-size 2048`) and link `../09-tech-implementation.md#specifications--parameters` for the two-pass variant.

### MINOR-5 — Templates omit now-resolvable links to docs 09/10 (deliberate at authoring time)
- **Files/locations & fixes:**
  - `templates/design-system-spec.md` §10 Performance Budget → add link to the canonical budget table `../09-tech-implementation.md#specifications--parameters`; header comment → add schema owner link `../10-modes-and-artifacts.md#specifications--parameters`.
  - `templates/motion-spec.md` header comment → add `../10-modes-and-artifacts.md#specifications--parameters` (§4 schema).
  - `templates/implementation-plan.md` §1 → `../09-tech-implementation.md#decision-framework`; §4 → `../09-tech-implementation.md#specifications--parameters`; header comment → `../10-modes-and-artifacts.md#specifications--parameters` (§5 schema).
  - `templates/design-tokens.tokens.json` `agent.guidance` → add a reference string to `10-modes-and-artifacts.md` §3 (schema + `agent.meta` requirement).

### MINOR-6 — letterSpacing unit conflict between doc 04 and the tokens template
- **Files:** `04-typography.md` §4.3 ("letter-spacing always in **em**") vs `templates/design-tokens.tokens.json` `typography.display` (`letterSpacing: {value: -1, unit: "px"}`; DTCG `dimension` allows px/rem only).
- **Problem:** The template's px value (with an explanatory `$description`) silently contradicts doc 04's rule; the reconciliation lives only in the template.
- **Fix:** Add one sentence to doc 04 §4.3: "DTCG `dimension` cannot express em — store the px equivalent at the composite's fontSize in the token file and keep em values in authored CSS," or store the em factor in `$extensions["agent.tracking"]`.

### MINOR-7 — Near-duplicate fluid-recipe tables in docs 03 and 06
- **Files:** `03-layout.md` "Fluid layout dimension recipes" (lines 136–144) vs `06-spacing.md` "Canonical worked recipes" (lines 164–171).
- **Problem:** ~8 lines of substantively identical clamp recipes (gutter/margin/section) in both docs. Doc 06 is the owner (§4 ownership map: "Spacing scale, rhythm, fluid spacing"). Currently in sync, but two copies invite drift (see MAJOR-10 for what drift does).
- **Fix:** In doc 03, keep only the two recipes its Code Example A consumes, marked "values owned by [doc 06](./06-spacing.md#specifications--parameters) — do not edit here"; drop the derivation row (doc 06 owns the math).

### MINOR-8 — Doc 07 Sources entry is a file path, not a URL
- **File:** `07-animation-choreography.md` Sources & Verification, first entry (line 471): `- ./_facts.md — confirmed: …`.
- **Problem:** `_conventions.md` §1.6 entry format is URL + fact + date. Substantively fine (it correctly credits `_facts.md`), but format-deviant.
- **Fix:** Keep the entry but lead with "(internal)" or move it to a one-line preamble above the URL list, e.g. "All versions/installs/imports and the VT support matrix per `_facts.md`."

---

## Consolidated UNVERIFIED list ("UNVERIFIED — confirm before use" flags across the KB)

| # | File (line) | Item |
|---|---|---|
| 1 | `_facts.md` (105, 204) | `@react-three/drei` v11-alpha ↔ fiber v10 pairing |
| 2 | `_facts.md` (111, 205) | `postprocessing` v7 (beta) WebGPU support details |
| 3 | `_facts.md` (131, 206) | curtains.js "officially legacy" designation (dormancy verified; no official notice) |
| 4 | `_facts.md` (134, 207) | gpu-curtains as formally declared "official successor" to curtains.js |
| 5 | `_facts.md` (208) | GSAP plugin import subpath syntax — tarball-verified, quoted-docs confirmation pending |
| 6 | `02-image-generation.md` (121) | Current Midjourney default `--sv` value |
| 7 | `02-image-generation.md` (141, 390) | Nano Banana Pro published aspect-ratio enumeration (third-party source only) |
| 8 | `02-image-generation.md` (200) | nidorx/matcaps repo license for commercial use |
| 9 | `02-image-generation.md` (210, 401) | BRIA RMBG-2.0 commercial-use license terms |
| 10 | `04-typography.md` (191, 215) | `pyftsubset` (fontTools) / `subfont` versions (not in `_facts.md`) |
| 11 | `05-color.md` (250) | Style Dictionary version/package (token build tool) |
| 12 | `06-spacing.md` (231) | Style Dictionary version (token transform pipeline) |
| 13 | `07-animation-choreography.md` (119) | `power2.in` CSS approximation `cubic-bezier(0.55, 0.055, 0.675, 0.19)` (Penner easeInCubic) |
| 14 | `08-webgl-effects.md` (71, 214) | gpu-curtains successor status (carries _facts flag #4) |
| 15 | `08-webgl-effects.md` (176) | postprocessing v7-beta WebGPU details (carries _facts flag #2) |
| 16 | `08-webgl-effects.md` (210) | drei v11-alpha ↔ fiber v10 pairing (carries _facts flag #1) |
| 17 | `08-webgl-effects.md` (215) | curtainsjs "officially legacy" (carries _facts flag #3) |
| 18 | `09-tech-implementation.md` (276) | `npm create nuxt@latest` scaffolder name |
| 19 | `09-tech-implementation.md` (280) | `web-vitals` library version (not in `_facts.md`) |
| 20 | `templates/implementation-plan.md` (58–59, 137–138) | drei v11-alpha pairing + postprocessing v7-beta (carried flags, pre-filled example risk rows) |

(References to the flag *syntax* in `_conventions.md`, `_facts.md` headers, doc 10 policy text, `01-visual-motion.md`:336, and template placeholder text are rule statements, not open items, and are excluded.)

---

## Summary

| Severity | Count |
|---|---|
| BLOCKER | 1 |
| MAJOR | 13 |
| MINOR | 8 |
| **Total findings** | **22** |
| UNVERIFIED items (consolidated) | 20 |

**Overall:** Structural compliance is excellent — all 10 docs match the shared template exactly, all 199 internal links resolve, every version number matches `_facts.md`, and the canonical glossary values (spacing scale, easings, durations, ratios, budgets, contrast, mode names) hold across the corpus. The concentrated risk is exactly where predicted: the four `templates/` skeletons predate doc 10 and diverge from its canonical artifact schemas in section names, order, required sections (`agent.meta`, Provenance & Confidence, Changelog, Accessibility Plan) and the confidence-dimension set. Secondary cluster: a handful of motion-value contradictions (stagger bands, reduced-motion duration, Lenis lerp cap, hover scale) between docs 01/04/07, and one internal layout contradiction in doc 03.

---

## Re-review (fix-cycle verification, 2026-06-12)

Method: every original finding re-checked against current file state; regression pass on all touched files (doc 10 internal renumbering, schema↔template section-for-section diff, doc 04 ↔ tokens `type.step` values, canonical values vs `_facts.md`/`_conventions.md`); scripted full link sweep (16 files); scripted JSON parse + alias resolution.

### Per-original-finding verification

| Finding | Status | Evidence (current state) |
|---|---|---|
| BLOCKER-1 | **RESOLVED** | `09`:140 + 279 now read "howler@2.2.4 (MIT; version per `_facts.md` §4 — dormant ~33 months but stable)"; contradiction removed |
| MAJOR-1 | **RESOLVED** | `09`:364–365 now links "(schemas: [doc 10](./10-modes-and-artifacts.md#specifications--parameters))" |
| MAJOR-2 | **RESOLVED** | tokens JSON root `$extensions["agent.meta"]` (lines 4–21) with `version` 1.0.0, `mode`, `archetype`, `personality`, `intensity`, `generated`, 8-key `confidence`; `fillOrder[0]` marks confidence recreate-only (DELETE in create/modify) |
| MAJOR-3 | **RESOLVED** | spec-template frontmatter confidence block now the canonical 8 keys (`webgl-stack` in, `components` out); new §11 Provenance & Confidence with Dimension/Confidence/Provenance/Evidence/Snap-deltas table |
| MAJOR-4 | **RESOLVED** | doc 10 §2 amended to a 12-section schema (Motion Language §8, Performance Budget §10 added as explicit schema sections; Accessibility §9, Provenance & Confidence §11, Changelog §12); template now matches §1–§12 name-for-name, order-for-order; frontmatter keys renamed `personality`/`intensity` |
| MAJOR-5 | **RESOLVED** | motion-spec template = doc 10 §4 exactly: 1 Motion Identity · 2 Easing & Duration Tokens (with `motion.*` token names) · 3 Choreography Inventory (overlap column present) · 4 Scroll Behavior · 5 Page Transitions · 6 Reduced-Motion Variants · 7 Performance Notes (transform/opacity + ≤200 ms INP guard); Quality Gate absorbed into §7 |
| MAJOR-6 | **RESOLVED** | impl-plan = doc 10 §5 exactly: 1 Stack Decision (WebGL rung row + ruled-out lighter rungs REQUIRED; library tables as a §1 subsection, sanctioned by §5.1 "framework + libraries") · 2 Performance Budgets · 3 Build Phases · 4 Asset Pipeline · 5 Accessibility Plan (dedicated section present) · 6 Testing & Verification Gates · 7 Risks & Open Questions |
| MAJOR-7 | **RESOLVED** | all three .md templates: `version: 1.0.0` with semver comment |
| MAJOR-8 | **RESOLVED** | doc 10 Code Example B key is `"in-out"` (kebab-case, = tokens template) |
| MAJOR-9 | **RESOLVED** | one vocabulary: doc 10 §3 group list now defines `type` (`type.step.{N}`, owner doc 04, clamp-max + `agent.fluid`) and `typography` composites whose `fontSize` MUST alias `{type.step.N}`; tokens template has the `type.step` group (0: 18px/min 16, 6: 69px/min 48, range 320–1280 = doc 04 §4.2 exactly) and `typography.display/body` aliasing `{type.step.6}`/`{type.step.0}`; spec-template §2 table uses `typography.*` role tokens with `{type.step.N}` aliases |
| MAJOR-10 | **RESOLVED** | doc 03 breakpoints table now shows the clamp-resolved values (gutter 16/16/17.6/20.8/24/26 px; margin 24/24/24/37.44/52.8/62.4 px) with explicit "never stepped per breakpoint" rule + worked math; sequences monotonic (margin min holds to 800, max at 2000) — re-derived and confirmed arithmetically |
| MAJOR-11 | **RESOLVED** | aligned on doc 07 bands: doc 04 §4.7 now "chars 0.02–0.05 s, words/lines 0.06–0.10 s — stagger standards owned by doc 07"; recipe `stagger: 0.06`; doc 07 chars row credits doc 04 as recipe owner; doc 04 checklist matches |
| MAJOR-12 | **RESOLVED** | doc 04 reduced branch now `duration: 0.2` (≤ 200 ms canonical collapse) |
| MAJOR-13 | **RESOLVED** | doc 07:161 widened to "stay within 0.05–0.18 — per-personality bands: doc 01"; doc 01 snappy 0.14–0.18 now inside; both templates keep `<0.05–0.18>`; one value everywhere |
| MINOR-1 | **RESOLVED** | doc 07 hover-lift row defers scale to "the personality band owned by doc 01" |
| MINOR-2 | **RESOLVED** | doc 07 Code Example 4 comment: "old-out = UI-transition class; new-in = content/section-reveal class" (matches 250/420 ms values) |
| MINOR-3 | **RESOLVED** | doc 02 §4.4: ladder widths declared "delivery sizes … independent of the canonical breakpoints in [03-layout]" |
| MINOR-4 | **RESOLVED** | impl-plan §4 one-shot now `--texture-compress ktx2 --texture-size 2048` + link to doc 09 two-pass variant |
| MINOR-5 | **RESOLVED** | all listed links present: spec-template header + §10 → docs 10/09; motion-spec header → doc 10 §4; impl-plan header/§1/§2/§4 → docs 10/09; tokens `agent.guidance.schema` → "10-modes-and-artifacts.md section 3" |
| MINOR-6 | **RESOLVED** | em factor now stored authoritatively in `$extensions["agent.tracking"]` (`em: -0.02` / `0`) with stored px = em × step max (−1.38 px = −0.02 em × 69 px, verified), per the finding's option B |
| MINOR-7 | **RESOLVED** | doc 03 recipes table marked "owned by [06-spacing] … do not edit them here"; derivation row dropped (slope/intercept math lives only in doc 06); values verified identical 03 ↔ 06 ↔ tokens `agent.fluid` ranges (640–1920 / 800–2000 / 800–1600) |
| MINOR-8 | **RESOLVED** | doc 07 Sources now all URL-format (npmjs/caniuse/gsap.com entries confirm the version facts); no file-path entry remains |

**22 / 22 original findings RESOLVED. 0 NOT RESOLVED.**

### Regression check (touched files)

- **Doc 10 renumbering:** all internal references consistent with the new 12-section §2 schema — `§2.11` confidence map (agent.meta), "spec §11" ×7 (Provenance & Confidence), "spec §12 changelog", "spec §8 summary" (Motion Language), "spec §6" (Imagery), "spec §4" (Layout & Grid), "implementation-plan.md §2" (Performance Budgets). No stale pointers found. Inbound references from docs 01/03/05/08/09 use heading anchors or unnumbered "doc 10" mentions only — none broken by the renumbering.
- **Schema ↔ template alignment (doc 10 §§2–5 vs all four templates):** section-for-section identical (names, order, required fields, columns). Spec §1 carries archetype/personality/intensity + 5–8 signals + signature interaction; choreography table has the overlap column; impl-plan §1 has the WebGL-rung row.
- **Doc 04 ↔ tokens `type.step`:** step.0 = 16→18 px and step.6 = 48→69 px @ 320–1280 in both; `typography.*` fontSizes alias, never restate.
- **Values vs `_facts.md`/`_conventions.md`:** all versions in touched files match `_facts.md` (gsap 3.15.0, lenis 1.3.23, motion 12.40.0, three 0.184.0, fiber 9.6.1, drei 10.7.7, howler 2.2.4, gltf-transform 4.4.0, frameworks/CMS rows); easing/duration/spacing/contrast/mode-name canonicals hold; tokens motion values sit in the fluid slices (160/350/600/800 vs doc 01 matrix); doc 10 Code Example B slice note (UI 300–400, reveal 450–650) matches doc 01.
- **Template compliance:** docs 01–10 all retain the 5 frontmatter keys, the exact 10-H2 order, and the three Mode-Specific H3s; max line count 492 (doc 07) — all ≤ 500.
- **New findings: none** (0 BLOCKER / 0 MAJOR / 0 MINOR).

### Link sweep (scripted, GitHub slugification)

206 internal markdown links across all 16 files: **all resolve** (file + anchor). Additionally, 84 plain-path references inside template comments (`../NN-*.md#anchor`) checked: **all resolve**. Doc 10's §2 restructure added no headings-level changes, so no inbound anchors broke.

### JSON validation

`templates/design-tokens.tokens.json`: **parses** (python3 json). 49 tokens defined; 25 alias references (in `$value`, composite sub-values, and `$extensions["agent.fluid"]` endpoints): **all resolve** to tokens defined in the same file. Root `agent.meta` complete; top-level groups (`color`, `space`, `font`, `type`, `typography`, `motion`, `button`, `card`) all within the doc 10 §3 group list.

### Verdict

VERDICT: PASS (0 BLOCKER / 0 MAJOR outstanding)
