# Group 3 review — prepared at EDB basis 11639

Prepared **490 guarded attribute replacements/additions and one separate ownership-edge retraction**. No EDB transaction, publication, learner attempt, or installed-generator mutation was performed.

The scope is six topics, 20 KPs, **323 questions/examples**, 12 tutorials, and 32 ordered lesson steps. Every question has an individual row in `review-ledger.json`. All 299 source-identified questions/examples have archived evidence, including `.exampleExplanation` canonical solutions and hashed historical captures. The remaining 24 are authored/generated questions with no Math Academy source ID; their complete prompts, solutions, fields, and choices were checked independently.

## Prepared corrections

- Complete 14 missing worked solutions and 18 missing correct links, reusing existing field-owned answers. `completion-evidence.json` records independent derivations and distinguishes local authorship from observed source content.
- Restore the three corrupted cross-product prompts q-19763/q-19769/q-19775, whose archived × operators had become dot products.
- Restore q-181442's complete set-builder response skeleton and five owned keys from its original dashed rectangle: real pairs with `1<x<5`, `2<y<4`.
- Correct source mathematics for q-33160: require a plane through C parallel to **the plane determined by the two distinct parallel lines**. This supplies the missing direction constraint and leaves exactly one correct existing choice. Correct the reversed scalar relation in its explanation. The original weaker wording admitted two choices.
- Correct q-280352's two-component cross-product outputs by embedding them in R³ with fixed zero third coordinates. Its two existing blank values and identities remain unchanged. `authored-math-proof.json` includes simultaneous concrete vectors realizing both supplied cross products.
- Require a nonempty subset in the tutorial subspace test; specify right-hand-rule orientation in the cross-product definition. Correct exterior-ellipse explanatory wording that mislabeled an exterior test point as outside the shaded region.
- Restore archived vector/blackboard fonts, colors, boxes, determinant fences, visible set braces, and complete checkbox statements. Source restoration is based on matching complete formula fragments after removing presentation differences, with per-change source paths. Mathematical corrections are separately evidenced.
- Wrap long set/line formulas at mathematical boundaries to avoid demonstrated clipping at 320 px. Source symbols, scalar values, diagrams, field IDs, option banks, and existing valid answer values are preserved.

`proposals.json` contains 223 `question/problem`, 211 `question/worked-solution`, 32 checkbox `answer-field/key` presentation changes, 18 `answer-field/correct`, and 6 `tutorial/content` changes. No existing answer value, UUID, answer bank, difficulty, or field type is changed.

For q-32988 (`17592186120218`), the original lesson has **one radio widget**. Keep active field `17592186390835`, already correctly keyed to `17592186390839`. Retract only the duplicate ownership edge to old field `17592186117469`; retain that field and its five answers as entities. The parent has separately proved zero retained learner usage of the old field/answers. This retraction is in `topology-proposals.json` and is projected into the final controls/grader fixtures. No missing-key assertion is proposed for the detached duplicate.

## Verification

| Check | Result |
|---|---|
| Individual content/math ledger | 323/323 |
| Plane checks | 182/182; exact point incidence, nonzero normal, independent directions, complete-plane equivalence, canonical solutions, and every radio/select choice |
| Cross-product checks | 47/47; independent ordered bilinear expansions, canonical solutions, response signs/coordinates, every choice |
| Geometric interpretation/regions | 94/94; independent set/diagram conclusions and domains |
| Diagram review | 76 complete question panels across nine contact sheets; unchanged asset paths |
| Closed numeric solution-chain checks | 75 equalities checked; zero failures |
| Tutorial/step review | 12 tutorials and all 32 source-ordered steps; exact content identities |
| Native grader, final staged questions | 303 gradable questions; 534 accepted and 1,397 rejected checks; zero unresolved |
| Additional equivalent scalar entries | 4 accepted, 2 rejected checks |
| Strict actual-player math rendering | 2,554 fields; zero errors, raw display delimiters, or matrix-layout failures |
| Actual-player controls | 323 prompts × 3 widths (760/390/320) × 3 feedback modes = 2,907 cases; exact blank-editor counts; zero math errors or horizontal/content overflows |
| Identity/bank integrity | All 323 pass; original valid keys, answer IDs/values/banks, UUIDs and diagram paths preserved; all active fields keyed and uniquely named |

The native entry point is `course_academy_engine::learning::grade_field`, exercised by the existing in-memory `../2026-10-28-topic-audit-3/check-engine` fixture runner. Browser checks use the repository's actual player rendering/control functions, MathJax, MathLive, and CSS. No learner writes are used for grading or rendering.

## Registered generators

Both cross-product packages were inspected and tested from their registered immutable locations and copied relocation directories. **512 generated records** cover easy, moderate, hard, and unclassified bands, two seeds, all supported response/profile families, and matching relocated output for every band at seed 17. Independent algebra confirms ordered × operators, three-dimensional vectors, fixed component skeletons, correct unique option banks, and correct scalar answers.

Generator native checks: **1,000 accepted / 1,804 rejected**, zero unresolved. Generator strict actual-player rendering: **3,096 fields**, zero failures. Package file SHA-256s match the installed manifests. No confirmed generator defect was found, so no successor package or generator update is staged. `generator-verification.json` records paths, hashes, sample parameters, exact derivations, and relocation results.

## Handoff and limits

The parent should integrate `proposals.json` with guarded CAS at the captured basis, apply the separately guarded duplicate-edge retraction, and perform committed readback/publication verification. This package is **prepared and validated**, not committed or published.

All source-identified records were compared against available local archives; generated records are explicitly marked as such. The numeric-chain checker covers its supported closed-expression forms and supplements, rather than substitutes for, the per-question mathematical/visual review. Native grading establishes application acceptance/rejection, while independent proofs establish mathematical correctness. No claims are made about topics outside this group or about learner history beyond the parent's explicit duplicate-usage proof.

To reproduce preparation, run `restore_source.py`, `complete_questions.py`, `layout_repairs.py`, `tutorial_repairs.py`, `finalize.py`, `narrow_layout.py`, and `prepare_checks.py` in that order. The saved final proposal/fixture hashes in `handoff.json` identify the reviewed result. Validation scripts and full results are retained alongside the individual evidence files.
