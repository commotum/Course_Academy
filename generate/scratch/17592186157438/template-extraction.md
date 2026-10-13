# Template extraction

Source wrapper/provenance and all original values are in source.json; complete original and generated learner content appears in review.md. layouts.json stores nonmathematical prose and whole mathematical-component slots; build_layouts.py extracts these masks reproducibly. No literal-source return path exists.

## 1. Describe each original before generalizing

All equations have one repeated positive exponential factor with base e or a positive integer, and affine real exponent. The factor never contributes a real zero. The requested answers are exact scalar fragments: ascending roots in separate keyed blanks or one scalar product in a five-option bank.

| Source | Polynomial after rearrangement | Common exponential | Required response / distinct stages |
|---|---|---|---|
| q237949 (unrated) | 3x²−5x−2 | e^(x+5) | ascending roots; source prose has `are$x =`; two widgets confirmed; solution absent |
| q88417 (unrated) | 4x²−25 | e^x | product; original five choices; solution and correct ref absent |
| q88472 moderate | 4x²+4x−3 | e^(5x) | product; right constant minus linear; no fields |
| q100797 moderate | 5x²−13x−6 | 8^x | product; right linear plus constant; first solution opening contains an extra blank whitespace row |
| q264786 easy | 2x²−50 | 3^(2x−5) | ascending −5,5; 2(x²−25) then 2(x+5)(x−5); scalar 2=0 excluded |
| q264787 easy | 4x²−144 | 5^(x−4) | ascending −6,6; same scalar stages as q264786 |
| q264788 easy | 9x²−64 | e^(x+3) | ascending −8/3,8/3; one aligned (3x+8)(3x−8) factor row; Pull lists field2 before field1 |
| q264791 moderate | 3x²+11x+6 | 7^x | ascending −3,−2/3; (3x+2)(x+3); captured second equation row has a trailing + |
| q264793 moderate | 4x²−25x+6 | e^(2x) | ascending 1/4,6; (4x−1)(x−6); first listing repeats x= before 6 |
| q88473 moderate | 3x²+4x−7 | 6^(x−2) | product −7/3; moves quadratic from right to left |
| q88474 moderate | 3x²−6x−45 | 5^x | product −15; scalar 3(x+3)(x−5) in aligned row without alignment marker; scalar 3=0 excluded |
| q110803 easy | x²−1 | 10^(2−x) | product −1; juxtaposition, no multiplication dots; reversed exponent ordering |

Original prompts and complete solutions retain their punctuation, spacing, braced x², multiplication style, display wrappers, optional aligned-factor rows, repeated x=, and row count. Whole math slots are filled with calculated components, not global short-text substitutions. Normal numeric constants beside numeric exponential bases gain a visible multiplication dot to prevent 49·10^u from rendering as 4910^u; the original unit-coefficient source remains exact.

## 2. Shared pattern and instructional purpose

Rearrange both sides into zero, factor out the common strictly positive exponential, use zero product, factor the residual quadratic, list two real roots, and either order them or multiply them. The common real domain and positivity argument are essential. Exponential evaluation, taking logarithms, solving unequal-base exponentials, hyperbolic simplification, and additional polynomial degrees are excluded.

Represent the quadratic as `g(px+q)(rx+s)` with positive integer g,p,r and nonzero signed q,s. Compute `A=gpr`, `B=g(ps+qr)`, `C=gqs`, roots `−q/p, −s/r` sorted, and product `C/A`. The templates control which complete terms start on which side. This factor parameterization guarantees an exactly factorable quadratic; it does not add a new skill.

## 3. Components, fields, and complete observed banks

source-cases.json maps every source to normal generator parameters, template, level assignment, and original profile. choice-mapping.json lists every original answer UUID, field, value, correct-presence flag, and parameterized expression shape. Field placeholders determine which sorted root belongs to which key; Pull field order is preserved independently of value order. Missing blank values in q237949 are derived separately as −1/3 and 2.

In the following complete bank mappings `t=C/A`, `a,b` are ascending roots, and A,B,C are the rearranged quadratic coefficients. Every listed value is reproduced, not just the correct choice. The source scalar options do not uniquely establish their author's error intent. These profiles are explicit replay expression shapes, have unresolved interpretation, and are never used by default.

| Profile / selection field | Source value → parameterized expression (entire bank) |
|---|---|
| observed:q88417 | −25/4→t; 4/25→−1/t; −1/25→−1/(−C); 1/4→1/A; 25→−C |
| observed:q100797 | 30→A(−C); −6/5→t; −5/6→1/t; −1/5→−1/A; −1/6→1/C |
| observed:q88473 | 3→A; −2/3→−(A−1)/A; 10/3→(A−C)/A; −7/3→t; −7→C |
| observed:q88474 | 10→2b; −5→−b; 5/3→b/A; −9/5→−A²/b; −15→t |
| observed:q110803 | 2→b−a; 1→b; 0→0; −1→t; −2→a−b |

Those mappings preserve observed expression forms, not recovered misconception code. They are mathematically parameterized rather than unrelated random perturbations or fitted polynomials. Changed-parameter examples are labeled replay-profile variants, not recovered author intent. A complete bank is chosen before sampling. If any required value coincides with another, the entire instance is rejected. No first-valid option pool or mixing profiles is used.

The authored default product bank has exactly five operations: correct product t, sign reversal −t, reciprocal 1/t, root sum a+b, and omitted leading divisor C. For monic difference-of-squares template A=1 the last operation would duplicate t, so its complete separately defined specialization uses root difference b−a. This is a method-derived authored bank, with no learner-facing diagnosis. Whole-bank collisions (including t=±1) reject the instance. The observed q110803 original t=−1 is valid under its distinct observed bank.

## 4. Reusable Markdown/value templates and bounds

Fixed prose follows the exact sources: factoring opening; zero-product statement with ab=0 iff a=0 or b=0; two equations; solving separately; polynomial factor stage; roots; exponential positivity sentence; and response-specific final sentence. The scalar impossibility sentence and two-stage common-scalar factor display are conditional on their original template, not indiscriminately added. Missing solutions q237949 and q88417 receive an explicitly authored solution using these shared stages. q264791 receives the smallest mathematical presentation correction, deletion of a trailing +. It is 1 repaired solution, not an exact solution.

Variable complete components are the full original equation, distributed rearrangement row, polynomial, exponential, complete factor-stage display, sorted root listing, and final product calculation. Complete source math spans become these slots; scalar parameters never replace prose, zero-product variables, field keys, or exponent literals globally. Exact rational LaTeX uses source `\frac` without CAS spaces after the leading minus. EDB radio values with doubled backslashes normalize to the same math; this notation normalization is distinct from string-level prompt/solution fidelity.

All explicit parameters obey the same documented bounds as sampling; bad values raise rather than changing the instance. The exponential base is e or integer 2..10, nonzero affine slope magnitude at most 5 and shift magnitude at most 6. Exponent changes affect presentation, not task variety.

Easy keeps B=0 and paired linear factors. Integer-root scalar templates use p=r=1, g=2..6; rational difference-square templates use g=1, p=r=2..6. Root numerators extend to 1..12, retaining familiar perfect squares; they are bounded authored peer variation, not a new branch. The monic reversed-exponent product uses p=r=g=1, slope −1 and shift 1..6. This narrow family has 12 meaningful root magnitudes (10 under the collision-free authored bank: root magnitudes 1 and 2 collide); the integer blank has 12. Coefficient scaling and exponent choices are excluded from the monic-polynomial task fingerprint. The rational templates require primitive linear factors (gcd(p,|q|)=1), so their nonunit denominators survive rather than collapsing into a monic task. With p=2..6 and numerator 1..12 there are exactly 34 reduced root magnitudes per rational layout. The broader rational templates supply these additional easy peer tasks; no misleading claim of dozens of distinct integer-root tasks is made.

Moderate has nonzero B,C, A≤6, |B|≤30, |C|≤60, factor-constant magnitude ≤8; source stage constraints remain enforced. Most families have g=r=1 with p≥2 and one nonunit leading factor. Each linear factor is primitive: gcd(p,|q|)=gcd(r,|s|)=1. This prevents hidden scalar GCF extraction from replacing the advertised nonmonic workload. q88472's equal-leading family uses p=r=2 and g=1 under the coefficient cap. The scalar-monic family has p=r=1,g≥2. Negative/positive ordered-root families enforce both roots' original signs. Samplers use constants up to 7 (up to 6 in the scalar-monic family), and source q88473's 7 remains accepted. Equal-leading family p=r=2 samples both signs with odd constants after primitive-factor rejection. Its bounded domain has 24 distinct normalized quadratics: two roots chosen from ±1/2,±3/2,±5/2,±7/2, excluding repeated roots and zero linear coefficient. This supplies same-level signed-factor peer tasks without adding another branch.

Hard has **no observed difficulty label** and is an authored scope claim. It starts with five nonzero exponential-polynomial terms split across both sides: `(A+d)x²E + l xE + CE = d x²E + (l−B)xE`. After moving right terms, both quadratic and linear coefficients require collection before the common factor is extracted; the four initial solution rows display the original equation, all five moved terms before collection, the collected three-term sum, and the common-factor product. Factoring is the same prerequisite nonmonic quadratic method, now with two nonunit leading factors. Choose g=1, p,r=2..4, |q|,|s|≤6, A≤16, |B|≤48, |C|≤36, d=1..4, l=1..6 and l≠B, B,C≠0, distinct roots. Five original terms, two coefficient collections, two linear-factor roots, and one positivity exclusion define the equal-level workload. Both hard linear factors must be primitive, so neither nonunit coefficient disappears through scalar extraction and both roots remain noninteger rationals. Two response layouts are peer alternatives, not a progression. The canonical rational-root example, prerequisite 1422, and the introduction's positivity argument support this authored extension. This keeps the distinguishing rearrangement step and never generates the sibling KP's already-zero initial equation.

Content identity includes version, actual rendered prompt, fixed full solution, and sorted full banks independent of option order/seed. Mathematical task fingerprints use normalized polynomial coefficients, response shape, and rearrangement family; they exclude exponent, source profile, bank, scalar spelling, and seed. Distinct banks change presentation identity but not the mathematical-task fingerprint. No plots are needed.

## Source anomalies and independently verified repairs

Original widgets were read from `/home/jake/Developer/MA/DATA/Lessons/2979/Source/2979.json`, and both available screenshots were visually inspected. Evidence copies are original-widgets.json and the two PNGs.

* q237949: widget confirms freeResponseTextbox1/2 are ordered math-entry blanks. `(3x+1)(x−2)=3x²−5x−2`, so roots are −1/3 and 2. No correct designation is visible in the widget. Two repaired values/designations, zero observed matches.
* q88417: widget confirms the full five-choice bank and no correct designation. `(2x+5)(2x−5)=4x²−25` and e^x>0 give roots −5/2,5/2 and product −25/4. Five values match; no missing designation is counted matched.
* q88472: absent from the available original widget snapshot. Raw EDB problem/solution agree: `(2x+3)(2x−1)=4x²+4x−3`, roots −3/2,1/2, product −3/4. The supported radio field/bank is authored and explicitly contributes no original-field/bank/designation matches.
* q264791: the source distributed row ends `+ & =0`, a syntax error. Delete only that trailing +; the row then expands to 3x²+11x+6 times E and has the independently checked roots −3,−2/3. Full original prose/stage sequence remains otherwise unchanged.

No unresolved field or correct-ref evidence is silently treated as fidelity success. Mathematical correctness, repaired presentation, original-value matches, designation matches, and native grading are separate results.
