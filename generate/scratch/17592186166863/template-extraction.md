# Extraction and bounded generalization

Exact per-question component descriptions, expressions, source IDs, and first
partial derivatives are in source-components.json. The retained source.json
contains full original wording and the complete choice records. The complete
source-field/choice-to-recipe mapping is in source-bank-replay.json after validation.
Each field's bank profile is Boolean false / Boolean true. These are independent
checkbox banks, not a pooled distractor list; all 66 choices and all 33 keys must
replay. No inferred error explanations appear in the learner presentation.

At original parameters u=v=1, each pair is exactly its captured mathematical
expression. Compare complete expressions, derivatives, three banks and keys.
Normalize LaTeX whitespace, R to mathbb R, trig notation and parentheses around
components; preserve ordered solution stages and instructional sentences. The
old radio conclusion wording in source solutions remains a subset conclusion.

For each of the three independent supplied vector fields, allow two bounded
coordinate slots u,v in {-2,-1,1,2}. If source components are P(X,Y),Q(X,Y), use
u P(ux,vy), v Q(ux,vy). This is a conservative same-method generalization,
not an observed original parameter range. It preserves smoothness on R²,
function nesting, the roles of x/y and F/G/H, all three tested objects, and the
partial-derivative comparison workload. Both comparison derivatives are uv
times their original derivative evaluated at (ux,vy). Since the coordinate map
is onto R² and uv is nonzero, equality everywhere and the correct subset are
preserved. Each coordinate slot changes all dependent components and derivatives
together. Do not vary domain topology, introduce singularities, add requested
potentials, change field types, or introduce new operations or reasoning stages.
All original functions are globally C1: positive quadratic denominators and log
arguments, entire exponentials/trig/polynomials, and arctan on R.

The fixed three-field workload and finite function families anchor moderate
difficulty; signed scale bounds keep coefficient arithmetic bounded. Fixed
source exponents preserve differentiation order and function nesting. The source
components and derivative expressions, not incidental positions, determine this
structure. The generator does not create easy/hard variants.

Compute exact components and derivatives with SymPy; render the source theorem,
domain statement, P/Q identification, displayed derivatives and per-field
conclusion for each instance. One concrete solution serves every learner choice.
Test displayed math by parsing it independently, not merely reading metadata.
Include changed-scale cases with all other fields held constant and negative
controls that deliberately retain an old solution.

Novelty: normalize rational common scalar multiples of each complete vector
field, including global sign, and sort the three normalized fields before hashing.
This ignores seed, identities, choice order, field permutation, profile labels
and uniform field multiples. Different full prompts must still be rejected if
this mathematical fingerprint matches any source, canonical or pool question.
The bounded sampler has at most 4^6 coordinate combinations per source triple;
this is an upper bound, not a promise of that many distinct tasks. Sampling
exhaustion leaves a shortage explicit; no fabricated alternatives are added.

Plots: none in prompts, answers or worked solutions; stages 5 and 7 require no
assets. Stage 8 therefore has an empty asset-hash list and no publication step.
