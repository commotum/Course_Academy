# q-130788: fixed-height augmented-matrix brackets

Question17592186551286 belongs to topic17592186050576 (Elementary2x2Matrices), KP17592186115244. It was included in the October27 linear algebra audit. It was not in the later October28 list of99topics.

The current stored worked solution uses `[\begin{array}{cc|cc}...\end{array}]` twice. Literal brackets have their normal fixed height. The enclosed matrix is roughly47–50px tall, while its brackets are18px tall. This reproduces the reported screenshot with the actual player renderer. Both the defective and corrected versions report zero TeX errors.

Changing only those two delimiter pairs to `\left[...\right]` repairs the visible bracket height with identical UI/CSS. The column rule, all entries, row operation, answer key and mathematical result remain unchanged. This is a stored-formatting defect, not a new UI clipping issue.

## How the audits missed it

1. The October24 MathML-table repair (T6326) recovered the augmented array and central column rule but retained literal bracket fences.
2. The October26 matrix-layout repair (T8500) handled fenced `aligned` and `matrix` environments. Its saved proposal for this exact question converted the final inverse to `bmatrix`, but left both augmented `array` expressions unchanged. The saved grid verification checked only that converted final matrix.
3. The October27 lesson audit (T9092) added an empty group after the outer `aligned` opening so MathJax would stop swallowing the visible `[N|I]` label as an optional positioning argument. It did not repair the two array fences. The saved rendering results for this question explicitly show zero errors and no leaked dollar delimiters.
4. The shared `validate_matrix_layouts` guard only checks the `aligned`/`matrix` conversion function. It currently accepts this exact defective solution. `normalize_tex` already knows how to make these array fences scalable, but that separate normalization was not applied by the reviewed repair/validation path. Syntax success was therefore mistaken for sufficient visual-layout coverage.

No database changes were made during this investigation. `preview.json` contains the narrow candidate change; `before.png`, `after.png` and `render-proof.json` reproduce the failure and correction without changing UI code. Future validation needs explicit fixed-fence/array geometry coverage in addition to syntax checks.

The paragraphs above describe the initial diagnostic state. The authorized repair subsequently committed at T11477, followed by database-wide repairs and generator prevention. See the [completed repair report](../2026-10-29-array-fences/REPORT.md) for final counts and verification.
