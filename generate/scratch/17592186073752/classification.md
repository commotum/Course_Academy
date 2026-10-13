# Classification

Database math, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the unchanged capture wrapper. Six practice sources: three easy and three unrated; canonical example excluded from practice counts.

| Template | Source IDs | Observed label | Fields | Banks | Plots |
|---|---|---|---|---|---|
| coefficient_b_first | q-167194, q-167210 | easy | two blanks, a and b scalar fragments | two field-owned single-answer banks each | none |
| coefficient_a_first | q-167226 | easy | two blanks, a and b scalar fragments | two field-owned single-answer banks | none |
| tuple_xy | q-171690 | unrated; authored easy | two blanks inside supplied ordered pair | missing answer banks and refs | none |
| direct_pq | q-5179 | unrated; authored easy | one scalar radio, p-q | one complete five-option profile | none |
| difference_ab | q-4133 | unrated; authored moderate | one scalar radio, a-b | one complete five-option profile | none |

The coefficient templates have different term order in both substitution and collection. Number changes within coefficient_b_first do not create separate templates. There are five observed mathematical/layout templates and two observed radio profiles. Hard adds a clearly authored `unit_pair` template with two supplied tuple fragments.

The route was traversed from activity/first-step 17592186074657 via step/next: Introduction -> this KP (17592186074658) -> Challenging substitution KP (17592186074659). The preceding introduction substitutes an already isolated unit-coefficient relation and backsubstitutes. Canonical e-13009 isolates x from x-y=4, substitutes in x+2y=16, and solves/backsubstitutes. Prerequisites: Introduction to Systems of Linear Equations (2225), Solving Two-Variable Equations (356). The sibling challenging KP isolates a nonunit coefficient and returns a rational coordinate. Other later topics separately cover decimal coefficients, fractional coefficients, nonlinear equations and modelling; none is introduced here.

Authored moderate peers use signed small integer coefficients, a unit coefficient on b, integer coordinates, and the source a-b response. Authored hard peers retain a unit isolation coefficient, use integer coefficients, and require exact noninteger coordinates with reduced denominators 2..7 and absolute values <=12. This is an authored difficulty distinction, supported by the basic substitution route and prerequisite single-equation algebra; it is not an observed hard label. No progression is imposed within either level.

Source anomalies: all six have an unmatched literal system brace in prompt or solution. q-171690 also has a malformed comma delimiter. The captured lesson 487/Source/487.json confirms two free-entry math-editor blanks with separately supplied '(' ',' ')' and confirms both five-option radio widgets. It contains no correct labels/solutions for these three unrated sources. Four missing correct field refs are independently derived, counted separately. Contextual coefficient prompts rely on an omitted preceding relation; source replay preserves the original prompt, while normal defaults add that relation. Raw source strings remain in source.json and review.md.
