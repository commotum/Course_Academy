The hard family uses the following complete bank, where `m` is the correct nonzero slope, `q` is the positive ordinate and `t` is the supplied point:

1. `m*x - m*t + q` (key)
2. `2*m*x + 2*m*t + q`
3. `-m*x + m*t`
4. `-m*x + 2*m*t + q`
5. `m*x - q`

The bank-only probe never receives the curve, point, target, answer key, generator metadata or a catalog of outputs. It groups the displayed x coefficients and their signs, then reads each constant's standalone rational term. Signs are visible signs of numeric coefficients of the common logarithm, not inferred by differentiating a target or evaluating a bound.

Three slopes have sign(m), two have the opposite sign. In the majority-sign group, coefficient m occurs twice and 2m once. Of the two m candidates, the correct one has positive rational term q and the other has negative rational term -q. The logarithmic intercept contributions do not alter this standalone rational term. Thus the bank construction encodes the key regardless of the sampled base, coefficient, exponent translation, point or radio order. This rule succeeds on 24/24 fresh records, all six controlled records, all four runner batch records before and after actual delivery filtering, and each displayed-point subgroup.

This also succeeds on the complete original q-107463 bank. That observation prevents claiming this as a newly introduced cue, but does not establish instructional necessity: the target answer domain is varying tangent equations, not a finite list learners are intended to recognize. The source itself includes wrong-ordinate alternatives at the correct slope. The evidence-only same-method-bank-witness.json changes one wrong-ordinate alternative to `m*x - m*t + 2*q`. It remains a distinct wrong equation with exactly the same response form and prerequisite workload. The probe then finds two positive-rational-term candidates and cannot uniquely identify the key. Native grading accepts the unchanged true tangent and rejects that wrong ordinate. No duplicate correct choices, new answer form or unrelated skill is needed to remove the reported cue. This fixture is a feasibility test, not an edit to the generator or approval of a proposed correction.

The regression exits 1 when this bank-only rule solves the whole provided candidate file. That is a deliberate failing regression, not a tooling failure. A future passing regression alone would not establish acceptance; the changed construction and its conditional subgroups still need independent review.

The stored original question is independently retained as inventory-hard.json with UUID 77c551c0-c155-56eb-9f11-d8d660941796 and entity 17592186524997. The captured hard pool has no other entries. This stored-pool repair belongs to the runner, separately from package repair.
