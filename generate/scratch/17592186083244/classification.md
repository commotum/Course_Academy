# Classification — KP 17592186083244

Database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Frozen wrappers are the sole source of observed enums. Six practice questions have seven fields and 23 answer values. Outer generator `knowledge_point` uses plain keys; captured inner enums become ident strings, and correct answer entities become owned lookup references.

| Observed difficulty | Questions | Field/layout | Mathematical templates | Plot rating |
|---|---:|---|---|---|
| moderate | 2 | radio whole line (5 options), blank RHS of `y=` | cubic/quadratic point-slope line; cubic/quadratic slope-intercept line | none |
| hard | 3 | radio coordinate pair (5 options) ×2; two coordinate blanks | exponential-product y-intercept; trigonometric-sum x-intercept; logarithmic-product y-intercept | none |
| absent | 1 | radio whole line (5 options), missing correct ref | quadratic/fifth-power tangent line | none |
| easy | 0 | authored radio whole line (5 options) | canonical-grounded linear/cubic tangent line | none |

Difficulty values are checked as well as key presence: exactly two `:question.difficulty/moderate`, three `:question.difficulty/hard`, and one absent. The unrated question does not acquire a captured difficulty in raw replay. Its normal moderate assignment is authored.

The canonical e-597 uses x=2t+3, y=t³−4t, t=−1: one constant coordinate derivative and one polynomial derivative, then derivative ratio and point-slope form. It anchors the missing easy level. The observed moderate problems differentiate both coordinates, while the hard problems compute a tangent then substitute the requested axis value. Source e-597's supplemental plot is not an assessment input; none of the six practice prompts, answer banks or solutions has an image reference.

The actual linked lesson route in lesson-route.json is Introduction → this KP → Horizontal or Vertical Tangents tutorial → Determining Points Where Tangent Is Horizontal/Vertical → Computing Normal Line → Determining Points Where Normal Is Horizontal/Vertical. The prerequisite KPs are Differentiating Parametric Curves and Calculating Equation of Tangent Line Using Differentiation. This generator does not search for horizontal/vertical parameter values or calculate normal lines. All supported tangent inputs have finite nonzero slopes.

Observed banks are kept intact as six public observed profiles, including both blank layouts. Three radio banks contain opaque historical distractors. Their explicit component generalizations are evidence only and not claimed as recovered mistake algorithms. Normal banks have four complete operation-derived errors; the bank is rejected as a whole when any option is equivalent, undefined, or correct.
