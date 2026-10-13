# Four extraction stages

## 1. Specific source descriptions

`classification.md` lists all source-specific representations and image placement. Original complete prompts, solutions, layouts and every option (including the legacy field) are preserved in `source.json`, reproduced in `review.md`, and mapped in `bank-mapping.json`.

q-33728 has sin(2t), cos(3t), bounds 0 to π. Its derivative row, norm of squared derivative components, collected square row, generic integral and final integral are distinct stages. q-33862 is e^t(i+2j+tk), bounds 1 to 2; the product derivative remains unevaluated as te^t+e^t, then norm, expansion, exponential factoring and positive exponential extraction. q-127419 pairs coefficient 4 on cos t/sin t with coefficient 3 on a second sin t; expansion, Pythagorean grouping and simplification precede its π/6 to π/4 integral. q-127427 has cos t+sin t, e^t, sin t−cos t over −1 to 1; the two trig derivative squares expand, cancel cross terms and group an identity, before its final integral. q-33857 uses sin 2t, cos 2t, t² over 0 to 1, then three squares, expanded sum, common-factor grouping and simplified speed. q-33706 uses t sin t, 2−t cos t on 0 to π, two product derivatives and six expanded square terms before cancellation. q-64723 is a unit helix in basis notation on 0 to 2π, with three derivative squares, expanded identity and constant speed. q-64724 has t³i+3tj+t⁴k on 2 to 5 and three squared power derivatives. Last four sources combine the generic and final integral on one row; the earlier sources use two rows.

## 2. Shared pattern

Differentiate every component of the displayed vector-valued curve, take the nonnegative Euclidean magnitude, and select the complete integral on the stated interval with differential dt. Do not evaluate that integral. Different source stages/representations stay separate templates.

## 3. Components and full banks

`bank-mapping.json` preserves each raw field, every answer UUID/value and correct designation, profile, parameters and the complete generalized integral object. `source_bank` in the script records every operation formula. Bounds are part of each option, including 0→1 errors, shifted bounds and half-upper-bound errors; multipliers outside source integrals are compared as part of the complete speed. All 45 displayed source values across nine banks must match one-to-one, allowing complete mathematical equivalence.

Observed recipes are explicit replay profiles. Chain-factor/square omissions, switched trig functions, omitted terms and changed limits can be interpreted from the method. Unexplained constants such as q-33862's t²+2t+4 or q-127427's prefactors do not identify an error algorithm. Their parameterized expression patterns are retained without claiming recovered author intent. Every observed bank is selected whole, never filled from a distractor pool.

Normal authored bank: correct speed; magnitude of original position vector; norm omitting last differentiated component; squared speed in place of speed; correct speed with upper endpoint increased by one. Each of its five operations depends on the assessed method. Equivalent or ambiguous complete choices reject the entire instance. Source profiles retain the original q-33857 non-real distractor radicand near t=1 as historical evidence; normal authored banks are nonnegative real throughout their intervals.

## 4. Reusable template

Fixed shared sentences: “First, we find … and …:” and “Therefore, the arc length of the curve is” with the source colon retained where present. Variable slots are whole coordinate components, whole derivative components, complete norm stages, full bounds and complete integrals. Tuple/basis layout, prompt newline and final integral row count follow the source. Standard TeX notation replaces Unicode norm, angle, prime and invisible trig application characters. Vector derivatives are not obtained by textual symbol replacement. Ordered unevaluated sums/products preserve expansion and factoring stages; only the final speed is simplified. No distractor diagnosis appears in learner content.

Sampling varies substantive coefficients, frequencies, compatible powers and interval data; shift h in the spiral is incidental to the assessed speed and excluded from its task fingerprint. Mathematical identity is canonical speed squared plus both bounds and dt, excluding bank, profile, rendering and incidental shifts. Content identity includes full prompt, solution, sorted complete bank, version and mathematical fingerprint; shuffling cannot create a new content identity. IDs are field-owned UUIDs and local JSON uses schema-shaped leading-colon keys only. Nothing is registered or transacted.

Repairs: q-33728 duplicate field is removed from normal layout and the missing legacy designation inferred independently, reported unavailable for fidelity. q-33857's first generic integral originally says 1→2 while its prompt and correct final integral say 0→1; the generic integral is repaired to the stated interval. Seven exact mathematical source solutions and one repaired mathematical solution are reported separately. Original raw prose remains evidence.
