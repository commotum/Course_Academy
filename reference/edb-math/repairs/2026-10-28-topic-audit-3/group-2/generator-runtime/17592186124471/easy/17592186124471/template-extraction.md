# Four-stage template extraction

## 1. Specific observations

The eight original prompts are imperative “Compute the rate of change…” sentences specifying f, r(t), and a scalar time. They use angle-bracket vectors and ask for one scalar, rather than a function of t. All banks contain five delimiter-free scalar math values. Exact original strings and fields are retained in source.json and source-cases.json.

q-167499 has f=x/y, r=⟨2t,√t⟩, t=9: quotient gradient, one composed-gradient row, square-root velocity, five chain rows, two evaluation rows. q-36227 has f=x³+y², r=⟨sin t,cos t⟩, t=π/4: power gradient, one composed-gradient row, trigonometric velocity, four chain rows, four evaluation rows including individual familiar-angle values and radical collection. q-94884 has f=x²−y², r=⟨t²,2t−1⟩, t=0: two composed-gradient rows, four chain rows, two evaluation rows.

q-94887 has f=xyz, r=⟨2t,√t,3t−1⟩, t=1: three product partials, two composed-gradient rows, five chain rows and two evaluation rows. q-94888 has f=xz²+y³, r=⟨t,4,√(t²−3)⟩, t=2: cross-power partials, two composition rows, constant-coordinate zero derivative, five chain rows and three evaluation rows. q-94891 has f=ln(x²+y²+z²), r=⟨t−1,3,2t⟩, t=0: three quotient partials, two composition rows with expanded common denominator, constant-coordinate zero derivative, five chain rows and three evaluation rows.

q-36247 and q-36253 contain the functions/curves listed in classification.md and five math choices; there is no captured worked solution. The authored solutions supply the same complete formal-operator, substituted-component, velocity-operator, dot-product and final-evaluation sequence.

## 2. Generalized instructional pattern

Compute ∇f with the other coordinates held fixed; substitute the complete curve into every coordinate; differentiate every curve component; take the dot product with all contributions present (including zero contributions); then evaluate at the requested time. No arclength normalization is performed. The source prose sequence is shared. Source masks reproduce its exact sentences and rows; normal method variants retain the sequence while inserting actual changed coordinates/time in both prose and math.

## 3. Component and bank mapping

Each source's original function/curve/time is explicitly encoded in SOURCE_SPECS. Each `_raw` profile is an entire observed bank. Its sole variable is a whole-function scale s∈{1,2,3,4}, with the original f, r, and time held fixed. Every gradient/composition/explicit scalar dot/evaluation RHS and every bank value is multiplied by s exactly once; the formal chain expression already refers to scaled f and is not scaled twice. Curve velocities stay fixed. Neutral s=1 elides multiplication and reproduces the original spelling. This is a parameterized equivariant mathematical replay operation. It is not an inferred distractor error algorithm.

| Public profile | Complete source bank in captured order | Independently correct scalar |
|---|---|---|
| q-36247_raw | −17, 1, −15, 9, 3 | −17 |
| q-36253_raw | 5 cos 2, −3 cos 8, 0, −3 cos 2, cos 2 | −3 cos 2 |
| q-167499_raw | −√3, −1/9, 1/√3, 1/3, 1 | 1/3 |
| q-36227_raw | (√3−2)/2, 2√3−1, 3/8, (3√2−4)/4, 0 | (3√2−4)/4 |
| q-94884_raw | −1, 4, −3, 5, 2 | 4 |
| q-94887_raw | −8, 15, 6, 12, −10 | 12 |
| q-94888_raw | −12, 10, 6, 9, −7 | 9 |
| q-94891_raw | 3/10, 8/13, −12/17, −1/5, 2/3 | −1/5 |

At scale s each table entry is the operation s×entry; the correct designation is independently selected by equality with d/dt[f(r(t))], never looked up by answer index. All 40 source values are matched one-to-one, not only correct entries. Several wrong scalar values have no defensible uniquely determined error interpretation. Therefore these complete source banks are explicit evidence profiles only. No fitted polynomial or unrelated random offset becomes a default distractor.

The public `q-36247_raw_omission` / `q-36253_raw_omission` profiles preserve all three missing assessment fields; their `_raw` profiles provide separately authored full completions for validation. These omissions are included in source-cases.json and the original review. Every raw profile is marked evidence_only=true and eligible_for_learning=false.

Default banks, separately labeled `_operations`, use G_i=∂_i f(r(t)), V_i=r_i′(t), T_i=G_iV_i and evaluate the following complete operations at t0:

* Two coordinates: correct ΣT_i; T_1 (omit second); T_2 (omit first); ΣG_i (omit curve velocity); T_1−T_2 (reverse second sign).
* Three moving-coordinate families: correct ΣT_i; T_2+T_3; T_1+T_2; ΣG_i; T_1+T_2−T_3.
* Radical-square/log families with a constant middle coordinate: correct ΣT_i; T_1; T_3; ΣG_i; ΣG_iV_i². The last operation really squares each velocity component before the dot sum, including its sign and zero values.

Each bank is selected as a complete five-operation object before construction. Every value must be real/finite and pairwise mathematically unequal. A failure rejects the whole sampled instance. Explicit calls fail without silently changing parameters. No first-valid option pool or post hoc perturbation is used.

## 4. Reusable masks, constraints and calculations

Observed replay extracts six display blocks into unchanged surrounding prose and per-RHS mathematical component masks. Formal gradient/composition/explicit dot/evaluation masks scale with f; the velocity block and formal chain reference are invariant. These masks are used at scale 1 and changed scales through the same generate API. A full function-expression slot in the prompt scales f; substitutions never perform short-symbol replacement in prose. Missing-solution sources always run the normal formal mathematical builder, including when replaying a source bank.

Normal builders parameterize the same structures:

| Template | f | r(t) |
|---|---|---|
| quadratic_affine (authored easy) | ax²+by² | ⟨ct+d,et+h⟩ |
| quotient | ax/y | ⟨bt,c√t⟩ |
| trig_powers | ax³+by² | ⟨c sin t,d cos t⟩ |
| square_difference | ax²−by² | ⟨ct²,dt+e⟩ |
| triple_product | axyz | ⟨bt,c√t,dt+e⟩ |
| radical_square | axz²+by³ | ⟨ct,d,√(t²−e)⟩ |
| log_norm | a ln(x²+y²+z²) | ⟨bt+c,d,et⟩ |
| mixed_product | ax²+bxyz | ⟨ct²,dt+1,et⟩ |
| sine_difference | a sin(x−y) | ⟨b√t,ct⟩ |

Explicit authored coefficients are integers of absolute magnitude ≤4. Every defining workload coefficient is nonzero, including constant coordinates and shifts where source structures require them; easy affine offsets may be zero. Default samplers use signed magnitudes 1..3. Ordinary evaluation times are −2..2; root-coordinate families use 1,4,9; trig uses π/6,π/4,π/3,2π/3,3π/4; radical-square uses t0=2 and e=3, retaining the source’s positive radicand1. Positive-root and log domains are checked. Source replay fixes every source parameter and permits only s1..4, preserving arithmetic workload.

Formal gradient and velocity operator vectors have every component. Composition retains unevaluated substitutions before reduction where source structure does so. Dot rows retain grouped signed multiplicative factors, then individual terms before collection. The trig evaluation has substitution, separately evaluated gradient/velocity factors, an uncollected radical sum, and final collection. Constant-coordinate zero contributions remain printed. Signed factors use parentheses and visible multiplication.

Identity hashes version, actual prompt, fixed solution, complete displayed bank and correct displayed value, ignoring shuffled order and seed. A separate mathematical fingerprint uses the symbolic f, complete curve and evaluation time, excluding bank/profile. This assesses traversal with respect to t, so time parameterization is meaningful. Rejection samples produce 24 distinct mathematical tasks per template over the 24 checked seeds; this is measured variety, not a claim of recovered source template count.

# Raw source anomalies and repair accounting

q-36247/q-36253 lack labels, correct refs and solutions. Their full original fields remain evidence; assigned hard/moderate labels and missing solutions/correct refs are authored and excluded from present-ref/present-solution match counts. Independent derivative values are −17 and −3cos2.

q-94888/q-94891 omit d/dt around their third component in the initial formal r′ row. The raw equality is mathematically false before the next correct velocity row. Raw public profiles reproduce and independently flag exactly those rows; normal output prints the operator on every component. No source answer bank is wrong or ambiguous.

q-36227/q-94884 introduce a two-variable function as f(x,y,z); q-94887/q-94888/q-94891 label a three-variable gradient as ∇f(x,y). These are retained in raw evidence and corrected in normal output. They are notation defects, separate from the two formal derivative errors. Decoded source bytes were checked: command backslashes are single; doubled slashes occur only at legitimate aligned row separators. No TeX-escaping repair is claimed.

Exact reproduction: prompts 8/8; banks8/8; scalar options40/40; present correct designations6/6; present worked solutions6/6. Raw mathematically correct solutions4/6, raw formally defective solutions2/6. Missing correct refs2 and missing worked solutions2 are authored. Normal generated instances have zero mathematical source errors. Source replay profiles are knowingly raw evidence; their derivative defects are not passed as valid teaching operations.
