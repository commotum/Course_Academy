# Template extraction: non-integer 2×2 determinants

Protocol: [4-template-extraction](../../../docs/4-template-extraction.md). Basis **1522**. [Every original](source-questions.md) includes all exact values and original solution text; [source cases](source-cases.json) describe entries a,b,c,d, ad, bc, fields, profiles, and each choice.

## Specific originals

Entries below are ordered (a,b;c,d), with determinant ad−bc. All symbolic variables are real; templates using √x require x≥0.

| Source | Level/field | Entries | Correct result | Additional work |
|---|---|---|---|---|
| q-1089 | Easy radio | (√x,y;y²,√x) | x−y³ | Root square and exponent addition |
| q-1083 | Easy radio | (2x,y²;z,−3) | −6x−y²z | Sign and monomial multiplication |
| q-1087 | Easy radio | (1/2,17;1,10) | −12 | A cancelling fraction product |
| q-275595 | Easy blank | (√3,y;2,√3) | 3−2y | Root square |
| q-317374 | Easy blank | (√6,y;4,√6) | 6−4y | Same root-blank family |
| q-69649 | Easy radio | (3√x,z²;2y,−√x) | −3x−2yz² | Root coefficients and signs |
| q-127601 | Moderate radio | (−x,−2y;x/2,5y) | −4xy | Two signed products and cancellation |
| q-127603 | Moderate radio | (2x,y;−5,xy) | y(2x²+5) | Factoring a shared y |
| q-69650 | Moderate radio | (−2r,3s;−2t,3u) | 6(st−ru) | Double negative and factoring 6 |
| q-317367 | Moderate blank | (2/5,−3;−1/2,2) | −7/10 | Subtract two fractions |
| q-317368 | Moderate blank | (−3/4,5;2,−1) | −37/4 | Fraction minus integer |
| q-317372 | Moderate blank | (3x,2y;−5,x) | 3x²+10y | Double-negative subtraction |
| q-1088 | Unrated radio | (√2,5;1,3) | 3√2−5 | Missing source solution/reference |

## Shared pattern, components, and templates

Evaluate a supplied 2×2 determinant directly using ad−bc. Fixed components are the determinant operation and the source's formula reminder followed by one fixed worked solution. Variable components are matrix letter, literal entries, products, intermediate simplifications, and final answer. Named-matrix prompts, bare determinant prompts, and blank layouts remain separate as classified. No equation solving, larger matrix, or determinant theorem is introduced.

Named-matrix radio form:

```text
Calculate $det(LETTER)$, if
$LETTER=[\begin{aligned}{a} & {b} \\ {c} & {d}\end{aligned}].$
```

The blank version appends `$det(LETTER)=$` and `{{field-1}}`; the bare blank form places the placeholder after the displayed determinant's `=`. Blanks expect the scalar/algebraic result alone. Preserve the source matrix letter and field key and keep canonical values delimiter-free.

The source worked solution reminds the learner that the determinant is ad−bc, repeats the actual matrix, substitutes the diagonal products, simplifies them, and optionally factors the result. Preserve all original intermediate rows; the proposed hard family adds algebra rows instead of silently dropping that scaffolding. Its formula reminder is retained, not replaced by a new method.

Useful constrained families include `diag(sqrt(k),sqrt(k))` with off-diagonal entries y and m; monomial entries with coefficients; signed rational entries; and families whose products share a visible factor. The observed root-blank parameters are (k,m)=(3,2),(6,4), not evidence that those are the only allowed values. Rational family denominators may be 1. Preserve observed negative coefficients and cancellation conditions. If x occurs under a radical, retain x≥0; purely polynomial variables have no positivity restriction.

## Complete choice-bank patterns

[Source-cases.json](source-cases.json) assigns every original choice to its field and source-specific bank, with its complete expression and parameters. Candidate prompt-based recipes are recorded only when they reproduce the whole original value. Recognizable patterns include ad+bc, bc−ad, one diagonal contribution, and dropped signs/factors. Symbolic banks also contain altered powers and coefficients; their complete expressions remain intact even where the author's error mechanism cannot be established.

For example, `q-69650`'s five choices are 6(ru−st), 6ru−3st, correct 6(st−ru), −6ru+3st, and 3(2st−ru). That entire profile is retained. `q-1083` additionally offers constants 5 and 1, which have no established generic derivation from its symbolic prompt. Those remain flagged fixed source constants, not invented “wrong-scale” explanations. Do not pool the banks or claim source fidelity from correctness alone. Blank fields have no distractor profile.

## Missing-hard experiment

[Authored probe](../probes.md#non-integer-determinant) retains a 2×2 matrix and the observed blank field, but uses conjugate radical fractions for all four entries. The learner must evaluate both diagonal products, use two conjugate-product simplifications, and combine rational results. The answer is −41/210.

This extension adds workload while preserving the determinant procedure. It deliberately exceeds the observed monomial/single-radical entry shapes, so label it an **authored proposed hard family**, not an extracted source hard template. Conjugate products are prerequisite algebra; the new difficulty is coupled to that algebra. Asking for an unknown k or changing to 3×3 would instead change the assessed KP and is rejected.

**Best judgment:** a hard setting is feasible inside the KP, with moderate design effort and no plotting burden. Its mathematical correctness is clear; the hard label remains our pedagogical estimate and needs no claim that Math Academy has that setting.
