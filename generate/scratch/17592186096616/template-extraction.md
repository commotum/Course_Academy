# Extraction and generation constraints

Source payloads are retained in source.json, original parameter tuples and layouts in source-cases.json. The following formulas account for every source option; source option strings/IDs, fields, correct refs and solutions remain in source.json. Replay validation matches complete banks one-to-one, ignoring order but preserving multiplicity and correct designation. There is no pooling or mixing between profiles.

The shared task is to differentiate y termwise and evaluate y' at a specified positive x. Lowercase parameter names below match source-cases.json. The constant k has its source sign. Rational parameters are reduced. Base b is an integer greater than one; common logarithm keeps b=10. Fixed input t=1 is retained for the legacy, natural-log quadratic radio, and base-log quadratic blank templates. The reciprocal-log radio always uses t=1/ln(b).

| Source | Original function; input | Source option recipes in original stored order |
|---|---|---|
| q-17373 | -(n/d) ln x; n=3,d=5,t=1 | -d/n, 0, n/d, **-n/d**, d/n |
| q-17395 | log_b x+c ln x; b=3,c=5,t=1 | 1/ln b, ln b+c, 0, c/ln b, **1/ln b+c** |
| q-101723 | a e^x-c log_b x; a=4,c=3,b=7,t=3 | No source field; authored scalar a e^t-c/(t ln b) |
| q-340014 | a x²+c ln x; a=5,c=6,t=3 | **2at+c/t** =32 |
| q-340022 | a ln x-c b^x; a=5,c=2,b=3,t=2 | **a/t-c b^t ln b** =5/2-18 ln3 |
| q-340109 | -a e^x+c log_b x; a=3,c=2,b=4,t=2 | **-a e^t+c/(t ln b)** twice in distinct equivalent TeX notations |
| q-70897 | a log_b x+b^x; a=2,b=2,t=2 | No source field; authored scalar a/(t ln b)+b^t ln b |
| q-101726 | ax-k+c log_b x; a=3,k=5,c=8,b=2,t=1/ln b | a+1, a+c ln b, **a+c**, c ln b+a-k, a+c-k |
| q-17371 | a ln x+c x²-kx; a=3,c=2,k=5,t=1 | **S=a+2c-k**, -a, -S, a+2c+k, -k |
| q-340024 | a x³-c log_b x; a=2,c=5,b=3,t=2 | **3at²-c/(t ln b)** =24-5/(2 ln3) |
| q-340026 | a log_b x+c x²-kx; a=6,c=4,k=3,b=2,t=1 | **a/ln b+2c-k** =6/ln2+5 |
| q-340110 | a e^x-c log_b x+k; a=4,c=3,b=2,k=7,t=3 | **a e^t-c/(t ln b)** =4e³-1/ln2 |
| q-70903 | a log x+x³-k; a=3,b=10,k=4,t=3 | at/ln b-t, **a/(t ln b)+3t²**, a/(t² ln b)+t, a/(t ln b)-t², a/ln b+t² |

For q-101726 and q-70903 the original author's mistaken-operation interpretation is unresolved. These are explicit observed expression patterns with narrow fixed polynomial structure, not asserted diagnoses. q-17371's -a similarly preserves an observed term/sign shape without claiming author intent. All 20 existing distractors and the entire five-option banks must replay; correctness tests do not substitute for this requirement.

Sampling is a proposed bounded policy, not recovered original bounds: coefficient and constant magnitudes 1..12, integer bases 2..9 (or fixed common base 10), positive input 1..4 except observed fixed/reciprocal inputs. Signs, degrees, independent variable, source term order, base-sharing, field keys, source choice count and the full selected profile remain fixed. Reduced nonunit fractions avoid equal reciprocal/sign options. Every bank with a collision or second correct value is rejected/resampled; explicit invalid parameters raise an error. All source tuples lie inside these bounds. No signed input is supported because ln(x) requires x>0. This policy has a finite domain; only enumerated/sample-validated capability counts are reported, never an invented exact capacity.

Fixed components: prompt phrasing and radio/blank layout, common introductory sentence, differentiation preamble, concluding slope sentence, termwise differentiation method, derivative/evaluation stage counts. Variable components: function terms, full numeric coefficients, logarithm bases, evaluation values, derivative intermediate terms, complete correct/distractor expressions. Missing fields/solutions are explicitly authored variants. Source TeX components such as ln⁡, log typography and coefficient spacing are standardized to supported LaTeX. Literal source prompt and solution strings are retained for review; fidelity is reported as mathematical/structural, separately from literal fidelity. q-70903's mistaken input in prose is repaired in generated content.

Each generated solution has exactly one fixed worked solution. Derivative rows first differentiate the sum, split terms/coefficient factors as in that source family, show derivative values, and collect the derivative. Evaluation rows substitute the same t, reduce terms, and collect the scalar. Short single-derivative source families retain their shorter sequence. Both introductory sentences and the conclusion scaffold are preserved. No distractor explanations or learner feedback are added. Missing legacy solutions are authored from the same scaffold, with an explicit repair label.

Plot extraction (stage 5) and plot generation (stage 7): not applicable. Every source, option and solution was inspected; none references an image or requires a generated plot. The generated asset map is empty, so stage 8 has no asset publication.

Question UUIDs derive from the full rendered mathematical intent and bank, using the KP's existing UUID namespace. Field UUIDs belong to the question/key, and answer UUIDs belong to their field/value. The generator identity is a stable UUID in that same namespace; registration uses existing schema attributes. Seeds and shuffling only control reproducible sampling/order. A separate fingerprint uses the simplified derivative and evaluation input; constant shifts, alternative answer notation, banks or layouts for the same task never increase the inventory count. Duplicate mathematical tasks anywhere in the KP including the canonical example are excluded from new stock.

Validation reads back displayed prompt and every solution row using an independent bounded TeX parser; computes the derivative from the displayed function; checks canonical answers, blank aliases, radio uniqueness, domains, stage counts and source replay. The real application grader checks every radio option, each blank alias, a separately unreduced equivalent derivative evaluation and an incorrect scalar. The package is frozen only after side-by-side review and passing native grading. See validation.json and review.md for fidelity/correctness/grading evidence.
