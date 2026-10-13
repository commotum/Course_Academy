# Classification — KP 17592186152119

Math database, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Exact capture is `source.json`; the canonical example is e-14815. Eight practice records were analyzed, including two unrated records. No plots or diagrams occur; plot rating **none**. No rendering dependency is needed.

| Level | Template/layout | Field | Source IDs | Complete banks |
|---|---|---|---|---|
| Easy observed | single shifted primitive factor | blank, key field-1 | q-222127, q-222129 | One entry each; two notation/multiple-list profiles |
| Easy observed | single shifted primitive factor | radio, key selection | q-76247 | Five entries, one complete bank |
| Moderate observed | two shifted primitive factors in independent variables | blank, key field-1 | q-222132 | One entry |
| Moderate observed | two shifted primitive factors in independent variables | radio, key selection | q-112230 | Five entries |
| Moderate observed | monomial and shifted factor, in independent variables | radio, key selection | q-76475 | Five entries; distinct monomial notation and multiple lists |
| Unrated → authored Easy assignment | single factor, legacy prompt with spaces | blank, key field-1 | q-218518 | Captured bank and correct designation absent |
| Unrated → authored Moderate assignment | monomial/binomial, legacy combined first-two-input span | blank, key field-1 | q-218519 | Captured bank and correct designation absent |
| Hard authored, no source difficulty labels | three already displayed binomials in the same two variables | blank or five-entry radio | none | Complete authored bank |

There are four rated mathematical/field families (`single_blank`, `single_radio`, `double_blank`, `double_radio`), with distinct binomial/binomial and monomial/binomial profiles of the last family. Two legacy prompt layouts remain separately named templates. Do not treat changed constants as additional templates. `masks.json` retains all exact span and prose differences, including commas, ellipses, powers, braces and the final aligned layout.

The captured local lesson JSON at `/home/jake/Developer/MA/DATA/Lessons/2626/Source/2626.json` confirms one free-response math-editor blank for each unrated record, no choices or solution. Its relevant widgets are copied to `missing-widget-evidence.json`. Derivations give 12(x+1)^5 and 20u^3(v-2)^4; these are completions, not observed source answers. Their Easy/Moderate assignments are authored from the corresponding rated factor count and workload.

q-222132's solution names `(x-y)` in its factor-selection sentence, while the prompt and every subsequent line use `(x-7)`. The supported correction is solely that factor reference. The original entire solution replays under `observed-q-222132-raw-error`; ordinary `observed-q-222132` and normal output use the corrected factor. No raw source answer bank is erroneous or ambiguous.

Lesson order is resolved from activity first-step and the step/next links: Introduction → constant-factor two-polynomial LCM → single-factor powered two-polynomial LCM → two-variable two-polynomial LCM → this three-polynomial KP. Prerequisite topic 2625 is LCM of two monomials. Subsequent rational-expression topics are not used as generator scope.

The hard extension is a design claim. The lesson's general rule takes the greatest power of each distinct variable part and multiplies the results with the coefficient LCM. Three displayed factors `(x+a)`, `(y+b)`, `(x+c)` add exactly one factor maximum column to the observed two-column task. The factors are already factored, monic and distinct; no factorization, roots or coprimality computation is demanded. All three inputs contain every factor, and unique maximum powers come from different inputs. It stays in two variables and uses the same coefficient arithmetic bounds as Moderate. These are unordered peer instances, with no additional mathematical branch or progression.

Public raw-omission replay profiles preserve missing banks, correct refs, ratings and worked solutions exactly; normal completions are separately labeled authored. Raw/error and observed scalar-bank replay profiles are evidence-only. Default normal radio banks perform GCF/product-content and minimum/sum-power mistakes, chosen whole before acceptance. Fingerprints canonicalize consistent variable aliases and input order. Hard supports consistent variable aliases for the same two-variable geometry, but these add no meaningful task count. Fully expanded multivariable responses can exceed the native grader512token input cap; canonical and partially factor-expanded equivalents are checked separately.
