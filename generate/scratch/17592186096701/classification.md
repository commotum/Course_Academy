# Classification

Read-only database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Raw wrapper is `source.json`; fourteen practice questions: seven easy, seven moderate, no hard or unrated sources. Every question has one owned field and a correct designation. Ten radios have five math choices; four blanks have one math fragment.

| Level | Prompt/solution/field family | Sources | Plots |
|---|---|---|---|
| easy | known unit a, unknown b, radio; OA then AC | q-19338, q-120244, q-70140, q-70141, q-70149 | heavy |
| easy | known unit a, unknown b, blank; OA then AC | q-321299 | heavy |
| easy | known unit b, unknown a, radio; OB then BC | q-70187 | heavy |
| moderate | known multiple b, unknown a, radio; introduce P then OP/PC | q-20435, q-120245, q-120250 | heavy |
| moderate | known multiple b, unknown a, blank; introduce P then OP/PC | q-275120, q-327049 | heavy |
| moderate | known unit a, unknown b, blank; OA then AC, oblique grid | q-327046 | heavy |
| moderate | known multiple b, unknown a, radio; OB/BC without P introduction | q-77230 | heavy |
| hard | authored fractional known b, unknown a, radio or blank; OP/PC plus exact fractional construction | no observed sources | heavy |

These are seven observed Markdown/value/field combinations within two shared scalar-finding recipes. Their ten radio banks remain ten explicit profiles; each blank has its own exact-answer profile. Per-source masks also preserve punctuation and the omitted P introduction in q-77230. The API `template` identifies the mathematical recipe (`known_unit`, `known_multiple`, `fractional_known`); source `profile` and `field_type` resolve the finer observed layouts.

## Curriculum scope

Following `activity/first-step` and `step/next`, the captured lesson order is Introduction → Writing a Position Vector Using Known Vectors → **this KP** → Vectors in Opposite Directions → Finding a Scalar Factor When Direction Reverses → Finding Two Scalar Factors in a Linear Combination → Expressing a Vector That Satisfies a Ratio in Terms of Known Vectors. Pull order is not used. Prerequisites are Problem Solving Using Vector Diagrams and Linear Combinations of Vectors and Their Properties.

Both coefficients stay positive. An oblique vector may point left/down, but its translated copy never reverses. We assess only one scalar; no two-unknown system, line equation, point-dividing ratio, or negative coefficient extension.

Normal easy peers construct a unit known component and compare a horizontal/vertical remaining displacement, with denominators ≤3. Normal moderate peers construct 2–4 times an oblique known vector before comparing the remaining displacement; the original moderate unit-coefficient source remains an observed exception. Hard is an authored missing-level design: positive known coefficient with denominator 2 or 3, oblique b with both coordinates nonzero and two genuinely fractional endpoint coordinates, then a remaining horizontal ratio with denominator 3 or 4. Exact diagram coordinates support these fractional readings. Its fixed solution prints the endpoint, subtraction, division, path sum, and coefficient matching. These extra demands are enforced on explicit inputs as well as sampling.

All fourteen banks preserve exact original strings. Raw-byte inspection confirms the four fraction option strings contain one backslash each; tool JSON serialization had initially made them appear doubled. There are zero source mathematical or presentation repairs and no exclusions.

The inspected canonical diagram has $c=\lambda a+2b$ and concludes $\lambda=2$; its oblique known b supports positive translated-component construction. The immediately following sibling's inspected diagram requires reversed path directions. Neither its negative coefficient nor its two-scalar sibling is borrowed for hard.
