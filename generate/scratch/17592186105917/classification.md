# Classification at basis 1356

Database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. 24 practice sources; canonical example e-15607 is supporting context and is not counted.

| Observed level | Radio | Blank | Mathematical/response families | Plot need |
|---|---:|---:|---|---|
| Easy | 7 | 7 | one component scalar projection, radio or scalar blank | none |
| Moderate | 6 | 3 | sum of two reciprocal projections (radio); difference (radio/blank) | none |
| Unrated | 1 | 0 | sum radio, missing designation and solution | none |
| Hard | 0 | 0 | authored extension described below | none |

The extracted substantive families are single, pair-sum and pair-difference. There are five observed family/field layouts. Numeric substitution style, opening wording, optional evaluated-product row, norm-reduction rows and common-denominator rows are preserved as captured layout subprofiles; their differences are listed in the extraction inventory. Changed numbers are variants, not additional skill/template counts. Every observed radio has its own complete bank profile; blanks have no distractor bank.

No prompt, answer, or worked solution in this KP contains a plot. The source lesson route follows first-step 17592186106941 and step/next through introduction, negative projections, angles/magnitudes KP, deriving the component formula (17592186106944), this KP (17592186106945), and the perpendicular-vector tutorial/sibling KP. The formula and prerequisite angle/dot-product arithmetic support signed components and radicals. The next vector-projection topic is outside scope.

Normal easy asks one projection with small signed integer or familiar root components. Moderate asks two projections and combines them using integer norms and integer dot products, including paired radicals as in q-101529/q-19146/q-19147. Observed q-19143 retains its moderate label even though its norms are irrational; its dot product is rational. **Hard is an authored difficulty claim**: retain two projections and the same formula, but require an irrational dot-product sum and two distinct nonsquare norms; all three component products are nonzero. No observed moderate has an irrational dot product. This adds radical arithmetic bookkeeping within the same operation, without vector projection, solving for unknowns or angle inference. Sum and difference have equal-level status.

Source q-126501 is unrated, lacks :answer-field/correct and :question/worked-solution; original lesson JSON confirms the same incomplete widget. Independent arithmetic gives D=4 and both norms=3, so its sum is 8/3. Raw public replay preserves omissions. Its case is assigned moderate only for generator routing/analysis, explicitly authored rather than an observed difficulty. Native original-designation counts exclude this absent reference.

## Source inventory

| Source | Label | Field | Operation | Ordered numeric rows |
|---|---|---|---|---|
| q-126501 | unrated (moderate route authored) | radio | sum |  |
| q-18374 | easy | radio | single | P:sub:dot:default:0, P:raw, P:norm, P:final |
| q-101526 | easy | radio | single | P:sub:dot:default:0, P:raw, P:final |
| q-101527 | easy | radio | single | P:sub:dot:default:0, P:raw |
| q-101528 | moderate | radio | difference | P:sub:dot:default:0, P:raw, P:norm, Q:known_dot, Q:raw, Q:norm, R:combine, R:factor, R:lcm, R:result |
| q-101529 | moderate | radio | sum | P:sub:dot:braced_radical:0, P:raw, P:final, Q:known_dot_braced, Q:raw, Q:final, R:combine, R:result |
| q-126502 | easy | radio | single | P:sub:dot:default:0, P:raw, P:norm, P:final |
| q-18372 | easy | radio | single | P:sub:dot:default:1, P:raw |
| q-19139 | easy | radio | single | P:sub:dot:default:0, P:raw |
| q-19142 | easy | radio | single | P:sub:dot:default:0, P:raw |
| q-19143 | moderate | radio | difference | P:sub:dot:default:0, P:raw, Q:known_dot, Q:raw, R:combine_raw, R:common_radical |
| q-19145 | moderate | radio | difference | P:sub:dot:default:0, P:raw, P:norm, Q:known_dot, Q:raw, Q:norm, R:combine, R:factor, R:lcm, R:result |
| q-19146 | moderate | radio | difference | P:sub:dot:default:0, P:raw, P:norm, Q:known_dot, Q:raw, Q:norm, R:combine, R:factor, R:lcm, R:result |
| q-19147 | moderate | radio | sum | P:sub:dot:default:0, P:raw, P:norm, Q:known_dot, Q:raw, Q:norm, R:combine, R:factor, R:lcm, R:result |
| q-275244 | easy | blank | single | P:sub:dot:default:0, P:raw |
| q-275245 | easy | blank | single | P:sub:dot:default:0, P:raw, P:norm |
| q-275247 | moderate | blank | difference | P:sub:dot:default:0, P:raw, P:norm, Q:known_dot, Q:raw, Q:norm, Q:final, R:combine, R:result |
| q-318977 | easy | blank | single | P:sub:paren:default:0, P:eval, P:norm |
| q-318979 | easy | blank | single | P:sub:paren:default:0, P:eval, P:norm |
| q-318981 | easy | blank | single | P:sub:paren:default:0, P:raw_inside, P:final |
| q-318987 | moderate | blank | difference | P:sub:paren:default:0, P:raw, P:norm, Q:known_dot, Q:raw, Q:final, R:combine, R:collect_same_den, R:result |
| q-318988 | moderate | blank | difference | P:sub:paren:default:0, P:raw, P:norm, Q:known_dot, Q:raw, Q:final, R:combine, R:result |
| q-318978 | easy | blank | single | P:sub:paren:default:0, P:eval, P:raw, P:final |
| q-318984 | easy | blank | single | P:sub:paren:default:0, P:eval, P:raw |
