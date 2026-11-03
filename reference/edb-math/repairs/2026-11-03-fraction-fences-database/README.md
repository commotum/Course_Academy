# Database-wide fraction fence sizing

This extends the two vector-function lesson repairs to the entire math database. The earlier named-operator repair was already database-wide; the fraction-fence sizing repair had only been applied to those lessons.

The census visits question prompts, worked solutions, typed answer values and feedback, checkbox labels, tutorial text, and multistep contexts. It includes standalone examples and assignment content as well as KP pools. The initial fixed-basis census covered 707,988 content facts and 707,981 distinct entity/attribute pairs at T12431. Repeated source assertions of the same field were checked for equality before deduplication. Answer types were resolved before processing bare answer strings as mathematics. Machine field keys were not rewritten.

The main pass repaired 17,604 attributes in 16 guarded batches, ending at T12449. A fresh census using the extended single-token fraction rule identified 15 additional attributes, repaired in the sibling folder ../2026-11-03-fraction-fences-database-shorthand/. These fields do not overlap the main plan. Total repairs: **17,619 attributes**.

| Content | Repaired attributes |
| --- | ---: |
| Worked solutions | 10,734 |
| Answer values | 4,443 |
| Question prompts | 1,973 |
| Tutorial text | 289 |
| Checkbox statements | 173 |
| Multistep contexts | 7 |

The rule sizes complete balanced parentheses, square brackets and vector angles containing fractions, including fractions mixed with other terms. It preserves script/annotation scope, optional indices, alignment cell boundaries and manually chosen sizes. The follow-up extends argument recognition to valid shorthand such as `\frac12`, `\frac{\sqrt3}2` and `\frac\pi2`; incomplete fractions and argument-taking macros are not treated as complete shorthand fractions. Fraction operands, powers, signs, all mathematical tokens, and existing question/field/answer identities and correct links remain unchanged. The mathematical-token comparison allows only insertion of scalable fence commands, equivalent angle delimiter spellings and whitespace.

Existing content remained undersized because the formatter improvement had not yet been backfilled database-wide. The shared formatter, import boundary, structural validator, and generator publication boundary now cover these fraction patterns, including output from packages carrying older helpers. Generator author/reviewer instructions explicitly include shorthand fractions. No question mathematics, difficulty bands or generators' sampling distributions were changed. This presentation repair does not retire questions or rewrite learner attempts.

Verification evidence:

- 118 relevant regression checks passed after the shorthand extension and import fix (55 formatter/publication/delivery, 48 math-format, and 15 capture database math-content tests). The import fix formats displayed checkbox statements while preserving literal non-checkbox placeholder keys; all 173 repaired statements retain the expected imported spelling and create no duplicate labels within their question banks.
- All 4,443 affected answer values retain the same import-matching identity. Preflight checked 1,275 banks in the main pass and one additional bank in the shorthand pass, with no introduced identical options. Twelve affected answer entities were already used; raw learner submissions were preserved.
- 88 actual changed formula profiles passed the learner UI renderer in the main pass, plus 8 shorthand profiles. These cover all affected content types and nested parentheses/brackets/angles, scripts, deliberate sizes, aligned equations, arrays, cases and determinant/matrix environments. Representative nested, determinant, tutorial and shorthand cases were visually inspected. This verifies the sizing change, not the general layout of every long existing equation.
- The main live sample checks 220 grading cases on 47 complete questions across radio, select, checkbox and blank responses and all difficulty bands. Correct and alternative responses have the same aggregate and per-field grades before and after. Six incomplete imported keys were preserved. The shorthand sample adds its separate baseline/readback checks; two unowned questions cannot use the topic-scoped grading route and are recorded explicitly.
- Every transaction is durable, basis guarded, and checked against exact native entity readback, including nested component attributes. Only the proposed CAS patches differ; identities, response links, grades and all unrelated attributes are preserved. Receipts and the original request keys are archived in batches/ and the shorthand sibling, with no unverified pending request rotated away.
- The final independent database-wide census and its exact snapshot basis are in final-census.json; completion.json consolidates the final counts and checks. A zero residual count is scoped to the implemented fraction-fence rules. It does not claim to audit every unrelated typography or mathematical defect, nor force ambiguous conditional bars or author-selected manual sizes to change.

Executable workflow and full evidence: export uses the read-only operator-content exporter from the earlier repair; build.py, preflight.py, identity.py, render.py, deploy.py, capture_live_samples.py, verify_live.py and final_scan.py retain the plan and verification. snapshot.jsonl.gz and final-snapshot.jsonl.gz preserve the fixed-basis read evidence after completion. intermediate-census.json and shorthand-residuals.json record the 15 cases caught before the final follow-up.
