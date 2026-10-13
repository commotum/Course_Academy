# Four-stage extraction

## 1. Specific source descriptions

Every prompt supplies a two-component vector field, a complete oriented parameterization and increasing closed interval, asking “Evaluate”. Exact expressions and full original sentences are retained in source.json and review.md. Fields are delimiter-free scalar math options, not integral setup or equation fragments. The eight rows in classification.md describe all source structures. The arcsine source omits the initial unspecialized F-vector row; log has no separate component-product/distribution row; rotation contains both unsimplified trig and identity rows; spiral has product, distribution, collection and identity rows; polynomial has extra substituted-square/distribution rows; rational has an extra canceled-product row. These omissions and distinctions remain in observed masks.

## 2. Shared pattern

Substitute both coordinates in both field components, differentiate the curve, multiply corresponding components and add, then integrate and evaluate endpoints. This is the direct plane vector-field line-integral method. The common prose is “We will use the formula”, “Along the curve C, we have”, “Therefore”, “Computing r′(t), we get”, and the source family’s fixed “Finally” sentence. Each instance has one worked solution independent of choices.

## 3. Complete component and bank mapping

The script's QUESTIONS maps each frozen record to its family, ORIGINAL_PARAMETERS supplies the original interval and amplitude, and OPAQUE/CORRECT_INDEX map all five original scalar values and designation in captured order. `source-cases.json` is executable API replay evidence. At amplitude c every whole field/substitution vector, dot product, reduced sum, definite integral, primitive and endpoint arithmetic is multiplied by c. Coordinates, derivative stages and symbolic named-field formula remain unchanged. Component masks operate on whole mathematical expressions, never short text replacement in labels. At c=1 all complete prompt/solution strings and answer spellings reproduce source text byte-for-byte; c≠1 explicitly displays a homogeneous field factor and wraps each affected whole stage. This is a defined parameterized evidence extension, not a literal-return source branch.

The scalar historical banks underdetermine wrong operations. Their complete value catalogs are preserved publicly by `observed_<family>` API profiles, all marked `evidence_only: true`, `eligible_for_learning: false`, with unresolved intended-error interpretations. Homogeneous replay does not pretend to recover distractor intent. No source bank is silently discarded, and no numerical interpolation is promoted to learner practice. There are no mathematical or presentation source replay repairs. Several originals use lowercase f in the formal final integral row although the prompt defines F; faithful evidence retains that spelling, while authored method solutions consistently use F. This notation standardization does not alter the source fidelity counts.

Normal complete method banks (correct plus the following four operations) are authored, selected before parameters, and reject the whole instance on equality, invalidity, unique correct sign or unique correct integer/noninteger form:

| Family | Four wrong operations |
|---|---|
| affine, mixed_power | omit dx; omit dy; omit x product; subtract y product |
| log | omit log derivative; omit exponential product; reverse log derivative; omit factor 2 in y component |
| polynomial | omit dx; omit y product; omit x product; subtract y product |
| offset_circle | omit x product; omit field constant; reverse dy; omit both coordinate derivatives |
| rotation | omit y product; subtract y product; double x product; double both derivatives |
| spiral | omit both radial product-rule terms; double radial terms; omit radial t in field; omit x radial derivative term |
| parabola | swap derivatives; omit t in dy; omit x product; omit y product |
| rational | omit dx; omit y product; omit x product; subtract y product |
| arcsine | omit inverse derivative; replace derivative sqrt by radicand; reverse primitive sign; replace inverse derivative by sqrt |

These are actual integrals of erroneous displayed-method expressions, not random scalar offsets. The arcsine bank can contain a logarithmic wrong answer from replacing the radical; this is only a distractor operation, not a required learner technique. No learner-facing distractor diagnoses are added.

## 4. Reusable slots, domains and difficulty bounds

Moderate source families vary nonzero integer field amplitude |c|≤6 and familiar interval endpoints, retaining their substitution/derivative workload. Polynomial endpoints are integer 0..2 and parabola endpoints 0..4, log endpoints 1..4, rational endpoints 2..5 (t=0 and t=1 singularities excluded), trig/spiral endpoints are quarter-turn indices 0..4, and arcsine uses 0,1/4,1/2,3/4 with |t|<1. Observed profiles retain their source intervals to preserve historical banks and sequence; normal method profiles vary intervals. Explicit parameters receive the same bounds as sampling. Sampling chooses all eight eligible moderate families before sampling parameters.

**Authored easy:** canonical-example-grounded linear components A y and B x+D y on an affine line (h+ut,k+vt), [0,1]. Both derivative coefficients are nonunit, all field coefficients nonzero; products reduce to a linear polynomial. Each signed coefficient/offset is an integer of magnitude at most 4. The default sampler uses ±2,±3,±4 for substantive variation. This removes nonlinear composition from observed moderate workloads, while retaining complete direct evaluation.

**Authored hard:** field components Axy+B y and D x²+E y, curve (u t²,v t³+k), [0,1]. All seven coefficients/offsets are nonzero integers of magnitude at most 4; sampler uses ±2,±3,±4. Both coordinates require power differentiation and every one of the four nonzero field terms contributes before collection. This adds nonlinear polynomial substitutions/products without a new integration method. Polynomial degree is bounded by 6; no integration by parts or conservative shortcuts are used. These workload boundaries prevent identical easy/moderate/hard prompts.

Normal authored solution masks explicitly show formal derivatives, substituted components, both derivative operators (including zero contributions), both component products, distributed component sums, reduced integrand, primitive, individually evaluated signed primitive terms at both endpoints, endpoint collection and final scalar. Parent QA reads those actual displays independently. Task fingerprints include difficulty and canonical component/curve/interval data; complete banks/profile aliases/seed/order are excluded. Content identity includes actual difficulty, version, displayed prompt, fixed solution and full sorted displayed bank; owned field/answer UUIDs follow that content identity. All results are JSON review data, never EDB transactions.

Variation is a bounded finite catalog for the eight observed families (before whole-bank rejection: log/rational 72, polynomial 36, parabola 120, each trig/spiral 120, arcsine 60, with twelve amplitudes). Easy/hard coefficient families have 6^7 default parameter combinations before bank rejection. Variable-letter and profile aliases do not inflate counts. Tests report actual distinct sampled task fingerprints separately from these domain ceilings.
