# Four-stage template extraction

## 1. Specific source descriptions

`extraction.json` is the exhaustive per-original record, with literal prompt/solution, all 50 choices and original answer IDs, observed key presence, each of four graph descriptions and every prompt/solution raster. Source-cases cover all ten practice records. The canonical example is described separately in that extraction.

The distinctive source cases matter. In q-36000, panel II shows only an increasing left branch ending at the vertical axis; a hypothetical decreasing continuation is not part of the shown domain. In q-108605 panel II, the lower increasing branch and upper increasing branch have disjoint output ranges, so global continuity is unnecessary. In q-36063 panel I, an isolated closed point repeats a height already present on the main branch. In q-108581 panel IV, the closed left endpoint and the increasing right branch repeat a level; the open lower starting point does not remove that collision.

All original axes lack numbered ticks and grids. Curve tails have no direction arrows. Only axes have arrows. Most curves terminate against a frame or at an unmarked finite position. Their exact formulas and precise endpoint coordinates/inclusion cannot be uniquely inferred. Smooth bell-like, wave-like and exponential-like descriptions are visual evidence, not equations. Pixel origin and blue-ink bounds are independently fitted per panel in the extraction.

## 2. Shared pattern and purpose

Identify precisely the subset of four displayed functions that are one-to-one on their actual shown domains. Use the horizontal-line test on the entire drawn object, including all separated pieces and marked points. No inverse calculation, coordinate interpolation or choice of a restricted interval is asked.

## 3. Components and complete banks

Every raw profile's bank is the complete five text choices in `extraction.json`; each choice is represented by its Roman-label subset mask. Correct designation presence is separately recorded, rather than treating absence as an incorrect answer. Source masks are parameterized response objects; the renderer and geometry supply their referent graphs. The historical choice-bank interpretations cannot be recovered beyond inclusion/omission of panels. No arbitrary numeric distractor transformation is invented.

A raw profile combines the full captured ink coordinate cloud with a positive diagonal affine map. This preserves all horizontal and vertical intersection multiplicities, circle interiors and axis/curve direction. Parameters are `order=[0,1,2,3]` and `scale=[sx,sy]`, with 0.75 ≤ sx,sy ≤ 1. Label reordering is explicitly rejected because these are opaque captured labels. Scale 1 retains original source asset references and exact full prose. Changed scales render Matplotlib coordinate-cloud evidence. Full-scale reconstructions are independently compared with original blue-pixel bounds and recovery; unchanged asset hashes alone do not establish recipe fidelity. Raw geometry is always marked ineligible for practice.

Every observed solution's complete paragraph/bullet sequence, wording, spacing and optional diagram is preserved. The two absent solutions remain absent. At raw replay, original difficulty, solution and correct-ref presence are checked separately from values. No source ID or mathematical academy ID is invented for generated records.

## 4. Reusable templates and constraints

Authored defaults select a complete five-choice source-shaped bank before selecting a correct subset and then generating all four graphs. All choices are distinct subsets, and exactly one matches the independent whole-domain horizontal-line criterion. No first-valid wrong-choice pool is used. Invalid explicit parameters are rejected without repair.

The fixed worked solution retains the source opening sentence, horizontal-line diagram, “From the above, we see that” heading, passing-panel bullet and failing-panel bullet. An explicit concluding choice sentence is supported by the canonical example. It is one solution independent of selected learner error. The source does not supply option-specific feedback, and none is invented.

Easy uses familiar continuous linear/cubic/exponential/logarithmic/reciprocal monotone segments, or parabola/V/wave/bell/constant failures. All graphs show the whole finite domain with closed endpoints. Sign reflections vary presentation but do not increase the mathematical fingerprint. The two-piece V is a single connected familiar shape, not a boundary-membership workload.

Moderate always supplies two individually monotone pieces. Their ordinate interiors either overlap or have a strict gap. Both use straight or monotone quadratic segments; branch direction and range order vary at equal workload. Endpoints cannot decide these questions, and their incidental closure flags do not increase the fingerprint. This is grounded in the disconnected source panel q-108605 II and the joined curve/line evidence in q-36063.

Hard is an explicitly authored missing-level extension. Every panel has three individually monotone pieces; output interiors are disjoint, but adjacent output ranges touch at two heights. The learner must check open/closed membership at those two heights. A passing graph excludes exactly one endpoint at each shared height; a failing graph includes both endpoints at the lower shared height and exactly one at the upper. Exterior output endpoints remain included. These same workload bounds apply to explicit parameters. The number of pieces and boundary checks is fixed across the level. This adds precision to the same horizontal-line recognition, supported by the marked endpoints in q-108581 and the lesson's domain emphasis. It never asks which interval to select.

`catalog.json` records the finite structural task counts under the implemented samplers. Banks, source ink scaling, variable aliases and easy reflection do not add mathematical tasks. The counts describe ordered graph structures, not unlimited numerical diversity. Matplotlib coefficients remain exact rational strings in sidecars and are converted only for drawing. Independent validation partitions the entire output axis at all endpoint/critical values and checks exact preimages in every resulting cell.

## Source limitations and separate inference

q-36000 and q-36897 have no observed correct refs, difficulty or worked solution. Their inferred visual answers are “I and II only” and “I only”, respectively. Those values are evidence annotations only. Raw API replay never inserts either correct ref or a difficulty. The `source-cases.json` easy routing label is explicitly authored API routing, not an observed attribute.

The other eight captured correct designations agree with the visually shown domains. Exact symbolic geometry recovery is **0/10**, not a claimed success: all raw profiles remain evidence-only. Exact prompt/prose/bank replication and native grading of observed refs are reported on their own denominators. Eligible generated graphs have exact analytic domains and mathematical answers.
