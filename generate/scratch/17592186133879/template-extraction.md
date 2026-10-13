# Template extraction

## 1. Specific source descriptions

No source has a plot. Every field is radio/selection with five scalar exact math options; original IDs, field-owned answers and complete correct entities are retained in source-cases.json. No source bank is omitted.

### q-39349 — radial_log

Consider the vector field $F,$ defined as

$$
F(x,y)=\frac{x}{1+{x}^{2}+{y}^{2}}\,i+\frac{y}{1+{x}^{2}+{y}^{2}}\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y={x}^{2}\operatorname{ln}⁡(x+1)$ for $x\in [0,1].$

Parameters: `{"a": 1, "h": 1, "k": 1, "s": 1}`. Potential recovered in source solution: $\frac{\ln{\left(x^{2} + y^{2} + 1 \right)}}{2}$. Endpoint pair: $(0,0)$, $(1,\ln{\left(2 \right)})$.

Displayed solution block row counts: `[1, 1, 1, 2, 1, 1, 2, 5]`. Field components are smooth on all R²; the hard source checks mixed partials, parametrizes y(x), reconstructs f, and evaluates endpoints.

### q-98995 — quartic_trig

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨t+\operatorname{sin}⁡(\frac{\pi t}{2}),t+\operatorname{cos}⁡(\frac{\pi t}{2})⟩,\,0\le t\le 1.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F=x{y}^{2}\,i+{x}^{2}y\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Parameters: `{"a": 1, "r": 1, "s": 1}`. Potential recovered in source solution: $\frac{x^{2} y^{2}}{2}$. Endpoint pair: $(0,1)$, $(2,1)$.

Displayed solution block row counts: `[1, 2, 1, 2, 5]`. A given parametrization and conservative hint support potential reconstruction without a separate conservative-existence check.

### q-104725 — cubic_exponential

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨t,{e}^{t}⟩,\,0\le t\le 1.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F=(3{x}^{2}{y}^{3}+2x)\,i+(3{x}^{3}{y}^{2}-4y)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Parameters: `{"a": 1, "b": 1, "c": 2, "r": 1, "s": 1}`. Potential recovered in source solution: $x^{3} y^{3} + x^{2} - 2 y^{2}$. Endpoint pair: $(0,1)$, $(1,e)$.

Displayed solution block row counts: `[1, 2, 1, 2, 5]`. A given parametrization and conservative hint support potential reconstruction without a separate conservative-existence check.

### q-104728 — exponential_cosine

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨{t}^{2}+1,t⟩,\,0\le t\le 2\pi .
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F={e}^{x}\operatorname{cos}⁡y\,i-{e}^{x}\operatorname{sin}⁡y\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Parameters: `{"a": 1, "h": 1, "n": 2, "s": 1}`. Potential recovered in source solution: $e^{x} \cos{\left(y \right)}$. Endpoint pair: $(1,0)$, $(1 + 4 \pi^{2},2 \pi)$.

Displayed solution block row counts: `[1, 2, 1, 2, 5]`. A given parametrization and conservative hint support potential reconstruction without a separate conservative-existence check.

### q-104731 — cubic_product

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨2t,{t}^{2}-1⟩,\,0\le t\le 2.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F=(2xy-y)\,i+({x}^{2}-x)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Parameters: `{"a": 1, "b": 1, "h": 1, "r": 2, "s": 1, "u": 2}`. Potential recovered in source solution: $x^{2} y - x y$. Endpoint pair: $(0,-1)$, $(4,3)$.

Displayed solution block row counts: `[1, 2, 1, 2, 5]`. A given parametrization and conservative hint support potential reconstruction without a separate conservative-existence check.

### q-104733 — separable_cubic

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨3\operatorname{ln}⁡t,{t}^{2}⟩,\,1\le t\le 2.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F=({x}^{2}-y)\,i+({y}^{2}-x)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Parameters: `{"a": 1, "b": 1, "c": 1, "r": 3, "s": 1, "u": 2}`. Potential recovered in source solution: $\frac{x^{3}}{3} - x y + \frac{y^{3}}{3}$. Endpoint pair: $(0,1)$, $(3 \ln{\left(2 \right)},4)$.

Displayed solution block row counts: `[1, 2, 1, 2, 5]`. A given parametrization and conservative hint support potential reconstruction without a separate conservative-existence check.

### q-104739 — sine_exponential

Consider the vector field $F,$ defined as

$$
F(x,y)={y}^{2}\operatorname{cos}⁡x\,i+(2y\operatorname{sin}⁡x+{e}^{y})\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y={x}^{2}+{sin}^{2}⁡x$ for $x\in [0,\pi ].$

Parameters: `{"a": 1, "b": 1, "k": 1, "s": 1}`. Potential recovered in source solution: $y^{2} \sin{\left(x \right)} + e^{y}$. Endpoint pair: $(0,0)$, $(\pi,\pi^{2})$.

Displayed solution block row counts: `[1, 1, 1, 2, 1, 1, 2, 5]`. Field components are smooth on all R²; the hard source checks mixed partials, parametrizes y(x), reconstructs f, and evaluates endpoints.

### q-104745 — mixed_exponential

Consider the vector field $F,$ defined as

$$
F(x,y)=({e}^{y}+y\operatorname{cos}⁡x)\,i+(x{e}^{y}+\operatorname{sin}⁡x)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x+\operatorname{cos}⁡x$ for $x\in [0,\pi ].$

Parameters: `{"a": 1, "b": 1, "k": 1, "s": 1}`. Potential recovered in source solution: $x e^{y} + y \sin{\left(x \right)}$. Endpoint pair: $(0,1)$, $(\pi,-1 + \pi)$.

Displayed solution block row counts: `[1, 1, 1, 2, 1, 1, 2, 5]`. Field components are smooth on all R²; the hard source checks mixed partials, parametrizes y(x), reconstructs f, and evaluates endpoints.

### q-104747 — sine_product

Consider the vector field $F,$ defined as

$$
F(x,y)=\operatorname{cos}⁡x\operatorname{sin}⁡y\,i+\operatorname{cos}⁡y\operatorname{sin}⁡x\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y={e}^{\operatorname{sin}⁡x}+\operatorname{cos}⁡x$ for $x\in [0,\frac{\pi }{2}].$

Parameters: `{"a": 1, "k": 1, "s": 1}`. Potential recovered in source solution: $\sin{\left(x \right)} \sin{\left(y \right)}$. Endpoint pair: $(0,2)$, $(\frac{\pi}{2},e)$.

Displayed solution block row counts: `[1, 1, 1, 2, 1, 1, 2, 5]`. Field components are smooth on all R²; the hard source checks mixed partials, parametrizes y(x), reconstructs f, and evaluates endpoints.

### q-104761 — negative_exponential

Consider the vector field $F,$ defined as

$$
F(x,y)=2x{e}^{-y}\,i+(2y-{x}^{2}{e}^{-y})\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=\operatorname{ln}⁡(x-1)$ for $x\in [2,3].$

Parameters: `{"a": 1, "b": 1, "h": 1, "s": 1}`. Potential recovered in source solution: $x^{2} e^{- y} + y^{2}$. Endpoint pair: $(2,0)$, $(3,\ln{\left(2 \right)})$.

Displayed solution block row counts: `[1, 1, 1, 2, 1, 1, 2, 5]`. Field components are smooth on all R²; the hard source checks mixed partials, parametrizes y(x), reconstructs f, and evaluates endpoints.

### q-104764 — cubic_radical_path

Consider the vector field $F,$ defined as

$$
F(x,y)=(6{x}^{2}-y)\,i-x\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y={x}^{2}-{e}^{\sqrt{x+1}}$ for $x\in [0,3].$

Parameters: `{"a": 2, "b": 1, "n": 1, "s": 1}`. Potential recovered in source solution: $2 x^{3} - x y$. Endpoint pair: $(0,- e)$, $(3,9 - e^{2})$.

Displayed solution block row counts: `[1, 1, 1, 2, 1, 1, 2, 6]`. Field components are smooth on all R²; the hard source checks mixed partials, parametrizes y(x), reconstructs f, and evaluates endpoints.

### q-104732 — cosine_product

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨\operatorname{sin}⁡\pi t,\frac{\pi t}{2}⟩,\,0\le t\le \frac{1}{2}.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F=(2x\operatorname{cos}⁡y+y)\,i-({x}^{2}\operatorname{sin}⁡y-x)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Parameters: `{"a": 1, "b": 1, "n": 1, "r": 1, "s": 1}`. Potential recovered in source solution: $x^{2} \cos{\left(y \right)} + x y$. Endpoint pair: $(0,0)$, $(1,\frac{\pi}{4})$.

Displayed solution block row counts: `[1, 2, 1, 2, 5]`. A given parametrization and conservative hint support potential reconstruction without a separate conservative-existence check.

## 2. Generalized family description

Given a two-dimensional conservative field and an oriented curve, recover a potential from both gradient components, find ordered endpoints from the path, and subtract f(end)−f(start). Moderate sources give the parametrization and conservative hint; hard sources establish conservativeness on R² and parametrize a supplied Cartesian curve. Each potential/path family is a same-level variation, not a progression. Integer powers, familiar sine/cosine evaluations, exact logarithms/exponentials and perfect-square radical evaluations remain as observed.

## 3. Component and complete-bank map

All observed profiles are named observed_homogeneous within their own template. The only replay parameter freedom is F↦sF, f↦sf, and each option↦s times its complete source-shaped expression, s=1,2,3; path and relative coefficients remain fixed. This is a coherent field-scale operation, not an arbitrary fitted error polynomial. Exact expressions are observed evidence; the original author’s incorrect operation is unresolved except where obvious. These replay banks are not default banks and do not establish the authored variety claim.

| Source | Field UUID | Source answer UUID | Correct? | Exact observed value | Replay expression |
|---|---|---|---|---|---|
| q-39349 | `aa5eacfc-70b8-5d6e-b1f9-f5af4734a6b5` | `69c13dff-cd6b-59c8-8afc-6e8f8eabf8f5` | False | $\frac{1}{2}\operatorname{ln}⁡(2+\operatorname{ln}⁡2)$ | $s\left(\frac{1}{2}\operatorname{ln}⁡(2+\operatorname{ln}⁡2)\right)$ |
| q-39349 | `aa5eacfc-70b8-5d6e-b1f9-f5af4734a6b5` | `7e0e1662-5531-5797-9a2d-180d1aefa39b` | False | $\frac{1}{2}\operatorname{ln}⁡(1+{ln}^{2}⁡2)$ | $s\left(\frac{1}{2}\operatorname{ln}⁡(1+{ln}^{2}⁡2)\right)$ |
| q-39349 | `aa5eacfc-70b8-5d6e-b1f9-f5af4734a6b5` | `b060de89-9a07-5c08-8a5a-902923743941` | False | $\frac{1}{2}\operatorname{ln}⁡(4)$ | $s\left(\frac{1}{2}\operatorname{ln}⁡(4)\right)$ |
| q-39349 | `aa5eacfc-70b8-5d6e-b1f9-f5af4734a6b5` | `df7d018d-9bcc-56b5-9a57-3f93a49339b0` | False | $\frac{1}{2}\operatorname{ln}⁡(2)$ | $s\left(\frac{1}{2}\operatorname{ln}⁡(2)\right)$ |
| q-39349 | `aa5eacfc-70b8-5d6e-b1f9-f5af4734a6b5` | `fba1ed0a-e6ae-5b81-9e9c-40ba51cc6012` | True | $\frac{1}{2}\operatorname{ln}⁡(2+{ln}^{2}⁡2)$ | $s\left(\frac{1}{2}\operatorname{ln}⁡(2+{ln}^{2}⁡2)\right)$ |
| q-98995 | `f8db0f63-bf1b-537c-b12e-a90d68712f38` | `21bae757-f490-594c-be1d-7a2d2c77f021` | False | $4$ | $s\left(4\right)$ |
| q-98995 | `f8db0f63-bf1b-537c-b12e-a90d68712f38` | `2d6c9f0e-8b69-578c-b5ae-a56b0b59e2e2` | False | $6$ | $s\left(6\right)$ |
| q-98995 | `f8db0f63-bf1b-537c-b12e-a90d68712f38` | `356d8fc5-06cd-5609-b39b-96eddcad3b4f` | False | $\frac{1}{2}$ | $s\left(\frac{1}{2}\right)$ |
| q-98995 | `f8db0f63-bf1b-537c-b12e-a90d68712f38` | `be29d524-2692-5e36-bb76-b3ac0de7b124` | False | $1$ | $s\left(1\right)$ |
| q-98995 | `f8db0f63-bf1b-537c-b12e-a90d68712f38` | `ea0cfc9c-4409-56c9-956d-a96016bee45d` | True | $2$ | $s\left(2\right)$ |
| q-104725 | `fe8d7464-8b34-59c0-a3ab-f6d1c3d9d9bf` | `1dc17ac8-c43f-5795-99c6-96724b983951` | False | ${e}^{2}+{e}^{2}+1$ | $s\left({e}^{2}+{e}^{2}+1\right)$ |
| q-104725 | `fe8d7464-8b34-59c0-a3ab-f6d1c3d9d9bf` | `8ebf9cef-e23a-5e13-9dc3-bf7b4436f362` | False | $0$ | $s\left(0\right)$ |
| q-104725 | `fe8d7464-8b34-59c0-a3ab-f6d1c3d9d9bf` | `cee04a38-9ba8-5587-a832-c024ade625b0` | False | ${e}^{3}+{e}^{2}$ | $s\left({e}^{3}+{e}^{2}\right)$ |
| q-104725 | `fe8d7464-8b34-59c0-a3ab-f6d1c3d9d9bf` | `fee0c938-94f4-5d82-a936-a0e6d4c287bd` | True | ${e}^{3}-2{e}^{2}+3$ | $s\left({e}^{3}-2{e}^{2}+3\right)$ |
| q-104725 | `fe8d7464-8b34-59c0-a3ab-f6d1c3d9d9bf` | `ffbb53c3-5822-5141-810e-1e1ceaf85e79` | False | $1+{e}^{2}$ | $s\left(1+{e}^{2}\right)$ |
| q-104728 | `4c402c1d-d0dd-5148-a3d3-ef8f8ca1b754` | `741bc569-8dcc-54a7-93f1-c3d9b892adc0` | False | ${e}^{{\pi }^{2}+1}$ | $s\left({e}^{{\pi }^{2}+1}\right)$ |
| q-104728 | `4c402c1d-d0dd-5148-a3d3-ef8f8ca1b754` | `76597f8f-a721-552f-bc46-44e414558f67` | True | $e({e}^{4{\pi }^{2}}-1)$ | $s\left(e({e}^{4{\pi }^{2}}-1)\right)$ |
| q-104728 | `4c402c1d-d0dd-5148-a3d3-ef8f8ca1b754` | `a05094d0-34c2-5de5-a965-8a05daab4caa` | False | ${e}^{4\pi }$ | $s\left({e}^{4\pi }\right)$ |
| q-104728 | `4c402c1d-d0dd-5148-a3d3-ef8f8ca1b754` | `a811fdf6-0ca8-5ba9-9b33-e28fa7b6d1c2` | False | $0$ | $s\left(0\right)$ |
| q-104728 | `4c402c1d-d0dd-5148-a3d3-ef8f8ca1b754` | `dbca776b-42f8-568c-8d08-0e204fad75f7` | False | $e({e}^{2\pi }-1)$ | $s\left(e({e}^{2\pi }-1)\right)$ |
| q-104731 | `e8418831-a814-5787-ba6f-30266ff0bc9a` | `1fb1fd90-967a-508f-964a-ddcc8ad1fec6` | False | $12$ | $s\left(12\right)$ |
| q-104731 | `e8418831-a814-5787-ba6f-30266ff0bc9a` | `38d3c833-662c-50cc-95fd-d02f93ab6c89` | False | $48$ | $s\left(48\right)$ |
| q-104731 | `e8418831-a814-5787-ba6f-30266ff0bc9a` | `780f23b5-b5bf-596a-b047-13dbffe326e2` | False | $0$ | $s\left(0\right)$ |
| q-104731 | `e8418831-a814-5787-ba6f-30266ff0bc9a` | `c5aaa345-119e-5e65-bc94-2528387dcd96` | True | $36$ | $s\left(36\right)$ |
| q-104731 | `e8418831-a814-5787-ba6f-30266ff0bc9a` | `de389670-0e34-52aa-9dc2-f2ea5b75eb5d` | False | $24$ | $s\left(24\right)$ |
| q-104733 | `6a6c211e-df9c-57af-8d94-442d4251996d` | `30453404-690a-5b85-850f-9aaa09a4efe2` | True | $9{ln}^{3}⁡2-12\operatorname{ln}⁡2+21$ | $s\left(9{ln}^{3}⁡2-12\operatorname{ln}⁡2+21\right)$ |
| q-104733 | `6a6c211e-df9c-57af-8d94-442d4251996d` | `35cdd507-7f75-51ad-acf4-534f3b62ea96` | False | ${ln}^{2}⁡2+9$ | $s\left({ln}^{2}⁡2+9\right)$ |
| q-104733 | `6a6c211e-df9c-57af-8d94-442d4251996d` | `58c144e5-2b4f-5201-b0bb-e144657253c7` | False | ${ln}^{3}⁡2-63$ | $s\left({ln}^{3}⁡2-63\right)$ |
| q-104733 | `6a6c211e-df9c-57af-8d94-442d4251996d` | `da6b93e1-2f2d-5dd2-9235-e2c75c2150c5` | False | ${ln}^{3}⁡2+\operatorname{ln}⁡2-9$ | $s\left({ln}^{3}⁡2+\operatorname{ln}⁡2-9\right)$ |
| q-104733 | `6a6c211e-df9c-57af-8d94-442d4251996d` | `e08284d3-5a39-5136-ad35-3aadf74bdc85` | False | $0$ | $s\left(0\right)$ |
| q-104739 | `58ef2ea0-0a2c-50ba-bcc4-0d5182b81264` | `1ab61eea-ba71-5224-bbe8-eca2df0fe157` | True | ${e}^{{\pi }^{2}}-1$ | $s\left({e}^{{\pi }^{2}}-1\right)$ |
| q-104739 | `58ef2ea0-0a2c-50ba-bcc4-0d5182b81264` | `4b0e41b7-21e7-573e-b5d2-f356608a6ae5` | False | ${e}^{\pi -1}$ | $s\left({e}^{\pi -1}\right)$ |
| q-104739 | `58ef2ea0-0a2c-50ba-bcc4-0d5182b81264` | `ace99781-1604-53b3-b08e-f26c241a358f` | False | ${\pi }^{2}$ | $s\left({\pi }^{2}\right)$ |
| q-104739 | `58ef2ea0-0a2c-50ba-bcc4-0d5182b81264` | `c2892dd7-dcc3-567c-8bcb-ac89416a6e15` | False | ${e}^{2}+\pi $ | $s\left({e}^{2}+\pi \right)$ |
| q-104739 | `58ef2ea0-0a2c-50ba-bcc4-0d5182b81264` | `e7de7023-d488-540d-962c-5b17cc9d176b` | False | $0$ | $s\left(0\right)$ |
| q-104745 | `6ed60cbe-d21d-5310-989e-903acd1a44f7` | `16f31b92-c386-50b2-b977-d94225bcfbc5` | False | ${e}^{\pi }+1$ | $s\left({e}^{\pi }+1\right)$ |
| q-104745 | `6ed60cbe-d21d-5310-989e-903acd1a44f7` | `465fbdf4-7176-5e2a-afb9-7055988a9594` | False | ${e}^{{\pi }^{2}-1}$ | $s\left({e}^{{\pi }^{2}-1}\right)$ |
| q-104745 | `6ed60cbe-d21d-5310-989e-903acd1a44f7` | `54e54a33-5402-591a-ac33-570a9653db6c` | True | $\pi {e}^{\pi -1}$ | $s\left(\pi {e}^{\pi -1}\right)$ |
| q-104745 | `6ed60cbe-d21d-5310-989e-903acd1a44f7` | `796fc17c-d543-5b01-83ae-f85bfdb65ad5` | False | $2\pi $ | $s\left(2\pi \right)$ |
| q-104745 | `6ed60cbe-d21d-5310-989e-903acd1a44f7` | `dfd66caa-a9be-51dd-a8aa-57947da3bed9` | False | ${\pi }^{2}+1$ | $s\left({\pi }^{2}+1\right)$ |
| q-104747 | `7afbb94e-3c3c-582d-befe-a39fc2c5fb10` | `03d4147a-c71a-5c94-85e5-f5d9a8038924` | False | $\operatorname{sin}⁡2\operatorname{sin}⁡(e-1)$ | $s\left(\operatorname{sin}⁡2\operatorname{sin}⁡(e-1)\right)$ |
| q-104747 | `7afbb94e-3c3c-582d-befe-a39fc2c5fb10` | `27bb17e7-e9f0-57ab-a950-9c30d0a83e5a` | False | $\operatorname{sin}⁡e-\operatorname{sin}⁡2$ | $s\left(\operatorname{sin}⁡e-\operatorname{sin}⁡2\right)$ |
| q-104747 | `7afbb94e-3c3c-582d-befe-a39fc2c5fb10` | `5d7a11a7-e4b9-5d99-a4e6-6b05e88774ae` | True | $\operatorname{sin}⁡e$ | $s\left(\operatorname{sin}⁡e\right)$ |
| q-104747 | `7afbb94e-3c3c-582d-befe-a39fc2c5fb10` | `6d475b88-50f1-508c-94ec-f40b5b005181` | False | $2\operatorname{sin}⁡e-1$ | $s\left(2\operatorname{sin}⁡e-1\right)$ |
| q-104747 | `7afbb94e-3c3c-582d-befe-a39fc2c5fb10` | `e3f3259a-1dbd-5b91-9075-78bd6e17f1dd` | False | $\operatorname{sin}⁡2e-\operatorname{sin}⁡{e}^{2}$ | $s\left(\operatorname{sin}⁡2e-\operatorname{sin}⁡{e}^{2}\right)$ |
| q-104761 | `61dfdacb-ab42-5b45-8340-88f93ef0c7b8` | `28b3b744-39b6-57dd-83b1-ca255a0e5591` | False | $1-\operatorname{ln}⁡2$ | $s\left(1-\operatorname{ln}⁡2\right)$ |
| q-104761 | `61dfdacb-ab42-5b45-8340-88f93ef0c7b8` | `9d7d66b3-3253-501c-9d23-d0a00aa17af4` | True | $\frac{1}{2}+{ln}^{2}⁡2$ | $s\left(\frac{1}{2}+{ln}^{2}⁡2\right)$ |
| q-104761 | `61dfdacb-ab42-5b45-8340-88f93ef0c7b8` | `b2a48cb6-3488-5f91-a510-56e98f26b7eb` | False | $1+{ln}^{2}⁡3$ | $s\left(1+{ln}^{2}⁡3\right)$ |
| q-104761 | `61dfdacb-ab42-5b45-8340-88f93ef0c7b8` | `d222d7af-bcc2-54b0-bd8f-b14855923fe3` | False | $\frac{{ln}^{2}⁡2}{3}$ | $s\left(\frac{{ln}^{2}⁡2}{3}\right)$ |
| q-104761 | `61dfdacb-ab42-5b45-8340-88f93ef0c7b8` | `f773a812-93fa-544d-b4f9-b7fcdc706cd6` | False | $\frac{1}{2}+\operatorname{ln}⁡3$ | $s\left(\frac{1}{2}+\operatorname{ln}⁡3\right)$ |
| q-104764 | `49f3d66e-e3ad-5896-806b-677f9fc2a9bb` | `2652d9ba-683c-5862-9cda-3f3daeece5c9` | False | $3{e}^{2}-1$ | $s\left(3{e}^{2}-1\right)$ |
| q-104764 | `49f3d66e-e3ad-5896-806b-677f9fc2a9bb` | `61cedf07-823b-5fcb-9c03-378f9a5536db` | False | $3(e+3)$ | $s\left(3(e+3)\right)$ |
| q-104764 | `49f3d66e-e3ad-5896-806b-677f9fc2a9bb` | `7ec9781a-d4b2-5ee0-add1-074981a33f38` | False | ${e}^{2}+27$ | $s\left({e}^{2}+27\right)$ |
| q-104764 | `49f3d66e-e3ad-5896-806b-677f9fc2a9bb` | `9fa1d769-7e7e-5880-bb59-e10f4d9e33b0` | False | $9(3e-1)$ | $s\left(9(3e-1)\right)$ |
| q-104764 | `49f3d66e-e3ad-5896-806b-677f9fc2a9bb` | `d3b4b0e5-c5b9-5c22-abf0-49ca0a07f26b` | True | $3({e}^{2}+9)$ | $s\left(3({e}^{2}+9)\right)$ |
| q-104732 | `4c9c0c78-b891-5f32-8dca-852634763b9b` | `29a72800-4e23-513e-92c2-5437578df2cf` | True | $\frac{2\sqrt{2}+\pi }{4}$ | $s\left(\frac{2\sqrt{2}+\pi }{4}\right)$ |
| q-104732 | `4c9c0c78-b891-5f32-8dca-852634763b9b` | `62d13908-df4e-538d-9943-7c76652cbac9` | False | $\frac{2\sqrt{2}-\pi }{2}$ | $s\left(\frac{2\sqrt{2}-\pi }{2}\right)$ |
| q-104732 | `4c9c0c78-b891-5f32-8dca-852634763b9b` | `aad335b1-b4de-568f-b2e2-0f2fa5a05048` | False | $\frac{\sqrt{2}}{2}$ | $s\left(\frac{\sqrt{2}}{2}\right)$ |
| q-104732 | `4c9c0c78-b891-5f32-8dca-852634763b9b` | `b5a24286-6aba-57bd-af78-4a37875e9372` | False | $0$ | $s\left(0\right)$ |
| q-104732 | `4c9c0c78-b891-5f32-8dca-852634763b9b` | `c1ede2a6-76f1-5387-b6b8-e8fb84166eba` | False | $\frac{\sqrt{2}}{2}+1$ | $s\left(\frac{\sqrt{2}}{2}+1\right)$ |

## 4. Reusable templates and workload bounds

Fixed parts: source prose, theorem, reconstruction instructions, constant-C explanation, endpoint wording, one worked solution independent of selected option, field layout and option count. Variable parts are complete field components, complete potential, complete path components/interval, cross derivative (hard only), endpoint coordinate tuples and arithmetic rows. Inline endpoint prose uses a whole-sentence mask; no arbitrary short-expression substitution occurs. Standard TeX replaces the source Unicode invisible function-application and underbrace glyphs; this normalization is reported separately from prose/sequence fidelity.

Final arithmetic uses separate per-family masks: ordered uncomputed substitution; then simplified endpoint values for one-term potentials, uncollected term evaluations for cubic/exponential and separated-cubic potentials, grouped zero contributions for the hard sine/exponential potentials, retained trig factors for sin(x)sin(y), and distributed then collected arithmetic for the radical-path source. Original row counts and operation stages are retained at changed parameters. Final collection/factorization occurs only in the last row.

| Template | Level | Explicit sampling bounds | Substantive endpoint arithmetic |
|---|---|---|---|
| easy_product | easy | `{"a": [-3, 3], "h": [-2, 2], "k": [-2, 2], "r": [1, 2]}` | 2 full potential-term substitutions across two endpoints |
| easy_separable | easy | `{"a": [1, 3], "b": [1, 3], "h": [-2, 2], "k": [-2, 2], "r": [1, 2]}` | 4 full potential-term substitutions across two endpoints |
| quartic_trig | moderate | `{"a": [-3, 3], "r": [1, 3]}` | 2 full potential-term substitutions across two endpoints |
| cubic_exponential | moderate | `{"a": [-3, 3], "b": [-3, 3], "c": [1, 3], "r": [1, 2]}` | 6 full potential-term substitutions across two endpoints |
| exponential_cosine | moderate | `{"a": [-3, 3], "h": [1, 3], "n": [1, 2]}` | 2 full potential-term substitutions across two endpoints |
| cubic_product | moderate | `{"a": [-3, 3], "b": [-3, 3], "h": [1, 2], "r": [1, 3], "u": [1, 2]}` | 4 full potential-term substitutions across two endpoints |
| separable_cubic | moderate | `{"a": [-3, 3], "b": [-3, 3], "c": [1, 3], "r": [1, 3], "u": [2, 3]}` | 6 full potential-term substitutions across two endpoints |
| cosine_product | moderate | `{"a": [-3, 3], "b": [-3, 3], "n": [1, 3], "r": [1, 3]}` | 4 full potential-term substitutions across two endpoints |
| radial_log | hard | `{"a": [-3, 3], "h": [1, 3], "k": [1, 3]}` | 2 full potential-term substitutions across two endpoints |
| sine_exponential | hard | `{"a": [-3, 3], "b": [-3, 3], "k": [1, 3]}` | 4 full potential-term substitutions across two endpoints |
| mixed_exponential | hard | `{"a": [-3, 3], "b": [-3, 3], "k": [1, 3]}` | 4 full potential-term substitutions across two endpoints |
| sine_product | hard | `{"a": [-3, 3], "k": [1, 3]}` | 2 full potential-term substitutions across two endpoints |
| negative_exponential | hard | `{"a": [-3, 3], "b": [-3, 3], "h": [1, 3]}` | 4 full potential-term substitutions across two endpoints |
| cubic_radical_path | hard | `{"a": [-3, 3], "b": [-3, 3], "n": [1, 2]}` | 4 full potential-term substitutions across two endpoints |

All a,b,c coefficients are nonzero; signed absolute magnitudes are at most 3. Easy uses integer endpoints, one product term or two uncoupled quadratic terms. Moderate keeps the observed powers/potential families and at most three terms, with original familiar trig/log/exp endpoints. Hard keeps at most two potential terms (or the radial logarithm), equal continuous mixed partials on R², and the original path complexity. The radical-path n=1,2 makes both endpoint radicands perfect squares; logarithmic path arguments are positive over the full interval.

The easy scope is authored because no practice source has an easy label. It is anchored to canonical e-8760, the actual lesson route and the Calculating Potential Functions prerequisite: reconstruct a simple potential before subtracting values at a supplied linear path’s endpoints. Both easy templates require the KP-defining reconstruction. There is no conservative-existence check or new branch at easy.

Default complete authored bank: I; −I (reverse endpoints); 2I (double every coefficient while reconstructing f); I/2 (halve every coefficient while reconstructing f); 0 (subtract the same endpoint value twice). These are explicit full operations on the reconstructed potential/endpoints. Reject the entire instance if any member is equivalent; with this bank that means I=0. No first-valid recipe pool, source-choice sampling or learner-facing error diagnosis is used.

Source profiles fix relative parameters; authored defaults independently vary coefficients/path parameters with s=1, also enforced on explicit input. The canonical mathematical fingerprint uses the displayed field and ordered endpoints, omitting banks/profiles and curve parameters that cannot affect endpoints; the full presentation identity includes version, level, exact prompt, fixed solution, entire bank and domain. Easy zero-result paths and any other zero-result instance are rejected with their entire bank; explicit invalid inputs raise rather than resample.

### Source errors and repairs

- q-104747: r(0)=⟨0,2⟩ is correct, but the next prose sentence says (0,0). The path y=exp(sin x)+cos x gives y(0)=2. Generated prose uses (0,2). The final f(0,2) and bank are already correct.
- q-104764: endpoints/substitution correctly use (0,−e), but the symbolic final f subtraction says f(0,e). The path y=x²−exp(sqrt(x+1)) gives y(0)=−e. Generated subtraction uses f(0,−e). Numerically both evaluate to zero because x=0; this does not make the incorrect coordinate acceptable.

No options or correct designations are erroneous. Exact unrepaired endpoint solution denominator is 10/12, repaired solution denominator is 2/12; complete bank/value/designation fidelity remains 12/12. Original raw errors remain in source.json, source-cases.json and original review sections.
