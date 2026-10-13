# Template and plot extraction

All seven practice questions were read and preserved in source.json. Each complete source is described below; bank-extraction.json maps every exact original option to its field and complete profile, coefficient, power and canonical designation. All 25 option values and 20 distractors must replay exactly. No feedback or invented error interpretations are added.

The generalized family asks for an indefinite integral of c(ax-b)^n or c(b-ax)^n. Let u be the whole linear expression, use dx=du/a with signed a, integrate u^n by the power rule, return to x, then differentiate the result to verify the original integrand. The answer is c/[a(n+1)] times u^(n+1) + C, for real x and arbitrary constant C. All source exponents are positive integers; slope is nonzero. Five math options belong to the selection radio field.

## q-113486: easy

Source db ID 17592186247354. Prompt: $\int 48(3x-2)^{7}\,\text{d}x=$

Parameters: signed slope 3, constant magnitude 2, exponent 7, outer coefficient 48; linear expression `3x-2`. Source bank profile `q-113486` has five options with the same linear base and power 8; exact coefficient patterns and correct designation appear in bank-extraction.json. All original choices are retained in templates.json. The source solution layout and arithmetic are fixed; only the complete base expression changes. The positive-slope easy profile uses positive differential substitution; negative-slope moderate profiles retain the explicit negative differential factor and signed final antiderivative.

## q-113492: moderate

Source db ID 17592186247355. Prompt: $\int 6(5-3x)^{2}\,\text{d}x=$

Parameters: signed slope -3, constant magnitude 5, exponent 2, outer coefficient 6; linear expression `5-3x`. Source bank profile `q-113492` has five options with the same linear base and power 3; exact coefficient patterns and correct designation appear in bank-extraction.json. All original choices are retained in templates.json. The source solution layout and arithmetic are fixed; only the complete base expression changes. The positive-slope easy profile uses positive differential substitution; negative-slope moderate profiles retain the explicit negative differential factor and signed final antiderivative.

## q-113503: moderate

Source db ID 17592186247358. Prompt: $\int 9(3-2x)^{8}\,\text{d}x=$

Parameters: signed slope -2, constant magnitude 3, exponent 8, outer coefficient 9; linear expression `3-2x`. Source bank profile `q-113503` has five options with the same linear base and power 9; exact coefficient patterns and correct designation appear in bank-extraction.json. All original choices are retained in templates.json. The source solution layout and arithmetic are fixed; only the complete base expression changes. The positive-slope easy profile uses positive differential substitution; negative-slope moderate profiles retain the explicit negative differential factor and signed final antiderivative.

## q-113502: moderate

Source db ID 17592186398102. Prompt: $\int 18(2-5x)^{5}\,\text{d}x=$

Parameters: signed slope -5, constant magnitude 2, exponent 5, outer coefficient 18; linear expression `2-5x`. Source bank profile `q-113502` has five options with the same linear base and power 6; exact coefficient patterns and correct designation appear in bank-extraction.json. All original choices are retained in templates.json. The source solution layout and arithmetic are fixed; only the complete base expression changes. The positive-slope easy profile uses positive differential substitution; negative-slope moderate profiles retain the explicit negative differential factor and signed final antiderivative.

## q-72424: moderate

Source db ID 17592186398961. Prompt: $\int 16(7-2x)^{7}\,\text{d}x=$

Parameters: signed slope -2, constant magnitude 7, exponent 7, outer coefficient 16; linear expression `7-2x`. Source bank profile `q-72424` has five options with the same linear base and power 8; exact coefficient patterns and correct designation appear in bank-extraction.json. All original choices are retained in templates.json. The source solution layout and arithmetic are fixed; only the complete base expression changes. The positive-slope easy profile uses positive differential substitution; negative-slope moderate profiles retain the explicit negative differential factor and signed final antiderivative.

## Components and bounded sampling

Fixed: source slope, exponent, outer coefficient, five bank coefficients, correct option, field layout, full solution sequence and prose, differential notation, sign/order of the linear expression. Variable: positive constant magnitude b. Optional components: none. Conditional components: original positive versus negative slope layout; these are selected as whole source profiles, never pooled distractor recipes.

The proposed narrower sampling policy varies b over 1..20; it covers all observed b values 2, 3, 5 and 7. It deliberately does not vary slope, exponent or outside scale, and makes no claim about unobserved signed constants or hard difficulty. Correct and incorrect option derivatives are checked independently; duplicate or ambiguous banks are rejected. Distinctness uses the expanded integrand, independent of seed, identity, bank profile and option order. The bounded universe has 20 easy and 80 moderate integrands. This is a package limit, not a claim that the mathematical topic has a finite number of possible problems.

q-12015 has outside scale 14, base 2x-5 and exponent 6; its correct antiderivative would be (2x-5)^7+C, which appears in the bank. q-12493 has unit outside scale, base x-2 and exponent 10; its correct antiderivative would be (x-2)^11/11+C, which appears in the bank. Both lack correct refs, worked solutions and difficulty. These mathematical observations are recorded evidence only: neither is repaired or used as rated practice.

Stages 5/7: none. There are no plot references; standalone LaTeX is not a plot. No plot generation, asset publication or hash rewriting is needed. templates.json is the reusable Markdown/value template source. Its original full inner expression is replaced atomically everywhere in prompt, each answer and solution; unrelated numbers cannot be substituted. A source replay uses the original b and is byte-identical in prompt, solution and complete bank. review.md places original, replay and changed-constant variants side by side.
