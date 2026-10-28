# Group 3 linear algebra audit

Captured basis: **9047**. All work is staged; this folder performed no live transactions or production-file edits.

Integration payloads:

- `proposals.json`: 73 exact formatting replacements (9 tutorial fields, 34 problems, 30 worked solutions).
- `completion-solutions.json`: 22 independently authored missing worked solutions.
- `missing-key-completions.json`: 23 missing canonical links to existing answers owned by the same field. Existing solution q-20966 is preserved.
- `generator-candidates.json`: staged KP 17592186100873 package descriptor. `generator-proposals.json` records before/after hashes. `generator-17592186100873/` preserves source data and adds source selection focus to fresh selected-entry solutions.

The parent-owned flagged entities, existing KP 17592186100872 solutions, and q-318413 HTML answer table are excluded. The two baseline KP 17592186100872 missing solutions (q-1029 and q-1034) are included as independently authored completions.

Read `validation-report.json` and `coverage.json` for counts and limits. `snapshot.json` retains every assigned question and explicit membership at the captured basis. `fields.json` contains all 5,416 unique content, solution, choice, and feedback fields. All passed structural validation and actual-renderer checks. The 95 proposed content fields also render; all 19 changed interactive matrix layouts preserve keys and control IDs and pass mobile overflow checks. Representative original SVG and proposed screenshots are in `source-screens/` and `proposed-screens/`.

`source-comparisons.json` records 1,579 source formula comparisons. The original source survives for 380 questions and all 23 tutorials. `missing-sources.json` explicitly lists 201 source-identified questions without retained originals; 198 generated questions have no original-source identity. `source-bank-validation.json` checks 697 complete captured banks across 302 questions: 505 normalized exact matches, 22 equivalent matrix-divider/Unicode-domain forms, and 170 comparisons whose response representation had already changed (for example radio subsets migrated to checkbox fields).

`intermediate-matrix-validation.json` independently verifies 425 numeric augmented matrices in 97 Gaussian elimination chains across the 188 questions in source topics 1733 and 1374. All are row equivalent; no numeric matrix was skipped. `product-math-validation.json` verifies all 46 selected-entry and outer-product questions, including canonical examples. These checks do not constitute an independent proof of every determinant/inverse intermediate in the full group.

`grading.json` checks all current or completed owned canonical fields: 1,182 accepted and 2,819 rejected responses, no failures. `generator-validation.json` samples 144 records across supported difficulty bands of all 17 registered packages. Twelve fresh staged selected-entry records are additionally checked mathematically. `generator-grading.json` reports 268 accepted and 574 rejected responses without failures; `generator-render-validation.json` checks all 1,139 generated content/answer fields. `staged-generator-validation.json` verifies exact complete-source replay for all 10 source questions with a retained solution, plus unchanged source-data bytes. The two original selected-entry questions without solutions synthesize a newly focused solution.

Source e-4722 contains two original MathML error nodes; its existing E2 E1 A solution is correct and renders, so those source errors are not propagated. KP 17592186100913 advertises moderate/hard CLI arguments although fresh generation supports only easy; unsupported bands are not counted as failures. KP 17592186184172 supports moderate/hard rather than easy. Initial sample invocations without `--format json` were corrected; the final sample report uses the actual supported JSON protocol.

Some coefficient-matrix repairs change textual placeholder traversal order because coefficient and right-hand-side brackets are separate groups. Field entities, keys, answer banks, and original matrix-cell positions are preserved; compare placeholder multisets.

## Final aligned-bracket UI regression and package refresh

`aligned-guard-regression.json` exercises the actual UI renderer, `ui/math-protection.js`, and vendored SVG MathJax. Both minimal visible `[A | I_3]` labels and original tutorial 3170 (entity 17592186116501, from group 2) retain A, I, brackets, and the vertical bar. Direct unguarded MathJax silently renders only `= B`. Screens are in `aligned-guard-screens/`. Genuine `[t]`, `[b]`, and `[c]` options remain byte-for-byte unchanged and produce MathJax alignments `baseline 1`, `baseline -1`, and `axis`, respectively. No MathJax errors occurred.

`aligned-leading-bracket-scan.json` scans all 5,438 group 3 fields after merging the exact after-values reported committed at T9071 with the captured baseline. It finds **zero** affected entity IDs.

The staged KP873 package now contains the latest `scripts/question_capture/math_format.py`, including the new normalization guards. `generator-candidates.json` includes the complete publication descriptor and approved digest `0bb7250591b2ca521fbab7a0201654c5f7dd325cbd74ada055fdca171c88f1e6`. Twelve fresh staged samples, all ten complete source replays, 842 native grading checks, and all 1,139 generated render fields were rerun successfully after the helper refresh. Complete source replay JSON and raw source-data bytes remain unchanged; no source normalization differences appeared. `staged-helper-refresh.json` records the helper hashes.

## Checkbox statement-label coverage

The initial 5,416-field inventory omitted statement text stored in `answer-field/key`. This gap is now closed independently at current basis **9085**. `checkbox-labels-current.json` explicitly reads all **476** checkbox labels across 139 questions. All labels passed syntax checks and rendered through the actual `checkboxControl`, Markdown protection, and vendored MathJax. Every control retained its field ID and Boolean answer identity.

`checkbox-label-proposals.json` contains **22 key-only corrections**: 14 recover mathematical notation from retained original statements; eight are explicitly **authored notation repairs**, supported by original statement templates or sibling statements, for six source-gap vector labels and two generated dimension labels. They restore bold vector names, six visible Span set-brace pairs, and blackboard real-space notation. No values, predicates, field order, choices, correct links, or learner history change. Before/after numeric sequences are identical and no label collisions arise. `checkbox-label-source-comparison.json` retains per-field source evidence; 248 labels have retained originals, 18 source-identified labels lack direct originals, and 210 labels belong to generated questions. After the six supported source-gap repairs, 12 labels remain explicitly without direct originals; they have no identified formatting defect.

`checkbox-label-render-validation.json` checks all 476 current controls and all 22 proposed controls. `checkbox-label-grading.json` verifies 476 accepted and 476 rejected Boolean responses with no failures. Coverage and limitations are in `checkbox-label-validation-report.json`, `checkbox-label-coverage.json`, and `checkbox-label-source-gaps.json`; before/after screenshots are in `checkbox-label-screens/`.

The owning source templates reproduce the lost real-space notation in KP **17592186184172**. `generator-17592186184172-labels/` stages the narrow fix before decision application and identity creation, bumps version 1.1.1 to 1.1.2, and includes the latest shared formatter. The same correction also reaches generated statement copies in prompts and explanations. Raw `source-current.json` is unchanged. `checkbox-generator-candidates.json` is a **separate** publication descriptor from the already published KP873 candidate; approved digest is `2f470ad55708ce92230912b6f2071e3666ba4ea64892e3455d13696812281675`. All 15 original template families were exercised with fresh parameters; 24 generated checkbox labels and all 137 generated content fields render. Native grading passes 31 accepted and 52 rejected responses, and before/after canonical values agree. The other owning KP, 17592186119845, has no registered generator.
