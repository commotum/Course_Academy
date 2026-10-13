# Template extraction

## Stage 1 — describe each source specifically

Every item below has observed moderate difficulty; the p and q parameter keys are internal vector slots, while the learner uses the source names. Values such as sqrt(2) or sqrt(3) occur only in a product with zero. The answer shape is the exact scalar x; the nonzero receiving vector condition is independently verified at that answer.

| Source | Names / layout | Vector parameters | Field | Reduced-order / solving structure |
|---|---|---|---|---|
| q-236734 (17592186106213) | p,q / angle | `['-1', '1', '2']` ; `['4', 'x', '1']` | radio `selection` | x term first, direct solve, dot=0 opening, unevaluated component products |
| q-236735 (17592186106214) | p,q / column | `['6', '1', '4']` ; `['x', '4', '-4']` | radio `selection` | x term first, separate isolation, dot=0 opening, unevaluated component products |
| q-237014 (17592186290486) | p,q / column | `['-2', '0', '5']` ; `['15', 'sqrt(2)', 'x']` | radio `selection` | x term first, separate isolation, dot=0 opening, unevaluated component products |
| q-237015 (17592186290487) | p,q / column | `['5', 'x', '2']` ; `['4', '-2', '-3']` | radio `selection` | constant first, separate isolation, dot=0 opening, unevaluated component products |
| q-237016 (17592186290488) | a,b / column | `['0', '-2', '1']` ; `['-2', 'x', '2']` | radio `selection` | constant first, separate isolation, dot=0 opening, unevaluated component products |
| q-237017 (17592186290489) | p,q / basis | `['1', '-3', '0']` ; `['x', '2', '1']` | radio `selection` | x term first, direct solve, dot=0 opening, unevaluated component products |
| q-237018 (17592186290490) | a,b / basis | `['5', '-4', '3']` ; `['-7', 'x', '1']` | radio `selection` | x term first, separate isolation, dot=0 opening, unevaluated component products |
| q-237020 (17592186290491) | p,q / angle | `['2', '0', '3']` ; `['3', '0', 'x']` | radio `selection` | x term first, separate isolation, dot=0 opening, unevaluated component products |
| q-237021 (17592186290492) | c,d / angle | `['-3', 'sqrt(3)', '1']` ; `['x', '0', '-12']` | radio `selection` | x term first, separate isolation, dot=0 opening, unevaluated component products |
| q-237022 (17592186290493) | p,q / angle | `['3', '5', 'x']` ; `['-3', '1', '2']` | radio `selection` | x term first, separate isolation, dot=0 opening, unevaluated component products |
| q-275253 (17592186292829) | p,q / angle | `['-1', '2', '1']` ; `['2', 'x', '0']` | blank `field-1` | constant first, separate isolation, dot=0 opening, unevaluated component products |
| q-275256 (17592186292830) | a,b / column | `['-1', '2', '4']` ; `['0', 'x', '2']` | blank `field-1` | x term first, separate isolation, dot=0 opening, unevaluated component products |
| q-319150 (17592186299726) | p,q / angle | `['3', '-1', '2']` ; `['x', '1', '1']` | blank `field-1` | x term first, separate isolation, dot=0 opening, unevaluated component products |
| q-319171 (17592186299731) | p,q / angle | `['4', '1', '-2']` ; `['1', 'x', '3']` | blank `field-1` | x term first, direct solve, dot=0 opening, unevaluated component products |
| q-319172 (17592186299732) | p,q / angle | `['-2', '3', '4']` ; `['1', '2', 'x']` | blank `field-1` | x term first, separate isolation, dot=0 opening, evaluated first products |
| q-319252 (17592186299736) | p,q / basis | `['2', '-3', '1']` ; `['x', '4', '0']` | blank `field-1` | x term first, separate isolation, dot=0 opening, unevaluated component products |
| q-319253 (17592186299737) | p,q / basis | `['-4', '2', '-3']` ; `['5', 'x', '0']` | blank `field-1` | constant first, separate isolation, dot=0 opening, unevaluated component products |
| q-319254 (17592186299738) | p,q / basis | `['3', '2', '-1']` ; `['-2', 'x', '0']` | blank `field-1` | constant first, separate isolation, dot=0 opening, unevaluated component products |
| q-319255 (17592186299739) | a,b / column | `['3', '-2', '1']` ; `['x', '1', '2']` | blank `field-1` | x term first, direct solve, dot=0 opening, unevaluated component products |
| q-319256 (17592186299740) | a,b / column | `['-2', '5', '1']` ; `['3', 'x', '-4']` | blank `field-1` | x term first, separate isolation, reduced-equation opening, unevaluated component products |
| q-237019 (17592186379342) | p,q / basis | `['1', '2', 'x']` ; `['3', '6', '-3']` | radio `selection` | constant first, separate isolation, dot=0 opening, unevaluated component products |
| q-319257 (17592186379369) | a,b / column | `['4', '-1', '3']` ; `['2', '0', 'x']` | blank `field-1` | x term first, separate isolation, reduced-equation opening, unevaluated component products |

## Stage 2 — shared mathematical pattern

For nonzero vectors the zero scalar projection gives perpendicularity and therefore dot product zero. Multiply corresponding components, collect Ax+B, and solve x=-B/A. The first worked block retains the formal component sum, the actual component substitution (or the one observed pre-evaluated product row), and the collected expression. The second block retains the source's dot=0 row presence, isolation-row presence, and final x row. Shared prose is stored as masks; the solution is fixed and independent of the selected wrong answer.

## Stage 3 — map every component and every bank

`recipes.json` records the full source masks, formal rows, parameters, field keys/types, per-bank exact values, original correct value, and opaque ratios in original choice order. `source-cases.json` maps all 22 sources to their public API recipe and profile. No choice is discarded. A complete observed radio bank is represented by v_j=r_j x_correct, with each historical ratio r_j explicitly listed below. This is a parameterized preservation of historical scalar values, **not** an inferred misconception or an authored default recipe. Its error interpretation remains unresolved. Replay labels mark it evidence-only even when all mathematical values and native choices pass.

| Source profile | Original complete bank | Original correct | Complete value pattern |
|---|---|---|---|
| `observed:q-236734` | `['0', '2', '1', '-3', '-1']` | `2` | `[0 * solved_x, 1 * solved_x, 1/2 * solved_x, -3/2 * solved_x, -1/2 * solved_x]` |
| `observed:q-236735` | `['-2', '0', '2', '3', '-1']` | `2` | `[-1 * solved_x, 0 * solved_x, 1 * solved_x, 3/2 * solved_x, -1/2 * solved_x]` |
| `observed:q-237014` | `['3', '-2', '6', '2', '5']` | `6` | `[1/2 * solved_x, -1/3 * solved_x, 1 * solved_x, 1/3 * solved_x, 5/6 * solved_x]` |
| `observed:q-237015` | `['7', '6', '-7', '-6', '3']` | `7` | `[1 * solved_x, 6/7 * solved_x, -1 * solved_x, -6/7 * solved_x, 3/7 * solved_x]` |
| `observed:q-237016` | `['0', '2', '1', '-2', '-1']` | `1` | `[0 * solved_x, 2 * solved_x, 1 * solved_x, -2 * solved_x, -1 * solved_x]` |
| `observed:q-237017` | `['-3', '-2', '3', '1', '6']` | `6` | `[-1/2 * solved_x, -1/3 * solved_x, 1/2 * solved_x, 1/6 * solved_x, 1 * solved_x]` |
| `observed:q-237018` | `['-8', '-4', '2', '-6', '4']` | `-8` | `[1 * solved_x, 1/2 * solved_x, -1/4 * solved_x, 3/4 * solved_x, -1/2 * solved_x]` |
| `observed:q-237020` | `['-2', '3', '-3', '1', '-1']` | `-2` | `[1 * solved_x, -3/2 * solved_x, 3/2 * solved_x, -1/2 * solved_x, 1/2 * solved_x]` |
| `observed:q-237021` | `['-4', '2', '-2', '6', '1']` | `-4` | `[1 * solved_x, -1/2 * solved_x, 1/2 * solved_x, -3/2 * solved_x, -1/4 * solved_x]` |
| `observed:q-237022` | `['4', '-3', '2', '-1', '-2']` | `2` | `[2 * solved_x, -3/2 * solved_x, 1 * solved_x, -1/2 * solved_x, -1 * solved_x]` |
| `observed:q-275253` | `['1']` | `1` | `[solved_x]` |
| `observed:q-275256` | `['-4']` | `-4` | `[solved_x]` |
| `observed:q-319150` | `['-1/3']` | `-1/3` | `[solved_x]` |
| `observed:q-319171` | `['2']` | `2` | `[solved_x]` |
| `observed:q-319172` | `['-1']` | `-1` | `[solved_x]` |
| `observed:q-319252` | `['6']` | `6` | `[solved_x]` |
| `observed:q-319253` | `['10']` | `10` | `[solved_x]` |
| `observed:q-319254` | `['3']` | `3` | `[solved_x]` |
| `observed:q-319255` | `['0']` | `0` | `[solved_x]` |
| `observed:q-319256` | `['2']` | `2` | `[solved_x]` |
| `observed:q-237019` | `['10', '3', '-3', '-1', '5']` | `5` | `[2 * solved_x, 3/5 * solved_x, -3/5 * solved_x, -1/5 * solved_x, 1 * solved_x]` |
| `observed:q-319257` | `['-8/3']` | `-8/3` | `[solved_x]` |

Normal radio banks are selected from the eligible source mask before sampling any coordinates. They contain exactly five entries; one collision rejects the entire instance. The known products are T1,T2; the linear coefficient is A; their sum is B; r=-B/A.

| Complete authored profile | Values / operations |
|---|---|
| two-products | [r, -r, -T1/A, -T2/A, -B]: correct, wrong sign, omit either known product, omit coefficient division |
| two-products-unit | [r, -r, -T1/A, -T2/A, (T1-T2)/A]: replace duplicate no-division error by reversing first known product sign |
| one-product | [r, -r, -B, u, v]: known product uv; omit division or use either known component alone |
| one-product-unit | [r, -r, u, v, -(u+v)/A]: replace duplicate no-division error by adding known components instead of multiplying |
| hard | [r, -r, -B/c, -B/a, -B]: omit either of two x contributions, wrong sign, or omit division |
| blank | [r] exact scalar fragment, no wrong choices |

These are explicit authored operations from the printed dot method. Their labels stay outside learner text. No random offset values or post-parameter pool replacements are used. The bank type and source mask are selected first; eligibility and all five mathematical values are checked together.

## Stage 4 — reusable templates and constraints

A source recipe stores `@V1@` and `@V2@` as complete vector-component slots in the prompt, `@DOTBLOCK@` and `@SOLVEBLOCK@` as complete aligned blocks in the solution. It never blindly substitutes a small number or letter across prose. The vector renderer retains angle tuples, aligned columns, or suppressed unit/zero basis coefficients. The numeric product renderer groups signed factors. The collected expression retains the observed term order; a conditional signed sum never prints +− or −−. Each exact replay is produced through `generate`, not a copied payload branch or private helper.

The observed original parameters reproduce every prompt and every worked-solution byte. Each source is additionally exercised with two changed vector parameter sets through the same public observed profile, plus two normal generated variants with its method-derived bank. Changed source values keep the same category of unit coefficient and zero constant so stage masks do not add/drop rows. Source source values are fixed provenance; normal sample bounds and hard/easy scope are authored policy described in classification. Normal output repairs q-275256's name inconsistency; raw-exact and repaired teaching prose are counted separately.

The mathematical fingerprint records the normalized three contribution expressions and their number of x contributions; vector notation, variable names, choice order, source/profile alias, and common equation scaling do not inflate variety. Numeric inputs in zero products have no contribution. Easy has one fingerprint because both supplied-information forms reduce to the same categorical fact. Content identity includes actual level, prompt, complete fixed solution, full displayed bank, field type and key. Changing a seed or option order alone does not change it; changing a displayed bank does.
