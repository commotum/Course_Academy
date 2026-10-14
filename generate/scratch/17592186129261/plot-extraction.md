# Rectangle plots

The original two native rasters were inspected at full pixels:

| Source | Reference | Native geometry and labels |
|---|---|---|
| q-160870 | images/9c/9c17c81b4abc0d4ebd1eadfe951b0eb0c2674d9eb07b785e7fd972fd00e513ae.png | u=−2..2,v=1..3; upper red v=3, lower blue v=1; axes cross at zero; u labels −2,2 |
| q-160891 | images/05/05d2ca47db245b147cb52f95a474a60ece144931c8b6e1e40c6628a99b53d690.png | u=2..3,v=1..3; upper blue v=3, lower red v=1; zero axes left/below; u labels 2,3 |

Each plot has a white background, black arrowed u/v axes, a pale blue rectangle with a blue Δ, colored solid horizontal edges, fill-only vertical edges, and light dashed **guides below** the region from its lower edge to the u axis. The vertical guides are not open region sides. Independent semantic inclusion for left,right,bottom,top is `[true,true,true,true]`, established by the source rectangle inequalities. No plotted answer options, endpoints or point markers are present; the set-boundary inclusions do not change scalar area.

General recipe: compute axis bounds from zero and all rectangle endpoints; fill the rectangle; draw upper/lower sides in the family-specific colors; draw guides only on `[0,j]` at L,H; place each u-bound label below the u axis, each v label above/below its own colored edge, and Δ at the region center. All dimensions and labels follow actual per-instance parameters. Signed easy bounds preserve the zero-axis crossing; positive nonlinear bounds leave zero axes outside the rectangle. Source has unequal axes scale (rectangles are diagrams, not area-readback tasks); generated dimensions follow source interpretation.

Matplotlib only, Figure/CanvasAgg, 559×468 native PNG at 130 dpi. Plot metadata records all four inclusions and each separate edge stroke; PNG and JSON are both required for cache hits. Native source paths are preserved only when source replay has unchanged complete geometry. Every changed rectangle is rendered. Atomic temporary file writes prevent mixed concurrent instances; fresh concurrency checks use an isolated private render directory and verify identical/different instances and no temporary files.

`plot-review.png` shows regenerated anchor geometry alongside both original native rasters, and generated signed/positive/hard examples for visual inspection. Semantic inclusion mutation is checked independently from render metadata; native-pixel labels, zero axes, bounds and guides were reviewed. No direct SVG, TikZ, or image model is used.

Canonical figures were also inspected at full pixels: `images/12/1207d8cdb8afd7c55d712caca043edfe9f0d0395343a6cbd329cf5861ec3bce7.png` shows `[1,3]×[2,4]` with the same positive-rectangle conventions; `images/e4/e4acf61532998ca5b0768b7edde16be779298c1be15ef11b14472678ba43043a.png` and `images/37/3706f0373bb39ebd41d78dd453896548ec03638a656e1fe36604f2a43108ba8e.png` are static T and T⁻¹ column-vector arrows, rendered as source-shaped TeX in current practice solution scaffolds. They are context evidence, not extra practice examples. Signed-rectangle v labels and Δ are placed independently beside the zero axis, following the original source, to prevent the zero stroke obscuring their glyphs.
