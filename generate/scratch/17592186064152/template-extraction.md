# Four-stage template extraction

## Stage 1 — specific source descriptions

All seven originals are qualitative, exact, number-free single-radio questions. Function symbols denote geometric quantities, and the derivative argument specifies the independent quantity. Answers are complete English fragments, with embedded single-symbol math preserved. Full original prompts, options and all available solution sentences appear in review.md; raw missing fields remain in source.json.

### circle — q-48616 (DB 17592186064831)

Consider a circle such that the radius $r$ can vary. If $A$ is the area of the circle, what is the best interpretation of $A^{′}(r)$?

Physical output: area; physical input: radius; object: circle. Original symbols: A and r. Field shape: five text options, selection radio. Bank profile: observed_circle.

Solution sequence: absent; supported authored function-declaration, differential-quotient and rate-conclusion repair.

### rectangle — q-48684 (DB 17592186064834)

Consider a rectangle such that the height is fixed but its base $b$ can vary. What is the best interpretation of ${A}^{′}(b)$ if $A$ is the area of the rectangle?

Physical output: area; physical input: base; object: rectangle. Original symbols: A and b. Field shape: five text options, selection radio. Bank profile: observed_rectangle.

Solution sequence: one function-declaration sentence; one displayed three-member chain (derivative = differential quotient = qualitative change quotient); one rate-conclusion sentence. No optional rows or computed values.

### ellipse — q-112063 (DB 17592186247238)

Consider an ellipse such that its major axis $a$ can vary while its minor axis is fixed. What is the best interpretation of ${S}^{′}(a)$ if $S$ is the area enclosed by the ellipse?

Physical output: area; physical input: major axis; object: ellipse. Original symbols: S and a. Field shape: five text options, selection radio. Bank profile: observed_ellipse.

Solution sequence: one function-declaration sentence; one displayed three-member chain (derivative = differential quotient = qualitative change quotient); one rate-conclusion sentence. No optional rows or computed values.

### cube — q-48685 (DB 17592186329905)

Consider a cube such that the length of each side $s$ varies. What is the best interpretation of ${V}^{′}(s)$ if $V$ is the volume of the cube?

Physical output: volume; physical input: each side; object: cube. Original symbols: V and s. Field shape: five text options, selection radio. Bank profile: observed_cube.

Solution sequence: one function-declaration sentence; one displayed three-member chain (derivative = differential quotient = qualitative change quotient); one rate-conclusion sentence. No optional rows or computed values.

### square_inverse — q-48686 (DB 17592186329906)

Consider a square such that its area $A$ can vary. What is the best interpretation of ${s}^{′}(A)$ if $s$ is the length of each side of the square?

Physical output: each side; physical input: area; object: square. Original symbols: s and A. Field shape: five text options, selection radio. Bank profile: observed_square_inverse.

Solution sequence: one function-declaration sentence; one displayed three-member chain (derivative = differential quotient = qualitative change quotient); one rate-conclusion sentence. No optional rows or computed values.

### sphere_inverse — q-72099 (DB 17592186339058)

Consider a sphere such that its volume $V$ can vary. What is the best interpretation of ${r}^{′}(V)$ if $r$ is the length of the radius of the sphere?

Physical output: radius; physical input: volume; object: sphere. Original symbols: r and V. Field shape: five text options, selection radio. Bank profile: observed_sphere_inverse.

Solution sequence: one function-declaration sentence; one displayed three-member chain (derivative = differential quotient = qualitative change quotient); one rate-conclusion sentence. No optional rows or computed values.

### polygon — q-72104 (DB 17592186339059)

Consider a regular pentagon such that the length $s$ of each side varies. What is the best interpretation of ${P}^{′}(s)$ if $P$ is the perimeter of the pentagon?

Physical output: perimeter; physical input: each side; object: pentagon. Original symbols: P and s. Field shape: five text options, selection radio. Bank profile: observed_polygon.

Solution sequence: one function-declaration sentence; one displayed three-member chain (derivative = differential quotient = qualitative change quotient); one rate-conclusion sentence. No optional rows or computed values.

## Stage 2 — generalized family and scope

Interpret a derivative by matching its function symbol to the dependent physical quantity and its argument to the independent physical quantity. State the instantaneous rate of output change with respect to input change. Fixed dimensions are context cues, not additional differentiations. No numerical evaluations, derivative formulas, geometric calculations or units are required.

The observed prompt/opening masks remain seven separate templates. Cosmetic symbol changes alone do not define a new mathematical task. Authored extensions vary the actual geometric role tuple within the specified level domain, preserving the same conceptual operation.

## Stage 3 — every component and complete bank recipe

For semantic rate options, the operation is an ordered pair `(changing output, changing input)`. Reversal exchanges the pair; other-input/output errors replace the specified physical quantity; value options discard the rate relation and name a physical quantity. These are completely identified textual operations, not underdetermined numerical distractor fits. Every profile contains all its five observed operations together; no pooled first-valid selection is used.

### observed_circle

Prompt mask: `Consider a circle such that the radius ${ind}$ can vary. If ${dep}$ is the area of the circle, what is the best interpretation of ${dep}^{{′}}({ind})$?`

Opening mask: `The function ${dep}({ind})$ gives the area of a circle with radius ${ind}.$ So`

| Operation | Full source option and parameter mask | Designation |
|---|---|---|
| `value_out` | The area of a circle with radius $r$ — mask `The area of a circle with radius ${ind}$` | wrong interpretation |
| `reverse` | The rate at which the radius changes as the area changes — mask `The rate at which the radius changes as the area changes` | wrong interpretation |
| `value_in` | The length of the radius of the circle — mask `The length of the radius of the circle` | wrong interpretation |
| `other_value` | The circumference of the circle — mask `The circumference of the circle` | wrong interpretation |
| `correct` | The rate at which the area changes as the radius changes — mask `The rate at which the area changes as the radius changes` | supported inferred correct; original designation missing |

Bank reproduction: all five options match exactly at the source parameters. Original choice order is incidental; complete bank membership and correct meaning are preserved.

### observed_rectangle

Prompt mask: `Consider a rectangle such that the height is fixed but its base ${ind}$ can vary. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the area of the rectangle?`

Opening mask: `The function ${dep}({ind})$ gives the area of a rectangle with base ${ind}.$ So`

| Operation | Full source option and parameter mask | Designation |
|---|---|---|
| `value_out` | The area of a rectangle with base $b$ — mask `The area of a rectangle with base ${ind}$` | wrong interpretation |
| `fixed_reverse` | The rate at which the height changes as the area changes — mask `The rate at which the height changes as the area changes` | wrong interpretation |
| `value_in` | The length of the base of the rectangle — mask `The length of the base of the rectangle` | wrong interpretation |
| `fixed` | The rate at which the area changes as the height changes — mask `The rate at which the area changes as the height changes` | wrong interpretation |
| `correct` | The rate at which the area changes as the base changes — mask `The rate at which the area changes as the base changes` | original correct |

Bank reproduction: all five options match exactly at the source parameters. Original choice order is incidental; complete bank membership and correct meaning are preserved.

### observed_ellipse

Prompt mask: `Consider an ellipse such that its major axis ${ind}$ can vary while its minor axis is fixed. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the area enclosed by the ellipse?`

Opening mask: `The function ${dep}({ind})$ gives the area of the ellipse with major axis ${ind}.$ So,`

| Operation | Full source option and parameter mask | Designation |
|---|---|---|
| `correct` | The rate at which the area changes as the major axis changes — mask `The rate at which the area changes as the major axis changes` | original correct |
| `value_in` | The major axis of an ellipse with area S — mask `The major axis of an ellipse with area {dep}` | wrong interpretation |
| `other_rate` | The rate at which the perimeter changes as the major axis changes — mask `The rate at which the perimeter changes as the major axis changes` | wrong interpretation |
| `two_inputs` | The rate at which the major axis changes as the minor axis changes — mask `The rate at which the major axis changes as the minor axis changes` | wrong interpretation |
| `value_out` | The area of an ellipse with major axis $a$ — mask `The area of an ellipse with major axis ${ind}$` | wrong interpretation |

Bank reproduction: all five options match exactly at the source parameters. Original choice order is incidental; complete bank membership and correct meaning are preserved.

### observed_cube

Prompt mask: `Consider a cube such that the length of each side ${ind}$ varies. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the volume of the cube?`

Opening mask: `The function ${dep}({ind})$ gives the volume of a cube with side ${ind}.$ So,`

| Operation | Full source option and parameter mask | Designation |
|---|---|---|
| `value_in` | The length of each side of the cube — mask `The length of each side of the cube` | wrong interpretation |
| `reverse` | The rate at which each side changes as the volume changes — mask `The rate at which each side changes as the volume changes` | wrong interpretation |
| `correct` | The rate at which the volume changes as each side changes — mask `The rate at which the volume changes as each side changes` | original correct |
| `value_out` | The volume of a cube with side $s$ — mask `The volume of a cube with side ${ind}$` | wrong interpretation |
| `other_rate` | The rate at which the surface area of the cube changes as each side changes — mask `The rate at which the surface area of the cube changes as each side changes` | wrong interpretation |

Bank reproduction: all five options match exactly at the source parameters. Original choice order is incidental; complete bank membership and correct meaning are preserved.

### observed_square_inverse

Prompt mask: `Consider a square such that its area ${ind}$ can vary. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the length of each side of the square?`

Opening mask: `The function ${dep}({ind})$ gives the length of each side of a square with area ${ind}.$ So,`

| Operation | Full source option and parameter mask | Designation |
|---|---|---|
| `correct` | The rate at which each side changes as the area changes — mask `The rate at which each side changes as the area changes` | original correct |
| `value_out` | The length of each side of the square — mask `The length of each side of the square` | wrong interpretation |
| `other_rate` | The rate at which each side of the square changes as the perimeter changes — mask `The rate at which each side of the square changes as the perimeter changes` | wrong interpretation |
| `reverse` | The rate at which the area changes as each side changes — mask `The rate at which the area changes as each side changes` | wrong interpretation |
| `value_in` | The area of a square with side $s$ — mask `The area of a square with side ${dep}$` | wrong interpretation |

Bank reproduction: all five options match exactly at the source parameters. Original choice order is incidental; complete bank membership and correct meaning are preserved.

### observed_sphere_inverse

Prompt mask: `Consider a sphere such that its volume ${ind}$ can vary. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the length of the radius of the sphere?`

Opening mask: `The function ${dep}({ind})$ gives the length of the radius of a sphere with volume ${ind}.$ So,`

| Operation | Full source option and parameter mask | Designation |
|---|---|---|
| `other_inverse` | The rate at which the volume changes as the surface area changes — mask `The rate at which the volume changes as the surface area changes` | wrong interpretation |
| `reverse` | The rate at which the volume changes as the radius changes — mask `The rate at which the volume changes as the radius changes` | wrong interpretation |
| `other_rate` | The rate at which the surface area changes as the radius changes — mask `The rate at which the surface area changes as the radius changes` | wrong interpretation |
| `correct` | The rate at which the radius changes as the volume changes — mask `The rate at which the radius changes as the volume changes` | original correct |
| `other_input` | The rate at which the radius changes as the surface area changes — mask `The rate at which the radius changes as the surface area changes` | wrong interpretation |

Bank reproduction: all five options match exactly at the source parameters. Original choice order is incidental; complete bank membership and correct meaning are preserved.

### observed_polygon

Prompt mask: `Consider a regular {shape} such that the length ${ind}$ of each side varies. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the perimeter of the {shape}?`

Opening mask: `The function ${dep}({ind})$ gives the perimeter of a {shape} with side ${ind}.$ So,`

| Operation | Full source option and parameter mask | Designation |
|---|---|---|
| `correct` | The rate at which the perimeter changes as each side changes — mask `The rate at which the perimeter changes as each side changes` | original correct |
| `other_rate` | The rate at which the area changes as each side changes — mask `The rate at which the area changes as each side changes` | wrong interpretation |
| `reverse` | The rate at which each side changes as the perimeter changes — mask `The rate at which each side changes as the perimeter changes` | wrong interpretation |
| `other_input` | The rate at which the perimeter changes as the area changes — mask `The rate at which the perimeter changes as the area changes` | wrong interpretation |
| `other_inverse` | The rate at which each side changes as the area changes — mask `The rate at which each side changes as the area changes` | wrong interpretation |

Bank reproduction: all five options match exactly at the source parameters. Original choice order is incidental; complete bank membership and correct meaning are preserved.

## Stage 4 — reusable masks, constraints and computations

Fixed: question wording, original field layout, five-option bank operation set, one worked-solution sequence, and semantic relationship output/input. Variable: complete dependent/independent symbol components, eligible regular-polygon object, or an authored complete geometric role tuple. Conditional: the held dimension sentence is present only in contexts that explicitly state one; source-specific punctuation (So / So,) and derivative braces are preserved. No optional algebraic rows are introduced.

Exact computation: identify the function/argument roles first; form the correct ordered rate pair; construct every other bank member from the profile operations; reject the whole bank if values or eligible correct interpretations collide. No answer lookup, random numerical perturbation or literal-source return branch exists. The generator does not load source payloads.

Parameters: single symbols from A, B, P, S, V, a, b, h, r, s, x, y, C, d, with distinct output/input symbols. Polygon domain: regular triangle, square, pentagon, hexagon, heptagon, octagon, nonagon, decagon, dodecagon. Authored contexts are enumerated whole tuples in the script and semantic-catalog.json; explicit calls use identical bounds. Physical dimensions are positive and fixed dimensions remain fixed; ellipses retain major/minor ordering. No numerical values are sampled.

Easy design: direct circle/sphere aggregate measure as a function of radius/diameter, anchored to the circle source and spherical-balloon canonical example. Moderate design: explicitly distinguish one varying dimension from one fixed dimension, anchored to the rectangle source; regular-polygon perimeter/side variants retain the observed polygon demand. Hard design: inverse size/aggregate roles or one variable ellipse axis, anchored to all three hard sources. Each level is unordered same-skill practice.

Identity: the mathematical task fingerprint includes geometric object, output quantity, input quantity and fixed quantity, excluding symbol names, seed, option order and complete bank. Presentation identity includes actual prompt, complete fixed solution, sorted displayed bank, correct designation, difficulty and generator version. Default source/authored duplicates are merged into a finite uniform catalog: 8 easy, 20 moderate, 8 hard.

## Anomalies, interpretation criterion and limitations

q-48616 has no captured difficulty, solution or correct designation; the original MA widget confirms the same bank but does not fill these omissions. Its field count and all options are preserved. The inferred correct meaning follows directly from A being area and r radius; it is not counted as an observed matched designation. No source question is excluded.

The source circle bank includes the circumference. Numerically, d(πr²)/dr = 2πr equals circumference, but the requested best interpretation is the rate relation, not a quantity named without the relation. This distinction is retained and is checked as response eligibility, rather than incorrectly reporting a duplicate textual interpretation. This KP neither asks for nor displays that derivative calculation.

The source Change in / Change in chain is qualitative differential shorthand. It does not specify finite increments or assert an average rate over a numerical interval. The prerequisite and dF/dx notation identify instantaneous change. Authored contexts explicitly use Instantaneous change in the numerator; source replay preserves complete source prose.

Authored banks are separately labeled and use correct rate, reversed rate, output value, input value, and rate with the fixed input (when present) or another output. They preserve five text options, but do not claim recovery of source banks. The triangle/parallelogram distractors never assume their perimeter is determined by base/height alone.

Plot requirement is none for all practice templates; plot-extraction.md records the inspected canonical sphere as non-assessed decoration.
