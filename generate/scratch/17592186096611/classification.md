# Classification

Capture: math, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The raw wrapper is preserved in `source.json`.

Nine practice questions, nine distinct prompt/solution/field families, six complete radio banks, three blank banks. Two practice questions are unrated and have no correct designation or worked solution. Those are included with explicitly authored supported level assignments. There are no practice hard questions. Canonical e-3625 is context, not a tenth practice case.

| Level | Template | Source | Field | Plot |
|---|---|---|---|---|
| easy, authored assignment | direct_quadratic | q-11728 | radio, five whole equations | none |
| easy | difference | q-167636 | blank, derivative RHS | none |
| easy | slope_quad | q-140431 | radio, five exact scalars | none |
| easy | slope_polyfirst | q-140432 | radio, five exact scalars | none |
| easy | slope_zero | q-17247 | radio, five exact scalars | none |
| easy | slope_seventh | q-304035 | blank, scalar, two captured bank values | none |
| moderate, authored assignment | direct_extended | q-11730 | radio, five whole equations | none |
| moderate | branch | q-167694 | blank, derivative RHS | none |
| moderate | slope_extended | q-17255 | radio, five exact scalars | none |
| hard, authored missing level | two_powers | canonical e-3625 anchor | blank, derivative RHS | none |

Lesson order was obtained from `:activity/first-step` 17592186097413 and successive `:step/next` refs, not collection order: introduction → constant-plus-exponential KP96610 → this polynomial KP96611 → other-base tutorial → other-base KP96612 → rule justifications. Prerequisite topic edges and the local MA lesson 1114 both list tangent slopes (332), natural logarithm (818), and exponential graphs (1530). Following topics include exponential chain rule (1007) and logarithmic derivatives (1116); these are excluded here. The preceding sibling handles constants without polynomials; the following sibling owns bases other than e. Our hard questions remain termwise differentiation of constant multiples of e^x and two polynomial powers.

Observed difficulty labels are not an increasing-degree ladder: q-304035 explicitly labels differentiating a seventh power at -1 easy. Its odd exponent and familiar input preserve easy arithmetic. The authored hard claim is **two nonconstant powers with exponents at least two**, both requiring coefficient multiplication and exponent reduction, anchored to the canonical `4e^x+3x^4-x^2`; it does not rely merely on making a single degree bigger. All hard instances have the same two-power workload; no hidden progression, tangent-equation solving, composition, or general products occur.

q-167636 and q-167694 depend on preceding definitions absent from the practice prompt. Their observed profile retains the prompt and source prose. Normal output explicitly supplies the functions. q-167636 contains a malformed distributed derivative row; it is repaired and reported independently from exact fidelity. q-304035's extra blank-bank derivative expression is not a valid slope fragment and is retained only in observed replay. q-17255's scalar distractor intentions are uncertain, so they are not used as the default bank.

No source question contains plots or graphical assets. Steps 5/7 therefore require no renderer.
