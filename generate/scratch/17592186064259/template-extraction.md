# Polynomial slope templates

The supplied object is a polynomial curve; the requested object is the real
x-coordinate where the tangent has the supplied slope. Fixed stages are:
identify the slope as f'(x), apply the power rule, equate the derivative to the
requested slope, solve the linear/quadratic equation, then select the positive
root when required. Vertical coordinates, tangent equations, new operations,
additional fields, and different branch requests are outside this package.

Slots a,b,c,d,m define f(x)=a*x^3+b*x^2+c*x+d and requested slope m. Original
parameters are stored exactly in the generator's CASES. Every original question
is described below; all number values, answer fragments and bank values remain
in `source.json` and source replay evidence.

| Source | a,b,c,d,m | Roots | Requested answer |
|---|---|---|---|
| q-102236 | 0,1,-3,10,-1 | 1 | radio equation x=1 |
| q-343735 | 0,2,4,-3,1 | -3/4 | blank fragment -3/4 |
| q-343737 | 1,1,14,-6,22 | -2,4/3 | positive blank fragment 4/3 |
| q-48692 | 1,-2,-5,0,27 | -8/3,4 | positive radio equation x=4; inferred absent key |
| q-48970 | 8,-3,-12,-4,6 | -3/4,1 | positive radio equation x=1 |
| q-48817 | -2,6,20,-1,2 | -1,3 | radio equation containing BOTH roots |
| q-48816 | 1,3,6,-3,3 | -1 (double) | radio equation x=-1; inferred absent key |
| q-128236 | function absent; derivative given only in prior-step solution | k=-8 in solution | excluded context-dependent blank |

Profiles are selected as complete banks before sampling. Let r be the requested
single root, and u<0<v the two roots. These recipes account for EVERY original
option (including the correct one), ignoring choice order:

- q-102236: x=-r, -2r, 0, 2r, r; at r=1, matches -1,-2,0,2,1.
- q-48816: x=-r, r, -2r, 2r, 0; at r=-1, matches 1,-1,2,-2,0.
- q-48692: x=r-1, r+1, r, r-2, r-3; at r=4, matches 3,5,4,2,1.
- q-48970: x=12r, 2r, r, 3r, 4r; at r=1, matches 12,2,1,3,4.
- q-48817: x=v; x=-v; x=-u; x=-v,-u; x=u,v. At u=-1,v=3,
  matches 3; -3; 1; -3,1; -1,3. The field remains a single radio choice
  representing a full pair, not an independently selected subset.
- q-343735 and q-343737: one canonical numeric fragment, no distractor profile.

The intent behind offsets/multipliers is unresolved; these are observed value
patterns, not asserted misconception diagnoses. They are not replaced with a
pooled bank or presented as learner feedback. Bank collisions reject the entire
instance. Values and identities are field-owned, with no delimiters in storage.

Sampling is a conservative same-method extension: signed integer coefficients
of magnitude <=200, nonzero quadratic coefficient for quadratic templates,
nonzero cubic coefficient for cubic templates, exact rational roots, one positive
and one negative root for positive/all cubic templates, a nonzero repeated root
for the repeated template. Positive-offset roots exceed 3 so the observed bank
continues to consist of positive locations. Quadratic roots are nonzero. Signed
leading terms, nonzero shifts, zero constant terms, rational/integer answers and
all defined roles are retained; CASES preserves every original coefficient.
The normal sampler uses a narrower finite range documented in the Python script.
It varies coefficients and slopes, constructs cubic equations from rational
roots, and rejects nonintegral coefficients. Continuous/unbounded generation is
not claimed. No location/target slots exist apart from the numeric root request.

Normal prompts standardize spacing and TeX and add an explicit radio placeholder.
Solutions preserve source instructional stages but standardize TeX, render a
separate evaluated power-rule row, and put all polynomial solving steps into an
aligned block. This is a documented layout/wording extension, not exact prose
fidelity. Source replay compares the entire mathematical curve, slope, branch,
field type, every bank object and every present correct designation. q-343737's
conclusion typo is locally corrected; no database source repair is authorized.

Plots: none. No plot extraction, generation or asset publication is needed.

Mathematical deduplication uses the monic derivative-minus-slope equation plus
the requested branch. Constants, simultaneous derivative/slope shifts, polynomial
scale aliases, seed, UUID, response type and bank order cannot inflate inventory.
For example two vertically translated curves with the same slope equation count
as one task even though their rendered prompts differ. Original and canonical
tasks are excluded from generation by this stricter fingerprint.
