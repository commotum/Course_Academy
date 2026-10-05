# MathCore evaluation for Course Academy

Evaluated October 5, 2026, using the published Rust crate **mathcore 0.3.1**,
Rust 1.90.0, and the saved historical-question format audit.

**Decision: MathCore is not sufficient as our primary symbolic answer checker
in its current published form.** Its license is suitable, but its simplification
and expression semantics fall short of what our entered answers require.

## License and scope

MathCore uses the [MIT license](https://github.com/Nonanti/mathcore/blob/master/LICENSE).
It permits use, modification, and distribution, including commercial use,
subject to retaining the copyright and license notice. It has no registration,
license key, or runtime core restriction in that license.

This evaluation created an isolated Cargo project. It made no production engine
changes and no database writes. The production project's Cargo dependencies
were not changed. Cargo downloaded the library and dependencies into its cache.

## Actual saved-answer coverage

The source is `../mathacademy/history-question-import-2026-10-04/format-audit/questions.json`,
filtered by `runtime-readiness.json` to the same **160 unsupported questions**.
These contain **210 answer fields**, including numeric components of multipart
questions whose other fields cause the question to be unsupported.

| Probe | Successful fields | Total fields |
|---|---:|---:|
| Parse original saved notation directly | 39 | 210 |
| Parse after the evaluation TeX adapter | 177 | 210 |
| Evaluate adapted expression at one positive substitution | 171 | 210 |

All fields parsed after adaptation for 129 questions; all fields evaluated at
that single substitution for 123 questions. **These are parsing/evaluation
counts, not grading coverage or proof of mathematical equivalence.** The adapter
reuses our authoring interpreter, inserts explicit multiplication and grouping,
and preserves pi/e/imaginary-unit constants. It interprets `i` as an index in
sigma/Riemann contexts and a formal symbol in vector contexts. It is an
evaluation fixture, not a finished learner-input parser.

The adapter rejects standalone inequality signs and infinity tokens. DNE,
infinity, inequalities, and vector basis labels need explicit answer semantics;
a CAS alone would not resolve them. Evaluation also encountered unsupported
cosecant/cotangent functions, non-real results, and an overflow.

## Equivalent-answer checks

We tested 20 mathematically equivalent expression pairs and six deliberately
different pairs. Many pairs use the canonical answers of specific saved
questions; question IDs are recorded in `inputs.json` and `results.json`.

The probe tries both equality of the simplified expression trees and whether
simplifying their difference produces zero. MathCore's expression type lacks
`PartialEq`; the fixture compares Debug tree representations, not formatted
display strings. This comparison is for evaluation only.

Only **4 of 20 equivalent pairs** were recognized: `x-x = 0`, `1*x = x`,
`x+0 = x`, and `1/3+1/6 = 1/2`. It failed all 16 other pairs, including:

| Saved question | Equivalent forms missed |
|---|---|
| q-216930 | `7*b` and `b*7` |
| q-167208 | `400*a+20*b` and `20*(20*a+b)` |
| q-288850 | `x^2-5*x-50` and `(x-10)*(x+5)` |
| q-241753 | `2*sqrt(10)` and `sqrt(40)` |
| q-339941 | `(-11)/x` and `(-11)*x^(-1)` |
| q-332492 | `(sqrt(6)-sqrt(2))/4` and `1/(sqrt(6)+sqrt(2))` |

Other missed identities include `x+x = 2*x`, expanded rational denominators,
`sin(x)^2+cos(x)^2 = 1`, odd sine, and cosecant as reciprocal sine.

The simplifier also produced **two false acceptances in six negative probes**:

- `0.00000000000000001*x` simplified to zero because the library's zero predicate
  treats very small numeric coefficients as zero.
- `9007199254740992` and `9007199254740993` became the same numeric value because
  the normal expression representation stores numbers in `f64`.

These are targeted counterexamples, not estimates of real-world error rates.
MathCore has a separate arbitrary-precision module, but its normal parser,
`Expr::Number`, simplifier, and evaluator use floating point. Adding exact
arithmetic to that grading path would require further work.

## Expression behavior

The published parser evaluates **`-x^2` at `x=2` as +4**, and `-2^2` as +4.
Standard mathematical precedence gives -4 in both cases. Explicit grouping can
work around this, but passing ordinary learner text directly would misread it.

`7b` is rejected, while `ab` is treated as one variable name. An adapter must
resolve implicit multiplication using our mathematical notation conventions.

The numerical evaluator handles square roots and logarithms in these probes.
It does not evaluate `sec`, `csc`, or `cot`; reciprocal rewrites could add those.
Bare `i` is an undefined variable; the evaluator can represent explicit complex
literals, while `evaluate_with_vars` returns only real-number results.

`0*(1/0)` evaluates as a division-by-zero error but simplifies to zero. Domain
information must therefore be preserved separately if the simplifier is used.

These findings agree with the public implementation of the
[simplifier](https://docs.rs/mathcore/0.3.1/src/mathcore/lib.rs.html),
[parser](https://docs.rs/mathcore/0.3.1/src/mathcore/parser/mod.rs.html), and
[expression types](https://docs.rs/mathcore/0.3.1/src/mathcore/types/mod.rs.html).
This evaluation does not claim to cover an unreleased GitHub branch.

## Recommendation

Do not add MathCore as the production symbolic grader. It could serve as a
limited numerical evaluator after notation conversion, but the crucial work
would remain ours: safe parsing, exact algebraic equivalence, function rewrites,
domains, special answers, and structured response semantics.

A narrower Rust checker for polynomial/rational expressions, radicals, common
functions, and explicit special tokens is a viable direction. Numerical
substitution can demonstrate that two expressions differ; matching samples
alone does not prove equivalence. That implementation or another library needs
its own evaluation before we enable the remaining questions.

## Reproduce

From the repository root:

```sh
python3 reference/mathcore-evaluation-2026-10-05/prepare_probe.py
CARGO_TARGET_DIR=/tmp/course-academy-mathcore-evaluation/target cargo run \
  --offline --locked --release \
  --manifest-path reference/mathcore-evaluation-2026-10-05/Cargo.toml -- \
  reference/mathcore-evaluation-2026-10-05/inputs.json \
  reference/mathcore-evaluation-2026-10-05/results.json
```

Offline reproduction requires the locked dependencies to be cached. The
JSON inputs and results, source-content SHA-256, Cargo lockfile, and probe code
are retained here. `summary.json` records the counts. All timings in
`results.json` describe one probe run, not a performance benchmark.
