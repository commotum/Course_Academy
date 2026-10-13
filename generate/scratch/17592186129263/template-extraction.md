# Template extraction

## 1. Specific source descriptions

All sources use exact scalars, no rounding, one five-option radio field. Original prompts, fields, UUIDs, answer values and worked solutions remain intact in source.json.

### q-160380 — polar

Parameters: `{"U": "1", "V": "2", "a": 2, "b": 3}`. Domain: `R^2`. Functions and point are displayed in the exact source/replay review. Correct scalar: $6$.

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}2u\operatorname{cos}⁡v \\ 3u\operatorname{sin}⁡v\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}1 \\ 2\end{aligned}].$

### q-160394 — exp_pair

Parameters: `{"U": "0", "V": "-5", "a": 1, "b": 1}`. Domain: `R^2`. Functions and point are displayed in the exact source/replay review. Correct scalar: $-2$.

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{u+v} \\ {e}^{u-v}\end{aligned}].
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}0 \\ -5\end{aligned}].$

### q-160383 — quotient

Parameters: `{"U": "-2", "V": "3", "a": 1, "b": 1}`. Domain: `u != 0`. Functions and point are displayed in the exact source/replay review. Correct scalar: $-3$.

For the transformation $T,$ defined as 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}uv \\ \frac{v}{u}\end{aligned}]
$$

 

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}-2 \\ 3\end{aligned}].$

### q-160402 — exp_log

Parameters: `{"U": "1", "V": "1", "a": 1, "b": 1}`. Domain: `uv > 0`. Functions and point are displayed in the exact source/replay review. Correct scalar: $2$.

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{u-v} \\ \operatorname{ln}⁡(uv)\end{aligned}].
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}1 \\ 1\end{aligned}].$

### q-160427 — square_pair

Parameters: `{"U": "-2", "V": "1", "a": 1, "b": 1}`. Domain: `R^2`. Functions and point are displayed in the exact source/replay review. Correct scalar: $16$.

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}+{v}^{2} \\ {u}^{2}-{v}^{2}\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}-2 \\ 1\end{aligned}].$

### q-160428 — complex_square

Parameters: `{"U": "-1", "V": "-2", "a": 1, "b": 1}`. Domain: `R^2`. Functions and point are displayed in the exact source/replay review. Correct scalar: $5$.

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{{u}^{2}-{v}^{2}}{2} \\ uv\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}-1 \\ -2\end{aligned}].$

### q-160431 — mixed_linear

Parameters: `{"U": "8", "V": "-2", "a": 1, "b": 1}`. Domain: `R^2`. Functions and point are displayed in the exact source/replay review. Correct scalar: $2$.

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{v}^{2}+uv \\ v-u\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}8 \\ -2\end{aligned}].$

### q-160440 — diagonal_trig

Parameters: `{"U": "pi/6", "V": "0", "a": 1, "b": 1}`. Domain: `R^2`. Functions and point are displayed in the exact source/replay review. Correct scalar: $-\frac{1}{2}$.

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\operatorname{cos}⁡u \\ \operatorname{sin}⁡v\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}\pi /6 \\ 0\end{aligned}].$

### q-160445 — diagonal_trig

Parameters: `{"U": "pi/4", "V": "pi/4", "a": 2, "b": -3}`. Domain: `R^2`. Functions and point are displayed in the exact source/replay review. Correct scalar: $3$.

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}2\operatorname{cos}⁡u \\ -3\operatorname{sin}⁡v\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}\pi /4 \\ \pi /4\end{aligned}].$

### q-160434 — coupled_trig

Parameters: `{"U": "pi/4", "V": "pi/4", "a": 1, "b": 1}`. Domain: `R^2`. Functions and point are displayed in the exact source/replay review. Correct scalar: $2$.

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\operatorname{cos}⁡(u+v) \\ \operatorname{sin}⁡(u-v)\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}\pi /4 \\ \pi /4\end{aligned}].$

### q-160387 — quadratic_linear

Parameters: `{"U": "1", "V": "1", "a": 3, "b": 2, "c": 1, "d": 2}`. Domain: `R^2`. Functions and point are displayed in the exact source/replay review. Correct scalar: $22$.

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}3{u}^{2}+2v \\ u+2{v}^{2}\end{aligned}].
$$

compute the value of the Jacobian determinant at the point where
$[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}1 \\ 1\end{aligned}].$

## 2. Generalized pattern

For differentiable x(u,v),y(u,v) on an open domain containing the stated point, compute the four partial derivatives, form x_u y_v−x_v y_u, simplify, and evaluate at the given coordinates. Output one exact scalar using the observed radio layout. Trig pairs require the familiar Pythagorean identity or familiar-angle values; exponential/log pairs require chain rule and reciprocal derivatives; polynomial pairs use ordinary power/product derivatives. No separate geometric interpretation is assessed.

## 3. Component and complete-bank mapping

Let E be the independently computed determinant value at the prompt point. Each table row maps every original option to its field and parameterized value `r*E`. This normalized scalar pattern is an explicit replay representation, not a recovered learner error theory. Sparse scalar evidence underdetermines error intent; ratios are recorded honestly and never promoted to default generation. E is derived from source function/point parameters on every call, so changing those parameters changes the full bank without any source-value lookup.

### observed_polar

Source q-160380; field `selection` / `55a2c95f-16e9-55cb-83b5-4438e90426c5`; parameters `{"U": "1", "V": "2", "a": 2, "b": 3}`.

| Original answer UUID | Exact source value | Parameterized operation | Correct |
|---|---|---|---|
| 683571f2-07f3-587b-82c8-c91f90742301 | $0$ | `(0)*E` | False |
| 875f9442-0384-5276-af8d-5acd1c256c62 | $4$ | `(2/3)*E` | False |
| 8db57813-6b8a-52b7-ac15-2e606c882c87 | $12$ | `(2)*E` | False |
| ab3728d1-c1cf-5eef-a87d-a43db22f1937 | $8$ | `(4/3)*E` | False |
| cae52c74-ecff-52ad-a806-db5d5566d474 | $6$ | `(1)*E` | True |
### observed_exp_pair

Source q-160394; field `selection` / `482d9065-f53f-5f23-9e90-27007d015ddc`; parameters `{"U": "0", "V": "-5", "a": 1, "b": 1}`.

| Original answer UUID | Exact source value | Parameterized operation | Correct |
|---|---|---|---|
| 0ef5e4bf-4d3f-5f5c-ac33-42ad4c6e3790 | $3$ | `(-3/2)*E` | False |
| 845f2f7c-94cc-5110-b14d-4efb54d153b3 | $-2$ | `(1)*E` | True |
| 899c753d-d349-5813-ae0c-d11e4c3c1c90 | $-1$ | `(1/2)*E` | False |
| d720bef8-4451-5b2f-95c9-1413643ea08d | $1$ | `(-1/2)*E` | False |
| f4f59278-293f-5cf8-80d1-7875f8166412 | $-3$ | `(3/2)*E` | False |
### observed_quotient

Source q-160383; field `selection` / `3f823688-c59b-5a64-9e51-9b7c368087e1`; parameters `{"U": "-2", "V": "3", "a": 1, "b": 1}`.

| Original answer UUID | Exact source value | Parameterized operation | Correct |
|---|---|---|---|
| 27184dd5-9306-5151-ba71-71c0184555b9 | $-4$ | `(4/3)*E` | False |
| 921684d8-1a85-53da-b8a7-23bd356d4d8f | $-3$ | `(1)*E` | True |
| a6b6ecd9-7efa-5fbf-99f4-87cf3cf2fc2b | $3$ | `(-1)*E` | False |
| a9f4d180-9148-56f8-af89-c87393729376 | $1$ | `(-1/3)*E` | False |
| bc4ef6cf-c02f-531a-934f-84c5afac9290 | $2$ | `(-2/3)*E` | False |
### observed_exp_log

Source q-160402; field `selection` / `795a7cef-1005-511a-9200-2ed1ac91ad82`; parameters `{"U": "1", "V": "1", "a": 1, "b": 1}`.

| Original answer UUID | Exact source value | Parameterized operation | Correct |
|---|---|---|---|
| 1b2ac211-6ede-500a-9363-0c90ed1326ea | $2$ | `(1)*E` | True |
| 241de261-1031-55ca-a058-00911568c512 | $0$ | `(0)*E` | False |
| 54f35b13-d77e-5a66-b2b8-4f7e13bf0284 | $1$ | `(1/2)*E` | False |
| b3da8c48-0f97-556c-90bd-47b71461d13c | $3$ | `(3/2)*E` | False |
| c49fcad0-5cc2-5449-8be5-a58c6c177d96 | $-1$ | `(-1/2)*E` | False |
### observed_square_pair

Source q-160427; field `selection` / `ade1226d-3be4-5422-9ead-d085939320b3`; parameters `{"U": "-2", "V": "1", "a": 1, "b": 1}`.

| Original answer UUID | Exact source value | Parameterized operation | Correct |
|---|---|---|---|
| 3a030248-80e5-5392-828d-2bf5b0f34c56 | $16$ | `(1)*E` | True |
| 46441063-cd17-57f8-93da-47999b8389f3 | $-8$ | `(-1/2)*E` | False |
| 4d076db5-f0b8-5a55-b9f9-a751427c3ef4 | $14$ | `(7/8)*E` | False |
| 8d6588ee-c55c-5f42-9ca1-f5f8f0e473ab | $12$ | `(3/4)*E` | False |
| dc0b5777-e3d4-5733-95a0-9024964404d1 | $18$ | `(9/8)*E` | False |
### observed_complex_square

Source q-160428; field `selection` / `cc930da6-f008-59fd-875c-d797cf29d182`; parameters `{"U": "-1", "V": "-2", "a": 1, "b": 1}`.

| Original answer UUID | Exact source value | Parameterized operation | Correct |
|---|---|---|---|
| 7338df5d-9ede-525b-86f7-9575217f0621 | $5$ | `(1)*E` | True |
| 9194b3db-7eb6-5b12-82d1-c39ced725329 | $-2$ | `(-2/5)*E` | False |
| 9f339d05-8ec4-52fc-929d-9e259b65d946 | $2$ | `(2/5)*E` | False |
| ae707e98-98f8-52a3-8963-4e1ec7a26492 | $3$ | `(3/5)*E` | False |
| e115090f-5258-55ab-a7de-95ef1c7a3b91 | $8$ | `(8/5)*E` | False |
### observed_mixed_linear

Source q-160431; field `selection` / `946d36e5-48fa-5671-b5c2-6b9df0953fbc`; parameters `{"U": "8", "V": "-2", "a": 1, "b": 1}`.

| Original answer UUID | Exact source value | Parameterized operation | Correct |
|---|---|---|---|
| 09e0e11f-ca64-573d-aa4a-39c0085748ca | $4$ | `(2)*E` | False |
| 2571ec42-1410-5512-abb4-5d9f33e67cf4 | $6$ | `(3)*E` | False |
| 6056f233-baaf-59fc-ab26-47501271c259 | $1$ | `(1/2)*E` | False |
| e97346e5-01ac-55ce-b840-edd902ee3c65 | $2$ | `(1)*E` | True |
| fa81b135-dfdc-52eb-85bc-1dd61c22d3d4 | $3$ | `(3/2)*E` | False |
### observed_diagonal_trig

Source q-160440; field `selection` / `ed0e005f-2ede-5db6-90a3-c44e813e721d`; parameters `{"U": "pi/6", "V": "0", "a": 1, "b": 1}`.

| Original answer UUID | Exact source value | Parameterized operation | Correct |
|---|---|---|---|
| 201b5adb-fe9e-56a4-a103-cfa7fd40fca9 | $-1$ | `(2)*E` | False |
| 6b7b2609-013a-5fdd-ad02-4411dd975fa7 | $0$ | `(0)*E` | False |
| 7c015757-c6cd-5661-8772-840f2ddff2cf | $\frac{1}{2}$ | `(-1)*E` | False |
| 803b5ba9-187d-5e4c-a266-d33068d508bd | $1$ | `(-2)*E` | False |
| af79779a-7d08-51aa-a7a1-413703ca604d | $-\frac{1}{2}$ | `(1)*E` | True |
### observed_diagonal_trig_scaled

Source q-160445; field `selection` / `c478e331-2d1a-585a-9599-198d7061ae49`; parameters `{"U": "pi/4", "V": "pi/4", "a": 2, "b": -3}`.

| Original answer UUID | Exact source value | Parameterized operation | Correct |
|---|---|---|---|
| 4dc0ac04-220f-5368-899c-f4b853d6caf1 | $3$ | `(1)*E` | True |
| f515d3db-880a-5d23-99f0-9cb65e633ebf | $2$ | `(2/3)*E` | False |
| 57254211-1cc3-5a7f-87e1-0c345d6ba0b6 | $6$ | `(2)*E` | False |
| 0ab4227a-a1c7-56de-9a4e-de04cc753871 | $4$ | `(4/3)*E` | False |
| 47ca5fb3-37c5-5519-9b75-0484cfdf1808 | $-6$ | `(-2)*E` | False |
### observed_coupled_trig

Source q-160434; field `selection` / `eeaaf6e0-abe7-5c25-953e-f15cf6c1b87a`; parameters `{"U": "pi/4", "V": "pi/4", "a": 1, "b": 1}`.

| Original answer UUID | Exact source value | Parameterized operation | Correct |
|---|---|---|---|
| b616ca6f-9ed2-50cf-882d-c8ff1503540f | $2$ | `(1)*E` | True |
| e8495e34-5713-5977-90f2-f1d23c192117 | $1$ | `(1/2)*E` | False |
| f3941799-b16e-5c96-afab-c5161cad125c | $4$ | `(2)*E` | False |
| 8235a654-792e-5e9c-921e-555040b5595a | $-1$ | `(-1/2)*E` | False |
| 2326b5cf-7dc7-542b-9226-1befd327ddd0 | $-2$ | `(-1)*E` | False |
### observed_quadratic_linear

Source q-160387; field `selection` / `b6520f4c-cce8-5e56-adce-0289e4c3517a`; parameters `{"U": "1", "V": "1", "a": 3, "b": 2, "c": 1, "d": 2}`.

| Original answer UUID | Exact source value | Parameterized operation | Correct |
|---|---|---|---|
| 0e0d4b0b-8093-5290-b6b4-484e2a3c019b | $20$ | `(10/11)*E` | False |
| 3f52c558-a8f4-5f12-84e4-136a7b9663ae | $24$ | `(12/11)*E` | False |
| ad3faf64-35fa-5814-9c5b-2c546aef7f2f | $12$ | `(6/11)*E` | False |
| c802b759-c3a3-5234-a525-52e3dcf0d733 | $22$ | `(1)*E` | True |
| df929076-a9d7-5c37-b534-2a48f5c0f2ed | $16$ | `(8/11)*E` | False |

Authored default complete banks derive P=x_u*y_v at the point and Q=x_v*y_u at the point. General polynomial noncancelling families use `[E,P+Q,-E,P,-Q]`. Cancelling families use `[E,-E,P,x_u(point)-Q,y_v(point)-Q]`; omitted factors are whole derivative-factor omissions, not random value perturbations. Diagonal trig uses `[E,-E,-ab,ab*cos(U)*cos(V),ab*sin(U)*sin(V)]`, corresponding to sign/derivative/evaluation operations. The entire selected bank is rejected if any pair is equivalent or any value is nonfinite. These inferred method-error banks are separately authored; they do not claim recovered source intent. No error diagnosis is inserted into learner text.

## 4. Reusable Markdown/value template

Fixed prompt: "For the transformation $T,$ defined as" + displayed transformation, then "compute the value of the Jacobian determinant at the point where" + displayed column-vector equality. Fixed solution sentences match the sources: "Given a transformation", determinant definition, "Here, we have", "First, we find the partial derivatives:", "Therefore, the corresponding Jacobian determinant is", "Finally, when", and "the value of our Jacobian determinant is".

Variable components: two exact function expressions, exact point coordinates, four derivatives, derivative determinant matrix, fully parenthesized distributed ad-bc row, source-family extra simplification row where present, simplified determinant and actual numeric substitution/value. Conditional extra rows are the polar identity, exponential-pair two terms, cancelling square products, mixed-linear products and coupled-trig products. One worked solution is fixed independent of chosen answer. Sources with short solutions retain that sequence without invented distractor explanation. Notation is normalized, not claimed byte-for-byte.

Domains: R² except quotient u≠0 and log-product uv>0. Coefficients are nonzero exact small integers; generator functions and domain checks are shared across profiles. Point inputs are exact integer strings or familiar pi fractions. Source parameter dictionaries are replayable, including negative points/scales; explicit invalid dictionaries fail instead of silently resampling. Normal sampling uses positive scales1..5, small signed integer points1..4, familiar trig angles, with documented exp/log cancellation (moderate unequal coefficients2..7 and same-sign points), trig familiar-argument restriction and hard bounds.

Identity: mathematical fingerprint uses canonical SymPy function/point/domain expressions, independent of profile or source parameter spelling; content identity uses version, difficulty, displayed prompt, fixed worked solution and full sorted bank, independent of shuffle seed. Distinct displayed banks have distinct IDs. Full-field native grading is separate from independent printed mathematics and original-bank fidelity.

Source correction: q-160380 cos²+cos² is repaired to cos²+sin². Original remains available. No questions or wrong options are dropped. No plots are generated because all inspected canonical assets encode standalone mathematics.
