# Template extraction

## 1. Specific source descriptions

`source-cases.json` records every exact factor/exponential tuple and source level. Write
P(x)=g(ax+b)(cx+d), A=gac, B=g(ad+bc), C=gbd, E(x)=base^(kx+h).
The complete displayed prompt is Ax²E+BxE+CE=0, with B omitted only in the easy difference-of-squares family. These are real equations; bases are positive and never one.

| Source | g; (a,b); (c,d) | base; k,h | Assessed response / source display |
|---|---|---|---|
| q-237947 | 1; (1,2); (1,3) | 4; 1,1 | roots −3,−2, two blanks; factors (x+2)(x+3) |
| q-88412 | 1; (1,3); (1,−3) | e; 2,0 | product −9; legacy unbraced e prompt; no supplied solution/ref/level |
| q-100781 | 1; (1,−2); (1,−6) | 7; 1,−3 | product 12; extra original whitespace after opening preserved |
| q-100785 | 1; (1,6); (1,−6) | e; 9,0 | product −36; e juxtaposition, negative root parenthesized |
| q-237946 | 1; (1,3); (1,−3) | 5; 3,0 | roots −3,3, two blanks |
| q-264754 | 2; (1,−5); (1,5) | 7; 2,0 | roots −5,5; two-row GCF factoring and false-scalar paragraph |
| q-264772 | 2; (1,6); (1,−4) | 3; 1,0 | roots −6,4; two-row GCF factoring and false-scalar paragraph |
| q-264778 | 1; (2,−1); (1,−3) | 2; 1,3 | roots 1/2,3; primitive leading factor |
| q-264780 | 1; (1,7); (1,4) | 5; 2,1 | roots −7,−4; factors preserve x+7 then x+4 |
| q-88458 | 1; (1,−3); (1,−4) | 3; 1,2 | product 12; underidentified scalar bank |
| q-88460 | 1; (2,−1); (1,−4) | 6; 1,3 | product 2; underidentified scalar bank |
| q-110801 | 1; (1,1); (1,−1) | 7; −1,2 | product −1; exponent 2−x, extra original whitespace, bare −1 product |
| q-88454 | 1; (1,5); (1,−5) | 4; 3,0 | product −25 |
| q-88459 | 2; (1,1); (1,5) | 2; 1,−1 | product 5; GCF single-row factoring |

All displayed choices are delimiter-free math fragments. Two blanks retain their distinct field keys and original captured field order. `display-profiles.json` consists of nonmathematical masks with whole mathematical component slots, source punctuation/layout flags, and field ordering. It contains no answer lookup or original mathematical payload.

## 2. Shared instructional pattern

Take out the common positive exponential, apply the zero-product property, factor the remaining quadratic, discard the impossible exponential equation, and report either both real roots in ascending order or their product. Within each level the variants are peers, with no progression or added mathematical branch.

## 3. Every source bank and mathematical component

Let u<v be the two roots, z=uv, and r the positive radius for opposite roots. All rows below describe a complete five-choice bank chosen before evaluating any option. Interpretation is an authoring hypothesis unless explicitly marked; recipes are algebraic patterns that generalize displayed source values.

| Profile | Exact original choices (captured order) | Complete parameterized bank | Interpretation status |
|---|---|---|---|
| q-88412 | −9,9,−3,3,0 | z,−z,u,v,0 | same symmetric-root pattern; correct designation unavailable |
| q-100785 | −36,−6,0,36,6 | z,−z,u,v,0 | root/product/sign/false exponential root |
| q-88454 | −5,25,0,−25,5 | z,−z,u,v,0 | same complete bank |
| q-110801 | 2,1,0,−1,−2 | 2v,−z,0,z,2u | doubled-root scalar pattern; original intent underidentified |
| q-100781 | 6,8,2,24,12 | v,u+v,u,2z,z | single root, sum, doubled product |
| q-88458 | 6,−8,−4,12,8 | z/2,−2v,−v,z,2v | replay-only expression pattern; intent underidentified |
| q-88459 | −5,10,−10,15,5 | −z,2z,−2z,3z,z | replay-only scalar factors; intent underidentified |
| q-88460 | −6,3/4,1/8,−1/4,2 | −3z,3z/8,z/16,−z/8,z | replay-only scalar factors; intent underidentified |

All six blank sources produce u and v from their two root parameters, not from bank lookup. There are 52 original displayed values total (40 radio values and 12 blank values), 19 available source field designations, and one unavailable designation. Thirty-two radio alternatives are reproduced; the four alternatives in q-88412 are designated incorrect by independently verified derivation, not an original ref.

The mathematical stage mask maps: original distributed equation → factored common exponential (two aligned rows); fixed zero-product rule; separate P=0 and E=0; repeated P=0; either one fully factored row or GCF extraction then factored row; ascending roots; optional false nonzero scalar equation; E=0 and positivity explanation; final roots or product. No stages are simplified away. Nonmathematical prose, paragraphs, blank lines, punctuation, and repeated roots remain exact. Negative product parentheses and exponent order are display flags, independent of wrong choices.

## 4. Reusable templates, domains, and extension bounds

All roles are built from complete mathematical components. No substring replacement or source-answer branch occurs. Each question has one fixed worked solution. Profiles preserve complete banks; any undefined, duplicate, equivalent-to-correct or otherwise ambiguous option rejects the entire instance. Explicit invalid parameters raise rather than silently resample. Radio choices shuffle deterministically; order and seed do not determine identity.

Easy: a=c=1, b=−d, radius 1..12, scalar 1 or 2..3 for the distinct GCF layout. The exponent is a nonconstant linear expression; base e or integer 2..9, |k|≤9 and |h|≤4. Exponent/base variety changes presentation only; positivity supplies no roots and no exponent evaluation is required, so those slots do not inflate mathematical-task counts. Radii 10..12 are an authored extension to familiar integer perfect squares through 144; the assessed difference-of-squares operation remains the same. The default radius-one bank uses ±2u instead of colliding root/product fragments; this is an authored bank variant.

Moderate: c=1, a≤3, |b|,|d|≤9, B≠0, scalar 1 except the designated GCF/scaled layouts (2..3); expanded A≤3, |B|≤30, |C|≤72. Leading layouts require the nonunit factor to be primitive, preserving one noninteger rational root. This contains the observed integer-root and single-rational-root demands. The field layout and GCF stage remain template-specific. Radio defaults compute product, sum instead of product, either single root, and the unscaled constant (when leading coefficient is nonunit); monic defaults instead use the sign-reversed product. These are separately authored whole operation banks, not promoted scalar fits.

Hard (authored missing level): g=1; both a and c in 2..4; primitive factors gcd(a,b)=gcd(c,d)=1; nonzero |b|,|d|≤9; distinct nonzero roots; B≠0; expanded A≤16, |B|≤72, |C|≤81. Two nonunit linear factors give two rational roots after the same common-factor step. This is a bounded strengthening of the observed 2x−1 factor and the prerequisite leading-coefficient factoring topic. It introduces no rearrangement, irrational roots, extra polynomial degree, logarithms, or new functions. Radio and blank layouts remain unordered peers. This difficulty assignment is a design claim rather than a recovered original label.

Fingerprints normalize the polynomial to monic form, include response demand and the presence of nonunit scalar extraction, and exclude scalar value, exponential base/input, bank/profile/order. The finite easy domain contains 12 opposite-root pairs in each of its three observed workload/response layouts, hence 36 substantive tasks; exponential and GCF scalar numerical variation adds no tasks. Content identity additionally covers version, original mathematical parameters, exact displayed prompt/solution, and complete displayed banks. Changed banks therefore change identity; option shuffling does not. No plot extraction/rendering is required (rating none). Steps stop before database preparation.

### Enumerated substantive authored task domains

The validator exhaustively enumerates the bounded integer factor slots, enforces every scope and complete-bank constraint, and deduplicates by unordered exact root pair, response demand, and presence of nonunit scalar extraction. Base, exponent, scalar magnitude, factor order, answer bank, and option order contribute no task counts.

| Template | Eligible distinct tasks |
|---|---:|
| difference_radio | 12 |
| difference_blank | 12 |
| difference_gcf_blank | 12 |
| quadratic_radio | 112 |
| quadratic_blank | 144 |
| quadratic_scaled_radio | 96 |
| quadratic_gcf_blank | 112 |
| leading_radio | 321 |
| leading_blank | 380 |
| hard_leading_radio | 476 |
| hard_leading_blank | 480 |

Deduplicated level totals are easy **36**, moderate **1165**, hard **956**. This is a finite easy skill bank; additional exponential/coefficient display variation is useful for recognition but does not claim extra assessed tasks. Sixty seeded draws per template cover all 12 easy tasks in each of the three easy layouts, and 42–56 distinct tasks in each moderate/hard layout. The counts describe authored defaults; observed replay banks retain their own complete-bank eligibility conditions and do not inflate these totals.
