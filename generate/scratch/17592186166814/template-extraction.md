# Template extraction

## Stage 1: individual observed descriptions

Every source asks which of three first-order ODEs are autonomous (easy), or **not** autonomous (moderate). The dependent variable is y and independent variable x. Derivatives use Leibniz or prime notation; the exact source spelling, including Unicode prime/function-application characters, remains intact. Functions include powers, exponentials, radicals, reciprocal powers, log and familiar trigonometric functions. Integers, zero, unit coefficients, a rational derivative coefficient, and pi occur. Each field is a Boolean checkbox, not an equation blank or a combined subset radio. No source answer value is an unexplained scalar distractor.

### q-95984 (database 17592186167441)

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}={e}^{y}$
- **II.** $\frac{\text{d}y}{\text{d}x}-3y=0$
- **III.** $2\frac{\text{d}y}{\text{d}x}-xy=\sqrt{x}$

Integer component slots: `{"n2": 2, "n3": 3}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-96387 (database 17592186167467)

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}={e}^{x}$
- **II.** ${y}^{′}-\frac{3}{y}=0$
- **III.** $\frac{1}{2}{y}^{′}-xy={e}^{x}$

Integer component slots: `{"n2": 2, "n3": 3}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-118863 (database 17592186233256)

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{'}-8{e}^{y}=2$
- **II.** $y{y}^{'}+3=\operatorname{cos}y$
- **III.** $x{y}^{'}-8={e}^{y}$

Integer component slots: `{"n2": 2, "n3": 3, "n8": 8}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-96702 (database 17592186234492)

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{\text{d}y}{\text{d}x}-x={e}^{y}$
- **II.** $y\frac{\text{d}y}{\text{d}x}-2=\sqrt{y}$
- **III.** $4\frac{\text{d}y}{\text{d}x}-\frac{x}{y}=5y$

Integer component slots: `{"n2": 2, "n4": 4, "n5": 5}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-96703 (database 17592186234493)

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** $x\frac{\text{d}y}{\text{d}x}-3{y}^{3}=2$
- **II.** $\frac{\text{d}y}{\text{d}x}-7{y}^{2}=\frac{1}{y}$
- **III.** $\frac{\text{d}y}{\text{d}x}=\operatorname{ln}y$

Integer component slots: `{"n2": 2, "n3": 3, "n7": 7}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-96705 (database 17592186234494)

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{y}\frac{\text{d}y}{\text{d}x}-3{y}^{3}=0$
- **II.** $\frac{\text{d}y}{\text{d}x}-2x=\operatorname{ln}⁡y$
- **III.** $5x\frac{\text{d}y}{\text{d}x}-\frac{y}{x}=0$

Integer component slots: `{"n2": 2, "n3": 3, "n5": 5}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-96712 (database 17592186234495)

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{'}=1-\sqrt{y}$
- **II.** ${y}^{'}-\operatorname{tan}y={e}^{2}$
- **III.** $x{y}^{'}-\frac{1}{y}=4$

Integer component slots: `{"n2": 2, "n4": 4}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-118858 (database 17592186253519)

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{2y}{y}^{′}+1=0$
- **II.** ${y}^{′}+\sqrt{xy}=2$
- **III.** ${y}^{′}=\operatorname{ln}⁡y$

Integer component slots: `{"n2": 2}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-118859 (database 17592186253520)

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}-3{x}^{2}=1$
- **II.** ${y}^{′}+6y={e}^{3y}$
- **III.** ${y}^{′}=\operatorname{ln}⁡(2{x}^{2}+1)$

Integer component slots: `{"n2": 2, "n3": 3, "n6": 6}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-118868 (database 17592186253522)

Which of the following are autonomous ordinary differential equations?

Select all that apply.

- **I.** ${x}^{2}{y}^{′}+6x{y}^{2}=8$
- **II.** ${y}^{′}+\frac{1}{x}=3{y}^{2}$
- **III.** ${y}^{′}=\operatorname{arctan}⁡({y}^{2}+2)$

Integer component slots: `{"n2": 2, "n3": 3, "n6": 6, "n8": 8}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-118869 (database 17592186253523)

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** $\frac{{y}^{′}}{y}+\frac{1}{\operatorname{arctan}⁡y+2\pi }=0$
- **II.** ${y}^{′}+{y}^{2}={x}^{2}$
- **III.** ${y}^{′}=\operatorname{sin}⁡x$

Integer component slots: `{"n2": 2}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-118870 (database 17592186253524)

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}={e}^{3-y}-2$
- **II.** $y{y}^{′}+\operatorname{cos}⁡y=1$
- **III.** ${y}^{′}=\operatorname{tan}⁡(x+y)$

Integer component slots: `{"n2": 2, "n3": 3}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-96711 (database 17592186360698)

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}=\operatorname{sin}⁡(\frac{y}{x})$
- **II.** ${y}^{′}-{x}^{2}y={e}^{x}$
- **III.** ${y}^{′}-\frac{3}{{y}^{2}}=1$

Integer component slots: `{"n2": 2, "n3": 3}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-96713 (database 17592186360699)

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${e}^{-y}{y}^{′}=-\sqrt{y}$
- **II.** ${y}^{′}-{y}^{3}=2{e}^{x}$
- **III.** ${y}^{′}-\frac{2}{{y}^{3}}=3\sqrt{y}$

Integer component slots: `{"n2": 2, "n3": 3}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

### q-96715 (database 17592186360700)

Which of the following are **not** autonomous ordinary differential equations?

Select all that apply.

- **I.** ${y}^{′}=\sqrt{{x}^{2}+\operatorname{sin}⁡y}$
- **II.** ${y}^{′}=\operatorname{sec}⁡\sqrt{2y}$
- **III.** ${y}^{′}-{y}^{3}=3\sqrt{y}$

Integer component slots: `{"n2": 2, "n3": 3}`. Units and zeros stay fixed.

| Field | Complete bank values | Correct source value | Mathematical response recipe |
|---|---|---|---|
| I | false; true | true | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| II | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |
| III | false; true | false | Isolate this displayed derivative, inspect explicit x dependence; invert predicate for **not** |

The first introductory definition and checking sentence are shared. Equation-specific prose distinguishes already-isolated versus rearranged equations. Original aligned row counts/order and final subset sentence are retained; see the complete raw worked solution in review.md and source.json.

## Stage 2: generalized mathematical pattern

Recognize whether a first-order ODE can be written D=f(y), rather than an expression that depends explicitly on x. y itself is a function of x; that implicit dependence does not make the equation nonautonomous. Rearrange by elementary addition/division on intervals where the expressions and derivative coefficients are defined. Do not integrate, solve for y(x), decide order, or assess IVPs. Compute each of three Boolean responses independently, then apply the positive/negative selection criterion.

## Stage 3: components and complete banks

Prompt components are the selection criterion, a fixed three-item I/II/III layout, and three complete equations. Source numeric component masks tie a source integer to its coefficient/exponent appearances in prompt and every worked stage. They are deliberately constrained integer substitutions, not numerical fitting. Every field retains both true and false choices; correct values are recomputed from actual displayed equations. The wrong option is the logical negation of the requested predicate. There is no inferred learner-facing distractor diagnosis. All 45 source banks use this fully defensible Boolean recipe. Source IDs, exact parameters, template and bank profile are listed individually in source-cases.json.

A structural exception is q-96705: x squared in Equation III’s derived denominator is the product of the two original x factors. This whole mathematical component remains x squared when Equation II’s unrelated coefficient 2 changes. It is masked before integer substitutions; changed-parameter stage checks enforce the product.

## Stage 4: reusable templates, constraints and authored scope

Observed templates retain the complete prompt/prose mask, every aligned stage and row omission, final subset sentence, answer field layouts, complete banks, and source key presence. Raw replay regenerates source math from component slots and recomputes Boolean designations; no API branch returns a copied source payload or uses an answer lookup. Component slots are integers 2..8, narrowed to 2..3 when used as variable powers in the displayed prompt. Explicit inputs obey the same guards. These finite coefficient/exponent substitutions are notation/arithmetic variants; they are not counted as new categorical skills. Normal observed_repaired differs only for q-96702.

Authored easy has 8 semantic items: power, exponential, square root or logarithm, each with an x or y argument. Select three distinct items with mixed x/y arguments, in either selection criterion. All are already isolated, with exactly three direct dependence checks; powers are 2 or 3. The count is 2 × (C(8,3) − 2C(4,3)) = 96, excluding numeric and letter aliases.

Authored moderate has 10 semantic items: power, exponential, square root, sine or cosine, each paired with an x or y argument/coefficient. Every equation has coefficient-times-derivative plus b equal to a times the function. Each of three checks requires one subtraction and one division, then dependence recognition. The count is 2 × (C(10,3) − 2C(5,3)) = 200.

Authored hard has 8 semantic items: power, exponential, square root or sine of y, paired with matching or unmatched affine x factors. Every equation has (x+a)D=(x+d)(F(y)+b), with d=a for autonomous and d=c for nonautonomous. Each of the three checks requires division and recognition of a whole common factor; the display supplies the factors, so no expansion/factoring method is introduced. Reduced expressions are computed exactly. Autonomous hard equations show the actual cancellation row; unmatched factors retain their quotient and proceed directly to the formal dependency row, avoiding a redundant CAS row. The count is 96 by the same mixed-category combinatorics as easy. Hard is a missing-level design claim, not a recovered MA label.

For all authored levels: a∈{2,3,4}, b∈{1,2,3,4}, n∈{2,3}, c∈{5,6,7}; c differs strictly from a. Every catalog item needed for a level is nonzero. No negative coefficients, accidental all-autonomous/all-nonautonomous sets, higher-order derivatives, solving, or extra algebra branches are allowed. Easy is isolated, moderate has an additive term and coefficient division in every item, hard has explicit common independent-variable factors in every item. These demands are mutually separated even when their reduced RHS expressions can be equivalent. Within each level catalog items are unordered same-workload alternatives, not a progression.

### Curriculum anchor

The owning topic is Introduction to Differential Equations (MA 3215). The route was followed via activity/first-step then step/next: Introduction → Identifying the Order of an ODE → Autonomous Ordinary Differential Equations → this KP → First-Order Initial Value Problems → Initial Value Problems and Initial Conditions. The autonomous tutorial defines y′=f(y) and contrasts it with (y+2)/x². Canonical e-8460 uses direct recognition and division by x. Source easy equations already include y or exponential derivative prefactors; moderate sources include reciprocal coefficients and compound function arguments. Thus elementary coefficient isolation and hard common-factor recognition are anchored to the definition and existing algebra, while solving ODEs and IVPs remain outside this KP. The capture has no separate explicit prerequisite attribute; no prerequisite list is invented.

### Source error and supported repair

q-96702 Equation II is yD−2=√y. Its original solution prints D=(√y+2)/2, twice. Independently dividing the actual printed equation gives D=(√y+2)/y, on the domain y>0 for the isolated equation. Both expressions have no explicit x, so the checkbox designation is unaffected. Public observed_raw preserves the wrong row and where-f expression, marks evidence_only=true and eligible_for_learning=false, and matches the original wording exactly. Public observed_repaired changes the two denominator components from the tied constant slot to y. Raw-exact fidelity is 15/15 solutions; original mathematical correctness is 14/15; supported repair is 1/1. No repair changes an answer bank, source difficulty, or correct designation.

### Identity, independent verification and stop boundary

Content identity includes actual prompt, fixed solution, complete displayed Boolean banks/correct values, version and level; seeds and choice order do not affect it. Mathematical fingerprints exclude numerical aliases, layout, bank profile and order of independent checks; catalogs report only semantic structure and criterion. Raw/repaired profiles share the assessed-task fingerprint. Source interpretation remains labeled separately from authored defaults. Displayed equations and every calculation/where-f row are independently parsed into exact SymPy expressions. Formatting, UUID ownership, key presence, source full strings/stage sequence, explicit guards, complete categorical enumeration and actual native checkbox grading are failure-enforced. Runtime metadata records Python and SymPy versions; native engine hashes appear in validation.json. Plot rating none; work stops after step 7.
