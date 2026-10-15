# Template extraction

## 1. Specific original instances

Every exact original prompt, field, ordered solution and complete choice bank is in `source.json`; `source-cases.json` contains generated local records for all eight originals, not copied Pull evidence.

| Source | Supplied integrand and parameters | Requested object | Ordered operative solution |
|---|---|---|---|
| q-113852 | `2 exp(3x)(exp(3x)+2)^3`; a=2,k=3,b=2 | whole primitive +C | introduce u; compute du; reorder product; substitute u and proportional differential; move scalar outside; integrate u^3; back-substitute |
| q-73670 | `2^z/sqrt(2^z-9)`; base=2,b=9 | whole primitive +C | introduce u; compute du with ln(base); separate reciprocal root and exponential; substitute; power -1/2; divide by 1/2; back-substitute |
| q-49577 | `5 exp(x)sqrt(exp(x)+4)`; a=5,b=4 | whole primitive +C | introduce u; du=exp(x)dx; factor a outside and reorder; substitute sqrt(u); power 1/2; integrate; express u^(3/2) as sqrt(u^3); back-substitute |
| q-73669 | `2^(x+1)sqrt(2^x-5)`; base=2,b=5 | whole primitive +C | introduce u; differential containing ln(base); split shifted exponential; factor base; substitute; power 1/2; divide by 3/2; simplify 2/3; write root cube; back-substitute |
| q-113873 | `(exp(2x)-1)/(exp(2x)-2x)`; k=2,c=1 | whole primitive +C | derivative-proportional numerator observation; introduce u; factor du; rewrite quotient product; substitute reciprocal u and scale; logarithmic primitive; back-substitute absolute logarithm |
| q-31478 | `5^x/(5^x+1)`; base=5,b=1 | whole primitive +C | derivative-proportional observation; introduce u and du; reciprocal product; substitute; factor 1/ln(base); ln(abs(u)); back-substitute abs; remove abs using positive denominator |
| q-31480 | `4^x/(4^x+2)`; base=4,b=2 | whole primitive +C | same stages as q-31478, different observed bank |
| q-113876 | `3^(x+1)/sqrt(3^x+1)`; base=3,b=1 | source has no correct reference | solution absent; authored completion uses shifted-exponential factor and reciprocal-root substitution, ending with `2 base sqrt(U)/ln(base)+C` |

All source fields are radio, key selection, five bare TeX math values, no feedback. There are no plots. The shared sentences, whitespace, nested aligned environments and math-row order remain full parameterized masks in `masks()`. Source text is not used as an answer lookup or a raw question return branch.

## 2. Shared backbone

The inner function U contains an exponential plus a shift, or an exponential minus a linear term. Its derivative is proportional to the remaining numerator factor. Substitute u=U, transport the scalar and differential, apply the existing power or logarithmic rule, then return to the original variable. Each family preserves its source factorization and power-conversion stages. Each question has one concrete solution independent of the selected option.

## 3. Every original bank recipe

Notation: E=exp(kx) for easy; U=E+b. For roots with integer base B, E=B^x (or B^z), L=ln(B); U=E-b for negative-shift roots. For natural roots U=exp(x)+b. For ratios U=B^x+b, J=ln(U). All expressions below have +C. Choices are listed in captured order; starred values are correct. Historical error interpretations of unusual scalar recipes are unresolved rather than invented.

| Source | Complete ordered empirical bank |
|---|---|
| q-113852 | `U^4/4`; `U^3/3`; `a U^4/(4k)`*; `a U^3/(4k)`; `a U^4/k` |
| q-73670 | `sqrt(U)/2`; `2 sqrt(U)`; `2 sqrt(U)/L`*; `sqrt(U)/(2L)`; `2 L sqrt(U)` |
| q-49577 | `(a-2)sqrt(U^5)`; `sqrt(U^3)/a`; `a sqrt(U^3)`; `2a cbrt(U^2)`; `2a sqrt(U^3)/3`* |
| q-73669 | `B sqrt(U)`; `3B sqrt(U^3)/L`; `2B sqrt(U^3)/(3L)`*; `B sqrt(U)/(3L)`; `B sqrt(U^3)/3` |
| q-113873 | with U=exp(kx)-kc*x and J=ln(abs(U)): `kJ/E`; `J/k^2`; `J/(kE)`; `J/E`; `J/k`* |
| q-31478 | `Bx/L`; `J/L`*; `BJ/L`; `1/(EL)`; `J/(BL)` |
| q-31480 | `ln(E)/L`; `1/(EL)`; `J/(BL)`; `J/L`*; `BJ/L` |
| q-113876 | with U=B^x+b: `2B sqrt(U)/L` (inferred correct); `sqrt(U)/(2BL)`; `2sqrt(U)/(BL)`; `sqrt(U)/L`; `B sqrt(U)/(2L)` |

These are whole empirical banks, never pooled choice recipes. They reproduce all 40 original values, including the unusual coefficients and reversed root power. Replays preserve complete mathematical expressions and exact source notation. Independent rendered-math checks verify all five choices, not merely the designated answer. Every pair is tested modulo a constant on the actual domain.

The three underdetermined scalar banks (q-49577, q-73669 and q-113876) remain explicit `observed:<id>` and `completed:<id>` empirical profiles. Ordinary sampling uses a separately labeled complete `method_errors` bank for those families: correct `K sqrt(U^n)`, wrong power `K sqrt(U^(n+2))`, inverted scale `sqrt(U^n)/K`, negative sign `-K sqrt(U^n)`, and retained integrand exponent (`K sqrt(U)` for positive-root integrands, `K/sqrt(U)` for inverse-root integrands). Here n=3 for positive roots and n=1 for inverse roots, with K from the actual substitution. It adds no learner-facing feedback or extra solution stages. Original banks and genuinely changed-parameter variants remain served through the normal generator API; they are not evidence-only raw copies.

## 4. Reusable slots, bounds and calculations

| Family | Explicit bounds | Fixed mathematical roles |
|---|---|---|
| easy integer power | a,k in 2..6; b in 1..8; reject a=k or 3a=4k | cubic power, one positive-slope exponential, direct proportional differential a/k, quartic primitive; reject complete-bank collisions |
| inverse root | B in 2..7, b in 1..9 | reciprocal square root; variable z; negative shift; domain B^z>b |
| natural positive root | a in 3..7,b in 1..8 | exp(x), positive square root, positive shift; K=2a/3 |
| shifted-base positive root | B in 2..7,b in 1..9 | exponent x+1, one square root, negative shift; K=2B/(3ln B), domain B^x>b |
| derivative ratio | k in 2..7,c in 1..6 | numerator exp(kx)-c, denominator exp(kx)-kc*x, derivative scale 1/k; denominator nonzero on each solution interval |
| positive base ratios | B in 2..7,b in 1..9 | exponential numerator and positive shifted denominator; logarithmic primitive /ln B; retain each full first-distractor profile |
| shifted-base inverse root completion | B in 3..7,b in 1..8 | numerator B^(x+1), positive shifted reciprocal root; K=2B/ln B; B=2 excluded because the empirical bank would contain two equivalent wrong values |

These conservative bounds include all anchors and meaningful variation in every declared slot. The fixed cubic/root powers preserve the observed workload and operative power conversion; base, shift, numerator scale and derivative proportionality vary without introducing a different method. The multiplier c in the derivative ratio is an explicitly authored generalization of the existing numerator constant and denominator linear coefficient; it preserves the same factorization `U'=k(E-c)` and four integration rows. No new term or operator is added.

The generator computes every display scale from a single parameter tuple. Scalar simplification is used only where the source expresses a simplified coefficient. Transport is simultaneous, longest-token-first, so a new base or shift cannot be rematched as an old source value. No special literal-original answer branch exists.

Batch selection uses a finite catalog keyed by the actual normalized displayed integrand, integration variable, and whole-indefinite-primitive-modulo-constant target. Exponential powers are expanded canonically and rational algebra is normalized without forcing root branches. Original bank profiles and formatting aliases never add capacity. The hard base-ratio pair contributes54 semantic slots, with both original profiles retained as alternatives inside each slot. The easy pool remains152 after exact integrand normalization: equal a/k ratios with different k values have different exponential arguments and are different integrands. Batches select semantic slots without replacement, then select an eligible original/default bank alternative. Requests above capacity fail before returning any output. Both public seed and batch count contracts reject non-built-in-integer values, including booleans.

Domains: roots with negative shifts require U>0; positive shifts are positive for all real input. Absolute logarithms are evaluated on connected intervals with U nonzero, allowing both signs without replacing a branch restriction. Antiderivatives differing only by an additive constant are equivalent; no constant-only offset appears as an incorrect choice.
