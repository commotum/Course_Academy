# Classification

Snapshot: math, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; original wrapper preserved as source.json. Owning topic 17592186050555 (MA1938), Directional Derivatives. Sources are practice records, canonical example excluded from practice counts.

| Template | Source | Observed difficulty | Field | Bank | Plot |
|---|---|---|---|---|---|
| cosxy |17592186124963 / q-36293|unrated|radio, selection, five mathematical vectors|source|none|
| quadratic |17592186265872|easy|same|source|none|
| exp |17592186351517|easy|same|source|none|
| trig_product |17592186354478|easy|same|source|none|
| linear_sin |17592186124965|moderate|same, 3-component vectors|source|none|
| mixed_sin |17592186323874|moderate|same, 3-component vectors|source|none|

Six distinct function/solution families and six original bank profiles. The unrated cosine-plus-product receives an authored easy assignment based on two held partials and small coordinates, comparable to the observed trigonometric/product easy question. Its raw replay omits difficulty, solution and correct ref, as captured. Its original five-choice widget was also found in `/home/jake/Developer/MA/DATA/Lessons/1938/Source/1938.json`, question_id 36293, confirming layout but no authoritative key or solution. The normal key `(2-sin(1),1)` is independently derived.

No hard source. Authored hard computes three logarithmic chain-rule partials and requests the **unit** direction of maximum increase/decrease, then normalizes the gradient. This is supported by the canonical log-product example and the lesson's unit-gradient formula, not a maximum-rate or directional-derivative evaluation. All hard items have these same stages. Positive log-domain coordinates <=3, powers <=6; reduced gradient components <=4, denominator <=3, squared norm <=36 with reduced numerator <=50 and denominator <=9, nonuniform components. The reduced bounds apply to explicit inputs too.

Easy defaults serve every source-shaped two-variable family. Coefficients 1–4; polynomial coordinates nonzero signed integers <=3; exp point x in +/-1,+/-2, y=1 so ln evaluation remains familiar and exact; trig-product x in -1,0,1, y=+/-1. Moderate defaults serve both three-variable families. Linear-inner trig phases are integer multiples of pi bounded by 12pi (mixed <=6pi), all chain coefficients remain nonzero, linear_sin's two chain coefficients must differ, coordinates <=3 (mixed z <=2). These are variation bounds, not claimed recovered source generation rules. Observed easy source arithmetic varies in term count and cancellation, so comparability is the same held-partial/evaluation/orientation demand, not an invented ordering within a level.

The actual lesson route was reconstructed by first-step/next: Introduction -> Calculating a Directional Derivative -> Gradient as Direction of Maximum Increase -> this KP -> Generalization of Partial Derivative -> Rate in Direction of Gradient -> sibling maximum-rate KP -> Derivation. Prerequisite topic The Gradient Vector (17592186050143) supports calculating partials; the introduction establishes vector normalization. The neighboring rate KP is outside this generator's assessed demand.

Source anomaly: exp solution's evaluation label is `∇f(1,1)` although prompt, substitution and final answer use (-1,1). Raw replay is evidence-only; normal solution repairs only that label. Actual decoded answer commands have one backslash, not two: `decoded-source-bytes.json` stores ord arrays and adjacent-backslash counts. No unsupported escape repair was performed.

`variety.json` independently enumerates 1,369 eligible hard coefficient/point tuples and 296 distinct oriented unit directions (excluding all positive common gradient magnitude). Parameter-context counts are reported separately and are not used as canonical direction counts. The x=0 easy trig-product subfamily has exactly two oriented axis directions.

Pairwise equivalence uses the actual response criterion for the entire bank. Normal trig has preselected axis_method (x=0) and nonaxis_method (x=+/-1, unequal coefficients for bank eligibility). Its finite coefficient/point domain supports 42 canonical oriented directions total, of which two are axis orientations; positive common gradient magnitude and bank aliases are not counted. The nonaxis bank uses omitted x-partial contribution, reversed y cosine sign and component swap; the axis bank uses omitted x factor, swap and wrongly retained cosine in the x derivative. Source bank profiles remain separate evidence. Counts are reproducible with `.venv/bin/python generate/scratch/17592186124459/enumerate-variety.py`.
