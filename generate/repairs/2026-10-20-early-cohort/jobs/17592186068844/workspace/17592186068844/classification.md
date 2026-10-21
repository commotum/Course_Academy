# Classification

Captured math database basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All eleven practice questions are rated easy; all use one radio field keyed `selection`, five complete-equation math choices, and one correct ref. There are eleven observed Markdown/value templates and eleven complete observed bank profiles. Moderate/hard have no practice sources. Canonical e-10997 is context, not a twelfth practice source.

Plot rating: **none** for every template, prompt, bank and solution. No images or plot asset references occur.

## Ordered lesson context

Following `activity/first-step` and then `step/next` gives Introduction (17592186069783) → First-Order Separable Equations (17592186069784) → Separating the Variables (17592186069787/KP68842) → Implicit Form (17592186069789/KP68844) → Explicit Form (17592186069785/KP68840) → Rearranging Then Integrating (17592186069786/KP68841). This order differs from the Pull array order. The lesson defines separation as A(y)y′=B(x), requires g(y)≠0, and integrates by substitution. Our output stops at the implicit relation; inversion and rearranged-equation entry belong to siblings. The canonical source integrates y dy=x dx, then absorbs 2K into C.

## Observed families

- `exp_linear`: q-154359 / db 17592186069078; easy, radio×5, 6 aligned equalities; one final displayed relation; plots none.

- `arcsin_autonomous`: q-154367 / db 17592186069079; easy, radio×5, 6 aligned equalities; one final displayed relation; plots none.

- `tan_exp`: q-118885 / db 17592186253525; easy, radio×5, 7 aligned equalities; one final displayed relation; plots none.

- `log_exp`: q-14246 / db 17592186272345; easy, radio×5, 6 aligned equalities; one final displayed relation; plots none.

- `tan_autonomous`: q-154357 / db 17592186275322; easy, radio×5, 6 aligned equalities; one final displayed relation; plots none.

- `power_cube`: q-154361 / db 17592186275323; easy, radio×5, 7 aligned equalities; one final displayed relation; plots none.

- `exp_affine`: q-154369 / db 17592186275324; easy, radio×5, 5 aligned equalities; one final displayed relation; plots none.

- `root_power`: q-154373 / db 17592186275325; easy, radio×5, 8 aligned equalities; one final displayed relation; plots none.

- `sin_poly`: q-158035 / db 17592186275423; easy, radio×5, 6 aligned equalities; one final displayed relation; plots none.

- `sec_log`: q-158116 / db 17592186275450; easy, radio×5, 6 aligned equalities; one final displayed relation; plots none.

- `log_sin`: q-158117 / db 17592186275451; easy, radio×5, 6 aligned equalities; one final displayed relation; plots none.

## Authored missing levels

Moderate `two_x_terms`: y′=(a x²+b)/y²; a=2..6 and b∈{-5,…,-1,1,…,5}. Separate, integrate two x components and one y power, retain C, and stop. Hard `two_sided_terms`: y′=(a x²+b)/(y²+d), same a,b bounds, d=1..5. Integrate two components on each side; the positive d prevents a singular denominator. These are design labels, not recovered source ratings. The source monomial and affine examples, canonical constant absorption, and lesson formal integration support this bounded termwise extension. No new integration method, IVP, or explicit branch inversion is introduced. Both levels require every listed term; explicit inputs cannot remove them. Within each level, coefficients change the same number of primitive evaluations.

Easy translation policy: h,k∈[-6,6] integers; x↦x+h, y↦y+k. Autonomous sources have h=0 since an x constant shift is absorbed into C and has no ODE effect. Unit-slope translations keep primitive types and complete ordered source stages. This is an authored sampling policy, not recovered original ranges.

## Evidence and repairs

No field-format anomalies or ambiguous banks were found. Explicit y=… choices are legitimate wrong response forms and are also checked against the ODE; they are not source ambiguities. q-158116 says -π/2<y<π/2, but sec(y)tan(y)=0 at y=0. The original bank, prompt and solution remain exact in the observed public profile. The standard prompt adds y+k≠0, and all metadata defines the connected admissible branches. Natural real domains such as x+h≥0,y+k>0 for root_power and cos(y+k)≠0 for sin_poly are independently enforced in interpretation.

Raw observed wrong choices may have extra restrictions: q-14246 includes ln|x| and e^(sqrt(x)); q-154357 includes sqrt(x) and tan(x); q-158035 includes 1/x³; q-158117 includes sec(x). These restrictions further prevent those options from being valid general solutions on the ODE domain. They are preserved as wrong source response objects, not silently repaired or labeled ambiguous. Standard banks avoid these extra-domain wrong functions.
