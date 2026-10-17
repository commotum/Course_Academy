# Read-only source and generator audit

All four reported records have Math Academy provenance; none was created by our generators.

| EDB question | Math Academy ID | Source role |
|---|---|---|
| 17592186514433 | q-166071 | Part 2 of the ten-part Math Academy multistep 1610, captured in task 14199167 |
| 17592186235429 | q-167324 | Part 1 of an eight-part Math Academy multistep, captured in task 13944593 |
| 17592186096417 | e-3634 | Canonical product-rule example: differentiate x cos(x) |
| 17592186514464 | q-166073 | Part 4 of the same ten-part multistep as q-166071 |

The source captures for tasks 13944593 and 14199167 both contain the exact shared context f(x)=e^x/2, g(x)=8x−2x^3/3, h(x)=−4sin(x). The full multisteps use all three functions: h differentiation, g second derivative, tangent slope of f·h, and subsequent composition/integration tasks. These functions are therefore meaningful in the original complete exercise. Repeating the full bank when presenting an individual part alone introduces irrelevant definitions.

The derivative tasks q-166071 and q-167324 are the same mathematical task with the same solution and answer −4cos(x); the local prompt differs only by whitespace. They belong to overlapping Math Academy multistep sets, with different source IDs, rather than representing new generated practice. The slope tasks q-166073 and q-167326 similarly share the same function product, point π, full answer bank, and exact worked solution. This was already recorded by the slope generator's source refresh.

The eight-part captured task has q-167324 as its first part, g'' as part 2, and the f·h tangent slope as part 3. The ten-part captured task adds a continuity task before these, and a graph/stationary-point task later. This accounts for differing source identity and part numbering despite repeated derivative and slope subtasks.

## Generator checks

- The live registered derivative generator is `generate/scratch/17592186059675.py`. Its `DATA` contains q-1847, q-1900, q-30991, q-341383, and q-47985. It does not generate the three source h-only fragments q-167324/q-167778/q-166071. The later unregistered draft likewise labels those fragments raw-only evidence.
- The live registered tangent-slope generator is `generate/scratch/17592186096619.py`. Its normal `source_problem` path supplies only f and h for named-function templates q-167326/q-167780. It never inserts g. Its sampler varies h's amplitude and the evaluation point. Three direct normal samples of q-167326 were checked; each includes the required f/h definitions and no g.
- The slope replenishment code recognizes q-166073 as the same mathematical template as q-167326. It records incomplete captured named-function fragments separately rather than claiming them as additional distinct generated tasks.
- The raw original canonical example e-3634 has `\eqalign` with a single backslash before each intended row break. This malformed TeX is already present in both frozen source captures at basis 1356. It is not generated solution text.

## Evidence

- `reference/mathacademy/question-capture/13944593/context-step-1.json`: exact original shared context, with captured MathJax/MathML source.
- `reference/mathacademy/question-capture/13944593/content.json`: original eight-part task, individual source IDs, local prompts, shared-context references, and worked solutions.
- `reference/mathacademy/capture/multivariable/14199167/content.json`: original ten-part multistep 1610, title “Applying the Rules of Differentiation and Integration,” shared context and q-166070 through q-166079.
- `generate/scratch/17592186059675-draft/classification.md`: source derivative duplicates and their exclusion from normal generation.
- `generate/scratch/17592186096619/reference/refreshed-source-q166073.json`: scalar answer/solution identity of q-166073 and q-167326.
- `generate/scratch/17592186096617/source.json`: original e-3634 canonical example and malformed row separators.
- `capture-3407/snapshot.json` and `capture-3407/parents.json`: current database identity, registered generator paths, and original multistep membership captured by the root agent.

No database or application changes were made by this audit.
