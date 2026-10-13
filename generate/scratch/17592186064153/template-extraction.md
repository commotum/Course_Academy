# Template extraction

Basis 1356; exact six-question wrapper in `source.json`. Original and replay prompt, full banks, and complete fixed worked solutions appear in `review.md`. `source-choice-mapping.json` maps every original answer UUID/value to its complete bank and parameterized operation. The operation labels are author metadata, never learner distractor feedback.

## 1. Describe each source specifically

| Source | Supplied object and units | Input/rate | Number forms/sign | Prompt and solution stages |
|---|---|---|---|---|
| q-48571 | U(t), app users / hours | 4, 650 | positive integers; wrong quotient 162.5 | direct derivative notation; general derivative rate meaning → supplied equality → italic contextual conclusion |
| q-48615 | W(d), daily walking meters / day index | 3, 120 | positive integers; quotient 40 | direct derivative notation; no captured solution/key/difficulty; screenshot confirms bank |
| q-48688 | x(t), meters traveled / seconds | 30, 10 | positive integers; observed scalar 3 | direct derivative notation; same three prose stages, car wording |
| q-48691 | P(v), lemonade dollars / liters sold previously | 4, 0.5 | positive terminating decimal; 50 cents | italic tangent-slope statement → tangent slope equals derivative → displayed equality → italic contextual cents-per-liter conclusion |
| q-48709 | V(t), thousands of visitors / hours | 10, 1.5 | positive terminating decimal; 1500 visitors | same tangent-slope stages; conversion from thousands; source thin-space thousands notation |
| q-112091 | S(t), melting ice area cm² / minutes | 5, -7 | negative integer; positive magnitudes in options | direct derivative notation → source general-sign preamble → negative sign at supplied point → italic local decrease conclusion |

Each has exactly one five-choice radio field keyed `selection`, text answer values, no blank fragments, and no plots. Braced Unicode prime notation, punctuation inside math, optional final periods, italic conclusion, and source space before a paragraph are preserved exactly under observed replay. Answer order is ignored for fidelity but all 30 full text values are compared one-to-one. Stable generated UUIDs are field-owned rather than copied source UUIDs.

## 2. Generalized instructional pattern

Given what F(x) measures and a numerical F′(a)=r (or equivalent tangent slope), select the local statement: **at the supplied independent input a, the dependent quantity increases/decreases at magnitude |r| in dependent units per independent unit**. A positive output scaling s requires |r|s native output units. The derivative neither gives F(a), a finite interval's total change, nor a globally constant rate. Non-time inputs remain non-time inputs. No function formula or derivative calculation is supplied or required.

## 3. Components and complete banks

Let a be the supplied input, r its signed derivative, m=|r| and k the output scaling (1, 100 cents/dollar, or 1000 visitors/thousand). Correct choices are local at a with sign(r), magnitude km, and the correct output/input unit ratio. All five members are retained together for each profile.

* **app observed/authored:** local rate (a,r); global constant-rate quotient r/a; F(a) value (a,r); opposite local sign (a,r); finite change total r over the first a hours. Source r/a=162.5 is exactly derived. Shared source solution is retained in both profiles.
* **walking observed:** elapsed-day local rate (a,r); global constant-rate quotient r/a at day a; F(a) value r meters on day a; opposite local sign; finite change total r after a days. Source r/a=40. Correct key is derived independently, not observed. **Authored:** same numerical operations, with continuous-model/on-day location repairs and a newly authored three-stage solution.
* **car observed:** local rate; global constant reciprocal quotient a/r; F(a) distance value; opposite local sign; finite total r in first a seconds. Source a/r=3. Its interpretation is unresolved; the explicit numerical replay pattern is not promoted to default generation. **Authored:** the whole five-member bank uses r/a for the global-rate mistake instead, and replaces the impossible decreasing cumulative-distance rate with the positive input a misused as the rate at that point. a=r rejects the entire bank rather than making duplicate local claims. The worked solution's exact shared stages remain.
* **price observed/authored:** local cents-per-liter rate km at a liters; swapped input/output with decreased volume a liters/dollar at price km cents; opposite price sign; price F(a)=km cents; swapped input/output with increased volume. k=100. Swapped recipes are parameter exchange, not the mathematically computed reciprocal derivative. Fixed solution retains the tangent-to-derivative displayed row and cents interpretation.
* **visitors observed/authored:** opposite local sign; finite total km; correct local sign/rate km; global constant-rate quotient km/a; opposite finite total km. k=1000. Fixed solution retains slope-to-derivative equality and thousands conversion. **Authored signed_visitors** explicitly models visitors currently on the website, so a negative derivative refers to a changing count rather than cumulative visits. It uses this entire operation bank with negative r, reversing verbal sign appropriately; the positive magnitude preserves physical visitor counts.
* **ice observed:** F(a)=m area; correct local decrease at a with m cm²/min; swapped point/magnitude plus opposite sign at m with a cm²/min; global constant decrease m throughout first a minutes; swapped F(m)=a area. Correct negative r stays in the prompt and displayed equality; all contextual times/magnitudes in options stay positive. **Authored:** same complete bank and solution sequence, with one preamble word repair. a=m rejects the entire bank because two value claims become identical.
* **authored budget:** canonical e-271 prompt and three prose stages; local positive dollars/student, opposite sign, F(a) budget value, interval total r dollars from zero to a students, global rate r/a.
* **authored temperature:** negative degrees-Celsius/minute derivative; local decrease, opposite sign, F(a) value, finite total decrease, globally constant decrease. No neighboring skill or arithmetic beyond interpreting the supplied value.

Each original answer ID and exact value is mapped in `source-choice-mapping.json`; recipe operations are distinct from their inferred psychological explanations. Notably the scalar 3 alone cannot prove an original author intended input/rate. Its reproduction is complete bank fidelity, not recovered intent.

## 4. Reusable templates and constraints

Fixed components: complete contextual wording, function and variable roles, source radio key/type/count, unit phrases, paragraph sequence, derivative notation, solution sentences, whole bank membership. Variable components: complete numerical slots a,r,m,km, quotient values, and appropriate increasing/decreasing verbs for the signed visitors authored extension. Optional components: tangent-slope preamble and displayed derivative row only for the observed tangent families. Conditional components: observed versus authored car quotient, walking location/continuous-model wording, and ice preamble repair. Source replay is generated by the same parameterized recipes as changed-input variants; no raw-payload return branch or answer lookup table is used.

Samplers and explicit bounds are documented in classification and enforced before render. Complete banks are built before shuffling; duplicates reject the whole instance. Formatting validates every prompt/solution/choice, including observed replay. Content identity hashes actual prompt, full fixed solution, sorted complete bank and correct value, plus generator version. Seed/order/profile names alone do not change identity. Mathematical fingerprint excludes profile/bank; signed visitors shares the visitors context family. No renaming aliases inflate diversity.

Fidelity denominators: six exact prompts and complete banks, 30 exact options (24 incorrect and six local-rate values), five available correct designations, five available worked solutions. Walking's missing designation and solution are excluded **only from those metadata denominators**, while its entire question/bank is included. Ice raw solution is exact but carries one documented teaching-prose defect; normal authored solution has one mathematical repair, counted separately. Native choice-ID grading is separate from printed mathematical semantics.
