# Template extraction

Database math, basis 1356; lineage preserved in source.json. Four extraction stages follow. Symbols a,b,c / d,e,f / g,h,i always refer to fixed matrix positions. The correct expression D is `a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)`.

## 1. Describe each source specifically

### q-38128

Matrix entries: `[2, 0, 0]; [0, 7, 0]; [0, 0, -3]`. Signed exact integers; 6 zero entries. Template `legacy_radio`, field `selection`, type `:answer-field.type/radio`. Original difficulty: `None`. Determinant independently computed: `-42`.

Find the value of $\begin{vmatrix}2 & 0 & 0 \\ 0 & 7 & 0 \\ 0 & 0 & -3\end{vmatrix}$.

Displayed values in capture order: 14, -42, 21, -14, -21.

Worked solution: absent; generated source-style expansion is authored.

### q-9841

Matrix entries: `[0, -1, 3]; [2, 0, 1]; [7, -1, 0]`. Signed exact integers; 3 zero entries. Template `legacy_radio`, field `selection`, type `:answer-field.type/radio`. Original difficulty: `None`. Determinant independently computed: `-13`.

Find the value of $\begin{vmatrix}0 & -1 & 3 \\ 2 & 0 & 1 \\ 7 & -1 & 0\end{vmatrix}$.

Displayed values in capture order: 32, -13, 47, 0, -15.

Worked solution: absent; generated source-style expansion is authored.

### q-128309

Matrix entries: `[-2, 1, 1]; [1, 4, 0]; [5, -3, 1]`. Signed exact integers; 1 zero entries. Template `aligned_radio`, field `selection`, type `:answer-field.type/radio`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `-32`.

Find the value of $|\begin{aligned}-2 & 1 & 1 \\ 1 & 4 & 0 \\ 5 & -3 & 1\end{aligned}|.$

Displayed values in capture order: 20, -5, 12, 8, -32.

Worked solution: shared top-row alternating cofactor expansion; evaluated minor products, evaluated minors, weighted terms, total; zero terms may collapse.

### q-275585

Matrix entries: `[-5, 3, 0]; [1, 7, 5]; [0, -2, -3]`. Signed exact integers; 2 zero entries. Template `matrix_blank`, field `field-1`, type `:answer-field.type/blank`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `64`.

If $A=[\begin{aligned}-5 & 3 & 0 \\ 1 & 7 & 5 \\ 0 & -2 & -3\end{aligned}],$ then $det(A)=${{field-1}}.

Displayed values in capture order: 64.

Worked solution: shared top-row alternating cofactor expansion; evaluated minor products, evaluated minors, weighted terms, total; zero terms may collapse.

### q-280387

Matrix entries: `[0, 7, 2]; [1, 0, -5]; [4, -3, 0]`. Signed exact integers; 3 zero entries. Template `matrix_blank`, field `field-1`, type `:answer-field.type/blank`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `-146`.

If $H=[\begin{aligned}0 & 7 & 2 \\ 1 & 0 & -5 \\ 4 & -3 & 0\end{aligned}],$ then $det(H)=${{field-1}}.

Displayed values in capture order: -146.

Worked solution: shared top-row alternating cofactor expansion; evaluated minor products, evaluated minors, weighted terms, total; zero terms may collapse.

### q-280390

Matrix entries: `[0, 2, -3]; [0, 0, 5]; [0, 0, 4]`. Signed exact integers; 5 zero entries. Template `matrix_blank`, field `field-1`, type `:answer-field.type/blank`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `0`.

If $A=[\begin{aligned}0 & 2 & -3 \\ 0 & 0 & 5 \\ 0 & 0 & 4\end{aligned}],$ then $det(A)=${{field-1}}.

Displayed values in capture order: 0.

Worked solution: shared top-row alternating cofactor expansion; evaluated minor products, evaluated minors, weighted terms, total; zero terms may collapse.

### q-280393

Matrix entries: `[3, -2, 5]; [4, 1, 0]; [-1, 3, 2]`. Signed exact integers; 1 zero entries. Template `matrix_blank_products`, field `field-1`, type `:answer-field.type/blank`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `87`.

If $Q=[\begin{aligned}3 & -2 & 5 \\ 4 & 1 & 0 \\ -1 & 3 & 2\end{aligned}],$ then $det(Q)=${{field-1}}.

Displayed values in capture order: 87.

Worked solution: shared top-row alternating cofactor expansion; explicit product row, product evaluation, minors, weighted terms, total.

### q-280394

Matrix entries: `[1, -2, 0]; [4, 3, 5]; [6, -1, 2]`. Signed exact integers; 1 zero entries. Template `matrix_blank_products`, field `field-1`, type `:answer-field.type/blank`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `-33`.

If $R=[\begin{aligned}1 & -2 & 0 \\ 4 & 3 & 5 \\ 6 & -1 & 2\end{aligned}],$ then $det(R)=${{field-1}}.

Displayed values in capture order: -33.

Worked solution: shared top-row alternating cofactor expansion; explicit product row, product evaluation, minors, weighted terms, total.

### q-280400

Matrix entries: `[5, -2, 3]; [-1, 4, 6]; [2, -3, 1]`. Signed exact integers; 0 zero entries. Template `matrix_blank_products`, field `field-1`, type `:answer-field.type/blank`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `69`.

If $W=[\begin{aligned}5 & -2 & 3 \\ -1 & 4 & 6 \\ 2 & -3 & 1\end{aligned}],$ then $det(W)=${{field-1}}.

Displayed values in capture order: 69.

Worked solution: shared top-row alternating cofactor expansion; explicit product row, product evaluation, minors, weighted terms, total.

### q-38100

Matrix entries: `[1, -1, 2]; [0, 4, 1]; [0, 0, 8]`. Signed exact integers; 3 zero entries. Template `aligned_radio`, field `selection`, type `:answer-field.type/radio`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `32`.

Find the value of $|\begin{aligned}1 & -1 & 2 \\ 0 & 4 & 1 \\ 0 & 0 & 8\end{aligned}|.$

Displayed values in capture order: 24, -24, 15, 32, 18.

Worked solution: shared top-row alternating cofactor expansion; evaluated minor products, evaluated minors, weighted terms, total; zero terms may collapse.

### q-38124

Matrix entries: `[1, 0, 0]; [4, -1, 0]; [2, -6, -4]`. Signed exact integers; 3 zero entries. Template `aligned_radio`, field `selection`, type `:answer-field.type/radio`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `4`.

Find the value of $|\begin{aligned}1 & 0 & 0 \\ 4 & -1 & 0 \\ 2 & -6 & -4\end{aligned}|.$

Displayed values in capture order: 8, 4, -12, -8, 24.

Worked solution: shared top-row alternating cofactor expansion; evaluated minor products, evaluated minors, weighted terms, total; zero terms may collapse.

### q-38174

Matrix entries: `[-1, 0, 3]; [0, 5, 2]; [1, 0, -4]`. Signed exact integers; 3 zero entries. Template `aligned_radio`, field `selection`, type `:answer-field.type/radio`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `5`.

Find the value of $|\begin{aligned}-1 & 0 & 3 \\ 0 & 5 & 2 \\ 1 & 0 & -4\end{aligned}|.$

Displayed values in capture order: -23, 15, -20, 5, 20.

Worked solution: shared top-row alternating cofactor expansion; evaluated minor products, evaluated minors, weighted terms, total; zero terms may collapse.

### q-38176

Matrix entries: `[6, 0, 7]; [0, 2, 0]; [1, 0, -1]`. Signed exact integers; 4 zero entries. Template `aligned_radio`, field `selection`, type `:answer-field.type/radio`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `-26`.

Find the value of $|\begin{aligned}6 & 0 & 7 \\ 0 & 2 & 0 \\ 1 & 0 & -1\end{aligned}|.$

Displayed values in capture order: -12, -14, -2, -26, 2.

Worked solution: shared top-row alternating cofactor expansion; evaluated minor products, evaluated minors, weighted terms, total; zero terms may collapse.

### q-38180

Matrix entries: `[0, -1, 3]; [1, 0, 2]; [3, -2, 0]`. Signed exact integers; 3 zero entries. Template `aligned_radio`, field `selection`, type `:answer-field.type/radio`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `-12`.

Find the value of $|\begin{aligned}0 & -1 & 3 \\ 1 & 0 & 2 \\ 3 & -2 & 0\end{aligned}|.$

Displayed values in capture order: -12, 0, 6, 12, -6.

Worked solution: shared top-row alternating cofactor expansion; evaluated minor products, evaluated minors, weighted terms, total; zero terms may collapse.

### q-128308

Matrix entries: `[7, 1, -3]; [0, 3, 1]; [-3, 1, 2]`. Signed exact integers; 1 zero entries. Template `aligned_radio`, field `selection`, type `:answer-field.type/radio`. Original difficulty: `:question.difficulty/easy`. Determinant independently computed: `5`.

Find the value of $|\begin{aligned}7 & 1 & -3 \\ 0 & 3 & 1 \\ -3 & 1 & 2\end{aligned}|.$

Displayed values in capture order: 12, 1, -1, 5, -19.

Worked solution: shared top-row alternating cofactor expansion; evaluated minor products, evaluated minors, weighted terms, total; zero terms may collapse.

## 2. Generalize the shared pattern

Given nine explicit integer entries of one 3x3 matrix, compute a numeric determinant using its top row and three 2x2 minors. A radio returns one whole integer; a blank returns only the integer after the supplied determinant notation. The instructional purpose is correct alternating signs and minor multiplication/subtraction. Prompt/field/solution-stage variants are separated above; changed integer values do not form additional templates.

## 3. Components and every original choice

The following tables exhaust all original answers. `correct D` is calculated before the wrong values. A source scalar bank is observed; the polynomial generalization and error interpretation are hypotheses, not evidence of original authoring logic. For each displayed value, the expression is evaluated at its original entries. Complete profile membership is preserved as a unit.

### q-38128 / diagonal

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `98f5e0e0-c541-5d5e-b120-030d10523d76` | `14` | `a*e` | incorrect | exact |
| `b4a5c589-e2fa-52d4-bdc2-98052caa1a12` | `-42` | `correct D` | independently inferred correct | exact |
| `050bb88d-1c57-5dcc-9cba-c9dddc9dd491` | `21` | `-e*i` | incorrect | exact |
| `287927b3-cd33-5f0b-a23f-da8c2dcc0f8b` | `-14` | `-a*e` | incorrect | exact |
| `5a082a8b-804e-590d-a86c-ce9acb67344c` | `-21` | `e*i` | incorrect | exact |

### q-9841 / legacy_zero_diagonal

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `cb7f9378-1e2c-5fad-a64e-dba8350af45e` | `32` | `c*d*g + d**2*f - d*f*g` | incorrect | exact |
| `d0ce2cd2-c328-50a2-a7d8-262686f4f13c` | `-13` | `correct D` | independently inferred correct | exact |
| `f1b413f1-d53c-5d8d-939a-db24e1f1fc46` | `47` | `-d*f**2 + f*g**2` | incorrect | exact |
| `f83be477-467e-53c3-8f41-fa96ec94d220` | `0` | `a*(e*i - f*h)` | incorrect | exact |
| `3d8025f2-5776-57cc-9e01-ba1728d61b90` | `-15` | `c*d*f - c*f*g` | incorrect | exact |

### q-128309 / signed_one_zero

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `1682dd1e-6a3e-585a-b8de-5b23b7ea94c4` | `20` | `e*g` | incorrect | exact |
| `1689a068-b51c-5ee0-8061-d29ddb153fe2` | `-5` | `-g` | incorrect | exact |
| `1d2470ac-dd54-5b59-9478-94b73932f435` | `12` | `-e*h` | incorrect | exact |
| `7d4bbf76-c7a5-5145-83ec-650fb6db1e65` | `8` | `-a*e` | incorrect | exact |
| `de38351b-baf5-5a90-a6e5-ee73c0a46168` | `-32` | `correct D` | observed correct | exact |

### q-275585 / None

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `2c438cd2-2f9a-56e9-ba78-198237723b47` | `64` | `correct D` | observed correct | exact |

### q-280387 / None

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `eb31b60f-3050-5ef7-b4c3-2476ae1e52f6` | `-146` | `correct D` | observed correct | exact |

### q-280390 / None

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `18a27456-d8f3-561b-bb79-e130d6872c6c` | `0` | `correct D` | observed correct | exact |

### q-280393 / None

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `1339ed7b-7b32-5f2e-97a1-9339503ac331` | `87` | `correct D` | observed correct | exact |

### q-280394 / None

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `7756ac8b-4d3e-5612-bad7-e5a160c5a43f` | `-33` | `correct D` | observed correct | exact |

### q-280400 / None

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `199cfd6b-b7c6-5ebd-9bb2-5a78fca81a8a` | `69` | `correct D` | observed correct | exact |

### q-38100 / upper_triangular

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `66ee7868-897f-5ab3-8d7e-e9355eee0531` | `24` | `a*(e*i - f*h) + b*(-f*g + f*i)` | incorrect | exact |
| `6ad500fb-8c54-539b-bf4d-cd40316e5887` | `-24` | `-a*(e*i - f*i)` | incorrect | exact |
| `772ad7c2-6121-5b62-96eb-0eca3dab85ec` | `15` | `a*(e**2 - f**2)` | incorrect | exact |
| `b5556dee-a933-508a-b4bb-1dcfb4c54712` | `32` | `correct D` | observed correct | exact |
| `de02e7bb-d9a4-5bb9-bf6b-5f3af8e67385` | `18` | `c*f**2 + e**2` | incorrect | exact |

### q-38124 / lower_triangular

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `39c95b18-19e1-5456-b91d-959e901cf5fb` | `8` | `2*a*(e*i - f*h)` | incorrect | exact |
| `443dd17c-f660-5dbb-86c7-79e97787046f` | `4` | `correct D` | observed correct | exact |
| `9fe1db1b-04fb-517a-b8fb-6e795c914341` | `-12` | `a*(d*i - f*h) + a*(e*i - f*h)` | incorrect | exact |
| `aa28735a-4d12-597b-bcb9-1a0875584598` | `-8` | `a*(-f*h + g*i)` | incorrect | exact |
| `ecaf6396-e5cd-5350-bf10-b76c299fd393` | `24` | `a*(-f*h + h*i)` | incorrect | exact |

### q-38174 / sparse_two_terms

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `0635b999-97d3-5d18-9b12-3caeac9cc177` | `-23` | `a*(d*i - f*i) + c*(d*h - e*g)` | incorrect | exact |
| `348915a7-95ed-5f25-ae7f-358a86044ca7` | `15` | `-c*(d*h - e*g)` | incorrect | exact |
| `60f0d229-ffe4-53c3-82e2-22709bf924f1` | `-20` | `-a*(e*i - f*h)` | incorrect | exact |
| `7662322d-927c-5fb0-b5dc-73ffb2cfb282` | `5` | `correct D` | observed correct | exact |
| `af6c20f8-fd9a-5e48-9e1e-402c93631c91` | `20` | `a*(e*i - f*h)` | incorrect | exact |

### q-38176 / sparse_second_column

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `205ccffc-01c3-5074-bcb8-cc4b974d5c58` | `-12` | `a*(e*i - f*h)` | incorrect | exact |
| `2bb5b773-84ff-5a8d-8b87-3631203e61e7` | `-14` | `c*(d*h - e*g)` | incorrect | exact |
| `822fd678-004a-5da8-9c3e-6a6e50c794ee` | `-2` | `a*(e*g - f*h) + c*(d*h - e*g)` | incorrect | exact |
| `c67d2e1d-8417-5a78-a35c-8205ba48cf31` | `-26` | `correct D` | observed correct | exact |
| `f4ea0889-e7f0-58ed-8cf7-e8e35863a9f5` | `2` | `a*(e*i - f*h) + c*(d*h + e*g)` | incorrect | exact |

### q-38180 / zero_diagonal

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `11f2d595-4c96-599f-b04a-ef1a4facbf7d` | `-12` | `correct D` | observed correct | exact |
| `35476165-d1db-5ee5-b183-b3201978c25b` | `0` | `a*(e*i - f*h)` | incorrect | exact |
| `36554c2e-a686-5080-983a-7fd2be339db8` | `6` | `b*(d*i - f*g)` | incorrect | exact |
| `5dc9de58-8130-508b-ad5a-dc48cfe4914d` | `12` | `-a*(e*i - f*h) + b*(d*i - f*g) - c*(d*h - e*g)` | incorrect | exact |
| `a45499fc-34c3-5b71-b300-396e74e38e5c` | `-6` | `c*(d*h - e*g)` | incorrect | exact |

### q-128308 / signed_one_zero_b

| Source answer UUID | Complete value | Parameter recipe | Correct designation | Match |
|---|---:|---|---|---|
| `8b194044-2804-5fcf-a8b9-85153f639110` | `12` | `b*(d*i - e*g) + b*(d*i - f*g)` | incorrect | exact |
| `54638e37-8e75-56d4-9a53-7e2c86da678b` | `1` | `a*(e*i - f*i) + c*(d*h - e*g)` | incorrect | exact |
| `c81acd3d-ac95-59d4-82b7-c347ecf84382` | `-1` | `a*(e*i - f*h) + c*(-e*g + e*h)` | incorrect | exact |
| `0c9c5b60-f770-5f9a-ba14-7c25357899e4` | `5` | `correct D` | observed correct | exact |
| `00b39530-0e0b-51c1-a111-9de7ad7bbe3b` | `-19` | `-a*(e*i + f*h) + b*(d*i - f*g) - c*(d*h - e*g)` | incorrect | exact |

## 4. Reusable templates, constraints, and calculations

Fixed components: prompt sentences, answer-field key/type/count, source determinant/matrix notation, shared worked-solution opening, top-row cofactor order (+,-,+), and integer answer fragment. Variable components: all nine numeric entries, uppercase matrix name in blanks, all minors, products, signed sums, determinant, and values from one complete bank. Optional components: an explicit multiplication row for the product template; zero coefficient or minor terms may collapse; zero determinant remains a numeric answer. There are no mathematical branches or alternate solution methods.

Parameter input is a flat nine-integer `matrix`, with optional single uppercase ASCII `name` only for a blank. Booleans and floating values are rejected. Invalid explicit inputs fail without resampling. Random sampling chooses a full profile first; it preserves each observed radio zero mask and samples nonzero values from -7..-1 or 1..8 for easy. Blank easy instances vary over five observed sparse/dense mask shapes. Source replay is not restricted by those sampling bounds. The authored dense moderate/hard policies are documented in classification.

Calculations: derive three minors `(ei-fh, di-fg, dh-eg)`, signed coefficients `(a,-b,c)`, weighted terms, total determinant, then all four selected wrong expressions. If any two option integers agree, or an incorrect value equals the determinant, reject the whole instance. Never patch a bank with another recipe. The authored `cofactor_signs` complete bank reverses the second cofactor sign, reverses the third cofactor sign, uses addition in every minor, and negates D. It is labeled authored and is not used for original-bank replay.

Each fixed instance has one worked solution independent of its distractor values and choice order. Source explanations are preserved as shared prose and calculation structure; signed product notation and omitted zero terms are normalized consistently. Original source text is always retained separately. `q-128309` requires the documented sign correction. The other 12 supplied source solutions have no identified mathematical error. Older two cases have no source solutions.

No plots are needed (steps 5 and 7 assessed as none). Stable question identity hashes the displayed prompt, fixed solution, level, field type and complete displayed bank. Seed/order alone does not change it. Field IDs are owned by the question; answer UUIDs are owned by the field. Mathematical matrix fingerprint excludes bank, response format and letter, so duplicates can be detected across banks.

Validation separately checks all 51 original values / 36 distractors / 9 complete radio banks / 6 blank fragments, 15 exact prompts and field layouts, 13 observed correct refs and two independently inferred refs. Every generated arithmetic row is parsed from rendered LaTeX and independently evaluated; all displayed values, derived minors, stable identities and native accepted/rejected grading are checked. Review distinguishes original captures, parameterized replay, and generated authored variants.


## Default distractor policy

Default radio generation uses the authored `cofactor_signs` bank at every level: its wrong answers represent identifiable cofactor-sign or minor-subtraction errors. Observed scalar-bank generalizations remain available through explicit template/profile selection for fidelity replay; exact values do not establish their original error intent. The legacy radio template is excluded from automatic template selection. Thus uncertain polynomial fits cannot silently supply default learner choices.
