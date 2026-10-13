# Classification — Interpreting the Derivative of a Function

Captured database `math`, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The immutable wrapper and complete raw fields are in `source.json`. Seven practice sources have one `selection` radio field and exactly five text choices each. None has a plot. Different prompt structures and different worked-solution opening sentences are preserved as seven templates, each with one complete observed bank.

| Difficulty | Template / source | Assessed roles | Plot |
|---|---|---|---|
| Unrated; authored easy assignment | circle / q-48616 | area as output; radius as input | none |
| Moderate (observed) | rectangle / q-48684 | area from variable base; height fixed | none |
| Moderate (observed) | cube / q-48685 | volume from each side | none |
| Moderate (observed) | polygon / q-72104 | perimeter from each side of a regular pentagon | none |
| Hard (observed) | ellipse / q-112063 | area from major axis; minor axis fixed | none |
| Hard (observed) | square_inverse / q-48686 | side length from area | none |
| Hard (observed) | sphere_inverse / q-72099 | radius from volume | none |

The circle source omits difficulty, correct designation and worked solution. Its authoritative original widget, `/home/jake/Developer/MA/DATA/Lessons/296/Source/296.json`, question 48616, confirms the prompt and all five choices but also supplies none of these missing fields. We preserve that fact and independently infer the rate direction `area / radius`. The missing solution is authored by adapting the canonical example's three-part explanation; easy is a curriculum design claim, not recovered evidence.

Lesson order was followed through `activity/first-step` and `step/next`: introduction → determining derivative units → this KP → interpretation of an evaluated derivative → determining a net rate → relating derivatives to entry/exit rates. This KP's prerequisite is the instantaneous rate of change at a point. Its canonical example interprets spherical-balloon volume with respect to radius. Neither units, evaluated numerical rates, derivative calculation nor entry/exit arithmetic belongs to this generator.

Three explicitly authored templates supply same-skill variation. `easy_direct` uses a directly described circle/sphere size to aggregate measurement; `moderate_fixed` selects the stated varying dimension among two geometric dimensions; `hard_roles` interprets inverse size/aggregate roles or an ellipse's variable axis. Moderate regular polygon variants preserve the observed perimeter/side method. These variations have no within-level progression and require no geometric formulas. The observed cube remains moderate even though its rate interpretation is narrow.

The default catalog contains exactly **8 easy, 20 moderate and 8 hard semantic tasks**, with duplicate observed/authored contexts merged. Default selection is uniform over this finite catalog. Letter renaming, choice shuffling, and bank rephrasing do not increase these counts. `semantic-catalog.json` exposes every meaningful context, concrete prompt and mathematical-task fingerprint. Individual authored domains are 8 direct, 10 fixed-dimension and 8 inverse/axis tuples; the nine regular-polygon objects and observed cube contribute moderate contexts. Source and authored banks can share a task fingerprint while differing in presentation identity.
