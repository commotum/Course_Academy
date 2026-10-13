# Classification, math basis 1356

Database `math`, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Immutable source/topic/lesson captures are under `generate/runs/current`. `source.json` copies the complete KP capture wrapper. Ten practice sources, all one `selection` radio with five mathematical choices. All ten banks are accounted for. Eight original correct designations and worked solutions exist; two do not. No plots or image references occur.

| Source | Observed difficulty | Factoring site and expression structure | Bank profile | Original solution stages | Plot |
|---|---|---|---|---|---|
| q-65165 | absent; authored moderate | numerator: sin²(cos²+sin²)/(cos sin) | raw:q-65165 | absent | none |
| q-65166 | absent; authored moderate | denominator: sin²/[sin(sin²+cos²)] | raw:q-65166 | absent | none |
| q-119379 | moderate | numerator: sin cos²(sin²+cos²)/(cos sin) | raw:q-119379 | factor, identity, expand repeated factors, cancel, quotient, cosine | none |
| q-119387 | moderate | denominator: sin² cos/[sin³(sin²+cos²)] | raw:q-119387 | factor, identity, split sin³, cancel sin², ratio, cotangent | none |
| q-65246 | moderate | numerator: sin(cos²+sin²)/cos | raw:q-65246 | factor, identity, ratio, tangent | none |
| q-65248 | moderate | denominator: cos²/[sin cos(cos²+sin²)] | raw:q-65248 | factor, identity, cancel cosine, ratio, cotangent | none |
| q-65249 | moderate | denominator: cos sin/[cos²(cos²+sin²)] | raw:q-65249 | factor, identity, cancel cosine, ratio, tangent | none |
| q-119381 | hard | numerator: cos²(cos²+sin²)+cos² over cos² sin | raw:q-119381 | factor first pair, identity, collect two cos², cancel, reciprocal | none |
| q-119392 | hard | numerator: cos sin(sin²+cos²)+1 over sin² | raw:q-119392 | factor first pair, identity, separate fractions, split square, cancel, reciprocal-square sum | none |
| q-72712 | hard | numerator: sin(sin²+cos²)+1 over cos | raw:q-72712 | factor first pair, identity, separate fractions, tangent + secant | none |

Template counts: five rated moderate, three rated hard, two unrated whose raw omissions remain intact. Different source stage sequences and prompt layouts stay separate masks even when final functions coincide. Each observed template has its complete five-choice source profile and a separately authored default bank. The new easy template has one authored bank.

The canonical example e-3137 factors cos from a numerator, collapses sin²+cos² to 1, and recognizes cotangent. The ordered lesson chain is recovered from `activity/first-step` then `step/next`: 17592186060476 introduction → 17592186060497 expansion KP59655 → 17592186060477 factor-only KP59641 → 17592186060478 this rational KP59642 → 17592186060479 common-denominator KP59643. This order is not Pull array order. The key prerequisite is Simplifying Rational Expressions by Factoring (topic423). Basic trig ratios/reciprocals are established in the preceding topic203. Alternate identities are a later topic205.

Missing easy is explicitly authored: (k sin²+k cos²)/sin, or its cosine mirror. It retains one rational expression, one factor/identity site, and one reciprocal recognition; there is no surviving additive term or trig-monomial cancellation. The same three actions occur in every easy instance. Moderate keeps one factoring site followed by monomial cancellation and ratio/reciprocal recognition. Hard keeps the observed extra surviving term after the same identity reduction. Scalar 1–12 and sin/cos mirror vary elementary integer arithmetic and same familiar functions without adding a mathematical branch, common denominators, alternate identities, solving equations or a progression within any level. Original powers are unchanged (at most five). Angle aliases do not count as mathematical variety. Bounds apply to explicit inputs and sampling.

No additional reads or mutations of EDB were made. Original MA lesson207 JSON was inspected read-only: q65165 and q65166 are multiple-choice widgets with five choices, but the captured widget has no correct key or worked solution. The correct normal choices are independently derived: sin²/(cos sin)=tan and sin²/sin=sin on the respective original nonzero domains. Both inferred moderate labels and authored solutions remain separate from observed evidence.
