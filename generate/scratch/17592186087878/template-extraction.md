# Template extraction

## 1. Specific observed objects

Read `source.json` for every original prompt, whole answer bank, field order, UUID, raw notation and full worked solution. `source-cases.json` assigns every question to its own complete original bank and parameters. Inline legacy prompts differ from display-math current prompts; q-334915 has a colon/blank-line arrangement and legacy banks, q-335069 has a nonunit derivative coefficient, and q-335392 has x² forcing. Current prose distinguishes “already in the standard form” (q-335402) from “in the standard form”. Sources retain different IF row counts, a redundant log-to-power row in the moderate solutions, a direct derivative row before integration in easy and hard, and explicit IBP rows in hard. Every difference is preserved by whole mathematical-component masks.

All parameters are exact integers. Reciprocal coefficient families use x>0, permitting ln x and xⁿ IF without an absolute-value branch. C is arbitrary and belongs only to the solution field. No source assesses a particular solution fixed by initial data; every solution field represents an affine one-parameter family.

## 2. Generalized mathematical patterns

Write y′+P(x)y=Q(x), find I=e^(∫P dx), multiply and distribute, rewrite (Iy)′=IQ, integrate, and divide by I. Easy sources have constant P and direct integration after exponential combination/cancellation. Moderate sources require integrating n/x, using x>0 and a power IF. Hard uses exactly one integration-by-parts operation after the factor. The canonical cosine example and captured hard sine example support cosine/sine peers with IQ=x trig(rx).

## 3. Complete component/bank mappings

The executable `build` computes P,Q,I,F=∫IQ dx,Y=(F+C)/I before assembling complete banks. `bank-mapping.json` records **every** original option, its whole parameterized expression at original parameters, and exact mathematical match. No option is selected from a pool or replaced by a first-valid substitute.

Use A=a, B=b, R=r, N=n, M=m, K=k. In the following lists every semicolon separates an option; these are complete jointly observed profiles, not a pool.

| Profile | IF bank | Solution bank |
|---|---|---|
| q-335402 | e^(Rx); e^(Ax); e^(−Ax); e^(−Rx) | B/(R−A)e^((R−A)x)+Ce^(−Ax); −B/(R−A)e^(Rx)+Ce^(Ax); −B/(R−A)e^(−Rx)+Ce^(−Ax); B/(R−A)e^(Rx)+Ce^(Ax) |
| q-339138 / q-335392 | A ln x; e^(Ax); −A; e^(−Ax) | x^M e^(−Ax)/(M+1)+Ce^(−Ax); x^(M+1)e^(Ax)/(M+1)+Ce^(−Ax); x^M e^(−Ax)/(M+1)+Ce^(Ax); x^(M+1)e^(Ax)/(M+1)+Ce^(Ax) |
| q-339140 | x^(N−1); ln x; 1/x; x^N | x+C/x^(N−1); Bx/(N+1)+C/x^N; Bx/(N+1)+C/x^(N−1); x+C/x^N |
| q-334915 | x^(N−1); ln x; 1/x; x^N | Bx/(N+1)+C/x^N; Bx²/(N+1)+C/x^N; Bx²/(N+1)+C/x^(N−1); Bx/(N+1)+C/x^(N−1) |
| q-335412 | N/x; x^N; e^(N/x); e^(x^N) | (e^(Rx)/R+C)/x^N; x^(N−1)(e^(Rx)/R+C); (e^(Rx)/R+C)/x^(N−1); x^N(e^(Rx)/R+C) |
| q-335409 | N/x; e^(x^N); x^N; e^(N/x) | S−T+C/x^N; U+V+C/x^N; U−V+C/x^(N−1); S+T+C/x^(N−1); S−T+C/x^N |
| q-335069 | Kx; x^K; e^(−x/K); e^(x/K) | Bx−K+Ce^(x/K); B(x−K)+Ce^(−x/K); B(x−K)+Ce^(x/K); Bx−K+Ce^(−x/K) |

For the hard sine bank S=sin(Rx)/(R² x^N), T=cos(Rx)/(R x^(N−1)), U=sin(Rx)/(R² x^(N−1)), V=cos(Rx)/(R x^N). The duplicated fifth source option is repaired to S−T+C/x^(N−1). The authored cosine peer uses S=cos(Rx)/(R² x^N), T=sin(Rx)/(R x^(N−1)), and swapped powers U,V; it changes the fourth sign to prevent cosine's positive particular solution from duplicating its fifth option.

For q-334915 the correct x coefficient is B/(N+1); source IF option ordering is irrelevant. Numerical values from q-339140 (wrong x) and q-335069 (Kx and x^K) do not uniquely determine intended errors. These are **observed structural replay recipes**, not recovered student intentions. The authored q-339140 default bank uses Bx/N instead of x, a defined omission of the +1 in the integrated exponent denominator. The authored q-335069 IF bank replaces the underdetermined Kx/x^K source distractors with P=1/K and e^(Kx), explicitly confusing the coefficient with its reciprocal. Other banks express explicit sign, power, IF reciprocal, denominator/multiplication and integration-constant exponent changes; interpretations are inferred structural patterns, never learner-facing diagnosis. No distractor explanation is added to fixed worked solutions.

## 4. Reusable masks and constraints

Immutable fixed prose and Markdown delimiters come from the source capture. `fill_math` substitutes entire inline/display components in order, leaving prose untouched. Builders preserve every mathematical stage and omission; original parameter runs have exact prompt/solution stage strings without literal-payload branches. Changed parameters compute all components, banks, intermediate values and final answers. The three missing explanations are authored using shared source prose; the normalized equation's authored explanation additionally spells out standardization and the full exponential IBP scaffold.

Bounds are checked for random **and explicit** inputs:

- Easy exponential forcing: 2≤A≤6, 2≤B≤9, 1≤R≤5, R≠A. Easy cancellation: 2≤A≤6, M∈{1,2}; both are direct power integration after cancellation.
- Moderate power constant: 2≤N≤6, 2≤B≤9. Power exponential: 2≤N≤6, 1≤R≤3. All preserve reciprocal P and one direct integral after IF multiplication.
- Hard sine/cosine: 2≤N≤6, 1≤R≤3 with Q=trig(Rx)/x^(N−1); IQ remains exactly x trig(Rx), so every peer has one IBP. Hard nonstandard linear forcing: 2≤K≤4, 2≤B≤6, derivative coefficient remains nonunit and forcing remains linear.

Whole instances are rejected on collisions or absent/extra correct options; q-339140 observed bank rejects B=N+1. The raw q-335409 profile is marked evidence-only when explicit parameters are supplied, and rejects random learner generation because it is mathematically ambiguous. `generate` replays its complete raw bank only under the explicit evidence-only profile; every normal record has a unique correct mathematical family. Source cases explicitly name both original and repaired profile where needed.

IF equivalence permits constant scaling. General-solution equivalence permits C→aC+b, a≠0; it checks homogeneous coefficients and particular-solution differences. Independent validation substitutes every actual displayed solution into the actual displayed ODE, reads every aligned mathematical row, and checks arbitrary-C final families. Canonical task fingerprints contain normalized P,Q, domain and assessed IF/general-solution demand, excluding profiles/banks/prose. Content identities include actual prompt, fixed solution, complete displayed banks and version; seed/option order cannot change identity.

No plots: step 5 and step 7 require no renderer or assets for this KP.

The finite documented authored parameter domains contain 178 distinct easy tasks (168 nonresonant exponential-forcing tasks plus 10 cancellation tasks), 55 moderate tasks (40 reciprocal constant-forcing plus 15 reciprocal exponential-forcing), and 45 hard tasks (15 sine, 15 cosine, 15 normalized-linear). Legacy layouts and bank profiles do not inflate these counts. The validator also reports the actual deduplicated sampled counts separately; numerical upper bounds are not claimed as exhaustively tested instances.
