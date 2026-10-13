# Four-stage extraction

## 1. Specific originals

`classification.md` lists every source, original expression, point, field layout and row count. `source.json` is the complete raw record including all fields and answer UUIDs. `source-cases.json` is the original parameter replay map. The 11 solutions share the same prose: differentiation using the product rule, primitive identification, product-rule application, substitution to find tangent slope, final slope sentence. Named functions preserve a two-row aligned primitive-derivative block, with formal d/dx(f-expression)=f′ and d/dx(h-expression)=h′; the actual arguments and derivatives are checked separately. Other sources preserve simultaneous component derivative statements. Named functions use “Recall that” and “Then,” rather than “Let” and “Then, we have”. q319829 omits a reduced derivative row; q319842 and q319829 combine evaluated arithmetic and final equality. q319842 evaluates each polynomial monomial first, retains signs on zero components (1·(0−0+3)=3), and never introduces a 0^0 substitution row. Authored hard solutions separately show actual substitution, individually evaluated primitive factors, and final collected slope; trig/log evaluation stages have structural assertions beyond equality. q48515/q48517 include a symbolic evaluation row before actual substitution, while q48516/q48993 use that row followed by evaluated terms. These distinct stage counts are checked.

q48391 and q48901 have neither source difficulty, correct designation nor solution. Independent differentiation gives slopes 4 and 6π² respectively. The MA1109 authoritative capture `/home/jake/Developer/MA/DATA/Lessons/1109/Source/1109.json` contains the same complete five-choice widgets (question IDs 48391 and 48901), with no extra fields. Assignments easy/moderate and reconstructed solutions are explicitly authored. q31226 has no field: slope 3π² independently determines a supported blank; this is not counted as an observed matched field/designation.

## 2. Shared pattern

Given an explicit product y=u(x)v(x) and a defined evaluation point t, compute u′ and v′, distribute u v′ + v u′, reduce, evaluate at t, and give a scalar slope. Source number forms include small integer polynomial coefficients, natural exponentials, integer/half/quarter turns, and unit logarithm arguments. Functions and derivatives must be defined at t. Logs use natural-log notation; exact answers are preserved.

## 3. Component and complete-bank mapping

Symbols below refer to prompt parameters; every option is computed by the script's `observed_bank`, not copied answer strings. Correctness is assigned by comparing the independently calculated product derivative at t with the complete generated bank. Source IDs/UUIDs and raw values remain in source.json.

| Complete radio profile | Parameters at source | Ordered expression patterns (order ignored in fidelity) | Interpretation limit |
|---|---|---|---|
| q48391 | a=2,b=1,t=0 | a; 2a; √|a| e; 0; ae | Scalar values do not identify error operations; explicit replay pattern only |
| q48901 | a=8,n=3,t=π/2 | 3aπ²/8; −6aπ²/8; −3aπ²/8; 0; 6aπ²/8 | Coefficient-scaled observed patterns; no asserted original error intent |
| q48515 | a=3,b=−2,t=1 | ln(a); a+b; a+b−ln(−b); a−b+2ln(a−b); −2(a+b+1) | Opaque observed algebraic pattern, not recovered pedagogical recipes |
| q48516 | a=1,t=π,m=−e^π | 0; −m; m; −tm; tm | Explicit zero/sign/point scaling |
| q48517 | a=1,b=−1,n=3,t=2 | ne+(t^n+b−2); exp(t)+t; exp(t)+b; m; 2te | Opaque observed expression pattern; original operation intent unresolved |
| q48993 | a=1,b=0,t=e,m=2 | m; u(t)v(t); −u(t)v(t); −m; 0 | Correct slope, function value, sign reversals, zero |

All six blank source answers are independently derived full scalar slopes: −2, 2e^π (two sources), −π/2−2, 0, 3. There are 36 observed values, of which 24 are radio distractors. Original correct designations exist for 10 sources; the two missing radio correct refs and fieldless correct ref are inferred, never counted matched.

Default authored radio profile is the entire five-operation bank: m; −m; u(t)v(t); u′(t)+v′(t); u′(t)−v′(t). It assesses confusion between product rule, differentiation of sums/differences, function value and slope sign. For power-sine at the source half-turn points, the complete authored bank instead uses m; −m; u(t)v(t); n u(t)v(t) (wrong power reduction); a t^(n−1)v(t) (omitted degree multiplier). The primitive-sum bank would collide with the correct value there and is not eligible. All five values must be finite, real and pairwise unequal; the whole instance is rejected on a collision. Opaque observed banks are not used by default. No fabricated distractor explanation appears in learner content.

## 4. Reusable templates and constraints

The script constructs complete mathematical components before inserting them into original prompt math spans. It never globally replaces short parameter strings across prose. Original prose/whitespace remains the prompt shell, while normal output supplies missing f/h definitions. Source-specific solutions preserve shared fixed prose and ordered stages with normalized TeX; reductions retain rational sums or factored exponentials, and arithmetic masks avoid eager CAS collapse. No raw-exact solution claim is made. Two absent source solutions are fully authored. Every generated blank has `{{field-1}}`.

`observed` replays each complete observed bank with supported fields/context; `observed_raw` preserves missing f/h prompt context as explicit evidence while still computing the bank and solution. The two raw replay records are stored separately. No missing fields/correct refs are silently skipped. There are no known source mathematical answer errors. Changes are presentation normalization, two missing-context repairs, one field repair and three inferred designations.

All explicit inputs receive the same scope guards as sampled inputs: nonzero integer leading coefficients except the named half-scale; |coefficients|≤9; degrees 2 or 3; small integer exp points; familiar trig points; positive familiar log points. Shifted-log arguments equal 1 at the point, k=1…5. Easy exponential t=0 and shift 1…4; easy logarithm b=0,t=e. Hard all a,b,c nonzero integers with |a,b,c|≤5; trig points odd multiples of π/4; log t=e/e²; both contributions nonzero. Sampling bounds are authored policies, not recovered source code.

Mathematical fingerprint hashes the canonical expanded displayed function and point, excluding field/profile/answer banks. Content identity hashes version, actual prompt, fixed solution and complete bank (choice order ignored); parameter aliases/source-profile aliases do not create new identity. Seeds control only sampling and option order. No plots; steps 5/7 need no renderer. Native grading uses the shared captured check-engine without database writes.
