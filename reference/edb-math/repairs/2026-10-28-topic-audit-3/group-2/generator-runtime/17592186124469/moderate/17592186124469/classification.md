# Classification

Current inventory classification and durable preparation/commit are documented in [reference/current-classification.md](reference/current-classification.md). The basis-1356 analysis below remains historical source evidence.

Provenance: captured `math` basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the unchanged capture wrapper. The knowledge point has six practice questions, all single `selection` radio fields with five mathematical choices. No images, diagrams, or parameter-dependent plots occur (rating **none**).

| Template | Source | Captured level | Function and coordinates | Bank |
|---|---|---|---|---|
| square_exp | q-36211 | easy | x²+y²; (eᵗ,e⁻ᵗ) | one complete observed bank |
| log_cos | q-95056 | unrated | ln(xy); (cos t,t²) | one complete observed bank; correct designation absent |
| polylog | q-37099 | easy | 2x−xy²; (ln t,3t²) | one complete observed bank |
| cos_exp | q-95052 | easy | y cos x; (πt,eᵗ) | one complete observed bank |
| log_power | q-95054 | easy | ln(xy²); (t⁻²,eᵗ) | one complete observed bank |
| atan_product | q-95059 | easy | arctan(xy); (eᵗ,sin t) | one complete observed bank |

The five complete solutions use the same sentences: state vector chain rule; compute gradient with formal partial operators; substitute actual coordinates; differentiate the vector with both formal coordinate operators; apply the dot product and simplify. Families differ in intermediate row counts: log_power retains the unreduced partial quotients and substituted reciprocal vector, and its last block has a reduction and factored row. No redundant substitution row is inserted into the source families that have only one.

The authoritative original `/home/jake/Developer/MA/DATA/Lessons/1936/Source/1936.json` and `1936.md` confirm q-95056's five radio choices and its absence of solution/correct marking. The correct bank member is (2−t tan t)/t, derived by differentiating ln(cos(t)t²), equivalently 2/t−tan(t), on t≠0 with cos(t)>0. Its easy label and complete solution are **authored supplements**, not recovered source labels or matched source solution/designation.

Decoded answer strings were tested with `value.count(chr(92)*2)`: all 30 values return zero. There is no doubled-backslash source repair. Prompt and source solutions contain balanced TeX; no source fields are excluded.

## Missing-level rationale and bounds

The linked route is ordered by activity/first-step and step/next: Introduction → this two-variable KP → three-variable KP → derivative-at-a-point KP → rate-of-change tutorial → rate-at-point KP → intuition tutorial. Therefore the authored levels remain symbolic two-coordinate applications; they never add a third variable or evaluation at a chosen point. Key prerequisites are component dot products (177), differentiating vector-valued functions (4139), and multivariable chain rule (3173); the topic prerequisites also include the gradient (1934). The canonical example x²+2y³ with (sin t,eᵗ), and introductory xy² with (cos t,sin t), support polynomial sums, products, trig and exponential coordinates.

**Moderate** is authored f=a x²+b x y² with r=(ln t,c e^(kt)), a,b,c∈1..3, k∈1..2. Every instance requires two nonzero terms in f_x, one in f_y, two substitutions and three substantive products before reduction; the logarithmic coordinate and exponential coordinate require distinct derivative rules. Zero coefficients cannot collapse this to a source easy workload. These are unordered coefficient variations at one workload, not a progression.

**Hard** is authored f=arctan(a x y²) with r=(e^(kt),sin(lt)), a∈1..4 and k,l∈{2,3,4,5}. It retains the observed arctan outer chain and two-coordinate dot product while requiring the extra y² partial chain and both nonunit coordinate rates. The intermediate partial quotients retain both held-coordinate zero contributions. Both nonunit rates and the squared product argument are mandatory, including for explicit inputs. Bounds deliberately avoid broad algebraic complexity and unfamiliar functions.

Easy variations retain the six observed functional structures. Positive coefficients/rates are at most 4; the polylog coordinate power remains exactly 2; logarithmic powers are 1..3. Domain restrictions remain in author metadata. Each level has a normal separately labeled authored complete bank, while source bank profiles remain available for exact replay.

The finite authored catalogues contain 54 moderate parameterized tasks and 64 hard tasks, excluding seeds, option order and profiles. The validator enumerates every tuple, reads all displayed mathematical stages independently, and rejects any ambiguous full bank; cardinalities are reported only after those checks.
