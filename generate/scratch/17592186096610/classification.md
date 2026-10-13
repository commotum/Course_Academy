# Classification at captured basis 1356

The unchanged capture is `source.json` (database math; lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`). Seven practice questions, five rated easy and two unrated. The canonical e-3624 is evidence for instruction but does not inflate practice coverage. No practice or canonical problem has a plot; all ratings are **none**. No plot renderer is needed at steps 5/7.

| Template | Original IDs | Rating | Field and response | Banks | Solution structure |
|---|---|---|---|---|---|
| legacy_derivative | q-1927, q-51208 | Unrated; authored easy assignment | One radio, five full derivative equations | Two separate observed complete banks | Absent; canonical-based authored four-row derivative solution |
| slope_radio | q-101587, q-101590 | Easy | One radio, five scalars | Two observed banks | Four derivative rows, then respectively four or three evaluation rows |
| derivative_blank | q-340056 | Easy | One blank `field-1`, RHS expression | Two equivalent accepted expression spellings | Four derivative rows, nested source aligned environments |
| slope_blank | q-340067 | Easy | One inline blank `field-1`, scalar | Single expected scalar | Four derivative rows, four evaluation rows |
| derivative_radio | q-71053 | Easy | One radio, five full equations | One observed complete bank | Constant-first formal derivative/distribution/reduction/final, nested source aligned environments |

Thus there are five observed Markdown/answer-shape/layout templates, five observed radio profiles and two blank profiles. Changing coefficients, a constant's notation, or the slope point does not create a new instructional template. Distinct observed scalar-bank patterns are retained.

## Route and boundaries

Order is obtained by following `:activity/first-step` and `:step/next`, not collection order: 97413 introduction → 97414 this KP → 97415 plus-polynomial KP96611 → 97416 other-base tutorial → 97417 other-base KP96612 → 97418 justification → 97749 second justification. The introduction supplies d(e^x)/dx=e^x. Canonical e-3624 uses the sum and constant multiple rules on 3e^x+ln3. The key prerequisite is topic278, The Sum and Constant Multiple Rules for Differentiation. Topic1114's incoming prerequisite relations are slope by differentiation (332), natural logarithm (818), and graphing exponentials (1530). Topic1007, Chain Rule With Exponential Functions, occurs later.

All supported tasks remain **ae^x+c**, with exactly one x-dependent exponential, constant coefficient a, and x-independent c. There is no plus-polynomial, other base, scaled/translated exponent, tangent-line equation, solving for a point, or chain-rule extension. Evaluation at a supplied point is observed easy and uses the prerequisite slope interpretation.

## Missing-level authorship

No moderate or hard practice labels are observed. Their labels are design claims, not recovered MA definitions. They stay at this KP's same derivative-and-evaluate method, increasing only bounded exact arithmetic. Each level consists of unordered peers, never a progression.

* Easy: integer a with 2≤|a|≤12; a nonzero integer constant or signed ln of an integer 2…20. Source-familiar evaluation points 0, 1, or ln(n), n=2…9. Both signs and component orders are available. All seven originals fit; assigning the two unrated direct-derivative originals easy is explicitly authored.
* Moderate: a reduced noninteger rational with denominator 2…4, 1≤|numerator|≤12 and |a|≤6; the supplied point is −ln(n), n=2…9. Each peer differentiates the same two terms, evaluates the exponential as 1/n, and multiplies/reduces one rational product. Exact reciprocal evaluation is anchored to the source's e^{ln2}=2 and the prerequisite natural logarithm, with no new differentiation rule.
* Hard: the coefficient has the same bounded reduced rational form, denominator 2…5. The point is ±ln(r), where r is a reduced positive noninteger rational, numerator 2…12, denominator 2…5, 1/5≤r≤6, r≠1. Each peer uses the same derivative, inverse-exponential evaluation, and one rational product; signed reciprocal cases are unordered variations. This is arithmetic load within the established log/e evaluation, not a sibling KP.

Constants, component order, equivalent answer aliases and banks affect presentation but not the assessed mathematical-task fingerprint. For a derivative task the fingerprint contains a and the derivative response criterion; for an evaluated slope it contains a, the exact point, and the slope criterion. Changing c cannot inflate mathematical variety. A deterministic 200-seed audit found easy 73, moderate 156 and hard 190 distinct mathematical tasks (194, 199 and 200 presentations respectively). These numbers are distinct sampled tasks, not a claim of unbounded variety.

## Source anomalies and fidelity denominators

q-1927/q-51208 lack ratings, worked solutions and correct refs. The authoritative MA lesson `.../Lessons/1114/1114.md` and its captured radio widgets confirm the complete five-option layouts, also explicitly marking missing answers. Independently differentiating ln7+7e^x and ln2−4e^x uniquely identifies 7e^x and −4e^x. New refs and canonical-derived solutions are **authored repairs**; absent designations cannot count as matched originals. Raw capture stays unchanged.

q-340056's two blank choices are mathematically equivalent accepted spellings 6{e}^x and 6e^x, not two conflicting radio options. Preserve both as aliases in the replay profile. No original blank lacks its placeholder. No mathematical source answer or solution error was found. The only worked-solution spelling normalization is whitespace in `2 e` versus `2e`; raw-exact and notation-normalized solution counts are separate.
