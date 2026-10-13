# Step 4 — template extraction

## 1. Specific source descriptions

Every source uses a prose prompt supplying a minimum and maximum ordinate, then asks for the complete equation of the midline. No independent-variable values, graph-reading, period calculation, units, or rounding are present. Supplied numbers are small signed integers; extrema are ordered strictly. Radio choices are complete equations y=constant, not constants or equation fragments. Source choices have five distinct mathematical values. The shared solution gives the definition, generic average formula, explanatory sentence, substitution, numerator sum, final division, and “Therefore” equation. A negative maximum is parenthesized in the substitution row (q236903). q236750 has no captured solution; the two fieldless sources nevertheless have full solutions.

- **q-236750**: -9 ≤ extrema ≤ 1; average -4; sine prompt. Correct designation or entire field missing; preserved as captured.
- **q-236896**: -5 ≤ extrema ≤ 9; average 2; cosine prompt. Radio correct equation y=2.
- **q-236892**: 0 ≤ extrema ≤ 4; average 2; sine prompt. Correct designation or entire field missing; preserved as captured.
- **q-236903**: -14 ≤ extrema ≤ -4; average -9; cosine prompt. Correct designation or entire field missing; preserved as captured.
- **q-236890**: 2 ≤ extrema ≤ 10; average 6; sine prompt. Radio correct equation y=6.
- **q-236893**: -7 ≤ extrema ≤ 3; average -2; sine prompt. Radio correct equation y=-2.
- **q-236899**: 6 ≤ extrema ≤ 10; average 8; cosine prompt. Radio correct equation y=8.
- **q-236901**: 3 ≤ extrema ≤ 15; average 9; cosine prompt. Radio correct equation y=9.

## 2. Generalized pattern

For finite exact extrema L<U, compute M=(L+U)/2, and return the horizontal-line equation y=M. One fixed solution is independent of chosen response. Sinusoidal subtype is a presentation label and does not alter the operation.

## 3. Components and every observed choice

Prompt slots: entire minimum component, entire maximum component, sine/cosine word, and source terminal punctuation. Solution slots: substitution numerator, collected sum, final mean, concluding equation. Let M=(L+U)/2 and R=(U-L)/2. Below, `M+cR` is an **opaque affine evidence position**, not a claimed misconception. It gives an exact parameterized geometric coordinate for every whole RHS, retains the observed joint bank, and is ineligible for defaults. “Correct” below means captured designation; “inferred mean” is separate.

| Source/profile | Original complete option | Position recipe | Designation |
|---|---|---|---|
| raw_q-236750 | `y =-4` | M + (0)R | inferred mean; key absent |
| raw_q-236750 | `y =-9` | M + (-1)R | wrong value |
| raw_q-236750 | `y = 1` | M + (1)R | wrong value |
| raw_q-236750 | `y = 5` | M + (9/5)R | wrong value |
| raw_q-236750 | `y =-5` | M + (-1/5)R | wrong value |
| raw_q-236896 | `y=7` | M + (5/7)R | wrong value |
| raw_q-236896 | `y=9` | M + (1)R | wrong value |
| raw_q-236896 | `y=2` | M + (0)R | captured correct |
| raw_q-236896 | `y=-4` | M + (-6/7)R | wrong value |
| raw_q-236896 | `y=-5` | M + (-1)R | wrong value |
| raw_q-236892 | no captured options | field-presence omission | none |
| raw_q-236903 | no captured options | field-presence omission | none |
| raw_q-236890 | `y=10` | M + (1)R | wrong value |
| raw_q-236890 | `y=5` | M + (-1/4)R | wrong value |
| raw_q-236890 | `y=6` | M + (0)R | captured correct |
| raw_q-236890 | `y=9` | M + (3/4)R | wrong value |
| raw_q-236890 | `y=2` | M + (-1)R | wrong value |
| raw_q-236893 | `y=-2` | M + (0)R | captured correct |
| raw_q-236893 | `y=-4` | M + (-2/5)R | wrong value |
| raw_q-236893 | `y=-7` | M + (-1)R | wrong value |
| raw_q-236893 | `y=3` | M + (1)R | wrong value |
| raw_q-236893 | `y=0` | M + (2/5)R | wrong value |
| raw_q-236899 | `y=7` | M + (-1/2)R | wrong value |
| raw_q-236899 | `y=9` | M + (1/2)R | wrong value |
| raw_q-236899 | `y=6` | M + (-1)R | wrong value |
| raw_q-236899 | `y=8` | M + (0)R | captured correct |
| raw_q-236899 | `y=10` | M + (1)R | wrong value |
| raw_q-236901 | `y=3` | M + (-1)R | wrong value |
| raw_q-236901 | `y=12` | M + (1/2)R | wrong value |
| raw_q-236901 | `y=6` | M + (-1/2)R | wrong value |
| raw_q-236901 | `y=15` | M + (1)R | wrong value |
| raw_q-236901 | `y=9` | M + (0)R | captured correct |

All 30 options in six banks replay lexically, not only algebraically; five correct designations match. Unresolved historical wrong-operation intent is not promoted to recovered recipes. Raw variants preserve whitespace around equals and the whole source RHS slot. Bank values are generated from M and R; there is no payload-return branch or answer lookup table.

## 4. Reusable masks, domains, and complete authored banks

The generator builds the source prompt and shared source solution by complete mathematical slots. The exact easy worked solution is common across all seven supplied solutions, including their whitespace and three ordered aligned rows. The raw q236750 profile emits no solution/difficulty/correct key; raw fieldless profiles omit answer-fields rather than producing an empty list. Source math-academy and database IDs remain evidence attributes only; generated identity is content-derived.

Normal complete banks are chosen before parameter sampling:

- `method_average`: [M,L,U,(U-L)/2,L+U]. Errors respectively use an extremum, compute half-range instead of average, or omit division by two.
- `method_reverse_difference`: [M,L,U,(L-U)/2,L+U]. Errors use an extremum, subtract instead of adding, or omit division by two.
- `zero_minimum`: [M,L,U,-U,-(L+U)/2], eligible only for L=0. These are extremum use, maximum sign reversal, and mean sign reversal. It avoids the half-range/mean equality at a zero minimum.
- `zero_maximum`: [M,L,U,-L,-(L+U)/2], eligible only for U=0, with analogous minimum sign reversal.

All five members are computed together; any equivalence rejects the entire instance. No pooled first-valid replacements. Zero banks are separate eligible profiles; hard excludes them because both extrema must be nonintegral. Different field presence and complete displayed banks determine different content identities. Explicit parameters obey identical workload and collision rules; malformed/unknown parameters never resample. Raw changed-parameter evidence remains evidence-only and is not a workload claim.

The hard solution adds a distinct LCD-conversion row with two unevaluated common-denominator fractions before collecting the sum. Every displayed equality, including generic mean formula and final prose conclusion, is independently parsed from learner output. Half-integer moderate answers are exact, without invented rounding instructions. No added distractor diagnosis appears in learner content.

Source-format anomalies and independent repairs are in source-anomalies.json; exact fidelity, correct mathematics, and native grading have separate denominators in validation.json. Decoded backslash bytes are audited in tex-byte-audit.json; adjacent backslashes are valid aligned-row separators. No source TeX anomaly or repair is claimed.
