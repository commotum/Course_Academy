# Template extraction

## 1. Describe each original

Every complete prompt, solution, field, choice, key and raw omission is in source.json. Original-specific details and choices are enumerated below. E denotes the displayed n^(kx+b), D=n^6-1. The exact wrapper provenance is math, basis2275, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.

### q-31405

Anchor parameters: `{"a": 1, "b": -1, "k": 6, "n": 2}`. Field `selection`, `:answer-field.type/radio`.

Original prompt: What is $\displaystyle \int2^{6x - 1}dx$?

| Source choice identity | Exact value | Parameterized recipe | Original key |

| --- | --- | --- | --- |

| 9abbe1a2-b532-51a1-80f3-e85520454526 | `\frac{2^{6x - 1}}{\ln 2} + C` | `E/ln(n)` | absent |

| b2030311-b93b-5086-ac8a-22c14254a5bd | `\frac{2^{3x - 1}}{6} + C` | `n^(3x-1)/6` | absent |

| f17de8b1-8c36-542e-8869-051ce59fb3e3 | `\frac{2^{6x - 1}}{6} + C` | `E/6` | absent |

| 34308b09-4153-58b1-9482-a404961a3981 | `\frac{2^{6x - 1}}{6\ln 2} + C` | `E/(6 ln(n))` | absent |

| 572cb874-e27a-510f-85d8-8a946c5bb585 | `\frac{2^{3x - 1}}{\ln 2} + C` | `n^(3x-1)/ln(n)` | absent |

### q-31418

Anchor parameters: `{"a": 1, "b": -6, "k": -1, "n": 3}`. Field `selection`, `:answer-field.type/radio`.

Original prompt: What is $\displaystyle \int3^{-x - 6}dx$?

| Source choice identity | Exact value | Parameterized recipe | Original key |

| --- | --- | --- | --- |

| 8a0a1db5-167b-5f70-a564-82d5102adf3a | `\frac{3^{x + 6}}{3} + C` | `n^(x+6)/n` | absent |

| ad1e4e92-d55c-58f4-9e5d-b775f0cbec86 | `-\frac{3^{-x - 6}}{\ln 3} + C` | `-E/ln(n)` | absent |

| fd7ed679-6aae-5266-a8e0-9d47536a6cff | `-\frac{3^{x + 6}}{\ln 3} + C` | `-n^(x+6)/ln(n)` | absent |

| 035814d6-6224-5943-996a-04fa0cc9de74 | `-\frac{3^{-x}}{\ln 3} + C` | `-n^(-x)/ln(n)` | absent |

| 3dd1679a-328d-52a1-8d02-f2939bb088b4 | `\frac{3^{-x - 6}}{\ln 3} + C` | `E/ln(n)` | absent |

### q-31412

Anchor parameters: `{"a": 1, "b": 0, "k": -1, "n": 5}`. Field `selection`, `:answer-field.type/radio`.

Original prompt: $\int {5}^{-x}\,\text{d}x=$

| Source choice identity | Exact value | Parameterized recipe | Original key |

| --- | --- | --- | --- |

| 2e3c76b3-9a7e-5c31-b43e-02f9be81294d | `-\frac{{5}^{-x}}{\operatorname{ln}⁡5}+C` | `-E/ln(n)` | yes |

| 4ee811f8-8af9-53fa-be26-778f4f77cd67 | `-{5}^{-x}+C` | `-E` | no |

| 57a67b0f-0c05-5b5a-b5ea-792d6c56a440 | `\frac{{5}^{x}}{\operatorname{ln}⁡5}+C` | `n^x/ln(n)` | no |

| 5de84312-4ff6-5203-8c07-5a2dbc5c4c3e | `\frac{{5}^{-x}}{\operatorname{ln}⁡5}+C` | `E/ln(n)` | no |

| c521dc80-7e50-540f-93b7-e321d21cdb8a | `-\frac{{5}^{x}}{\operatorname{ln}⁡5}+C` | `-n^x/ln(n)` | no |

### q-31413

Anchor parameters: `{"a": 1, "b": 0, "k": 5, "n": 4}`. Field `selection`, `:answer-field.type/radio`.

Original prompt: $\int {4}^{5x}\,\text{d}x=$

| Source choice identity | Exact value | Parameterized recipe | Original key |

| --- | --- | --- | --- |

| 0233f9ce-2764-5d65-ab16-8209abe9223a | `\frac{{4}^{5x}}{5\operatorname{ln}⁡4}+C` | `E/(5 ln(n))` | yes |

| 12f09c2c-e425-5277-8d43-cc46fdd169bc | `\frac{{4}^{5x}}{5}+C` | `E/5` | no |

| 3076245a-c830-5476-aa4e-faa07b490fd8 | `\frac{{4}^{5x}}{\operatorname{ln}⁡4}+C` | `E/ln(n)` | no |

| 60697ea3-02a7-5388-b168-e038e029d1f8 | `-\frac{{4}^{5x-7}}{5\operatorname{ln}⁡4}+C` | `-n^(5x-7)/(5 ln(n))` | no |

| e998d14b-9dc3-5546-a7f6-0253d13262c0 | `\frac{{4}^{x}}{\operatorname{ln}⁡4}+C` | `n^x/ln(n)` | no |

### q-31417

Anchor parameters: `{"a": 1, "b": 0, "k": "1/3", "n": 6}`. Field `selection`, `:answer-field.type/radio`.

Original prompt: $\int {6}^{x/3}\,\text{d}x=$

| Source choice identity | Exact value | Parameterized recipe | Original key |

| --- | --- | --- | --- |

| 1277c0e2-5004-5ee3-b7fe-7022e68c6a19 | `\frac{{6}^{x}}{3\operatorname{ln}⁡6}+C` | `n^x/(3 ln(n))` | no |

| 7cdefd48-2695-5a38-8f5d-ed070355571e | `\frac{{6}^{x/3}}{3\operatorname{ln}⁡6}+C` | `E/(3 ln(n))` | no |

| cd384b9e-3f21-5c93-8eef-f209d288044d | `\frac{3\cdot {6}^{x/3}}{\operatorname{ln}⁡6}+C` | `3E/ln(n)` | yes |

| d8ca43b4-033c-5cd0-a8a6-8ea7eb292ebc | `\frac{3\cdot {6}^{x}}{\operatorname{ln}⁡3}+C` | `3 n^x/ln(3)` | no |

| e19fa8a4-2ede-5cc9-a74c-dbb6cdba1380 | `\frac{{6}^{x/3}}{\operatorname{ln}⁡3}+C` | `E/ln(3)` | no |

### q-30973

Anchor parameters: `{"H": 1, "L": 0, "a": 1, "b": 0, "k": 6, "n": 3}`. Field `selection`, `:answer-field.type/radio`.

Original prompt: Evaluate the integral ${\int }_{0}^{1}{3}^{6x}\,\text{d}x.$

| Source choice identity | Exact value | Parameterized recipe | Original key |

| --- | --- | --- | --- |

| 02b95ba0-8776-5e87-8a07-fb4dd6e251e3 | `\frac{728}{\operatorname{ln}⁡3}` | `D/ln(n)` | no |

| 36229afc-ab9a-5470-be3f-a37b681ee81b | `\frac{364}{3}` | `D/6 (fixed captured scalar pattern)` | no |

| 43ef6c71-98a2-5c12-8945-04c4d08e3cc6 | `\frac{364}{\operatorname{ln}⁡3}` | `D/(2 ln(n))` | no |

| 72e3fae5-ccad-59b0-8fc0-ac0e46bfbfb5 | `\frac{364}{3\operatorname{ln}⁡3}` | `D/(6 ln(n))` | yes |

| 8fc47e71-ee79-5542-acba-c30ea159db79 | `\frac{121}{\operatorname{ln}⁡3}` | `(n^5-1)/(2 ln(n))` | no |

### q-349625

Anchor parameters: `{"H": 2, "L": 1, "a": 1, "b": 7, "k": -2, "n": 3}`. Field `field-1`, `:answer-field.type/blank`.

Original prompt: Evaluate the following integral. Do not round the answer.

${\int }_{1}^{2}{3}^{7-2x}\,\text{d}x=$  
{{field-1}}

| Source choice identity | Exact value | Parameterized recipe | Original key |

| --- | --- | --- | --- |

| f9887105-989f-5006-a00d-02997b258f61 | `\frac{108}{\operatorname{ln}3}` | `a*(n^(kH+b)-n^(kL+b))/(k ln(n))` | yes |

### q-349626

Anchor parameters: `{"H": 3, "L": 1, "a": 3, "b": 5, "k": -1, "n": 2}`. Field `field-1`, `:answer-field.type/blank`.

Original prompt: Evaluate the following integral. Do not round the answer.

${\int }_{1}^{3}3\cdot {2}^{5-x}\,\text{d}x=$  
{{field-1}}

| Source choice identity | Exact value | Parameterized recipe | Original key |

| --- | --- | --- | --- |

| cabb7ef7-a5b4-56a3-899b-b57c3c0202b7 | `\frac{36}{\operatorname{ln}2}` | `a*(n^(kH+b)-n^(kL+b))/(k ln(n))` | yes |

### q-349631

Anchor parameters: `{"H": 1, "L": 0, "a": 2, "b": 1, "k": -1, "n": 4}`. Field `field-1`, `:answer-field.type/blank`.

Original prompt: Evaluate the following integral. Do not round the answer.

${\int }_{0}^{1}2\cdot {4}^{1-x}\,\text{d}x=$  
{{field-1}}

| Source choice identity | Exact value | Parameterized recipe | Original key |

| --- | --- | --- | --- |

| c1e0d6d6-2adc-5995-80ee-179a5a470810 | `\frac{6}{\operatorname{ln}4}` | `a*(n^(kH+b)-n^(kL+b))/(k ln(n))` | yes |

### q-349646

Anchor parameters: `{"H": 2, "L": 0, "a": 1, "b": -1, "k": 1, "n": 5}`. Field `field-1`, `:answer-field.type/blank`.

Original prompt: Evaluate the following integral. Do not round the answer.

${\int }_{0}^{2}{5}^{x-1}\,\text{d}x=$  
{{field-1}}

| Source choice identity | Exact value | Parameterized recipe | Original key |

| --- | --- | --- | --- |

| 723152d6-ad7a-5796-b242-18a007f91b9b | `\frac{24}{5\operatorname{ln}5}` | `a*(n^(kH+b)-n^(kL+b))/(k ln(n))` | yes |

### q-349648

Anchor parameters: `{"H": 1, "L": -1, "a": 1, "b": 1, "k": 1, "n": 3}`. Field `field-1`, `:answer-field.type/blank`.

Original prompt: Evaluate the following integral. Do not round the answer.

${\int }_{-1}^{1}{3}^{x+1}\,\text{d}x=$  
{{field-1}}

| Source choice identity | Exact value | Parameterized recipe | Original key |

| --- | --- | --- | --- |

| fd67e3a7-28e0-5d80-ab9d-4eee46bad316 | `\frac{8}{\operatorname{ln}3}` | `a*(n^(kH+b)-n^(kL+b))/(k ln(n))` | yes |

## 2. Shared mathematical pattern

Integrate a positive integer base raised to an affine exponent, after the one substitution u=kx+b. The response is the complete primitive including arbitrary C for indefinite integrals, or the complete scalar for definite integrals. The primitive is a*n^(kx+b)/(k ln(n)). No logarithmic integration, integration by parts, nonlinear inner function, inverse substitution, or additional technique is introduced.

## 3. Components and interpretation limits

masks.json specifies every whole-expression/number slot and the exact common prose and ordered formal operators. Original numeric fields stay fixed in base-only source masks except every displayed base, evaluated endpoint power and dependent scalar; this is a declared conservative source generalization. Source choices remain together as complete observed banks. The q-31413 -7 shift and q-30973 scalar 364/3 have unresolved historical distractor intent; the replay prototype retains those algebraic expression patterns rather than inventing an intent or arbitrary fitted recipe. Other recipe interpretations can be suggestive, but exact reproduction alone does not prove how an author obtained a wrong choice. All raw banks are explicit ineligible evidence.

Normal method banks are authored: indefinite banks omit ln(n), omit reciprocal slope, reverse a sign, or use the opposite exponent/input exponent. Negative-unit and reciprocal-slope complete profiles are specialized before parameters to avoid genuine degeneracy. Definite radio banks use correct F, omit 1/k (kF), omit ln(n) (ln(n)F), reverse limits (-F), and add endpoint powers rather than subtract them. Every full bank is computed, independently differentiated/evaluated, pairwise compared modulo arbitrary constant for primitives, and rejected whole on collision. No first-valid replacement pool exists.

## 4. Stable backbone and slots

Raw source masks vary n over built-in integers2..9, with all fixed slopes/shifts/scales/limits recorded in source-cases.json. Endpoint arithmetic is capped at max(n^abs(endpoint exponent))<=4096. No base is excluded to accommodate the grader. Raw anchors preserve source notation exactly, including omission of a redundant scale-extraction row for the two unit-positive definite profiles. Normal source profiles retain those exact stage sequences after shared normalization; only the exact-answer wording and authored bank change. Incomplete originals receive separate canonical four-stage completions.

Expanded affine easy varies n2..6, k in {-3,-2,2,3}, b in -3..3 with a=1: one substitution/derivative/differential, integral substitution, extracted factor, primitive, back-substitution. Moderate and hard use n2..6, nonzero integer |k|<=3, b in -3..3, a1..3, L in {0,1}, H in {1,2,3}, L<H. Endpoint exponents lie in -2..6 and power arithmetic stays <=4096. Moderate has a=1 or |k|=1; hard has a2..3, |k|2..3, b nonzero. Thus authored moderate and hard cannot share the same assessed object. Each explicit call and sampler enforces these rules. Expanded definite solutions keep separate substituted integral, extracted scale, primitive-at-limits, endpoint powers, individually evaluated endpoint powers, and final collected value.

The finite declared domain is exhaustively read back from the actual displayed strings in validate.py. Mathematical fingerprints canonicalize the actual exponential rate in prime-log form and the exact zero-input coefficient (including outside-factor/exponent aliases) and include definite bounds, excluding notation/profiles/banks. Content identity includes version, normalized full prompt, fixed full solution, complete bank, field/attribute contract, actual difficulty and correct value, and is invariant under seed/choice ordering. Batch output deduplicates mathematical tasks, not UUIDs.

No plots occur, so no generated images or plot sampler are needed.

Prime-base regressions equate the moderate tasks 4^(x+1) and 2^(2x+2) on the same bounds, as well as reciprocal-slope identities 8^(x/3)=2^x and 4^(-x/2)=2^(-x). Their content identities remain distinct when their displayed expressions differ.
