# Source classification

Immutable source: math basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. The source wrapper is retained byte-for-byte in source.json. Eleven practice questions: nine easy, two unrated, zero observed moderate/hard. Every question has one radio field keyed `selection`, five complete choices, and one vector of the general solution among the options. No blank or select fields occur.

Eight observed Markdown/value families and eleven complete source bank profiles. Numerical coefficient changes in the two-addition subscript family (three profiles) and dependent rank-one family (two profiles) are counted as variants, not new templates. The two unrated families have source prompt/choice layouts but no captured solution; their generated solution is explicitly authored. The `latter` wording, omitted free-variable row in q32517, and differing operation sequences remain distinct layouts.

| Source | Family | Difficulty | System | Fields/bank | Plots |
|---|---|---|---|---|---|
| q-32234 | unrated_constant_x | unrated → authored easy | 2×3; rank 2 | 1 radio / 5 choices | none |
| q-42040 | unrated_sign_coupled | unrated → authored easy | 2×3; rank 2 | 1 radio / 5 choices | none |
| q-131715 | two_additions_subscript | easy | 2×3; rank 2 | 1 radio / 5 choices | none |
| q-131717 | two_additions_subscript | easy | 2×3; rank 2 | 1 radio / 5 choices | none |
| q-32244 | rank_one_three_operations | easy | 3×2; rank 1 | 1 radio / 5 choices | none |
| q-32517 | scale_then_eliminate_constant_pivot | easy | 2×3; rank 2 | 1 radio / 5 choices | none |
| q-42041 | scale_then_eliminate_full_vector | easy | 2×3; rank 2 | 1 radio / 5 choices | none |
| q-131712 | rank_one_three_operations | easy | 3×2; rank 1 | 1 radio / 5 choices | none |
| q-32247 | two_additions_subscript | easy | 2×3; rank 2 | 1 radio / 5 choices | none |
| q-42019 | one_addition_constant_pivot | easy | 2×3; rank 2 | 1 radio / 5 choices | none |
| q-32220 | one_addition_latter_prose | easy | 2×3; rank 2 | 1 radio / 5 choices | none |

The three canonical SVG assets were decoded on a white background and inspected in source-asset-0.png through source-asset-2.png. They display a linear system, an augmented matrix with the separator before the final column, and the final system. These are mathematical formatting, not graphs. Practice questions use LaTeX only. Plot rating is none for every observed and authored family.

The prerequisite is Reduced Row Echelon Form (topic 1049). The canonical example has a 2-equation, 3-variable rank-two system, pivots x and z, and free variable y. Lesson ordering follows activity/first-step and step/next in ordered-lesson-route.json: introduction and this solving KP precede the separate consistency/classification/constant-parameter content. Sibling KPs are Determining the Value of a Constant for Which a Given Linear System Is Consistent or Inconsistent and Classifying a System as Consistent Dependent, Consistent Independent, or Inconsistent. Generated systems are always consistent with exactly one free variable; no parameter-consistency or classification response is added.

Normal authored easy peers use two nonzero row additions on a 2-equation / 3-variable rank-two system. Moderate is an authored extension: 3 equations / 3 variables / rank two, one free variable, exactly six operations including normalization and elimination of a dependent row. Hard is an authored extension: 3 equations / 4 variables / rank three, one free variable, exactly nine normalization/elimination operations. The NxM lesson introduction explicitly extends the same method to any number of equations and variables; RREF prerequisites supply these operations. These are bounded same-method workload definitions, not claims about unobserved MA difficulty labels. Every instance in a level has the same operation count; there is no staged progression within a level.

Source-format repairs: unclosed source literal system braces are escaped into a visible brace glyph; unrated inline semicolon systems receive aligned display formatting. q32234 and q42040 original widgets confirm all five choices and radio layout but supply no correct designation or worked solution. Independent row reduction yields [6,13−2z,z] and [−2−3z,2+3z,z], respectively. These two designations are inferred, never counted as source designation matches. There are no unresolved mathematical findings.
