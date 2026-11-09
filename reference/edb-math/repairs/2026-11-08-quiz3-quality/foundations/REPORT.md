# Foundations quality audit and committed repairs

Completed the six assigned topics. The frozen starting database basis was **13537**. The authorized content transaction committed at **13540**, with request key `quiz3-foundations-quality-f963320d9404427bab03cb30` and no allocated entity IDs.

| Topic | Tutorials | Steps | Canonical examples | Practice questions | Scalar attributes repaired | Grader checks |
|---|---:|---:|---:|---:|---:|---:|
| Euler's Formula (17592186048535) | 2 | 4 | 2 | 32 | 38 | 160 |
| Differential Operators (17592186048202) | 4 | 7 | 3 | 38 | 13 | 190 |
| Linear Differential Operators (17592186050537) | 3 | 6 | 3 | 30 | 21 | 154 |
| Introduction to Second-Order Linear ODEs (17592186050677) | 5 | 9 | 4 | 42 | 20 | 184 |
| Linear Dependence and Independence (17592186050426) | 4 | 7 | 3 | 73 | 162 | 363 |
| Linear Independence in Abstract Vector Spaces (17592186048257) | 2 | 5 | 3 | 45 | 104 | 209 |
| Total | **20** | **38** | **18** | **260** | **358** | **1260** |

All six routes are complete and acyclic and agree with saved source order. The abstract vector-space lesson's old snapshot has different step IDs; its ordered tutorial/KP titles agree exactly with the current chain. No route changes were needed.

The audit covered every tutorial, canonical example, and practice question, including all owned fields, choices, keys, stored solutions, source DOM roles, vector/scalar notation, images, and rendered controls. Complete Pull exports, original DOM manifests, re-extraction results, and before/after fields are retained under each topic folder. Twenty-nine locally authored questions in the vector-dependence bank were included; they intentionally have no Math Academy source ID.

## Defects repaired

- Completed nine missing solutions and their missing canonical keys: three Differential Operators questions, four Linear Differential Operators questions, and two second-order ODE questions. `completion-templates.json` records these as locally authored derivations using the owning KP's canonical examples, not observed Math Academy solutions.
- Corrected six wrong keys across three full linear-operator proof questions (`q-337728`, `q-337739`, `q-338094`). The linearity-condition fields had been keyed to the later nonlinearity inequality; derivative-expansion fields had been keyed to the later text conclusion `nonlinear`. Saved original banks confirm cross-stage contamination. Detached six alien active choice links while retaining every answer entity.
- Removed two duplicate legacy active field links from homogeneous/inhomogeneous question `q-337919`, preserving those field entities and their answers. The three complete source-aligned fields remain active.
- Removed fifteen duplicate active choice links from five three-field homogeneity questions and restored their fifteen surviving prose labels to the installed text answer type. All original entity IDs remain available.
- Repaired the first-stage-only `q-337675` prompt, which exposed its answer next to the select. Its saved original contains only the first dynamic proof stage, so that captured field and original bank were retained; the prompt now binds the select correctly and the complete operator-specific solution is authored explicitly.
- Corrected two mathematical typos in stored solutions: `q-130252` began by applying the operator to `cos(2x)` despite its given input `sin²(x)`; `q-130305` used `a x² y₂` instead of `b x² y₂` in a linearity expansion.
- Restored source-confirmed vector/zero notation and visible set braces in legacy extracted formulas and checkbox labels. Scalar coefficients and numerical matrix entries remain scalars. Applied the existing shared normalizer for operator notation and scalable math, preserving data-table roles. Removed the literal empty-bold `****` from the Euler tutorial's table header.

The transaction contains **358 cardinality-one CAS changes and 23 narrow membership retractions** (21 duplicate/alien choice links and two legacy field links). No `retractEntity` is used. The content transaction altered 137 question records/owned fields and two tutorials. Installed question, answer-field, answer, and tutorial specs passed native preview. All changed attributes have exact readback matches at receipt basis 13540.

## Validation

- `exact-mathematics.json` and `remaining-mathematics.json`: all **278** distinct canonical/practice questions covered. Checks independently derive differential-operator results, matrix ranks and nullspaces, polynomial coefficient relations, all classification truths, ODE homogeneity and IVP conditions, and Euler radii/angles. Every option is checked for equivalent mathematical correctness where applicable. Abstract qualitative statements and canonical proofs were also reviewed against their complete source and solution arguments.
- All **16 Argand assets** were opened together and their plotted coordinates independently recorded before checking every Euler answer. See `euler-argand-contact.png`.
- `grading-checks.json`: **1,260** actual application preview checks, **zero failures**, all at basis 13540. Every one of the 260 practice questions accepts its full canonical response, and every alternative active option is rejected with the other fields held correct. Preview grading created no learner attempts.
- `strict-after.json`: **2,331** tutorial/problem/solution/checkbox-label/answer fields passed strict actual-player MathJax rendering; math answer values were rendered as bare math. Zero undefined commands, math-structure failures, matrix-layout failures, or short matrix fences were found.
- `layout-report.json`: **596** desktop/mobile layouts (all 278 question prompts and 20 tutorials at 1100 and 390 pixels), using the actual player `fieldControl` and inline-field mounting. Zero missing/duplicate controls, visible unresolved field markers, math errors, or unloaded assets. Representative screenshots are in `visual/`.
- `verification.json`: all 358 scalar values match the commit; all receipt datoms are confined to question/answer-field/answer/tutorial namespaces plus the database transaction timestamp. No learner or other protected namespace was changed; no entity IDs were allocated. None of the detached answer choices was referenced by a saved learner response (`learner-answer-references.json`).

## Source limits

Saved original prompt DOM was found for **247 of the 249 Math Academy identified questions/examples**. The two unavailable originals are Differential Operators `q-338002` and `q-338188`; their complete stored prompts, solutions, and banks were independently checked from their givens and all choices, with no mathematical defect found. The 29 locally authored questions have no remote originals by design. Some original solution captures are absent, including the nine repaired stubs; authored completions are identified as such. The later dynamic proof stages of `q-337675` are not claimed to have been recovered verbatim. These evidence limits leave no unresolved active content, grading, binding, or rendering defect in the audited banks.

Authoritative transaction artifacts: `transaction.edn`, `commit-intent.json`, `preview.edn`, `receipt.edn`, `verification.json`. Source inventories/comparisons and repair logic are saved alongside them for reproducibility.
