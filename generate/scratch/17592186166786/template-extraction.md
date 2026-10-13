# Template extraction

Every source is assigned to exactly one profile, with no pooled or mixed banks. source.json retains all original prompts, values, UUIDs and field layouts. Neither practice source supplies a solution, feedback or correct designation. Derivation supplies the keys and the fixed authored step sequence. Distractor expressions are observable; author mistake intentions remain unresolved.

## q-95537, profile q-95537

The source has positive integer 2 inside cosh(2*x²), an outer x factor, variable x real, an indefinite integral and five antiderivatives ending in + C. Choices are positive/negative rational coefficients times sinh of x², 2*x² or 4*x². It uses one selection radio field. The original prompt contains the malformed LaTeX control word `\intx`; generated prompts use `\int x`. The full value bank replays exactly at a=2.

Shared pattern: integrate x*cosh(a*x²) using u=a*x², preserving the missing differential scale. Fixed components: instruction Calculate, variable x, x² inner power, cosh operator, outer x, indefinite dx, five radio answers and + C. Variable components: positive integer a, exact factor 1/(2a), and corresponding inner arguments. There are no optional components. Proposed sampling a=2..12 retains observed a=2. a=1 is excluded because two choices become equivalent. Wider, signed or fractional coefficients are not claimed.

| Source option and exact value (a=2) | Complete recipe | Correct |
|---|---|---|
| 1: (1/2)sinh(x²)+C | (1/2)sinh(x²)+C | no |
| 2: (1/4)sinh(2*x²)+C | (1/(2a))sinh(a*x²)+C | yes, derived |
| 3: -(1/4)sinh(2*x²)+C | -(1/(2a))sinh(a*x²)+C | no |
| 4: -(1/2)sinh(x²)+C | -(1/2)sinh(x²)+C | no |
| 5: (1/2)sinh(4*x²)+C | (1/2)sinh(2a*x²)+C | no |

Each recipe reproduces the entire observed option at a=2. Scaling a in options 2, 3 and 5 is an explicit observed-shape extension from one source, not evidence of the author's intended mistake. The authored solution differentiates u=a*x², isolates x dx, substitutes, integrates cosh u to sinh u, and substitutes back. Domain is all real x. Distinctness compares the integrand coefficient a, not seed, choice order or bank.

## q-95543, profile q-95543

The source has lower bound 1, upper bound e, outer 1/x, reciprocal hyperbolic square sech²(ln x), and one selection radio field. All five options are ratios of polynomials in positive exponential e with exact integer coefficients. The source spells sech as plain letters; generated prompts use operatorname{sech}. At b=1 all five original mathematical values replay exactly, preserving their stored notation.

Shared pattern: integrate sech²(ln x)/x over [1,e^b], using u=ln x and evaluating tanh(b). Fixed components: lower bound 1, outer 1/x, sech², ln x, five choices and real x>0. Variable components: positive integer b, upper bound e^b, transformed upper bound b, E=e^b, and exact answer (E²-1)/(E²+1). Proposed b=1..10 retains b=1 and bounds expression complexity. No extra templates, negative bounds or zero-width intervals are supported.

| Source option and exact value (b=1, E=e) | Complete recipe | Correct |
|---|---|---|
| 1: (1-2e)/(e²+1) | (1-2E)/(E²+1) | no |
| 2: (e-1)/(2e+1) | (E-1)/(2E+1) | no |
| 3: (e+1)/(e-1) | (E+1)/(E-1) | no |
| 4: (e²-1)/(e²+1) | (E²-1)/(E²+1) | yes, derived |
| 5: (e²+1)/(e²-1) | (E²+1)/(E²-1) | no |

Each recipe reproduces the complete observed value at b=1; there are no unmapped choices. E substitution in all five is an explicit observed-shape extension; mistake interpretations are unresolved. The fixed authored solution differentiates u=ln x, transforms both bounds, integrates sech² u to tanh u, evaluates the bounds and rewrites tanh b in exponentials. E>1 ensures all choice denominators are nonzero. Distinctness compares the definite integration interval: equal integrands with different upper bounds are different tasks. Seed and identity alone never count.

Both observed banks are exhaustively replayed, including exact original strings, cardinality, field key, field type and independently derived correct designation. Original keys and solutions cannot be compared because they are absent. Fidelity is reported separately from mathematics and native grading in source-replay.json and validation.json.
