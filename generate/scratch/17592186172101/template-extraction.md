# Template extraction and complete choice mapping

All exact source prompts, worked solutions, field identities/keys/types, correct values, every choice and image reference are retained in source.json and reference/initial/kp.edn. DATA in the script gives the complete formulas and bounds for every source. No source choice is omitted.

Backbone: supplied planar vector field; fixed axis-aligned rectangle; requested outward boundary flux; one radio selection. Solution stages: state flux form of Green, show region diagram, identify P and Q, compute P_x and Q_y, state D, set up divergence double integral, integrate x, substitute x limits, integrate y, substitute y limits, give scalar flux. Generated solutions retain the source theorem/diagram prefix and these concrete stages; intermediate simplifications use SymPy notation. Source replay separately preserves all literal source wording.

One variable slot: common positive scale k in {2,3,4,5}; k=1 is reserved for exact source replay. Components expand kP and kQ; every derivative, integrand, primitive, limit substitution and answer changes from this instance. Changing sign, powers, operators, function type, rectangle bounds, vertex identities, field count or response shape is outside this package. Geometry is fixed as a conservative sampling policy for verified asset reuse, not an intrinsic restriction of rectangle flux. Common scaling is an explicitly inferred same-method extension; only k=1 is observed. No cosmetic change of a divergence-free term counts as a distinct task. Fingerprint is expanded divergence plus rectangle bounds, ignoring seed, choice order, prose, identity and inert functions.

## Source bank profiles

Each bank recipe is the complete mathematical source value multiplied by k. These are exact algebraic value patterns, not asserted learner misconceptions. Opaque e-containing distractors stay opaque. This deliberately narrow linear scaling extension preserves the full observed bank rather than pooling or inventing error operations. Nonzero k preserves pairwise inequivalence; the validator checks the complete bank for every allowed k. Source bank replay compares all five values and the key as well as exact text.

### q-126820

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨{e}^{y}+2{x}^{2}y,\,{e}^{x}+2x{y}^{2}⟩
$$

through the boundary of the rectangle with vertices $(-1,0),(2,0),(2,1),$ and $(-1,1).$

| Source choice UUID | Exact value | Recipe | Correct |
|---|---|---|---|
| 18e2ed19-98ac-5bcb-a221-0caee13960fb | `2` | `k * (2)` | False |
| 337fdb38-6a77-58a2-a8ba-0427000097ef | `10` | `k * (10)` | False |
| bc81f5e4-801a-52a8-8bc4-b60b5b28c7ee | `4` | `k * (4)` | False |
| cb3c1ff6-71eb-5c98-bf53-9f9db4823148 | `6` | `k * (6)` | True |
| cf0dfe85-b143-550c-becd-1c76a74d08ea | `8` | `k * (8)` | False |
### q-126821

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨\operatorname{cos}⁡(\pi y)-{x}^{2},\,\operatorname{sin}⁡(\pi x)+2y⟩
$$

through the boundary of the square $0\le x\le 1,0\le y\le 1.$

| Source choice UUID | Exact value | Recipe | Correct |
|---|---|---|---|
| d24203b1-5e2d-543b-b875-84082292041c | `1` | `k * (1)` | True |
| 12450fac-5904-57a0-92e2-bc8a3468008b | `4` | `k * (4)` | False |
| 23c8d906-57d9-5dfc-98ed-afb30ba1cec2 | `0` | `k * (0)` | False |
| 58920047-051c-5179-a311-88f110077114 | `2\sqrt{2}` | `k * (2*sqrt(2))` | False |
| 5d55495b-d3c0-5a44-b16e-2735230596b3 | `\frac{1}{2}` | `k * (1/2)` | False |
### q-127303

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨\operatorname{sin}⁡y+2x,\,{x}^{5}-3y⟩
$$

through the boundary of the square $-1\le x\le 1,-1\le y\le 1.$

| Source choice UUID | Exact value | Recipe | Correct |
|---|---|---|---|
| 3f014674-85e2-5712-94fa-a1a4f4088850 | `4` | `k * (4)` | False |
| 540fd8b7-839b-5252-8a65-5ad6720e3081 | `8` | `k * (8)` | False |
| 69707d0e-2e50-52a2-a276-f84bd14a62a0 | `2` | `k * (2)` | False |
| dfb13e75-d527-5698-b332-2b8a249bc796 | `-4` | `k * (-4)` | True |
| fc605dab-f873-5fb2-8c9e-b56b75167414 | `-2` | `k * (-2)` | False |
### q-127308

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨\operatorname{cos}⁡y-3{x}^{3},\,x{e}^{x}-4x{y}^{3}⟩
$$

through the boundary of the rectangle $-1\le x\le 1,0\le y\le 1.$

| Source choice UUID | Exact value | Recipe | Correct |
|---|---|---|---|
| 21de3cf7-4b55-5b4f-ab6a-375c5a7d25e7 | `-6` | `k * (-6)` | True |
| a2335fe5-8b47-5e4b-835b-e3b58b0f5ed5 | `e-6` | `k * (-6 + E)` | False |
| ba1ad8f1-09f9-5de7-ba25-01fe8f576f3c | `-3` | `k * (-3)` | False |
| c26a51aa-0eb7-55e1-8247-693120014201 | `-12` | `k * (-12)` | False |
| f5911c8b-0c20-5a8d-91de-79dbd76c58cd | `-5` | `k * (-5)` | False |
### q-127322

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨\sqrt[3]{y}+x,\,\operatorname{sin}⁡x-3{x}^{2}{y}^{2}⟩
$$

through the boundary of the rectangle with vertices $(0,0),(2,0),(2,1),$ and $(0,1).$

| Source choice UUID | Exact value | Recipe | Correct |
|---|---|---|---|
| 08ef51b5-bef5-548c-8f51-a79f305af85b | `6` | `k * (6)` | False |
| 80081f79-d17b-5546-ab52-2540982bd374 | `-3` | `k * (-3)` | False |
| 806a70e6-fd99-58c6-a425-5c06d2336cd7 | `12` | `k * (12)` | False |
| ef1969e2-dc11-53e4-a52a-96db98443bc3 | `-6` | `k * (-6)` | True |
| ffc96c67-0441-581c-839f-b9e98cb25a8c | `-2` | `k * (-2)` | False |
### q-127324

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨\operatorname{sin}⁡(2y)-y{x}^{2},\,\operatorname{cos}⁡(2x)+2xy⟩
$$

through the boundary of the square with vertices $(0,-1),(1,-1),(1,0),$ and $(0,0).$

| Source choice UUID | Exact value | Recipe | Correct |
|---|---|---|---|
| 1d2058c9-6db4-581f-a065-7bb1cf07c556 | `-\frac{3}{2}` | `k * (-3/2)` | False |
| 2b8b210e-ceef-5d7e-a20b-9a79b427549e | `\frac{1}{2}` | `k * (1/2)` | False |
| be97a3e0-af5b-55f6-8a9d-668875533062 | `2` | `k * (2)` | False |
| bfa02f2a-4b5c-5f74-9d43-bc4fc65096f7 | `\frac{3}{2}` | `k * (3/2)` | True |
| cacc2a97-a4f6-538c-9ceb-91985ed7b814 | `-\frac{1}{2}` | `k * (-1/2)` | False |
### q-127305

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨{e}^{y}-4xy,\,\operatorname{cos}⁡x+2xy⟩
$$

through the boundary of the rectangle $-1\le x\le 1,-1\le y\le 0.$

| Source choice UUID | Exact value | Recipe | Correct |
|---|---|---|---|
| 072b4d5b-a518-50b1-9fd5-372915316f5c | `0` | `k * (0)` | False |
| 231a4e7e-143a-55ee-96ec-349dc902c4d0 | `8` | `k * (8)` | False |
| a888cc31-d112-55bf-8f2c-cc635b42c57e | `-8` | `k * (-8)` | False |
| e38494e3-564d-5089-a5ec-aa68869b4e33 | `4` | `k * (4)` | True |
| e4ef2656-ec3b-5442-90ba-703850ba3398 | `-4` | `k * (-4)` | False |
### q-127337

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨{y}^{7}-x,\,{e}^{3x}+x{y}^{2}⟩
$$

through the boundary of the rectangle with vertices $(-1,-1),(0,-1),(0,1),$ and $(-1,1).$

| Source choice UUID | Exact value | Recipe | Correct |
|---|---|---|---|
| 1afc0e4b-7ec3-5e04-a320-b09bbb7450d5 | `\frac{3}{2}` | `k * (3/2)` | False |
| 5ebdbb3a-9cd8-57c7-9768-3437a54bb5b2 | `2` | `k * (2)` | False |
| 783926e4-15e5-52ff-ad59-711ade6b214d | `-2` | `k * (-2)` | True |
| 9ceb053a-ae1f-53f2-9912-d9d9157552fa | `-\frac{3}{2}` | `k * (-3/2)` | False |
| db270bba-95df-51f5-b9d1-ccab96038132 | `-1` | `k * (-1)` | False |
### q-127326

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨y{e}^{y}-4xy,\,\operatorname{sin}⁡(\pi x)-4x{y}^{3}⟩
$$

through the boundary of the rectangle with vertices $(0,-1),(1,-1),(1,1),$ and $(0,1).$

| Source choice UUID | Exact value | Recipe | Correct |
|---|---|---|---|
| 036be383-69ad-5c54-97f4-245cc64ebdc5 | `8` | `k * (8)` | False |
| 84832c07-1cf7-5890-95f5-93379bbcf9e7 | `-2` | `k * (-2)` | False |
| a513c7fb-0fe0-56ce-955a-00f68e2e1226 | `2` | `k * (2)` | False |
| ac21a517-9ce2-51e1-a210-d1342e658153 | `-4` | `k * (-4)` | True |
| eb98dc31-4f54-5896-a0d6-e621b6d1e1f7 | `4` | `k * (4)` | False |
### q-127307

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨{y}^{2}+8x{y}^{3},\,{e}^{x}+2{y}^{2}⟩
$$

through the boundary of the square $-1\le x\le 0,0\le y\le 1.$

| Source choice UUID | Exact value | Recipe | Correct |
|---|---|---|---|
| 60eea807-02ce-5996-b952-62ec842109d3 | `e+4` | `k * (E + 4)` | False |
| 799a4193-8f0b-5d08-a4bf-2ba532ac8bb9 | `e+2` | `k * (2 + E)` | False |
| 7dd7d3e5-183d-50b2-bbd9-75b14c583ab6 | `0` | `k * (0)` | False |
| 974a14ee-cedf-5300-8d94-d8f4a66e99c1 | `2` | `k * (2)` | False |
| fbeea2e4-21f9-5c63-bc1c-d0e42e6ef742 | `4` | `k * (4)` | True |
