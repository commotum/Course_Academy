# Template and bank extraction

`source.json` retains every prompt, ordered worked solution and complete original bank. `reference/validation/source-bank-fidelity.json` maps every original answer UUID and exact value to a parameterized recipe index, checks every complete bank, and preserves correct designations independently of choice order. Recipes below are in the order returned by `model`, not source UUID order. There is one observed expression-pattern bank per template; no profiles are pooled or partially selected. Unclear distractor mechanisms remain labeled expression patterns. The formulas generalize complete source values and do not claim to identify a particular misconception.

The fixed backbone is one three-coordinate surface, a nonnegative rectangular parameter domain, one five-option radio field, and the missing scalar integrand ‖r_u × r_v‖. The supplied and requested roles remain fixed. Domain bounds are retained because the sign branch matters; no integration or extra response stage is introduced. Coefficients alter derivative and cofactor arithmetic, not merely overall scale, seed, identity or choice order. Additive translations and reordering are deliberately not sampling slots. The prompt's domain, its prose copy, tangent vectors, determinant/minors, cross product, norm arithmetic, bank and final integral share one instance.

## Moderate q-109941

Observed: r=(u²,u−v²,v²), 0≤u,v≤2, answer 2v√(1+8u²). Slot: first coordinate becomes a u², integer a∈{1,…,5}; observed a=1. The derivative stages and nonnegative-v branch remain unchanged. Bank: [2v√(1+8a²u²), u√(1+4a²v), √(v²−a²u²), √(a²u²+v²), v²√(1+4a²u²)]. The third is an invalid real-valued integrand on part of D and is an intentionally wrong candidate. Its interpretation is unresolved; the whole observed expression is preserved at a=1.

## Moderate q-109943

Observed: r=(u+v,3−v,1+4u+5v), 0≤u≤1,0≤v≤2. Tangents (1,0,4),(1,−1,5), cross (4,−1,−1), norm √18=3√2. Slots replace 4,5 by a,b. Integers 2≤a≤8 and a+1≤b≤a+3 preserve positive unequal coefficients and the same constant-vector workload. Exclude (2,3), where a source-pattern distractor collides with the correct answer. Bank: [√(a+b+1), √(b−a+2), u√(v²+1), 2√(u+v), √(a²+(a−b)²+1)]. The first two are conservative affine expression patterns inferred from a single source, not established error diagnoses. Other patterns retain their observed values and variable roles. Distinct surfaces with the same resulting integrand are deduplicated as one assessed task.

## Hard q-105613

Observed: r=(2u sin v,3u cos v,u), 0≤u≤1,0≤v≤π. Slot a∈{2,…,5}, b=a+1, r=(a u sin v,b u cos v,u). Bank: [u√((b²−a²)sin²v+a²(1+b²)), √(u²+a²b²), ab√(u²sin²v+u²+1), ab√(u²+1), √(b u²cos²v+a²u²+a²b²)]. The last pattern's b coefficient reproduces source 3; its error mechanism is unresolved. Correct answer follows from cross=(b u sin v,a u cos v,−ab u), trig identity, factoring u² and nonnegative u.

## Hard q-109948

Observed: r=(u,e^u sin v,e^u cos v), 0≤u≤4,0≤v≤π. Slot first coordinate a u, a∈{1,…,5}; observed a=1. Bank: [e^u√(u+a²), e^(2u)√(cos v+sin v), e^u√(e^(2u)+a²), e^u cos v sin v, √(e^u cos v sin v)]. The last three wrong patterns not involving a remain unchanged; the first's constant follows the axial derivative square. Correct cross=(−e^(2u),a e^u sin v,a e^u cos v). Square, collect trig terms, factor e^(2u), use e^u>0.

## Hard q-110019

Observed: r=(u²,2u sin v,u cos v), conflicting source u bounds documented in classification. Use 0≤u≤1,0≤v≤π consistently. Slot sine-coordinate coefficient a∈{2,…,5}; observed a=2. Bank: [u√(u²+cos²v), √(1+a u²), a u√(1+u²cos²v), cos v√(1+u²), u√(a²+4u²+4(a²−1)u²cos²v)]. The source √(1+2u²) is retained as the a-coefficient expression pattern. Cross=(−a u,2u²sin v,2a u²cos v). Correct norm uses trig identity and nonnegative u.

## Hard q-109947

Observed: r=(u+v,3u²,u−v), 0≤u,v≤1. Slot quadratic coefficient a∈{3,…,7}, observed 3. Bank: [√(u²+4), 2u√(a²u²+1), 2√(u²+1), 2√(2a²u²+1), u√(u²+4)]. Fixed 4 is an opaque source constant. Cross=(−2a u,2,−2a u); collect squares and extract factor 4.

## Hard q-109951

Observed: r=(u²,v²,uv), 0≤u≤2,0≤v≤4. Slot first coefficient a∈{1,…,5}, observed 1. Bank: [√(u²+v²), 2√(a²u⁴+v⁴+4a²u²v²), 2u²v, u√(u²+1), 2u√(v²+uv)]. Wrong patterns retain their full original expressions because their mechanism is unresolved. Cross=(−2v²,−2a u²,4a uv); sum squares and extract 4.

## Fidelity and limits

Every observed coefficient is replayable. The complete original banks, including correct selections, must match algebraically before any new question is eligible. Solutions retain the source prose and operative partial-derivative, determinant/cofactor, norm and integral stages. Captured Unicode and nested `aligned` determinant tables are rendered as canonical TeX and `vmatrix`; redundant factorization equalities are consolidated, recorded separately from mathematical fidelity. Every printed scalar equality and cofactor is independently read back and checked. Only declared integer domains are certified, and every member is tested. Conservative distractor generalizations beyond source coefficients are explicit; invalid or colliding full banks are excluded, never reduced to a subset. Mathematical task identity depends on the squared integrand, domain and template, with an additional cross-template integrand check at publication. Seed/order and bank variations do not create extra tasks.
