# Template extraction

## Stage 1 — specific source descriptions

All nine originals are preserved in source.json and displayed with their full worked solutions in review.md. The field is `selection`, radio, exactly five math fragments, no learner feedback. Easy prompts provide r_u×r_v and request only the missing integrand; moderate prompts give its monomial/exponential basis with unknown coefficients and request their sum. The following evidence accounts for every choice, without interpreting unknown numbers as proven errors.

### q-160839 / product_affine
Captured coefficients: `{'a': 1, 'b': 2, 'c': 1}`. F = `[x*z, 2*y, 1]`; r = `[u*v, u + v, 1 - v]`. Exact integrand = `u*v**2 + u*v - u + 2*v**2 + v`. Coefficient basis = `[u*v**2, v**2, u*v]`; required value = `4`.
Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨xz,\,2y,\,1⟩,\,r(u,v)=⟨uv,\,u+v,\,1-v⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}au{v}^{2}+b{v}^{2}+cuv-u+v\,\text{d}A
$$

what is the value of $a+b+c?$

Complete bank profile `observed` (one profile per template):

| Source field | Source exact option | Parameterized replay recipe | Correct | Interpretation |
|---|---|---|---|---|
| selection | `4` | `scale*(4)` | True | exact integrand/coefficient sum |
| selection | `2` | `scale*(2)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `5` | `scale*(5)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `8` | `scale*(8)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `3` | `scale*(3)` | False | observed expression pattern; underlying operation underdetermined |

### q-160840 / quadratic_cancel
Captured coefficients: `{'a': 2, 'b': 1, 'c': 2, 'd': 1, 'e': 1}`. F = `[2*x + y, 2*z, y + z]`; r = `[-u**2, 2*u**2 - v**2, v**2]`. Exact integrand = `8*u**3*v`. Coefficient basis = `None`; required value = `8*u**3*v`.
Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨2x+y,\,2z,\,y+z⟩,\,r(u,v)=⟨-{u}^{2},\,2{u}^{2}-{v}^{2},\,{v}^{2}⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

what is the missing expression?

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨8uv,\,4uv,\,4uv⟩.$*

Complete bank profile `observed` (one profile per template):

| Source field | Source exact option | Parameterized replay recipe | Correct | Interpretation |
|---|---|---|---|---|
| selection | `8u{v}^{3}+8{u}^{3}v` | `scale*(8*u*v**3+8*u**3*v)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `8u{v}^{3}` | `scale*(8*u*v**3)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `2u{v}^{3}+4{u}^{3}v` | `scale*(2*u*v**3+4*u**3*v)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `4u{v}^{3}+2{u}^{3}v` | `scale*(4*u*v**3+2*u**3*v)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `8{u}^{3}v` | `scale*(8*u**3*v)` | True | exact integrand/coefficient sum |

### q-161249 / quadratic_diagonal
Captured coefficients: `{'a': 2, 'b': 2, 'c': 1}`. F = `[2*x, 2*y, z]`; r = `[u**2, -u*v, v**2]`. Exact integrand = `2*u**2*v**2`. Coefficient basis = `None`; required value = `2*u**2*v**2`.
Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨2x,\,2y,\,z⟩,\,r(u,v)=⟨{u}^{2},\,-uv,\,{v}^{2}⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

what is the missing expression?

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-2{v}^{2},\,-4uv,\,-2{u}^{2}⟩.$*

Complete bank profile `observed` (one profile per template):

| Source field | Source exact option | Parameterized replay recipe | Correct | Interpretation |
|---|---|---|---|---|
| selection | `2{u}^{2}{v}^{2}` | `scale*(2*u**2*v**2)` | True | exact integrand/coefficient sum |
| selection | `{u}^{3}v+u{v}^{3}` | `scale*(u**3*v+u*v**3)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `-2{u}^{3}v-2u{v}^{3}` | `scale*(-2*u**3*v-2*u*v**3)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `6{u}^{2}{v}^{2}` | `scale*(6*u**2*v**2)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `{u}^{2}v-2{u}^{2}{v}^{2}+u{v}^{2}` | `scale*(u**2*v-2*u**2*v**2+u*v**2)` | False | observed expression pattern; underlying operation underdetermined |

### q-161303 / cubic_ruled
Captured coefficients: `{'a': 1, 'b': 2, 'c': 2, 'd': 3}`. F = `[1, 0, 2]`; r = `[u + v, u**2 + 2*v, u**3 + 3*v]`. Exact integrand = `-2*(u - 1)*(3*u + 2)`. Coefficient basis = `[u**2, u, 1]`; required value = `0`.
Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨1,\,0,\,2⟩,\,r(u,v)=⟨u+v,\,{u}^{2}+2v,\,{u}^{3}+3v⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}a{u}^{2}+bu+c\,\text{d}A
$$

what is the value of $a+b+c?$

Complete bank profile `observed` (one profile per template):

| Source field | Source exact option | Parameterized replay recipe | Correct | Interpretation |
|---|---|---|---|---|
| selection | `4` | `scale*(4)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `-2` | `scale*(-2)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `0` | `scale*(0)` | True | exact integrand/coefficient sum |
| selection | `-4` | `scale*(-4)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `2` | `scale*(2)` | False | observed expression pattern; underlying operation underdetermined |

### q-161306 / exponential_sum
Captured coefficients: `{'a': 1, 'b': 1, 'k': 1}`. F = `[x - 1/z, y + 1/z, z]`; r = `[u*exp(v), u*exp(-v), u]`. Exact integrand = `(exp(v) - 1)*(exp(v) + 1)*exp(-v)`. Coefficient basis = `[exp(v), exp(-v)]`; required value = `0`.
Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨x-\frac{1}{z},\,y+\frac{1}{z},\,z⟩,\,r(u,v)=⟨u{e}^{v},\,u{e}^{-v},\,u⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}a{e}^{v}+b{e}^{-v}\,\text{d}A
$$

what is the value of $a+b?$

Complete bank profile `observed` (one profile per template):

| Source field | Source exact option | Parameterized replay recipe | Correct | Interpretation |
|---|---|---|---|---|
| selection | `-2` | `scale*(-2)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `-1` | `scale*(-1)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `0` | `scale*(0)` | True | exact integrand/coefficient sum |
| selection | `1` | `scale*(1)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `2` | `scale*(2)` | False | observed expression pattern; underlying operation underdetermined |

### q-161384 / ruled_square
Captured coefficients: `{'a': 1, 'b': 1, 'c': 1}`. F = `[z**2, y**2, x]`; r = `[u**2, v, u]`. Exact integrand = `u**2*(2*u - 1)`. Coefficient basis = `None`; required value = `u**2*(2*u - 1)`.
Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨{z}^{2},\,{y}^{2},\,x⟩,\,r(u,v)=⟨{u}^{2},\,v,\,u⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

what is the missing expression?

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,0,\,2u⟩.$*

Complete bank profile `observed` (one profile per template):

| Source field | Source exact option | Parameterized replay recipe | Correct | Interpretation |
|---|---|---|---|---|
| selection | `2{u}^{2}` | `scale*(2*u**2)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `u{v}^{2}-2{v}^{3}` | `scale*(u*v**2-2*v**3)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `2{u}^{2}+uv` | `scale*(2*u**2+u*v)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `{u}^{2}-{v}^{2}` | `scale*(u**2-v**2)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `2{u}^{3}-{u}^{2}` | `scale*(2*u**3-u**2)` | True | exact integrand/coefficient sum |

### q-161251 / polar_hint
Captured coefficients: `{'a': 3, 'b': 3, 'c': 1, 'h': 1}`. F = `[3*x, 3*y, z]`; r = `[u*cos(v), u*sin(v), u**2]`. Exact integrand = `-5*u**3`. Coefficient basis = `None`; required value = `-5*u**3`.
Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨3x,\,3y,\,z⟩,\,r(u,v)=⟨u\operatorname{cos}⁡v,\,u\operatorname{sin}⁡v,\,{u}^{2}⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

what is the missing expression?

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-2{u}^{2}\operatorname{cos}⁡v,\,-2{u}^{2}\operatorname{sin}⁡v,\,u⟩.$*

Complete bank profile `observed` (one profile per template):

| Source field | Source exact option | Parameterized replay recipe | Correct | Interpretation |
|---|---|---|---|---|
| selection | `6{u}^{3}` | `scale*(6*u**3)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `{u}^{3}\operatorname{sin}⁡v\operatorname{cos}⁡v` | `scale*(u**3*sin(v)*cos(v))` | False | observed expression pattern; underlying operation underdetermined |
| selection | `2{u}^{2}\operatorname{sin}⁡v\operatorname{cos}⁡v` | `scale*(2*u**2*sin(v)*cos(v))` | False | observed expression pattern; underlying operation underdetermined |
| selection | `-5{u}^{3}` | `scale*(-5*u**3)` | True | exact integrand/coefficient sum |
| selection | `-3{u}^{2}` | `scale*(-3*u**2)` | False | observed expression pattern; underlying operation underdetermined |

### q-161383 / bilinear_hint
Captured coefficients: `{'a': 1, 'b': 1, 'c': 1}`. F = `[x*z, y, x*z]`; r = `[u, u*v, v]`. Exact integrand = `u*v*(u + v - 1)`. Coefficient basis = `None`; required value = `u*v*(u + v - 1)`.
Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨xz,\,y,\,xz⟩,\,r(u,v)=⟨u,\,uv,\,v⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

what is the missing expression?

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨v,\,-1,\,u⟩.$*

Complete bank profile `observed` (one profile per template):

| Source field | Source exact option | Parameterized replay recipe | Correct | Interpretation |
|---|---|---|---|---|
| selection | `{u}^{2}v` | `scale*(u**2*v)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `u{v}^{2}-{u}^{2}v` | `scale*(u*v**2-u**2*v)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `{u}^{2}{v}^{2}-2uv` | `scale*(u**2*v**2-2*u*v)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `u{v}^{2}+uv+2{u}^{2}v` | `scale*(u*v**2+u*v+2*u**2*v)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `u{v}^{2}-uv+{u}^{2}v` | `scale*(u*v**2-u*v+u**2*v)` | True | exact integrand/coefficient sum |

### q-161304 / graph_sum
Captured coefficients: `{'a': 1, 'b': 1, 'c': 1, 'h': 2}`. F = `[x**2, x*y, z]`; r = `[u, v, 2*u*v]`. Exact integrand = `-2*u*v*(2*u - 1)`. Coefficient basis = `[u*v, u**2*v]`; required value = `-2`.
Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨{x}^{2},\,xy,\,z⟩,\,r(u,v)=⟨u,\,v,\,2uv⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}auv+b{u}^{2}v\,\text{d}A
$$

what is the value of $a+b?$

Complete bank profile `observed` (one profile per template):

| Source field | Source exact option | Parameterized replay recipe | Correct | Interpretation |
|---|---|---|---|---|
| selection | `3` | `scale*(3)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `-2` | `scale*(-2)` | True | exact integrand/coefficient sum |
| selection | `-4` | `scale*(-4)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `0` | `scale*(0)` | False | observed expression pattern; underlying operation underdetermined |
| selection | `1` | `scale*(1)` | False | observed expression pattern; underlying operation underdetermined |

## Stage 2 — generalized descriptions

Easy: substitute the three coordinate expressions into the vector field and dot with the supplied ordered fundamental vector product. Moderate: differentiate r with respect to u and v, form r_u×r_v, substitute into F, dot, collect the displayed coefficients, and add them. No region bounds or evaluation are requested. Every family is another application at the same level, not an instructional progression.

## Stage 3 — components and banks

The tables above map every original value to its source field, captured coefficients and whole bank profile. Correct values are derived first from exact mathematics. Complete observed banks are homogeneously extended only when F is uniformly scaled and all original parameter ratios remain fixed. This preserves the mathematical expression patterns but does not recover original distractor authoring code or intent. Especially scalar moderate options are underdetermined; no numerical fitting or unrelated perturbation is promoted to a default. Defaults instead use complete authored banks based on reversing the ordered cross product, cofactor sign mistakes, omitted substitution, adding vector components, or using a tangent instead of the cross product. For moderate scalar answers, the same displayed coefficient-sum projection is applied after the wrong integral operation; any extra terms are discarded by that explicit compound-error recipe. See authored_bank and coefficient_value in the script for exact operation sequences. Each named tuple is chosen whole before sampling; an equivalence collision rejects the entire instance.

## Stage 4 — reusable templates, constraints and calculations

Fixed: original introductory/flux/hint/coefficient-question sentences, a single selection field, five expression fragments, original shared worked-solution sentences and stages. Variable: independent bounded positive integer field coefficients 1..4 by default (explicit 1..6), bounded existing surface coefficients, and uniform scale 1..4 for observed profiles. Optional/conditional: easy hint and supplied-cross stage versus moderate/hard tangent derivative, determinant and signed-minor stages; coefficient conclusion for moderate only. Symbolic substitution, exact tangent vectors, signed cross-product minors, component products, simplified integrand, basis coefficients and coefficient sum all derive from one instance. No plot metadata enters learner text. Seeds only sample and reorder; fixed objects and complete bank preserve content identity. Different displayed banks change identity and retain a separate parameter fingerprint.

### Missing hard rationale

There are no observed hard questions. The canonical e-12355 already teaches the unhinted derivative→cross→substitute→dot route; moderate q-161306 supplies reciprocal/exponential arithmetic and easy q-161251 supplies polar/trigonometric coordinates and the sin²+cos² identity. The introduction derives exactly the ordered r_u×r_v formula, with prerequisites Flux in Three-Dimensional Vector Fields (3178) and Surface Integrals Over Parametric Surfaces (3386). Two authored hard families retain that route with all three dot-product components active: polar_unhinted keeps unequal bounded radial field coefficients, so the Pythagorean identity leaves a nonconstant sin² term; exponential_unhinted keeps a bounded nonzero u² term alongside exp(v) and exp(-v). Both require the same fixed workload, with no ordering between families. No reverse-orientation instructions, integration limits, or evaluating flux (the next sibling KP) are added. This is a supported design claim, not an observed difficulty label.

### Source-format and domain repairs

Originals omit regular-domain restrictions. Generated exponential questions explicitly use u>0 so z=u and reciprocal components exist. Polar questions use u>0, 0<v<2π so the parametrization is regular and avoids angular overlap. Quadratic hinted questions use u>0,v>0 to avoid zero fundamental products. The cubic-ruled parametrization is singular at u=c/2 when 4d=3c² (including original c=2,d=3 at u=1); generated prompts explicitly exclude that value. Other source surface families are regular on the declared metadata domains. These restrictions narrow unspecified D without changing the original answers and are disclosed prompt repairs. q-161304 has a missing opening parenthesis in ∂(2uv)/∂u; the derivative renderer repairs it. Legacy Unicode angle brackets, prime placement, function application characters, and integral notation are normalized to standard LaTeX. Worked-solution sentences/stage sequence and exact intermediate math are preserved; generated rows standardize some original algebra grouping and add an explicit unsimplified substitution row. No source choices/designations are excluded or corrected; 45 values and nine correct designations are matched independently.