# Template extraction

## Stage 1: observed instances, before generalization

Every source ID, original prompt, complete bank, original solution and declared
difficulty is retained in `source.json`. The source-case parameters are in
`source-cases.json`. No source is omitted, reassigned, or repaired silently.

### q-104616: cubic (easy)

Two-variable cubic plus linear term; integer endpoints; two nonzero final terms and zero initial value.

Let $f(x,y)={x}^{3}+y.$ Given that $C$ is the path along the curve $r(t)=⟨3t,{t}^{3}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"c": 3, "scale": 1}`.

Correct scalar: $28$.

### q-104623: cycloid (easy)

Two signed polynomial products; familiar sine/cosine at 0 and pi; initial point is the origin.

Let $f(x,y)={x}^{2}y-{y}^{2}x.$ Given that $C$ is the path along the curve $r(t)=⟨t-\operatorname{sin}⁡t,1-\operatorname{cos}⁡t⟩$ for $t\in [0,\pi ],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"d": 1, "scale": 1}`.

Correct scalar: $2{\pi }^{2}-4\pi $.

### q-124002: sqrt_product (easy)

Polynomial product plus two linear terms; square-root upper parameter is a perfect square; initial value is nonzero.

Let $f(x,y)={x}^{2}{y}^{2}+x+y.$ Given that $C$ is the path along the curve $r(t)=⟨\sqrt{t},t+1⟩$ for $t\in [0,4],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"h": 1, "n": 2, "scale": 1}`.

Correct scalar: $106$.

### q-124003: exponential (easy)

Linear y factor times an exponential of a linear x input; initial y is zero; integer upper exponent.

Let $f(x,y)=y{e}^{2x}.$ Given that $C$ is the path along the curve $r(t)=⟨t,3{t}^{2}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"c": 3, "k": 2, "scale": 1}`.

Correct scalar: $3{e}^{2}$.

### q-124005: cos_linear (easy)

Cosine product plus linear x term; two nonzero endpoint values at pi/2 and pi; negative difference.

Let $f(x,y)=y\operatorname{cos}⁡x+x.$ Given that $C$ is the path along the curve $r(t)=⟨t,2t⟩$ for $t\in [\frac{\pi }{2},\pi ],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"c": 2, "scale": 1}`.

Correct scalar: $-\frac{3\pi }{2}$.

### q-104624: quadratic (easy)

Linear y plus squared x; shifted second curve coordinate; nonzero initial value; evaluated-square sum preserved.

Let $f(x,y)=y+{x}^{2}.$ Given that $C$ is the path along the curve $r(t)=⟨2t,{t}^{2}-1⟩$ for $t\in [0,2],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"b": 2, "c": 2, "h": 1, "scale": 1}`.

Correct scalar: $20$.

### q-104637: zero_ellipse (easy)

Polynomial/exponential product; ellipse endpoints each have a vanishing polynomial factor; result zero without computing an integral.

Let $f(x,y)=y{x}^{2}{e}^{xy}.$ Given that $C$ is the path along the curve $r(t)=⟨\operatorname{cos}⁡t,2\operatorname{sin}⁡t⟩$ for $t\in [0,\frac{\pi }{2}],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"c": 1, "d": 2, "scale": 1}`.

Correct scalar: $0$.

### q-99008: trig3 (moderate)

Three variables; two trigonometric products; upper inputs pi/2 and pi; signed cosine product retained before final simplification.

Let $f(x,y,z)=x\operatorname{sin}⁡y+y\operatorname{cos}⁡z.$ Given that $C$ is the path along the curve $r(t)=⟨\operatorname{sin}⁡t,t,2t⟩$ for $t\in [0,\frac{\pi }{2}],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"c": 1, "d": 2, "scale": 1}`.

Correct scalar: $1-\frac{\pi }{2}$.

### q-104640: helix (moderate)

Three variables; polynomial product and sine product; full-turn endpoints share x/y but z changes; vanished sine term remains visible.

Let $f(x,y,z)={x}^{2}z+x\operatorname{sin}⁡y.$ Given that $C$ is the path along the curve $r(t)=⟨\operatorname{cos}⁡t,\operatorname{sin}⁡t,t⟩$ for $t\in [0,2\pi ],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"c": 1, "d": 1, "scale": 1}`.

Correct scalar: $2\pi $.

### q-124008: exp_sum (moderate)

Sum of three exponentials; polynomial coordinates with small integer upper inputs; three initial exponentials each equal one.

Let $f(x,y,z)={e}^{x}+{e}^{y}+{e}^{z}.$ Given that $C$ is the path along the curve $r(t)=⟨t,{t}^{2},2{t}^{3}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"c": 1, "d": 1, "k": 2, "scale": 1}`.

Correct scalar: ${e}^{2}+2e-3$.

### q-104638: exp_product (moderate)

y times exponential of xz; quadratic coordinates with z=0 at both endpoints; signed y values give a subtraction of a negative.

Let $f(x,y,z)=y{e}^{xz}.$ Given that $C$ is the path along the curve $r(t)=⟨{t}^{2}+1,{t}^{2}-1,{t}^{2}-2t⟩$ for $t\in [0,2],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"b": 2, "h": 1, "k": 1, "scale": 1}`.

Correct scalar: $4$.

### q-104639: monomial3 (moderate)

Three-variable product with powers 1,2,3; polynomial curve powers 2,4,6; all initial factors vanish; simple upper products.

Let $f(x,y,z)=x{y}^{2}{z}^{3}.$ Given that $C$ is the path along the curve $r(t)=⟨{t}^{2},{t}^{4},{t}^{6}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

Original parameters: `{"c": 1, "d": 1, "k": 1, "scale": 1}`.

Correct scalar: $1$.

## Stage 2: shared pattern and instructional purpose

The learner receives a scalar potential f and an oriented parameter interval.
Evaluate the supplied curve at the two parameter endpoints, substitute both
coordinate tuples into f, and subtract the initial potential value from the
final one. The response is an exact scalar, never a gradient, an integral setup,
a parametrization, or a reconstructed potential. The full theorem statement,
endpoint table, endpoint-coordinate sentence and final equality chain remain.
Families remain distinct because the potential operators, curve forms,
simplification regimes and arithmetic rows differ. Numeric coefficients within
a family are variants of the same method, not new recovered templates.

## Stage 3: components and complete observed choice banks

Every bank below belongs to the source `selection` field. Its parameterized
component recipe is **lambda times the complete displayed scalar expression**;
the prompt potential is also lambda times the original potential. This is a
homogeneous potential-scaling replay profile. Its interpretation is intentionally
limited: one scalar distractor does not recover the original mistake algorithm.
These are observed component patterns, not claims of inferred author intent.
The curve and interval stay at their original values in `observed_scale`.
Changing them is rejected explicitly. No unrelated polynomial fit or random
perturbation is used. All five expressions travel together as one complete bank.

### cubic / observed_scale / q-104616

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `00980506-979a-5a3c-bb6b-3b50f009bfac` | $8$ | $\lambda(8)$ | false |
| `1aeef040-2421-5b1c-b55a-b92ee77dadcc` | $32$ | $\lambda(32)$ | false |
| `5daedb86-7dd6-576d-aff0-8f7b1f0062ec` | $28$ | $\lambda(28)$ | true |
| `a2214f1f-3631-5be2-85e4-d5102a1c44c0` | $10$ | $\lambda(10)$ | false |
| `d6de32bd-280a-5c5a-aa34-19f1b3faadf0` | $21$ | $\lambda(21)$ | false |

Replay validates 5/5 mathematical option values and the designation.

### cycloid / observed_scale / q-104623

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `0a528a36-e97e-5732-8fae-1697a81d8ff0` | ${\pi }^{2}+2\pi $ | $\lambda({\pi }^{2}+2\pi )$ | false |
| `44bbd131-4ecd-540b-ad14-259cefa4dcf3` | ${\pi }^{2}-1$ | $\lambda({\pi }^{2}-1)$ | false |
| `4ab4b784-0b5f-5e1b-9fde-ec17a7e2873d` | $\pi +2$ | $\lambda(\pi +2)$ | false |
| `89f290a7-499e-5b23-8f65-ac96513f25dc` | $0$ | $\lambda(0)$ | false |
| `ecb83a5e-cf58-56d7-bc9a-928b68a83802` | $2{\pi }^{2}-4\pi $ | $\lambda(2{\pi }^{2}-4\pi )$ | true |

Replay validates 5/5 mathematical option values and the designation.

### sqrt_product / observed_scale / q-124002

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `302b8581-4a68-5c5c-8795-9744e9d4a2d4` | $76$ | $\lambda(76)$ | false |
| `953e0310-1f6a-5dcb-9428-9966108f8f1b` | $98$ | $\lambda(98)$ | false |
| `b72e2f4d-4041-5680-a701-550b3147bc12` | $87$ | $\lambda(87)$ | false |
| `ca82cadd-75e5-598b-bacc-17ec432f7824` | $109$ | $\lambda(109)$ | false |
| `f5b95c82-3200-5da8-b666-432aa9c1aa8c` | $106$ | $\lambda(106)$ | true |

Replay validates 5/5 mathematical option values and the designation.

### exponential / observed_scale / q-124003

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `0eea1d61-c31a-52a0-9c80-b705eeabdf54` | $3e+1$ | $\lambda(3e+1)$ | false |
| `32a24c80-640c-5f96-9d30-3886433c358a` | $3+e$ | $\lambda(3+e)$ | false |
| `89fe846b-c77b-5114-acc8-ae328a43149b` | $3e$ | $\lambda(3e)$ | false |
| `d080e35c-13c8-5910-bdbc-1433606170a0` | $3{e}^{2}$ | $\lambda(3{e}^{2})$ | true |
| `de2288dd-737a-5b6e-99cf-5d7174075a26` | ${e}^{2}-1$ | $\lambda({e}^{2}-1)$ | false |

Replay validates 5/5 mathematical option values and the designation.

### cos_linear / observed_scale / q-124005

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `0bb8367f-a159-5457-99f5-50133f64eb7d` | $-\frac{3\pi }{4}$ | $\lambda(-\frac{3\pi }{4})$ | false |
| `0fa182ef-4a0a-5db2-a08b-55a80052cb00` | $\frac{\pi }{4}$ | $\lambda(\frac{\pi }{4})$ | false |
| `228efe5e-c3c4-564d-9dab-7a9a4edeb67d` | $-2\pi $ | $\lambda(-2\pi )$ | false |
| `3b05dbc7-a00e-579d-9183-316aebb35c95` | $\frac{\pi }{2}$ | $\lambda(\frac{\pi }{2})$ | false |
| `4e044364-8237-5de2-8e2f-2b3e611819bc` | $-\frac{3\pi }{2}$ | $\lambda(-\frac{3\pi }{2})$ | true |

Replay validates 5/5 mathematical option values and the designation.

### quadratic / observed_scale / q-104624

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `12811091-da24-5f9e-a3cc-d521c187f782` | $15$ | $\lambda(15)$ | false |
| `48539c5b-fd63-583d-8da2-566a4dd6e0bb` | $24$ | $\lambda(24)$ | false |
| `a1d2cb1e-5c01-5454-b9f6-ddf29ce394b3` | $12$ | $\lambda(12)$ | false |
| `b864bbf5-46ca-5a26-aa58-751cd0107a9b` | $6$ | $\lambda(6)$ | false |
| `cdf966f8-fa1b-5eaf-ab84-b21f9b032f94` | $20$ | $\lambda(20)$ | true |

Replay validates 5/5 mathematical option values and the designation.

### zero_ellipse / observed_scale / q-104637

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `1e6f935a-7227-56de-9d74-d58f3261b90a` | ${\pi }^{2}-2$ | $\lambda({\pi }^{2}-2)$ | false |
| `376dde01-d46a-5414-9e84-a7d099ab2f33` | $0$ | $\lambda(0)$ | true |
| `75de655b-bac7-5de2-9e4c-ce56729e4a3e` | $\pi {e}^{2\pi }$ | $\lambda(\pi {e}^{2\pi })$ | false |
| `87f317ce-1ebd-53fe-bd1c-2786b6ebd37d` | ${\pi }^{2}{e}^{{\pi }^{2}}$ | $\lambda({\pi }^{2}{e}^{{\pi }^{2}})$ | false |
| `db14b874-47ec-5b46-a18d-4f53face6c8f` | $\frac{{\pi }^{2}}{4}$ | $\lambda(\frac{{\pi }^{2}}{4})$ | false |

Replay validates 5/5 mathematical option values and the designation.

### trig3 / observed_scale / q-99008

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `1f63d9a1-0137-5a36-bb60-9969b4573aad` | $\pi +1$ | $\lambda(\pi +1)$ | false |
| `3699a6b4-d4d9-5e31-b162-16c5007ee57b` | $1-\frac{\pi }{2}$ | $\lambda(1-\frac{\pi }{2})$ | true |
| `89c4b85e-187b-55d0-84b5-4705fe0ffb20` | $1-\pi $ | $\lambda(1-\pi )$ | false |
| `be1533c1-05ff-53d2-b2f2-b8184c361484` | $\frac{\pi }{3}$ | $\lambda(\frac{\pi }{3})$ | false |
| `fd0d25c8-b49e-5a74-a54a-3eb3215a8c89` | ${\pi }^{2}$ | $\lambda({\pi }^{2})$ | false |

Replay validates 5/5 mathematical option values and the designation.

### helix / observed_scale / q-104640

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `1e699747-9682-50ad-bc3c-89217394ac15` | $0$ | $\lambda(0)$ | false |
| `2607fd46-ddb8-5e68-96ad-e64aed38f812` | ${\pi }^{2}$ | $\lambda({\pi }^{2})$ | false |
| `897eb260-f9ce-5892-bb70-7962baeb2fe3` | $2$ | $\lambda(2)$ | false |
| `95fcd466-856f-5f24-95dd-68c6e3fb2527` | $2\pi $ | $\lambda(2\pi )$ | true |
| `e5429a9a-ce6f-502f-af4d-a0421c2ce2a3` | $\pi +1$ | $\lambda(\pi +1)$ | false |

Replay validates 5/5 mathematical option values and the designation.

### exp_sum / observed_scale / q-124008

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `543ba384-51b6-557c-bf16-43ac82ca0e5d` | ${e}^{2}+3e$ | $\lambda({e}^{2}+3e)$ | false |
| `bfd16522-1981-538e-a666-611647c995ff` | $3{e}^{2}-2$ | $\lambda(3{e}^{2}-2)$ | false |
| `e2c6cd51-6e8f-5103-b8e1-9cf9c4743823` | ${e}^{2}+2e-3$ | $\lambda({e}^{2}+2e-3)$ | true |
| `ebc320e3-b118-5e6b-bdc4-5e336a48b133` | ${e}^{2}-2$ | $\lambda({e}^{2}-2)$ | false |
| `f7bffceb-ddbe-55f4-ac78-cfd9d1162748` | $3e-3$ | $\lambda(3e-3)$ | false |

Replay validates 5/5 mathematical option values and the designation.

### exp_product / observed_scale / q-104638

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `10c8a508-1d4a-574f-bb45-6efb1ced71fc` | $e$ | $\lambda(e)$ | false |
| `47d59bce-11d1-59ca-a980-8662920cfd55` | $0$ | $\lambda(0)$ | false |
| `cdbbdd8b-85ea-5741-9623-bb79a02c5a1c` | $4$ | $\lambda(4)$ | true |
| `d992fc1d-6425-5951-9f5f-b0d131ab532a` | $3{e}^{2}$ | $\lambda(3{e}^{2})$ | false |
| `e72ad3e5-d9a9-5e06-b65e-7fe892762e86` | $5{e}^{6}$ | $\lambda(5{e}^{6})$ | false |

Replay validates 5/5 mathematical option values and the designation.

### monomial3 / observed_scale / q-104639

| Source answer UUID | Original scalar | Recipe | Correct? |
|---|---|---|---|

| `2ceeb53b-391b-5fef-9ab5-1097ef938825` | $0$ | $\lambda(0)$ | false |
| `2f083f8e-a1a4-56c3-aea6-e98468b6122b` | $1$ | $\lambda(1)$ | true |
| `b6b875c4-e194-5a11-823c-e0a27f17aa6c` | $36$ | $\lambda(36)$ | false |
| `cc5489e8-7985-5f2a-b47e-2c5f4e8a4b10` | $8$ | $\lambda(8)$ | false |
| `d782c18b-724f-503c-9bd1-3a2cfd6e6827` | $64$ | $\lambda(64)$ | false |

Replay validates 5/5 mathematical option values and the designation.

## Stage 4: reusable Markdown/value recipes

The observed prompt has a slot for the **entire potential expression**; all
other observed prompt components are retained. The solution is split into its
original endpoint table and final equality-row components. The theorem row and
endpoint f-call row stay unscaled because f already names the scaled potential;
each numerical substitution/simplification row scales by lambda. This same
recipe runs at lambda=1, -2 and 3; there is no literal source-question return
branch and no answer lookup. Choice values are calculated from symbolic bank
expressions, with equivalent standard SymPy TeX normalization.

Normal generation uses authored complete operation banks. Its source families
vary the named curve parameters below while preserving familiar trigonometric
inputs, perfect-square root inputs, zero-product regimes and small integer
exponential arguments. Normal solution rows retain the family sequence: theorem
substitution → tuple substitution → expanded potential arithmetic → family
arithmetic simplification → final scalar. Zero ellipse has no redundant penultimate
zero row, as in its source. Cubic/quadratic retain their evaluated-power sums;
trig3 retains the cosine value -1 in its product; helix retains its zero sine
term; exp_sum collects equal exponentials and evaluates initial exponentials;
exp_product retains subtraction-of-negative simplification. All source sentence
blocks are reused, without distractor-specific feedback.

| Family | Authored parameter bounds (integers) |
|---|---|

| cubic | c=1..4 |
| cycloid | d=1..3 |
| sqrt_product | n=1..3, h=-2..3 |
| exponential | k=1..3, c=1..4 |
| cos_linear | c=1..4 |
| quadratic | c=1..3, b=1..3, h=-2..3 |
| zero_ellipse | c=1..3, d=1..4 |
| trig3 | c=1..3, d=2..2 |
| helix | c=1..3, d=1..3 |
| exp_sum | c=1..2, d=1..2, k=1..3 |
| exp_product | b=1..3, h=1..3, k=1..3 |
| monomial3 | c=1..2, d=1..2, k=1..2 |
| reciprocal_exp | a=-3..3, b=-3..3, h=1..3, end=1..2 |
| reciprocal_product | a=-3..3, b=-3..3, h=1..3, end=1..2 |

All observed families additionally have nonzero integer scale in -4..4 for
explicit requests; normal random scale is ±1, ±2 or ±3. Hard random scale is
one; explicit hard scaling must still keep both **displayed** potential
coefficients in magnitude 1..3, including the product of scale with A/B.
Scale is a potential coefficient, not a cosmetic answer change: it appears in
the displayed potential and every numerical substitution. Signed magnitude
bounds are enforced on explicit parameters. Parameters with invalid complete
banks fail; random generation rejects the entire bank and resamples. It never
replaces a single invalid option from a pool. Some admissible mathematical
parameter tuples have colliding operation banks and are therefore ineligible.

The authored banks are separate from observed replay. Operations include reverse
orientation, use the initial point twice, omit a potential term/power, add
endpoint values instead of subtracting, change a power or exponential input, and confuse
parameter values with endpoint coordinates for the vanishing-product family.
`generation.distractor_recipes` records the exact resulting symbolic scalar and
the operation for every owned answer. These diagnoses are author metadata only.

### Authored hard scope and equal-level workload

The canonical example e-8759 supplies a two-term potential xy²+2xz on
<e^t,t,e^-t>. The hard authored families keep that supplied-potential theorem
method and its reciprocal exponential coordinates, with r=<e^t,t+h,e^-t>,
h=1..3 and interval [0,end], end=1 or 2. Potentials are Axy²+Byz and
Axy²+Bxyz, with 1≤|A|,|B|≤3. Both require the same two 3D endpoint
substitutions, **four nonzero additive contributions before cancellation**,
simple exponential/product simplification, and one signed endpoint difference.
The nonzero h and coefficients prevent a defining contribution from disappearing.
Both families are equal-level variants, not a progression. Each term is checked
independently at each endpoint in validation. These are authored difficulty
claims anchored to the canonical example, lesson route and prerequisites;
there are no observed hard source labels to replay. No direct integration,
potential reconstruction, implicit-curve parametrization, unfamiliar trig
evaluation or arbitrary large algebra is introduced to manufacture hard work.

### Domain and provenance limitations

All potentials are globally smooth on real coordinates. The square-root family
uses t≥0 and a perfect-square upper endpoint. Its geometric path admits the
smooth reparametrization u=sqrt(t), so the endpoint theorem remains applicable
even though the supplied square-root parameter derivative is unbounded at 0.
Observed distractor intentions remain underdetermined; only their mathematical
homogeneous component recipes are claimed. Source numeric/choice and full
solution-sequence fidelity are separate from independent displayed mathematics
and native ID grading. No plots occur, so steps 5 and 7 have no renderer.

