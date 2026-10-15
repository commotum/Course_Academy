# Template extraction

Evidence basis 2644, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Full originals, fields, exact strings, source IDs and solutions remain in reference/source.json and source.edn.

Every template requests outward flux of a specified planar field through x=a cos(t), y=b sin(t), 0<=t<2*pi. The curve is a simple ellipse, traversed once counterclockwise; this orientation makes P dy-Q dx outward flux. All axes are strictly positive, and no geometric plots are required. Fixed stages: flux definition/outward normal; x,y substitution; P,Q along the curve; x',y'; parameter integral; the source's trig identity or substitution; endpoint evaluation. One selection radio field with five exact mathematical values is fixed. The supplied objects, requested scalar, operation, degree, interval and response contract never vary.

## Slots and domain

The variable semiaxes a,b occur in the curve, component substitutions, derivatives, integral coefficients, substitution bounds and banks. Circle templates enforce b=a; the circle-to-ellipse change is not permitted there. Ellipse templates permit positive unequal semiaxes where their source bank needs unequal values. Radius 1 remains available for source replay/boundaries. Sampling uses integers 2..10, with validation accepting 1..12 and checking both boundaries. The coefficient k is variable only in the observed radial-linear and cross-cubic families. Sample k=2..9; accept 1..12. Other templates hold k=1 to preserve the source structure. No free point/cell/term target slots exist: the target is always the full-curve outward flux.

Observed values are listed per source below; wider ranges are conservative same-method generalizations. They change exact supplied data and the assessed integrals while retaining operation count and integration method. No label, choice-order or seed change creates a new task. Fingerprints further collapse alternate parameter sets giving the same integral in the same instructional backbone; exponential axis swaps are conservatively merged. No difficulty relabeling follows from larger coefficients.

## Profiles and recipes

A profile is selected before constructing its whole bank. These are complete observed algebraic banks, not a pool of interchangeable distractors. Signed-half uses correct C=2kab*pi and distractors -C,C/2,-C/2,0. Component-scale uses C=2kab*pi with kab*pi,ka*pi,kb*pi,0; require a,b>1 and a!=b. Cubic-scale uses correct 0 and ±2a^3*pi/3, ±4a^3*pi/3. Coefficient-scale uses 0, ±k/2, ±k. Area-scale uses 0, ±ab*pi/2, ±ab*pi. Axis-square-scale uses 0, ±e(a^2+b^2)/(ab), ±e(b^2-a^2)/(ab), requiring unequal axes >=2.

The numeric recipes for zero-answer banks reproduce the observed values exactly; the underlying learner mistakes are unresolved. Their scale formulas are explicitly inferred, conservative extensions, not asserted source psychology. Every wrong option remains provably distinct from zero and each other. The area-scale dependence on b and axis-square dependence on a,b are inferred from sparse evidence; retain exact observed values for replay and keep these bounds explicit. Reject any invalid/colliding bank as a whole.

## Per-source observations and complete mappings

### q-127055 / circle-linear / signed-half

Calculate the flux of the vector field $F(x,y)=(x+y)\,i+(y-x)\,j$ across the closed curve $C$ given by $r(t)=3\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Observed parameters: `{"a": 3, "b": 3, "k": 1}`. Field `dab28699-4fc7-5cb2-8f84-87f7666ba43c`, key `selection`, five radio choices. Component structure: P=x + y, Q=-x + y. One complete traversal, no shifts or singularities. Correct source value: `18\pi `.

| Source answer UUID | Exact source value | Recipe at these parameters | Correct |
|---|---|---|---|
| 0cfab73e-541e-5dea-a884-264b4bd8ec97 | `0` | signed-half[4] = `0` | False |
| 1d03d1d4-83e8-5434-ba88-654e772f6034 | `18\pi ` | signed-half[0] = `18 \pi` | True |
| 2bedcbb9-3a20-535c-92e0-bda037bb0531 | `-9\pi ` | signed-half[3] = `- 9 \pi` | False |
| 94ef6336-a885-5e0f-9339-fb9e597d51dc | `-18\pi ` | signed-half[1] = `- 18 \pi` | False |
| c61c8d76-f473-524c-b92c-3be06cc40c20 | `9\pi ` | signed-half[2] = `9 \pi` | False |

Original solution stages are retained in reference/source.json and compared with replay and a changed-radius variant in reference/side-by-side.md.

### q-127060 / cross-quadratic / cubic-scale

Calculate the flux of the vector field $F(x,y)=xy\,i+{x}^{2}\,j$ across the closed curve $C$ given by $r(t)=2\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Observed parameters: `{"a": 2, "b": 2, "k": 1}`. Field `473e948e-e7b1-5fb0-bd43-b3e933074eaa`, key `selection`, five radio choices. Component structure: P=x*y, Q=x**2. One complete traversal, no shifts or singularities. Correct source value: `0`.

| Source answer UUID | Exact source value | Recipe at these parameters | Correct |
|---|---|---|---|
| 1451c613-e020-5234-9207-ca8e2b426177 | `0` | cubic-scale[0] = `0` | True |
| 545e7de3-77c0-5001-a9e8-6b1adc5f1466 | `-\frac{16\pi }{3}` | cubic-scale[2] = `- \frac{16 \pi}{3}` | False |
| 78acc197-697f-5085-b977-43333a81c4c4 | `\frac{32\pi }{3}` | cubic-scale[3] = `\frac{32 \pi}{3}` | False |
| 7b79330c-376e-54f4-b1b3-7e784422cfed | `\frac{16\pi }{3}` | cubic-scale[1] = `\frac{16 \pi}{3}` | False |
| a87d06f4-05e6-5e25-a200-9da07f1daa38 | `-\frac{32\pi }{3}` | cubic-scale[4] = `- \frac{32 \pi}{3}` | False |

Original solution stages are retained in reference/source.json and compared with replay and a changed-radius variant in reference/side-by-side.md.

### q-127077 / radial-linear / signed-half

Calculate the flux of the vector field $F(x,y)=x\,i+y\,j$ across the closed curve $C$ given by $r(t)=5\operatorname{cos}⁡t\,i+6\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Observed parameters: `{"a": 5, "b": 6, "k": 1}`. Field `30577348-fd2b-554c-96e0-1728db3f4497`, key `selection`, five radio choices. Component structure: P=x, Q=y. One complete traversal, no shifts or singularities. Correct source value: `60\pi `.

| Source answer UUID | Exact source value | Recipe at these parameters | Correct |
|---|---|---|---|
| 2873f634-c695-583b-b477-95e3c1ffc07a | `-60\pi ` | signed-half[1] = `- 60 \pi` | False |
| 4babd7c8-f323-5126-a6c0-63a9f81a9e3a | `-30\pi ` | signed-half[3] = `- 30 \pi` | False |
| 66277e5d-0782-5296-aac5-7543f0ac4723 | `0` | signed-half[4] = `0` | False |
| 86598988-6527-5185-a16f-ee494f22fee7 | `30\pi ` | signed-half[2] = `30 \pi` | False |
| a6bc2f7b-8b39-5063-8765-91cf86585fbd | `60\pi ` | signed-half[0] = `60 \pi` | True |

Original solution stages are retained in reference/source.json and compared with replay and a changed-radius variant in reference/side-by-side.md.

### q-127081 / cross-cubic / coefficient-scale

Calculate the flux of the vector field $F(x,y)=y\,i+9{x}^{3}\,j$ across the closed curve $C$ given by $r(t)=\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Observed parameters: `{"a": 1, "b": 3, "k": 9}`. Field `b00b1074-3f5c-50fa-8cd5-1bc5332b0ac4`, key `selection`, five radio choices. Component structure: P=y, Q=9*x**3. One complete traversal, no shifts or singularities. Correct source value: `0`.

| Source answer UUID | Exact source value | Recipe at these parameters | Correct |
|---|---|---|---|
| 2b2ab957-0579-5e99-8c2c-f53cec1a64ff | `-9` | coefficient-scale[4] = `-9` | False |
| 515d246a-bf62-5921-88e9-813966854ecc | `0` | coefficient-scale[0] = `0` | True |
| 681d213e-13d8-58eb-9b2e-feeb4d760e83 | `9` | coefficient-scale[3] = `9` | False |
| 787af263-8fcd-544e-a39d-804db798c96f | `\frac{9}{2}` | coefficient-scale[1] = `\frac{9}{2}` | False |
| 95210164-0d4e-5860-ac8f-9ab7e9038d97 | `-\frac{9}{2}` | coefficient-scale[2] = `- \frac{9}{2}` | False |

Original solution stages are retained in reference/source.json and compared with replay and a changed-radius variant in reference/side-by-side.md.

### q-127139 / square-constant / area-scale

Calculate the flux of the vector field $F(x,y)={x}^{2}\,i+j$ across the closed curve $C$ given by $r(t)=7\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Observed parameters: `{"a": 7, "b": 2, "k": 1}`. Field `b4fee625-b03f-59fc-b891-1aff5cd98622`, key `selection`, five radio choices. Component structure: P=x**2, Q=1. One complete traversal, no shifts or singularities. Correct source value: `0`.

| Source answer UUID | Exact source value | Recipe at these parameters | Correct |
|---|---|---|---|
| 6893a418-d322-5ab1-83ac-21e6380ffd8a | `-14\pi ` | area-scale[4] = `- 14 \pi` | False |
| 8d1a6f11-e4dc-58f0-b3b9-20f5896018bf | `14\pi ` | area-scale[3] = `14 \pi` | False |
| ad14b8d3-dc2a-51ae-93a4-3065094d2fff | `-7\pi ` | area-scale[2] = `- 7 \pi` | False |
| c8457952-5981-52f2-8dd0-d726a811dc80 | `7\pi ` | area-scale[1] = `7 \pi` | False |
| e9652b71-0ef3-57bb-b58d-c0c40977ff4e | `0` | area-scale[0] = `0` | True |

Original solution stages are retained in reference/source.json and compared with replay and a changed-radius variant in reference/side-by-side.md.

### q-127140 / radial-linear / component-scale

Calculate the flux of the vector field $F(x,y)=4x\,i+4y\,j$ across the closed curve $C$ given by $r(t)=8\operatorname{cos}⁡t\,i+6\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Observed parameters: `{"a": 8, "b": 6, "k": 4}`. Field `c2ba8e33-8924-5bcc-b848-378e5d728fa7`, key `selection`, five radio choices. Component structure: P=4*x, Q=4*y. One complete traversal, no shifts or singularities. Correct source value: `384\pi `.

| Source answer UUID | Exact source value | Recipe at these parameters | Correct |
|---|---|---|---|
| 8337cc5b-cbe0-5afa-9274-103e3f498697 | `24\pi ` | component-scale[3] = `24 \pi` | False |
| 8d8c2924-c012-51ca-aa9f-ebee29edb99a | `0` | component-scale[4] = `0` | False |
| 9958d4dc-9c0d-556d-9236-c69dc7ace6dc | `192\pi ` | component-scale[1] = `192 \pi` | False |
| 9c54fcc6-cb8b-5805-9834-9c56673a0e9b | `32\pi ` | component-scale[2] = `32 \pi` | False |
| b08ecf9c-f351-5fc2-9328-9e808bafe62f | `384\pi ` | component-scale[0] = `384 \pi` | True |

Original solution stages are retained in reference/source.json and compared with replay and a changed-radius variant in reference/side-by-side.md.

### q-127062 / cross-exponential / axis-square-scale

Calculate the flux of the vector field $F(x,y)={e}^{y}\,i+{e}^{x}\,j$ across the closed curve $C$ given by $r(t)=3\operatorname{cos}⁡t\,i+4\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Observed parameters: `{"a": 3, "b": 4, "k": 1}`. Field `452bd17e-660a-568a-8108-39d6d0770162`, key `selection`, five radio choices. Component structure: P=exp(y), Q=exp(x). One complete traversal, no shifts or singularities. Correct source value: `0`.

| Source answer UUID | Exact source value | Recipe at these parameters | Correct |
|---|---|---|---|
| 093b5f1d-7084-5cca-af48-56a7c276ea5d | `0` | axis-square-scale[0] = `0` | True |
| 1755e313-29bb-5235-930c-5480eea8e580 | `-\frac{25e}{12}` | axis-square-scale[2] = `- \frac{25 e}{12}` | False |
| 2a42ddb5-8533-50f3-9230-498c83bae1a9 | `-\frac{7e}{12}` | axis-square-scale[4] = `- \frac{7 e}{12}` | False |
| 93070110-72d1-593c-aaa7-f43291b04560 | `\frac{7e}{12}` | axis-square-scale[3] = `\frac{7 e}{12}` | False |
| c7b8c70b-0bf4-5466-85d5-56e8bfa6fc37 | `\frac{25e}{12}` | axis-square-scale[1] = `\frac{25 e}{12}` | False |

Original solution stages are retained in reference/source.json and compared with replay and a changed-radius variant in reference/side-by-side.md.

### q-127082 / triangular-linear / signed-half

Calculate the flux of the vector field $F(x,y)=x\,i+(x+y)\,j$ across the closed curve $C$ given by $r(t)=3\operatorname{cos}⁡t\,i+5\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Observed parameters: `{"a": 3, "b": 5, "k": 1}`. Field `8411ac91-aa07-508a-9904-aa0a020877bc`, key `selection`, five radio choices. Component structure: P=x, Q=x + y. One complete traversal, no shifts or singularities. Correct source value: `30\pi `.

| Source answer UUID | Exact source value | Recipe at these parameters | Correct |
|---|---|---|---|
| 29d3016e-ea1f-57be-ad3f-89bd52e2b595 | `-15\pi ` | signed-half[3] = `- 15 \pi` | False |
| 29d80bea-8d5f-5d6e-9d57-a11322c402b1 | `-30\pi ` | signed-half[1] = `- 30 \pi` | False |
| 2cd76549-ed5c-561a-a07f-a7506fbab6d4 | `15\pi ` | signed-half[2] = `15 \pi` | False |
| 3cf1e009-304c-5363-9a50-24170560d53d | `30\pi ` | signed-half[0] = `30 \pi` | True |
| eb22ea92-b3d9-59e8-9fe5-49b32e301c4f | `0` | signed-half[4] = `0` | False |

Original solution stages are retained in reference/source.json and compared with replay and a changed-radius variant in reference/side-by-side.md.

## Exceptions and fidelity

q-126717 is incomplete and unrated; exclude it explicitly rather than infer a level or alter it. q-127062 contains an endpoint typo, corrected only in generated solutions (v=a cos(t) starts and ends at a, not 1). Moderate/hard remain unsupported within this bounded package for the reasons in classification.md. Full bank fidelity requires 40/40 source values, 32/32 distractors and 8/8 complete correct designations. Layout checks are separate from mathematical bank equivalence. The replay uses normalized TeX and the same ordered instructional stages, not byte-identical captured OCR notation.

## Plot extraction and generation

No prompt, choice or solution contains an image or diagram. Rating: none. No assets are published; asset hashes are an empty list.
