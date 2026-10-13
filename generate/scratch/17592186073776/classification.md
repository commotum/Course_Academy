# Classification

Captured provenance: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the unmodified wrapper from `generate/runs/current/sources/17592186073776.json`. The topic is Systems of Equations With No Solutions and Infinitely Many Solutions (493). The local authoritative snapshot `/home/jake/Developer/MA/DATA/Lessons/493/Source/493.json` confirms all three widgets are select lists with three textual counts, with no worked solution or correct designation captured.

| Captured difficulty | Template | Questions | Fields | Complete banks | Plots |
|---|---|---|---|---|---|
| absent / unrated | standard | q-211984, q-237046 | one `:answer-field.type/select`, key `field-1` | same three values; two raw formatting profiles | none |
| absent / unrated | zero_rhs | q-237043 | same select field | same three values; separate source-order profile | none |

There are **2 observed Markdown/value templates**, **1 mathematical/textual complete bank**, and **3 explicit raw replay profiles** retaining per-question spelling/order and omissions. Their answer type is `:answer.type/text`. The bank is {no solutions, infinitely many solutions, a single solution}; it exhausts the possible numbers for two real linear equations. These categorical alternatives are actual response concepts, rather than numerical distractors calculated by perturbing a correct count. No additional count is invented.

All three records lack `:question/difficulty`, `:question/worked-solution`, and `:answer-field/correct`. Raw public replay omits all three rather than emitting null. Normal records supply independently inferred keys, authored worked solutions, and authored difficulty labels. A missing original key has **zero matched-designation denominator**, not three matched correct keys.

The captures use an unmatched literal `{` inside math, inherited from the MA system notation conversion. Exact public raw replay remains explicitly evidence-only and ineligible for learning; normal output escapes it as `\{` to display the opening system brace. The original MA widget has no answer-field ambiguity or duplicate fields. There are no discovered source mathematical errors.

## Curriculum-supported authored levels

The lesson route was read in linked order: `activity/first-step` 17592186074706, then `step/next` through 74707 (infinite elimination tutorial), 74708 (own canonical no-solution example), 74709 (three line cases), 74710 (sibling intersection-count example), 74711–74713 (general solutions, outside this KP's requested response). The first introduction says to solve using substitution/elimination and interpret the result. Prerequisites are Linear Equations With Infinitely Many Solutions (1414) and Elimination: One Transformation (4026). No larger systems or unknown coefficients are required.

- **Easy, authored:** standard two-variable equations with equal/opposite x coefficients; a signed unit multiplier directly cancels x. Coefficients have absolute value at most 5 and constants at most 12. No normalization of the displayed equations is needed. All three response branches occur as equal-level variations.
- **Moderate, authored:** the standard form of q-211984/q-237046, requiring one row multiplier of absolute value 2–4. Coefficients are at most 10; constants at most 30. Their source parameters satisfy this design. Each problem performs one integer row transformation and interprets the resulting identity/contradiction/single solution.
- **Hard, authored:** the y-first, zero-RHS form observed in q-237043, requiring moving the constant in *both* equations before the same one-row elimination. The first y coefficient is ±1, second y coefficient has absolute value 2–4, x coefficients are at most 12, and constants are nonzero with absolute value at most 30. The elimination multiplier is again an integer of absolute value 2–4. Signed coefficients, changed constants and all outcomes vary at fixed demand.

These are supported design assignments, **not recovered difficulty labels**. Each level fixes its information form and transformation workload; variants do not form a progression within a level. A unique solution needs the elementary back-substitution already supported by the one-transformation prerequisite. The generator does not ask for a general solution, graph intersections, slope analysis, rank terminology, three variables, nonlinear equations, or a parameter-solving task. SymPy rank is used only for independent author QA, never as learner prose.

The canonical context graph was inspected at full available resolution: two distinct descending parallel lines, labeled 4x+2y=4 (blue) and 2x+y=4 (red), confirming its no-solution conclusion. It is not an assessed practice image. No parameter-dependent graph is needed or reused in output; plot steps 5/7 are classified none.
