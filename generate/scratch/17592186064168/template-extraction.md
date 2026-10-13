# Template extraction

## 1. Specific source descriptions

q-2023 asks for the antiderivative of a cube root of x², has five complete scalar math options, and lacks its key, difficulty and worked solution. q-29635 asks for the antiderivative of x^(1/3), has five complete options, and lacks the same attributes. Local MA lesson 308's Markdown and original source layout list these same banks (in another order) and explicitly mark both answer keys missing. No authoritative key is claimed.

q-113674 and q-71096 directly provide exponents 1/4 and 5/2. Their fields are absent, but each has a full formal solution: use n, integral, unsimplified n+1 and division, evaluated new exponent, reduced coefficient, then five distinct derivative-check rows.

q-113680 and q-113695 provide fifth roots of x³ and x². They are labeled hard and fieldless. Their solutions add a first integral-equals-integral row converting the displayed radical to a rational power, before the same three arithmetic stages and five formal derivative stages. Their “Calculate” and “Find” prompts remain separate masks.

q-143041 and q-167564 provide cube/fifth roots of x and a one-choice `blank` for only the term before the supplied +C. Their compact/expanded whitespace prompt layouts remain distinct. Their “Since …” introductory conversion is inline; they do not have the redundant radical-to-power integral row. Their check opening is “Let's check our answer by differentiating:” rather than “Again, let's check by differentiating:”. The complete ordered prose and all row omissions are preserved.

## 2. Shared pattern

On x>0, convert the input radical to x^(p/d) where required, set n=p/d, apply ∫xⁿ dx=x^(n+1)/(n+1)+C, evaluate n+1=(p+d)/d, reduce the coefficient to d/(p+d), and check the result using formal derivative and power-rule steps. Blanks return only the primitive fragment; radios return full options. Unrated assignments and fieldless completions are authored decisions.

## 3. Components and complete choice banks

`source-choice-mapping.json` maps **every one of the 12 source values** to its source/field, exact value, actual parameterized expression/operation and interpretation status. `source-cases.json` covers all eight questions with public `raw:<source_id>` profiles, including unrated/fieldless cases. Profiles are selected as complete banks before any collision check.

For q-2023, n=p/d and m=(p+d)/d:

| Operation | Parameterized complete option | Value at p=2,d=3 |
|---|---|---|
| Lose inner power; multiply rather than divide by new exponent | ((d+1)/d)x^((d+1)/d)+C | 4x^(4/3)/3+C |
| Multiply rather than divide by new exponent | m x^m+C | 5x^(5/3)/3+C |
| Omit division and arbitrary constant | x^m | x^(5/3) |
| Correct power rule | (1/m)x^m+C | 3x^(5/3)/5+C |
| Lose inner power; correctly integrate the resulting unit root | (d/(d+1))x^((d+1)/d)+C | 3x^(4/3)/4+C |

These are defensible actual operations, with inference rather than recovered author-code claims. Every whole bank is checked for equivalent antiderivative families; any collision rejects the entire instance. The absence of C alone never creates an eligible distractor. At the given parameter it is also missing the correct coefficient, so it is mathematically wrong.

For q-29635 the complete captured bank is correct 3x^(4/3)/4+C, 7x^(-7)/6+C, x^(-7)+C, 2x^(4/3)/3+C, x⁶/7+C. The structural parameters b=2d, b+1=2d+1 and coefficient (d−p)/d reproduce all entries, but the apparent integer surrogates do not establish a genuine error process. The original intent remains unresolved. **No arbitrary numerical fit is promoted to learner generation.** Public raw and completed opaque profiles reproduce the entire parameterized structural bank and are always evidence-only/ineligible. The default rational-power radio bank instead uses the following actual operations on n and m:

1. Correct primitive (1/m)x^m+C.
2. Multiply rather than divide: m x^m+C.
3. Omit division: x^m+C.
4. Fail to increment the exponent, retaining the new denominator: (1/m)x^n+C.
5. Differentiate instead of integrate: n x^(n−1)+C.

The two blank source banks contain 3{x}^(4/3)/4 and 5{x}^(6/5)/6. Their coefficient/exponent derive from the same exact rule. No C is inserted into the field's value; +C remains outside the source placeholder.

## 4. Reusable masks, slots and checks

Slots are full radical/power components, exact rational numerator/denominator components, complete primitive expressions, and the formal operator arguments. They are rendered from p,d rather than searching/replacing short text. Prompt and solution masks share the original instructional prose and punctuation. Raw whitespace-expanded q-167564 is reproduced byte-for-byte. The six present source solutions reproduce byte-for-byte; there is no TeX normalization or mathematical repair disguised as fidelity.

Integration stages retain distinct unsimplified nodes: exponent p/d+1 and divisor (p/d+1), evaluated exponent (p+d)/d and divisor ((p+d)/d), then the reduced fraction. Derivative stages retain d/dx(primitive+C), split derivative plus derivative of C, coefficient times d/dx(power)+0, coefficient times new exponent times x^(new exponent−1), and the final original power. Independent QA reads every actual printed stage and introductory n/conversion; it does not merely inspect metadata or selected IDs.

Normal fieldless completions add a primitive-fragment blank with matching placeholder. All normal outputs say “Work on x>0.” and blank outputs explicitly require only the term before +C without an additive constant. Native grading tests canonical and independently unsimplified equivalent power quotients, rejects wrong values and additive shifts. Family equivalence is used for full radio antiderivatives, while fragment equality respects the supplied +C answer form. The two missing source radio keys are inferred by independently differentiating every displayed option, and are counted as completions rather than matched original designations.

The authored moderate/hard numerator catalog permits both proper and improper peers, using 2≤p≤20, p+d≤24, p/d≤5 and gcd(p,d)=1. The observed easy exponent 5/2 establishes improper positive fractions, and the lesson applies the rule to all n≠−1. Moderate retains indices 2–4 (22 distinct reduced exponents); hard retains indices 5–8 (41). These limits keep the successor numerator at most 24 and add no extra solution operation. Samplers are uniform over each unordered finite reduced catalog, not ordered by numerator; explicit calls obey the same bounds. Review variants include both proper and improper root forms, and native grading exhaustively exercises both.

There are no plots. Steps 5 and 7 are satisfied by a plot rating of none; no rendering or asset dependencies are introduced. UUIDs use the actual prompt, solution, complete bank and mathematical task; shuffling cannot alter identity. Equivalent mathematical tasks exclude bank/profile/layout in their fingerprint. The CLI supports all levels and omission-safe raw preview. No EDB transactions, engine edits or registration occurs.
