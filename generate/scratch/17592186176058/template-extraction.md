# Template extraction

## Stage 1: specific original questions

All six prompts, entire solutions, field presence and all thirty original choice fragments are retained in `source.json`, reproduced in `review.md`, and individually linked to normal parameterized recipes by `source-cases.json`. q-136548 supplies tan(a)=-2 and asks tan(-a); its solution states rotational symmetry, the formal oddness identity, then -tan(a), -(-2), 2. The remaining originals are identified by their exact captured database IDs below.

17592186269132 supplies 4/5 and asks the reflected tangent; the final chain stops at -4/5 without an extra redundant row. 17592186275424 supplies 3; its chain similarly stops at -3, and its bank includes -sqrt(3). Unrated 17592186176348 supplies 1/2 and asks tan(-x+12π), with standard `\\tan` spelling and spaced Unicode π; the captured widget confirms five radio options and has no captured key/solution.

Hard 17592186275425 supplies -4, multiplier 1/2, shift +3π and offset 3. Its exact final chain is (1/2)·4+3 →4/2+3 →2+3 →5. Hard 17592186275427 supplies -2, multiplier 3/5, shift -7π and offset 4/5. Its chain is (3/5)·2+4/5 →6/5+4/5 →10/5 →2. Each has one period-removal row, then three oddness RHS stages. Every solution uses one unchanged tangent plot. No option-specific diagnoses are added to learner text.

## Stage 2: shared mathematical pattern

Given a finite exact value v=tan(u), evaluate tan(-u) or a reflected tangent shifted by an integer multiple of π. Oddness maps the output to -v. Moderate removes the integer period first; hard additionally evaluates c(-v)+b. No inverse tangent, angle solving, sum formula, double-angle formula, cotangent, or periodicity-only question is introduced.

## Stage 3: components and complete observed banks

Let v be the supplied reduced rational, n the nonzero integer period shift, c the outer multiplier, b the outer offset and q the reduced denominator of v. Choice mappings below are expression recipes, not source-ID answer lookups. Exact original values alongside each mapping are generated in the bank appendix below. All profiles retain the complete five-element bank, field type/key and correct response shape.

| Profile | Complete ordered expression pattern | Interpretation status |
|---|---|---|
| reciprocal_zero | -v, v, 1/v, 0, -1/v | sign omission, reciprocal confusion, zero: method-related categorical errors |
| numerator_omission | v, 1/v, -v, -1/v, -1/q | final fragment omits numerator; reduced-denominator recipe |
| radical_observed | v, -1/v, -v, 1/v, -sqrt(v) | last scalar's original intent unresolved; expression-pattern replay, evidence-only |
| raw_unrated/output_shift | -v+nπ, v+nπ, -v, 0, v | treating input shift as output shift; raw has no original key; completion infers -v |
| integer_observed | -cv+b, 0, cv+b, -(cv+b), b | sign omission, global negation, omitted tangent; zero categorical error |
| fraction_observed | -cv+b, -(cv+b), π-(cv+b), -1, cv+b | π contamination and -1 underdetermine original intent; evidence-only |
| affine_operations (authored) | -cv+b, cv+b, -cv-b, -v+b, -cv | omit oddness, reverse offset, omit scale, omit offset; both hard families use same method-derived whole bank |

The radical and fractional historical banks reproduce their expression patterns for changed eligible inputs but are not promoted as inferred author intent or default learner generation. Whole-instance collision/nonreal rejection applies to these public profiles too. `integer_observed` is explicitly selectable; normal hard defaults select `affine_operations` because it offers consistently method-related errors in both observed structures.

## Stage 4: reusable Markdown/value masks

Fixed: source shared prose, explanatory graph, oddness identity, answer-field type/key, five choices, and a single fixed solution independent of selected error. Variable: complete tangent values, variable letters a/x/t, complete reflected argument, integer shift, outer multiplier and offset, and all arithmetic components. Negative supplied values conditionally include a separate numerical sign-reversal result; positive direct sources omit that redundant stage. Profile output-shift notation retains the source's spaced Unicode π; reflected hard arguments retain source Unicode function application and `\\pi` spacing.

Hard integer and fractional masks retain individually evaluated numerator rows before integer collection or common-denominator collection, respectively. The numerator is a product of the actual multiplier numerator and actual -v; there is no polynomial fitting or unrelated perturbation. Normal masks match source solutions exactly at their anchor inputs except the missing moderate solution, which is explicitly authored using the common periodicity/oddness prose. Negative bank expressions are grouped/sign-joined to avoid bare `+-` or `--`.

Question identity uses version, actual difficulty, prompt, fixed solution, complete displayed bank and correct fragment; random seed, choice ordering and profile aliases are excluded. Mathematical fingerprints retain assessed level, the presence of period removal, supplied value v, affine coefficients c/b and the hard arithmetic form. They exclude complete banks, variable-letter aliases, integer period n and direct sampler-policy aliases. Every tan(-u+nπ) with integer n reduces to the same reflected function; n remains in the prompt, worked solution, complete displayed bank and content identity. Finite default counts are **92 easy tasks, 92 moderate tasks and 245 hard tasks** (102 integer-affine plus 143 fraction-affine). The 24 nonzero shifts create **2,208 moderate and 5,880 hard presentation variants**, not new mathematical tasks. Current easy sampler domains are disjoint: eight negative integers, eight positive integers and 76 eligible reduced noninteger rationals. Overlap is checked after canonical identity normalization, rather than assumed from API labels. Counts exclude variable letters and bank/profile aliases.

Raw replay of unrated sources omits missing attributes. Its normal completed profile preserves the observed prompt/bank while supplying an inferred correct ref, moderate label and solution. Raw missing-key grading is unavailable; completed matching-bank evidence is graded separately. No source error is silently corrected or discarded.

## Per-option source recipe appendix

All values below are exact captured fragments, assigned one-to-one to their source-owned field; recipe descriptions are in Stage 3 above. No source option is omitted.

### Source 17592186176347 — field `a6737d96-a059-592e-9cfb-df4b5f79acd2`
| Exact source value | Parameterized recipe | Original correct designation |
|---|---|---|
| $2$ | oddness | correct |
| $-2$ | omit_oddness | incorrect |
| $-\frac{1}{2}$ | reciprocal | incorrect |
| $0$ | zero | incorrect |
| $\frac{1}{2}$ | negative_reciprocal | incorrect |

### Source 17592186176348 — field `e5ce442c-7d9b-5249-9270-f975f313b5c8`
| Exact source value | Parameterized recipe | Original correct designation |
|---|---|---|
| $-\frac{1}{2} + 12π$ | shift_output_after_oddness | absent |
| $\frac{1}{2} + 12π$ | shift_output_without_oddness | absent |
| $-\frac{1}{2}$ | oddness | absent |
| $0$ | zero | absent |
| $\frac{1}{2}$ | omit_oddness | absent |

### Source 17592186269132 — field `d4a81cb7-756d-567d-b8be-538028bb5ed2`
| Exact source value | Parameterized recipe | Original correct designation |
|---|---|---|
| $\frac{4}{5}$ | omit_oddness | incorrect |
| $\frac{5}{4}$ | reciprocal | incorrect |
| $-\frac{4}{5}$ | oddness | correct |
| $-\frac{5}{4}$ | negative_reciprocal | incorrect |
| $-\frac{1}{5}$ | omit_numerator | incorrect |

### Source 17592186275424 — field `b4d5e25b-e9dd-5b67-a360-a93e26d946ff`
| Exact source value | Parameterized recipe | Original correct designation |
|---|---|---|
| $3$ | omit_oddness | incorrect |
| $-\frac{1}{3}$ | negative_reciprocal | incorrect |
| $-3$ | oddness | correct |
| $\frac{1}{3}$ | reciprocal | incorrect |
| $-\sqrt{3}$ | opaque_negative_root_value | incorrect |

### Source 17592186275425 — field `5337af0e-e303-5162-b9ed-2cc7c66f30f0`
| Exact source value | Parameterized recipe | Original correct designation |
|---|---|---|
| $5$ | complete | correct |
| $0$ | zero | incorrect |
| $1$ | omit_oddness | incorrect |
| $-1$ | global_negative_without_oddness | incorrect |
| $3$ | omit_tangent_term | incorrect |

### Source 17592186275427 — field `e257a236-bcb1-507a-a11a-a984805bc856`
| Exact source value | Parameterized recipe | Original correct designation |
|---|---|---|
| $2$ | complete | correct |
| $\frac{2}{5}$ | negative_unreflected_affine | incorrect |
| $\pi +\frac{2}{5}$ | opaque_pi_plus_negative_unreflected_affine | incorrect |
| $-1$ | opaque_negative_one | incorrect |
| $-\frac{2}{5}$ | omit_oddness | incorrect |
