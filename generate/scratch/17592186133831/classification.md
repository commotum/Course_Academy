# Classification at math basis 1356

Frozen database `math`, basis `1356`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the unchanged capture wrapper. All five practice questions are observed easy; all have one `selection` radio field with five math-valued choices and one designated correct lookup. No question is unrated or fieldless. No assessed prompt, answer or solution contains a plot: rating **none** for every family. Tutorial illustrations are contextual and are not copied into assessment.

| Family | Source | Observed layout | Bank |
|---|---|---|---|
| polynomial | q-124638 | quadratic field, t/t² curve; three field rows, three derivative rows, two dot rows, two final setup rows | five polynomial integrals |
| rotation | q-124687 | rotational linear field, unit semicircle; two field rows, three derivatives, three dot rows, two setup rows | four integral choices plus scalar zero |
| shifted_circle | q-124679 | linear diagonal field with translated second component; two field rows, three derivatives, three dot rows, two setup rows | five trigonometric integrals; four equal zero |
| exponential_root | q-124680 | xy²/2y field, eᵗ/√t curve; three field rows, three derivatives, three dot rows, two setup rows | five exponential/root integrals |
| spiral | q-124685 | identity field, t cos t/t sin t; two field rows, three derivatives, five dot rows, two setup rows | five polynomial/trig integrals |

Every original bank has its own public observed profile and all 25 values are mapped in `bank-map.json`. The original recipe intentions cannot be uniquely inferred. Observed profiles parameterize an actual common field scaling and stated upper endpoint; they preserve expression patterns, not a claim to have recovered source-author distractor code. They remain evidence-only. Authored defaults use all five observed families with separately labeled complete banks derived from real dot-product omissions/sign errors.

No moderate or hard practice examples exist in this capture. The missing levels are authored and labeled as such. Moderate uses the polynomial/canonical family with two unequal nonunit coordinate powers; hard uses the observed spiral family with two mixed linear field components. Both assess construction alone, have one radio field and require no new plot.

## Scope and ordered context

The route was traversed from `activity/first-step` using `step/next`, not collection order:
Introduction → The Work Done by a Variable Force → A Concrete Example → **Constructing (this KP)** → Evaluating Plane Curves → Evaluating Space Curves → Derivation of the Main Result.

The variable-force tutorial gives the formula ∫ F(r(t))·r′(t) dt. The canonical example substitutes x=t³,y=t² into (xy,−x²), differentiates both coordinates and forms t⁷, stopping at the definite integral. Prerequisites are component dot products, differentiating vector-valued functions and scalar line integrals. The neighboring evaluation KPs explicitly go beyond this endpoint. None of our learners is asked to evaluate, find a potential, use arc length or apply Stokes.

## Public anomalies

* q-124679: correct ∫₀^π cos t dt and three other displayed choices all equal zero. It has only one structurally correct dot-product integrand, but the original wording asks for an equivalent integral without a response-form restriction. Raw replay stays exact and ineligible.
* q-124680: first dot-product vector omits its second `j` marker. Also r′ is singular at t=0; the source integral can be understood by the limiting product for t>0. Normal authored variants restore `j` and use a regular interval [1,2] or [1,3].
* q-124685: its distributed row ends in a malformed `sin cos t)` expression missing the sine argument and with an unmatched closing parenthesis. Normal output contains the complete product with balanced notation. The raw original remains public evidence, not a normal formatted question.
