# Classification — Cartesian FTLI

Immutable capture: database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Twelve practice questions: six easy, six moderate, no hard. Every question has one radio field with five delimiter-free mathematical choices. No source references an image or plot; rating none. Steps 5 and 7 require no renderer.

| Level | Template/source profile | Potential and Cartesian form | Arithmetic stages after endpoint substitution |
|---|---|---|---|
| easy | q-39749 | x²y; y=cos(x)+x³−2 | product substitution; final factorization |
| easy | q-104617 | sin(x)+cos(y); y=2x, x interval | trig substitution; trig values; collection |
| easy | q-104625 | eˣ sin(πy/2); y=x³+1 | product substitution; familiar-angle values; collection |
| easy | q-104626 | (x³+y³)/3; y=2x² | cube substitution; sum evaluation; fraction evaluation; collection |
| easy | q-124027 | xeʸ⁺¹; y=eˣ+1 | product substitution; collection |
| easy | q-124028 | yx³; y=ln(x) | product substitution; power evaluation; collection |
| moderate | q-123879 | y²−x²; y²=4x | square substitution; square evaluation; collection |
| moderate | q-124029 | x sin(y); y²=x | product substitution; trig values; collection |
| moderate | q-124030 | x²+eˣʸ; x/2=√y | substitution; square/product evaluation; collection |
| moderate | q-124032 | eʸ sin(x); y=2x, y interval | product substitution; trig values; collection |
| moderate | q-124034 | cos(x) cos(y); 2x=πy³ | trig substitution; trig values; collection |
| moderate | q-124035 | y²−x; x=cos(y) | substitution; sign collection; collection |

Distinct templates are retained because potentials, independent-coordinate conventions, omitted endpoint prose, and arithmetic row sequences differ. Each has its own complete source bank. Changed numbers or coefficient scales are variants of these templates, not new recovered skills.

Canonical e-9502 supplies f=xeʸ, curve x+2y=3, x from −1 to 1. Lesson traversal follows first-step 17592186134760 → 17592186134860 (concrete Cartesian example) → 17592186134824 (parametric supplied-potential sibling) → 17592186134850 (this KP) → 17592186134825 (potential-not-given sibling) → 17592186134861 (proof). Collection order was not used. Prerequisites concern Cartesian curves expressed as functions of x or y. The neighboring missing-potential KP is expressly outside this implementation.

## Source anomaly

q-39749 correctly displays r(0)=(0,−1), but the final block changes it to f(0,0) and 0²·0. Its answer is unaffected because x²=0. Raw source is preserved in source.json. The replay corrects these two slots to f(0,−1) and 0²·(−1), retaining the original two arithmetic rows. Report raw and repaired solution fidelity separately: 11/12 raw, 12/12 repaired.

## Authored scope

Default easy is a direct Cartesian quadratic with supplied cubic-sum potential; default moderate is a principal-root inverse curve with supplied square-plus-exponential potential. These are grounded in q-104626 and q-124030 respectively, retaining modest integer arithmetic and perfect-square input endpoints.

Hard is authored, not an observed difficulty label. It combines canonical e-9502's line solved for the dependent coordinate with two supplied terms kx²y+ℓxeʸ, both contributing nonzero values at both endpoints. It uses the same parameterize → endpoints → supplied-potential difference method, eight displayed multiplications across two endpoints and familiar integer exponents, bounded by 4. It adds no potential reconstruction, line-integral integration, new branches or arbitrary symbolic algebra. Parameters vary this fixed workload; no progression exists within any level.

The hard two-term evaluation is also supported by supplied-potential sibling e-8759, which evaluates two mixed contributions at endpoints. This design retains two-variable Cartesian curves. Easy dependent endpoints are bounded by absolute value 8, the largest cubic input in q-104626, to preserve comparable arithmetic.
