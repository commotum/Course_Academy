# Instructional account and targeted repair

The learner differentiates a composite radical: identify the inner polynomial,
apply the outer power rule, multiply by the inner derivative, then substitute the
stated point for a tangent slope. Tutorial 743ad997-8732-5c0f-9676-ff1d44f3b513
explicitly says to multiply the two derivatives and substitute the inner function.
Canonical e-182 (8fcdb2c8-71ca-5bfa-b7fe-49f8f2c05bbb) demonstrates these stages
with sqrt(1-x^2), including the nonconstant inner derivative.

All 17 captured questions and their complete fields, choices and solutions are in
data/source-questions.json. data/source-cases.json maps their original parameters,
profiles and missing-field repairs; data/templates.json preserves 15 layouts.
Easy covers evaluated slopes (including reciprocal quadratics and the observed
cubic sum), moderate symbolic linear radicals/reciprocals, and hard the observed
linear/quadratic blank derivatives and quadratic radio slope. All three bands are
supported; the requested band is easy. Radios select one of five exact expressions;
blanks supply the derivative RHS or numeric slope, retaining source scaffolds.
No diagrams are present. Prerequisite context is the polynomial power-rule chain
example e-181; no additional prerequisite records were supplied.

Fixed features have instructional reasons: one radical composition preserves the
chain-rule workload; positive evaluation radicands make the derivative finite and
real; square evaluation radicands retain source rational arithmetic; the cubic
term occurs only in q-20181, where a sum-rule stage is explicitly taught. Original
difficulty labels and response layouts are retained. Coefficient signs and target
points are variable. Quadratic blanks retain positive, negative and zero inner
derivatives (q-342789 is a legitimate zero slope), rather than freezing the target
at a vertex. The answer-bearing role is the derivative value, not a choice label,
sorted rank, or common spacing. Those assignments may vary independently.

The source banks have irregular scalar outcomes: q-107360
(c8b46779-d19f-5cca-987d-5f500a9de334) has -5/3, 1/3, -2/3, -3/4, 2;
q-107288 (67f07fb8-cc06-5cda-9a1f-cc029f68242d) has 1/3, 2/3, 3, 1/4, 2.
q-107291 (0ce97e32-c8a9-5155-bb70-6cb7385360f5) and q-107303
(98cde390-f268-5ffd-9f2f-31f016a0c432) share the correct radical denominator
across choices but vary the scalar, including division errors and reversed signs.
We cannot infer the cognitive intent of every empirical wrong scalar. Their exact
banks remain available through explicit source replay.

The defective production extension replaced those banks by consecutive integer
multiples of a common factor. Finding a68a8999b8ec7f376999 demonstrates that this
reveals the answer from spacing alone. The replacement is an explicitly authored
arithmetic-error profile, not a claim to recover an original bank: choose the
correct scalar's rank first, then select four irregular rational scalar outcomes
on the required sides from a bounded rational pool. Each scalar corresponds to a
possible erroneous multiplication/division result. For symbolic questions multiply
these scalars by the source radical denominator factor; for slopes they are final
rational slope outcomes. For the cubic sum add the same correctly computed cubic
contribution to all five radical outcomes, so a nearest-cubic heuristic does not
single out the key. Do not derive a common spacing from the correct coefficient.
Use independent denominators up to 24 in the pool, favoring simpler fractions;
reject an arithmetic progression of five values and banks where only the key has
a denominator as small as its own. Bound distractors within twice max(2,abs(scalar))
of the scalar to keep plausible magnitudes without selecting a fixed rank. Preserve the source's five-choice contract and shuffle choice positions.
The correct scalar and the pool use identical rational formatting. Numerical
bounds are conservative presentation limits, not additional mathematical rules.

This changes only the answer bank: the learner's function, reasoning, arithmetic,
key and solution remain derived from the same original instance. Tests must inspect
visible choices and independently differentiate visible prompts; metadata alone is
not evidence. Obligations: both coefficient signs, all scalar ranks and choice
positions per affected template; the exact reported parameters and CLI batch;
spacing and rank/sign/length/denominator cues before and after shared filtering;
changed evaluation target with function fixed; irrelevant bank changes preserving
key and solution; source bank replay, actual grading and representative UI images.

Source gaps remain: q-48846 omits difficulty, solution and key; the existing authored
moderate classification and correct derivative are retained. Blank answer lists
include historical incomplete submissions; they are preserved in the capture,
not served as answer banks. The derivation tutorial's assertion that g(x) differs
from g(a) near a is not generally valid; none of this application's rules uses it.

Inventory finding ab222f0376dcbf24176c belongs to the runner. The refreshed capture
marks all three identified generated radios retired. Original source records and
database content will not be modified. Selection cannot be claimed to reproduce
unknown learner histories or future entity IDs; shared filtering is run read-only.
