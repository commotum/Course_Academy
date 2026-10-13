# Template extraction

## 1. Describe each source specifically

The table in classification.md fixes every source's original number features, field and bank assignment. Specific descriptions and complete choice mappings follow below. The exact raw prompt/solution/choice evidence is source.json and originals are printed in review.md. Source function notation sometimes has invisible Unicode application characters; generated LaTeX normalizes those to standard ln. All source values are complete primitives, not coefficient blanks.

### q-14434

$\int 6x{e}^{4x}\,\text{d}x=$

Parameters `{"a": 6, "b": 0, "h": 0, "k": 4}`; template `e_positive`; field `radio/selection`, five math options. Polynomial derivative is 6; exponential slope 4 and additive exponent shift 0. Final layout: split. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `40e31ec9-8fca-5231-8200-ca80bc72b044` | $\frac{x{e}^{4x}}{3}+\frac{x{e}^{4x}}{9}+C$ | `(2*x*exp(h + k*x)/a) + (4*x*exp(h + k*x)/a**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `997e80aa-81e0-539a-a4da-c477e354e208` | $\frac{3x{e}^{4x}}{2}-\frac{3{e}^{4x}}{8}+C$ | `(a*x*exp(h + k*x)/k) + (-a*exp(h + k*x)/k**2) + C` | correct | empirical expression replay; historical error intent unresolved |
| `c854fd56-2342-58ef-b090-fd79a6ccd523` | $\frac{3x{e}^{4x}}{2}-\frac{3{e}^{4x}}{9}+C$ | `(a*x*exp(h + k*x)/k) + (-a*exp(h + k*x)/(2*(k - 1)**2)) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `df814db1-8188-5e1b-812c-d9b512f99e8d` | $\frac{x{e}^{4x}}{2}-\frac{3{e}^{4x}}{8}+C$ | `(x*exp(h + k*x)/2) + (-a*exp(h + k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `f0053e13-ea2e-5ba8-b9dc-186d83b1f4f5` | $\frac{{e}^{4x}}{3}+\frac{{e}^{4x}}{9}+C$ | `(2*exp(h + k*x)/a) + (4*exp(h + k*x)/a**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-114288

$\int 4x{e}^{8x}\,\text{d}x=$

Parameters `{"a": 4, "b": 0, "h": 0, "k": 8}`; template `e_positive`; field `radio/selection`, five math options. Polynomial derivative is 4; exponential slope 8 and additive exponent shift 0. Final layout: split. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `3f62ef64-e190-59a0-80de-2a8c873c7f56` | $\frac{x{e}^{8x}}{2}-\frac{{e}^{8x}}{4}+C$ | `(a*x*exp(h + k*x)/k) + (-exp(h + k*x)/a) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `81cbaf36-0102-5b7f-97ff-d66d8054c9ac` | $\frac{x{e}^{8x}}{4}+\frac{5{e}^{8x}}{16}+C$ | `(x*exp(h + k*x)/a) + ((a + 1)*exp(h + k*x)/(2*k)) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `99e7a715-8634-5d28-bb4e-237d83c69b86` | $\frac{x{e}^{8x}}{8}-\frac{{e}^{8x}}{16}+C$ | `(x*exp(h + k*x)/k) + (-exp(h + k*x)/(2*k)) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `afef77b3-81af-530d-a6f6-eb398f03a3c3` | $\frac{x{e}^{8x}}{2}-\frac{{e}^{8x}}{16}+C$ | `(a*x*exp(h + k*x)/k) + (-a*exp(h + k*x)/k**2) + C` | correct | empirical expression replay; historical error intent unresolved |
| `e249a080-5cfd-59dd-bdec-1e4e038339ad` | $\frac{3x{e}^{8x}}{8}+\frac{{e}^{8x}}{12}+C$ | `(x*(a - 1)*exp(h + k*x)/k) + (exp(h + k*x)/(a + k)) + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-2425

Calculate $\intx2^{x}dx$.

Parameters `{"a": 1, "b": 0, "r": 2}`; template `base_legacy`; field `radio/selection`, five math options. Polynomial derivative is 1; exponential base 2 requires division by ln(base) twice. Final layout: base. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `a175a8cb-a6ee-5116-a42e-7718588e0c8a` | $\frac{2^{x}}{\ln 2}(\frac{1}{x} - \frac{x}{\ln 2}) + C$ | `r**x*(-x/log(r) + 1/x)/log(r) + C` | missing original ref | empirical expression replay; historical error intent unresolved |
| `b04d4f7a-8a20-52a1-b476-c32936814c77` | $\frac{2^{x}}{\ln 2}(x - 1) + C$ | `r**x*(x - 1)/log(r) + C` | missing original ref | empirical expression replay; historical error intent unresolved |
| `da1a54a0-de58-5994-a0ad-8678d8dee9ba` | $\frac{2^{x}}{\ln 2}(1 - \frac{x}{\ln 2}) + C$ | `r**x*(-x/log(r) + 1)/log(r) + C` | missing original ref | empirical expression replay; historical error intent unresolved |
| `ec8d992b-235f-5112-bb41-ee409c14309a` | $\frac{2^{x}}{\ln 2}(x + \frac{1}{\ln 2}) + C$ | `r**x*(x + 1/log(r))/log(r) + C` | missing original ref | empirical expression replay; historical error intent unresolved |
| `638dab82-2814-5689-94e7-12a7d4a7dbd7` | $\frac{2^{x}}{\ln 2}(x - \frac{1}{\ln 2}) + C$ | `r**x*(x - 1/log(r))/log(r) + C` | missing original ref | empirical expression replay; historical error intent unresolved |
### q-114287

Calculate $\int 6x{e}^{-3x}\,\text{d}x.$

Parameters `{"a": 6, "b": 0, "h": 0, "k": -3}`; template `e_negative_distributed`; field `radio/selection`, five math options. Polynomial derivative is 6; exponential slope -3 and additive exponent shift 0. Final layout: split. An extra distributed by-parts row precedes the final integral. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `26da406a-b1ee-533c-8e84-f3f3308fd3a3` | $\frac{x{e}^{-3x}}{2}-\frac{2{e}^{-3x}}{3}+C$ | `(x*exp(h + k*x)/2) + (a*exp(h + k*x)/(3*k)) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `b6c223c6-0129-5a77-a5c1-dbc22604a28d` | $-2x{e}^{-3x}-\frac{2{e}^{-3x}}{3}+C$ | `(a*x*exp(h + k*x)/k) + (-a*exp(h + k*x)/k**2) + C` | correct | empirical expression replay; historical error intent unresolved |
| `b96beb80-9254-5797-a25b-3e85eaa45af7` | $4x{e}^{-3x}-\frac{3{e}^{-3x}}{2}+C$ | `(x*(a - 2)*exp(h + k*x)) + (k*exp(h + k*x)/2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `bc8237c1-5f1b-5b27-84a1-36bf62527629` | $-x{e}^{-3x}+\frac{2{e}^{-3x}}{3}+C$ | `(-x*exp(h + k*x)) + (-a*exp(h + k*x)/(3*k)) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `f1f75f10-d4ff-5f2b-8f08-23ed364814bc` | $-3x{e}^{-3x}-\frac{{e}^{-3x}}{3}+C$ | `(k*x*exp(h + k*x)) + (exp(h + k*x)/k) + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-114289

Calculate $\int x{3}^{x}\,\text{d}x.$

Parameters `{"a": 1, "b": 0, "r": 3}`; template `base_calculate`; field `radio/selection`, five math options. Polynomial derivative is 1; exponential base 3 requires division by ln(base) twice. Final layout: base. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `022d7b7b-070a-51f5-bd49-94b4db34c49a` | $\frac{{3}^{x}}{\operatorname{ln}⁡3}(2x+\frac{1}{\operatorname{ln}⁡3})+C$ | `r**x*(2*x + 1/log(r))/log(r) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `2e34cf00-1e95-5551-a888-a986e9043bfd` | $\frac{{3}^{x}}{\operatorname{ln}⁡3}(x-\frac{1}{\operatorname{ln}⁡3})+C$ | `r**x*(x - 1/log(r))/log(r) + C` | correct | empirical expression replay; historical error intent unresolved |
| `76108c8b-8f42-5f4a-9dd2-e847f09e6e05` | $\frac{{3}^{x}}{\operatorname{ln}⁡3}(\frac{1}{\operatorname{ln}⁡3}-\frac{x}{2})+C$ | `r**x*(-x/2 + 1/log(r))/log(r) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `8bfdc77f-bbbe-57f4-9329-f07738aa11a0` | $\frac{{3}^{x}}{\operatorname{ln}⁡3}(x-\frac{1}{3})+C$ | `r**x*(x - 1/r)/log(r) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `c6440ae3-1132-5195-b3a2-356c7752e48e` | $\frac{{3}^{x}}{\operatorname{ln}⁡3}(x-1)+C$ | `r**x*(x - 1)/log(r) + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-114290

Calculate the integral $\int (x-2){e}^{x+3}\,\text{d}x.$

Parameters `{"a": 1, "b": -2, "h": 3, "k": 1}`; template `hard_shift_unit`; field `radio/selection`, five math options. Polynomial derivative is 1; exponential slope 1 and additive exponent shift 3. Final layout: factor. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `04df1fbb-68fc-5df3-a2f3-5de5f64fbd4f` | $(x-3){e}^{x+3}+C$ | `(b + x - 1)*exp(h + k*x) + C` | correct | empirical expression replay; historical error intent unresolved |
| `059681dd-6855-5de5-adb1-fa9432d5314c` | $(\frac{x}{3}-6){e}^{x+3}+C$ | `(3*b + x/h)*exp(h + k*x) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `19b553b9-fab9-540b-be56-77f1ce0d0a8a` | $(2x-1){e}^{x+3}+C$ | `(-b*x - 1)*exp(h + k*x) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `c43e1a7b-f3a2-5b76-a623-7db7da101361` | $(\frac{x}{\operatorname{ln}⁡3}+3){e}^{x+3}+C$ | `(h + x/log(h))*exp(h + k*x) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `ec744b0d-6761-589d-ad26-06e817b26961` | $(\frac{x}{2}-3){e}^{x+3}+C$ | `(b - 1 - x/b)*exp(h + k*x) + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-114293

Calculate $\int (3x-4){e}^{-3x}\,\text{d}x.$

Parameters `{"a": 3, "b": -4, "h": 0, "k": -3}`; template `hard_negative_factor`; field `radio/selection`, five math options. Polynomial derivative is 3; exponential slope -3 and additive exponent shift 0. Final layout: factor. No extra distributed row. An additional common-denominator simplification row precedes the final factor.

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `36a625e0-f342-5d88-863b-2cc610f12c52` | $\frac{(2x-1){e}^{-3x}}{3}+C$ | `-(x*(a - 1) - 1)*exp(h + k*x)/k + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `3e06e8db-4185-544e-9ae5-0b2a2e9f7015` | $(1-x){e}^{-3x}+C$ | `(-a/k**2 + (a*x + b)/k)*exp(h + k*x) + C` | correct | empirical expression replay; historical error intent unresolved |
| `4d558edc-f058-5d64-aa0f-acff177c0e5b` | $(2-3x){e}^{-3x}+C$ | `(-a*x + 2)*exp(h + k*x) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `7aa27907-71bc-5690-9d5a-5ea98a3a03cb` | $(2x-1){e}^{-3x}+C$ | `(x*(a - 1) - 1)*exp(h + k*x) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `cd15176c-1580-5959-a4f3-0332eefaf817` | $\frac{(2-x){e}^{-3x}}{3}+C$ | `-(2 - x)*exp(h + k*x)/k + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-12462

Calculate the integral $\int 3x{e}^{-x}\,\text{d}x.$

Parameters `{"a": 3, "b": 0, "h": 0, "k": -1}`; template `e_negative_integral`; field `radio/selection`, five math options. Polynomial derivative is 3; exponential slope -1 and additive exponent shift 0. Final layout: split. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `271f180d-3faa-5476-a054-bf22f99176bc` | $-3x{e}^{-x}-2{e}^{-x}+C$ | `(-a*x*exp(h + k*x)) + ((1 - a)*exp(h + k*x)) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `4d6abd70-33c0-5278-82e7-159c499aad7f` | $-3x{e}^{-x}+{e}^{-x}+C$ | `(-a*x*exp(h + k*x)) + (exp(h + k*x)) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `9ef47045-065b-557c-a1cb-f734f625b80c` | $-3x{e}^{-x}-3{e}^{-x}+C$ | `(a*x*exp(h + k*x)/k) + (-a*exp(h + k*x)/k**2) + C` | correct | empirical expression replay; historical error intent unresolved |
| `b34f8ff6-8e7b-5a4a-b1de-16e75dced547` | $2{e}^{-x}-3x{e}^{-x}+C$ | `((a - 1)*exp(h + k*x)) + (-a*x*exp(h + k*x)) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `d29bd4f3-02bb-5eb5-b6ba-5b257eab8b0f` | $3{e}^{-x}-x{e}^{-x}+C$ | `(a*exp(h + k*x)) + (-x*exp(h + k*x)) + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-12556

Calculate the integral $\int x{e}^{-3x}\,\text{d}x.$

Parameters `{"a": 1, "b": 0, "h": 0, "k": -3}`; template `e_negative_integral`; field `radio/selection`, five math options. Polynomial derivative is 1; exponential slope -3 and additive exponent shift 0. Final layout: split. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `30b012af-7da3-57e7-b3fe-ad695b25321d` | $-\frac{x{e}^{-3x}}{3}-\frac{{e}^{-3x}}{9}+C$ | `(a*x*exp(h + k*x)/k) + (-a*exp(h + k*x)/k**2) + C` | correct | empirical expression replay; historical error intent unresolved |
| `394ffebc-fc15-59d2-b922-cf67e8668a24` | $\frac{x{e}^{-3x}}{9}+\frac{{e}^{-3x}}{9}+C$ | `(x*exp(h + k*x)/k**2) + (exp(h + k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `98f26b34-1c20-50e4-ae9f-0696b345d0e9` | $\frac{{e}^{-3x}}{3}-\frac{x{e}^{-3x}}{9}+C$ | `(-exp(h + k*x)/k) + (-x*exp(h + k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `dee11791-9fa1-5f13-86b4-6751c7ac156e` | $-\frac{x{e}^{3x}}{3}+\frac{{e}^{3x}}{9}+C$ | `(x*exp(h - k*x)/k) + (exp(h - k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `fa7bf65f-10a0-5fb7-85b0-318f615112d7` | $\frac{x{e}^{-3x}}{9}-\frac{{e}^{-3x}}{3}+C$ | `(x*exp(h + k*x)/k**2) + (exp(h + k*x)/k) + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-12559

Calculate $\int (3x+5){e}^{-5x}\,\text{d}x.$

Parameters `{"a": 3, "b": 5, "h": 0, "k": -5}`; template `hard_negative_split`; field `radio/selection`, five math options. Polynomial derivative is 3; exponential slope -5 and additive exponent shift 0. Final layout: split. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `236b60cf-ff8d-5674-870b-bcaaf8d37985` | $-\frac{(3x+5){e}^{5x}}{5}+\frac{3x{e}^{5x}}{25}+C$ | `(-(-a*x - b)*exp(h - k*x)/k) + (a*x*exp(h - k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `4d557db5-ba1a-5b05-b356-74912875cd91` | $\frac{(3x+5){e}^{-5x}}{5}+\frac{3x{e}^{-5x}}{25}+C$ | `(-(a*x + b)*exp(h + k*x)/k) + (a*x*exp(h + k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `5e1550eb-3fe9-5df7-a495-0e900c02c6de` | $\frac{(3x+5){e}^{-5x}}{25}-\frac{{e}^{-5x}}{5}+C$ | `((a*x + b)*exp(h + k*x)/k**2) + (exp(h + k*x)/k) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `5ffe0799-f21d-5fea-a233-c69798ab78fd` | $-\frac{(3x+5){e}^{-5x}}{5}-\frac{3{e}^{-5x}}{25}+C$ | `((a*x + b)*exp(h + k*x)/k) + (-a*exp(h + k*x)/k**2) + C` | correct | empirical expression replay; historical error intent unresolved |
| `92ec0b8f-683f-538a-921f-014ccb202f1e` | $-\frac{3x{e}^{-5x}}{25}-\frac{3{e}^{-5x}}{25}+C$ | `(-a*x*exp(h + k*x)/k**2) + (-a*exp(h + k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-12560

Calculate the integral $\int (x+7){e}^{2x+5}\,\text{d}x.$

Parameters `{"a": 1, "b": 7, "h": 5, "k": 2}`; template `hard_shift_split`; field `radio/selection`, five math options. Polynomial derivative is 1; exponential slope 2 and additive exponent shift 5. Final layout: split. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `109d035c-6ffc-56c3-8581-53bca2233532` | $-\frac{x{e}^{2x+5}}{4}+\frac{{e}^{2x+5}}{2}+C$ | `(-x*exp(h + k*x)/k**2) + (exp(h + k*x)/k) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `209845fa-bfdf-5169-8a21-91e5d6fa04ab` | $\frac{x{e}^{2x+5}}{4}-\frac{{e}^{2x+5}}{4}+C$ | `(x*exp(h + k*x)/k**2) + (-exp(h + k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `5be69881-f41a-506d-a346-ccfa892bacb0` | $\frac{(x+7){e}^{2x+5}}{4}-\frac{x{e}^{2x+5}}{4}+C$ | `((a*x + b)*exp(h + k*x)/k**2) + (-x*exp(h + k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `6a4a072e-05a9-58e4-83e0-911e978158f4` | $\frac{(x+7){e}^{2x+5}}{2}-\frac{{e}^{2x+5}}{4}+C$ | `((a*x + b)*exp(h + k*x)/k) + (-a*exp(h + k*x)/k**2) + C` | correct | empirical expression replay; historical error intent unresolved |
| `a0da683e-5345-5b81-9094-abd5ff0ec151` | $-\frac{(x+7){e}^{2x+5}}{4}+\frac{{e}^{2x+5}}{2}+C$ | `((-a*x - b)*exp(h + k*x)/k**2) + (exp(h + k*x)/k) + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-2420

$\int x{5}^{x}\,\text{d}x=$

Parameters `{"a": 1, "b": 0, "r": 5}`; template `base_equals`; field `radio/selection`, five math options. Polynomial derivative is 1; exponential base 5 requires division by ln(base) twice. Final layout: base. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `0c795865-da64-5e14-9024-3c7c02d718c0` | $\frac{{5}^{x}}{\operatorname{ln}⁡5}(\frac{1}{x}-\frac{x}{\operatorname{ln}⁡5})+C$ | `r**x*(-x/log(r) + 1/x)/log(r) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `51fe0db3-d702-5875-904d-f79bd58f19bd` | $\frac{{5}^{x}}{\operatorname{ln}⁡5}(x-1)+C$ | `r**x*(x - 1)/log(r) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `6e5a066a-1db0-5b07-b438-285b415f19bb` | $\frac{{5}^{x}}{\operatorname{ln}⁡5}(x-\frac{1}{\operatorname{ln}⁡5})+C$ | `r**x*(x - 1/log(r))/log(r) + C` | correct | empirical expression replay; historical error intent unresolved |
| `9611c013-b6fd-5217-9d39-883aca3329d3` | $\frac{{5}^{x}}{\operatorname{ln}⁡5}(1-\frac{x}{\operatorname{ln}⁡5})+C$ | `r**x*(-x/log(r) + 1)/log(r) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `c91e7928-ce32-56f4-8b9f-43257961903a` | $\frac{{5}^{x}}{\operatorname{ln}⁡5}(x+\frac{1}{\operatorname{ln}⁡5})+C$ | `r**x*(x + 1/log(r))/log(r) + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-114291

Calculate the integral $\int (2x+1){e}^{3x}\,\text{d}x.$

Parameters `{"a": 2, "b": 1, "h": 0, "k": 3}`; template `hard_positive_factor`; field `radio/selection`, five math options. Polynomial derivative is 2; exponential slope 3 and additive exponent shift 0. Final layout: factor. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `7fea6d91-968c-5f4d-8499-0425dc5d7fe2` | $\frac{(3x+2){e}^{3x}}{9}+C$ | `(a + x*(a + 1))*exp(h + k*x)/k**2 + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `df58de38-7310-5f19-9844-03c75ef49b7d` | $\frac{(6x+1){e}^{3x}}{9}+C$ | `(a*k*x - a + b*k)*exp(h + k*x)/k**2 + C` | correct | empirical expression replay; historical error intent unresolved |
| `f721fccd-de41-549f-b75e-093592b0c032` | $\frac{(6x+4){e}^{3x}}{3}+C$ | `(a*k*x + 2*a)*exp(h + k*x)/k + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `7db9ef7b-e876-5195-b2bc-5e90b186c364` | $\frac{(4x-3){e}^{3x}}{9}+C$ | `(-k + x*(a + 2))*exp(h + k*x)/k**2 + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `cab8da55-0308-5e36-8634-1b58557947b2` | $\frac{(4x-1){e}^{3x}}{3}+C$ | `(-b + x*(a + 2))*exp(h + k*x)/k + C` | incorrect | empirical expression replay; historical error intent unresolved |
### q-12558

$\int 3x{e}^{2x+5}\,\text{d}x=$

Parameters `{"a": 3, "b": 0, "h": 5, "k": 2}`; template `e_shift`; field `radio/selection`, five math options. Polynomial derivative is 3; exponential slope 2 and additive exponent shift 5. Final layout: split. No extra distributed row. 

| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |
|---|---|---|---|---|
| `2ba8cff6-a436-587b-947b-b845d40cdf1e` | $\frac{x{e}^{2x+5}}{4}+\frac{3{e}^{2x+5}}{4}+C$ | `(x*exp(h + k*x)/k**2) + (a*exp(h + k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `0bf7139d-5b6a-513e-8c05-ea38b19064dc` | $\frac{3{e}^{2x}}{2}-\frac{3x{e}^{2x}}{4}+C$ | `(a*exp(k*x)/k) + (-a*x*exp(k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `1a22e02f-c34e-55ad-b5ee-acd29d97566a` | $\frac{3{e}^{2x+5}}{2}-\frac{3x{e}^{2x+5}}{4}+C$ | `(a*exp(h + k*x)/k) + (-a*x*exp(h + k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |
| `b3c30e70-a737-5f41-9c71-a8d0f2188c7a` | $\frac{3x{e}^{2x+5}}{2}-\frac{3{e}^{2x+5}}{4}+C$ | `(a*x*exp(h + k*x)/k) + (-a*exp(h + k*x)/k**2) + C` | correct | empirical expression replay; historical error intent unresolved |
| `b1a00544-29af-5a0e-9dbd-8c18e64ae108` | $\frac{{e}^{2x+5}}{2}+\frac{3{e}^{2x+5}}{4}+C$ | `(exp(h + k*x)/k) + (a*exp(h + k*x)/k**2) + C` | incorrect | empirical expression replay; historical error intent unresolved |

In patterns x is the integration variable; a,b are polynomial coefficient/constant; k,h are exponential slope/shift; r is the integer base. `exp(k*x+h)` and `r**x` are computed from those prompt parameters. Each observed profile contains all five patterns together. Separate structured pieces preserve displayed sums even when algebraic collection is possible. The mappings are explicit empirical generalizations of whole expressions, not claims to have recovered source authoring code. Some coefficients in an empirical bank remain numerically anchored to its observed pattern. They are restricted to explicit replay/profile requests and never promoted to default distractor intent.

## 2. Generalized mathematical pattern

Integrate `(ax+b) exp(kx+h)` or `x r^x` by taking u to be the linear polynomial and v' the exponential. Compute u'=a and v=exp(kx+h)/k (or r^x/ln r), form uv minus the residual exponential integral, integrate it once, and append C. Source levels differ in the signed/logarithmic divisions and affine simplification they require; no new integration technique is introduced.

## 3. Components and banks

Each table above maps every original answer UUID and exact value to its whole expression recipe. Prompt template controls equals/Calculate/Calculate the integral, exponential type, linear-factor parentheses, and integral notation. The worked solution uses the source's shared sentences, states the by-parts identity, fixes u/u'/v'/v, substitutes their values, displays the remaining exponential integral, then a primitive and optional factored simplification. e_negative_distributed retains its extra distributed row and the original "We, substitute" sentence. hard_negative_factor retains the extra simplification row. Base layouts retain both the expanded primitive and final outer factor. No chosen error changes the fixed worked solution.

All 14 five-option source profiles are complete. The normal authored profile is `authored:parts_errors`, selected before any parameters are constructed. Its complete bank comprises correct uv-a*z/rate^2, reversed residual-integral sign uv+a*z/rate^2, omitted residual integral uv, reversed uv sign -uv-a*z/rate^2, and replacing u' with u in the residual integral uv-u*z/rate^2. This last operation is an explicit algebraic method error; no distractor feedback is shown. If any complete-bank member is equivalent, invalid, or correct unexpectedly, the whole instance is rejected. There is no first-valid pool or unrelated random perturbation.

## 4. Reusable template and constraints

The public API supports all 12 layouts, radio field requests, deterministic sampling, and exact source parameters/profiles. Explicit invalid inputs raise rather than silently changing values. Easy: a=1..8,k=1..8,b=h=0. Moderate negative: a=1..8,k=-1..-8,b=h=0; shifted moderate: positive k=1..8 and nonzero h=-8..8,b=0; base moderate: a=1,b=0,r=2..9. Hard: a=1..8, nonzero b=-8..8, the same k bounds and observed template sign/shift constraints; the unit-slope shift layout keeps a=k=1. Sampling remains unordered within each difficulty. Authored domains include the source coefficients and enough meaningful sign/coefficient/shift combinations for repeated practice, with the same single by-parts workload.

A source bank is eligible only for its assigned layout. Empirical profiles may have unknown error interpretation, but correct values and complete displayed bank equality are validated mathematically at every source parameter and at varied parameters. Their default alternatives are separately labeled authored banks. Values are compared modulo an additive integration constant because the assessed whole objects are indefinite primitives with explicit +C. Full derivatives, not isolated terms, are compared. Literal prose and semantic integration stages are checked separately from mathematical bank fidelity; LaTeX whitespace, standard ln notation, fraction placement, and equivalent grouping are normalized, so this is mathematical/structural fidelity rather than byte-for-byte source LaTeX.

q-2425 has no solution or correct designation in either source capture; its default supported solution follows the rated base-log layout. Prompt-spacing repair and derived designation are separated from original designation matches. All raw omissions remain in source.json. No empirical source errors in available correct primitives or worked stages were found. Source final choices retain +C; no arbitrary learner-facing error diagnoses are added.

Content identity hashes generator version, visible prompt, fixed worked solution, complete displayed bank, field type and key; it is independent of seed/choice order for fixed inputs. The mathematical fingerprint hashes the simplified visible integrand, independent of layout, bank, and presentation. UUIDs are field owned. JSON is local review data, never transaction EDN.

Plots: none. Steps 5 and 7 need no plot extractor/renderer. No image model, SVG, or plot dependency is used.
