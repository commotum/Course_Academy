# Extracted templates

Evidence is `source.json` at basis 2248. Raw source text, fields, keys, identities, correct designations and complete banks are retained there. Classification accounts for all nine source practice questions. `review.md` places each supported source prompt/solution beside a concrete changed-parameter variant.

Every supported template asks which point must lie on the transformed curve, given one point on the original curve. Keep five math-valued radio choices under `selection`, and two worked methods. Method 1 starts with the base curve, applies the first transformation to the point, then applies the second. Method 2 states the known function value, substitutes the transformed x-coordinate, simplifies using that known value, and states the final point. No assets are required. Function families and transformation operators stay fixed per template; random sampling changes only the named numerical slots.

For the following exact recipes, `A,B` mean `a,b` for symbolic questions and the given numerical coordinates for numeric questions. Listed banks preserve source order only for readability; order does not affect identity. Correct answers are marked C. Each source choice is reproduced exactly as a complete mathematical point at the observed parameters, including the less interpretable choices.

| Profile and source | Observed slots | Ordered complete bank |
|---|---|---|
| quadratic, q-121220 | h=1, k=2; base x²; target (x-h)²+k | (A,B+k+h), (A,B+k), **(A+h,B+k) C**, (A-h,B+k), (A+k,B+h) |
| exponential, q-121383 | h=2, k=3; base 2ˣ; target 2^(x-h)+k | (A-h,B+k), (A-h,B-k), (A-h,kB), **(A+h,B+k) C**, (A+h,B-k) |
| absolute, q-121385 | h=-3, k=-2; base abs(x); target abs(x-h)+k | (A+k,B+h), **(A+h,B+k) C**, (A-h,B+k), (A-h,B-k), (A+h,B-k) |
| horizontal_scale, q-121399 | s=2, k=1; base 3ˣ; target 3^(x/s)+k | (A/s,B-k), (A+s,B+k), (A^((s+1)/s),B+k), **(sA,B+k) C**, (A/s,B+k) |
| numeric_shift, q-26398 | A=1, B=4, h=1, k=1; base f(x); target f(x-h)+k | (A,B+k), (A-h,B+k), (A-h,B-k), **(A+h,B+k) C**, (A+h,B-k) |
| numeric_reflection, q-26594 | A=3, B=1, k=-1; base f(x); target -f(x)+k | **(A,-B+k) C**, (-A,-B+k), (A,B-k), (-A,-B+2k), (A,-B+2k) |

The transformations for wrong choices are the expressions in the table, not vague error labels. Horizontal-scale A^((s+1)/s) is an explicit expression-pattern extension of observed A^(3/2); its psychological error interpretation is unresolved. It remains a distinct complete profile. This distractor may be nonreal for negative A; it does not necessarily describe a point on a real curve. The validator supplies positive real witnesses to disprove it without assuming a branch outside its domain. Source banks already include this expression.

Observed values above are distinguished from conservative sampling bounds: nonzero signed h,k in [-8,8]; horizontal stretch s in {2,3,4,5}; numerical A,B nonzero signed integers in [-10,10] (normal sampling uses [-8,8]). Signed horizontal/vertical translations use the same substitution and workload. Numeric slots avoid zero and resample whenever choices coincide. Both easy and moderate labels are observed labels; no difficulty upgrade is authored. Function base and operation stages stay fixed because changing them could change the instructional method. Zero shifts, different functions, additional transformations, blank fields and hard labels are excluded. `generate` rejects mismatched profile/difficulty combinations and invalid or colliding banks.

The symbolic functions retain real graph domains: quadratic and absolute value accept all real a; exponentials have b>0. The incomplete square-root source additionally needs a>=0. It is not sampled. Numeric f is arbitrary with f(A)=B; distractors at different x are disproved using a free-slope linear function, rather than pretending the base function is known.

The initial q-121220 Method 1 line says +1 while its prompt, later solution, bank and correct answer say +2. Evidence supports +2; only the new solution fixes this typo. Canonical e-13411 ends with “III only” although its list is not numbered; that wording is not reused. Three other source questions have no fields: q-121381, q-121393, q-158540. Their prompts/solutions are retained in source evidence but they cannot provide complete bank replay or inventory. No banks are fabricated for these templates.

Source-bank fidelity is 6/6 complete banks, 24/24 distractors, and every correct designation. Presentation fidelity is reported separately: notation and aligned substitutions are normalized, while the ordered mathematical stages and two-method wording are preserved. Every declared numeric slot has a changed-slot check with other data held fixed, signed boundary tests and sampled coverage. Identity uses template plus mathematical parameters, never seed or option order.
