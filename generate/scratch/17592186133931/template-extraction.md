# Template extraction

## 1. Describe each original before generalizing

The classification table records every individual practice source and its complete bank. `source.json` preserves the raw record, including all original identifiers, attribute omissions and exact string bytes. `source-cases.json` maps every source to a public replay with complete parameters/profile; `review.md` prints each original in full.

All ten flux prompts specify six planes bounding a rectangular prism, positive outward orientation and a three-component vector field. Nine are moderate and have the common theorem prose followed by three formal held partials, three substituted terms (zero terms retained), reduced divergence, triple-integral theorem application, repeated integral in dz dy dx order, three separated integrals, three primitives/width differences, individually substituted or evaluated endpoints and final scalar. `cos`, `log`, and `exp` include a further reduction row. `affine` has an additive x primitive and omits its redundant lower zero sum. `xy_a` places the factor 3 in the z integral; `xy_b` splits 4 as 2x times 2y; cancellation families retain signed terms before collection. The unrated `xz` source lacks a solution and correct ref entirely.

The remaining moderate blank preserves a long captured whitespace/layout, a supplied repeated integral ending at `4-x-y`, and `{{field-1}}` for only the missing integrand. It references a missing prior field/region; the worked solution says “In part 1, we found that” div F = 2x. It neither assesses evaluation nor supplies a self-contained mathematical premise. Full context is unresolved; fragment/layout fidelity and native fragment grading are still required.

The source `exp` bank has ordinary single-backslash TeX commands and U+2061 function-application characters. Decoded byte inspection disproved a doubled-slash anomaly; no normalization or repair was made.

## 2. Generalized pattern and purpose

Compute outward flux through the boundary of a rectangular box by the divergence theorem. Differentiate each component with respect to its matching coordinate, holding the other two coordinates fixed; combine the divergence; integrate it over the displayed box. Maintain source-specific allocations of constant factors, integration order and endpoint stages. The normal learner response remains a scalar radio answer, five options, key `selection`; the raw context fragment remains a one-choice blank, key `field-1`.

## 3. Components and complete observed bank mappings

Fixed components: original prose and vector field per family, positive orientation, theorem statement, formal partial terms, source factorization and row sequence. Variable components: six complete boundary-equation slots and all corresponding integral limits, primitive substitutions, endpoint evaluations and final result. No naked digit replacement is used in prose or field formulas. The exact original primitive-limit spelling is retained at its parameter value (for example pi/2 and operatorname ln 3).

| Template | Original box (x; y; z) | Separated factors | Primitives / width stages |
|---|---|---|---|
| xz | [−1,1]; [0,1]; [0,1] | 1; 1; 2z | x width; y width; z² |
| cos | [0,2]; [0,1]; [0,pi/2] | 2x; 1; cos z | x²; y width; sin z, then familiar sine evaluation |
| xy_a | [0,2]; [0,4]; [1,2] | x; y; 3 | x²/2; y²/2; 3z |
| log | [1,e]; [0,2]; [0,2] | 1/x; y; 1 | ln x; y²/2; z, followed by three individually reduced differences |
| affine | [0,1]; [1,2]; [1,3] | 2x+2; 1; 1 | x²+2x; y/z widths |
| xy_b | [0,1]; [1,2]; [−1,1] | 2x; 2y; 1 | x²; y²; z width |
| cancel_x | [1,3]; [0,2]; [−1,1] | 2x; 1; 1 | x²; y/z widths |
| cancel_x2 | [−1,1]; [0,3]; [1,3] | 3x²; 1; 1 | x³; y/z widths; preserve signed cubed endpoints before evaluation |
| cancel_z | [−1,2]; [0,1]; [−1,2] | 1; 1; 4z | x/y widths; 2z² |
| exp | [0,1]; [1,3]; [0,ln 3] | 3x²; 1; e^z | x³; y width; e^z, then individually evaluate exponential endpoints |

For each scalar option v in the full classification bank, explicit raw profile recipe is `v * A/A₀`, where A is the parameterized flux and A₀ is its original flux (2,4,48,4,6,6,32,12,18,4 respectively). This is an observed numerical pattern, not a recovered learner error. The exponential profile's two log options are explicitly `2*(z₁−z₀)` and `(z₁−z₀)/2`, preserving their original TeX at `[0,ln 3]`; other members use the scalar pattern. All 51 values are accounted for and all eleven complete banks replay. Original correct designation is preserved when present; the missing `xz` designation does not count as a recovered source designation. The blank profile is `c*x` with original c=2 and cap=4; only its fragment is independently recoverable.

Observed distractor intentions remain underdetermined for every scalar bank. Consequently all raw profiles carry `evidence_only=true`, `eligible_for_learning=false`, including profiles with mathematically correct observed designations. No opaque multiplier is promoted into normal sampling.

## 4. Reusable recipe and proposed domains

Each family has its own fixed field/component and worked-solution recipe. Geometry changes feed every limit/primitive/evaluation slot. Constant fields additionally vary an actual easy field coefficient. Mathematical objects and field-owned UUIDs are exact/deterministic; shuffled option order does not change content identity. Fingerprints exclude bank/profile/seed aliases; easy additionally sorts box widths to deduplicate commutative width permutations. Box limits affect evaluated flux and therefore are substantive parameters in full flux families. The context-setup fingerprint excludes its unused cap bound.

Normal moderate samplers choose one of all ten supported flux families before sampling limits. Integer boxes sample ten explicitly enumerated intervals with endpoint magnitudes at most 4. Log x endpoints are e^k, k=0..3, strictly ordered and positive, so the ln derivative is valid throughout the box. Cos z endpoints are ordered familiar half-pi multiples from −pi/2 through 3pi/2. Exponential z endpoints are ln(k), k=1..5. Integer/half-pi/log endpoint forms preserve source arithmetic; signs are parenthesized. Explicit parameters obey the same arithmetic ceilings, though ordered integer intervals within that ceiling can be supplied outside the ten sampler intervals.

Authored easy: `<a*x+1,3z,xy>` for integer a=2..9, one nonzero held partial, three distinct widths selected from 2..5, all lower endpoints zero. Exactly the same constant-divergence and three-width product workload throughout. Easy width permutations are presentation aliases; `catalog.json` counts their mathematical tasks once.

Authored hard: canonical `<e^z,x²y²,4x²yz>`, three held partials (two nonzero), combination `6x²y`, separate `3x²` and `2y` integrations, cubic and quadratic endpoint differences, then z width. Both x/y intervals have positive nonzero translated endpoints chosen from (1,2), (1,3), (1,4), (2,3), (2,4); z uses the integer interval catalog. Explicit hard calls also require positive translated endpoints within the same ceiling. No easy/moderate template is served as hard. This adds endpoint bookkeeping within the canonical method, without introducing another theorem, solid, change of coordinates or integration technique.

Every normal bank is a complete authored profile chosen as a unit. The following operations are derived from the actual field/derivative/primitive, rather than unrelated scalar perturbations. Orientation reversal is always the wrong inward sign. Collisions reject the entire instance; no member is replaced or drawn from a pooled first-valid list.

| Family | Other three wrong operations after orientation reversal |
|---|---|
| xz | omit the coefficient in ∂x(2xz); treat z as 1; omit lower z² endpoint |
| cos | omit factor 2 in ∂x(x² cos z); use −cos instead of sin as the cosine primitive; replace cos by 1 before integrating |
| xy_a, xy_b, canonical | omit the second nonzero partial; take each held partial twice; omit z width |
| cancel_x, cancel_x2, cancel_z | drop negative derivative sign before sum; take each held partial twice; omit z width |
| log | omit y factor; differentiate ln x as 1; omit 1/2 in y primitive |
| affine | omit constant partial; omit x partial; omit lower additive-primitive endpoint |
| exp | differentiate e^z as 1; omit lower exponential endpoint; use x² instead of x³ primitive |
| constant | omit x width; omit y width; omit z width |

The default solution is fixed independent of options. `affine` adds an explicitly labeled two-row individual endpoint-term calculation after its unchanged source chain; raw replay has no added rows. Signed endpoint grouping is a presentation extension under changed limits. All other source stage sequences and factorizations remain intact.

## Source anomalies and repairs

17592186134139: absent difficulty/solution/correct designation is preserved in raw evidence. An independent divergence/integral gives flux 2, which exists in the bank. Normal presentation receives an authored moderate label, a supported complete worked solution and a correct ref; no claim of observed designation fidelity is made.

17592186235537: missing preceding context remains unresolved. Authoritative owning lesson JSON/Markdown under `/home/jake/Developer/MA/DATA/Lessons/2135/` corroborates `xz` prompt/bank but contains no recoverable part-1 context for this blank. This source is not silently omitted: public replay, full bank, original whitespace, original worked solution and native fragment checks are all retained. It stays ineligible for normal learning. No mathematical correction or guessed vector field is added.

No other source mathematical error or formatting repair was necessary. Complete raw-exact prompts/solutions and preserved attribute omissions are tested separately from the mathematical correctness of supported normal output. No plots occur; plot extraction stages 5/7 have no assets to inspect or generate.

## Enumerated variation and review evidence

The complete finite normal sampler catalog has 32 easy semantic tasks (excluding all width permutation aliases), 4,715 moderate tasks across all ten supported families, and 100 hard tasks. Per-family candidate and whole-bank eligible counts are in `catalog.json`; invalid zero/equal-value banks do not count. The count concerns assessed field/box objects, never answer-order, bank-profile or seed aliases. Fixed original fields are deliberate: independently changing six meaningful integration limits provides substantial integration practice while preserving the source's derivative and factorization workload. Explicit supported intervals inside the same arithmetic ceiling can enlarge the domain beyond this enumerated sampler; no uncounted enlargement is included in these counts.

`review.json`/`review.md` contain two normal generated variants for each supported family (including each authored level) and two separately labeled ineligible changed-parameter raw-bank variants for each of all eleven observed profiles. Native grading covers every complete review-bank choice; raw missing-correct records remain ungraded as originals. A correlated endpoint mutation adds the same constant to both evaluated endpoints, preserving their final difference; independent individual endpoint checks reject it. Other regressions alter a formal held coordinate, a substituted derivative, the required factorization structure, a primitive and a control character.
