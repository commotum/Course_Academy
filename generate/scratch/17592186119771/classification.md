# Classification

Frozen provenance: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is an unchanged copy of the current capture wrapper. Owning topic 17592186050283 / MA1777 is **Triangular Matrices**. Ten practice records: six rated easy, three rated moderate, one unrated. The canonical example e-4394 is context, not an eleventh practice record.

| Source | Rating | Parameters (rows separated by ;) | Family/layout | Fields / recorded correct refs |
|---|---|---|---|---|
| q-13759 | easy | A=[7,0,0;3,-1,0;0,5,0] | lower / aligned | 2 / 1 |
| q-13769 | omitted | A=[3,0,0;6,8,0;4,5,1] | lower / inline bmatrix | 1 / 0 |
| q-126340 | easy | C=[-1,0;-5,3] | lower / aligned | 1 / 1 |
| q-126342 | easy | C=[2,1;0,-4] | upper / aligned | 1 / 1 |
| q-13761 | moderate | A=[3,0,0;0,2,0;0,0,3] | diagonal / aligned | 1 / 1 |
| q-13770 | easy | A=[1,1,2;0,2,3;0,0,3] | upper / aligned | 1 / 1 |
| q-13779 | moderate | A=[4,0,0;0,5,0;0,0,-1] | diagonal / aligned | 1 / 1 |
| q-13782 | easy | A=[9,0,0;2,7,0;0,4,1] | lower / aligned | 1 / 1 |
| q-68710 | moderate | A=[-2,0,0;0,3,0;0,0,1] | diagonal / aligned | 1 / 1 |
| q-13781 | easy | A=[2,4,7;0,2,6;0,0,3] | upper / aligned | 1 / 1 |

All eleven fields are radio/text with the same five complete categories: Identity matrix, Diagonal matrix, Upper triangular matrix, Lower triangular matrix, Other. No numerical error operations are inferred from these categorical options. The three mathematical families share a prompt stem, but their worked-solution masks differ (above, below, both). Observed presentation/layout subfamilies are lower2/aligned, lower3/aligned, lower3/bmatrix without a supplied solution, upper2/aligned, upper3/aligned, diagonal3/aligned. Public source-specific profiles retain these layouts, bank attributes, omission patterns, and the duplicate layout artifact; normal defaults choose eligible families before matrix values.

All practice plot ratings are **none**: standalone TeX matrices are notation, not plots. The canonical PNGs are small rasterized matrices; both were inspected at their original 162×74 resolution, including the blue structural-zero highlighting in the solution.

## Source anomalies and normal repairs

q-13759 has duplicate fields with the same `selection` key. The original MA1777 JSON widget (`question-13759`, lesson index 3) and its full-resolution section PNG display **one** multiple-choice widget with five labels. `authoritative-widget.json` preserves that exact widget extraction. Raw public replay keeps both fields, including the first unkeyed field; normal generation has one complete five-category radio field. The keyed capture and independent zero-region check agree on Lower triangular matrix.

q-13769 omits difficulty, worked solution and correct ref. Its raw public replay omits all three. Its normal completion receives an explicitly authored easy assignment (same 3×3 lower-triangular scan as the canonical example and rated easy siblings), the source-family worked-solution recipe, and a mathematically derived correct ref. Those additions are not counted as original designation/solution matches.

## Authored level bounds

Easy retains strict upper/lower square matrices of size 2 or 3. Moderate retains nonidentity diagonal matrices of size 3. Hard is an **authored 4×4 extension** of the same lower/upper/diagonal scan, never an observed MA rating. Strict 4×4 questions inspect six entries in the candidate zero region and find a concrete nonzero witness on the opposite side; diagonal 4×4 questions inspect twelve off-diagonal entries. The workload stays fixed within each hard family, with unordered support masks. There are no products, determinants, transposes, symbolic systems, multi-matrix selection or statement-analysis branches.

The captured introduction says an upper/lower triangular matrix is a *square* matrix with zeros below/above the diagonal; it imposes no order limit and permits any number, including zero, elsewhere. The linked prerequisite, MA862 **Zero, Square, Diagonal and Identity Matrices**, defines diagonal matrices by all off-diagonal zeros, permits zero diagonal entries, and defines identity as diagonal entries all one. Thus 4×4 changes the scan length within the same definition. The route is followed by `activity/first-step` and `step/next`: introduction → this KP → Identifying a Triangular Matrix → Identifying Correct Statements About a Matrix. Later sibling transpose/statements and downstream determinants/LU are deliberately outside this generator.

Normal prompts state the most-specific listed criterion. Identity outranks diagonal; diagonal outranks either triangular description; strict upper and strict lower cannot overlap. Other applies only when none of these categories applies. The square zero matrix is diagonal under the available bank; there is no Zero matrix option. Normal sampling excludes identity and Other as correct families because neither is an observed correct family here. This does not invalidate their category-bank role. Explicit inputs enforce the same family/size bounds as sampling.
