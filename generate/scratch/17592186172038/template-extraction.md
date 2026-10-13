# Four-stage template extraction

## 1. Specific originals

Every original prompt, field, UUID, correct-ref presence, image path and full worked solution is retained in source.json. White-composited source contact sheets and source-raster.json map every displayed choice. Points and coefficients are transcribed in source-cases.json. The five easy sources include signed points, squares, zero slopes, a whole quotient, a half coefficient and integer slopes through8. The two unrated sources contain the same isolated-point response format; they receive an authored easy replay assignment.

### q-50099: constant_product

- Equation: `-x*y + 2`. Points in worked order: `[[-1, 2], [1, 3], [0, -2]]`. Exact slopes: `[4, -1, 2]`.
- Five image choices and the source concluding diagram have the same locations. All three substitution rows, initial instruction, substitution explanation and concluding paragraph are preserved when present. q-50099/q-80494 have no worked solution; their replacements are explicitly authored.

### q-80494: quadratic_linear

- Equation: `x**2 - 2*y`. Points in worked order: `[[1, 2], [-1, -1], [2, -2]]`. Exact slopes: `[-3, 3, 8]`.
- Five image choices and the source concluding diagram have the same locations. All three substitution rows, initial instruction, substitution explanation and concluding paragraph are preserved when present. q-50099/q-80494 have no worked solution; their replacements are explicitly authored.

### q-119674: rational_square

- Equation: `-y**2/x`. Points in worked order: `[[-1, -2], [2, -2], [2, 2]]`. Exact slopes: `[4, -2, -2]`.
- Five image choices and the source concluding diagram have the same locations. All three substitution rows, initial instruction, substitution explanation and concluding paragraph are preserved when present. q-50099/q-80494 have no worked solution; their replacements are explicitly authored.

### q-49811: two_quadratic

- Equation: `2*x**2 - y**2/2`. Points in worked order: `[[1, 2], [1, 0], [-1, -2]]`. Exact slopes: `[0, 2, 0]`.
- Five image choices and the source concluding diagram have the same locations. All three substitution rows, initial instruction, substitution explanation and concluding paragraph are preserved when present. q-50099/q-80494 have no worked solution; their replacements are explicitly authored.

### q-80499: affine_fraction

- Equation: `x/4 + y/2`. Points in worked order: `[[4, -2], [2, 1], [-1, 3]]`. Exact slopes: `[0, 1, 5/4]`.
- Five image choices and the source concluding diagram have the same locations. All three substitution rows, initial instruction, substitution explanation and concluding paragraph are preserved when present. q-50099/q-80494 have no worked solution; their replacements are explicitly authored.

### q-80497: affine

- Equation: `x - 2*y`. Points in worked order: `[[-2, -1], [2, -1], [2, 1]]`. Exact slopes: `[0, 4, 0]`.
- Five image choices and the source concluding diagram have the same locations. All three substitution rows, initial instruction, substitution explanation and concluding paragraph are preserved when present. q-50099/q-80494 have no worked solution; their replacements are explicitly authored.

### q-96089: affine

- Equation: `x + 2*y`. Points in worked order: `[[-2, 1], [1, 1], [2, 1]]`. Exact slopes: `[0, 3, 4]`.
- Five image choices and the source concluding diagram have the same locations. All three substitution rows, initial instruction, substitution explanation and concluding paragraph are preserved when present. q-50099/q-80494 have no worked solution; their replacements are explicitly authored.

## 2. Shared mathematical purpose

For `dy/dx=f(x,y)`, evaluate exactly at three marked points and identify three short segments with those slopes. Each question has one five-option image radio field. Three independent substitutions supply a single fixed worked solution. Six expression forms retain complete mathematical component masks; they do not branch into solving differential equations or inferring global regions.

## 3. Every bank component

The following complete recipes reproduce every observed image's mathematical orientation. `s0,s1,s2` are freshly evaluated correct slopes in the stated point order; `a` is the displayed leading coefficient. `oo` means a vertical line, not an undefined correct differential-equation value. The complete profile is chosen before parameters. These operations map visual patterns, with underdetermined error interpretation: they are **replay profiles**, not claims about the original author's distractor intent. Especially unit/zero/vertical patterns cannot justify defaulting to arbitrary fitted expressions. Normal generation instead uses the complete authored method bank below.

| Source | Index | Raw image value | Exact slope triple | Parameter recipe | Correct status |
|---|---:|---|---|---|---|
| q-50099 | 0 | `images/23/23960cd365d0417853d592889b388d983db542780393f9399321038b6e7eb90d.png` | `[4, -1, 0]` | `s0,s1,0` | incorrect |
| q-50099 | 1 | `images/34/34effb89fcb17eb363b96531377aac0179f0bb9c6c630dc4e19d3e88be26cfff.png` | `[4, 1, 2]` | `s0,-s1,s2` | incorrect |
| q-50099 | 2 | `images/ae/aeb84d93a75a36faf3592ff50bb733d896b4137469eb059080f8770bfce1d673.png` | `[-4, -1, -2]` | `-s0,s1,-s2` | incorrect |
| q-50099 | 3 | `images/d1/d1a077cc4d330fa27496380ca2a278f80c44732955e2b156a5925d4665185267.png` | `[4, -1, 2]` | `s0,s1,s2` | inferred correct; raw designation absent |
| q-50099 | 4 | `images/ad/ad979f40ecb247821077f08b2746558e95931cecc2a38e300155001446754347.png` | `[0, -1, 2]` | `0,s1,s2` | incorrect |
| q-80494 | 0 | `images/64/646ab4dfffc89f9a93399bad2b51d9c5e5e04363f3315460daf4e181bcd4d0eb.png` | `[-3, 3, 8]` | `s0,s1,s2` | inferred correct; raw designation absent |
| q-80494 | 1 | `images/49/49a94bebceab2be91680224ec11063d61bee6fd7672ff5951539a54bf48632be.png` | `[3, -3, 0]` | `-s0,-s1,0` | incorrect |
| q-80494 | 2 | `images/ca/caba7f4d1cfc28aa787bcb334bbb623b4972552af23775ece965e929c0972278.png` | `[3, 0, -8]` | `-s0,0,-s2` | incorrect |
| q-80494 | 3 | `images/ae/ae6dca155711c63cee07be58a82c554ec18bd6ee869329ae4a238aca67252545.png` | `[0, -3, 8]` | `0,-s1,s2` | incorrect |
| q-80494 | 4 | `images/84/8400ee6f8ac57e57211f93bd38b2ca8668c6b60d9cc8c237676a35c25fc640a9.png` | `[3, 3, 8]` | `-s0,s1,s2` | incorrect |
| q-119674 | 0 | `images/5e/5e6b2df4680cea04cda42312659c76ba713a025150ebcc547dddc2a6501aebf3.png` | `[4, -2, -2]` | `s0,s1,s2` | observed correct |
| q-119674 | 1 | `images/d4/d48911eaffd88e249ef115a5511bff979ffa0f848ef8a1e8556db07ad273e41a.png` | `[4, -2, 2]` | `s0,s1,-s2` | incorrect |
| q-119674 | 2 | `images/a0/a0f75b52c741eca3322f4fe61009ba3c65e573f588edf9d3785019a1227f9769.png` | `[0, -2, -2]` | `0,s1,s2` | incorrect |
| q-119674 | 3 | `images/c7/c78c6d760cffb3dfb95233f9fc21dfea5a951371b056827885d1aa35469a458c.png` | `[4, 2, -2]` | `s0,-s1,s2` | incorrect |
| q-119674 | 4 | `images/4a/4afe9527d6ff39ce7f5325a4a35ce5095d9bf0b1beb2fcde4de86a977bdac9e8.png` | `[-4, 0, 2]` | `-s0,0,-s2` | incorrect |
| q-49811 | 0 | `images/9b/9bba5f86445177b9124813e85bf9294b7b566a029686f163c685663f5b352e30.png` | `[oo, 1, -1]` | `oo,a/2,-a/2` | incorrect |
| q-49811 | 1 | `images/3d/3dcb95f44f53f046c543d281038c0ac03fb14357cecdb7b96d5f41d33e9b0ed6.png` | `[0, 2, 0]` | `s0,s1,s2` | observed correct |
| q-49811 | 2 | `images/7a/7a550e346a2b31e09ec2dbfcf8eefe9a80108a74edffa92cb3a617643a810e31.png` | `[oo, 1, 1]` | `oo,a/2,a/2` | incorrect |
| q-49811 | 3 | `images/e5/e5b20b6b0ae17ca9ee891ec33efa93fd23f684e938b1527e56db01f11a2e53d8.png` | `[oo, 1, 0]` | `oo,a/2,0` | incorrect |
| q-49811 | 4 | `images/a8/a87973b958bd7a598da127164fd77365daaf121a601c25d198f1a3256bd84f6d.png` | `[-1, 1, -1]` | `-a/2,a/2,-a/2` | incorrect |
| q-80499 | 0 | `images/c4/c4f19e6b424610387a8973b037c3f4636c09dba441ab1d6bd36dbe103d779a88.png` | `[0, -1, 5/4]` | `s0,-s1,s2` | incorrect |
| q-80499 | 1 | `images/77/770f3089576cabd68f3c80b597eb4f15df279538c49853526b0ea123bc75af08.png` | `[5/4, -1, 0]` | `s2,-s1,s0` | incorrect |
| q-80499 | 2 | `images/82/8255d8370e49983ff0e37b5068a8a997de5eeadaedf7bd7869cf5dcd3c826ca1.png` | `[-1, 1, 0]` | `-s1,s1,s0` | incorrect |
| q-80499 | 3 | `images/e1/e1ca6081e8077bcbc54de6a71e10ef1d278bbbc6b99842f1eee0d3dfcb71ebda.png` | `[0, 1, 5/4]` | `s0,s1,s2` | observed correct |
| q-80499 | 4 | `images/5b/5b77994fcd8b675c439a37e1b2049c0c6d266f12b3dc298b3183133b9010c818.png` | `[-1, 0, 5/4]` | `-s1,s0,s2` | incorrect |
| q-80497 | 0 | `images/32/327d6ae536cd6d76eff01387b51a4d2cc0522559d6ec6d02e3a86c2a3977f7b2.png` | `[-4, 4, 4]` | `-s1,s1,s1` | incorrect |
| q-80497 | 1 | `images/1b/1b8e42e667d2fe4c713e92f879c9894e826fdbe3e6928addb3c4b36ce71991e0.png` | `[4, 0, 4]` | `s1,0,s1` | incorrect |
| q-80497 | 2 | `images/e7/e7e267508d68c1d4eeb31509a4a2957e120cecab920481ba6dc2b0fa1f84433b.png` | `[0, 0, 0]` | `0,0,0` | incorrect |
| q-80497 | 3 | `images/3d/3ddcc5784dc1fd60ba3c95ecda373678d00fc6c45e6b5e5655febcc130c37d95.png` | `[0, 4, 0]` | `s0,s1,s2` | observed correct |
| q-80497 | 4 | `images/25/2527ad3b4f6d0a1d84a9e907b5e3e9bddee439fbd17c2a1a4c3ca8c418f65293.png` | `[-4, -4, -4]` | `-s1,-s1,-s1` | incorrect |
| q-96089 | 0 | `images/bf/bfd9789a91f680d5105d9081e51103ffba5e986fa4a96331cde06df6d0c42854.png` | `[0, 0, 1]` | `0,0,a` | incorrect |
| q-96089 | 1 | `images/54/543365359599203eb6f9e8824f6e3b2987a1fec9121568dd7a9098bfc16870f1.png` | `[0, 3, 4]` | `s0,s1,s2` | observed correct |
| q-96089 | 2 | `images/3e/3edf063230f100455638fa25f28a4c5e59e2e54884d9e273724b76ae483aa0bc.png` | `[-3, 1, -1]` | `-s1,a,-a` | incorrect |
| q-96089 | 3 | `images/63/631f9d7772354c6962f98e857371eac65d0fe36116bbae60dacd0db7ba01bc04.png` | `[1, 1, 0]` | `a,a,0` | incorrect |
| q-96089 | 4 | `images/76/7670c9662fec950b45f2f939ed416590d278875b168caea9d7e5b70f7c8c6a9f.png` | `[1, 1, -1]` | `a,a,-a` | incorrect |

Authored default bank (five complete members): correct coordinate substitution; reverse every segment's sign; use x for both x and y; set y=0; omit the x-dependent term (use x=1 for rational square), with constant-product's last member omitting its constant instead. The commutative product makes swapping x/y indistinguishable, so that operation is not used. Reject all five when any member is invalid/equivalent or when any pair lacks an8° orientation distinction at some assessed point. No diagnosis text is inserted into learner output.

## 4. Reusable masks, constraints and extension bounds

Fixed prompt asks which diagram supplies slopes at indicated points. A full RHS component varies; prose is never globally symbol-replaced. Source masks preserve each original prompt's derivative notation and terminal punctuation. The source solution opening retains its precise coordinate/punctuation layout; three source rows become three complete coordinate→substitution→result masks, with coefficient/component TeX normalization disclosed separately from mathematical sequence/prose fidelity. Original image paths are regenerated assets. Authored moderate/hard rows additionally show evaluated terms before combining, without adding another point or assessment demand.

Easy coordinates are integers |coordinate|≤4; coefficients are nonzero small integers |coefficient|≤4, except the observed two-quadratic b half coefficient; positive integral outer denominators ≤4. Moderate uses integer coordinates |coordinate|≤3 and a **nonintegral half leading coefficient** (±1/2,±3/2,±5/2,±7/2 within |a|≤4), with small nonzero integer second coefficients and an evaluated-term arithmetic stage. Hard retains two-quadratic, rational-square and affine-fraction forms, uses a nonintegral half/quarter leading coefficient |a|≤6, and **both coordinates nonintegral halves at each of the three points**, |coordinate|≤7/2. Negative coordinate substitution is required at moderate/hard. All bounds apply to explicit inputs as well as samplers; x never vanishes in a rational denominator.

The distinction from easy's existing half coefficient/whole quotient is the required nonintegral leading multiplier throughout moderate, and six nonintegral input coordinates throughout hard. These are authored arithmetic workload choices grounded in the same source squares/quotients and prerequisite substitution arithmetic, not new DE methods or recovered MA difficulty labels. Within each level there is no progression.

Identity canonicalizes rational coefficient spellings and unordered point triples for mathematical-task fingerprints; complete banks, ordered displayed worked solution and presentation belong to content identity. Plot geometry and intermediate values derive from the same exact parameters. Missing refs are inferred by independent evaluation: q-50099 `(4,-1,2)` matches index3; q-80494 `(-3,3,8)` matches index0. Raw widget/source refs stay missing. Only five stored designation matches are reported.

Signed multiplicative coefficients are parenthesized in all RHS/substitution/evaluation masks, so subtraction of a negative coefficient appears as `-(-b)` rather than bare `--`. The signed-mask audit independently parses4608 displayed stages across1536 coefficient/coordinate sign combinations. This is mathematical notation normalization; the five source worked solutions still preserve all non-math prose and their ordered three coordinate→substitution→result rows. Exact source math notation is not claimed.
