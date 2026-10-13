# Template extraction

## 1. Specific sources

Each source graph was inspected individually at native resolution, including canonical e-3663. Exact source field/value/correct-presence details are retained in source.json, source-cases.json, and bank-mapping.json. The following complete choices appear together; q-79188 preserves two separate captured field IDs.

### q-65549

Parameters: {'B': '5', 'D': '3/2', 'k': -2}.

Field 0b4a0441-f374-5ba6-b7d7-22b89426a4ce, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `-2` | `(-1)*(B+kD)` | False |
| `7` | `(7/2)*(B+kD)` | False |
| `8` | `(4)*(B+kD)` | False |
| `-1` | `(-1/2)*(B+kD)` | False |
| `2` | `(1)*(B+kD)` | True |

### q-79188

Parameters: {'B': '3', 'D': '3', 'k': 1}.

Field 2d980f41-06e1-5562-995c-dd718d6a8c7a, key selection, original correct ref ABSENT.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `9` | `(3/2)*(B+kD)` | False |
| `6` | `(1)*(B+kD)` | False |
| `\frac{3}{2}` | `(1/4)*(B+kD)` | False |
| `3` | `(1/2)*(B+kD)` | False |
| `\frac{1}{3}` | `(1/18)*(B+kD)` | False |

Field 1848e56b-8e02-510d-9f75-0f28e4f3c082, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `9` | `(3/2)*(B+kD)` | False |
| `3` | `(1/2)*(B+kD)` | False |
| `6` | `(1)*(B+kD)` | True |
| `\frac{3}{2}` | `(1/4)*(B+kD)` | False |
| `\frac{1}{3}` | `(1/18)*(B+kD)` | False |

### q-117798

Parameters: {'B': '3/2', 'D': '2', 'k': 1}.

Field d6f51877-7815-5bb3-9f0e-484d066099ae, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `4` | `(8/7)*(B+kD)` | False |
| `\frac{11}{2}` | `(11/7)*(B+kD)` | False |
| `\frac{7}{2}` | `(1)*(B+kD)` | True |
| `3` | `(6/7)*(B+kD)` | False |
| `\frac{11}{4}` | `(11/14)*(B+kD)` | False |

### q-117800

Parameters: {'B': '5/2', 'D': '5/4', 'k': 1}.

Field ebfa8d92-cd88-5898-b22c-46f756efc46d, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `\frac{7}{2}` | `(14/15)*(B+kD)` | False |
| `\frac{13}{2}` | `(26/15)*(B+kD)` | False |
| `\frac{13}{4}` | `(13/15)*(B+kD)` | False |
| `\frac{15}{4}` | `(1)*(B+kD)` | True |
| `\frac{11}{4}` | `(11/15)*(B+kD)` | False |

### q-143665

Parameters: {'B': '3/2', 'D': '-5', 'k': 1}.

Field 5721fa62-48d4-5b2c-87d7-f6231add9a93, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `-\frac{3}{2}` | `(3/7)*(B+kD)` | False |
| `\frac{13}{2}` | `(-13/7)*(B+kD)` | False |
| `-\frac{7}{2}` | `(1)*(B+kD)` | True |
| `-\frac{17}{4}` | `(17/14)*(B+kD)` | False |
| `\frac{23}{4}` | `(-23/14)*(B+kD)` | False |

### q-143666

Parameters: {'B': '5/4', 'D': '9/4', 'k': -1}.

Field a9af95c9-9911-57b3-8b64-ba864ef27435, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `\frac{7}{2}` | `(-7/2)*(B+kD)` | False |
| `1` | `(-1)*(B+kD)` | False |
| `\frac{1}{4}` | `(-1/4)*(B+kD)` | False |
| `-1` | `(1)*(B+kD)` | True |
| `-\frac{1}{4}` | `(1/4)*(B+kD)` | False |

### q-143668

Parameters: {'B': '3/5', 'D': '-12/5', 'k': 1}.

Field c8f9e0d5-a165-5d96-b7ec-3b0afc3b50ce, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `\frac{6}{5}` | `(-2/3)*(B+kD)` | False |
| `-\frac{9}{5}` | `(1)*(B+kD)` | True |
| `-\frac{3}{5}` | `(1/3)*(B+kD)` | False |
| `-\frac{6}{5}` | `(2/3)*(B+kD)` | False |
| `3` | `(-5/3)*(B+kD)` | False |

### q-117799

Parameters: {'B': '3/4', 'D': '-3', 'k': 1}.

Field 4b387afd-4a67-578b-8db3-0662089f213d, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `-\frac{5}{2}` | `(10/9)*(B+kD)` | False |
| `\frac{1}{2}` | `(-2/9)*(B+kD)` | False |
| `-\frac{9}{4}` | `(1)*(B+kD)` | True |
| `2` | `(-8/9)*(B+kD)` | False |
| `-1` | `(4/9)*(B+kD)` | False |

### q-141999

Parameters: {'B': '2', 'D': '1', 'k': 2}.

Field 412e6109-4d77-5424-95b6-1257add5ac9c, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `2` | `(1/2)*(B+kD)` | False |
| `4` | `(1)*(B+kD)` | True |
| `0` | `(0)*(B+kD)` | False |
| `-1` | `(-1/4)*(B+kD)` | False |
| `-2` | `(-1/2)*(B+kD)` | False |

### q-142000

Parameters: {'B': '3', 'D': '1', 'k': 1}.

Field 25043d55-6e38-5a47-9ce8-35564e623dc7, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `3` | `(3/4)*(B+kD)` | False |
| `2` | `(1/2)*(B+kD)` | False |
| `1` | `(1/4)*(B+kD)` | False |
| `4` | `(1)*(B+kD)` | True |
| `5` | `(5/4)*(B+kD)` | False |

### q-143669

Parameters: {'B': '4', 'D': '-9/4', 'k': -2}.

Field a33bc7f4-158e-59b4-b555-27008daa9757, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `\frac{5}{2}` | `(5/17)*(B+kD)` | False |
| `-\frac{1}{2}` | `(-1/17)*(B+kD)` | False |
| `\frac{13}{2}` | `(13/17)*(B+kD)` | False |
| `-\frac{7}{2}` | `(-7/17)*(B+kD)` | False |
| `\frac{17}{2}` | `(1)*(B+kD)` | True |

### q-65550

Parameters: {'B': '5/4', 'D': '-3', 'k': -1}.

Field fd0dd138-ee92-58b5-a97c-038d65811dd6, key selection, original correct ref present.

| Exact source value | Parameterized replay recipe | Designated correct |
|---|---|---|
| `-\frac{7}{4}` | `(-7/17)*(B+kD)` | False |
| `-\frac{5}{4}` | `(-5/17)*(B+kD)` | False |
| `\frac{3}{4}` | `(3/17)*(B+kD)` | False |
| `4` | `(16/17)*(B+kD)` | False |
| `\frac{17}{4}` | `(1)*(B+kD)` | True |

## 2. Generalized mathematical pattern

Read the distance T from zero to the first positive vertical asymptote, compute B=pi/T, read the height D of the point at x=T/2, and evaluate the stated B+kD. The final curve equation is included in the fixed worked solution. The native response is the delimiter-free scalar radio value. The positive B convention follows the strictly decreasing A=1 cotangent branch; no sign ambiguity arises.

## 3. Components and complete banks

Every original choice is mapped one-to-one above; no source option is dropped, pooled or assigned a speculative intent. Sparse scalar banks underdetermine their authoring errors. The scaling-ray recipe is an explicit numerical replay pattern, not a recovered distractor misconception: it scales the entire original bank by (B+kD)/(B0+kD0). Correctness follows because the designated original scalar is B0+kD0; source constants are rational ray multipliers, not an answer lookup table. If the requested value is zero, all ray choices collide and the complete instance is rejected. Every observed profile is evidence-only and excluded from defaults.

Normal banks are explicitly authored and contain five eligible method-derived options chosen together before parameter sampling:

- method_sign_period: B+kD; 1/B+kD (confuse stretch and B); B-kD (reverse shift); B/2+kD (double period); 2B+kD (halve period).
- method_midpoint_offset: B+kD; B+k(D+1); B+k(D-1) (read the cotangent quarter-period heights as the midpoint D); B (omit shift); 1/B+kD (use horizontal stretch).
- easy_period: B; 1/B; 2B; B/2; 2/B (stretch/period reciprocal and half/double-period confusions).

All options are computed, exact rational scalars. A collision or incorrect cardinality rejects the whole bank; no pooled first-valid replacement is used. Displayed banks have five choices, shuffled only after the correct identity is recorded. Fixed solution prose never diagnoses an option.

## 4. Reusable masks and bounds

Source solution masks isolate complete math tokens, never short variable strings across prose. Exactly eleven math tokens are retained: T; first period row; T; formal family; formal period formula; reciprocal calculation; D; absolute shift; signed D equation; arithmetic chain; final curve. Fixed prose and blank-line layout remain source-exact. Source-specific period subtraction, inline first row, grouped negative substitution, and omission of redundant rows are retained. Direction/unit prose is conditional on D. All 12 solutions match their complete original strings at replay parameters.

Normal defaults use the common observed displayed-period solution sequence, retaining formal family, formal period, reciprocal substitution, reduced B, signed D, complete arithmetic chain, and final equation. The source formal A,C symbols appear only in the remembered period formula; assessed curves always have A=1,C=0. No phase-shift inference is required.

Reduced B is sampled from n/q, n=1..20, q in {1,2,4,5}, with 1/2<=B<=8; reduced D from n/q, |n|<=25, the same denominator set, 0<|D|<=5. Easy has k=0 and integer D=1..4. Moderate has k in {-2,-1,1,2} and at least one of B,D with reduced denominator <=2. Hard has both denominators in {4,5}. Public explicit calls enforce the exact same catalog bounds. Source replay has separate observed-family bounds to retain source cases; only its original expression is allowed per profile. All bounds preserve familiar source number forms and the same arithmetic method.

Mathematical fingerprints use reduced B, requested k, and (when shift is assessed) reduced D and its tick increment. Easy excludes D, since the requested B is independent of it. Notation, seed, layout, bank aliases and original profile are excluded from task counts; content identity includes version, level, displayed prompt, complete bank, fixed solution and rendered geometry. Two banks for the same mathematical task get distinct content IDs. All outer records are directly serializable local review JSON, with schema-shaped colon keys only inside question/fields/answers.

Source anomaly: canonical e-3663 calls the cotangent function a tangent in one sentence. Raw evidence is retained; authored/normal solutions say cotangent. No practice solution requires a mathematical repair. Native blank grading is inapplicable because no source or authored blank is generated.
