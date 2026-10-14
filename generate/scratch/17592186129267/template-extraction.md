# Four extraction stages

## 1. Specific source descriptions

All questions ask to **express**, not evaluate, the displayed triple integral in cylindrical coordinates. The projection is origin-centered and radial range begins at zero. The answer is a complete definite iterated integral with order dz dr dθ, five mathematical radio options, key selection. Practice sources have the common change-of-variables formula, x/y/z conversion, sketch, verbal heights, explicit Δ set, then a fixed aligned substitution chain. q-161520 lacks the chain and rating; q-39481 includes a second legacy field.

| Source / template | Original parameters | Angular sector | Cartesian integrand | Height surfaces | Chain |
|---|---|---|---|---|---|
| q-161520 / half_xz | S=25,H=6 | x≥0, −π/2..π/2 | xz | 0..6+y | absent; normal authored substitution then Jacobian collection |
| q-39481 / full_zradial | S=9,H=10,L=1 | full disk | z sqrt(x²+y²) | 1..10−x | substitute coordinates → factor r²(cos²+sin²) inside root → r²z |
| q-161605 / full_z2radial | S=1,H=1 | full disk | z² sqrt(x²+y²) | 0..1 | substituted root → factor radial square with Jacobian outside → r²z² |
| q-161607 / full_sphere_inverse | S=2,K=16 | full disk | 1/sqrt(1+z) | 0..sqrt(16−x²−y²) | unchanged z function times r → definite integral |
| q-161611 / half_difference | S=9 | x≤0, π/2..3π/2 | x²−y² | x..y² | substituted difference → r times difference of radial squares → r³(cos²−sin²) → double-angle identity |
| q-161612 / half_zdifference | S=5,H=2,L=−1 | y≥0, 0..π | z(x²−y²) | −1..y+2 | same difference chain, with z factor held unchanged |
| q-161613 / quarter_sphere_volume | S=1,K=4 | x≤0,y≥0, π/2..π | 1 | 0..sqrt(4−x²−y²) | direct final Jacobian integral; no extraneous algebra chain |
| q-161604 / full_cone_radial | S=9,H=3 | full disk | sqrt(x²+y²) | sqrt(x²+y²)..3 | substitute root → r sqrt(r²(cos²+sin²)) → r² |

Number forms include integer radii 1/3/5 and sqrt(2)/sqrt(5), integer offsets, hemisphere constants 4/16, a negative lower plane −1, and first/second powers of z. Observed angle endpoints use the standard quadrants and halves. The source uses r≥0; sqrt(r²)=r is valid. Region descriptions and surface ordering are retained.

## 2. Shared generalized pattern

Write x=r cosθ,y=r sinθ,leave z unchanged, convert the original sector and two heights, simplify the substituted integrand with the radial/trigonometric identity and multiply by Jacobian r. Return the whole integral. Normal chains retain each family's original root factorization or difference expansion and the common prose. No integration is requested, and no shifted circle equation is introduced.

## 3. Component and bank map

`source.json` preserves all exact original fields and values. `source-cases.json` assigns every practice question to its template, original parameters and complete public replay profile. `bank-map.json` maps all 45 original displayed strings to a six-component operative integral recipe (theta lower/upper, radial upper, height lower/upper, integrand), including radial lower where nonzero. Modern fields are independently parsed and checked against normal mathematical banks. Flat legacy r 2 text is preserved exactly but needs the independently supported squared-r interpretation from the owning widgets; it is not claimed as valid original TeX. `widget-39481.json` confirms a single five-option question, so normal output retains only the modern field. Its duplicate legacy field and missing designation remain in raw public replay. `widget-161520.json` confirms the assessed xz integral; r²z cosθ is independently correct but its absent source correct ref cannot be counted as matched.

Banks are complete operation lists, never first-valid pools. They include omitted Jacobian, wrong angular sector, x/y swap in a height or integrand, use of the cylinder's squared radius as radial bound, substitution r² for r in the cone, collapse of a sloping plane to its intercept, replacement of a constant z bound by r, and erroneous radial interval R..2R. The 4−r sphere distractor generalizes as sqrt(sqrt(K)−r); this is a preserved expression pattern with uncertain original intent, explicitly distinct from a recovered author algorithm. Source distractors that combine several operations retain those exact combinations. `bank-map.json` provides every complete formula, rather than only error labels.

There are no unseen-choice diagnoses in learner content. Radio choices use complete integral values; scalar equivalence is independently checked, since distinct bounds/integrands alone do not establish unequal answers. At original parameters all interpreted banks are distinct. An early hypothesis that q-39481 had a collision was rejected: its z integrand integrates to a squared top height, and the cos² term survives angular integration. Changed instances with collisions or nonreal options reject the whole chosen bank.

Source repairs are separate: q-161607's first LHS is corrected from 1/sqrt(z) to 1/sqrt(1+z); q-161612's extra trailing r in the expanded middle row is removed. Raw replay preserves both errors. Literal region set braces are escaped only in normal output; exact source strings remain available. Missing q-161520 solution is explicitly authored with the same common formula, coordinate substitutions, heights, region and xz/Jacobian chain.

## 4. Reusable Markdown/value recipes

The script builds whole-component masks for cylinder RHS, radius labels/bounds, independent height parameters and sphere constants. Masks are applied to each captured prompt, solution and bank member. Numeric exponents in integrands are not parameter slots. Normal choices are evaluated by the explicit complete tuple recipes in `banks`; raw replay uses the extracted notation masks and preserves every attribute omission. Seed shuffles choices only after field-owned answer identities and correct ref are established. Identity is based on actual prompt, fixed solution, difficulty and complete displayed bank; equivalent profile aliases do not change identity. Mathematical fingerprint retains assessed Cartesian integrand and region, excludes banks and profile labels.

The bounded domains are S=1..36, H=1..12, L=−4..4, K∈{4,9,16,25,36,49,64,81} with K>S. Default L is −3..3. Sloping planes require H−L>sqrt(S), half y-positive planes H>L, cone H≥sqrt(S). These constraints apply to explicit parameters too. Sampling chooses a family and complete bank before parameters, then rejects whole invalid instances; original profiles are publicly replayable. Radial roots may be exact integers or radicals. Parameter catalog sizes before bank rejection are recorded in `catalog.json`; these are finite scope counts, not counts of proven eligible banks.

Hard `quarter_zdifference` is authored: x≤0,y≥0,lower x,upper H+y²,integrand z(x²−y²). Its fixed solution retains all four difference-chain stages and actual heights. H≥1 prevents reduction to a zero-offset source moderate instance, and quadrant bookkeeping remains. All parameters use only observed substitutions, familiar quadrants and powers. Its bank chooses exactly: correct, omitted Jacobian, squared-radius bound, swapped lower height x→y, omitted H. The optional authored method profile for observed templates uses correct, omitted/duplicate Jacobian, squared-radius bound and combined omitted-Jacobian/squared-radius error. It is clearly labeled, not presented as observed provenance.
