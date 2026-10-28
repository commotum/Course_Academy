# Template extraction

Specific original prompts, solutions, parameters and every original option's exact
value/recipe are retained in template-components.json. Raw database records remain
in source.edn and source.json. source-replay.json separates mathematical bank
fidelity from notation and source defects.

Shared backbone: given a positive axis-aligned ellipse in two coordinates and a
three-component cylinder parametrization with one trigonometric component absent,
select that component. The remaining coordinate is free. No translations, rotations,
phase shifts, additional operations, bounds, or extra fields are introduced.

Easy keeps a normalized ellipse and requests the sine component. Moderate includes
normalizing positive integer coefficients before selecting a sine or cosine
component. The solution retains the source sequence: recall/normalize ellipse;
state planar parametrization and t interval; verify substitution and the Pythagorean
identity; lift to three dimensions with free coordinate; name the missing component.

Slots a,b are positive integer semiaxes in 1..12. Source values 1,2,3,4,5,6 are
retained in replay. Normal generation samples 2..12 (a conservative subset); the
validator also exercises 1 and 12. Plane xy or xz is observed, and both are sampled
for each profile as a conservative same-method generalization. The first planar
coordinate has a cos(t), the second b sin(t). The free coordinate and vector position,
requested ordinal, equations, solution and distractors all follow that plane.
Signs remain positive, as in every source. Ordinary full-circle t in [0,2pi), free
coordinate real. The target sine/cosine role is fixed by profile; changing it needs
another observed profile. Arbitrarily swapping sin/cos or signs would change the
contract. The displayed integer equation is the primitive integer multiple of the
normalized equation: b²v²+a²w²=a²b², divided by the coefficients' gcd.

Full banks are selected before construction, never pooled. Recipes use a,b and free
coordinate u; exact per-option mapping is in template-components.json. The q-164522
3 cos(t) option is modeled as (b/2) cos(t), an observed algebraic pattern with unknown
misconception; no stronger interpretation is claimed. q-164530's unscaled sin/cos
and q-164534's unscaled sin/cosh stay fixed as observed. Legacy q-103980/q-103981
profiles are replay-only because source keys/solutions and difficulty are absent.
All banks retain 5 choices and reject equivalent/colliding choices.

A task fingerprint is (a,b,plane,target-role), ignoring equation scale, seed, profile,
UUID and order. Source/canonical tasks are excluded before selection. Different
banks can have different stable authored UUIDs but cannot count as different tasks.

q-164524's first substituted denominator is corrected from 5 to a²=25 at original
parameters; the remaining steps already use 25. The generator consistently derives
all denominators from a²,b². Originals are preserved. q-167887 is an excluded
contextual blank, not a supported generator field combination. Hard is not produced.
