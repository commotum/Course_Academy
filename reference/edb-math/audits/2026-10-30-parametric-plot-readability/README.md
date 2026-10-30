# Parametric graph readability review

Read-only live review at math **T11753**, 2026-10-30. No production generator, plot assets or database records were changed. The prototype PNGs are local exploratory renders, not published replacements.

## Scope and provenance

- Reported question **17592186535273**, UUID `9e42324e-b194-5960-ac19-d09b25aae359`, is active, generated and moderate.
- Topic **17592186048293 — Graphing Curves Defined Parametrically**; KP **17592186087721 — Graphing a Curve Defined Parametrically**.
- Its original generation record was recovered from `generate/scratch/17592186087721/reference/replenishment/basis-2558/generated-published.json` and copied to `reported-generation.json`. It is `parametric-graphs-1`, template `factored-pair`, parameters a=2, b=1, h=−1, k=−2.
- The registered generator is now `parametric-graphs-2`, at `generators/e0/e05bbd4bb034c9a637cd5c1bded1fc3b11b434081eb8b2007bd60f4d13bf4a5f/generator.py`. The reported record is an older served question, not an exact current-runtime sample. The current renderer retains the same scale-selection defect.
- Live KP snapshot: `kp.json`; renderer/package snapshot: `package/`. There are 16 imported practice questions, all marked easy, plus a canonical example. There are 18 active generated questions.

## Mathematical check

For x=t(t−2)−1 and y=t(1−t)−2, the table at t=−2,−1,0,1,2 is exactly:

| t | x | y |
|---|---|---|
| −2 | 7 | −8 |
| −1 | 2 | −4 |
| 0 | −1 | −2 |
| 1 | −2 | −2 |
| 2 | −1 | −4 |

The curve and worked table agree. The defect concerns how learners can read the curve. One distractor translates the correct curve horizontally by only one unit. The old renderer's union bounds are x=[−8.5,9.5], y=[−9.6,9.6]; `MaxNLocator(7,integer=False)` produces three-unit major spacing. There is no intervening one-unit grid. See `plot-measurements.json` and `bank-17592186535273.png`.

## What was visually reviewed

All 16 imported correct choices and all 16 corresponding solution graphs were compared, plus the canonical solution graph and three complete imported answer banks (q-16190, q-73602, q-16191). Every option of the reported generated bank was inspected. Fresh current-runtime moderate and hard samples were also rendered and inspected. This review does not claim to have re-inspected every distractor in all 16 imported banks.

The four `sources-*.png` sheets pair imported correct choices with their worked graphs. The `bank-*.png` sheets retain all five choices in the selected banks.

## Evidence from imports

| Imported source | Observed presentation | Consequence |
|---|---|---|
| q-123780 / 17592186259562 | One-unit grid with every second unit labeled; unmarked choice, table dots in solution | Unit readability does not require labeling every integer or adding computed points to choices. |
| q-123781 / 17592186259563 | One-unit grid, labels every two units; sampled points at integer coordinates appear only in solution | Good model for reading nearby integer checkpoints. |
| q-73602 / 17592186393320 | One-unit grid and labels every two units; downward parabola contrasted with visibly different graph families | Grid supports coordinates; options do not require distinguishing nearly overlapping copies. |
| q-16190 / 17592186088027 | Coarser grid, sideways parabola; bank includes a reciprocal graph, an upward parabola, and other clearly different loci | It is incorrect to claim every source plots every table value on its own grid line. |
| q-16191 / 17592186281377 | Five-unit grid; broad arch contrasted with other graph families | Coarse source grids are evidence for broad shape recognition, not permission to require one-unit discrimination on a three-unit grid. |
| q-16194 / 17592186088028 | Ten-unit grid across large coordinate ranges | A universal one-unit-grid requirement would be an unjustified extrapolation across all templates. |

In all 16 reviewed correct choice/solution pairs, the choice omits the table-point dot overlay and the solution adds it. Coordinate labels and parameter-value labels are not added to the choice curves. The earlier extraction itself explicitly recorded that source choice curves have no endpoint dots; generated endpoint dots were an authored presentation extension. No directional curve arrows are part of these reviewed choices.

## Generator failure

The renderer treats axis selection as an extent/layout problem. It concatenates coordinates from all five curves, pads the resulting bounds, and passes them to an automatic major tick locator. It does not assess whether the decision-relevant table coordinates or the distance between plausible options can be resolved on that grid.

Current `package/render.py` lines 28–36 retain union bounds and use `MaxNLocator(9,integer=True)`. Integer tick labels do not imply one-unit intervals. The fresh moderate/hard samples in `current-samples.json` still render three-unit horizontal spacing. Merely increasing the requested number of ticks has not established coordinate readability.

The generator changed the task from the broad shape contrasts seen in the inspected source banks toward translated copies and deliberately shared checkpoints, without adapting the plot specification to that finer discrimination. Existing uniqueness checks establish different mathematical loci, but do not establish that the differences are readable at learner display size.

Shared bounds and equal numerical aspect across a bank are useful protections against presentation cues. They should be retained while adding a readability constraint; fitting the correct curve alone would risk a new cue and inconsistent comparisons.

## Justifiable repair contract

1. **For the reported bank**, use a regular one-unit grid with labels every two units, readable numbers close to the axes and adequate display size. All five listed checkpoints must be locatable without estimating thirds of a three-unit cell. The local `prototype-choice-*.png` renders demonstrate this without any point markers or coordinate annotations.
2. Derive one common window, grid and labeling policy for the complete bank before selecting which graph is correct. Keep dimensions, scale, contrast and line weight consistent across options. Use a regular lattice rather than special ticks only at the correct answer's coordinates.
3. Keep computed table dots, coordinate annotations, t labels and construction guides out of the answer choices. Mark table points in the worked solution, as the imports do. Finite endpoints must remain mathematically correct; any endpoint-marker convention must be consistent across the bank and separately justified.
4. Choose grid spacing according to the coordinates and distinctions actually assessed by each template. Do not impose one-unit grids indiscriminately on large-scale, irrational or decimal-coordinate source families. If the viewport and display size cannot make the required distinction readable, adjust the sampled bank/ranges or render a larger usable plot; do not make visual estimation the hidden difficulty.
5. Validate at the intended desktop and narrow-screen display sizes: checkpoints visible, grid resolution adequate, labels legible, nearby candidates distinguishable, no clipping of assessed features. Store tick positions, grid interval, plot pixel bounds and display-scale measurements alongside curve correctness. Check these properties for every possible target role so readability cannot encode the key.
6. Cover both the current renderer and existing generated stock. Updating the current immutable package alone will not change the old images on 17592186535273.

The next implementation should follow this contract and undergo a concrete plot-bank review before production publication. This turn performed the source study and produced local examples only.
