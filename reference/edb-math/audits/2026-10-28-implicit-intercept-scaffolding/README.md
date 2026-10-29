# Implicit-intercept scaffolding review — 2026-10-28

Question `17592186711063`, generated exemplar UUID `05d3989d-1da3-57a6-ac84-893d2cb998a4`, is still active at basis T10640. It belongs to KP `17592186054847`, Determining an Intercept of a Tangent or Normal Line to a Curve Given in Implicit Form, topic `17592186049470`, Implicit Differentiation.

All 14 imported practice prompts and canonical example `e-192` were read. None gives the differentiated equation, point-slope construction or instruction to set the axis coordinate to zero in the prompt. Their seven prompt diagrams were visually inspected along with the reported generated diagram; they locate the curve, given point, line and unknown intercept but do not print those calculations.

The imports have six moderate, six hard and two unclassified records, with no easy anchor. For example, `q-14680` gives 2x²+6y²=8 at (1,1) and asks for the tangent’s y-intercept without procedural help. `e-192` asks for the normal’s intercept on a translated circle, also without procedural help in the question. Such steps appear in the worked solutions.

The investigation explicitly introduced an authored easy band by supplying the differentiated circle equation, point-slope setup and axis reminder. That table identifies the reported exemplar’s exact (3,4), 25/4 calculation. This is documented authoring, not an accidental numerical simplification or a faithful copy of source scaffolding.

The current registered runtime package restores the differentiation step but still appends the point-slope formula and axis-zero reminder to every easy prompt. Its authoring account explicitly treats reduced support as part of the progression. It also says the earlier scaffolded exemplar remains published. Updating the sampler therefore did not remove this older question from the active pool.

One imported exception matters: `q-342325` asks for a y-intercept at a given point already on the y-axis, (0,2). It allows an immediate answer. The generator account correctly recognized and excluded this bypass from fresh sampling. This exception does not establish source support for adding procedural hints to every easy question.

Recommended repair: preserve the full derivative → slope → line → intercept task. Make arithmetic simpler using small coefficients, points and manageable exact results. Put the differentiation, point-slope substitution and axis-setting reminders in the worked solution. Audit and retire affected old generated descendants as well as updating runtime construction. This run is analysis only; no generator or database changes were made.

Evidence: `question.json`, `17592186054847.json`, `analysis.json`, `prompt-diagrams.png`, `prompt-diagrams.json`, and snapshots of the original `investigation.md` and later `instructional-account.md`. The registered generator reference and code hash are retained in `analysis.json`.

Additional reported question `17592186711810` is an active easy question with x²+4y²=68 at (2,−4). It asks for the tangent’s y-intercept and explicitly supplies “Use y−y₀=m(x−x₀) with the given point” and “On the y-axis, x=0.” It does not supply the derivative. This directly demonstrates that the current easy runtime branch still inserts procedural hints; it is not solely a legacy exemplar problem. The full record is retained in `question-17592186711810.json`.
