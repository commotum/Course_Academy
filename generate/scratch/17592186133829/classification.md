# Classification — basis 1356

Source wrapper: database `math`, basis `1356`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. All six practice records are preserved in source.json; canonical e-6307 is contextual, not counted as a practice.

| Captured difficulty | Practices | Field shape | Separate prompt/solution templates | Plots |
|---|---:|---|---:|---|
| easy | 1 | selection radio; five math choices | 1 | none |
| moderate | 4 | selection radio; five math choices | 4 | none |
| absent | 1 | selection radio; one text and four math choices; missing key | 1 | none |
| hard | 0 | authored selection radio, five math choices | 1 authored | none |

The unrated source q-76368 retains difficulty, worked-solution and correct-ref omissions in public `observed:q-76368` replay. Its scalar substitution is independently completed in a separate `completed-source` profile, with an explicitly authored moderate assignment. Its captured owning lesson JSON confirms a five-option multiple-choice widget; no legacy field was dropped.

Lesson activity `17592186133993` is traversed from first-step, using each step/next: Introduction -> General Formula -> this setup KP -> Evaluating the Scalar Line Integral (133830) -> Evaluating Using Substitution (133827) -> Derivation. The collection order is not the lesson route. The key prerequisite is Arc Length of a Vector-Valued Function (topic1837). The canonical quarter-circle example teaches substitution, component derivatives, magnitude, metric factor and definite-integral bounds. Evaluating a primitive belongs to the later sibling KPs and is excluded here.

Authored hard demand: substitute three nonzero coordinate expressions into x*y-z^2, retain a product and a squared binomial, expand their separate components and collect a noncancelling cubic; derive the three-component speed and set up the definite integral. All hard instances have the same operations; coefficient/offset choices are unordered. Coefficients a,b,d in1..3, signed nonzero offsets c,e in ±1..3, amplitude in±1..3 and half-integer bounds in0..3 keep elementary polynomial differentiation/algebra within the arc-length prerequisite. No learner integration or new curve-parameterization task is added. This is a design claim, not an observed hard label.

Observed/default families are unordered, chosen before parameters. Easy retains one rational substitution and speed cancellation; moderate retains each observed family's cancellation or trigonometric identity stage sequence. Cubic completion is moderate because a linear curve has constant speed but cubic scalar substitution; this level was not present in the capture. The amplitude slot is an outer numerical coefficient; it does not claim a new skill/template. Bounds meaningfully change the path segment and required definite integral, and are included in task identity.

Every historical bank is evidence-only because its authoring intention is opaque; q-40253 and q-76356 additionally contain non-real wrong-option radicals on parts of their original intervals. Their correct setups and available keys are mathematically sound. Normal defaults use complete method-derived banks, never pools of first-valid errors.
