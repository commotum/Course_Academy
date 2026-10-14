# Template extraction — four stages

## 1. Describe the individual sources

- **q-66139**: “Calculate” prompt, `3^x`, easy, radio. Bank: `3^x/ln3+C`, `ln(3^x)+C`, `3^x ln3+C`, `3^x+C`, `ln x/ln3+C`. One solution row states division by the base's natural log.
- **q-113887**: same prompt and solution backbone at base 5, easy. Bank: `5^x ln5+C`, `5^x+C`, `ln x/ln5+C`, `5^x/ln5+C`, `5 ln x+C`. Its final logarithmic wrong value differs from q-66139, so its complete bank is kept separate.
- **q-113890**: bare integral equality prompt, `2*9^x`, moderate. Bank: `2*9^x+C`, `ln9/9^x+C`, `9^x/ln2+C`, `ln2/(9 ln x)+C`, `2*9^x/ln9+C`. Solution: prose names 2; first row factors 2; second applies the base rule.
- **q-31249**: same moderate backbone at `3*2^x`. Bank: `2*3^(ln x)/ln2+C`, `ln x/ln2+C`, `3*2^x/ln2+C`, `3*3^(2x)/ln3+C`, `2/ln x+C`. Swapped base/coefficient and changed-exponent expressions are full raw evidence; their historical intentions are unresolved.
- **q-113893**: “Calculate” `(1/8)^x`, hard. Bank: `(1/8)^x ln8+C`, `-(1/8)^x/ln8+C`, `ln x/ln8+C`, `-ln x/8^x+C`, `8^x/ln8+C`. Solution first divides by `ln(1/8)`, then separately displays `ln1-ln8`, `0-ln8`, `-ln8`, then the full final primitive equality. No scalar factoring row.
- **q-31248**: “What is” `4*5^x` with no difficulty, correct designation or solution. Bank: `5/ln x+C`, `ln x/ln5+C`, `2*4^x/ln5+C`, `4*5^(ln x)/ln5+C`, `4*5^x/ln5+C`. The last option's derivative equals the displayed integrand. This inference does not fabricate source attributes.

Raw decoded strings have **U+2061 FUNCTION APPLICATION** after literal `ln` in the five rated questions. These are not doubled-backslash corruption. The original q-31248 uses standard TeX `\ln`. `source-choice-map.json` records actual decoded adjacent-backslash counts and Unicode counts. Raw prompts, complete banks, all available solutions, and attribute presence replay exactly. Normal output changes literal Unicode function application to standard `\ln `, with no algebra or stage change.

## 2. Generalize the shared pattern

Find the family of antiderivatives of `c*a^x`, where the base is a positive constant other than 1 and the exponent is exactly `x`. The fixed response is a complete primitive plus arbitrary `C`, selected from five radio options. Easy uses `c=1,a=b>1`; moderate uses a nonunit integer scalar and integer `a=b>1`; hard uses `c=1,a=1/b` and explicitly applies `ln(1/b)=-ln b`. The independent/dependent variable is always x. There is one concrete solution per instance, independent of the selected option.

## 3. Map every component and whole bank

`source-choice-map.json` has every original option record, exact replayed string, parameterized recipe label, exact full mathematical value at its anchor, and evidence/interpretation status. `source-cases.json` gives all six source IDs, parameters, families and public `raw:<source-id>` profiles. `source.json` retains the full source wrapper and every missing-attribute distinction.

Let `b` be the original integer base (hard: reciprocal denominator), `c` the scalar. All entries below include `+C`; correct is computed before the four wrong values, but order shown is source order.

| Public source profile | Original parameters | Complete parameterized evidence bank |
| --- | --- | --- |
| raw:q-66139 | b=3,c=1 | b^x/ln b; ln(b^x); b^x ln b; b^x; ln x/ln b |
| raw:q-113887 | b=5,c=1 | b^x ln b; b^x; ln x/ln b; b^x/ln b; b ln x |
| raw:q-113890 | b=9,c=2 | c b^x; ln b/b^x; b^x/ln c; ln c/(b ln x); c b^x/ln b |
| raw:q-31249 | b=2,c=3 | b c^(ln x)/ln b; ln x/ln b; c b^x/ln b; c c^(b x)/ln c; b/ln x |
| raw:q-113893 | b=8,c=1 | (1/b)^x ln b; -(1/b)^x/ln b; ln x/ln b; -ln x/b^x; b^x/ln b |
| raw:q-31248 | b=5,c=4 | b/ln x; ln x/ln b; (c/2)(b-1)^x/ln b; c b^(ln x)/ln b; c b^x/ln b |

The halved coefficient/predecessor-base mask in q-31248 parameterizes its complete displayed `2*4^x` value. It is **not a claim that the historical author intended that algorithm**. The compound expressions in q-31249, q-113890 and q-113893 likewise remain explicit evidence-only banks. Raw log-coefficient banks require positive c. Other complete eligibility guards and derivative-equivalence rejection still apply to raw replay. No source values are discarded or replaced.

Normal easy banks preserve each of the two observed bank shapes with standard ln notation. Moderate normal banks are clearly authored: both contain correct `c b^x/ln b`, omitted scalar `b^x/ln b`, omitted logarithm `c b^x`, then either (a) multiplied logarithm `c b^x ln b` and log coefficient `c b^x/ln|c|`, or (b) reciprocated scalar `b^x/(c ln b)` and reciprocated base `c b^(-x)/ln b`. Complete bank (a) is ineligible when |c|=b. Hard normal bank is authored from the assessed base/log steps: correct negative quotient, omitted negative sign, positive logarithm multiplier, inverted reciprocal base, omitted base logarithm. These whole profiles are selected before parameters; no first-valid recipe pool or random offset exists.

## 4. Extract the reusable masks

Fixed components: x exponent/variable, indefinite integral, base-rule method, arbitrary C, shared full source prose, ordered solution stages, one selection field and five math answers. Variable slots: integer b=2..20; moderate nonunit signed integer c of magnitude2..12. Dependent parts: every integrand occurrence, scalar prose, factored coefficient, base quotient, all bank values, and all hard log/conclusion occurrences. Conditional grammar: moderate retains the source scalar opening, easy/hard retain the source general-base opening. “What is” uses its original compact prompt and the existing moderate solution in normal completed records. Raw q-31248 keeps its absent solution.

Exact solution structural masks are independently compared with full source prose and stage sequence; numeric changes cannot remove or add an operative row. The hard logarithm quotient, ln1-minus-ln b, zero-minus-ln b, negative-ln b and full concluding equality remain distinct. Neither numerical equality nor row counts alone satisfy the structure check.

Invalid parameters reject explicitly; random sampling resamples the whole parameter pair for the preselected complete family/bank. Every pair in the displayed bank is compared by equality of derivatives on a common positive-x interval, which identifies arbitrary-C equivalent primitive families and catches wrong/wrong ambiguity. Domain-limited historical log distractors are preserved; the intended correct primitive is valid for all real x. No error-explanation prose or feedback is authored.

Presentation identity includes actual prompt, concrete fixed solution, difficulty/presence, complete bank, correct designation policy and version. Mathematical identity uses only the actual integrand and response contract. Stable seed shuffling changes display order, never identity; banks/layouts do not inflate meaningful task counts. No plots appear anywhere: standalone TeX needs no renderer, so steps5 and7 have no plot artifacts.
