# Template extraction: four stages

Provenance: `source.json`, math basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source-cases.json` supplies every practice replay. Source capture values and authored parameter ranges are separate.

## 1. Describe each source before generalization

Complete directed route matrices independently read from the captured diagrams are below. Row and column orders are A,B,C[,D]. The ordered unknown coordinates are the a,b,c slots or field-1,field-2,field-3. Every diagram was viewed directly with its original arrowheads; matrix values were not inferred merely from correct scalar choices.

| Source | Complete ordered matrix | Missing coordinates | Correct response | Exact complete choice bank |
|---|---|---|---|---|
| q-138940 | [[0,1,1],[0,1,2],[1,0,0]] | A→B, B→B, B→C | sum 4, inferred absent ref | {1,5,4,3,2} |
| q-139685 | [[0,1,1],[0,0,1],[1,1,0]] | A→A, B→A, C→B | sum 1, inferred absent ref | {2,5,0,1,3} |
| q-139689 | [[1,1,0],[0,1,2],[0,1,0]] | A→B, B→B, C→A | sum 2 | {4,2,0,3,1} |
| q-139719 | [[0,1,0,2],[0,0,1,0],[0,0,0,1],[0,0,1,0]] | A→D, B→C, C→C | sum 3 | {0,4,2,1,3} |
| q-319346 | [[0,2,0],[1,0,3],[2,0,0]] | A→B, B→A, B→C | fields 2,1,3 | {2}; {1}; {3}, matched by key |
| q-319412 | [[0,1,2,0],[2,0,1,0],[1,0,0,2],[0,1,1,0]] | A→C, B→A, C→C | fields 2,2,0 | {2}; {2}; {0}, matched by key |
| q-319429 | [[1,1,3],[1,2,2],[0,1,1]] | A→C, B→B, C→B | fields 3,2,1 | {3}; {2}; {1}, matched by key |

Sources use nonnegative integer counts, zero absent routes, up to three parallel routes, loops counted once per directed loop, and directional asymmetry. Three/four stations are labeled inside circles, not by list position. Numeric entries are delimited math; blank placeholders occupy whole cells. q-139689 uses the complete original HTML table with rowspan/colspan and blue heading backgrounds. Other templates use original Markdown tables including the captured extra empty trailing cells. Every radio asks a+b+c; every blank template asks for the three missing elements separately.

The five available solutions have this exact sequence: common opening “Let's examine our diagram.”; three count/direction explanations in requested order; original completion-introducing sentence; completed ordered table; only radio adds “Therefore,” and one displayed equation showing symbolic sum, three individual counts, collected scalar. Two absent solutions receive the same authored sequence. q-319429's incorrect B→C discussion is separately retained/repaired, as detailed in classification.

## 2. Generalize the shared pattern

Translate a directed route diagram to an ordered adjacency table, reading departures from row headings and arrivals from column headings. Count exactly three indicated directed relations, including zeros and loops. Report the three separate counts or their sum. All variants use the same single operation; the alternatives are peer route arrangements, not an instructional progression.

## 3. Map every source component and choice

`specs.json` records the complete matrices, missing coordinates, source IDs and image references. The prompt mask slots are **whole ordered cells**, not substitutions of single digits throughout prose. Source solution table masks preserve every completed cell. Count explanation slots comprise full count/direction paragraphs; changed counts choose zero/singular/plural grammar, and original exact paragraphs are retained when their complete values and directions agree.

Every source choice is fully accounted for by these complete finite catalog profiles:

| Profile | Computation of every option | Original correct member |
|---|---|---|
| observed_138940 | enumerate integers from 1 through 5, inclusive | m[A,B]+m[B,B]+m[B,C]=4 |
| observed_139685 | enumerate {0,1,2,3,5} | m[A,A]+m[B,A]+m[C,B]=1 |
| observed_139689 | enumerate integers from 0 through 4, inclusive | m[A,B]+m[B,B]+m[C,A]=2 |
| observed_139719 | enumerate integers from 0 through 4, inclusive | m[A,D]+m[B,C]+m[C,C]=3 |

Each catalog is an observed bounded response set, not a claimed inference about author error operations. The generator independently calculates the answer and rejects the whole instance if its sum lies outside the chosen observed catalog. There is no literal source-question return, scalar lookup of the correct option, arbitrary fitted polynomial, or per-choice random perturbation. Entire catalog content is preserved for source replay, while question matrices, counts, tables, diagrams and solutions are fully parameterized. Every blank answer is the required cell count, not a reordered tuple or sum.

The authored normal radio bank is the complete five-operation tuple `(a+b+c, a+b, a+c, sum(counts for the reversed three relations), sum(all displayed route counts))`. Wrong operations omit a queried count, reverse the three departure/arrival relations, or count the entire graph. Its eligibility condition is five distinct nonnegative values. A collision rejects the whole instance. This rejects zero/collision combinations where an omission or reversal becomes equal to the correct sum; it does not force the same three counts or a constant sum. Original zeros remain valid in observed replay catalogs and blanks. No feedback about these error operations is inserted into learner-facing content.

## 4. Reusable template and parameter constraints

Fixed: source sentences, three requested relations, diagram-first layout, route interpretation, station-letter system, table heading structure and number of fields/options. Variable: complete adjacency counts, consistent diagrams, all numeric table values, three count explanations, all sum intermediate values. Conditional: singular/plural/zero count grammar; radio final sum stage; exact original figure reuse. Hard additionally varies independent row/column heading permutations.

- Every matrix is square 3×3 or 4×4, counts are exact integers 0..3, at most 16 arrows for readable diagrams; no fractional or negative routes.
- Easy source families retain ordinary A,B,C[,D] heading order and their three unknown coordinate slots. Samplers vary originally positive known routes within 1..3, preserve originally zero known routes, and vary unknowns within 0..3. Explicit inputs receive the same count, size, density and table-order guards.
- Moderate retains the original three-node HTML sum, directed relation slots and ordinary headings, counts 0..3 and at most 16 arrows. It uses the observed scalar catalog on explicit replay and the authored whole bank by default.
- Hard is an authored four-node sum with exactly three unknowns, exactly one queried diagonal entry, at least one queried count >=2, two off-diagonal relations, two distinct nonidentity row/column heading permutations and the same 0..3/count-density limits. Samplers and explicit calls enforce all these requirements. This adds heading-direction mapping, not arithmetic branches.

The finite matrix/slot/order domain has substantial meaningful variety: validation enumerates 500 deterministic candidate draws per template and reports valid unique matrices, slots and orders. Those draws are not a claim of exhaustive finite-domain cardinality. Station renaming and option shuffle do not increase counts. Mathematical fingerprints exclude seed/profile/bank but retain complete diagram, queried relations, response shape and heading orders because direction-reading and table arrangement are assessed. Content UUIDs include actual rendered prompt, fixed complete solution and unordered complete bank; changing option order leaves identity fixed.

There are no omitted banks, unavailable images, hidden mathematical exclusions or database writes. The two absent source labels/designations/solutions and the source wrong-choice intent limitations remain explicitly reported.
