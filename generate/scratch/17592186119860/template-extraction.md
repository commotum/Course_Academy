# Four-stage template extraction

## 1. Specific source descriptions

The following records describe every source independently; exact prompts, fields, original choice values/IDs and solutions are preserved in source.json.

### q-33759 — log_square

![](images/c7/c76cff47179efaaf490430856b8db1f2b85f0d2000d34725a9c40a9e150ccf6b.png)

Find the arc length of the curve $r(t) = ⟨\ln t, 2t, t^{2}⟩$
from $t = 1$ to $t = e$.

Coordinates: `log(t)`, `2*t`, `t**2`. Interval [1,E]. Speed `1/t+2*t`. Reciprocal derivative, positive-domain perfect square, logarithmic antiderivative; source solution unavailable. Numeric endpoint-stage count: 0.

Original field shape: radio selection, five complete scalar exact expressions; no distractor-specific feedback.

### q-33779 — product_trig

Find the arc length of the curve $f(t)=⟨\operatorname{cos}⁡t+t\operatorname{sin}⁡t,\,\operatorname{sin}⁡t-t\operatorname{cos}⁡t,\,\frac{\sqrt{3}}{2}{t}^{2}⟩$
from $t=1$ to $t=3.$

Coordinates: `cos(t)+t*sin(t)`, `sin(t)-t*cos(t)`, `sqrt(3)*t**2/2`. Interval [1,3]. Speed `2*t`. Product-rule expansion and cancellation, Pythagorean identity, positive t, quadratic endpoint difference. Numeric endpoint-stage count: 2.

Original field shape: radio selection, five complete scalar exact expressions; no distractor-specific feedback.

### q-127635 — poly_negative

Find the arc length of the curve $r(t)=⟨2t,\,\frac{1}{3}{t}^{3},\,{t}^{2}⟩$ from $t=-1$ to $t=0.$

Coordinates: `2*t`, `t**3/3`, `t**2`. Interval [-1,0]. Speed `t**2+2`. Polynomial perfect square, negative lower bound; explicit substitution, sign distribution, evaluation. Numeric endpoint-stage count: 3.

Original field shape: radio selection, five complete scalar exact expressions; no distractor-specific feedback.

### q-76906 — quadratic_two

Find the arc length of the curve $r(t)=⟨{t}^{2},\,4,\,{t}^{2}⟩$
from  $t=0$ to $t=2.$

Coordinates: `t**2`, `4`, `t**2`. Interval [0,2]. Speed `2*sqrt(2)*t`. Two nonzero linear velocities, nonnegative t, radical coefficient; direct final evaluation. Numeric endpoint-stage count: 1.

Original field shape: radio selection, five complete scalar exact expressions; no distractor-specific feedback.

### q-76908 — poly_ordered

Find the arc length of the curve $r(t)=⟨t,\,{t}^{2},\,\frac{2{t}^{3}}{3}⟩$
from  $t=0$ to $t=3.$

Coordinates: `t`, `t**2`, `2*t**3/3`. Interval [0,3]. Speed `1+2*t**2`. Three nonzero polynomial velocities, quartic perfect square; component evaluation then collection. Numeric endpoint-stage count: 2.

Original field shape: radio selection, five complete scalar exact expressions; no distractor-specific feedback.

### q-76914 — chain_product

Find the arc length of the curve $r(t)=⟨2t\operatorname{cos}⁡2t-\operatorname{sin}⁡2t,\,\frac{3{t}^{2}}{2},\,2t\operatorname{sin}⁡2t+\operatorname{cos}⁡2t⟩$
from  $t=0$ to $t=2.$

Coordinates: `2*t*cos(2*t)-sin(2*t)`, `3*t**2/2`, `2*t*sin(2*t)+cos(2*t)`. Interval [0,2]. Speed `5*t`. Product and chain-rule cancellations at frequency 2; Pythagorean identity and nonnegative t; direct final evaluation. Numeric endpoint-stage count: 1.

Original field shape: radio selection, five complete scalar exact expressions; no distractor-specific feedback.

### q-77064 — poly_constant

Find the arc length of the curve $r(t)=⟨10,\,\frac{{t}^{3}}{3}-t,\,{t}^{2}⟩$
from  $t=0$ to $t=3.$

Coordinates: `10`, `t**3/3-t`, `t**2`. Interval [0,3]. Speed `t**2+1`. Constant component, expanded quartic sum then perfect square; component evaluation then collection. Numeric endpoint-stage count: 2.

Original field shape: radio selection, five complete scalar exact expressions; no distractor-specific feedback.

### q-127633 — helix

Find the arc length of the curve $r(t)=⟨t,\,\operatorname{sin}⁡t,\,\operatorname{cos}⁡t⟩$
from $t=0$ to $t=1.$

Coordinates: `t`, `sin(t)`, `cos(t)`. Interval [0,1]. Speed `sqrt(2)`. Linear plus sine/cosine, constant speed; factor-out integration row and endpoint difference. Numeric endpoint-stage count: 2.

Original field shape: radio selection, five complete scalar exact expressions; no distractor-specific feedback.

### q-76909 — quadratic_three

Find the arc length of the curve $r(t)=⟨2-{t}^{2},\,{t}^{2}+4,\,\frac{{t}^{2}}{2}⟩$
from  $t=0$ to $t=4.$

Coordinates: `2-t**2`, `t**2+4`, `t**2/2`. Interval [0,4]. Speed `3*t`. Three nonzero linear velocities, perfect-square coefficient norm; direct final evaluation. Numeric endpoint-stage count: 1.

Original field shape: radio selection, five complete scalar exact expressions; no distractor-specific feedback.

### q-76910 — poly_radical

Find the arc length of the curve $r(t)=⟨\frac{4-\sqrt{3}{t}^{2}}{\sqrt{2}},\,{t}^{3},\,t+5⟩$
from  $t=0$ to $t=5.$

Coordinates: `(4-sqrt(3)*t**2)/sqrt(2)`, `t**3`, `t+5`. Interval [0,5]. Speed `1+3*t**2`. Radical polynomial derivative, quartic perfect square; component evaluation then collection. Numeric endpoint-stage count: 2.

Original field shape: radio selection, five complete scalar exact expressions; no distractor-specific feedback.

## 2. General mathematical pattern

For a displayed three-coordinate curve, differentiate each component, compute the Euclidean magnitude, simplify using a perfect-square polynomial or the Pythagorean identity with the displayed interval domain, and integrate the speed exactly between the displayed endpoints. Each source family retains its own intermediate stage masks and row count. Intervals are parameterized; fixed curves are mathematical components of these templates, not literal whole-question replay branches.

## 3. Components and complete bank mapping

The choices below are matched as whole expressions. For all non-logarithmic observed banks, scalar values underdetermine original error operations. The replay-only amplitude mapping is explicitly `v_i(a,b) = ratio_i * L(a,b)`; ratios describe the observed numerical shape, not recovered author intent. These profiles are never defaults. This is evidence preservation, not a claim that proportional perturbation teaches an error recipe. The separately authored default is a complete operation bank: correct L; half speed integral L/2; doubled speed integral 2L; omission of the norm square root ∫v²; omission of integration v(b). All five must be positive, real, unequal, and have exactly one correct value. Failure rejects the whole parameter instance.

### observed_q-33759

| Source answer UUID | Original value | Parameterized shape | Correct status |

|---|---|---|---|

| 80732c44-5634-545c-8ff4-349bbfb066cc | $\frac{1}{e} + e^{2} - 2$ | `1/b+b²−2a²` | wrong |

| 8580dd5e-760c-5889-98d9-960bbf1db32d | $e^{2} - 1$ | `b²−a²` | wrong |

| a62f4b65-d49a-56e3-9420-a6fd0017782c | $e^{2} + 1$ | `b²+a²` | wrong |

| 0730b85e-9b1c-5d8e-bd2e-6057303c06e3 | $\frac{1}{e^{2}} + e^{2} - 2$ | `1/b²+b²−2a²` | wrong |

| 1dd0a809-82f3-5432-8d1d-1a4d827a4d3d | $e^{2}$ | `ln(b/a)+b²−a²` | independently derived correct; original designation missing |

### observed_q-33779

| Source answer UUID | Original value | Parameterized shape | Correct status |

|---|---|---|---|

| 5e49651a-bdf3-5daa-a8ac-b0f9a1acf337 | $4$ | `L × (1/2)` | wrong |

| 683d57e8-3476-5871-b8ce-02f1e4add2e5 | $8\sqrt{2}$ | `L × (sqrt(2))` | wrong |

| 8f378059-5350-57fd-9b5f-1f9ef63dc60c | $8\sqrt{3}$ | `L × (sqrt(3))` | wrong |

| b4bd39a7-2f29-5a63-9c46-e2b53b0a1e5a | $8$ | `L × (1)` | correct |

| d51c476d-8e1e-5c39-9e95-2b6de637ee4f | $4\sqrt{3}$ | `L × (sqrt(3)/2)` | wrong |

### observed_q-127635

| Source answer UUID | Original value | Parameterized shape | Correct status |

|---|---|---|---|

| 12089a6a-a880-58fd-8015-e683d64044cf | $\frac{11}{6}$ | `L × (11/14)` | wrong |

| 2e79b9bf-496a-5b86-95db-3519ffcc1fd5 | $4$ | `L × (12/7)` | wrong |

| 32f21b1e-e0d3-5e8b-a4f6-207a056c3331 | $3$ | `L × (9/7)` | wrong |

| bcdb4104-831e-55b0-8287-359801a260f4 | $\frac{9}{2}$ | `L × (27/14)` | wrong |

| fcb575b0-eaae-5420-9b87-61fc65e0c4d3 | $\frac{7}{3}$ | `L × (1)` | correct |

### observed_q-76906

| Source answer UUID | Original value | Parameterized shape | Correct status |

|---|---|---|---|

| 107d5a2a-4f6f-52c4-a7ea-a3c986f47360 | $4\sqrt{2}$ | `L × (1)` | correct |

| 12208fda-53a7-5d69-9f6a-dbdffb153e06 | $8$ | `L × (sqrt(2))` | wrong |

| 768320a8-bc68-56f3-9b17-f4dad32ac2f9 | $2\sqrt{2}$ | `L × (1/2)` | wrong |

| 9381484a-6981-59d3-b123-6f51531c898a | $4$ | `L × (sqrt(2)/2)` | wrong |

| bd7ef7a7-f907-538f-b138-4c1ddb333884 | $16$ | `L × (2*sqrt(2))` | wrong |

### observed_q-76908

| Source answer UUID | Original value | Parameterized shape | Correct status |

|---|---|---|---|

| 63bfa53b-e47b-50cc-89fd-5a4e4528fce4 | $15$ | `L × (5/7)` | wrong |

| 79ea6bc3-b230-56b5-bb39-3960352c7365 | $19$ | `L × (19/21)` | wrong |

| 87e6f26e-9f09-5844-8065-ef122df54dbc | $24$ | `L × (8/7)` | wrong |

| 9e0991c3-27a4-50a9-8460-379ec4e4da59 | $10$ | `L × (10/21)` | wrong |

| d6cbc97b-38b5-54a3-92bc-84bf1dbbd503 | $21$ | `L × (1)` | correct |

### observed_q-76914

| Source answer UUID | Original value | Parameterized shape | Correct status |

|---|---|---|---|

| 4f74f6bc-5e7b-58d7-b7fc-c365ef4e92f3 | $24$ | `L × (12/5)` | wrong |

| 57499e39-7bdc-59ad-a99d-360f1fc7b2ca | $20$ | `L × (2)` | wrong |

| 6677667e-3442-5a82-af63-c15f1638bd7c | $10$ | `L × (1)` | correct |

| fd321b38-e06d-5b93-9ae1-a114b299ba87 | $6$ | `L × (3/5)` | wrong |

| fdf30511-d971-58e6-a9d7-f63d74b0483c | $18$ | `L × (9/5)` | wrong |

### observed_q-77064

| Source answer UUID | Original value | Parameterized shape | Correct status |

|---|---|---|---|

| 2b5a67bb-0704-5374-80b7-f3c08e8d80a0 | $15$ | `L × (5/4)` | wrong |

| 46234d75-8481-586d-a8d6-e8817f41182e | $12$ | `L × (1)` | correct |

| 8ba3f5f9-1429-57ca-8bd7-30d8b83aa72f | $9$ | `L × (3/4)` | wrong |

| d2b57ee9-5770-5bad-bc47-e53eff6914ec | $3$ | `L × (1/4)` | wrong |

| e992c30b-4dd9-5634-88df-cea97771fa79 | $6$ | `L × (1/2)` | wrong |

### observed_q-127633

| Source answer UUID | Original value | Parameterized shape | Correct status |

|---|---|---|---|

| a0c3c144-342c-568c-8008-dfc3bbf3e55b | $\sqrt{2}$ | `L × (1)` | correct |

| 819bb05a-265c-5492-a6f2-63e69e3366e0 | $\pi -1$ | `L × (sqrt(2)*(-1 + pi)/2)` | wrong |

| 7cc99bc0-2cfc-57b8-ad76-ee0deba98fe7 | $2\sqrt{2}-1$ | `L × (2 - sqrt(2)/2)` | wrong |

| 9773cc34-e79f-5a4a-b9ef-d818a89d1a1e | $2\pi $ | `L × (sqrt(2)*pi)` | wrong |

| e1a2a18e-b24b-5257-8c86-2b702af0f038 | $\frac{\sqrt{2}}{2}$ | `L × (1/2)` | wrong |

### observed_q-76909

| Source answer UUID | Original value | Parameterized shape | Correct status |

|---|---|---|---|

| a712676f-2c97-5cb7-966d-09797a5f8021 | $12$ | `L × (1/2)` | wrong |

| cc3eecdc-de51-5ae0-8de8-01a1ae198ae8 | $60$ | `L × (5/2)` | wrong |

| 21bd52ca-4869-53d6-8d7a-03019261b5ab | $36$ | `L × (3/2)` | wrong |

| 70e3eb1f-dcfb-53cc-99f6-b1609cba2012 | $48$ | `L × (2)` | wrong |

| f5d56a9c-d543-5f82-9abd-1d18c7ec7d92 | $24$ | `L × (1)` | correct |

### observed_q-76910

| Source answer UUID | Original value | Parameterized shape | Correct status |

|---|---|---|---|

| 4ffcfd43-b15b-55e0-9453-963134a6d995 | $130$ | `L × (1)` | correct |

| 2e9391e4-7424-54d0-a36c-f5b21aa3b4e9 | $150$ | `L × (15/13)` | wrong |

| 726ddffe-91b8-5f33-bfb8-b9930883abab | $125$ | `L × (25/26)` | wrong |

| 4048f826-7e00-5c3f-ad4e-3b51a78539bf | $75$ | `L × (15/26)` | wrong |

| 4ab3aac1-31a4-5103-a8fc-ee5e47c2090b | $90$ | `L × (9/13)` | wrong |

## 4. Reusable masks, constraints and calculations

templates.json stores prompt bound slots, complete source derivative/norm/prose masks and ordered endpoint row slots. It preserves whether an intermediate substitution row appears, whether evaluated terms are displayed before collection, and whether the source evaluates directly. No short-expression substitution is applied across coordinates, function names, exponent values or prose. The builder replaces only entire endpoint components; exponent powers remain fixed. Answers use exact SymPy integration, with no floating-point correctness test.

Bounds for polynomial/helix easy templates: half-integers from −3 through 5, increasing with span ≤5; all four speed-proportional-to-t families require a≥0. The moderate product-trig notice uses t≥0 when the lower endpoint is zero and retains t>0 for a positive lower endpoint. Moderate product-trig and hard chain-product bounds: half-integers 0 through 5 with a<b. Log-square bounds: increasing pairs from {1/2,1,2,e}. Explicit parameters enforce the same guards and are never silently resampled. These endpoint policies are authored sampling bounds, not observed source code. Interval endpoints materially change assessed integration/evaluation; constant coordinate values remain fixed and do not inflate variety counts. Mathematical fingerprints identify canonical speed and assessed interval (constant coordinates and translations do not affect the assessed operation), excluding profiles/banks/order. Content identities additionally include version, prompt, fixed solution and full bank (plot asset-path normalization is reported separately); option order/seed do not create identities.

Source anomalies and supported repairs: q-127635 and q-127633 each have an extra closing parenthesis in the first derivative tuple; q-76908 is missing a comma between derivative components in that first row. These three are presentation repairs; all original mathematics remains in evidence. Six available solutions match exactly after documented whitespace/redundant-group notation normalization; all nine match after the three presentation repairs. The q-33759 source lacks difficulty, correct ref and worked solution. Its source choice bank and prompt are preserved; correct designation and solution are explicitly authored. Independent derivation: r′=(1/t,2,2t), v²=1/t²+4+4t²=(1/t+2t)²; t>0 implies v=1/t+2t. Thus L=[ln t+t²]₁ᵉ=(1+e²)−1=e². There are nine observed correct-designation matches, not ten.

Authored defaults remain within each observed level’s method and workload. The seven easy families are unordered alternatives, moderate retains the observed explicit product-rule simplification (plus the separately assigned unrated log family), and hard retains both product/chain rules at frequency 2. Changing endpoints adds no new skill. All banks remain positive arc-length quantities; squared-speed choices can be numerically larger but are real and physically admissible lengths. No diagnosis prose has been invented.

Formatting scope guard: any hyperbolic-function notation introduced by SymPy simplification is expanded back to exponentials before learner rendering. Every prompt, solution and option is checked for forbidden sinh/cosh/tanh/coth/sech/csch notation. This preserves the source exponential notation and avoids introducing another curriculum branch.

Natural logarithms render as `\ln` throughout learner expressions and exact plot-coordinate labels. A notation guard rejects `\log` to preserve the source convention and avoid a base-10 reading.
