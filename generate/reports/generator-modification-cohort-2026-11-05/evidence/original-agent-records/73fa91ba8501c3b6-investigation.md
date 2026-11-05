# Using the Double-Angle Formula Multiple Times

Target KP **17592186059672**, UUID `d820aa9f-7c02-53b5-9b09-c25ee59dbdaf`; math lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, basis **7200**. Investigation uses only the supplied source, inventory, and reference snapshots. No database selection, publication, or import mutation was performed.

## Learner operation and source fidelity

Recognize a matched sine–cosine pair, account for the factor of two, and notice that doubling its angle creates another matched pair. Apply the identity again, then evaluate a special-angle sine. In quotient forms, a reciprocal identity reveals the second pair. Degree/radian fluency, reciprocal identities, exact special-angle values, and fraction arithmetic are the supporting operations.

The supplied lesson derives `sin(2x)=2 sin(x) cos(x)` from the sine addition formula and visits product simplification (KP 17592186059671), ratio simplification (17592186059673), and single-use exact evaluation (17592186059674) before the target. These are lesson-context supports; the target has no explicit prerequisite records in this snapshot. Canonical example **35535b08-b3d8-5037-a821-6815577169d2** uses angles pi/24 → pi/12 → pi/6 and two factors of one-half to obtain 1/8. Retained components are the repeated-angle chain, explicit coefficient accounting, exact evaluation, radio choice banks, and hard blank responses. The source has no diagrams or image references; plot requirement is **none**.

Complete imported practice: **6 moderate, 7 hard, 0 easy**. Observed coverage remains **moderate, hard**, including incomplete imports' stored labels. The product chain is moderate in **b22f045c-0b9c-53f1-b536-66fda02ca447**, but also occurs with hard labels in **91b3ae38-a411-55e5-ba0c-b0976c1d82dd** and **4270d786-b50e-5319-88f8-bca386712273**. Thus neither radians nor the imported label alone establishes a harder reasoning task.

Five moderate items instead use one double-angle substitution followed by cosecant cancellation; examples are **8883bfa3-8f36-5e8a-8a63-990442c2b246** and **f30309d1-f3e3-55ac-be8a-acbe0c0f980a**. These are valid source evidence, but are unsuitable as the defining repeated-use progression. Hard quotient examples include radio **87e7afa8-1798-5127-a9ff-a08924db07de**, blank **6a88295e-a9f4-5381-9209-7cdc6c3b161d**, and secant-over-product blank **4fabc70d-25ca-5a30-9a52-90a915524efa**, whose negative exact answer also supports quadrant reasoning. The inventory ledger in `evidence/source-classification.json` records every target question's response structure, complete bank, and missing components.

Partial imports **0ab58d1b-4097-516b-91bf-48c130e66ed2** (missing solution, difficulty, key) and **19bb82ee-2583-57ae-92ec-48971505d385** (missing fields) remain exactly as stored. Their product/quotient structures inform interpretation without supplying nonexistent answers or provenance.

## Reference progression and design decision

Reference KP **17592186059673** has five-choice radio fields throughout. Easy **dde407ba-34c3-55d5-a98c-cb0e2c5bb577** expands a numerator and cancels; easy **95efa6da-7216-501c-8391-1e0cbd18db0c** also converts cotangent. Moderate **b2050e06-0476-56c1-a7a1-1d0ef234a4b2** expands a denominator and recognizes secant; **1a84df43-c63e-5997-bb62-0b42cedd5faa** converts cosecant and cancels. These easy/moderate labels overlap in actual workload. Hard **df53af64-a7fb-5920-a9ae-4765f5d7236c** and **20492e7a-2ad5-5346-9935-34abf42dcea6** genuinely add coordinating identities, factoring a difference of squares, and cancellation.

The reference's long worked solutions appear **after** answering: they are explanations, not supplied hints or required written work. The target imports likewise mainly assess a final selection/value. I adapt the reference's shift toward coordinating representations, without importing its Pythagorean/factorization task.

Exactly three new ordinary questions are in `exemplars.json`:

| Level | New question UUID | Demand before answering |
| --- | --- | --- |
| Easy | 067c61cc-fb72-4125-a7e4-fd924b1637d0 | Identity and both substitution angles supplied; learner carries out both substitutions and selects sqrt(2)/2. |
| Moderate | 46b09c53-7b97-4c54-86c4-759100a3b61d | No hints; discover the repeated pair and manage two one-half factors; select 3 sqrt(3)/8. |
| Hard | ecc19dce-75cf-4814-9cfd-aa73bdf46186 | Reorganize a secant quotient, apply double-angle twice, determine the quadrant sign, and enter -4 sqrt(2) without answer choices. |

Easy support is deliberately added in the prompt, rather than treating a post-answer derivation as scaffolding. Every level retains repeated use. Increased independence and reciprocal restructuring determine difficulty; coefficient magnitude does not. The harder blank matches existing target response demands. No written derivation is required from the learner. All new identities are fresh UUIDs, and none claims a Math Academy ID or carries reconstruction tags.

## Checks and result

- Independently evaluated all three expressions with exact SymPy trigonometry, separately from the written derivations; residuals are zero. Checked all radio choices for uniqueness and exactly one correct value (`evidence/independent-math.json`).
- Actual native `learning::grade_field`: **18 checks, 5 accepted, 13 rejected, zero unresolved**. This includes every radio option, the hard canonical answer, two exact equivalents, and five plausible sign/factor/special-angle errors (`evidence/grading.json`). Initial use of a pulled-object correct reference was changed to the generator's normal UUID lookup reference before the successful check; no shared repair was needed.
- All three band-specific delivery audits accepted one question each, with zero duplicates against the captured inventory and zero database writes. Strict math-format and publisher validation also passed. Fresh IDs and correct references remain consistent (`evidence/delivery-{easy,moderate,hard}/delivery.json`).
- Rendered the final records through `generate/pipeline/render_preview.py` and the unmodified learning UI. Inspected all completed screenshots, prompts, radio options, blank response, and full solutions. Corrected a clipped easy-solution equation by naming the original expression E and rerendered; all lines are now readable. Reports show no math/JavaScript errors, raw TeX, broken images, or missing glyphs. There are no dropdown controls. Supplemental active-route previews check the unanswered controls (`evidence/render/`, `evidence/render-active/`).
- Input snapshot hashes are retained and rechecked; imports are unchanged. No shared files or grader binary were changed. `session-state.md` records the completed state.

These are three checked instructional examples, not a generator distribution audit or live publication. Future practice should vary compatible angle chains, coefficient accounting, and the supported quotient roles while preserving the operation and rejecting undefined denominators. The examples do not establish broad random-sampling or shortcut coverage.
