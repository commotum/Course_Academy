# Current source reconciliation

Database math, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1, captured basis 2660. `initial-kp.edn` is the complete current source read, including all seven practice questions, field-owned banks, correct references, worked solutions, plots and canonical example. The earlier frozen generator uses basis 1356. Current reads under api.lock must match this new snapshot before submission.

| Source | Rating | Field and bank | Template and supplied objects | Plots | Generation scope |
|---|---|---|---|---|---|
| q-160365 / 17592186129504 | easy (now complete) | radio, 5 scalar math answers | u=y−2x, v=y+x; four lines; area | light | Existing linear_legacy; old raw missing fields preserved as historical evidence |
| q-160379 / 17592186129506 | absent | radio, 5 math answers; no key or solution | u=y/x², v=xy; positive quadratic/hyperbolic boundaries | none in capture | Existing quotient, authored moderate completion only; source excluded |
| q-160870 / 17592186371899 | easy | radio, 5 rational math answers | u=y−3x, v=y+2x; four lines; area | light | Existing linear; first-quadrant source conflict excluded |
| q-160891 / 17592186371913 | moderate | radio, 5 log math answers | u=1/(xy), v=x²y; reciprocal curves | light | Existing reciprocal |
| q-160875 / 17592186491983 | easy | radio, 5 scalar math answers | u=2y−x, v=y−x; four positive-slope lines | light | Newly classified source-only family; negative v rectangle outside sampler |
| q-160893 / 17592186491996 | moderate | radio, 5 scalar/log math answers | u=y/x², v=y²/x; two y=quadratic and two x=quadratic boundaries | light | Newly classified source-only family; second coordinate differs from existing quotient |
| q-160892 / 17592186492063 | moderate | radio, 5 log math answers | u=x²/y, v=xy; quadratic/hyperbolic curves | light | Newly classified source-only family; reciprocal of existing quotient coordinate |

Every source asks for scalar area and uses one five-option field. Completed solutions use boundary substitution, rectangle, derivative matrix/determinant, reciprocal determinant and absolute-Jacobian integration. All new plots were inspected: q-160875 shows [-2,2]×[-2,-1], red top and blue bottom, guides upwards to the zero axis; q-160893 shows [1,3]×[1,4], blue top and red bottom; q-160892 reuses [1,3]×[2,4]. Plots sit in Step 1 only; they are filled rectangles with all edges included, arrowed axes and a Δ label. No new source plot is silently fed into the existing positive-v renderer.

## New family extraction and complete banks

q-160875 gives lines y=1+x/2, y=−1+x/2, y=x−1, y=x−2. Boundary images are u=2,−2 and v=−1,−2; determinant 1. Full rectangle gives area A=4, but y=u−v is negative on part of the rectangle. Exact first-quadrant clipping gives **7/2**, absent from its bank. Observed ordered bank is [4,2/3,4/3,1/3,2], keyed 4. A complete expression profile at the source anchor is [A,A/6,A/3,A/12,A/2]; the fractions are opaque source ratios with unresolved error interpretations, not asserted generalized pedagogy. Source is retained and excluded from validated inventory. General sampling of a full negative-v rectangle with this map requires a prompt repair or extra geometric restrictions, so this family is explicitly outside the frozen sampler.

q-160893 gives y=x², y=3x², x=y², x=y²/4. Rectangle [L,H]×[j,k]=[1,3]×[1,4], determinant −3y²/x⁴, inverse −1/(3u²), A=(k−j)(1/L−1/H)/3=2/3. Ordered bank [1/3,ln3/3,ln3,2ln3/3,2/3], keyed 2/3. One exact recorded expression profile is [A/2,R/3,R,(H−L)R/3,A] with R=ln(H/L); interpretation of the logarithmic distractors is unresolved. This is a source-only extraction, not a claim of new-bank generalized fidelity. Its source nested integral reverses written differential order; separated integrals and final value agree. The sampler retains its previously validated families instead of changing the supplied second coordinate.

q-160892 gives y=x², y=x²/3, y=2/x, y=4/x. Rectangle [1,3]×[2,4], determinant 3x²/y=3u, inverse 1/(3u), A=(k−j)ln(H/L)/3=2ln3/3. Ordered complete bank [2ln3/3,ln3/3,3ln3/2,ln3,ln3/2], keyed 2ln3/3. With Z=k−j,R=ln(H/L), a recorded profile [ZR/3,R/3,3R/Z,R,R/Z] reproduces 5/5 values; 3R/Z has an unresolved error interpretation. This does not silently replace U by its reciprocal in the frozen quotient family. Source differential-order issue is preserved and documented.

q-160365 is now complete; its key 2/3 is correct in the first quadrant. Its boundary minimum x=0,y=1/3 is nonnegative. q-160870 still has the previously established literal area 89/60 versus key 8/5. q-160891 has area ln3/6; its sign inside absolute value is harmless, while its nested differential order is inconsistent with its separated integrals. No source is edited by this work.

## Frozen package and replenishment decisions

The existing generator retains source-bank replay of all four frozen profiles (20/20 choices), explicit raw evidence-only output, repaired normal prompts/solutions, seeded exact samplers and native five-choice grading. New source-only families above are classified and independently checked for current inventory, with **no claim of new-family replay fidelity or sampling support**. These are bounded template coverage exclusions, not unsupported difficulty levels. Existing easy and moderate templates can fill those bands with mathematically distinct boundary sets. The validated hard extension fixes cubic exponent 3 and nonunit c,d in u=c/(xy),v=d x³y, uses inverse c/(2u²v), and preserves the same four instructional stages; its rating is authored, not observed.

Inventory excludes canonical examples, any historically shown/reserved source, the incomplete unrated source, and both quadrant/key conflicts. Native inventory alone would count the two invalid easy sources; the saved validated count is stricter. Task deduplication uses canonical exact boundary loci across all existing practice and canonical questions; aliases, banks, seeds, option order, equation scaling and coordinate-map scaling cannot inflate distinctness. The validated finite sampling domains exceed five per supported level; no per-level capacity exception is needed for this job.
