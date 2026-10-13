# Template extraction

## 1. Specific source descriptions

The following records preserve each given-vector tuple, variable names, response shape and norm row sequence. Cross products use a 3×3 formal determinant, all three 2×2 minors, the six ordered coordinate products, evaluated basis-vector components, and an ordered coordinate tuple. The source minus sign on the j minor is retained before reduction. `ab`/`ba` below describes whether the subtracted product writes a-coordinate first or b-coordinate first; it is notation, not a distinct skill.

- **q-19983:** a=[1, 3, 2], b=[4, 1, -2]; products `ba`; cross [-8, 10, -11]; norm squared 285; area sqrt(285)/2. Template `triangle_radio_radical`; one radio scalar field. Norm layout `radical`.
- **q-20003:** a=[-2, -3, -1], b=[1, 2, 1]; products `ab`; cross [-1, 1, -1]; norm squared 3; area sqrt(3). Template `parallelogram_radio_unrated`; one radio scalar field. Norm layout `radical`.
- **q-18580:** r=[1, -2, 3], t=[0, 1, -2]; products `ab`; cross [1, 2, 1]; norm squared 6; area sqrt(6)/2. Template `triangle_radio_radical`; one radio scalar field. Norm layout `radical`.
- **q-19981:** u=[2, 1, -1], v=[1, 2, 0]; products `ba`; cross [2, -1, 3]; norm squared 14; area sqrt(14). Template `parallelogram_radio_radical`; one radio scalar field. Norm layout `radical`.
- **q-19997:** f=[1, 1, -2], g=[3, 2, 1]; products `ba`; cross [5, -7, -1]; norm squared 75; area 5*sqrt(3). Template `parallelogram_radio_simplified`; one radio scalar field. Norm layout `simplified`.
- **q-20004:** h=[2, 0, 3], l=[4, 1, 3]; products `ba`; cross [-3, 6, 2]; norm squared 49; area 7. Template `parallelogram_radio_simplified`; one radio scalar field. Norm layout `simplified`.
- **q-275220:** a=[-4, -2, 1], b=[0, -2, -1]; products `ba`; cross [4, -4, 8]; norm squared 96; area 4*sqrt(6). Template `parallelogram_blank_direct`; one blank scalar field. Norm layout `direct`.
- **q-275222:** a=[-2, -1, 0], b=[-4, 2, -2]; products `ba`; cross [2, -4, -8]; norm squared 84; area sqrt(21). Template `triangle_blank_direct`; one blank scalar field. Norm layout `direct`.
- **q-316345:** a=[-3, 5, 0], b=[4, -1, 2]; products `ab`; cross [10, 6, -17]; norm squared 425; area 5*sqrt(17). Template `parallelogram_blank_expanded`; one blank scalar field. Norm layout `expanded`.
- **q-316350:** a=[1, 0, 0], b=[0, 3, 4]; products `ab`; cross [0, -4, 3]; norm squared 25; area 5. Template `parallelogram_blank_expanded`; one blank scalar field. Norm layout `expanded`.
- **q-316355:** p=[0, 5, -1], q=[6, 0, 1]; products `ab`; cross [5, -6, -30]; norm squared 961; area 31/2. Template `triangle_blank_expanded`; one blank scalar field. Norm layout `expanded`.

## 2. Generalized family pattern

Compute the given vectors’ determinant cross product, then its Euclidean magnitude. Return that magnitude for the observed parallelogram prompts, or half that magnitude for triangle prompts. All given-vector slots feed every minor, multiplication, evaluated coordinate, norm square, optional sum and simplification, and triangle halving stage. Shared source prose stays fixed and solutions are independent of which error option is selected.

## 3. Complete component and choice map

For each observed radio bank, the recipe below maps every original displayed option one-to-one. Let a=s a₀ and b=t b₀ for the listed source baseline, where s,t are nonzero integers with |s|,|t|≤3. Each displayed scalar is `abs(s*t) * coefficient * sqrt(radicand)`. This is an explicit observed radical-pattern scaling operation, not a recovered error diagnosis. Outside these scaling rays the original scalar options underdetermine defensible parameterized mistakes, so profiles reject inputs rather than generalize by polynomial fitting or fixed norm offsets. All five patterns remain together as a complete bank. They are never the default bank.

| Source profile | Original displayed value | Parameterized observed pattern | Original designation |
|---|---|---|---|
| q-19983 | `$\frac{\sqrt{273}}{2}$` | `abs(s*t)*1/2*sqrt(273)` | wrong |
| q-19983 | `$\frac{\sqrt{285}}{2}$` | `abs(s*t)*1/2*sqrt(285)` | correct |
| q-19983 | `$\frac{\sqrt{825}}{2}$` | `abs(s*t)*1/2*sqrt(825)` | wrong |
| q-19983 | `$\sqrt{177}$` | `abs(s*t)*1/1*sqrt(177)` | wrong |
| q-19983 | `$\frac{\sqrt{582}}{2}$` | `abs(s*t)*1/2*sqrt(582)` | wrong |
| q-20003 | `$\frac{3\sqrt{3}}{2}$` | `abs(s*t)*3/2*sqrt(3)` | missing; independently inferred wrong |
| q-20003 | `$\frac{\sqrt{3}}{2}$` | `abs(s*t)*1/2*sqrt(3)` | missing; independently inferred wrong |
| q-20003 | `$\frac{\sqrt{2}}{2}$` | `abs(s*t)*1/2*sqrt(2)` | missing; independently inferred wrong |
| q-20003 | `$\frac{3\sqrt{2}}{2}$` | `abs(s*t)*3/2*sqrt(2)` | missing; independently inferred wrong |
| q-20003 | `$\sqrt{3}$` | `abs(s*t)*1/1*sqrt(3)` | missing; independently inferred correct |
| q-18580 | `$\sqrt{6}$` | `abs(s*t)*1/1*sqrt(6)` | wrong |
| q-18580 | `$\frac{\sqrt{3}}{2}$` | `abs(s*t)*1/2*sqrt(3)` | wrong |
| q-18580 | `$\frac{\sqrt{6}}{2}$` | `abs(s*t)*1/2*sqrt(6)` | correct |
| q-18580 | `$2\sqrt{3}$` | `abs(s*t)*2/1*sqrt(3)` | wrong |
| q-18580 | `$2\sqrt{6}$` | `abs(s*t)*2/1*sqrt(6)` | wrong |
| q-19981 | `$\frac{\sqrt{14}}{2}$` | `abs(s*t)*1/2*sqrt(14)` | wrong |
| q-19981 | `$\frac{\sqrt{14}}{3}$` | `abs(s*t)*1/3*sqrt(14)` | wrong |
| q-19981 | `$\sqrt{14}$` | `abs(s*t)*1/1*sqrt(14)` | correct |
| q-19981 | `$\sqrt{7}$` | `abs(s*t)*1/1*sqrt(7)` | wrong |
| q-19981 | `$\frac{\sqrt{7}}{2}$` | `abs(s*t)*1/2*sqrt(7)` | wrong |
| q-19997 | `$3\sqrt{3}$` | `abs(s*t)*3/1*sqrt(3)` | wrong |
| q-19997 | `$3\sqrt{5}$` | `abs(s*t)*3/1*sqrt(5)` | wrong |
| q-19997 | `$\frac{2\sqrt{5}}{3}$` | `abs(s*t)*2/3*sqrt(5)` | wrong |
| q-19997 | `$\frac{5\sqrt{3}}{2}$` | `abs(s*t)*5/2*sqrt(3)` | wrong |
| q-19997 | `$5\sqrt{3}$` | `abs(s*t)*5/1*sqrt(3)` | correct |
| q-20004 | `$\frac{\sqrt{3}}{2}$` | `abs(s*t)*1/2*sqrt(3)` | wrong |
| q-20004 | `$\frac{\sqrt{2}}{2}$` | `abs(s*t)*1/2*sqrt(2)` | wrong |
| q-20004 | `$\frac{7}{2}$` | `abs(s*t)*7/2*sqrt(1)` | wrong |
| q-20004 | `$5$` | `abs(s*t)*5/1*sqrt(1)` | wrong |
| q-20004 | `$7$` | `abs(s*t)*7/1*sqrt(1)` | correct |

q-275220 blank `field-1`: required scalar fragment `4\sqrt{6}`; formula norm(c).

q-275222 blank `field-1`: required scalar fragment `\sqrt{21}`; formula norm(c)/2.

q-316345 blank `field-1`: required scalar fragment `5\sqrt{17}`; formula norm(c).

q-316350 blank `field-1`: required scalar fragment `5`; formula norm(c).

q-316355 blank `field-1`: required scalar fragment `\frac{31}{2}`; formula norm(c)/2.

The 6 complete radio banks contain 30 displayed values; 5 blank fields add 5 required fragments. There are 10 available designations and one separately inferred key. Source fidelity compares all values under exact equivalence; it does not compare only answers or claim original author intent.

## 4. Reusable Markdown/value construction

Fixed: source opening, parallelogram-magnitude paragraph, triangle-half paragraph when applicable, field types/counts, determinant/minor/component/magnitude sequence. Variable: two complete 3D vectors and their variable labels, all coordinate operands, all cross components, squared norm and area. Conditional: unit coefficients are omitted in basis-vector notation; negative multiplicands/squares are parenthesized; the expanded source shows its zero i component; actual radical simplification adds a final evaluated row; triangle halving shows an unreduced numerator before cancellation when needed. No scalar substring replacement across vectors/prose is used.

Norm layouts: radical = substituted squares → sqrt(N); simplified = substituted squares → sqrt(N) → simplified magnitude; direct = substituted squares → simplified magnitude; expanded = substituted squares → individually evaluated square sum → sqrt(N) → simplified magnitude. Default radical templates require N>1 squarefree; other templates require actual simplification. The original source-parameter strings reproduce all ten available worked solutions byte-for-byte. q-20003 gets an authored full formal solution through the same nodes.

Default complete authored radio bank: correct norm factor, incorrect area factor (half for parallelogram or omitted half for triangle), then norms with exactly the x², y², or z² cross-component contribution omitted, retaining the requested area factor. These are actual operation recipes, not numeric perturbations. Select the whole profile first; reject the whole sampled instance if any scalar is nonpositive or any pair is equivalent. No member is replaced using a first-valid pool. This rules out zero cross components and equal squared-component omissions in radio defaults. No learner-facing diagnosis is appended.

All normal easy inputs satisfy integer |coordinate|≤5, max |cross component|≤30 and norm squared≤1800; moderate has |coordinate|≤6, max |cross component|≤45 and norm squared≤4000. Hard coordinates are also bounded by 6. These guard evaluated arithmetic as well as the input presentation. Source-pattern profiles explicitly permit only |s|,|t|≤3 scaling rays and are evidence replay rather than default level policy. Explicit invalid inputs reject without silent resampling. Authored hard additionally enforces its primitive/dense/reduced-workload requirements on explicit calls. Parallel vectors always reject. Parameter fingerprints use sign-canonical unordered vector pairs plus requested shape, excluding names, template/field aliases, answer banks and profile. Scaling changes actual given-vector areas and remains substantive. Content identity hashes version, actual prompt, full fixed solution, field type and sorted complete displayed bank, so shuffled order/seed/profile alias cannot generate new IDs.

The tested normal bank’s substantive variety is reported in validation.json after deduplicating aliases. Authored hard has two response-layout templates at one level, not a progression. Plot rating is none; no prompt/option/solution contains plots.
