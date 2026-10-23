Committed to `math` at **T5664** (`13194139538976`) with source `:agent/codex`.

The repair replaced **6,919 formula-image occurrences** across **1,973 fields on 1,526 entities**: 716 question problems, 665 worked solutions, and 592 tutorial bodies. It recovered 5,494 distinct assets (4,754 SVG and 740 PNG). All 428 genuine image references in those fields were preserved, together with every byte outside the replaced image spans. Entity identities, lesson/KP/question/answer/choice links, activity structure, generators, learner responses and progress were unchanged.

[Verification](verification.json) confirms exact readback of all 1,973 values at the committed basis. The [global scan](global-post-repair-scan.json) examined 2,720,814 exported facts, including 1,368,170 textual values, and found **zero remaining formula-image references** and zero unresolved image assets. One diagram introduced since the original audit was independently reviewed and retained as a genuine coordinate-region graphic.

The [transaction](transaction.edn) contains only scalar compare-and-swap operations, each guarded by its exact original content. The [persisted request](commit-intent.json), [receipt](receipt.edn), [preapply check](preapply-check.json), and [exact saved values](after.edn) record submission and outcome. The transaction SHA-256 is `3e04faa92dfc3df7891239e74f84394e6d244887be00febdb3e264f8d9cc3d02`; its stable request key is `repair-math-images-2026-10-22-3e04faa92dfc3df7891239e7`.

Recovery used the intact formula data rather than whole-field rollback:

- 3,020 formulas came from embedded TeX/MathML titles.
- 1,930 matched retained or archived TeX by rendered glyphs and mathematical structure.
- 530 were reconstructed from retained MathJax semantic SVG trees and checked by rendering back to the source structure.
- 11 required removal of capture-only title wrappers/comments.
- Three damaged Gauss–Jordan titles were recovered from their intact rendered displays. Their matrices and row operations were checked independently; see [source displays](review/) and [row-operation verification](matrix-row-operation-verification.json).

The [asset checks](asset-validation.json) validated every selected formula in the installed player. They compare fractions, roots, scripts, limits, matrix cells, foreground colors and background highlighting where a semantic SVG is available, and reject rendering errors and undefined commands. Currency-marker repairs were independently checked against dollar glyphs in the intact SVG drawing. Unsupported `boldsymbol`, hyperbolic operator names and HTML color-model syntax were expressed using forms supported by the installed player.

[Complete-field validation](field-render-verification.json) exercised the actual Markdown protection, sanitization and MathJax pipeline for all 1,973 fields. It confirmed exactly 6,919 additional math expressions, no new undefined commands or MathJax errors, and no page errors. The original example `17592186092122` was visually inspected at [desktop](review/example-731-desktop.png) and [mobile](review/example-731-mobile.png) widths. One pre-existing `Missing \\end{aligned}` error in tutorial `17592186148781` occurs in existing textual math outside the replaced image; that unrelated text remains unchanged and is recorded in the validation report.

The [original audit](../../audits/2026-10-22-math-images/README.md) contains the import lineage and reproductions. Both DOM extractors accepted a MathJax SVG without locally recoverable TeX/MathML as an image asset with an empty error list. Older capture code rasterized that asset; newer capture code saved its SVG. The newer-source import selected the latest successful capture without considering whether it had degraded existing textual math to images. Thus good LaTeX could be overwritten first by PNG and later by SVG. This transaction repairs the stored content; it does not change that capture/import selection code.

The reproducible recovery and application scripts are retained here. Large immutable input exports, original SVG capture bytes and the candidate-render cache remain under ignored `.local/edb/math-image-import-audit-2026-10-22/`. `prepare.py` refuses to regenerate an intent once the commit journal exists; `apply.py` reconciles an uncertain submission using its exact persisted payload and key.
