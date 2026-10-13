# Template extraction

## 1. Describe every original

### 17592186198624 — linear_yz

Original parameters: `{"a": "2", "b": "1", "c": "1", "d": "-2", "lu": "0", "hu": "1", "lv": "-1", "hv": "1", "lw": "1", "hw": "4"}`. Original volume $\frac{6}{5}$. Bounds are finite rectangular intervals in u,v,w. The source defines R through these three coupled coordinate expressions, rather than providing the inverse map.

Forward coordinate functions: $x,2 y + z,y - 2 z$. Actual inverse: $u,\frac{2 v}{5} + \frac{w}{5},\frac{v}{5} - \frac{2 w}{5}$.

Nine ordered partials: $\begin{vmatrix}1 & 0 & 0 \\ 0 & 2 & 1 \\ 0 & 1 & -2\end{vmatrix}$. Forward determinant $-5$; signed inverse $- \frac{1}{5}$; absolute inverse $\frac{1}{5}$.

### 17592186198965 — reciprocal

Original parameters: `{"a": "1", "b": "1", "c": "1", "d": "1", "lu": "1", "hu": "2", "lv": "1", "hv": "2", "lw": "1", "hw": "5"}`. Original volume $\frac{4}{5}$. Bounds are finite rectangular intervals in u,v,w. The source defines R through these three coupled coordinate expressions, rather than providing the inverse map.

Forward coordinate functions: $y,x + \sqrt{y},\frac{1}{z + 1}$. Actual inverse: $- \sqrt{u} + v,u,-1 + \frac{1}{w}$.

Nine ordered partials: $\begin{vmatrix}0 & 1 & 0 \\ 1 & \frac{1}{2 \sqrt{y}} & 0 \\ 0 & 0 & - \frac{1}{\left(z + 1\right)^{2}}\end{vmatrix}$. Forward determinant $\frac{1}{\left(z + 1\right)^{2}}$; signed inverse $\frac{1}{w^{2}}$; absolute inverse $\frac{1}{w^{2}}$.

### 17592186374152 — log

Original parameters: `{"a": "1", "b": "1", "c": "1", "d": "1", "lu": "1/2", "hu": "1", "lv": "3", "hv": "10", "lw": "1", "hw": "2"}`. Original volume $\ln{\left(128 \right)}$. Bounds are finite rectangular intervals in u,v,w. The source defines R through these three coupled coordinate expressions, rather than providing the inverse map.

Forward coordinate functions: $x,x^{2} + y,x z$. Actual inverse: $u,- u^{2} + v,\frac{w}{u}$.

Nine ordered partials: $\begin{vmatrix}1 & 0 & 0 \\ 2 x & 1 & 0 \\ z & 0 & x\end{vmatrix}$. Forward determinant $x$; signed inverse $\frac{1}{u}$; absolute inverse $\frac{1}{u}$.

### 17592186374159 — shear

Original parameters: `{"a": "1", "b": "1", "c": "1", "d": "1", "lu": "0", "hu": "1", "lv": "0", "hv": "1", "lw": "-1", "hw": "1"}`. Original volume $2$. Bounds are finite rectangular intervals in u,v,w. The source defines R through these three coupled coordinate expressions, rather than providing the inverse map.

Forward coordinate functions: $x,x + y,x^{2} + y^{2} + z$. Actual inverse: $u,- u + v,- u^{2} + w - \left(- u + v\right)^{2}$.

Nine ordered partials: $\begin{vmatrix}1 & 0 & 0 \\ 1 & 1 & 0 \\ 2 x & 2 y & 1\end{vmatrix}$. Forward determinant $1$; signed inverse $1$; absolute inverse $1$.

### 17592186374166 — linear_xz

Original parameters: `{"a": "1", "b": "1", "c": "1", "d": "-1", "lu": "-5", "hu": "5", "lv": "0", "hv": "10", "lw": "0", "hw": "6"}`. Original volume $600$. Bounds are finite rectangular intervals in u,v,w. The source defines R through these three coupled coordinate expressions, rather than providing the inverse map.

Forward coordinate functions: $x + z,y,y - z$. Actual inverse: $u - v + w,v,v - w$.

Nine ordered partials: $\begin{vmatrix}1 & 0 & 1 \\ 0 & 1 & 0 \\ 0 & 1 & -1\end{vmatrix}$. Forward determinant $-1$; signed inverse $-1$; absolute inverse $1$.

### 17592186374173 — sqrt

Original parameters: `{"a": "1", "b": "1", "c": "1", "d": "1", "lu": "-2", "hu": "2", "lv": "0", "hv": "1", "lw": "1", "hw": "4"}`. Original volume $60$. Bounds are finite rectangular intervals in u,v,w. The source defines R through these three coupled coordinate expressions, rather than providing the inverse map.

Forward coordinate functions: $x,x^{2} - y - z,\sqrt{z}$. Actual inverse: $u,u^{2} - v - w^{2},w^{2}$.

Nine ordered partials: $\begin{vmatrix}1 & 0 & 0 \\ 2 x & -1 & -1 \\ 0 & 0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}$. Forward determinant $- \frac{1}{2 \sqrt{z}}$; signed inverse $- 2 w$; absolute inverse $2 w$.

## 2. Shared pattern and purpose

Find volume from R alone by recognizing the coordinate forms in its inequalities, finding a rectangular transformed domain, computing all nine partial derivatives of the forward map, evaluating its determinant (source cofactor or triangular reduction), taking its signed reciprocal, then using the absolute value as density1 Jacobian in a triple integral. Separate variables, write elementary primitive brackets, evaluate both endpoints and collect the scalar. The original common prose, four numbered steps and every ordered mathematical row are preserved verbatim in raw source replay. Nonlinear maps are restricted to positive branch intervals away from singularities. Normal output retains the common prose and full stages, adds explicit inverse branch verification and all three first-row cofactors, and shows substituted plus individually evaluated primitive endpoint components. These additions are authored; they do not count as source-sequence fidelity.

## 3. Components and complete-bank accounting

Each raw profile is attached to a complete captured field bank. Every option below is an explicit homogeneous region-stretch recipe h×E; this reproduces the actual scalar value at h=1 and parameterizes the changed v-interval geometry. The unknown historical wrong operation is **unresolved** for every wrong scalar. Homogeneous scaling is not promoted as a recovered learner distractor operation. The complete profile is ineligible, including the historical negative reciprocal option.

### raw_17592186198624

Field 0: `b34c2735-f65f-5fac-8644-8b3f3758b0a1`, key selection, radio. Correct designation absent.

| Owned source answer ID | Original scalar | Recipe | Correct designation |

|---|---|---|---|

| 8865e6bb-6344-5115-83bd-d794ad8a6d9f | `\frac{6}{5}` | `h*((6)/(5))` | False |

| af38e17d-9eab-5171-abb0-c3baabb6b6ba | `\frac{8}{5}` | `h*((8)/(5))` | False |

| 11c289d0-561a-554e-a828-5cbceec4f39a | `15` | `h*(15)` | False |

| 71cd64af-d215-54eb-bc30-68cf19a7e94a | `2` | `h*(2)` | False |

| 792612f0-0e7e-56ef-ad2a-ff27287e9ee7 | `\frac{2}{5}` | `h*((2)/(5))` | False |

Field 1: `6efacc92-066c-57b7-8f28-3ccd8c8edf81`, key selection, radio. Original correct \frac{6}{5}

| Owned source answer ID | Original scalar | Recipe | Correct designation |

|---|---|---|---|

| 5a834bf3-3872-5b5d-969c-61edac983b6b | `15` | `h*(15)` | False |

| 775b3096-ba1d-5165-b372-dbf63725687c | `\frac{6}{5}` | `h*((6)/(5))` | True |

| 03c2babe-4839-5bdc-afc4-6749f697b54b | `\frac{2}{5}` | `h*((2)/(5))` | False |

| 42f92fc3-0b2e-5275-897a-62f665a73321 | `2` | `h*(2)` | False |

| fe97e990-5c5d-5501-b58a-2aaf7be8b50a | `\frac{8}{5}` | `h*((8)/(5))` | False |

### raw_17592186198965

Field 0: `3cd3b3e1-98ae-532b-94b3-c5b9b8ab641b`, key selection, radio. Correct designation absent.

| Owned source answer ID | Original scalar | Recipe | Correct designation |

|---|---|---|---|

| 881b0dd0-01c6-5013-9685-0e58c6da71c5 | `4` | `h*(4)` | False |

| c8a11a8a-6503-5229-93d1-630340faec00 | `1` | `h*(1)` | False |

| 33e5fb8a-a7fa-5959-b381-9183f9303802 | `\frac{4}{5}` | `h*((4)/(5))` | False |

| 3404d280-8cad-5644-8ec1-3e6e08824288 | `2` | `h*(2)` | False |

| 4cd7243b-48c8-50fa-aaa2-6aa1ef439e80 | `-\frac{2}{5}` | `h*(-(2)/(5))` | False |

### raw_17592186374152

Field 0: `5287f396-f7c5-5f63-8e16-6e1738da83ab`, key selection, radio. Original correct 7\operatorname{ln}⁡2

| Owned source answer ID | Original scalar | Recipe | Correct designation |

|---|---|---|---|

| 4b2d1ca3-fd9b-57f2-ac29-4b16c135420c | `28` | `h*(28)` | False |

| d3fd9c37-4c27-5746-b851-f7b4512dd4ea | `2\operatorname{ln}⁡2` | `h*(2*log(2))` | False |

| a9c9008f-7ebb-5f0c-9ef4-3aba8c68542d | `7\operatorname{ln}⁡2` | `h*(7*log(2))` | True |

| f9d1a911-155e-5064-989c-bdd887a93726 | `14` | `h*(14)` | False |

| 730b3a0c-ab79-5dd0-b3b4-eb287d28f6b6 | `30` | `h*(30)` | False |

### raw_17592186374159

Field 0: `081961bd-b52b-565f-b46b-523fd43cde20`, key selection, radio. Original correct 2

| Owned source answer ID | Original scalar | Recipe | Correct designation |

|---|---|---|---|

| 74cbe566-120c-5aa2-9d0f-8b0d51b92825 | `3` | `h*(3)` | False |

| 372e9f40-cc59-532c-a782-6948b90925c9 | `\frac{1}{2}` | `h*((1)/(2))` | False |

| 8a16bd5e-23ba-5f37-8518-594f3a0cc660 | `2` | `h*(2)` | True |

| 455911a2-33b2-56a3-a5e6-863976f27387 | `1` | `h*(1)` | False |

| fe23f6e2-faba-5fcc-a1dc-a65a5472035a | `4` | `h*(4)` | False |

### raw_17592186374166

Field 0: `11699b7d-5958-5ded-80ec-84552796d392`, key selection, radio. Original correct 600

| Owned source answer ID | Original scalar | Recipe | Correct designation |

|---|---|---|---|

| 1020cd0b-a734-523c-a873-ae4ccc88f60a | `60` | `h*(60)` | False |

| eded55eb-08dc-5eea-9038-37f16794d4b0 | `120` | `h*(120)` | False |

| 5a6e2d78-660c-5283-ab55-0c4291532b27 | `600` | `h*(600)` | True |

| 9479d209-1358-5b6d-b729-5097d39ca7d5 | `100` | `h*(100)` | False |

| db3a4d38-29e5-54a0-b850-59abf8d19cfe | `200` | `h*(200)` | False |

### raw_17592186374173

Field 0: `230795bb-1c46-5274-8505-2f18821e3031`, key selection, radio. Original correct 60

| Owned source answer ID | Original scalar | Recipe | Correct designation |

|---|---|---|---|

| cedf6411-1c50-521c-9753-b78164606edd | `12` | `h*(12)` | False |

| 2156f8ec-e04e-51b8-bc96-f4f57ab9bd72 | `60` | `h*(60)` | True |

| 641c62ce-a323-535d-adec-144d3026c01d | `36` | `h*(36)` | False |

| 08e58611-c6b0-57ca-af8a-daaeefda2147 | `6` | `h*(6)` | False |

| 652a7c70-07d1-5457-a185-ceed917c21bf | `30` | `h*(30)` | False |

## 4. Reusable masks, domains and calculations

Raw recipes have complete-component slots for lv,hv, both inequalities (R and Δ), repeated/separated integral bounds, primitive v brackets, evaluated v endpoint differences, and final scalar. The fixed transformations and all nine derivatives/Jacobians remain unchanged because v-width is the varied component and the density does not depend on v. h=1..4 is explicitly bounded; no literal original-payload branch or answer table lookup is used. source-cases.json supplies h=1 for every question. Every optional difficulty/solution/correct attribute follows original presence. The reciprocal unrated question remains without a worked solution in raw output.

Normal parameters vary coefficients, offsets/endpoints and interval widths. Coefficients are nonzero signed integers of magnitude1..3; unused coefficients do not enter mathematical fingerprints because only actual coordinate inequalities are hashed, normalized under nonzero common scaling with endpoint reversal for negative scaling. Presentation and complete banks have a separate content fingerprint. General bounds are integer or half-integer, absolute lower ≤6/upper ≤12, strictly ordered. Easy a,c are2or3, all lower endpoints0, upper endpoints≤6; sample widths are distinct members of2..6. Hard log requires u>0; reciprocal requires u>0,w>0; sqrt/cube require w>0. Cube endpoints are perfect cubes (sampler1,8). Explicit calls obey identical bounds. There is one elementary nonconstant Jacobian factor at hard. Singular coefficient blocks and any invalid/ambiguous complete bank are rejected whole.

Authored complete banks, with V correct, lengths du,dv,dw, rectangular volume B=du dv dw, and J absolute inverse density:

| Family | Four full wrong operation values |

|---|---|

| affine | B; B/J; V/du; V/dv |

| linear_yz, shear, linear_xz | V/du; V/dv; V/dw; V·hu/du (upper coordinate instead of its length) |

| log | B; abs(b)dv dw(hu²−lu²)/2 (forward Jacobian); V/dv; dv dw ln(hu)/abs(b) (omit lower primitive) |

| sqrt | B; V/2 (omit chain factor2); du dv(hw³−lw³)/3 (use z=w² in place of dz/dw); du dv hw² (omit lower square) |

| reciprocal | B; du dv(hw³−lw³)/3 (forward Jacobian); du dv/hw (only upper reciprocal magnitude); du dv(1/lw²−1/hw²) (integrate the magnitude of the differentiated density) |

| cube | B;3V (omit chain factor3); abs(ad−bc)V (omit inverse linear-block determinant); V/du |

All these banks are authored method operations, selected before parameters; none uses an arbitrary numeric perturbation. Every displayed option must be a positive real value and unequal to every other option.

Source presentation evidence: all 35 decoded source choice strings have single command backslashes; JSON escaping does not establish doubled bytes. Source solutions themselves already have balanced TeX and are preserved exactly. Source linear_xz inequalities have standard comma separation; no punctuation defect is claimed. No mathematical source correction is needed in the five rated solutions. Native grading of choice IDs cannot establish these mathematical/fidelity claims.

Frozen QA checks192 family-specific normal records plus120 default records. The full valid sampler Cartesian product is not exhaustively enumerated or claimed as a task count; exact tested meaningful unique counts are in validation.json. The domain has coefficient, signed shear and genuinely different region-width variation within one method, not letter/bank aliases.
