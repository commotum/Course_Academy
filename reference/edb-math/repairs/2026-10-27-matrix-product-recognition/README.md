# Remove matrix-multiplication hints — 2026-10-27

Deployed at EDB T8909 and verified live at T8910.

KP `17592186059747` — Multiplying 3x3 Square Matrices. Topic `17592186048297` — Multiplying Square Matrices.

The registered v1.0.0 generator added two forms of assistance to every easy question: a row/column process reminder and the fully selected dot product for one requested entry. These appeared in question `17592186695793` and four other active generated questions.

## Evidence and scope

Of the 12 imported 3×3 questions, four (`q-318332`, `q-318338`, `q-318339`, `q-318328`) provide partial output matrices and request five entries. None supplies an entry's dot-product setup or an additional process reminder in its prompt. Their partial-matrix format supports reducing repeated calculations while retaining row/column selection for each requested entry.

Version 1.1.0 removes both added hints. Partial output matrices remain. The complete procedure, expanded calculations and final product remain in worked solutions. This repair preserves the existing numerical ranges, sparsity and three/five/nine requested-entry progression; it does not claim that this progression has been empirically calibrated or perform a broader difficulty redesign.

The separate identity-matrix question `17592186385986` is imported (`q-1021`) under the 2×2 KP and is unchanged.

## Publication

Registered package: `generators/a9/a94cca56f1b193b678022a4709a73ce0ff52a720feb0959cc58c53f05ff54a85/generator.py`.

Retired the five hinted versions from future practice: `17592186695558`, `17592186695774`, `17592186695777`, `17592186695793`, `17592186695797`.

Published five unused easy questions: `17592186725453`, `17592186725441`, `17592186725439`, `17592186725451`, `17592186725467`. Three retain the exact operands and requested positions of unused old questions; two introduce fresh instances rather than repeating the calculations of the two already-used questions. One older exemplar uses the current matrix layout in its replacement.

The 12 imported questions, canonical example, 11 unhinted moderate/hard generated records, existing question/field/answer content and learner history are preserved. Saved attempts retain their original question wording. Readback uses the publication snapshot, including learner responses saved between initial investigation and publication.

## Verification and recurrence prevention

- Independently reconstructed matrix products from displayed operands for five replacements and 180 fresh samples across all three levels. Every supplied entry, requested entry and worked final matrix matched.
- Reproduced fresh samples exactly through the relocated immutable package CLI for all three levels.
- Native grading: 30 accepted, 15 rejected, zero unresolved checks. Equivalent integer/decimal entries are accepted.
- Live grading: all 45 checks passed, with the other fields held correct while exercising each individual field. No learner-state writes were made by verification.
- All five replacements passed actual learning-UI rendering checks. Screenshots 002 and 005 were visually inspected.
- 54 focused tests passed: matrix prompt policy, publisher and generator package tests. Negative controls cover the original question, the process reminder alone and an expanded calculation alone. Target-position descriptions and partial matrices remain allowed.
- The generator and publisher both reject these hints in ordinary 3×3 practice. Author/reviewer prompts now distinguish supported partial matrices from procedural help. The service was reloaded to apply the publication guard.

Reproduce with `.venv/bin/python reference/edb-math/repairs/2026-10-27-matrix-product-recognition/check.py` and `.venv/bin/python -m unittest tests.test_matrix_product_prompt_policy tests.test_generator_publish tests.test_generator_packages -q`.

Evidence: `before.json`, `capture.json`, `fresh-source/`, `corrected-examples.json`, `replacement-inputs.json`, `candidate-pool.json`, `generator-verification.json`, `grader-verification.json`, `render/`, `publication/`, `verification.json`, `live-grading-verification.json`, `completion.json`. `deploy.py` retains the exact request and supports recovery without creating another question batch.
