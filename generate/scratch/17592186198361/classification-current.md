# Current source classification

The captured math basis is 2590, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `reference/initial/kp.edn` preserves all fourteen practice sources and the canonical example at this basis. It supersedes the seven-source basis-1356 inventory classification; the historical snapshot remains the replay fixture for the unchanged validated generator.

Every practice template uses one radio field named `selection` and five mathematical choices. All have plot rating **none**; no images occur in their prompt, bank or solution. Each row represents a distinct prompt/solution template and its complete source-bank profile. New templates are classified for inventory; generation remains limited to the previously validated families.

| Source | Difficulty | Supplied map and response | Inventory decision |
|---|---|---|---|
| 17592186198948 / q-38129 | unrated | x+y, y−x; transformed integral of y²−x² | Missing key/solution/rating; excluded |
| 17592186198950 / q-38371 | moderate | xy, y+x; evaluate absolute-Jacobian exponential | Wrong rectangular image and omitted second branch; excluded |
| 17592186373909 / q-160897 | moderate | y/x², xy; evaluate xy | Valid, positive-quadrant bijection |
| 17592186375103 / q-38369 | easy | 2x+y, y; transformed quadratic integral | Valid |
| 17592186375495 / q-82808 | easy | y−x, x+y; transformed 8xy integral | Two complete answers equal zero; excluded |
| 17592186375502 / q-82827 | easy | 2x+5y, x+3y; transformed exponential integral | Valid |
| 17592186375509 / q-83647 | easy | x+y, y−x; transformed squared sum integral | Valid |
| 17592186481371 / q-83656 | moderate | eˣ, eʸ; evaluate y | Valid, transformed ln(v)/(uv) |
| 17592186481424 / q-82798 | easy | 2y−x, y−x; transformed x² integral | Valid, inverse x=u−2v, y=u−v |
| 17592186481429 / q-82818 | easy | x+1, y+(x+1)²; transformed x−y+1 integral | Valid, global triangular inverse |
| 17592186481431 / q-160850 | moderate | x+y, x−y; evaluate fractional power product | Valid, v≥0 and transformed uv^(3/2)/2 |
| 17592186481440 / q-82911 | moderate | x+y, x−y; evaluate x²−y² | Valid, transformed uv/2 |
| 17592186493956 / q-160899 | moderate | y/x, xy; evaluate exp(−xy/2) | Correct bank, but worked solution switches dv to du mid-integration; conservatively excluded |
| 17592186493973 / q-82985 | moderate | x+3y, x+2y; evaluate ratio | Valid, transformed u/v |

Totals: six easy templates, seven moderate templates, one unrated template, zero observed hard templates; fourteen complete source-bank profiles. Five easy and five moderate source tasks pass mathematical bank and solution review, before learner exposure/reservation exclusions. `audit-current.py` independently derives inverses, Jacobians, transformed integrands and exact integrals, evaluates every complete option, verifies stored keys, rejects full-value collisions and checks the ten eligible source banks through the native radio grader. Its retained output contains every source prompt/solution, bank values and explicit exclusions. Existing mathematical and incomplete source defects are preserved.

The generator's easy/moderate families, original complete-bank replay, authored bank extensions, bounds, fixed transformation roles and solution sequences remain documented in `template-extraction.md`. Additional source families above do not enter its sampling domain. The previously reviewed hard extension keeps the supplied y/x²,xy transformation, replacing xy with (xy)² and quadratic endpoint arithmetic with cubic endpoints; it remains an authored difficulty judgment. Fresh validation checked all 45 hard and 84 moderate bounded tasks. Changed bounds alter the assessed integration limits or endpoint arithmetic; identity, seed, bank and order changes do not establish distinct tasks.
