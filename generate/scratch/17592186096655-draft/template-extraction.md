# Template extraction

## 1. Specific originals

`template-extraction.json` contains every original prompt, ordered solution row, original parameter, field contract, exact option and correct designation. `source-cases.json` covers all12 originals. `independent-inventory.json` uses the standard questions wrapper and retains the complete3 non-MA records with their independent role and relationship. These records are not used as observed difficulty evidence.

q-13733 asks for ∫3e^(-6x)dx; it has five complete primitive choices, but omits difficulty, key and solution. q-113833 has reciprocal slope1/2 and offset-1; its distractors separately omit the reciprocal, change its sign, multiply by the slope or change the exponent slope to1. q-13732 scales e^(3x) by5; its complete bank includes coefficient inversion, omitted division, coefficient/slope substitution and replacing the exponent's slope by the outside coefficient.

q-30923 has a=k=1/3 with bounds0,3, transforming to0,1. q-13775 has outside4, slope6 and upper ln2, with nine formal rows including exponent/log rewrites and explicit multiplication. q-13786 has outside5, slope-4, upper ln3 and ten rows including both reciprocal-power and evaluated-rational endpoints. q-30922 has outside-5, slope-2 and upper ln4, keeping its own nine-row chain. q-349595/596 are blank analogues with slopes5/3, scales4/5, upper ln2/ln4 and distinct final multiplication/collection rows. q-349601 uses a=k=4, offset1, limits0,2; it omits the redundant evaluated e^1 row and has six rows. q-362689 has outside12, slope-4 and limits-1,0, transforming to4,0, with seven rows. q-51160 first combines e^z e^z into e^(2z), then preserves its five-row substitution chain and arbitrary C.

## 2. Shared pattern and purpose

For a nonzero constant linear slope, define u=kx+b, compute du/dx=k and dx=du/k, substitute, extract a/k, integrate e^u, and back-substitute or evaluate the transformed limits. Product preprocessing and logarithmic endpoint arithmetic are retained only in their observed families. A source's field layout, five-option contract or supplied blank fragment stays fixed.

## 3. Components and complete banks

The exact component inventory is machine-readable in `template-extraction.json`. Every original option is mapped one-to-one to its field, designation and exact expression. Raw bank recipes apply the source-independent-coordinate substitution v→v-r to the **entire primitive option**. Scalar options remain scalar, because translating both independent-coordinate bounds leaves their definite values fixed. This is an explicit conservative source-mask generalization, not a claim to infer an opaque distractor's intention. There is no answer lookup branch at original parameters: r=0 is the identity of the same recipe used at every permitted r.

The normal complete banks are chosen before parameters. Fractional-slope, scaled, negative-slope and product families retain the source-shaped primitive mistakes; negative log banks whose scalar mistakes are underdetermined instead get a separately labeled authored bank consisting of omitted slope, reversed subtraction, omitted lower endpoint and endpoint addition. Other source banks are retained in raw evidence. Every pair, including wrong/wrong pairs, is checked for equivalence. Indefinite primitives are compared modulo an arbitrary constant, so adding1 does not manufacture a wrong answer. Normal blanks use the complete exact scalar. Wrong scalars0,1 and answer+1 are measured through the native grader. No correct-plus1 probe is used for indefinite families.

## 4. Reusable masks, slots and constraints

Each original source string is a fixed mask with mathematical variable, independent-coordinate bound and x/z-table endpoint slots. `shift_string` protects commands, differential labels and table headings before filling whole coordinate components. It translates only bounds of integrals whose operand still uses x/z; u limits and scalar endpoints remain fixed. Original prose, primitive conventions, complete banks, row order and attribute presence remain exact at r=0. Source masks are sampled uniformly over shift -4..4. Option order is seeded but excluded from identity.

Expanded affine masks add signed integer outside scale, integer/reciprocal slope and offset, with the bounded domain in classification.md. Easy has four rows. Definite masks retain extraction, substitution, factor pull-out, primitive operator, exponent substitution, **individually scaled upper and lower primitive components**, and collection. Validation reads every formal operand, u/du relation, supplied/transformed bound, component and bank from actual generated learner strings. It compares source-specific stage signatures and rejects a mutation deleting an integral stage while preserving mathematical equality and row count. Question identity includes actual prompt, fixed solution, complete bank, correct value, field contract and difficulty; task identity includes actual canonical integrand and bounds, excluding bank/profile/seed and coefficient aliases.

### Recorded source anomalies and minimal normal repairs

- q-13733 has no difficulty, correct designation or solution. Raw replay omits those exact attributes. Normal easy routing, key and canonical four-row solution are explicitly authored/inferred from independent differentiation.
- q-13775 and q-30922 use du in the initial extracted-factor integral while retaining the x operand and x limits. Raw preserves it. Normal changes that differential to dx, retaining the full subsequent chain.
- q-51160 has two mixed z-operand/du intermediate rows and nested aligned environments. Raw preserves both. Normal explicitly substitutes z-r=u/2 inside those two operands, retaining both operations and all subsequent rows. Nested aligned structure is balanced, and no unnecessary presentation repair is claimed.
- “Do not round the answer” is retained in raw blanks. Normal uses “Give an exact answer.” Native equivalent-form restrictions are measured separately.
- Decoded source bytes were inspected: the alleged doubled TeX slashes were serialization escaping. The first q-13733 fraction begins bytes92,102,114,97 and has zero adjacent slash pairs. No slash repair is claimed.

Raw defects and missing attributes do not enter normal correctness denominators. Normal repairs, inferred completion and authored banks are all separate from exact replay counts. No source teaching error is silently used to claim fidelity in served output.
