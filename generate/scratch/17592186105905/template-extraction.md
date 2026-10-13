# Template extraction

Database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Captured wrapper retained verbatim in source.json. No database writes.

## 1. Specific source descriptions

| Source | Original rating/layout | Parameters, in solution order | Original complete bank | Correct designation |
|---|---|---|---|---|
| q-18180 | unrated / radio | (10, 6, 62°) + (11, 9, 51.8°) | 62, 65, 60, 68, 58 | absent |
| q-54258 | unrated / radio | (8, 5, 80°) + (10, 7, 50°) | 45.7, 43.8, 46.5, 47.4, 42.3 | absent |
| q-72754 | moderate / fieldless | (6, 8, 85°) + (14, 16, 37°) | absent | absent |
| q-279762 | moderate / blank | (10, 6, 60°) doubled | 52 | 52 |
| q-285703 | moderate / blank | (6, 7, 50°) + (7, 8, 43°) | 35.2 | 35.2 |
| q-285737 | moderate / blank | (4, 8, 120°) doubled | 28 | 28 |
| q-54339 | moderate / radio | (8, 5, 55°) doubled | 33, 40, 38, 42, 30 | 33 |
| q-67787 | moderate / radio | (12, 14, 42.1°) + (5, 7, 103.8°) | 83.4, 88.2, 73.3, 76.6, 69.8 | 73.3 |
| q-67788 | moderate / radio | (18, 21, 60°) + (36, 30, 33°) | 416, 462, 458, 437, 422 | 458 |
| q-72768 | moderate / radio | (18, 8, 70°) doubled | 65, 135, 132, 98, 112 | 135 |

The paired lengths are adjacent at the marked included angle, not arbitrary opposite sides. BD diagrams use AB/AD at A and DC/BC at C; the AC source q-67788 uses DA/DC at D and AB/BC at B. Parallelogram sources use symmetry along AC, including the obtuse 120° source. All source side lengths are positive integers, angles are positive degrees, some are decimal, and final answers are numerals rounded to integer/tenth. Source radio values are delimiter-free scalars. Every blank supplies the field-1 slot in the prompt; the fieldless source supplies neither a slot nor a field.

Each original solution is preserved as an explicit component mask in recipes.json. Decomposition sources contain three aligned blocks: substituted 1/2 × two lengths × sine, multiplied scalar coefficient × sine, evaluated component area; repeat for second triangle; named sum, sum of two evaluated components, total; finish with the final rounded numeral in prose. Parallelograms contain two blocks: the same three triangle rows followed by named doubling, numerical doubling, final product. Sources differ in triangle labels, AC/BD splitting, dot versus adjacent-parenthesis multiplication, approximation signs, decimal grouping, three/four-place rounding prose, bold final precision, and image placement. These differences are retained. The canonical example confirms independent opposite-vertex triangle sums. Missing solutions use the complete q-285703 source chain as a clearly authored completion.

## 2. General shared pattern

Find the area of a quadrilateral by a valid diagonal decomposition. Compute each triangle from its two sides and their included angle with 1/2 ab sin C, then add; for a parallelogram exploit equal triangle areas and double. Preserve requested rounding and fixed worked solution regardless of selected error. This is an area-composition task, not an unknown-side/angle task.

## 3. Component and complete-bank mapping

Public observed-<source-id> profiles preserve every bank listed above. Original parameters are in source-cases.json; source fields own every answer ID and their exact values. Correctness is designated only where captured. No unmatched value is discarded. The six historical scalar radio banks do **not** reveal defensible wrong-operation recipes, including plausible 40 in q-54339 whose remaining values 38/42/30 cannot establish a complete operation bank. They are opaque numerical patterns, not claimed recovered distractor intent. Evidence replay generalizes their recorded values by common length scale squared; all angles/precision remain fixed. This explicit uniform scaling preserves each observed value at scale one and stays publicly available through generate. These profiles are evidence-only/ineligible, including changed scales; rounded source values need not remain mathematically keyed under scaling. No historical bank is a normal default.

Supported normal radio banks have five members chosen together before sampling. For parallelograms let u=ab sin(theta)/2: [2u, u, ab, 2ab, ab/2], representing the correct doubled triangle, omitted symmetry, omitted sine, omitted sine plus omitted triangle half, and omitted sine plus omitted symmetry. For general quadrilaterals let u and v be the two sine areas: [u+v, u, v, 2(u+v), |u-v|], representing the correct sum, one omitted triangle each way, omitted halves, and subtraction instead of addition. Each member is rounded to the prompt's exact precision. A collision, zero/negative area option, or bad geometry rejects the **whole** instance. Blanks have only the exact rounded numeral. No fabricated learner-facing feedback or distractor diagnosis is inserted.

## 4. Reusable masks and constraints

Slots replace complete numerical factors, complete angle arguments, product coefficients, evaluated decimals, total and final answer; replacement is not global number substitution. Source image references remain exact at original raw parameters; changed instances get Matplotlib rasters. The original complete problem/solution strings and attribute omission sets are reconstructed through normal mask filling even at the anchor, not returned as a source payload branch. Raw snapshots remain untouched. UUIDs depend on actual displayed prompt, solution, whole bank, correct designation and actual difficulty; shuffle seed never enters identity. The task fingerprint canonicalizes the order of the two lengths and component triangles and excludes banks, variable spelling and template/profile aliases. It includes response precision and supplied-versus-inferred splitting information. Plot identity depends on data and diagonal visibility, with atomic assets and sidecars.

### Source anomalies and supported repairs

q-18180 is unkeyed/unrated/solutionless; independent sine areas 26.4884277858 + 38.8999162122 yield 65 to integer, which is present in its bank. q-54258 is also unkeyed/unrated/solutionless: its displayed sine calculation yields 46.5 to tenth, present in its bank, but its lengths and angles are geometrically incompatible: the first triangle implies the second included angle 58.14314°, rather than 50°. Thus no raw keyed repair is silently promoted; normal data are sampled under the consistency guard.

q-72754 is fieldless. The independently derived nearest-integer area is 91, supporting a normal authored blank with a field-1 placeholder. Its source last total 91.3119 is truncated; the displayed 23.9087+67.4033 equals 91.3120. Raw retains the anomaly, normal shows the corrected rounded-component sum. Its second included angle implied by the first triangle is slightly below the printed 37° and falls outside the nominal half-degree rounding allowance; normal parameters must pass consistency rather than inherit the anomaly. Normal illustration insertion fixes its absent “illustration below.”

q-72768's first area is labeled A_ACD although prose and doubling use A_ACB; these are congruent triangles but the chain's named operand is inconsistent. Raw retains it; normal labels the computed triangle A_ACB throughout. Other source sums are the sum/doubling of already-rounded component values, rather than independent rerounding of the unrounded total; this stage is preserved. Genuine nearest-integer/tenth requirements remain unchanged. The native grader accepts canonical rounded numerals and rejects arithmetic expressions representing those numerals; those are recorded as intentional form-sensitive rejections, not grader errors. Raw missing designations and fieldless records cannot be submitted directly to the fixture harness and are reported separately, not counted as grading passes.

Native form limitation: an additional probe submitted a leading-plus rounded numeral (for example +35), which the engine rejected even though it has the same numerical value and precision. This is a rejected equivalent-entry limitation, not a source mathematical error. Faithful raw wording is preserved; normal blanks explicitly request digits and an optional decimal point. Both leading-plus and unreduced arithmetic-equivalent entries are exercised and reported as rejected. No engine change is made.
