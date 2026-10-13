# Classification: Computing a Reciprocal Ratio Using the Pythagorean Identity

EDB `math`, basis **1522**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. KP `17592186110756`, canonical example `e-3484`. Protocol: [3-classify](../../../docs/3-classify.md).

The selected missing **easy** score is **94.7935**, based on five distinct rated questions. The inventory is five moderate plus one unrated question. No generator is associated. Owning topic: **Using the Pythagorean Identity in the First Quadrant**.

All six original prompts, 30 answer values, and five stored worked solutions were read. All use one five-choice math-radio field, `selection`. [Originals](source-questions.md) and [component/bank mapping](source-cases.json) retain every value; each complete bank is its own profile.

| Difficulty | Field type | Template | Sources | Plot rating |
|---|---|---|---|---|
| Moderate | Radio | Rational y-coordinate → secant | q-124750 | Moderate |
| Moderate | Radio | Rational x-coordinate → cosecant | q-124743 | Moderate |
| Moderate | Radio | Radical y-coordinate → secant | q-65062, q-85234 | Moderate |
| Moderate | Radio | Radical x-coordinate → cosecant | q-65064 | Moderate |
| Easy / hard | No rated sources | None observed | — | — |
| Unrated | Radio | Rational y with perfect-square complement | q-65066 | Moderate for new plotted parameters |

All five rated sources recover an irrational complementary coordinate, take its reciprocal, and rationalize the denominator. Coordinate choice and target function change the prompt and solution roles; rational versus radical input changes the substitution structure. Simplification coefficients within those families are variants, not extra templates.

The diagrams were visually inspected. Every practice prompt has a first-quadrant point P on the unit circle, a radius, and a marked angle θ. Complete solutions use an annotated counterpart labelled P(cos θ, sin θ). The quadrant selects the positive root; the angle and point move with the coordinate. New parameters therefore require recurring paired figures, not just reuse of an unchanged image. [Plot extraction](plot-extraction.md) records that dependency. LaTeX itself is not counted as a plot.

`q-65066` supplies y=3/5. Its mathematically correct answer is sec θ=5/4, present in its bank; its difficulty, canonical correct reference, and worked solution are absent. It must not be relabelled as a source-observed easy question. Nevertheless, its content demonstrates a same-KP case with no irrational-denominator rationalization. The complete canonical example also reaches csc θ=7/5 from x=2√6/7 without rationalizing.

The actual neighboring KPs separately ask for a coordinate, an ordinary sine/cosine ratio, and a tangent/cotangent ratio. An easier variant must keep reciprocal recovery, rather than remove that step or substitute one of those sibling tasks.

**Classification result:** a natural lower-workload family exists inside the KP: choose a complementary coordinate with an exact rational square root. Inventing this family is straightforward; matching the original five-choice distractor banks is a separate extraction problem.
