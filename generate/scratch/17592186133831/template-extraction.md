# Four extraction stages

## 1. Specific observed questions

All original strings, fields and owned banks are in `source.json`. `source-cases.json` maps every practice record to a complete replay profile. `bank-map.json` lists each of the 25 original exact choice values, parsed integrand, limits, complete scalar value and source correct designation. This is the exhaustive per-choice mapping rather than a correct-answer-only table.

q-124638 uses P=y², Q=−x², x=t, y=t², t∈[0,1]. It substitutes the squared y coordinate before reduction, differentiates the two displayed coordinates formally, and computes t⁴−2t³. Its five integrands are 1−t², t⁴−2t³, t⁴−4t³, t²−t and 4t³−3t², all under the same bounds.

q-124687 uses P=y, Q=−x and x=cos t, y=sin t on [0,π]. Direct substitution has no redundant reduction row. Formal differentiation retains both coordinate derivatives. The dot product reduces −sin²t−cos²t to −1. Its bank is ∫(1−sin t), −∫1 (correct), ∫1, ∫sin t, and scalar 0.

q-124679 uses P=x, Q=y+1 with the same unit semicircle and bounds. Its component products −cos t sin t+(sin t+1)cos t reduce to cos t. The bank integrands are −cos t, 2sin t cos t, cos t (correct), −sin t cos t, and sin t. Four complete integrals equal zero; raw ambiguity is retained explicitly.

q-124680 uses P=xy², Q=2y and x=eᵗ,y=√t on [0,1]. It shows squared-root substitution, then reduction, formal coordinate derivatives eᵗ and 1/(2√t), then two scalar products and t e²ᵗ+1. Bank integrands are e²ᵗ, t e²ᵗ+1 (correct), eᵗ√t, eᵗ+√t, and t eᵗ+2√t. The missing `j` in the raw vector is not silently copied into normal variants.

q-124685 uses P=x,Q=y and the spiral x=t cos t,y=t sin t over [0,π]. Both coordinate derivatives require the product rule. Its dot block has the vector product, two products, distributed terms, collected trig squares, and t. The malformed distributed row remains exact in evidence. Bank integrands are sin t, cos t, t (correct), t cos t, t sin t.

## 2. Shared pattern

Compute the integral associated with the *supplied* parameterization: substitute both coordinates into both field components, differentiate both coordinate functions, take their component dot product and retain the stated integration limits. The expected response is a complete definite integral, never an evaluated scalar or an alternative reparameterization. Original wording is retained only in raw profiles; normal wording explicitly states this response criterion.

## 3. Components and complete-bank mapping

Fixed prose is the source sequence “We will use the formula”, “Along the curve C”, “Therefore”, “Computing r′(t)”, “Therefore”, and “Finally, we can write the integral as follows”. It is independent of option order or selected error. There is one `selection` radio, five delimiter-free math values and one owned correct ref. The outer local review record uses plain `db_id`, `id`, `title`.

Observed masks replace *complete* field, field-substitution, dot-product and final-integral components. The scaling c multiplies the actual field and each corresponding scalar integrand; the derivative vectors do not scale. The upper endpoint is a complete limit argument. c=1 gives exact raw strings and complete banks, including scalar 0, derivative row omissions and source anomalies. Nonunit c is a transparent algebraic generalization of the historical pattern, not a recovered explanation of wrong answers. Whole-bank operation patterns are not mixed or trimmed.

The normal authored complete bank is chosen before parameters: (1) P(r)x′+Q(r)y′, (2) its negative, (3) P(r)x′, (4) Q(r)y′, (5) P(r)+Q(r). These are actual derivative/sign/term omissions. The correct answer is computed first; all four wrong members are derived from the displayed components. Any whole-bank collision rejects the entire sampled instance. No first-valid pool replaces an option. Author recipes are metadata only; learner-facing distractor diagnosis is absent.

## 4. Reusable masks, bounds and identities

Source replay uses the source prose and six complete display-block masks. Formal coordinate differentiation has the same order and count as the original. The normal renderer separately uses the same prose skeleton and retains substitution, formal derivative and component-product stages. For the two source notation anomalies, generated solution repairs are explicitly reported. Normal hard distribution has each scalar term before reduction, and source direct-linear field families omit a redundant substitution reduction row.

Easy defaults independently choose all five families. Signed nonzero integer field coefficients have magnitude ≤4. Polynomial limits are [0,1|2|3], regular exponential/root limits [1,2|3], and circle/spiral limits [0,π/3|2π/3|4π/3]. These same-method interval variations are authored, chosen to permit complete eligible banks; they do not create an evaluation workload. Moderate powers are unequal integers in {2,3,4}, with two nonunit power derivatives and otherwise the same workload. Hard has four nonzero mixed linear coefficients with unequal diagonal and cross coefficients; both curve derivatives are the observed two-term product rule and the dot product has four substituted products. Hard collection retains sin t/cos t products and squares; it does not introduce double-angle identities. Every explicit input follows the same guards. Within a difficulty families and parameters are unordered practice variations.

The nominal bounded authored domains before whole-bank rejection contain 192 polynomial, 24 rotation, 192 shifted-circle, 128 exponential/root, 24 spiral, 1152 moderate and 9408 hard parameter tasks. The independent finite-domain audit in `variety.json` verifies all of those complete banks as eligible. Deduplicating the actual constructed integrand and bounds gives 192 polynomial, 24 rotation, 24 shifted-circle, 128 exponential/root, 24 spiral, 576 moderate and 9408 hard tasks. The diagonal circle coefficient cancels, so it does not inflate task counts; moderate coordinate/power exchanges producing the same integrand are deduplicated. Exact coefficientwise scalar integration proves bank distinctness, using rational coefficients of algebraic constants, π and integer exponentials. No variable aliases or profile names inflate these counts.

Two equivalence tests are kept separate: response-form eligibility requires the printed dot-product integrand and the supplied limits; complete definite-integral scalar equality identifies coincidental integrals. Normal banks conservatively reject both kinds of collision. Raw source ambiguity remains preserved and ineligible. Scalar integration is an internal independent validation calculation only.

Content identity hashes generator version, difficulty, actual prompt, fixed solution and unordered full displayed bank. Mathematical fingerprints hash the constructed integrand, stated bounds and response criterion, excluding bank, profile alias, seed and option order. A change of seed/order at fixed parameters retains identity. Choices have field-owned UUIDs; answer, field and question UUIDs are local review identities rather than the original database identities. JSON is plain serialization, not transaction EDN.
