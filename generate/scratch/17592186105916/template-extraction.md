# Four-stage template extraction

## 1. Describe each original

All prompts supply a positive exact magnitude and a familiar angle between named vectors, then ask for the scalar projection of the first onto the second. Angles observed: 30°,45°,60°,90°,120°,135°,150°, including their radian forms. Magnitudes are integers or integer multiples of sqrt2/sqrt3. Names carry direction roles but renaming does not create a mathematical task. Blank prompts supply `comp_b a=` and the exact matching `{{field-1}}`; radios use key selection. Each complete bank is listed below; missing attributes are retained.

### q-19136 / legacy_radio

Suppose $\mid c|= 14$ and the angle between vectors $c$ and $d$ is $θ = 60^{∘}$. Find the scalar projection of $c$ onto $d$.

Magnitude coefficient 14, radicand 1, angle 60°, display degrees. Correct reference **absent**; worked solution **absent**; difficulty **absent (unrated)**.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| selection / 1 | `$7$` | `M * (1/2)` | unmarked |
| selection / 2 | `$\frac{7}{2}$` | `M * (1/4)` | unmarked |
| selection / 3 | `$7\sqrt{3}$` | `M * (sqrt(3)/2)` | unmarked |
| selection / 4 | `$14$` | `M * (1)` | unmarked |
| selection / 5 | `$-7$` | `M * (-1/2)` | unmarked |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-71532 / radio_operator

Suppose $|\,c\,|=18$ and the angle between vectors $c$ and $d$ is $\theta =\frac{3\pi }{4}.$ Find the scalar projection of $c$ onto $d.$

Magnitude coefficient 18, radicand 1, angle 135°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| selection / 1 | `$-9\sqrt{2}$` | `M * (-sqrt(2)/2)` | correct |
| selection / 2 | `$9$` | `M * (1/2)` | incorrect |
| selection / 3 | `$-\frac{9\sqrt{2}}{2}$` | `M * (-sqrt(2)/4)` | incorrect |
| selection / 4 | `$-9$` | `M * (-1/2)` | incorrect |
| selection / 5 | `$9\sqrt{2}$` | `M * (sqrt(2)/2)` | incorrect |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-101522 / radio_operator

Suppose $|\,a\,|=14$ and the angle between vectors $a$ and $b$ is $\theta =\frac{2\pi }{3}.$ Find the scalar projection of $a$ onto $b.$

Magnitude coefficient 14, radicand 1, angle 120°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| selection / 1 | `$-7\sqrt{2}$` | `M * (-sqrt(2)/2)` | incorrect |
| selection / 2 | `$-14$` | `M * (-1)` | incorrect |
| selection / 3 | `$-7$` | `M * (-1/2)` | correct |
| selection / 4 | `$14$` | `M * (1)` | incorrect |
| selection / 5 | `$7$` | `M * (1/2)` | incorrect |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-101523 / radio_operator

Suppose $|\,p\,|=10\sqrt{2}$ and the angle between vectors $p$ and $q$ is $\theta ={45}^{∘}.$ Find the scalar projection of $p$ onto $q.$

Magnitude coefficient 10, radicand 2, angle 45°, display degrees. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| selection / 1 | `$10$` | `M * (sqrt(2)/2)` | correct |
| selection / 2 | `$5\sqrt{6}$` | `M * (sqrt(3)/2)` | incorrect |
| selection / 3 | `$5\sqrt{2}$` | `M * (1/2)` | incorrect |
| selection / 4 | `$0$` | `M * (0)` | incorrect |
| selection / 5 | `$10\sqrt{2}$` | `M * (1)` | incorrect |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-126498 / radio_operator

Suppose $|\,c\,|=5$ and the angle between vectors $c$ and $d$ is $\theta =\frac{\pi }{2}.$ Find the scalar projection of $c$ onto $d.$

Magnitude coefficient 5, radicand 1, angle 90°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| selection / 1 | `$-5$` | `M * (-1)` | incorrect |
| selection / 2 | `$0$` | `M * (0)` | correct |
| selection / 3 | `$5$` | `M * (1)` | incorrect |
| selection / 4 | `$\frac{5}{2}$` | `M * (1/2)` | incorrect |
| selection / 5 | `$-\frac{5}{2}$` | `M * (-1/2)` | incorrect |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-275243 / blank_operator

Suppose $|\,c\,|=4$ and the angle between vectors $c$ and $d$ is $\theta =\frac{\pi }{2}.$ Find the scalar projection of $c$ onto $d.$

${\text{comp}}_{d}\,c=$
{{field-1}}

Magnitude coefficient 4, radicand 1, angle 90°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| field-1 / 1 | `$0$` | `M * (0)` | correct |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-318964 / blank_operator

Suppose $|\,k\,|=2\sqrt{2}$ and the angle between vectors $k$ and $l$ is $\theta ={120}^{∘}.$ Find the scalar projection of $k$ onto $l.$

${\text{comp}}_{l}\,k=$
{{field-1}}

Magnitude coefficient 2, radicand 2, angle 120°, display degrees. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| field-1 / 1 | `$-\sqrt{2}$` | `M * (-1/2)` | correct |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-318971 / blank_plain

Suppose $|\,r\,|=10$ and the angle between vectors $r$ and $s$ is $\theta =\frac{2\pi }{3}.$ Find the scalar projection of $r$ onto $s.$

${\text{comp}}_{s}\,r=$
{{field-1}}

Magnitude coefficient 10, radicand 1, angle 120°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| field-1 / 1 | `$-5$` | `M * (-1/2)` | correct |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-318972 / blank_plain

Suppose $|\,p\,|=8$ and the angle between vectors $p$ and $q$ is $\theta =\frac{\pi }{6}.$ Find the scalar projection of $p$ onto $q.$

${\text{comp}}_{q}\,p=$
{{field-1}}

Magnitude coefficient 8, radicand 1, angle 30°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| field-1 / 1 | `$4\sqrt{3}$` | `M * (sqrt(3)/2)` | correct |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-318975 / blank_plain

Suppose $|\,t\,|=\sqrt{2}$ and the angle between vectors $t$ and $u$ is $\theta =\frac{3\pi }{4}.$ Find the scalar projection of $t$ onto $u.$

${\text{comp}}_{u}\,t=$
{{field-1}}

Magnitude coefficient 1, radicand 2, angle 135°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| field-1 / 1 | `$-1$` | `M * (-sqrt(2)/2)` | correct |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-318976 / blank_plain_have

Suppose $|\,r\,|=3\sqrt{3}$ and the angle between vectors $r$ and $s$ is $\theta =\frac{\pi }{2}.$ Find the scalar projection of $r$ onto $s.$

${\text{comp}}_{s}\,r=$
{{field-1}}

Magnitude coefficient 3, radicand 3, angle 90°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| field-1 / 1 | `$0$` | `M * (0)` | correct |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-71527 / radio_operator

Suppose $|\,p\,|=\sqrt{3}$ and the angle between vectors $p$ and $q$ is $\theta =\frac{\pi }{6}.$ Find the scalar projection of $p$ onto $q.$

Magnitude coefficient 1, radicand 3, angle 30°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| selection / 1 | `$3$` | `M * (sqrt(3))` | incorrect |
| selection / 2 | `$\frac{3}{2}$` | `M * (sqrt(3)/2)` | correct |
| selection / 3 | `$\frac{3}{4}$` | `M * (sqrt(3)/4)` | incorrect |
| selection / 4 | `$\sqrt{3}$` | `M * (1)` | incorrect |
| selection / 5 | `$\frac{\sqrt{3}}{2}$` | `M * (1/2)` | incorrect |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-71530 / radio_operator

Suppose $|\,p\,|=3\sqrt{2}$ and the angle between vectors $p$ and $q$ is $\theta =\frac{\pi }{4}.$ Find the scalar projection of $p$ onto $q.$

Magnitude coefficient 3, radicand 2, angle 45°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| selection / 1 | `$\frac{3\sqrt{2}}{2}$` | `M * (1/2)` | incorrect |
| selection / 2 | `$6$` | `M * (sqrt(2))` | incorrect |
| selection / 3 | `$\frac{3}{2}$` | `M * (sqrt(2)/4)` | incorrect |
| selection / 4 | `$-3$` | `M * (-sqrt(2)/2)` | incorrect |
| selection / 5 | `$3$` | `M * (sqrt(2)/2)` | correct |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-19135 / radio_operator

Suppose $|\,a\,|=8$ and the angle between vectors $a$ and $b$ is $\theta ={120}^{∘}.$ Find the scalar projection of $a$ onto $b.$

Magnitude coefficient 8, radicand 1, angle 120°, display degrees. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| selection / 1 | `$4\sqrt{2}$` | `M * (sqrt(2)/2)` | incorrect |
| selection / 2 | `$-4\sqrt{3}$` | `M * (-sqrt(3)/2)` | incorrect |
| selection / 3 | `$-4$` | `M * (-1/2)` | correct |
| selection / 4 | `$-4\sqrt{2}$` | `M * (-sqrt(2)/2)` | incorrect |
| selection / 5 | `$4$` | `M * (1/2)` | incorrect |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-318969 / blank_plain

Suppose $|\,m\,|=12$ and the angle between vectors $m$ and $n$ is $\theta =\frac{\pi }{4}.$ Find the scalar projection of $m$ onto $n.$

${\text{comp}}_{n}\,m=$
{{field-1}}

Magnitude coefficient 12, radicand 1, angle 45°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| field-1 / 1 | `$6\sqrt{2}$` | `M * (sqrt(2)/2)` | correct |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-71528 / radio_operator

Suppose $|\,c\,|=10$ and the angle between vectors $c$ and $d$ is $\theta =\frac{\pi }{3}.$ Find the scalar projection of $c$ onto $d.$

Magnitude coefficient 10, radicand 1, angle 60°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| selection / 1 | `$\frac{5}{2}$` | `M * (1/4)` | incorrect |
| selection / 2 | `$-5$` | `M * (-1/2)` | incorrect |
| selection / 3 | `$5\sqrt{3}$` | `M * (sqrt(3)/2)` | incorrect |
| selection / 4 | `$5$` | `M * (1/2)` | correct |
| selection / 5 | `$\frac{5\sqrt{3}}{2}$` | `M * (sqrt(3)/4)` | incorrect |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

### q-71533 / radio_operator

Suppose $|\,p\,|=2$ and the angle between vectors $p$ and $q$ is $\theta =\frac{5\pi }{6}.$ Find the scalar projection of $p$ onto $q.$

Magnitude coefficient 2, radicand 1, angle 150°, display radians. Correct reference present; worked solution present; difficulty easy.

| Source field / choice | Exact displayed value | Parameterized evidence operation | Correct designation |
|---|---|---|---|
| selection / 1 | `$\sqrt{3}$` | `M * (sqrt(3)/2)` | incorrect |
| selection / 2 | `$-\frac{\sqrt{3}}{2}$` | `M * (-sqrt(3)/4)` | incorrect |
| selection / 3 | `$1$` | `M * (1/2)` | incorrect |
| selection / 4 | `$-\sqrt{3}$` | `M * (-sqrt(3)/2)` | correct |
| selection / 5 | `$-1$` | `M * (-1/2)` | incorrect |

Historical scalar-ratio intent is unresolved; it is a homogeneous evidence expression, not an inferred learner error. Correctness separately checks M cosθ.

## 2. Shared pattern

Compute comp_b a = |a| cosθ as an exact signed scalar. Supplied magnitude is the magnitude of the projected vector, never of the vector projected onto. Degree/radian representations use the same familiar angle domain. Each instance has one fixed solution independent of which wrong answer is chosen.

## 3. Components and complete banks

The per-source table above maps every option to its owned field and complete original profile. Ten radio profiles contain five homogeneous scalar patterns; seven blanks contain one scalar. No bank is mixed with another. Every public raw profile is labeled evidence_only=true and eligible_for_learning=false, including the malformed missing-reference original. Changing M proportionally changes every historical answer through these expressions; no literal source-payload return or correct-answer lookup is used. Source parameter replay constructs the actual prompt and solution from complete mathematical slots. The normal banks are authored method extensions:

| Profile | Complete operations | Conditions |
|---|---|---|
| trig_signed | M cosθ, M sinθ, -M cosθ, M, cosθ | nonright angle; complete exact-value uniqueness |
| trig_denominator | M cosθ, -M cosθ, 2M cosθ, cosθ, M/2 | nonright angle; complete exact-value uniqueness |
| right_angle | 0, M, -M, M/2, -M/2 | θ=90°, easy only |
| blank | M cosθ | scalar fragment |

Sine replaces cosine; sign reversal loses/changes the projection sign; M omits cosine; cosθ omits magnitude; 2M cosθ omits the denominator 2 from the familiar cosine; M/2 uses the wrong familiar cosine cos60°. These operations apply to the actual method. Intent is authored, not attributed to the historical bank. Each profile is chosen before parameters; any equality rejects the whole instance. In particular sine/cosine collide at45°, so trig_signed rejects that complete bank. Sampling does not pick first-valid members from a pool.

## 4. Reusable masks and bounds

The generator renders magnitude, complete angle, projected-vector name and onto-vector name as independent slots. Shared original prose remains fixed: “Using the formula for the scalar projection, we obtain” (or the observed “we have”). The four structural stages are generic formula -> magnitude*cos(actual angle) -> magnitude*exact cosine -> simplified scalar. Operator-cos and plain-cos spellings remain separate masks. Negative exact cosines retain parentheses; rational/radical factors are rendered with explicit cdot. The original legacy prompt retains its spacing and absent solution. Actual original strings are byte-exact at source parameters; no presentation normalization is required.

Every explicit input and sampler uses the same exact reduced-rational, radicand, familiar-angle and level workload guards. Coefficients are positive reduced rationals with numerator <=24 and denominator <=4. Easy denominator=1. Moderate denominator>1, radicand=1, nonright angle. Hard denominator>1 and crossed radical only: radicand2 with30°/150°, radicand3 with45°/135°. Float coefficients and nonstandard angles are rejected. The numerator ceiling retains observed magnitudes2–18 and adds same-workload small coefficients for repeat practice. Standard exact cosine evaluation is never replaced with approximate or arbitrary-angle trigonometry.

Normal defaults choose among all four supported nonlegacy source-shaped masks before parameters and select an eligible complete method bank. Degree/radian and vector-letter aliases affect content identity but not mathematical fingerprint. The mathematical fingerprint excludes profile, choice order, field layout and onto-vector letters. At90° the supplied magnitude is incidental to the zero result and is excluded as well. Complete prompt, solution, difficulty, bank and optional-key presence determine content identity; changing seed or shuffling alone does not. Enumeration and sampled coverage are reported in validation.json.
