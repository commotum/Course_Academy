# Classification

Captured source: database **math**, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the unchanged capture wrapper. There are 22 practice questions: 11 five-choice radios and 11 one-answer blanks, all observed **moderate**. No practice source is unrated, fieldless, or missing a correct reference. The blank key is `field-1` and appears in each prompt; radio key is `selection`.

All assess a single unknown component using zero scalar projection, perpendicularity, dot product zero, and a nondegenerate linear equation. Layouts are angle tuples, column vectors, and basis notation. There are six layout/field families, with **16 distinct detailed Markdown/value stage masks** after preserving term order, row count, pre-evaluated products, and formal-product notation. The implementation exposes 22 source-specific recipe names, rather than falsely identifying changed numbers as different skills. Each source radio bank has its own complete explicit profile: 11 profiles, totaling 55 choices. Blanks contribute another 11 values.

| Detailed mask | Sources | Fields | Plot rating |
|---|---|---|---|
| 1: angle; x term first; direct solve; dot=0 row; component products; formal multiplication signs | q-236734 | radio | none |
| 2: column; x term first; isolation row; dot=0 row; component products; formal multiplication signs | q-236735, q-237014 | radio | none |
| 3: column; constant first; isolation row; dot=0 row; component products; formal multiplication signs | q-237015, q-237016 | radio | none |
| 4: basis; x term first; direct solve; dot=0 row; component products; formal multiplication signs | q-237017 | radio | none |
| 5: basis; x term first; isolation row; dot=0 row; component products; formal multiplication signs | q-237018 | radio | none |
| 6: angle; x term first; isolation row; dot=0 row; component products; formal multiplication signs | q-237020, q-237021, q-237022 | radio | none |
| 7: angle; constant first; isolation row; dot=0 row; component products; formal multiplication signs | q-275253 | blank | none |
| 8: column; x term first; isolation row; dot=0 row; component products; formal multiplication signs | q-275256 | blank | none |
| 9: angle; x term first; isolation row; dot=0 row; component products; formal multiplication signs | q-319150 | blank | none |
| 10: angle; x term first; direct solve; dot=0 row; component products; formal multiplication signs | q-319171 | blank | none |
| 11: angle; x term first; isolation row; dot=0 row; evaluated products; formal multiplication signs | q-319172 | blank | none |
| 12: basis; x term first; isolation row; dot=0 row; component products; formal multiplication signs | q-319252 | blank | none |
| 13: basis; constant first; isolation row; dot=0 row; component products; formal multiplication signs | q-319253, q-319254 | blank | none |
| 14: column; x term first; direct solve; dot=0 row; component products; formal multiplication signs | q-319255 | blank | none |
| 15: column; x term first; isolation row; start at reduced equation; component products; formal juxtaposition | q-319256, q-319257 | blank | none |
| 16: basis; constant first; isolation row; dot=0 row; component products; formal multiplication signs | q-237019 | radio | none |

The canonical example embeds two raster-rendered column vectors, a=(0,0,1) and b=(2,-4,0). These are typeset mathematical expressions, not diagrams. Both were visually inspected; no plotted geometry or arrows are involved. Practice prompts have no images. Plot generator is therefore not required.

## Curriculum and authored missing levels

The lesson route is reconstructed from activity first-step then step next, not array order: Introduction → Negative Scalar Projections → angles/magnitudes KP → Deriving a General Formula → components KP → Projecting Perpendicular Vectors → this KP. The immediately preceding tutorial explicitly states comp_b(a)=0 iff nonzero a and b are perpendicular; it also notes the reverse projection is zero. The component formula and solving a simple linear equation are already used in the observed questions. Vector projection is a later separate topic and is excluded.

**Easy (authored):** infer zero from supplied perpendicularity, either directly or as a 90-degree angle. The two information forms are presentations of **one mathematical recognition task**, not two new tasks. There are no magnitude, letter, number, bank, layout, or projection-direction parameters padding diversity. Both generator entrypoints and review are available; repeated easy practice has a genuine finite limit of one assessed outcome.

**Moderate (observed):** exactly one unknown component in one coordinate; three component-product slots, at most two nonzero known products; sign, zero, nonzero radical times zero, and integer/rational solved values retain the observed arithmetic route. Default coordinates are integers in [-6,6] with template zero/nonzero structure and coefficient-unit/zero-constant stage categories preserved. Original replay permits up to magnitude 15, preserving the source 15 input. Explicit parameters obey the same bounds and masks as sampling.

**Hard (authored):** p=(x,a,b), q=(c,x,d), all supplied coefficients nonzero integers with magnitude at most 6. The dot product has exactly two nonzero linear contributions cx and ax and one nonzero known product bd. Students collect the two x terms and then solve the same zero dot-product equation. Require a≠c and 2≤|a+c|≤12; no cancellation or unit sum can collapse the collection demand. No x*x products, quadratics, vector projection, angle calculation, norm simplification, or extra branches. Both blanks and five-choice radios use this fixed workload. This is a documented authored difficulty design, not a recovered historical label.

## Source anomalies and eligibility

Practice q-275256 (17592186292830) prints vectors a,b but names p,q throughout its solution. Its numerical products and answer -4 are correct. Raw observed replay retains exact prose and names; it is evidence-only. Normal output performs the minimal p→a, q→b repair without altering stages or values. The canonical example has c_z where a_z is intended in the formal numerator; its actual substitution is correct. This canonical typo is documented and not copied into generated lessons.

Source radio distractor intent is underdetermined. Exact observed banks are public `observed:q-*` evidence profiles, with explicit opaque proportional value patterns. They are never sampled as normal learner defaults. All normal radio families retain the source prompt and solution masks and use complete method-derived authored banks selected before parameters. Source correct refs, full values, layout, and prose are verified independently of native ID grading.

The finite hard coefficient domain is enumerated in `finite-domains.json`: 14,400 valid blank parameter tuples reduce to 768 mathematical tasks under the stated normalized-contribution fingerprint; 10,656 eligible radio tuples reduce to 714 tasks after rejecting equivalent complete-bank values. Factorization, letter, layout, bank, and common-scale aliases are excluded. Moderate sampling validation gives a checked lower bound of 141 meaningful fingerprints in 200 default seeds, rather than claiming a fully enumerated domain.
