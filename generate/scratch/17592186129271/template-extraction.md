# Template extraction

## Stage 1 — specific source descriptions

### q-39666 — sparse_trig (easy)
Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}4v \\ 3{u}^{2}+2\operatorname{cos}⁡(vw) \\ vw\end{aligned}].
$$

Field `785a8a4c-9863-5dc4-b03a-b4c3232d979e`, key selection, radio/math, five choices; correct `-24uv`. Original parameters `{"a": 4, "b": 3, "c": 2, "d": 1}`. Signed integer coefficients, fixed polynomial degrees and operator arguments, formal independent inputs u,v,w; constants held fixed. Column-vector prompts identify components explicitly in the solution; equation prompts omit that redundant identification stage.

Ordered solution: formal transformation; formal 3×3 derivative determinant; component identification; nine partial derivatives; substituted 3×3 matrix; chosen-cofactor minor(s); evaluated minor products; final collected/factored determinant.

### q-161793 — sparse_exp (easy)
Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u{e}^{w} \\ w-u \\ w{e}^{u}-3v\end{aligned}].
$$

Field `d23defb7-252c-5ea7-b5af-33ad4ec74ab1`, key selection, radio/math, five choices; correct `3{e}^{w}(1+u)`. Original parameters `{"a": 1, "b": 1, "c": 1, "d": 3}`. Signed integer coefficients, fixed polynomial degrees and operator arguments, formal independent inputs u,v,w; constants held fixed. Column-vector prompts identify components explicitly in the solution; equation prompts omit that redundant identification stage.

Ordered solution: formal transformation; formal 3×3 derivative determinant; component identification; nine partial derivatives; substituted 3×3 matrix; chosen-cofactor minor(s); evaluated minor products; final collected/factored determinant.

### q-161794 — sparse_square (easy)
Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{u}^{2}+{v}^{2} \\ u+3w \\ -v\end{aligned}].
$$

Field `ea688683-0e2b-5e81-8438-0d34494b3330`, key selection, radio/math, five choices; correct `6u`. Original parameters `{"a": 1, "b": 1, "c": 1, "d": 3, "e": 1}`. Signed integer coefficients, fixed polynomial degrees and operator arguments, formal independent inputs u,v,w; constants held fixed. Column-vector prompts identify components explicitly in the solution; equation prompts omit that redundant identification stage.

Ordered solution: formal transformation; formal 3×3 derivative determinant; component identification; nine partial derivatives; substituted 3×3 matrix; chosen-cofactor minor(s); evaluated minor products; final collected/factored determinant.

### q-161796 — log_product (easy)
Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\operatorname{ln}⁡(u\,v\,w) \\ u+2w \\ uv\end{aligned}].
$$

Field `65c51ca4-49aa-5089-b98e-4e0fed70679a`, key selection, radio/math, five choices; correct `\frac{u}{w}`. Original parameters `{"a": 1, "b": 1, "c": 2, "d": 1}`. Signed integer coefficients, fixed polynomial degrees and operator arguments, formal independent inputs u,v,w; constants held fixed. Column-vector prompts identify components explicitly in the solution; equation prompts omit that redundant identification stage.

Ordered solution: formal transformation; formal 3×3 derivative determinant; component identification; nine partial derivatives; substituted 3×3 matrix; chosen-cofactor minor(s); evaluated minor products; final collected/factored determinant.

### q-39299 — rotation (moderate)
Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=u\operatorname{cos}⁡\theta +v\operatorname{sin}⁡\theta ,\,y=v\operatorname{cos}⁡\theta -u\operatorname{sin}⁡\theta ,\,z=w.
$$

You may assume that $\theta $ is a fixed constant.

Field `60477555-dd44-54e5-9698-cd175b7154c1`, key selection, radio/math, five choices; correct `1`. Original parameters `{"a": 1, "b": 1, "c": 1}`. Signed integer coefficients, fixed polynomial degrees and operator arguments, formal independent inputs u,v,w; constants held fixed. Column-vector prompts identify components explicitly in the solution; equation prompts omit that redundant identification stage.

Ordered solution: formal transformation; formal 3×3 derivative determinant; nine partial derivatives; substituted 3×3 matrix; chosen-cofactor minor(s); evaluated minor products; final collected/factored determinant.

### q-161792 — polynomial_column (moderate)
Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=u{v}^{2}+w,\,y={u}^{3}+v,\,z=uv.
$$

Field `095a93fc-962d-5e7a-8222-89b127de9857`, key selection, radio/math, five choices; correct `3{u}^{3}-v`. Original parameters `{"a": 1, "b": 1, "c": 1, "d": 1, "e": 1}`. Signed integer coefficients, fixed polynomial degrees and operator arguments, formal independent inputs u,v,w; constants held fixed. Column-vector prompts identify components explicitly in the solution; equation prompts omit that redundant identification stage.

Ordered solution: formal transformation; formal 3×3 derivative determinant; nine partial derivatives; substituted 3×3 matrix; chosen-cofactor minor(s); final expanded polynomial.

### q-39710 — polynomial_mixed (moderate)
Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x={u}^{2}+vw,\,y=2-uv,\,z={v}^{2}-w.
$$

Field `bc7e9e1f-8201-5457-9ae8-866cb0a50e5b`, key selection, radio/math, five choices; correct `2{u}^{2}-2{v}^{3}-vw`. Original parameters `{"a": 1, "b": 1, "c": 1, "d": 1, "k": 2}`. Signed integer coefficients, fixed polynomial degrees and operator arguments, formal independent inputs u,v,w; constants held fixed. Column-vector prompts identify components explicitly in the solution; equation prompts omit that redundant identification stage.

Ordered solution: formal transformation; formal 3×3 derivative determinant; nine partial derivatives; substituted 3×3 matrix; chosen-cofactor minor(s); evaluated minor products; final collected/factored determinant.

### q-39294 — linear_offdiag (moderate)
Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=v+w,\,y=u+w,\,z=u+v.
$$

Field `2d447ea2-8560-5077-b8b9-f3304d7a91d8`, key selection, radio/math, five choices; correct `2`. Original parameters `{"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1}`. Signed integer coefficients, fixed polynomial degrees and operator arguments, formal independent inputs u,v,w; constants held fixed. Column-vector prompts identify components explicitly in the solution; equation prompts omit that redundant identification stage.

Ordered solution: formal transformation; formal 3×3 derivative determinant; nine partial derivatives; substituted 3×3 matrix; chosen-cofactor minor(s); evaluated minor products; final collected/factored determinant.

### q-39664 — symbolic_diagonal (moderate)
Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=au,\,y=bv,\,z=cw.
$$

You may assume that $a$, $b$ and $c$ are fixed constants.

Field `3708f8e2-7d98-51bd-8b21-20ee27c9855a`, key selection, radio/math, five choices; correct `abc`. Original parameters `{"a": 1, "b": 1, "c": 1}`. Signed integer coefficients, fixed polynomial degrees and operator arguments, formal independent inputs u,v,w; constants held fixed. Column-vector prompts identify components explicitly in the solution; equation prompts omit that redundant identification stage.

Ordered solution: formal transformation; formal 3×3 derivative determinant; nine partial derivatives; substituted 3×3 matrix; chosen-cofactor minor(s); evaluated minor products; final collected/factored determinant.

## Stage 2 — generalized shared pattern

Given three direct component functions, differentiate each while holding the other two inputs fixed, place the nine partials in output-row/input-column order, expand the chosen sparse row/column, and return its signed determinant. Operator and sparsity families remain separate because their mathematical stages differ. Five math choices share one fixed worked solution independent of error selection.

## Stage 3 — complete component/choice maps

Uppercase A,B,C,D,E,F and K below are generator coefficients. Lowercase a,b,c in the diagonal family are the displayed fixed symbolic constants. Every row is a complete expression-pattern recipe, not a fitted numeric answer. “Opaque” means that causal intent is unresolved even though replay is exact. Raw choices and UUIDs remain in source.json.

### sparse_trig-observed
Prompt component slots: $x=A v,\quad y=B u^{2} + C \cos{\left(v w \right)},\quad z=D v w$.

| Source choice UUID | Complete original value | Parameterized expression recipe | Designation | Interpretation |
|---|---|---|---|---|
| 01c262fc-9bb7-50e9-9bd9-71220d222eee | $12uv$ | $A B u v$ | wrong | opaque expression pattern |
| 1f7284f1-bddd-57c4-bee7-4e81f853fddb | $-2vw\operatorname{cos}⁡(vw)$ | $- C v w \cos{\left(v w \right)}$ | wrong | opaque expression pattern |
| 45d58fec-b6fd-54bf-819d-1320f8bbad5b | $4vw$ | $A v w$ | wrong | opaque expression pattern |
| 5a92451e-4ced-5c86-9ad8-ed111fb7bb27 | $4vw\operatorname{cos}⁡(vw)$ | $A v w \cos{\left(v w \right)}$ | wrong | opaque expression pattern |
| b55d6eaa-09cc-570c-89c0-c7bfca63934e | $-24uv$ | $- 2 A B D u v$ | correct | direct determinant |

Bank: five expressions together, selected before sampling; reject the entire instance on an equivalent or correct wrong expression. All five original values match their parameter recipes at the exact captured parameters. No extra/missing source choices.

### sparse_exp-observed
Prompt component slots: $x=A u e^{w},\quad y=- B u + C w,\quad z=- D v + w e^{u}$.

| Source choice UUID | Complete original value | Parameterized expression recipe | Designation | Interpretation |
|---|---|---|---|---|
| 39a3a5e9-764a-5e8b-8b50-93add8b3fc05 | ${e}^{w}$ | $A e^{w}$ | wrong | opaque expression pattern |
| 723714f3-b594-566d-a56e-12b3c635b92e | $3{e}^{w}(1+u)$ | $A B D u e^{w} + A C D e^{w}$ | correct | direct determinant |
| 790dd6b1-fb1b-55ce-8d23-99d906744d93 | $-uw{e}^{u+w}$ | $- A u w e^{u + w}$ | wrong | opaque expression pattern |
| b3690af9-7cf0-5336-b7d4-e7c30102fb21 | ${e}^{u+v}-3{e}^{w}$ | $- D e^{w} + e^{u + v}$ | wrong | opaque expression pattern |
| f77275e3-e3d3-5b1d-ad31-9113451a2bec | $3w{e}^{u+v}$ | $D w e^{u + v}$ | wrong | opaque expression pattern |

Bank: five expressions together, selected before sampling; reject the entire instance on an equivalent or correct wrong expression. All five original values match their parameter recipes at the exact captured parameters. No extra/missing source choices.

### sparse_square-observed
Prompt component slots: $x=A u^{2} + B v^{2},\quad y=C u + D w,\quad z=- E v$.

| Source choice UUID | Complete original value | Parameterized expression recipe | Designation | Interpretation |
|---|---|---|---|---|
| 07db5547-d099-5a39-ad82-abc875d51fab | $2(u-v)$ | $2 A u - 2 B v$ | wrong | opaque expression pattern |
| 273f9725-21b0-51ad-aa3e-3681dbe69685 | $-2u$ | $- 2 A u$ | wrong | opaque expression pattern |
| 5643486d-15ec-545d-a303-f0e9cc3db1be | $6u$ | $2 A D E u$ | correct | direct determinant |
| 5a7bc25d-f032-5290-9eff-ce5cbada276f | $6u-2v$ | $2 A D E u - 2 B v$ | wrong | opaque expression pattern |
| 848acec7-1e41-5ca9-b95e-cefaaa4e11e1 | $0$ | $0$ | wrong | opaque expression pattern |

Bank: five expressions together, selected before sampling; reject the entire instance on an equivalent or correct wrong expression. All five original values match their parameter recipes at the exact captured parameters. No extra/missing source choices.

### log_product-observed
Prompt component slots: $x=A \ln{\left(u v w \right)},\quad y=B u + C w,\quad z=D u v$.

| Source choice UUID | Complete original value | Parameterized expression recipe | Designation | Interpretation |
|---|---|---|---|---|
| 555199b9-aced-5dd0-a7a4-1c3b529e0ad8 | $\frac{1}{w}$ | $\frac{A}{w}$ | wrong | opaque expression pattern |
| 71d28527-0b0f-581a-b145-41b591816c80 | $-\frac{uv}{w}$ | $- \frac{A B D u v}{w}$ | wrong | opaque expression pattern |
| 9bf35eb4-7d06-504d-97d6-6d62c0d12660 | $0$ | $0$ | wrong | opaque expression pattern |
| 9e2827ef-81bc-5319-a0af-3f83476042b9 | $\frac{u}{w}-\frac{1}{v}$ | $\frac{A B D u}{w} - \frac{A}{v}$ | wrong | opaque expression pattern |
| f447c433-d789-5722-828c-42983f30e64f | $\frac{u}{w}$ | $\frac{A B D u}{w}$ | correct | direct determinant |

Bank: five expressions together, selected before sampling; reject the entire instance on an equivalent or correct wrong expression. All five original values match their parameter recipes at the exact captured parameters. No extra/missing source choices.

### rotation-observed
Prompt component slots: $x=A \left(u \cos{\left(\theta \right)} + v \sin{\left(\theta \right)}\right),\quad y=B \left(- u \sin{\left(\theta \right)} + v \cos{\left(\theta \right)}\right),\quad z=C w$.

| Source choice UUID | Complete original value | Parameterized expression recipe | Designation | Interpretation |
|---|---|---|---|---|
| 02ec0914-5828-5c4a-81c9-ce52c1488ee6 | $\operatorname{cos}⁡\theta $ | $A B C \cos{\left(\theta \right)}$ | wrong | method-related expression |
| 350992e5-036c-535c-8a4b-6a5ab4c6fa16 | $\operatorname{sin}⁡\theta $ | $A B C \sin{\left(\theta \right)}$ | wrong | method-related expression |
| 81e74165-da06-5f93-ae92-aeef9db19857 | $0$ | $0$ | wrong | method-related expression |
| a528987d-54c7-5615-ae6d-cbc6a9db0c60 | $1$ | $A B C$ | correct | direct determinant |
| efd74025-7232-59ef-bfa0-45a2a9dfad28 | $\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta $ | $A B C \sin{\left(\theta \right)} \cos{\left(\theta \right)}$ | wrong | method-related expression |

Bank: five expressions together, selected before sampling; reject the entire instance on an equivalent or correct wrong expression. All five original values match their parameter recipes at the exact captured parameters. No extra/missing source choices.

### polynomial_column-observed
Prompt component slots: $x=A u v^{2} + B w,\quad y=C u^{3} + D v,\quad z=E u v$.

| Source choice UUID | Complete original value | Parameterized expression recipe | Designation | Interpretation |
|---|---|---|---|---|
| 46d3639c-107c-558c-b1c4-6ddd7cb81df1 | $6{u}^{3}v-{v}^{2}$ | $6 A C u^{3} v - A D v^{2}$ | wrong | opaque expression pattern |
| 58a20343-ced5-57fc-b813-e98d7f250092 | $v(3{u}^{2}+2)$ | $v \left(2 A + 3 C u^{2}\right)$ | wrong | opaque expression pattern |
| 59f8ccb9-adf9-523b-b70b-b84e01b6cdc1 | $3{u}^{3}-v$ | $3 B C E u^{3} - B D E v$ | correct | direct determinant |
| ba0b239b-6293-5a6c-a399-4c20fbd9ba89 | $2{u}^{2}{v}^{2}$ | $2 A E u^{2} v^{2}$ | wrong | opaque expression pattern |
| c9d8a949-98c9-53b2-a5c0-d91ecebaaf5b | $-u{v}^{2}$ | $- A E u v^{2}$ | wrong | opaque expression pattern |

Bank: five expressions together, selected before sampling; reject the entire instance on an equivalent or correct wrong expression. All five original values match their parameter recipes at the exact captured parameters. No extra/missing source choices.

### polynomial_mixed-observed
Prompt component slots: $x=A u^{2} + B v w,\quad y=- C u v + K,\quad z=D v^{2} - w$.

| Source choice UUID | Complete original value | Parameterized expression recipe | Designation | Interpretation |
|---|---|---|---|---|
| 03b82058-2ed1-5ab3-8be0-f2ccd9e791be | $2uv-2u{v}^{2}-vu$ | $2 A C u v - 2 B C D u v^{2} - C u v$ | wrong | opaque expression pattern |
| 2b07851c-5666-5e08-93b4-ea52710578c9 | $2{u}^{2}-2{v}^{3}-vw$ | $2 A C u^{2} - 2 B C D v^{3} - B C v w$ | correct | direct determinant |
| 4e04d287-7eaa-501d-ba5e-706a25e1adcd | $2vw$ | $2 B v w$ | wrong | opaque expression pattern |
| 78a6574d-a7a7-5dd3-9372-265b4fd8dfa8 | $2uv-2u{v}^{2}+vu$ | $2 A C u v - 2 B C D u v^{2} + C u v$ | wrong | opaque expression pattern |
| c5d7dba0-5d86-5a7b-97ed-55ed0cf1cb1c | $2{u}^{2}-2{v}^{3}+vw$ | $2 A C u^{2} - 2 B C D v^{3} + B C v w$ | wrong | opaque expression pattern |

Bank: five expressions together, selected before sampling; reject the entire instance on an equivalent or correct wrong expression. All five original values match their parameter recipes at the exact captured parameters. No extra/missing source choices.

### linear_offdiag-observed
Prompt component slots: $x=A v + B w,\quad y=C u + D w,\quad z=E u + F v$.

| Source choice UUID | Complete original value | Parameterized expression recipe | Designation | Interpretation |
|---|---|---|---|---|
| 09c7d7c2-430d-5af8-9d05-fa5665e62862 | $2$ | $A D E + B C F$ | correct | direct determinant |
| 6f2a26b3-3177-579e-877d-0fe20ffae536 | $0$ | $0$ | wrong | opaque expression pattern |
| 9406cdae-72e2-5c66-8ad2-f1e16969ae1d | $-1$ | $- A$ | wrong | opaque expression pattern |
| af88273c-a488-5b6d-af48-680f8f2c6cda | $-2$ | $- A D E - B C F$ | wrong | opaque expression pattern |
| de9aadb1-15c7-5202-b107-ef067be5cce6 | $1$ | $A$ | wrong | opaque expression pattern |

Bank: five expressions together, selected before sampling; reject the entire instance on an equivalent or correct wrong expression. All five original values match their parameter recipes at the exact captured parameters. No extra/missing source choices.

### symbolic_diagonal-observed
Prompt component slots: $x=A a u,\quad y=B b v,\quad z=C c w$.

| Source choice UUID | Complete original value | Parameterized expression recipe | Designation | Interpretation |
|---|---|---|---|---|
| 146610e3-5c1c-5561-9ca3-9774666c6c05 | $-a-b-c$ | $- A a - B b - C c$ | wrong | method-related expression |
| 4d3fd2ac-fcea-50a9-92dd-45cccffc9e3a | $-abc$ | $- A B C a b c$ | wrong | method-related expression |
| 5938eea0-a7c5-5a7f-bf1f-a9fd0efaaf3a | $a+b+c$ | $A a + B b + C c$ | wrong | method-related expression |
| 7a38c64c-896b-5232-a5e4-465265d40434 | $abc$ | $A B C a b c$ | correct | direct determinant |
| b5179334-ac94-5f42-8f5c-8c9ece45c7a9 | $0$ | $0$ | wrong | method-related expression |

Bank: five expressions together, selected before sampling; reject the entire instance on an equivalent or correct wrong expression. All five original values match their parameter recipes at the exact captured parameters. No extra/missing source choices.

## Stage 4 — reusable Markdown/value templates

The implementation retains each source’s full prose and common formal blocks. Whole display components are slots: prompt component vector/equations, optional “Here” equations, nine partials, and the final aligned determinant calculation. Complete slots prevent unintended substitutions inside labels or basis variables. Components, Jacobian entries, chosen minors, signs, evaluated products, and final answer are all computed from the same exact SymPy expressions. Normalization changes typography/grouping, not mathematical equations or prose.

Chosen expansions: sparse_trig row 1; sparse_exp column 2; sparse_square row 3; log_product column 3; rotation row 3; polynomial_column column 3; polynomial_mixed column 1; linear_offdiag row 1; symbolic_diagonal row 1. The square source uses its third row, avoiding an extra zero minor. The log source intentionally retains the second cancelling minor. Polynomial_column has three calculation rows; all other observed templates have four. Source prose and all display-stage counts are enforced independently.

The authored hard family expands row 3 and has six calculation rows: substituted determinant, two-minor Laplace expansion, distributed w-identity factors, reduced w terms, factored v-identity, final determinant. Its intermediate structures are retained with explicit masks; CAS simplification is reserved for correct final expressions.

All authored complete bank operations are implemented explicitly in bank(): wrong cofactor sign, omitted power/chain factor, wrong held coordinate, omitted pivot scale, omitted diagonal/offdiagonal minor product, swapped variable/column, cancelling only one minor, omitted Laplace contribution, trace instead of determinant, and omitted radial product. Each family selects exactly its own complete five-operation profile before sampling. There is no pooled first-valid fallback and no unrelated numeric perturbation. Exact operations are named in generation.distractor_recipes.

Parameters/domains and provenance belong to generation metadata; field/answer UUIDs are field-owned. A mathematical fingerprint hashes the full printed derivative matrix, excluding additive constants and banks. Content identity hashes version, difficulty, actual prompt, fixed solution and the complete sorted bank/correct value; seed and option order are excluded. Changing the complete bank changes identity when displayed content changes.

## Plots

Plot rating none. Practice questions contain only mathematical displays. Canonical and introductory image references used to display formulas/intuition do not become assessment plots; no parameter-dependent geometry is assessed. No image assets are emitted.
