# Classification at captured basis 1356

Database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is a byte-for-byte copy of the capture wrapper, not a replacement of its colon-key record. Eight practice records: **three easy, three moderate, two unrated**. All require solving the zero component dot product of two printed 2D/3D vectors. No plots, references or image choices occur; plot rating **none** for every template.

| Original level | Source | Template | Field | Bank profile | Structure |
|---|---|---|---|---|---|
| easy | q-1348 | linear2 | radio, 5 math scalars | observed_q1348 | 2D linear, one unknown component |
| easy | q-317932 | linear3 | blank, field-1 | none | 3D linear, collect two unknown terms |
| easy | q-317945 | square2_blank | blank, field-1 | none | 2D squared component, positive integer root |
| moderate | q-101417 | square2_scaled | radio, 5 math scalars | observed_q101417 | 2D, constant product plus scaled square, negative root |
| moderate | q-19023 | square3_collect | radio, 5 math scalars | observed_q19023 | 3D, collect two squared products, negative irrational root |
| moderate | q-77152 | square3_shared | radio, 5 math scalars | observed_q77152 | 3D, two constant products, negative integer root |
| unrated | q-19021 | square2_shared | radio, 5 math scalars | observed_q19021 | 2D shared unknown, positive root |
| unrated | q-19022 | repeated3 | radio, 5 math scalars | observed_q19022 | 3D repeated quadratic root |

The six radio banks remain separate complete profiles. Their scalar wrong answers underdetermine authoring intent; preservation is numerical evidence, not recovered misconception algorithms. Authored complete operation banks are the normal output. Two blank layouts retain a single exact unknown fragment and their original placeholder.

Unrated questions have no captured correct reference or worked solution. Owning authoritative MA lesson `/home/jake/Developer/MA/DATA/Lessons/177/Source/177.json` and `177.md` confirm both five-choice widgets and prompts, without a revealed answer or solution. They are neither excluded nor counted as matched original designations. Their inferred answers are independently verified: q-19021 has roots ±2 and x>0 selects 2; q-19022 has dot product `(x-3)^2`, with the sole distinct real root 3. The supplied solutions and moderate labels are authored repairs, clearly recorded in source cases. The repeated-root family is explicit-only in moderate; it does not expand default quadratic sampling into general factoring.

## Curriculum and missing hard scope

The owning topic is **Calculating the Dot Product Using Components** (MA177). Traverse the captured activity from `activity/first-step` through `step/next`: introduction, component dot-product KP59730, perpendicular-unknown KP59731, then intuition. Collection order is not used. Introduction teaches summing corresponding products, including signed components in 2D/3D; the canonical unknown example sets a 3D dot product to zero and solves its linear equation. KP key prerequisites include **Solving Equations Using the Square Root Method** and **Calculating the Dot Product Using Angle and Magnitude**. The sibling assesses computation only; the unknown KP additionally solves the resulting equation. Later angle-between-vectors and plane topics do not define this generator's scope.

No observed hard questions exist. Two explicitly authored hard layouts (radio and blank) retain q-19023's exact same three-product, collect-square, zero, transpose, divide, ±square-root and sign-selection method. Nonunit signed coefficients in all three products, a nonunit collected square coefficient, and a small reduced rational nonsquare radicand increase arithmetic workload. Bounds: absolute component coefficients 2..12; absolute collected coefficient 2..6; reduced radicand numerator 2..30, denominator 2..6; positive radicand, exactly one sign-selected root. No other vector geometry, projection, generic quadratic branch, polynomial degree, or new solution method is introduced. This is a curriculum-grounded design claim, not an observed MA label.

Easy uses absolute coefficients ≤8, linear roots with denominator ≤8 and magnitude ≤40, or familiar integer square roots ≤8. Moderate uses absolute coefficients ≤9 and positive integer radicands ≤64, allowing exact irrational roots already observed. These guards apply to explicit inputs as well as random sampling; source evidence profiles preserve original parameters without relabeling them. Families within a level are alternative workloads, not a progression. Meaningful task identity tracks the printed ordered coordinate products and sign constraint, excluding bank/profile, field layout and variable-letter aliases.
