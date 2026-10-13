# Template extraction — four stages

Frozen math basis 1356; lineage and complete untouched source are in source.json.

## 1. Describe the sources

All 11 prompts request a scalar surface integral of curl, with supplied positively oriented closed parameterized boundary. Coordinates use t; field uses x,y,z. Excluding the terminal duplicated point does not alter the definite integral endpoints. Moderate polynomial arithmetic is on [0,1), [−1,0) or [−1,1). Hard uses full trigonometric cycles (πt on [−1,1), t on [0,2π)), plus the explicitly observed signed polynomial source. All fields are five-option radios; one historical duplicate and one unrated/missing-ref source are preserved raw. No images occur.

## 2. Generalize the family

Use Stokes to turn the supplied curl flux into circulation, substitute every coordinate into the field, differentiate each coordinate, form the dot product, reduce it, integrate and evaluate both endpoints. This is the reverse of the sibling task that chooses a surface for a supplied line integral. Positive normal orientation is induced by increasing-t boundary traversal, not automatically upward.

## 3. Map every component and whole bank

Each row below maps a source-owned option to an exact parameterized scalar pattern. Historical distractor intent is opaque. All raw banks are evidence-only; multiplying the field by c consistently multiplies each field-dependent stage/value by c. This is not a recovered wrong-operation interpretation. The entire original bank is retained, not mixed or filled from a pool. Full source prose and whole mathematical-component masks are in source-masks.json.

### q-161928

Observed label: {':db/ident': ':question.difficulty/moderate'}; coordinates `('t**2-t', 't-t**3', '2*t**2-2*t')`; field `('y', '0', 'x')`; interval `[0,1)`.

| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |
|---:|---|---|---|---|

| 0 | bf2943fc-f134-53a9-994e-b427709ccf39 | `0` | `c*(0)` | missing ref |

| 0 | e5f799a3-f0e5-55d2-ba9e-bfe3224a4cd1 | `-1` | `c*(-1)` | missing ref |

| 0 | 26fae208-019b-555a-99b1-0bcb29c38820 | `\frac{1}{60}` | `c*(\frac{1}{60})` | missing ref |

| 0 | 51f21ab6-f636-592c-9370-671a399beb99 | `\frac{3}{32}` | `c*(\frac{3}{32})` | missing ref |

| 0 | 602c1799-3e61-52e6-8f53-9f39f1b26950 | `\frac{2}{25}` | `c*(\frac{2}{25})` | missing ref |

| 1 | 77457099-bf92-5a80-b30d-5158400cc17a | `\frac{1}{60}` | `c*(\frac{1}{60})` | correct |

| 1 | 114e3ccc-e21f-52db-b19d-3f3897328e86 | `\frac{2}{25}` | `c*(\frac{2}{25})` | wrong |

| 1 | 57a39c82-1760-5e0d-ab2f-00a266a5b5cf | `0` | `c*(0)` | wrong |

| 1 | 52460aa2-bb42-52a1-ba47-8cd7c05b7e29 | `\frac{3}{32}` | `c*(\frac{3}{32})` | wrong |

| 1 | 0670939e-8e1b-5069-8ab1-36c39e6a1734 | `-1` | `c*(-1)` | wrong |

Source solution: full theorem → coordinates → field substitution → formal/evaluated derivative → dot product expansion/reduction → integral, primitive and endpoints → final scalar. Full original row fragments are in the extracted masks, with exact source replay tested separately from correctness.

### q-162377

Observed label: unrated; coordinates `('sin(pi*t)', 'cos(pi*t)', 'sin(pi*t)')`; field `('x', '0', 'y')`; interval `[-1,1)`.

| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |
|---:|---|---|---|---|

| 0 | 00d95993-6fce-50a6-9da0-c38e0b9621ce | `0` | `c*(0)` | missing ref |

| 0 | 02754b0a-e75b-5997-be48-1296815d866a | `-2π` | `c*(-2π)` | missing ref |

| 0 | 0c0bbee9-caa1-52ab-a326-73150026e797 | `2π` | `c*(2π)` | missing ref |

| 0 | 1e11ae00-c494-5174-8b2a-aa2dab840740 | `π` | `c*(π)` | missing ref |

| 0 | 5b48ccdf-94f7-5b30-b9e9-c2b9d97a02fb | `1` | `c*(1)` | missing ref |

Source solution: absent; raw retains omission

### q-162316

Observed label: {':db/ident': ':question.difficulty/moderate'}; coordinates `('2*t**3-2*t', '3*t**2+3*t', 't**3-t')`; field `('z', '0', 'y')`; interval `[-1,0)`.

| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |
|---:|---|---|---|---|

| 0 | 27840c28-45a9-5916-b4c1-d818db73736e | `\frac{7}{5}` | `c*(\frac{7}{5})` | wrong |

| 0 | 70f20afe-3ba7-5528-8071-2b9eaa046011 | `\frac{1}{5}` | `c*(\frac{1}{5})` | wrong |

| 0 | a723a97b-4d1b-542c-b720-ec65cd2786a5 | `\frac{1}{20}` | `c*(\frac{1}{20})` | correct |

| 0 | ddabc804-5099-5814-b0bc-e09a67f7767a | `7` | `c*(7)` | wrong |

| 0 | e94716b8-3388-57e0-901d-e8160a0aacf0 | `\frac{-5}{103}` | `c*(\frac{-5}{103})` | wrong |

Source solution: full theorem → coordinates → field substitution → formal/evaluated derivative → dot product expansion/reduction → integral, primitive and endpoints → final scalar. Full original row fragments are in the extracted masks, with exact source replay tested separately from correctness.

### q-162324

Observed label: {':db/ident': ':question.difficulty/hard'}; coordinates `('cos(pi*t)', 'sin(pi*t)', 'cos(pi*t)')`; field `('y', '0', 'x')`; interval `[-1,1)`.

| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |
|---:|---|---|---|---|

| 0 | 125e28c0-bbb7-5d93-95b9-69fe92e1f551 | `2\pi ` | `c*(2\pi )` | wrong |

| 0 | 3eefc9e2-c929-54c3-9081-01b14d2b4379 | `2` | `c*(2)` | wrong |

| 0 | 5764f77b-9cd0-5e34-8a78-c0ca6ff9d828 | `-\frac{2}{\pi }` | `c*(-\frac{2}{\pi })` | wrong |

| 0 | d9a7cfdf-beb6-5886-9078-290c6cf747ca | `-\pi ` | `c*(-\pi )` | correct |

| 0 | dad10f5c-6829-52c8-b539-d1d5a5320bea | `-1` | `c*(-1)` | wrong |

Source solution: full theorem → coordinates → field substitution → formal/evaluated derivative → dot product expansion/reduction → integral, primitive and endpoints → final scalar. Full original row fragments are in the extracted masks, with exact source replay tested separately from correctness.

### q-162886

Observed label: {':db/ident': ':question.difficulty/moderate'}; coordinates `('t**2+t', 't**3+t**2', '2*t**2+2*t')`; field `('y', 'z', 'x')`; interval `[-1,0)`.

| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |
|---:|---|---|---|---|

| 0 | 12d80d2d-e154-51fd-a594-5eba0a5e6b8f | `\frac{2}{15}` | `c*(\frac{2}{15})` | wrong |

| 0 | 14b8499c-89bd-5bc3-931b-c40e7ce37aea | `\frac{7}{45}` | `c*(\frac{7}{45})` | wrong |

| 0 | 72b205e0-a52e-5333-be4c-5c18dbe481a1 | `\frac{3}{20}` | `c*(\frac{3}{20})` | wrong |

| 0 | aa3aff6a-8638-5f77-8507-0d3f55b19bbf | `\frac{1}{15}` | `c*(\frac{1}{15})` | wrong |

| 0 | f732e6da-e394-595c-9b7c-3f0005986060 | `\frac{1}{60}` | `c*(\frac{1}{60})` | correct |

Source solution: full theorem → coordinates → field substitution → formal/evaluated derivative → dot product expansion/reduction → integral, primitive and endpoints → final scalar. Full original row fragments are in the extracted masks, with exact source replay tested separately from correctness.

### q-162887

Observed label: {':db/ident': ':question.difficulty/moderate'}; coordinates `('t**3-t', '2*t**2+1', 't**2-1')`; field `('y', '3', 'y*z')`; interval `[-1,1)`.

| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |
|---:|---|---|---|---|

| 0 | 77a49d17-1ccd-5d21-8067-3cc28c01dfc8 | `\frac{5}{6}` | `c*(\frac{5}{6})` | wrong |

| 0 | 9498af25-8e31-5391-9c5d-57b5a039adb3 | `\frac{11}{10}` | `c*(\frac{11}{10})` | wrong |

| 0 | 9af2af40-8464-54ca-9c05-b548baff602f | `\frac{7}{12}` | `c*(\frac{7}{12})` | wrong |

| 0 | b3c29f02-dc00-5dc7-805e-51068b29a448 | `\frac{16}{15}` | `c*(\frac{16}{15})` | correct |

| 0 | e84e4b95-0c02-5828-a503-1bc5e276aa93 | `\frac{9}{8}` | `c*(\frac{9}{8})` | wrong |

Source solution: full theorem → coordinates → field substitution → formal/evaluated derivative → dot product expansion/reduction → integral, primitive and endpoints → final scalar. Full original row fragments are in the extracted masks, with exact source replay tested separately from correctness.

### q-162892

Observed label: {':db/ident': ':question.difficulty/hard'}; coordinates `('cos(pi*t)', 'sin(pi*t)', '2*sin(pi*t)')`; field `('2*y', '-2*x', 'exp(z-2*y)')`; interval `[-1,1)`.

| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |
|---:|---|---|---|---|

| 0 | 1c5b07f3-4813-5a4a-a0e6-a5bf77edd48d | `2\pi ` | `c*(2\pi )` | wrong |

| 0 | 24161e0a-0b08-5db9-9481-589c38c2931e | `-\pi ` | `c*(-\pi )` | wrong |

| 0 | 3927e74a-4b53-5c18-92e5-d51492930769 | `3\pi ` | `c*(3\pi )` | wrong |

| 0 | bc856658-afbb-5fe8-bdf2-8d82839c6b6f | `-4\pi ` | `c*(-4\pi )` | correct |

| 0 | f923d8f6-fbaa-5b3e-a1a9-91366f82223e | `0` | `c*(0)` | wrong |

Source solution: full theorem → coordinates → field substitution → formal/evaluated derivative → dot product expansion/reduction → integral, primitive and endpoints → final scalar. Full original row fragments are in the extracted masks, with exact source replay tested separately from correctness.

### q-162889

Observed label: {':db/ident': ':question.difficulty/hard'}; coordinates `('cos(t)', 'sin(t)', '1')`; field `('z', '3*x', '2*y**2')`; interval `[0,2*pi)`.

| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |
|---:|---|---|---|---|

| 0 | d45117c8-92b5-5e85-be68-59207cfdcaeb | `4\pi ` | `c*(4\pi )` | wrong |

| 0 | 94d1fa98-7766-5aa8-ae09-9d3addbd727b | `\pi ` | `c*(\pi )` | wrong |

| 0 | 6ec03585-7795-522f-a5f2-67e2d22d5768 | `\pi +1` | `c*(\pi +1)` | wrong |

| 0 | ce20f1dc-7964-554d-81c6-eddb4382c3ac | `3\pi ` | `c*(3\pi )` | correct |

| 0 | fae3e8e3-085f-5a58-b783-baab0dfc6066 | `2\pi -1` | `c*(2\pi -1)` | wrong |

Source solution: full theorem → coordinates → field substitution → formal/evaluated derivative → dot product expansion/reduction → integral, primitive and endpoints → final scalar. Full original row fragments are in the extracted masks, with exact source replay tested separately from correctness.

### q-162891

Observed label: {':db/ident': ':question.difficulty/hard'}; coordinates `('cos(t)', 'sin(t)', '1-sin(t)')`; field `('y-z', 'z-x', 'x-y')`; interval `[0,2*pi)`.

| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |
|---:|---|---|---|---|

| 0 | 1f568a2f-7b80-5f85-b384-1c1a684d00a1 | `-8\pi ` | `c*(-8\pi )` | wrong |

| 0 | db5f892d-b188-5614-98ed-59c650396111 | `-2\pi ` | `c*(-2\pi )` | wrong |

| 0 | ceb21bec-4585-5873-bda2-04c6a3caa80b | `-4\pi ` | `c*(-4\pi )` | correct |

| 0 | 37824a70-c1a6-564e-97d8-b4dfb038f620 | `\pi ` | `c*(\pi )` | wrong |

| 0 | ea2d7d23-39ba-56a6-a28d-95d8896f320a | `3\pi ` | `c*(3\pi )` | wrong |

Source solution: full theorem → coordinates → field substitution → formal/evaluated derivative → dot product expansion/reduction → integral, primitive and endpoints → final scalar. Full original row fragments are in the extracted masks, with exact source replay tested separately from correctness.

### q-162999

Observed label: {':db/ident': ':question.difficulty/moderate'}; coordinates `('t**2-t', 't**2-t**3', 't**2-t')`; field `('2*z', '0', '3*y')`; interval `[0,1)`.

| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |
|---:|---|---|---|---|

| 0 | 0a5ee6b0-2be5-5581-a028-5db7075b5455 | `\frac{4}{15}` | `c*(\frac{4}{15})` | wrong |

| 0 | 9ceea66b-fcc6-5f70-83a1-36dc6fc02ef6 | `\frac{2}{5}` | `c*(\frac{2}{5})` | wrong |

| 0 | 9df165e3-93dc-582f-b6c7-50fa8041ebef | `\frac{3}{25}` | `c*(\frac{3}{25})` | wrong |

| 0 | b623ffee-6400-53b3-8d80-728480b3c9fb | `\frac{1}{20}` | `c*(\frac{1}{20})` | correct |

| 0 | f29e0799-e667-5d4c-b0bf-49fdbd64159a | `\frac{1}{15}` | `c*(\frac{1}{15})` | wrong |

Source solution: full theorem → coordinates → field substitution → formal/evaluated derivative → dot product expansion/reduction → integral, primitive and endpoints → final scalar. Full original row fragments are in the extracted masks, with exact source replay tested separately from correctness.

### q-162314

Observed label: {':db/ident': ':question.difficulty/hard'}; coordinates `('2*t**3-2*t', 't+t**2', '-t-t**2')`; field `('y', '0', 'x')`; interval `[-1,0)`.

| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |
|---:|---|---|---|---|

| 0 | 3927b4fa-c581-50e7-9636-601f0c7f2db1 | `-\frac{2}{3}` | `c*(-\frac{2}{3})` | wrong |

| 0 | a2c0ebdd-99e9-5a8d-ba80-6dbf22ca7b81 | `\frac{9}{5}` | `c*(\frac{9}{5})` | wrong |

| 0 | ad732c00-dd52-57e7-a26e-fd44e8ff888d | `-2` | `c*(-2)` | wrong |

| 0 | b206cf8d-5ac9-5e6e-abb0-0881fe9594e2 | `\frac{1}{15}` | `c*(\frac{1}{15})` | correct |

| 0 | e08a22bc-8ede-59c0-a3f4-3fa119eeb7a3 | `0` | `c*(0)` | wrong |

Source solution: full theorem → coordinates → field substitution → formal/evaluated derivative → dot product expansion/reduction → integral, primitive and endpoints → final scalar. Full original row fragments are in the extracted masks, with exact source replay tested separately from correctness.

## 4. Reusable masks and authored variation

Raw fixed scaffold holds every shared source sentence, derivative, coordinate and interval. Complete field/vector/scalar RHS components are the variable slots, not short coordinate or basis-letter replacements. Unit scale removes an ordinary identity factor, so c=1 and changed c pass through the same slot recipe. Symbolic boundary and F(r) integral rows already refer to the parameterized field and are not scaled twice. Numerical integrands/primitives/endpoints are scaled as whole components. Scalar source-bank patterns scale with c and remain opaque/ineligible. The raw public API preserves the unrated source's absent difficulty/solution/correct ref and the legacy field's absent ref. No literal source payload-return or answer lookup branch exists.

Normal source-shaped families vary coordinate multipliers a,b,d and whole-field multiplier c, nonzero signed integers |value|≤3. Moderate bilinear b,d are further bounded by 2. The exponential family enforces d=b, keeping z−2y=0 along the boundary, so the original substitution simplification survives. Easy fixes d=1. All rules apply equally to explicit inputs and sampled ones. These broader same-method coefficients are authored bounds, not observed source-authoring rules.

Easy has no observed source. Its authored horizontal ellipse with field (−cy,cx,0) has two nonzero tangent coordinates and immediate sin²+cos² reduction. Moderate/hard retain observed per-family polynomial or full-turn trigonometric workload; the unrated π-angle, three-coordinate tangent gets an explicit authored hard assignment. No surface-selection, new theorem, non-elementary integration, or within-level progression is added.

Normal solutions share the original theorem and common prose, while their vector notation and additional formal/distributed/component endpoint stages are authored. This difference is disclosed: normal prose/stage layout is not falsely counted as raw-exact source replication. Every field substitution (including yz and exponential cancellation), coordinate derivative including zero, first dot-product distribution, reduced integrand, primitive and individually evaluated endpoints is independently checked from displayed math.

Complete method banks are fixed before parameters:

* Polynomial: correct integral; reversed boundary; integrate F(r)·r (coordinate instead of tangent); integrate sum of field components (omit tangent); integrate F(r′)·r′ (wrong field input). Values are actual results of these displayed-method operations.
* π-angle trig: correct; reverse; assume zero curl; first half interval; omit π chain factor in tangent.
* Unit-angle hard: correct; reverse; assume zero curl; first half interval; omit the 1/2 factor in squared-trigonometric identities. The other linear/cross terms integrate to zero over a full turn, so this final wrong operation doubles the correct scalar.
* Authored easy: correct; reverse; zero; half interval; omit π from the angular endpoint.

No diagnoses are invented in learner-facing output. Each complete five-value bank must be pairwise mathematically unequal. A collision/invalid value rejects the WHOLE instance; no first-valid replacement is allowed. Historical opaque banks do not become defaults. Sampling chooses a family/bank before coefficients and default family coverage is verified.

Content identity includes generator version, displayed difficulty, prompt, fixed worked solution and entire bank; random order/seed cannot change it. The mathematical fingerprint includes the actual parameterized curve, its traversal/interval and field, not profile/bank or spelling. Assessed curve derivatives and field substitutions make these coefficients substantive even when final scalars coincide.

No practice plot exists; plot extraction/specification and Matplotlib/TikZ rendering are consequently unnecessary (rating none). Tutorial diagrams were treated solely as lesson context. No figure or unrelated demand is introduced just to require a plot. Freeze after step 7; no database preparation/registration/transactions are performed.

