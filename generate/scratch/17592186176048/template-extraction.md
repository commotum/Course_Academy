# Four extraction stages

## 1. Specific observations

q-103242 gives c=-5/8 and shift +12π, returning c; its period/identity, n=6 substitution, expanded full angle and concluding given-value sentence form two display blocks. q-103243 gives sqrt(2)/3 and -14π, using signed n=-7 with parentheses in the expanded angle. q-70671 gives 1/2 and -10π, adding “for some x” and shortening the substitution to a single cosine equality. q-70672 has the same short layout with sqrt(3)/3 and +16π. q-103279 gives 3/8, shift -10π, coefficient 4, offset 5; after the same expanded-angle blocks it has three affine arithmetic rows: substitute c, evaluate 4c, collect 4c+5. The two unrated originals use standard TeX cosine rather than Unicode cos/application; q-65179 gives -1/sqrt(3), shift +10π, and q-65176 gives sqrt(3)/2, shift -6π, scale 4 and offset -1. The authoritative saved lesson 3557/Source/3557.json shows all five choices for both widgets and no original worked solution or answer-key designation.

## 2. General pattern

Given cos(x)=c, recognize a full-period angle x+2nπ and replace its cosine by c. Direct fields require the scalar c. Affine fields require ac+b. Keep coefficient of x exactly +1; no evenness branch. Each answer is a complete scalar math value, with a fixed shared solution independent of selected choice.

## 3. Components and complete banks

Symbols: c=given cosine value, n=nonzero integer periods, a=outer scale, b=offset, R=ac+b. The choice list below follows captured Pull bank order; replay compares one-to-one ignoring order by exact mathematical equivalence. Correct values are c for direct and R for affine. An inferred error name cannot establish author intent; these observed expression recipes are merely explicit parameterized shape continuations. They are available for fidelity, while authored operation banks are normal defaults.

| Profile | Complete source-order bank |
|---|---|
| observed_q65176 | -c, R, c+2n, -c-b, -(a/2)c-b |
| observed_q65179 | -1/c, -1-c, 1/c, c, -c |
| observed_raw_q103242 | -c, π+c+2/denominator(c), c+2π, 2π+c, c |
| observed_q103243 | -c, c, c-2π, denominator(c)c+denominator(c), 2π-c |
| observed_q103279 | R, R/a, -R, 2π+ac, 2π-2c |
| observed_q70671 | c, c+2nπ, c-2π, -c, -c-2nπ |
| observed_q70672 | c, c+2π, -c+2nπ, -c, c+2nπ |

Every source option is covered by source-cases.json and tested individually against the original displayed scalar. No polynomial interpolation or arbitrary numerical perturbation is used. Unusual recipes (especially π+c+2/denominator(c), -1-c, and R/a) have unresolved pedagogical interpretation and are not promoted to defaults. Observed-profile changed-parameter reviews only demonstrate expression-pattern reproducibility. Rational q103242 profile requires rational c; all profiles reject equivalent members as a complete bank except the explicit raw source-error profile.

Authored direct bank: c, -c, c+2π, c-2π, -c+2π (sign reversal and adding/subtracting the period to output). Authored affine bank: R, -ac+b, ac-b, c+b, a(c+b) (sign reversal, offset sign, omitted scale, erroneous distribution). Both are five-option complete banks; collisions reject the entire sampled instance. No learner-facing distractor diagnosis is introduced.

## 4. Reusable templates and constraints

The normal API computes c, n, ac and R exactly with SymPy, renders every prompt/prose/equation slot, then generates and shuffles the complete chosen bank. Shared standard solution: period statement → formal cos identity → signed integer substitution → expanded full-angle equality → conclusion substituting the given c. The short source layout preserves its omitted expanded substitution row. Affine variants append exactly three ordered arithmetic rows; intermediate products stay separate from the final sum, including signed b. The legacy prompt slots retain spaces, π glyph and reciprocal-radical notation for source replay; their missing solutions are authored using standard stages. No copied payload or source-value lookup is returned.

Explicit inputs and samplers share guards: real nonzero |c|≤1; rational denominator ≤12 or listed small radicals; integer n. Easy |n|=1..2, eight familiar c values, a=1,b=0. Moderate |n|=3..10, a=1,b=0. Hard |n|=2..10, 2≤|a|≤6, 1≤|b|≤6. Positive and negative shifts, given values, scales and offsets are equal-level variations. Zero c is excluded to keep all complete authored banks informative. Endpoints c=±1 are valid cosine inputs; they are not transformed via evenness or special-angle evaluation.

Source anomalies: q103242 has two distinct source IDs displaying the same value -5/8+2π. Public observed_raw_q103242 preserves the whole ambiguous bank with distinct notation and identities; native ID grading alone cannot establish mathematical validity. observed_q103242 makes the smallest supported repair: change one duplicate to c-2π. Normal output uses an authored bank unless a profile is explicitly requested. Report raw fidelity (7 banks/35 options), mathematical validity (6 original banks) and the one repair separately. The two unrated missing correct refs are inferred independently as c and R; this is not matched observed designation fidelity. Their missing levels and solutions are explicitly authored, and raw evidence remains unchanged.

Task fingerprint canonicalizes c, a, b and the reduced angle x. Full-period shift aliases and reciprocal-radical spellings cannot inflate mathematical variety; prompt, solution and complete bank govern separate presentation identity. Easy has only eight semantic c tasks, with shift signs/magnitudes offering presentation practice. Moderate has a finite exact-value catalog. Seeds/order do not change identity for fixed displayed mathematics and bank. All work stops at step 7, with no database registration.
