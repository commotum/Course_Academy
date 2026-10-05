# Exact symbolic answer checker

Implemented October 5, 2026, in `engine/rust/symbolic.rs` and integrated with the
study app's `learning::grade` and question-eligibility checks. It extends the
existing exact rational checker without adding dependencies or license keys.

## Supported answers

- Exact multivariate polynomials and rational expressions, including reordered,
  expanded, and factored forms, implicit multiplication, and scientific notation.
- Real roots of degree 2 through 8 and bounded rational powers. Numeric radicals
  factor into prime-root atoms, so `2√10`, `√40`, and equivalent rationalized
  forms compare exactly. Supported variable-root identities retain their domains.
- Sine/cosine parity and the Pythagorean identity; tangent, cotangent, secant, and
  cosecant as ratios/reciprocals. Standard pi angles reduce to exact radicals.
- Logarithmic and exponential atoms, logarithm bases, and exponential sums with
  integer coefficients. This is a limited set of identities, not a general CAS.
- Complex coefficients using `i² = -1`. For vector and Riemann/sigma questions,
  `i` is a formal symbol instead. Sequence/series/sigma contexts allow integer
  powers of a negative base when the exponent is an integer polynomial in the
  named indices `n`, `k`, `j`, and `i`.
- Standalone positive/negative infinity, DNE, and inequality/equality tokens.
- Saved TeX, MathQuill-style grouping, Unicode radicals/operators, and ordinary
  keyboard expressions. Use parentheses around ambiguous function arguments;
  for example `sin(2*x)`. Unspecified calls such as `f(x)` are unsupported;
  write `f*x` when multiplication is intended.

Choice questions continue to compare the selected authored answer entity ID.
Text blanks retain their existing text comparison. Prompts requiring rounding,
significant figures, or a particular reduced representation retain their
existing form-sensitive matching.

## How equivalence is established

The parser builds a bounded expression tree with conventional unary-minus and
power precedence: `-x^2` means `-(x^2)`. Algebra uses `BigRational` coefficients
and sparse commutative polynomials. Rational functions compare by exact cross
multiplication. Root powers, the imaginary unit, and squared cosine reduce with
explicit exact relations. Normalization never uses floating-point tolerance.

Division records nonzero conditions; even real roots record nonnegative
conditions; logarithms and unrestricted variable exponents record positive
conditions. These obligations survive cancellation. Thus `x/x` versus `1`,
or `sqrt(x)^2` versus `x`, remain unresolved because their unrestricted domains
differ. The checker does not infer additional domain assumptions from prose.

A zero exact difference proves equivalence. A nonzero rational polynomial
proves that two expressions differ. Other nonzero differences can be rejected
using **exact rational interval bounds**, sometimes at explicit integer
substitutions that satisfy the recorded domain conditions. Root bounds use
bisection; logarithm, sine/cosine, and exponential bounds use convergent series
with rigorous remainder bounds. Matching samples never establish correctness.

Different domain representations or identities outside the supported rules
return `Err`, even when a human could recognize an equivalence. `learning::grade`
propagates that error. The native app submits response, outcome, timing, and
credit transactions only after grading succeeds. An unresolved comparison
therefore does not become an incorrect learner outcome. The compatibility
predicate `learning::equivalent_math` returns true only for proved equivalence;
the learner-facing grading path uses the error-preserving comparison.

## Limits and remaining scope

Inputs are limited to 4,096 bytes, 512 tokens, and 64 nested parser levels.
Algebra has a 100,000-operation budget, at most 128 expanded terms, bounded
monomial degree, coefficient sizes, and integer powers of absolute value at most
64. Nested normal-form structure is also limited to 4,096 atom occurrences and
64 levels, preventing nested function expansions from escaping the term limit.
Numeric radicands must fit the bounded factoring range (at most 10¹², with
the operation budget still enforced). Interval witnesses use smaller term,
degree, coefficient, and argument limits. Oversized expressions return errors.

This implementation does not include general inverse-trig identities,
arbitrary functions, symbolic quotient roots, units, generic matrices/sets,
arbitrary equation solving, or general domain-equivalence proofs. More content
can be added through explicit rules and verified fixtures. Supporting a saved
canonical answer does not mean accepting every equivalent way to write it.

## Verification

`runtime-readiness.json` runs the **actual native grader** against the saved
1,506-question history batch, including all choice distractors. It also changes
each blank separately while keeping every other field correct.

| Check | Result |
|---|---:|
| Previously supported questions | 1,346 |
| Supported questions after this change | **1,506** |
| Previously blocked questions now supported | **160** |
| Deliberately changed blanks graded incorrect | **511** |
| Changed blanks accepted or left unresolved | **0** |
| Focused comparison fixtures | **70** |
| Full Rust library suite | **83 tests passed** |

The 70 fixtures include 47 equivalent pairs, 15 different pairs, and eight
expected unsupported comparisons. They cover actual saved answers, factored
polynomials, rationalized radicals, function notation, integer-index context,
precision counterexamples from the MathCore evaluation, and domain failures.
Additional unit tests cover undefined expressions and resource limits. The
full saved-content audit took about 0.21 seconds in one release-mode run; that
is an observation, not a formal performance benchmark.

All 25 current schemas passed the native EDB `--schema-only` checks. The native
study backend compiled successfully. The full legacy `check_rust_edb.sh` still
fails at its already documented retired `assessment/*` activity fixture
(`schema/unknown-attribute`, `tx[7]`); see `engine/rust/README.md` and
`engine/edb/README.md`. This change does not alter that fixture or any schema.

The original captured questions, choices, difficulties, KP links, and import
receipts were not rewritten. **No database transactions were needed:** the
existing records become eligible through the updated grader. Old audit records
remain historical evidence. `summary.json` records current counts and hashes.

## Run and reproduce

Restart an already running study app to load the compiled checker. For the user
service described in the repository README:

```sh
systemctl --user restart course-academy.service
```

For unit and focused comparison checks:

```sh
cargo test --offline --lib
```

To repeat the saved-question audit, build the library and compile
`scripts/validate_historical_question_readiness.rs` against the current release
`course_academy_engine` and `serde_json` libraries in `target/release/deps`.
Pass these two arguments to that helper:

```text
reference/mathacademy/history-question-import-2026-10-04/format-audit/questions.json
reference/symbolic-grader-2026-10-05/runtime-readiness.json
```

The helper requires no database and rejects any authored distractor or changed
blank that grades correct. The comparison fixtures run directly under
`symbolic::tests::captured_answers_and_independent_correctness_cases`.
