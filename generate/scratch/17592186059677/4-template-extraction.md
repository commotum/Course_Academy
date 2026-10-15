# Extraction and permitted variation

`extraction.json` contains each complete prompt and worked solution, every answer value and choice ID, source field/key, missing attributes, feedback presence, and separate complete bank profile. `source-cases.json` contains the exact full Pull question records and explicit original parameters. Raw API calls accept only an original source ID and are evidence-only; no repaired or inferred value can become an original key. Separately, five complete source templates expose eligible faithful generated profiles at original scale=1 and whole-function scales1–6.

Define the backbone before choosing values: provide a function (or the already-known first derivative), calculate its first derivative when necessary, differentiate that derivative once, then optionally evaluate the second derivative at the requested point. Render the formal first-stage input as the actual function and the formal second-stage input as the actual first derivative. Formal differentiation inside either stage is **one** derivative; the left label records whether the result is the first or second derivative. Function names, target points, signs and coefficient calculations travel together through prompt, stages and key.

| Authored template | Fixed supplied structure / stages | Variable slots and constraints | Field |
|---|---|---|---|
| quartic | `a x^4 + b x^2 + c`; first and second differentiation | a=2,3,5; b=-7,-4,2; c=-8,-7,3 | radio |
| powers | `a x^6 + b x^5`; first and second differentiation | a,b=1,2,3 | radio |
| cubic_evaluation | `a x^3 + b x^2 + c`; differentiate twice, evaluate | a=2,3,4; b=2,4,5; c=-7,-3,2; t=-2,-1,1,2 | radio |
| known_first | already-known `f'(x)=a x^2+b x+c`; one differentiation gives second derivative | a=-3,-2,2; b=-6,-4,3; c=12,18,24 | blank |
| linear_cubic | `g(x)=a x-(b/3)x^3`; two differentiations | a=4,6,8; b=1,2,3 | blank |
| sqrt_sum | `a sqrt(x)+b x^2+c x`; rewrite radical, differentiate twice | a=4,8,12; b=3,5,7; c=1,2,3; x>0 | radio |
| power_sqrt_evaluation | `g(x)=a x^2 sqrt(x)+b x+c`; fractional power, two derivatives, evaluation | a=4,8,12; b=-3,-2,2; c=3,5,7; t=4,9; x>0 | radio |
| mixed_sqrt_evaluation | `g(x)=a x^3+b x sqrt(x)`; fractional power, two derivatives, evaluation | a=-3,-2,-1; b=4,8,12; t=1,4,9; x>0 | blank |

These are separately authored extensions of observed structures. The blank variants explicitly restore the supplied function/derivative shown by the original worked solutions, because their captured prompts omit that context. The two Easy records without answer fields and the two unrated records without keys/solutions remain raw evidence; missing field contracts are not guessed. Direct trig and quintic-evaluation source records are preserved exactly but do not create extra authored families.

A radio template has one complete authored procedure-error bank. It is selected before evaluating all its options, and the entire instance is rejected if any options coincide or a distractor equals the correct value. There is no offset fallback, pooled recipe selection, or source-literal copying into new banks. `bank_recipes` records each bank's exact implemented derivative mistake. Wrong sign, omitted terms/multipliers, stopping after one derivative, retaining an exponent and using the wrong multiplier produce meaningful alternate computations. Blanks have no distractors or inferred feedback.

Original source banks retain their complete observed mathematical values—including the opaque `24x^2-24` choice in q-10883 and opaque numeric banks. The five served faithful profiles multiply every complete choice value by the same whole-function scalar. Their unknown misconception intentions are not inferred. All 13 records preserve field layouts, omissions, original keys and exact source prose. The 11 existing worked solutions independently check as mathematically correct. A served repair is limited to supplying the missing function context; it does not silently rewrite the source record.

Coefficient, target, and whole-bank collisions are exhaustively checked. Valid zero/one canonical targets remain supported. Native zero/one probes expect acceptance exactly when they equal the correct answer; only actual complete-bank collisions are excluded. No function-name or option-order shuffle inflates capacity. Mathematical fingerprints use the supplied function (or derivative), mathematical family and evaluation point. Different constants in supplied data count as different functions even if their second derivatives coincide; repeated MA IDs with the same data do not count again.


## Served faithful source templates

| Template | Source | Field / bank count | Ordered original rows preserved |
|---|---|---|---:|
| faithful_q10883 | q-10883 | radio / 5 | 8 |
| faithful_q10892 | q-10892 | radio / 5 | 9 |
| faithful_q10902 | q-10902 | radio / 5 | 6 |
| faithful_q28556 | q-28556 | radio / 5 | 11 |
| faithful_q342851 | q-342851 | blank / 1 | 11 |

`faithful.py` extracts a mathematical common-scalar slot from differentiation's linearity. For scale1 it exactly reproduces original prompt layout, all bank values/correct designation, shared solution words, and every ordered mathematical row, apart from canonical math presentation and generated field-owned UUIDs. For scales2–6 it multiplies the supplied function by the scalar, places that scalar **inside every formal derivative operand**, and scales each complete non-operator row and answer. It retains the original intermediate decomposition, number and order of rows, final evaluation stages, and function name. A mathematical readback checks these transformations independently.

These profiles keep the original evaluation point as a deliberately narrower source-bank sampling policy: the original numeric distractor banks do not establish how those errors should vary with a new target. The separately named authored evaluation families already vary points while retaining the same method. Scope does not require fixing the target; source-bank evidence limits this particular mask. All 21 choices in the five supported complete original banks match at original parameters. The remaining eight records have missing keys/solutions, missing answer fields, or missing givens; their 14 captured choices and four truncated blank layouts remain exact raw evidence and are explicitly excluded from served source-fidelity claims.

Explicit source anchors: `generate('moderate', template='faithful_q10883', parameters={'scale':1})` or `generate('moderate', profile='source_faithful', source_id='q-10883', parameters={'scale':1})`. The default sampler/CLI includes these faithful profiles. `profile='authored'` selects only the separately authored extension banks. Mathematical capacity de-duplicates identical supplied functions/targets across faithful and authored profiles; changing a bank does not create another mathematical task.
