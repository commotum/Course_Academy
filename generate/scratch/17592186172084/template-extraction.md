# Template extraction

## Stage 1 — Specific source descriptions

All prompts use one full-plane blue-arrow diagram and the identical question sentence. Source coordinate axes have arrowheads and x/y labels but no numeric ticks; identification is qualitative. Source answer math is delimiter-free, named F/G/H/K, and uses x/y input plus i/j output components. Captured notation is rendered by a whole-component formatter; source spaces and thin spaces are preserved per profile. Exact source strings and all fields remain in source.json and source-cases.json.

### q-122296

Underlying field at original parameters: ('a*x', '-a'). horizontal variation → vertical negative → F (authored completion). Original stage sequence has two elimination bullet paragraphs, two displayed bank-equation blocks, and one inline final conclusion, except q122296 has none captured. Parameter a originally 1, sx=sy=1, swap=false. Field layout: selection, radio, five choices.

### q-122463

Underlying field at original parameters: ('-a', 'a'). horizontal negative → vertical positive → G. Original stage sequence has two elimination bullet paragraphs, two displayed bank-equation blocks, and one inline final conclusion, except q122296 has none captured. Parameter a originally 1, sx=sy=1, swap=false. Field layout: selection, radio, five choices.

### q-122629

Underlying field at original parameters: ('a', 'a*x'). horizontal positive → vertical varies with x → K. Original stage sequence has two elimination bullet paragraphs, two displayed bank-equation blocks, and one inline final conclusion, except q122296 has none captured. Parameter a originally 1, sx=sy=1, swap=false. Field layout: selection, radio, five choices.

### q-122631

Underlying field at original parameters: ('0', '-a*y'). horizontal zero → vertical varies with y → F. Original stage sequence has two elimination bullet paragraphs, two displayed bank-equation blocks, and one inline final conclusion, except q122296 has none captured. Parameter a originally 1, sx=sy=1, swap=false. Field layout: selection, radio, five choices.

### q-122632

Underlying field at original parameters: ('0', 'a*x'). horizontal zero → vertical varies with x → H. Original stage sequence has two elimination bullet paragraphs, two displayed bank-equation blocks, and one inline final conclusion, except q122296 has none captured. Parameter a originally 1, sx=sy=1, swap=false. Field layout: selection, radio, five choices.

### q-122633

Underlying field at original parameters: ('a*y', '0'). vertical zero → horizontal varies with y → G. Original stage sequence has two elimination bullet paragraphs, two displayed bank-equation blocks, and one inline final conclusion, except q122296 has none captured. Parameter a originally 1, sx=sy=1, swap=false. Field layout: selection, radio, five choices.

### q-122634

Underlying field at original parameters: ('a', '0'). vertical zero → horizontal positive → K. Original stage sequence has two elimination bullet paragraphs, two displayed bank-equation blocks, and one inline final conclusion, except q122296 has none captured. Parameter a originally 1, sx=sy=1, swap=false. Field layout: selection, radio, five choices.

### q-122637

Underlying field at original parameters: ('0', '-5*a'). horizontal zero → vertical negative → H. Original stage sequence has two elimination bullet paragraphs, two displayed bank-equation blocks, and one inline final conclusion, except q122296 has none captured. Parameter a originally 1, sx=sy=1, swap=false. Field layout: selection, radio, five choices.

### q-122630

Underlying field at original parameters: ('-2*a', 'a*y'). horizontal negative → vertical varies with y → H. Original stage sequence has two elimination bullet paragraphs, two displayed bank-equation blocks, and one inline final conclusion, except q122296 has none captured. Parameter a originally 1, sx=sy=1, swap=false. Field layout: selection, radio, five choices.

## Stage 2 — Shared mathematical pattern

Match vector-component zero/nonzero status, sign, and variation across horizontal/vertical positions to a complete proposed formula. Use elimination and conclude with one named function. Easy has no variable components, moderate exactly one, authored hard exactly two. Distinct prose/stage patterns remain distinct templates. Choices are complete fields, not independently graded components.

## Stage 3 — Complete component and bank mapping

Each table below maps every original option to its whole-bank recipe. Every field key is selection. Recipes are symbolic expressions in common signed scale a, followed by the same signed-coordinate transformation R V(R^-1 p) as the prompt field. Scalar multiples, constant choices, mixed dependencies and signs are observed expression patterns; their cognitive error intentions are unresolved. None of the listed is retained in every profile. It is wrong because exactly one displayed full field matches. No option is dropped or replaced.

### q-122296

| Exact original full value | Recipe before R | Original designation |
|---|---|---|
| `F(x, y) = xi - j` | `(a*x, -a)` | missing; independently derived correct |
| `H(x, y) = i + 2j` | `(a, 2*a)` | designation absent |
| `G(x, y) =-xi + yj` | `(-a*x, a*y)` | designation absent |
| `K(x, y) = i - 2j` | `(a, -2*a)` | designation absent |
| None of the listed | fixed text | designation absent; independently derived incorrect |

### q-122463

| Exact original full value | Recipe before R | Original designation |
|---|---|---|
| `F(x,y)=i-2\,j` | `(a, -2*a)` | incorrect |
| `G(x,y)=-i+j` | `(-a, a)` | correct |
| `K(x,y)=-j` | `(0, -a)` | incorrect |
| `H(x,y)=i` | `(a, 0)` | incorrect |
| None of the listed | fixed text | incorrect |

### q-122629

| Exact original full value | Recipe before R | Original designation |
|---|---|---|
| `H(x,y)=2\,i-j` | `(2*a, -a)` | incorrect |
| `F(x,y)=-i-j` | `(-a, -a)` | incorrect |
| `K(x,y)=i+x\,j` | `(a, a*x)` | correct |
| `G(x,y)=i+2\,j` | `(a, 2*a)` | incorrect |
| None of the listed | fixed text | incorrect |

### q-122631

| Exact original full value | Recipe before R | Original designation |
|---|---|---|
| `K(x,y)=-2\,j` | `(0, -2*a)` | incorrect |
| `G(x,y)=-i+2\,j` | `(-a, 2*a)` | incorrect |
| `H(x,y)=x\,i-y\,j` | `(a*x, -a*y)` | incorrect |
| `F(x,y)=-y\,j` | `(0, -a*y)` | correct |
| None of the listed | fixed text | incorrect |

### q-122632

| Exact original full value | Recipe before R | Original designation |
|---|---|---|
| `K(x,y)=-i-2\,j` | `(-a, -2*a)` | incorrect |
| `H(x,y)=x\,j` | `(0, a*x)` | correct |
| `G(x,y)=5\,j` | `(0, 5*a)` | incorrect |
| `F(x,y)=i+j` | `(a, a)` | incorrect |
| None of the listed | fixed text | incorrect |

### q-122633

| Exact original full value | Recipe before R | Original designation |
|---|---|---|
| `H(x,y)=y\,i+j` | `(a*y, a)` | incorrect |
| `F(x,y)=x\,i` | `(a*x, 0)` | incorrect |
| `G(x,y)=y\,i` | `(a*y, 0)` | correct |
| `K(x,y)=-i` | `(-a, 0)` | incorrect |
| None of the listed | fixed text | incorrect |

### q-122634

| Exact original full value | Recipe before R | Original designation |
|---|---|---|
| `K(x,y)=i` | `(a, 0)` | correct |
| `F(x,y)=-j` | `(0, -a)` | incorrect |
| `H(x,y)=-i` | `(-a, 0)` | incorrect |
| `G(x,y)=j` | `(0, a)` | incorrect |
| None of the listed | fixed text | incorrect |

### q-122637

| Exact original full value | Recipe before R | Original designation |
|---|---|---|
| `K(x,y)=-3\,i` | `(-3*a, 0)` | incorrect |
| `G(x,y)=2\,j` | `(0, 2*a)` | incorrect |
| `F(x,y)=4\,i` | `(4*a, 0)` | incorrect |
| `H(x,y)=-5\,j` | `(0, -5*a)` | correct |
| None of the listed | fixed text | incorrect |

### q-122630

| Exact original full value | Recipe before R | Original designation |
|---|---|---|
| `K(x,y)=x\,i+j` | `(a*x, a)` | incorrect |
| `H(x,y)=-2\,i+y\,j` | `(-2*a, a*y)` | correct |
| `G(x,y)=i+j` | `(a, a)` | incorrect |
| `F(x,y)=-i+j` | `(-a, a)` | incorrect |
| None of the listed | fixed text | incorrect |

## Stage 4 — Reusable templates and constraints

Fixed: prompt sentence, one five-choice radio, field key selection, same source two-bullet elimination/stage sequence and fixed conclusion, source function labels. Variable: complete displayed formulas; source images reused only for original complete field geometry; all changed diagrams rendered. Conditional: component/direction nouns swap together when axes swap; positive/negative prose flips by sign(a)*sx or sign(a)*sy before swap. Formula slots are protected while prose is transformed, so function inputs/basis variables are not accidentally rewritten. All four choices are constructed from a selected complete bank; duplicate or unmatched fields reject the whole instance. No diagnosis or seed/domain metadata appears in learner text.

R maps each old component to its new basis with sx/sy signs and optionally swaps axes. Old input coordinates receive the same inverse map. Common scale a is a nonzero signed integer with |a|≤3; hard requires a=1. Defaults use a=±1 and signed isometries. Explicit parameters have identical guards. The authored hard bank is the correct field, flipped horizontal sign, flipped vertical sign, and exchanged coordinate dependencies, plus None of the listed. Every hard field has two nonzero linear components and distinct x/y dependencies.

Finite meaningful catalogs (common positive magnitude removed, signs/ratios/dependencies retained): easy 8, moderate 32, hard 8. No unlimited numeric-variety claim. Content identity includes actual prompt asset path, full solution, full bank, level/version; seed/order excluded. Mathematical identity excludes profiles/banks and common positive magnitude. Cross-profile i and rotated/scaled -5j dedup while content IDs remain separate.

## Source anomalies and repair denominators

q122296 lacks difficulty, correct designation, and solution in EDB. Captured original widget confirms exactly the same five choices and one radio assessment; widget-q122296.json preserves evidence. The plotted horizontal component is x and vertical is constant negative; only F=xi-j fits. Moderate is authored because it matches the one-variable observed workload. Complete bank reproduction counts 5/5; designation is inferred, not claimed matched. Worked solution is authored from the source common elimination/conclusion pattern.

q122629 lists F=-i-j but its solution prints F=-i+xj as an eliminated option. The horizontal-negative elimination is valid for the actual F, so generator minimally replaces that whole erroneous formula with the actual bank F. Raw evidence remains unedited. Bank and designation exact; raw solution prose 7/8, repaired solution 1/8, missing/authored 1. No algebraically wrong source teaching is copied into normal output.

Original prompt references are normalized to absolute captured local assets; exact sentence/layout and original PNG bytes match all9, but raw path strings are not claimed exact. All45 displayed choice strings reproduce exactly. Full mathematical comparison is separate from native radio-selection grading.
