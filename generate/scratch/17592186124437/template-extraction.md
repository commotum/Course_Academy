# Four-stage extraction

## 1. Specific source descriptions

The raw source is retained in source.json, including every key and absence. extraction.json maps every individual source answer UUID, exact value, correct designation presence, complete bank, row count, derivative, parameters and point layout. All 55 observed options are accounted for before authored banks.

Sources have linear, trig+coordinate product, rational+perfect-square radical, shifted-cosine product, two-monomial difference, single monomial, log−exponential quotient, sum times cosine exponential, radical quotient and fixed-base exponential structures. Coordinates use small integers, e, pi or quarter turns; denominators remain nonzero and radical evaluations exact. f_x is supplied when y is held, f_y when x is held. Full 3D points and coordinate-only points remain distinct.

## 2. Shared purpose

Choose the partial derivative for the free coordinate of the fixed-coordinate surface section, substitute both point coordinates into the supplied derivative, and return its scalar value. The unknown surface can always have a constant adjusted to the stated z coordinate. No need to reconstruct the surface.

## 3. Component and bank mapping

The following bank continuations are public evidence profiles, not recovered learner misconceptions. Each expression uses actual point/coefficient slots X,Y,A,B. Scalar evidence underdetermines intent: these algebraic pattern continuations reproduce all values but are never eligible for normal learning. observed_raw and observed_supported are both marked evidence_only=true and eligible_for_learning=false. The supported profile only authors omitted fields for q-36463; it does not make opaque distractors valid inferred pedagogy. All complete banks reject collisions as a whole.

| Source/family | Parameter slots | Source value → continuation |
|---|---|---|
| q-36216/linear | {'x': 2, 'y': 3, 'z': 9, 'a': 6} | -3 → -Y; 12 → A*X; 9 → A*X - Y; 1 → X - 1; -1 → 1 - X |
| q-36463/cos_sum | {'x': 'pi/2', 'y': 0} | 1 → Y*cos(X) + cos(Y); π → 2*X; 2 → 2; \frac{π}{2} → X; 0 → 0 |
| q-132579/sin_product | {'x': '-pi/2', 'y': 2} | -1-\pi  → X*Y + sin(X); 1+2\pi  → -2*X*Y - sin(X); -\pi  → X*Y; 2-\pi  → Y*(X + 1); \pi -1 → -X*Y + sin(X) |
| q-132584/rational_radical | {'x': 1, 'y': -3, 'z': 8} | -\frac{25}{9} → (X**(5/2)*Y**3 + X**2 + 1)/(X**2*Y**2); \frac{15}{6} → -5*Y/6; \frac{2}{3} → -2/Y; -\frac{7}{3} → (sqrt(X)*Y**2 - X**2 - 1)/Y; -\frac{16}{9} → (X**2 + 2*Y**3/3 + 1)/Y**2 |
| q-64968/cos_shift | {'x': 1, 'y': 0} | 0 → Y; 1 → sqrt(2)*X*cos(X*Y + pi/4); 2 → 2*X; -2 → -2*X; -1 → -X |
| q-71198/polynomial | {'x': 2, 'y': 1, 'a': 3, 'b': 6} | 1 → Y; -1 → -Y; 2 → X; 0 → X*Y*(A*X - B*Y); -3 → -A*Y |
| q-132578/monomial | {'x': 1, 'y': 2, 'z': 5, 'a': 4} | 12 → A*(X + Y); 20 → A*(X + Y**2); 8 → A*X**2*Y; 6 → A + Y; 4 → A |
| q-132580/log_exp | {'x': 'E', 'y': 2, 'z': 3} | 2-{e}^{2} → Y - exp(Y); 3 → Y + 1; 4-e → 2*Y*log(X) - exp(Y)/X; 4{e}^{2} → 2*Y*exp(Y); 3e → X*(Y + 1) |
| q-132582/exp_cos | {'x': 1, 'y': 'pi'} | \pi  → Y; \frac{1+\pi }{e} → (X + Y)*exp(cos(X*Y)); 2\pi e → 2*E*Y; e+\pi  → Y + E; \frac{\pi }{{e}^{2}} → Y*exp(-2) |
| q-71199/radical_ratio | {'x': 3, 'y': 2} | -\frac{1}{2} → -1/Y; \frac{1}{2} → 1/Y; 1 → 1; 0 → 0; -1 → -sqrt(X**2 - 2*Y**2)/(X - Y) |
| q-64966/base_exp | {'x': 0, 'y': 1, 'z': 0, 'a': 2} | 2 → A**(X + Y)*X*Y*log(A) + A**(X + Y)*Y; 1 → Y; -1 → -Y; -2 → -A**(X + Y); 0 → X |

Authored default banks follow the displayed substitution operations and use the complete five-member bank for the chosen family. The independent validator parses every displayed member and rejects equal values. Family-specific wrong operations:

- linear: reverse subtraction; omit fixed-coordinate term; omit varying-coordinate term; exchange coordinate substitutions.
- cos_sum: evaluate first cosine as sine; reverse cosine sign and omit first term; use fixed coordinate as slope; first cosine as sine and subtract second term.
- sin_product: reverse sine sign; omit coordinate product; omit sine; omit fixed-coordinate factor.
- rational_radical: use first power of fixed coordinate in denominator; omit radical term; omit rational term; reverse sign of radical term.
- cos_shift: omit angular shift; omit square-root coefficient; omit cosine evaluation; reverse cosine sign.
- polynomial: reverse subtraction; omit second monomial; omit first monomial; exchange coordinate substitutions.
- monomial: omit square on varying coordinate; exchange coordinate roles; omit fixed-coordinate factor; replace final product by sum.
- log_exp: omit factor two and exponential denominator; omit exponential term; omit log term; reverse subtraction.
- exp_cos: omit varying-coordinate addend and exponential; reverse exponent cosine sign; distribute exponential only to fixed-coordinate addend; use exponent cosine as multiplicative factor.
- radical_ratio: reverse denominator subtraction; omit varying-coordinate denominator term; negate omitted-denominator result; omit coefficient two in radicand.
- base_exp: omit fixed coordinate in exponent; reverse total sign; omit constant one in final factor; replace multiplication by fixed coordinate with addition.
- canonical_rational: reverse subtraction; omit rational term; omit polynomial term; omit rational denominator.
- canonical_trig: reverse polynomial subtraction; omit rational term; omit polynomial term; omit rational denominator.

## 4. Reusable masks, stages and bounds

Complete slots include the plane equation, full point, coordinate-only value, evaluation pair, entire supplied derivative and each operative aligned row. No short global x/y/numeric replacement occurs. Prose is masked before math slots are inserted. The normal generator uses the original shared prose and family chain at changed parameters, including the original omissions of redundant substitution rows. Exact anchor replay passes through the same recipe functions; no source payload return or numeric answer lookup exists.

The aligned recipes retain: one substitution/equality row for linear and monomial; one substitution plus final row for sin+product; substitution, separately evaluated fraction/radical, final row for rational+radical; shifted input, angle evaluation, cosine value, product for shifted cosine; substituted two monomials, evaluated difference, collected result for polynomial; one substitution/equality row for log-exp and base-exp; substituted cosine argument, evaluated exponent, quotient result for exp-cos; substituted radicand/denominator, separately squared values, final result for radical quotient. q-36463 authors substitution plus final slope because no source chain exists. Missing levels use canonical substituted rational/polynomial components, individually evaluated component sum, final result; hard retains the extra cosine evaluation.

Bounds are enforced on explicit parameters as well as samplers. See guards and sample in the generator. Perfect-square radicands, familiar trig angles and small exponential bases keep the observed arithmetic workload. The strict noninteger rational component avoids moderate/hard reduction to a single easy integer arithmetic instance. The hard cosine component cannot vanish. Blank is a clearly authored optional field-layout extension with matching {{slope}} placeholder and only one scalar answer; default and original replay remain radio.

Formatting is verified on decoded strings. No doubled adjacent source slash was found; serialization was not treated as a TeX error. Source notation is retained exactly at anchors. Raw difficulty, solution and correct-ref absences are preserved individually. Identities include actual prompt, solution, bank, field shape, difficulty and correct presence; changing option order leaves identity unchanged. Mathematical fingerprints exclude banks/profiles/ancillary z.
