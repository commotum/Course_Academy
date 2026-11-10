# Inline proof dropdowns and menu layout repairs

Completed in the live database and the shared UI. The requested response format remains **dropdowns**.

## Changes

The proof questions q-337728 (`17592186311877`), q-337739 (`17592186311880`), and q-338094 (`17592186311915`) now place their dropdowns directly at each missing expression. Their imported markers were inside a single `aligned` TeX block. The renderer could not put interactive HTML inside that SVG, so it drew empty underlines and placed the controls after the equation. The repaired prompts use complete math fragments with actual field slots between them. The fourth similar question, q-337675, was already inline and was checked without changing it.

Dropdown menus now size to their options before selection, use the available screen width, and shift into the viewport when needed. The old 360px cap clipped long expressions; selecting a long option happened to widen the trigger and therefore the menu. Menus no longer use horizontal or internal vertical scrolling. If an expression exceeds the viewport, its SVG scales proportionally to keep the complete option visible. Menus stay open during interactions with their own padding; real outside clicks, Tab, and Escape retain their normal behavior. Positioning updates after math rendering and on window resize.

The operator list in canonical example e-21786 (`17592186228933`) mixed one inline expression with two centered display blocks. All three now use the same inline display style and share the same left edge.

## Saved content and history

The proof-layout transaction committed at **13677**. The example-format transaction committed at **13696**. Exact-basis readback of all 33 lesson questions matches the intended result. Both receipts contain only `question/problem` changes and transaction timestamps. Field types, keys, choice banks, correct answers, solutions, entity IDs, learner attempts, and progress were preserved. The grading engine is unchanged.

## Verification

- All **30 practice questions** passed **154 actual read-only grading checks**, covering correct responses and every alternative option. No learner attempts were created.
- All **190 dropdown banks** found across the 19-topic list passed **570 layout/interaction checks** at 1100px, 708px, and 390px. Options are fully visible before selection, selected values fit, menus have no nested horizontal scrollbars, and pointer/keyboard behavior preserves choice IDs. The menu also stays open and correctly positioned during viewport resizing.
- All four proof questions passed **12 actual-player inline placement checks**. Every required control is mounted once, inside its intended proof step, with no trailing bank or ghost underline.
- The alignment example passed at all three widths. Its SVG left-edge spread is now **0px**, versus up to 211px before correction.
- All **15 shared question-field unit tests** pass. The running app serves the final CSS and JavaScript.

Reload an already-open page to load the updated shared UI.

## Evidence

- [Combined verification](verification-summary.json)
- [Committed content readback](final-readback.json)
- [Grading checks](grading-checks.json)
- [All dropdown checks](all-19-dropdown-verification.json)
- [Current bank inventory](all-19-bank-freshness.json)
- [Inline placement checks](inline-verification.json)
- [Alignment checks](alignment-layout.json)
- [Inline proof screenshot](visual/inline-proof-708.png)
- [Dropdown screenshot](visual/dropdown-708.png)
- [Aligned operators screenshot](visual/operator-alignment-after-708.png)
