# Classification

Snapshot: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Owning topic 17592186050482 / MA 4132, Computing Double Integrals Using a Change of Variables. Source wrapper is preserved in `source.json`.

| Template | Source database ID / MA ID | Observed difficulty | Fields / bank | Plot rating |
|---|---|---|---|---|
| difference |17592186198948 / q-38129|unrated|one radio, five complete definite integrals; missing correct ref|none|
| sum_product_evidence |17592186198950 / q-38371|unrated|one radio, five exponential scalars; missing correct ref|none|
| ratio_product |17592186373909 / q-160897|moderate|one radio, five scalars|none|
| triangular_quadratic |17592186375103 / q-38369|easy|one radio, five complete definite integrals|none|
| product |17592186375495 / q-82808|easy|one radio, five complete definite integrals|none|
| exponential |17592186375502 / q-82827|easy|one radio, five complete definite integrals|none|
| sum_square |17592186375509 / q-83647|easy|one radio, five complete definite integrals|none|

Seven distinct practice Markdown/value templates and seven observed complete banks; four rated easy templates, one rated moderate, two unrated, zero observed hard. The two unrated records also lack worked solutions; omission presence is faithfully retained by `profile='observed'` and cannot count as matched correct designations. Original MA 4132 HTML/JSON and full resolution question1/question2 rasters confirm the existing five-choice layouts without a captured correct designation.

The canonical example e-7285 supplies u=4x+2y, v=y−x and transforms a sine integrand without evaluating it. Its only two images are coordinate-column transformation notation, inspected at original resolution; they contain no parameter-dependent geometry. Practice questions have no images. No diagram rendering is needed.

Lesson route reconstructed by activity/first-step and step/next: introduction17592186199250 → this KP17592186199251 → transformation inferred from domain17592186199273 → transformation inferred from integrand17592186199274. Key prerequisite is Computing Areas Using a Change of Variables (MA 1998); it supplies Jacobians and transformed domains. Scope here always **gives** the transformation, and does not ask learners to infer it.

Normal easy generation covers all four observed setup families and an explicitly authored completion of unrated `difference`. Normal moderate retains the supplied nonlinear ratio/product map and logarithmic/quadratic endpoint integration. Authored hard uses that same map with (xy)²: cubic rather than quadratic endpoint arithmetic, keeping the same four formal teaching steps and ten integration rows. This hard label is a curriculum-grounded design claim, never a recovered source rating. Bounds keep familiar logarithms (u upper bound4,9,16), positive v endpoints and integer cubic endpoints through 6. There is no within-level progression or new transformation branch.
