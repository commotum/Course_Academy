# Template extraction

Database math basis 1356; source wrapper and full original fields/banks/presence are retained in `source.json`. R=(u−h)²+(v−k)² and r=√R. Recipes describe exact operations reproducing source values, not recovered author intent or learner-facing diagnosis. All equations are compared as complete residual polynomials up to nonzero scalar over an exact symbolic coefficient field.

## 1. Specific source descriptions

| Source | C; X | Difficulty | Radius form | Distance rows | Equation rows | Template/profile |
|---|---|---|---|---:|---:|---|
| q-54215 | (4,-4); (-4,2) | moderate | √100 | 4 | 3 | `integer_center_first` / `bank-q-54215` |
| q-72616 | (-1,2); (2,3) | absent | √10 | absent | absent | `incomplete_radio` / `bank-q-72616` |
| q-117096 | (-4,-3); (-1,0) | moderate | √18 | 3 | 3 | `radical_simplified` / `bank-q-117096` |
| q-117099 | (-4,-3); (0,-1) | moderate | √20 | 3 | 3 | `radical_simplified` / `bank-q-117099` |
| q-72617 | (-2,3); (1,-1) | moderate | √25 | 4 | 3 | `integer_signed` / `bank-q-72617` |
| q-72619 | (-1,-3); (1,1) | moderate | √20 | 3 | 3 | `radical_unsimplified` / `bank-q-72619` |
| q-72621 | (3,-3); (-1,2) | moderate | √41 | 3 | 3 | `radical_unsimplified` / `bank-q-72621` |

q-54215 computes C−X, then positive differences 8 and 6, square-root 100, radius 10. q-72617 computes X−C, retaining negative vertical difference −4, then √25 and 5. q-117096/q-117099 compute X−C and show positive differences, ending immediately in simplified radical radius; their substitution squares the grouped radical. q-72619/q-72621 retain the signed X−C differences and stop at the unsimplified square root, then explicitly square that same radius. Source banks may simplify that root independently. Every complete source solution has the same opening equation and concluding introduction, followed by generic equation, actual center/radius substitution and collected final equation. The differences in row count and radius notation remain separate template recipes. q-72616 has no source solution, label or designation; its five choices and field type exist and the MA widget agrees.

## 2. Generalized pattern

Given center C(h,k) and point X(u,v) on the circumference, compute the radius by the distance formula and substitute the center and squared radius into (x−h)²+(y−k)²=R. The required response is the whole equation. Preserve signed coordinate subtraction, both squared components, addition, square root and substitution. Equation equivalence must compare the complete relation. There is no midpoint, diameter, center extraction, completing square, intercept or other conic task.

## 3. Component and complete-bank mapping

All fields have key `selection`, type `:answer-field.type/radio`, answer type `:answer.type/math`, five owned choices. q-72616 has no correct ref; the other six refs exist. Source choice UUIDs and exact full values below identify every member. Original bank ordering is not significant, but membership and correct designation are. Recipe ordering below follows captured Pull choice order solely to map evidence; generated option order is shuffled.

### q-54215 — integer_center_first

Prompt: ![](images/63/63102dc32e44d75681b95ca5570c737224d7fd887d7c86d2b5c7a1e41a26c9f3.png)  The circle above is centered at $C(4,-4)$ and the point $X(-4,2)$ lies on the circumference. Find the equation of the circle.

| Original choice UUID | Exact equation | Correct designation | Parameterized operation |
|---|---|---|---|
| `41966cdb-4ae0-5538-9bc6-e14f91d4170f` | $(x-4)^{2}+(y+4)^{2}=100$ | correct | `correct`: center (h,k), RHS R |
| `8cd5e9e5-1f75-55a3-a81f-00682c5cd0dc` | $(x+4)^{2}+(y-4)^{2}=10$ | incorrect | `reverse_both_radius`: center (−h,−k), RHS r |
| `91982f68-5ef2-530b-998a-6c4d449f2b6e` | $(x-4)^{2}+(y+4)^{2}=10$ | incorrect | `radius`: center (h,k), RHS r instead of r² |
| `aa024009-c4d9-5a22-a9e5-fe96f4fb3494` | $(x+4)^{2}+(y-2)^{2}=100$ | incorrect | `reverse_x_point_y`: center (−h,v), RHS R (reversed horizontal sign and use given point y) |
| `ccb27233-f2ce-5f96-b456-6c8d1e14e5c5` | $(x-4)^{2}+(y+2)^{2}=100$ | incorrect | `point_y_reverse`: center (h,−v), RHS R (use negative given point y) |

### q-72616 — incomplete_radio

Prompt: ![](images/9e/9e905d98eafd51cd455811dc9b84fbca74f45dedb7fd7363e9dd97c953b3170a.png)  The circle above is centered at $C(-1, 2)$ and the point $X(2, 3)$ lies on the circumference. Find the equation of the circle.

| Original choice UUID | Exact equation | Correct designation | Parameterized operation |
|---|---|---|---|
| `c9c351e4-8bd6-5e57-9b6f-32dc18b88bd4` | $(x + 1)^{2} + (y + 2)^{2} = 10$ | absent | `reverse_y`: center (h,−k), RHS R |
| `ceb055af-6e86-5af2-9d4e-27f5372d988c` | $(x + 1)^{2} + (y - 2)^{2} = 10$ | absent | `correct`: center (h,k), RHS R |
| `0e091c04-e028-5876-b964-f681d5d46426` | $(x + 1)^{2} + (y - 2)^{2} = \sqrt{10}$ | absent | `radius`: center (h,k), RHS r instead of r² |
| `5b7da5f6-d41c-5640-809e-40b797691500` | $(x - 1)^{2} + (y + 2)^{2} = 10$ | absent | `reverse_both`: center (−h,−k), RHS R |
| `5cfb2715-4047-59fb-923f-fb6f02e15f87` | $(x - 1)^{2} + (y + 2)^{2} = \sqrt{10}$ | absent | `reverse_both_radius`: center (−h,−k), RHS r |

### q-117096 — radical_simplified

Prompt: ![](images/16/16d6786a4b1934ed234d4bf0896187aa6e93ec70cf045ddf4b743b1f51eaac2f.png)  The circle above is centered at $C(-4,-3)$ and the point $X(-1,0)$ lies on the circumference. Find the equation of the circle.

| Original choice UUID | Exact equation | Correct designation | Parameterized operation |
|---|---|---|---|
| `1b0c7c14-a555-5e01-8838-765e944ceedf` | $(x-4)^{2}+(y-3)^{2}=3\sqrt{2}$ | incorrect | `reverse_both_radius`: center (−h,−k), RHS r |
| `78dc7686-f3de-5b7d-8046-a89585820e9c` | $(x+4)^{2}+(y-3)^{2}=18$ | incorrect | `reverse_y`: center (h,−k), RHS R |
| `994030d6-5bdf-505c-ac30-a525c985caa5` | $(x+4)^{2}+(y+3)^{2}=18$ | correct | `correct`: center (h,k), RHS R |
| `a7739a17-e686-57c5-ba6c-a87d9d4e8077` | $(x+4)^{2}+(y+3)^{2}=3\sqrt{2}$ | incorrect | `radius`: center (h,k), RHS r instead of r² |
| `d0408c11-e9e7-55cb-940f-15a1df96ac67` | $(x-4)^{2}+(y-3)^{2}=18$ | incorrect | `reverse_both`: center (−h,−k), RHS R |

### q-117099 — radical_simplified

Prompt: ![](images/2b/2bd7e3cb9594623c6f5dc3fad35c33c71df0efe9e80b2053dde33f4ef9080bda.png)  The circle above is centered at $C(-4,-3)$ and the point $X(0,-1)$ lies on the circumference. Find the equation of the circle.

| Original choice UUID | Exact equation | Correct designation | Parameterized operation |
|---|---|---|---|
| `1cb0ea5e-ad3e-596c-a47f-1b2f569400c9` | $(x+4)^{2}+(y-3)^{2}=20$ | incorrect | `reverse_y`: center (h,−k), RHS R |
| `1dd34dda-6f93-5397-a33e-2a03884b982c` | $(x+4)^{2}+(y+3)^{2}=2\sqrt{5}$ | incorrect | `radius`: center (h,k), RHS r instead of r² |
| `b690d28c-7840-5bec-9fea-01836e32189d` | $(x+4)^{2}+(y+3)^{2}=20$ | correct | `correct`: center (h,k), RHS R |
| `bff71f03-a6dd-5c42-a982-4c93c6ea8bd5` | $(x-4)^{2}+(y-3)^{2}=2\sqrt{5}$ | incorrect | `reverse_both_radius`: center (−h,−k), RHS r |
| `dfbf80d1-3ee1-578b-9627-526049a9423e` | $(x-4)^{2}+(y-3)^{2}=20$ | incorrect | `reverse_both`: center (−h,−k), RHS R |

### q-72617 — integer_signed

Prompt: ![](images/d4/d45a9c753270dfd9186bc16736d1815a11997c88d2f35a0c40f487e6acef66c6.png)  The circle above is centered at $C(-2,3)$ and the point $X(1,-1)$ lies on the circumference. Find the equation of the circle.

| Original choice UUID | Exact equation | Correct designation | Parameterized operation |
|---|---|---|---|
| `27f70d2a-fc69-5d4c-8d76-eb29f542cee8` | $(x+2)^{2}+(y-3)^{2}=25$ | correct | `correct`: center (h,k), RHS R |
| `6d8195c7-e766-5e8a-9057-7cf807388cde` | $(x-2)^{2}+(y-3)^{2}=5$ | incorrect | `reverse_x_radius`: center (−h,k), RHS r |
| `8aa99c96-03d0-5732-b316-93ca22442393` | $(x-2)^{2}+(y-3)^{2}=25$ | incorrect | `reverse_x`: center (−h,k), RHS R |
| `c9082b17-653a-55a6-b4da-3fcc60887456` | $(x+2)^{2}+(y-3)^{2}=5$ | incorrect | `radius`: center (h,k), RHS r instead of r² |
| `e3377fdf-0433-59b7-872c-aa80d378fdc0` | $(x-2)^{2}+(y-3)^{2}=\sqrt{5}$ | incorrect | `reverse_x_double_root`: center (−h,k), RHS √r (an extra square root) |

### q-72619 — radical_unsimplified

Prompt: ![](images/2f/2ff035f38f5892f61d1eb037c7e39c59c8ec5104babac45224c4902152a0cfaa.png)  The circle above is centered at $C(-1,-3)$ and the point $X(1,1)$ lies on the circumference. Find the equation of the circle.

| Original choice UUID | Exact equation | Correct designation | Parameterized operation |
|---|---|---|---|
| `024d17a6-71d7-5b07-a9f7-4e90925b4266` | $(x+1)^{2}+(y-3)^{2}=20$ | incorrect | `reverse_y`: center (h,−k), RHS R |
| `39733cc5-69a1-5e1d-bebb-7bb234749a05` | $(x-1)^{2}+(y-3)^{2}=20$ | incorrect | `reverse_both`: center (−h,−k), RHS R |
| `cdc3778a-58ce-553d-acdf-2eca8ef39844` | $(x-1)^{2}+(y-3)^{2}=2\sqrt{5}$ | incorrect | `reverse_both_radius`: center (−h,−k), RHS r |
| `d77e9864-505e-5fbd-9ca7-87866b380248` | $(x+1)^{2}+(y+3)^{2}=2\sqrt{5}$ | incorrect | `radius`: center (h,k), RHS r instead of r² |
| `e5fd184d-c4e9-5208-a605-04a08c3cfd8d` | $(x+1)^{2}+(y+3)^{2}=20$ | correct | `correct`: center (h,k), RHS R |

### q-72621 — radical_unsimplified

Prompt: ![](images/6e/6e68ede9db2528ea607fc6fd63f0ec4ca1c1378982239913ef49153e1cf5b609.png)  The circle above is centered at $C(3,-3)$ and the point $X(-1,2)$ lies on the circumference. Find the equation of the circle.

| Original choice UUID | Exact equation | Correct designation | Parameterized operation |
|---|---|---|---|
| `44ceba2e-461c-5d6f-94d0-fffabcaa7f4e` | $(x-3)^{2}+(y-3)^{2}=\sqrt{41}$ | incorrect | `reverse_y_radius`: center (h,−k), RHS r |
| `67364410-21ff-5ab6-b499-984469e0f0b3` | $(x-3)^{2}+(y+3)^{2}=41$ | correct | `correct`: center (h,k), RHS R |
| `7e6b7a0c-3051-526a-9636-efd77cb0b591` | $(x+3)^{2}+(y+3)^{2}=41$ | incorrect | `reverse_x`: center (−h,k), RHS R |
| `c00a31e7-30ad-5958-a723-a2568cb7ceb8` | $(x-3)^{2}+(y+3)^{2}=\sqrt{41}$ | incorrect | `radius`: center (h,k), RHS r instead of r² |
| `ccdecbe3-6add-5929-86dd-7b81307f2bae` | $(x+3)^{2}+(y+3)^{2}=\sqrt{41}$ | incorrect | `reverse_x_radius`: center (−h,k), RHS r |

q-54215 has two compound point-coordinate substitutions; these are explicit complete-component operations supported as mathematical source-bank patterns, with the original author’s intended error explanation unresolved. Ordinary moderate selects among all six rated observed profiles before sampling parameters; these compound operations remain exact parameterized substitutions rather than claims about author intent. The selected profile supplies its complete bank and original worked-solution mask. q-72616 remains explicit evidence/completion and cannot be selected by ordinary defaults. No scalar curve fitting, constant noise, first-valid recipe pool or bank mixing occurs. q-72617’s additional √r is a source-supported second square-root operation, producing a radical distractor even when the radius is an integer.

## 4. Reusable templates and parameter policy

Fixed parts: source prose, generic circle equation, C/X labels, one five-choice radio and one shared worked solution per eligible instance. Variable components are complete coordinate tuples, complete squared-difference expressions, the radius rows, the whole substituted/final equations, diagram geometry and complete operation banks. Templates do not substitute short numeric text globally. Conditional components are sign grouping, simplification of zero center shifts, exact root form and source-specific radius row count. The incomplete template omits precisely its absent learner fields publicly; authored completion is separate.

All observed source banks use exact h,k,u,v and derive R/r. Independent symbolic whole-equation equivalence rejects the entire instance when any choices collide. With nonzero h,k, the sign-based banks have five distinct equations for every admitted task. Point-coordinate hybrid q-54215 can collide, so its entire sampled/explicit bank is rejected and no option is replaced. Defaults keep the selected profile fixed during parameter resampling. q-54215 and q-72617 require perfect-square R, preserving their observed four-row radius computation and actual square-root-to-integer final step; non-square R would duplicate the last two rows. q-117096/q-117099 require nonsquare R with a nonunit square factor, preserving their actual radical-reduction step. q-72619/q-72621 require nonsquare R and deliberately retain the unreduced √R radius. These guards reject incompatible explicit inputs as well as sampled parameters, with all original source parameters still accepted. Filtered domain counts for all six profiles are in `validation.json`; their union covers 24,400 tasks through the integer and unsimplified-radical profiles. Profile and notation aliases do not multiply that count. Degree-two residuals are monic in x², so the generator’s direct residual equality rejects equivalence up to scaling; the displayed-answer validator independently parses all equation members and compares full residuals. The coefficient field includes radicals from every bank.

Authored easy has a zero vertical center and the canonical/source Pythagorean distance patterns. Its five operations are correct, reverse h, use X as center, leave r unsquared, and omit the vertical distance square. This separate complete bank avoids sign duplicates caused by k=0. Authored hard uses the same five operations as q-117096, with exactly two half-integer differences/squares. Parameter magnitudes are bounded to 9/2 and R is noninteger; no larger-denominator algebra is admitted. Level-specific guards are enforced on explicit inputs and samplers. Missing levels are authored design claims, not labels inferred from sources.

The mathematical fingerprint includes center and on-circle point because the assessed arithmetic depends on both, even when another point gives the same resulting circle. It excludes profiles, templates, seed, ordering and variable-spelling aliases. The displayed bank, prompt, solution and actual difficulty contribute to content identity. Source IDs/provenance are metadata; generated UUIDs are field-owned. No source EDB identities are reused as new content identities.

Frozen verification includes complete original bank/prose/presence replay, parsed displayed coordinate/solution mathematics, wrong-equation uniqueness, changed-parameter tests per bank, strict explicit invalid-call tests, meaningful finite-domain counts, seed-independent content identity, fresh concurrent Matplotlib calls and native radio grading. Ordinary moderate coverage checks seeds 0–35, exercises all six rated profiles, independently verifies all 36 complete banks and formal/derived solution stages, compares each with explicit replay at the same parameters, verifies selection occurs before sampling, and natively grades every displayed choice. `validation.json` reports every denominator separately. Raw q-72616 is not sent to a native fixture because it has no correct ref; its authored completion is graded and not counted as a recovered source designation. No source mathematical errors were detected; missing attributes remain unresolved captured evidence.
