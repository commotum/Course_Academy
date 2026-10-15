# Current source classification and generator scope

Database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, basis 2603.
The complete current Pull is retained in `reference/replenishment/initial-read/kp.edn`
and its JSON projection in `kp.json`. These supersede the inventory observations
in the historical basis-1356 classification without rewriting that evidence.

All 12 current practice records are moderate, with one five-choice math radio
field keyed `selection`. No prompt, choice, or solution needs a plot. All correct
scalars and complete banks were checked independently from the displayed
coordinate maps, original integrands, and region inequalities. The native grader
accepted all 12 correct choices and rejected all 48 alternatives.

The original seven families retain their original complete banks. Previously
missing difficulty, solutions, and keys have been supplied in the database;
the old raw replay preserves the historical omissions and remains evidence-only.
The generator's existing seven-family mathematical validation remains applicable
to its normal authored method banks. It does not claim fidelity to the five
additional families below.

| Source | Template and supplied coordinates | Transformed density before Jacobian | Box | Correct scalar |
|---|---|---|---|---|
| 17592186482530 / q-161894 | Linear sine product: u=x+y, v=y+z, w=z | sin(u)sin(v) | [π,2π]×[0,π]×[0,1] | −4 |
| 17592186482599 / q-161933 | Quotient/log primitive: u=y+z, v=x+4z, w=2y | u/v | [0,2]×[1,e]×[0,2] | 2 |
| 17592186482606 / q-162140 | High power with quadratic y shear: u=x+y², v=y+z, w=z | u⁹w | [0,1]×[0,5]×[0,4] | 4 |
| 17592186499491 / q-161893 | Linear mixed exponential: u=x+y, v=y−x, w=z | u exp(v) | [1,2]×[0,1]×[0,3] | 9(e−1)/4 |
| 17592186522780 / q-162128 | Arctangent primitive: u=2x+y, v=3x+2z, w=z | 12/(1+v²) | [1/π,2/π]×[0,1]×[0,2] | 2 |

Each additional source is a separate template/profile with plot rating **none**.
Their complete observed scalar banks, ignoring order, are respectively:

- q-161894: −2, 2π, −4, π, 2.
- q-161933: 4, 2, 1, ln(2), 2ln(2).
- q-162140: 4, 6, 5, 8, 9.
- q-161893: 3e, (e−1)/3, 3e/2, 9(e−1)/4, 3e+2.
- q-162128: π/3, 1, 2, 4, π.

These are captured banks, not inferred distractor recipes. Every option is
retained with its original field and identity in the source snapshot. None of
these five profiles is sampled by the generator. Their regeneration is outside
this package's bounded seven-family capability; no wider coverage is claimed.
This restriction does not prevent replenishment at any difficulty, because the
validated domains already provide distinct questions in all three bands.

All five additional solutions follow the same four stages: box, forward
Jacobian, inverse Jacobian, and transformed integration. Their primitive stages
differ as shown above, so they are not folded into existing masks merely because
the introductory prose matches. Observed coefficients and endpoints are retained
for source checks only; no new sampler bounds are inferred for these families.

Two source presentation defects exclude those records from the conservative
usable inventory count: q-161916 has an unmatched endpoint parenthesis, and
q-162140 states w≤2 in Step 1 although its region, integral, and answer use w≤4.
q-161894 and q-161893 show an inconsistent signed Jacobian inside absolute-value
bars in Step 4; their absolute values and computed integrals remain correct.
All sources are preserved unchanged. No source defect is copied into generated
learner records.

The supported easy/moderate/hard domains and complete authored method recipes
remain those in `template-extraction.md`. Replenishment checks every selected
instance with the independent rendered-prompt/solution validator and the native
grader. Deduplication uses the original-coordinate integrand and normalized region,
excluding seed, UUID, answer ordering, solution wording, and coordinate scale.
