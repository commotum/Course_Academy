# LaTeX quality check: two vector topics

Two **GPT-6.1-sol agents at high reasoning** reviewed the requested topics at EDB **basis 11863**. This was a read-only quality pass: no database repairs or application changes were made.

The reviews cover **189 practice questions, eight canonical examples, six tutorials**, and their linked choices and expected answers. **1,123 instructional/title fields pass strict MathJax checks**, but the following defects survive syntax validation.

| Finding | Position-vector topic 17592186048780 | Vector-line topic 17592186049485 |
|---|---:|---:|
| Malformed arrow/bar expressions | 14 occurrences in 11 fields | 1 occurrence in 1 field |
| Source-confirmed loss of bold vector styling | 21 fields | 32 fields |
| Broader vector-font consistency candidates, including confirmed fields | 298 fields | 217 fields |
| Questions missing solution and answer key | 17592186097240 | 17592186106065 |

The malformed expressions use pseudo-TeX such as `OR^(→)` or `PQ^(―)`. They display literal superscript parentheses rather than an arrow or bar spanning the letters. Use `\overrightarrow{OR}` or `\overline{PQ}` as appropriate. An independent parent-agent scan confirmed all **15 occurrences across 12 fields**, and representative screenshots confirm the visible defect.

The **53 source-confirmed vector-font mismatches** lose the original bold vector convention; some formulas mix bold prose variables with plain display variables. The broader **515-field candidate list is not 515 individually verified import defects**. Font restoration must preserve scalar parameters and coefficients.

Two other completeness issues affect grading: the missing key/solution on each topic's question above, and duplicate `selection` fields on position-vector question **17592186097046**. The reports identify existing correct answer entities and the duplicate fields.

The line-equation review also found **13 solutions** that simplify a principal square root using ± instead of an absolute value. For example, `\sqrt{18t^2}=3\sqrt2|t|`; ± belongs when solving for `t`. The canonical source contains the same imprecision, and the final answers remain correct. This is distinct from import corruption.

The previously repaired `\overset{\to -}` defect is absent from both topic snapshots. No additional concrete delimiter, matrix/fence, or grouping defect was identified.

- [Position-vector report and exact IDs](topic-17592186048780/report.md)
- [Vector-line report and exact IDs](topic-17592186049485/report.md)
- [Independent coverage inventory](coverage.json)
- [Independent malformed-notation scan](independent-pseudo-notation-scan.json)
- [Machine-readable summary](summary.json)

All existing in-scope fields received automatic rendering checks and source-string review. Visual inspection and comparisons with original capture files were representative; not every field was individually screenshotted or matched to historical source. The audit covers current linked content at the pinned basis, including stored generated items, not every possible future generator output or unlinked historical entity.
