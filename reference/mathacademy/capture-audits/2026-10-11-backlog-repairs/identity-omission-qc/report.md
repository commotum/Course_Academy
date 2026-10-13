# Identity omission QC and one finite source repair

The inspected inventory contained 55 identity omissions in 13 packages: the previously reported 48 and seven new omissions in linear task 14122959. Every omitted record was explicitly quarantined as `unreconciled:*`, retained an observed permanent question ID, and had one consistent question number across its own original control IDs. Forty-six records also had a stable `step-qN` root; nine used the diagnostic `questionContainer` root. No inspected record had conflicting or unbound control IDs, fresh extraction errors, or incomplete fresh controls.

The omission message did not mean that the original source lacked an ID. Most quarantines were caused by older history extraction omitting the authored `.questionBody` portion of the prompt. Pure offline re-extraction with the current shared extractor established strict problem and typed-control equality for 53 of the 55 records. This used the existing source comparator and transferred no grades. No identity or mathematical comparison rule was weakened.

| Account | Task | Records | Strict fresh matches |
| --- | --- | ---: | ---: |
| multivariable | 14121715 | 5 | 5 |
| differential | 14117039 | 6 | 6 |
| linear | 14117285 | 3 | 3 |
| foundations | 14116619 | 4 | 4 |
| multivariable | 14111253 | 9 | 7 |
| linear | 14122959 | 7 | 7 |
| linear | 14116776 | 3 | 3 |
| linear | 14118157 | 2 | 2 |
| linear | 14121140 | 7 | 7 |
| linear | 14119271 | 5 | 5 |
| multivariable | 14121869 | 1 | 1 |
| multivariable | 14121047 | 1 | 1 |
| multivariable | 14120884 | 2 | 2 |

The remaining two are separate authored-source differences. q331821's live original literally concatenates `below.By`, whereas history has a paragraph boundary. q37456 has a source TeX difference and history exposes no radio choices. Their own permanent control IDs are consistent, but those facts alone cannot authorize history grades or relax source comparisons. The archive repair agent owns their independent source reconstruction.

Exact owning IDs, source keys, original file hashes, every observed control ID, scoped failures, and live/history comparison results are retained in `inspection.json` and `fresh-extraction.json`. Other package files were only read during this QC.

Only newly assigned linear 14122959 was repaired by this agent. `repair_linear_14122959.py` imports the established archived driver, filters solver payloads to authored problem/solution/choices/diagrams, and uses configured `gpt-6.1-sol` with high reasoning. Preparation produced 15 supported questions and three canonical examples with zero gaps or limitations. Normal DatabasePipeline preview, commit, and pinned readback verified the repair; the subsequent preview returned `no_changes` at basis 1070 with no omissions. `linear-14122959-prepared.json` and `linear-14122959-applied.json` retain results and protected original hashes.

The original checkpoint, capture-complete record, and retakes file were hash-checked unchanged. Preparation also checked unchanged content/history-content files. No learner checkpoint or ledger mutation path was invoked. The initial wrapper mistakenly looked for `xp-ledger.json`; consequently it did not establish before/after byte equality for the actual `xp.json` and `daily-xp.json` files. The wrapper now names those correctly for future executions; no retrospective hash assertion was invented. Native commit guards cover learner/engine database facts separately.
