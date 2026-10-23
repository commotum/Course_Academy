Read-only diagnosis of inline/display math in `math` at **T5759**. The database and production importer/renderer code were not changed.

**The reported discrepancy is reproducible source-style loss during import.** The saved DOM for `q-349253` (`17592186319332`) contains an inline MathJax container whose assistive MathML wraps the entire integral in `<mstyle displaystyle="true" scriptlevel="0">`. The capture converter flattens that `mstyle` to its children, discarding its attributes. Since the outer container lacks `display="true"`, the converter emits ordinary `$...$` delimiters with no `\displaystyle`. The saved DOM for `q-114289` (`17592186250225`) demonstrates the same behavior for an indefinite integral.

Replaying those exact DOMs through both extractors reproduces the stored bad prompts, with **empty error lists**. The good `e-491` example (`17592186064099`) takes the SVG-title path, where the original TeX title explicitly contains `\displaystyle`; that command survives. [Reproduction results](reproduction.json) include exact outputs, source paths and code hashes; [reproduce.py](reproduce.py) performs the offline replay and controlled-fixture assertions.

The relevant production code is [the active MathML flattener](../../../../capture/scripts/browser/extract.js:292), its [display-delimiter decision](../../../../capture/scripts/browser/extract.js:334), and the corresponding legacy logic in [dom.js](../../../../scripts/question_capture/dom.js:364). A controlled fixture also proves that a directly encountered `<math display="block">` becomes inline because the delimiter decision only recognizes the string `"true"`. That additional bug is demonstrated separately; it is not asserted to explain every inventory entry.

The [shared prose normalizer](../../../../scripts/question_capture/math_format.py:545) preserves the existing delimiter choice and has no policy that promotes standalone integral equations to display blocks. Thus later normalization does not recover the lost style or improve block placement. The player then renders the stored delimiters and TeX as supplied.

There are two distinct formatting properties. `\displaystyle` controls mathematical sizing; `$$...$$` also establishes a separate equation block. All three supplied good prompts are still inline `$\displaystyle ...$` expressions. The source also intentionally places some full-size integrals inside prose. Making almost all substantive integrals separate display equations is an additional layout rule beyond restoring source style.

[Lineage for all nine supplied IDs](supplied-example-lineage.json) confirms that the six problematic prompts lack `\displaystyle` at their earliest retained assertions: T86 for `17592186250225` and `17592186250233`, T110 for `17592186319332`, and T3862 for `17592186582344`, `17592186582346` and `17592186582385`. Their problem fields were not changed by the previous formula-image repair at T5664. The three good prompts retain `\displaystyle` from their earliest retained assertions. All nine belong to Introduction to Integration by Parts, topic 317.

The global scan examined 2,722,256 exported facts. In question problems, worked solutions, tutorial bodies and multipart context, it identified:

| Formatting category | Integral occurrences |
|---|---:|
| Inline, without `\displaystyle`, already on a standalone line | 1,563 |
| Inline, without `\displaystyle`, embedded in prose/layout | 3,594 |
| Inline, with `\displaystyle`, already on a standalone line | 92 |
| Inline, with `\displaystyle`, embedded in prose/layout | 829 |
| Total | 6,078 |

The 5,157 occurrences without an explicit display-style command span **3,995 fields, 3,786 entities and 132 topics**. The clearest block-promotion group—the 1,563 unstyled integrals already on standalone lines—spans **1,496 entities and 85 topics**. All inline-integral categories together span 158 topics.

These are lexical formatting candidates, not a claim that all 5,157 expressions should receive an identical replacement. Scope matters: an inner `\displaystyle` may not govern the integral, a prose reference may reasonably stay inline, and HTML answer tables require their layout to be preserved. Bare TeX answer values have a different schema/rendering contract and are excluded from the primary prose totals.

Representative additional cases include:

| Entity | Content | Lesson | Observation |
|---|---|---|---|
| `17592186064480` | Question problem | Integrating Algebraic Functions Using Substitution | The complete integral equation is stored as a single-dollar expression. |
| `17592186064538` | Question problem | Integration Using Inverse Trigonometric Functions | A radical/fraction integrand is an unstyled inline equation. |
| `17592186069382` | Question problem | Integrating Rational Functions Using Partial Fractions | A bounded integral occupies its own line but uses inline math. |
| `17592186078742` | Question problem | Definite Integrals of Piecewise Functions | The integral below a graph is on its own line but remains inline math. |
| `17592186055964` | Tutorial content | The Arithmetic of Functions | A four-row `aligned` derivation uses single-dollar delimiters. |
| `17592186059976` | Question problem | Systems of Equations as Augmented Matrices | A three-equation system on its own line uses inline delimiters. |

The broader scan collected **11,983 prose fields** with non-integral review candidates: large operators/limits, multiline environments or matrices, and long fraction/radical expressions. This broader list is intentionally less certain. Some compact matrices and layout wrappers are suitable as authored, and some old entries also have mathematical-conversion damage that must be handled separately from delimiter changes. It must not be applied as a blind rewrite.

The complete inventories are [prioritized integral occurrences (CSV)](prioritized-integral-occurrences.csv), [per-field integral candidates](inline-integrals.json), [other display candidates](other-display-candidates.json), and [summary counts](summary.json). Entity/attribute keys, current transaction/source, occurrence offsets, ownership/topic context and original value hashes are retained. The immutable raw snapshot and exporter manifest are under ignored `.local/edb/math-image-import-audit-2026-10-23-inline-display-facts.*`.

A subsequent repair should preserve scoped MathML styles in the extractor, define the desired integral/block layout policy, and then prepare guarded content updates from the reviewed inventory. This audit makes no such code or database changes.
