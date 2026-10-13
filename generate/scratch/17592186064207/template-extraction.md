# Extraction

Every supported question asks for an antiderivative of n/(ax+b), with x real, a and n nonzero, x excluding -b/a. Responses are a radio selection of one math expression, containing an arbitrary positive K. The solution substitutes u=ax+b, computes du/dx=a and dx=du/a, integrates 1/u, then rewrites C=(n/a)ln K and combines logs. Since K ranges over positive reals and n/a is nonzero, that expression represents every real C independently on each connected domain interval.

The exact source-by-source prompt, worked solution, choices and correct values are retained in source.json and reference/source.edn. contract.json contains six source-specific Markdown templates, original parameter tuples, and original complete banks. Generator bank() records the full parameterized transformations in source order. No pooled or mixed profiles are used. Placeholders D, R, J, N, A stand for the rendered affine denominator, n/a, 1/a, numerator, and signed slope. All instructional sentences and each source's solution sequence are fixed. Source replay requires byte equality for prompt, solution and complete answer bank, preserving designation and count while ignoring order.

| Source | (n,a,b) | Mathematical features | Complete bank recipes in source order |
|---|---|---|---|
| q-113532 | (1,2,3) | positive nonunit slope, unit numerator | (1/b)ln(K|D|); (a/b)ln(K|D|); ln(|D|/K); (1/a)ln(K|D|), correct; (K/a)ln(|D|) |
| q-30368 | (1,3,4) | same integrand shape at observed moderate level; shorter log combination | (b/a)ln(K|D|); a ln(K|D|); (1/b)ln(K|D|); (1/a)ln(K|D|), correct; (a/b)ln(K|D|) |
| q-113537 | (4,5,3) | nonunit positive numerator and slope; factors numerator explicitly | n ln(K|D|); (1/a)ln(K|D|); (-n/a)ln(K|D|); (a/n)ln(K|D|); (n/a)ln(K|D|), correct |
| q-113538 | (3,-4,1) | signed slope, explicit negative Jacobian and constant coefficient | (-n/(2a))ln(K/|D|); (n/a)ln(K|D|), correct; (-n/a)ln(K|D|); (1/(2a))ln(K|D|); n ln(K|D|) |
| q-72445 | (1,-1,7) | fixed negative unit slope | -ln(K|D|), correct; (-1/b)ln(K|D|); (1/2)ln(K|D|); ln(K|D|); (1/b)ln(K|D|) |
| q-72446 | (1,-2,5) | negative nonunit slope | (-1/a)ln(K|D|); (-a)ln(K|D|); ln(K|D|); (1/a)ln(K|D|), correct; a ln(K|D|) |

D denotes ax+b (rendered b-|a|x when a is negative). These are observed expression patterns; sparse single-bank evidence does not establish the learner's underlying mistake. The fixed 1/2 option in q-72445 stays fixed; no invented misconception is shown. All source options reproduce exactly at their source parameters.

Proposed bounded sampling is narrower than the universe of possible integrals: positive slopes 2..6, negative nonunit slopes -6..-2, positive shifts through 9, nonunit numerators 2..6; q-72445 fixes a=-1 and n=1 and samples b=3..9. Positive unit-numerator banks exclude b=a, b=a², and a=b²; positive scaled banks exclude n=a, n=a², and a=n², which would collide or change a coefficient's notation/layout. All observed parameters and signs are included. Actual constraints and complete enumerations are in allowed() and candidates(). No new difficulty assignment is inferred from parameter size.

The K-dependent option in q-113532 has derivative K/a times a/D, so it is not an identity for an arbitrary positive K and cannot represent the arbitrary integration constant: changing K changes its derivative. It can accidentally agree at an isolated K, which does not make it an arbitrary-K antiderivative formula. Validation compares whole symbolic derivative functions with K free.

The excluded q-113533 bank has two correct families: (1/3)ln(K|3x+4|) and (1/3)ln(|3x+4|/K). Both differentiate to 1/(3x+4), and their difference is a constant in x. The original bank remains unchanged; this profile is excluded rather than emitting an ambiguous question. q-49513, q-49516 and q-49515 lack essential grading records and are also excluded. Their full source evidence remains in the package.

Distinctness is the reduced exact rational integrand, compared against every current KP question and the canonical example. Alternate banks, source profiles, constant spelling, identities, seeds, and option order cannot manufacture another inventory question for the same integrand.
