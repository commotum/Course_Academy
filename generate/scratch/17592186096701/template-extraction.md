# Four extraction stages

## 1. Each specific source

`source.json` contains every full prompt, field, bank, correct designation and complete fixed worked solution. `source-cases.json` maps every source to original exact parameters and its complete replay profile. `profiles.json` stores math-component masks, all option-to-target ratios, original number presentation styles, and the two original plot roles. `review.md` prints raw originals and generated replays/peers.

| Source | Level | Unknown | Known coefficient | Correct scalar | Field | Original complete bank |
|---|---|---|---|---|---|---|
| q-19338 | E | b | a | 5/2 | radio | -2,5,2.5,2,1 |
| q-20435 | M | a | 3b | 1/2 | radio | -2,1,2,3/2,1/2 |
| q-120244 | E | b | a | 2 | radio | 2,1,3,2.5,1.5 |
| q-120245 | M | a | 3b | 2 | radio | 2.5,1.5,2,3,1 |
| q-275120 | M | a | 3b | 3 | blank | 3 |
| q-321299 | E | b | a | 2/3 | blank | 2/3 |
| q-327046 | M | b | a | 2 | blank | 2 |
| q-327049 | M | a | 2b | 1/2 | blank | 1/2 |
| q-70140 | E | b | a | 3 | radio | 2,2.5,3,3.5,1.5 |
| q-70141 | E | b | a | 1/2 | radio | 1/4,4,1/2,1.5,2 |
| q-70149 | E | b | a | 3/2 | radio | 1.5,2.5,2,3.5,1.75 |
| q-70187 | E | a | b | 4 | radio | 8,3,4,2,6 |
| q-120250 | M | a | 3b | 1 | radio | 2.5,2,0.5,1.5,1 |
| q-77230 | M | a | 2b | 3 | radio | 3,1,2,-3,-2 |

The table writes fractions compactly for readability; exact valid single-backslash source TeX remains unchanged in `source.json` and replay banks. Source fractions, decimal scalars, positive same-direction vectors, simple square-grid reads and diagram-first layout are material features.

## 2. General pattern

Trace the known component from O; its endpoint determines the remaining vector to C. Use the grid to compare that vector with the unknown basis vector. Because a and b are nonparallel, match its coefficient with the scalar in the given combination. Blanks ask for the scalar fragment, not a vector or equation.

## 3. Component mapping and interpretation limits

Every observed answer is mapped one-to-one in `profiles.json`: recipe `scalar * bank_ratios[i]` with presentation `bank_styles[i]`. These measured option/target ratios are explicit replay expressions and intentionally **do not infer a student's mistake**. There is insufficient evidence to recover the numeric bank author's intent. They are available only by named observed profile; normal generation uses an independently labeled authored complete operation bank. Source selection, correct membership, all ten banks and four blank fragments are tested independently.

The authored radio bank is chosen as a whole: correct λ; -λ (reverse direction); 1/λ (invert length ratio); λ times the relevant basis-coordinate magnitude (omit normalization); and, for easy, λ+k (add unlike scalar contributions), or for moderate/hard, the unadjusted endpoint coordinate divided by the unknown basis coordinate (fail to remove the known component). Any equality among its five complete values rejects the whole instance. No pooled first-valid distractors or random numerical perturbations are used. These operations are author metadata, with no new learner-facing diagnosis.

## 4. Reusable templates and calculations

Fixed source prose and ordered equation rows are masks. Only complete supplied combinations, component vector terms, length ratios, and scalar answer slots vary. Commands, single-letter vector labels and triangle names are not globally substituted. Known-unit OA/AC and OB/BC sequences, known-multiple OP/PC with the P introduction, q-77230's shorter OB/BC path, final equation ordering and punctuation retain their full observed shape on replay.

Compute C=ca·a+cb·b exactly, P=known·known_basis and C−P. The solution keeps the formal path sum and the coefficient substitution as two distinct unevaluated aligned rows. Hard adds the fractional endpoint and horizontal subtraction/normalization before these common stages. Basis coordinates are bounded integers, both coefficients positive and determinant nonzero. See script sections and classification for enforced level-specific bounds.

Mathematical identity consists of unknown role, reduced exact coefficients and the primitive basis geometry, with global vector/grid scaling removed. It excludes bank/profile, option order, labels and seed. Full presentation identity includes displayed prompt, fixed solution, complete bank, field layout, mathematical task fingerprint and generator version. A profile alias or unused seed does not create content identity. Geometry differences are counted only after primitive normalization; the finite sampled domain is reported separately from actually rendered records.

Observed replay profiles preserve their original basis geometry, known coefficient and unknown role. Their variable target scalar has denominator at most 3 for easy (value ≤5) or 2 for moderate (value ≤4). This supports each observed scalar recipe without silently admitting arbitrary fractional workloads or a new geometry family. Normal authored samplers enforce their narrower bounds separately.
