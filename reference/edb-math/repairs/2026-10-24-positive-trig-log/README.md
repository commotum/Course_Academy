# Positive trigonometric logarithms — engine repair

Reported question: **17592186678417**, KP17592186068918, topic17592186050489.

The integrand is 3 sin(x)/(cos(x)+2), and the canonical answer is −3 ln|cos(x)+2|, with an external +C. The entered −3 ln(cos(x)+2) is correct: −1 ≤ cos(x) ≤ 1 implies 1 ≤ cos(x)+2 ≤ 3.

The former engine represented ln(u) and ln(abs(u)) as distinct atoms and could not establish positivity of a variable trigonometric sum. The live endpoint returned HTTP409 with “constant antiderivative difference is not established by the supported rules.” `live-before.json` retains that reproduction; the new regression test also failed against the original engine.

The repair adds universal exact [−1,1] enclosures for sine and cosine of structurally real arguments, on the real domains retained during parsing. These bounds can discharge sign obligations and simplify abs(v) when v is provably nonnegative or nonpositive. This produces identical logarithm atoms for equivalent forms. No sampled values establish equality. Hidden imaginary arguments remain outside this proof, and original domain guards survive cancellation.

Regression cases cover the exact TeX entry, reordered sums, numeric constant shifts, scaled sine arguments, negative absolute-value arguments, fractions, and nested real logarithm arguments. Wrong signs, coefficients, offsets and inner arguments remain rejected. Sign-changing logarithms, hidden complex arguments, zero boundaries and cancelled poles remain protected. Both symbolic equality and the real grade_field path are tested.

All **198 release engine tests passed**. `build-verification.json` binds the production helper to its source hashes. `live-after.json` records read-only checks on the exact live question after the service reload; these checks create no learner attempts. No question content or learner history is changed.
