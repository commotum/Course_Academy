# Prepared position-vector LaTeX repairs

Prepared **295 existing string-field replacements** for topic **17592186048780** (MA **1106**) from the audit snapshots at math basis **11863**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. **No EDB writes were performed.** Root can refresh and submit these before/after values under CAS.

The batch contains **102 prompts, 103 worked solutions, and 90 authored answer values**. It resolves the entire 298-field candidate set: **295 fields changed**, while **3 scalar-only answer choices** were false positives and remain unchanged (**17592186572323**, **17592186572348**, **17592186572467**). [unresolved.json](unresolved.json) is empty.

Changes are confined to math spans:

- Replace 14 pseudo-accent occurrences in 11 fields, including `OR^(→)` → `\overrightarrow{OR}` and `PQ^(―)` → `\overline{PQ}`. The existing text in incomplete question **17592186097240** is corrected; absent fields remain absent.
- Restore bold typography for named vectors, including the partially degraded aligned displays in canonical examples **17592186096451** and **17592186096452**. Scalar parameters `\lambda` and `\mu`, numeric coefficients, and uppercase point labels remain unchanged.
- Replace the fixed horizontal glyph `\overset{―}{XY}` with a properly spanning `\overline{XY}` in **33 prompts**. These fields also receive vector-font corrections.

Evidence is explicit about its strength. **241 fields across 87 question/example entities** have retained original MathML evidence identifying the bold vector symbols. This proves symbol roles and typography; it does not claim the entire current field exactly matches a single old source version. Normalized prompt/solution match flags and source file hashes are retained in [source-proofs.json](source-proofs.json); original bold MathML nodes are retained in [source-mathml-proofs.json](source-mathml-proofs.json).

The remaining **54 fields across 17 entities** are verified through their defining vector equalities and labeled arrow diagrams, rather than claimed exact source-text matches. Ratio questions explicitly define lowercase symbols as origin-to-point vectors. Grid questions combine the arrow-labeled vectors using scalar `\lambda`/`\mu`. Those vector roles are unambiguous, and uppercase point labels and scalar parameters are excluded. The inspected contact sheet is [remaining-source-diagrams.png](remaining-source-diagrams.png). Each replacement records its individual role/diagram evidence.

All **295 proposed fields pass the current strict actual-player renderer and structural math validator**, with **zero failures**: [strict-render-results.json](strict-render-results.json). The preparation script reverses only the approved font/accent changes and asserts that every other character matches the original. Prose, images, ratios, fractions, real minus signs, algebraic values, and existing answer identities are preserved. Representative corrected arrow choices, canonical displays, ratio bars, and role-verified variants were visually inspected in [visual/](visual/).

Missing solutions and answer keys remain missing. Duplicate answer-field structures remain unchanged. No learner-entered response history is included. No source-inherited mathematical claim was edited. Shared importer/validator changes are owned by root; this directory introduces none.

Submission payload: [changes.json](changes.json). Counts: [summary.json](summary.json). Reproducible field preparation: [prepare_changes.py](prepare_changes.py).
