# Four-stage extraction

## 1. Specific source descriptions

q-45165: a 0–100 m graph, ten-meter grid, horizontal labels 10 through 90, vertical speed 0–90 km/h with 10-unit grid and labels 20,40,60,80. Orange Car A decreases from 80 to 5; blue Car B from 40 to 15. Both lines cross at (80,20). The prose asks for distance, in meters. Its `selection` radio bank is 40,30,15,80,20, with neither correct ref nor solution. The complete original payload is retained in `source.json`. The authoritative widget ordering is 15,30,80,40,20; choice order is not bank identity.

q-59886: a 0–7 hour graph, unit-hour grid, distances 0–900 miles with 100-mile grid and labels 200,400,600,800. Orange Truck A travels away from the center with A=50t; blue Truck B toward it with B=750−75t. They cross at (6,300). The prose asks when distances from the center are equal, not whether trucks share a location. Bank: 3h,6h,5h,2h,4h; correct ref and solution absent. The authoritative widget confirms all five choices and no additional field.

Canonical e-13130: two pools, volume in liters vs integer days. The graph shows A=150+50t, B=775−75t on 0–7 days, 100-liter grid and 200-liter labels. Intersection (5,400). Solution sequence: contextual equality is graph intersection; annotated plot; identify point; interpret common volume and time. There is no practice bank or difficulty attached to this example.

## 2. Generalized pattern

Read the intersection of two already plotted linear contextual functions. Interpret its horizontal coordinate as distance or time. Preserve each observed paragraph, labels, units, radio field and complete five-option bank. Internally derive rational line intersection exactly before rendering or generating choices; internal algebra does not appear as a new learner task.

## 3. Component and complete-bank map

`t` denotes the horizontal intersection; `y` the vertical intersection; `dx` the graph horizontal grid spacing. Every listed source choice belongs to `selection` and is math, including truck values with the literal `h` suffix.

| Profile/source | Original choice | Replayed expression | Status |
|---|---:|---|---|
| observed_car_ratios / q-45165 | 40 | t/2 | wrong; intent unknown |
| same | 30 | 3t/8 | wrong; intent unknown |
| same | 15 | 3t/16 | wrong; intent unknown |
| same | 80 | t | independently inferred correct |
| same | 20 | t/4 | wrong; intent unknown |
| observed_truck_ratios / q-59886 | 3h | (t/2)h | wrong; intent unknown |
| same | 6h | th | independently inferred correct |
| same | 5h | (5t/6)h | wrong; intent unknown |
| same | 2h | (t/3)h | wrong; intent unknown |
| same | 4h | (2t/3)h | wrong; intent unknown |

These are explicitly **observed-expression replay profiles**, not recovered mistakes or fitted default pedagogy. A single scalar bank does not identify its author's algorithm. Linear scaling expresses a transparent parameterized replay convention; it makes no claim that the options originally arose from scaling time/distance. In cars, 40 also happens to be blue initial speed, 20 the shared speed, and 15 the blue endpoint; these coincidences do not determine the original operation. Such profiles are optional evidence replay, never the normal sampled bank. Every member is computed normally and the whole profile must satisfy positive integer values, visible domain, and unequal complete values.

Authored `adjacent_grid` contains exactly [t, t−2dx, t−dx, t+dx, t+2dx]. It represents reading one or two neighboring horizontal gridlines instead of the intersection gridline. This is a fixed complete graph-reading bank, not unrelated random numerical perturbations and not a candidate pool. Any invalid member rejects the entire sampled instance. Explicit invalid parameters raise an error and are never resampled. It has five integer positive visible x-coordinates; no distractor diagnosis enters learner content.

## 4. Reusable templates and constraints

Fixed parts: source contextual paragraphs, A/B labels, axis names/units, `selection` radio shape, five math options, and canonical solution stage sequence. Variable parts: both line intercepts/slopes, grid scales, axis limits, intersection coordinates, generated plots, final contextual values. Optional parts: annotated dot/guides/point label only in solution plot. Source geometry reuses the exact captured PNG; changed geometry always gets a Matplotlib plot. Plot paths may normalize but geometry/content must agree.

Easy trucks: initial A=0, rates A in 25,50,75,100; B in −25,−50,−75,−100; t integer 3–9; dx=1, dy=100. Moderate pools: starting A integer 50–200, rate A in 25,50,75; B in −50,−75,−100; t integer 3–9; dx=1, dy=100; authored intersections lie between numbered two-day ticks. Hard cars: slopes A in −1/2,−3/4,−1; B in −1/4,−1/2 with A<B<0; t multiple10 in 30–100; dx=dy=10; authored intersections lie between numbered twenty-meter ticks. Both intercepts are nonnegative integers, both complete displayed segments nonnegative and within bounds, and intersection y is a positive integer grid coordinate. All explicit inputs obey these guards too. Random sampling selects complete defaults before constructing banks; the exact inspected source geometries retain their original numbered ticks, and source replay may use its own shorter original graph bound if the entire observed bank is visible. Authored defaults use a bound three gridlines past t so all neighbor options are shown.

New easy/moderate/hard questions receive a fixed canonical-method solution regardless of chosen wrong option. Canonical pool prose and ordered stages are preserved; cars/trucks are labeled authored adaptations because no original solutions exist. No plotting of new nonlinear branches or new contextual quantities occurs.

Mathematical-task fingerprint includes context, both canonical rational line expressions and horizontal minor-grid/numbered-tick increments (assessed reading workload); vertical/axis window bounds, bank, profile and shuffle are excluded because they do not change the assessed intersection operation. Content identity includes version, displayed prompt, complete fixed solution and entire bank, independent of order or seed. Equivalent parameter spellings normalize before hashing. Unused profile aliases do not create identities.

Observed car and truck scalar replay profiles have narrow integral eligibility under these bounds (respectively t=80 and t=6). Their changed-geometry variants demonstrate ordinary parameterized mathematics while retaining the observed bank convention. They are not claimed to provide a broad recovered question bank. The authored default graph/grid bank supplies normal diversity. Original car hard placement and canonical pool moderate placement are fidelity-only authored placements with their original numbered tick labels; only normal defaults claim between-numbered-tick workload.

## Additional source templates at basis 2019

q-102519: airplane altitude in thousands of feet vs minutes. A=4+4t/3, B=5t/3, intersection (12,20); horizontal grid/numbered ticks every 3 minutes, vertical grid every 4 thousand feet. Source window is 0–24 by 0–36 and clips B above 36. Prompt asks elapsed minutes. The five math radio choices are 9,20,12,15,16; correct is 12. Full bank replay expressions [3t/4,5t/3,t,5t/4,4t/3] reproduce all values. Distractor intent is unresolved; this entire observed-expression profile is fidelity-only by default. Normal authored banks are [t,t−6,t−3,t+3,t+6], all visible positive distinct integer horizontal gridlines. Solution: find intersection; annotated graph; (t,y); interpret time and multiply y by 1000 for feet, with comma grouping. Replay preserves exact source wording and normalized solution. Normal samples t=9,12,15,18; B rate in {4/3,5/3,2}; slope gap in {1/3,2/3}; A starts gap*t, B starts zero. Full generated displayed segments are nonnegative and visible, with no clipping.

q-237989: water pumped between two tanks, A=25−5t/2, B=5+5t/2, intersection (4,15), window 0–7 minutes by 0–35 liters; unit-minute numbered grid and 5-liter vertical grid. Field-1 is a numeric blank with one canonical math answer 4, no distractors. Preserve the exact source paragraph and `after{{field-1}}minutes` line. Solution: equality is intersection; annotated graph; (t,y); interpret liters and minutes. Normal samples integer t=2–6, conserved rates ±{5/2,5}, B start in {0,5,10}, A start B0+2*rate*t, right boundary t+2. The sum of tank volumes stays constant. Reject any negative displayed volume. No field-type substitution or additional learner algebra.

New source replays and generated instances are recorded in `current-review.json`. No source choice is dropped, fitted mistakes are not presented as known misconceptions, and canonical source answers remain field-owned. `extensions.py` uses the same exact line arithmetic and Matplotlib renderer with contextual axis/unit labels.
