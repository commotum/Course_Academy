# Template extraction: four stages

## 1. Specific source descriptions

* q-1927: unrated legacy radio; ln7 is first, positive integer coefficient 7 second; asks f′(x); five whole equations. No worked solution/correct ref. Coefficient equals log argument, but the generalized recipe retains separate slots.
* q-51208: unrated legacy radio; ln2 first, −4e^x second; five whole equations, including 2−4e^x rather than ln2−4e^x. No solution/ref.
* q-101587: easy radio; 5e^x+1; slope at 0; scalar five-choice bank. Four formal derivative rows, then restriction at x=0, 5e^0, 5·1, 5.
* q-101590: easy radio; 2e^x−ln11; slope at 1; scalar bank. Derivative stages preserve the signed constant as D(−ln11). Evaluation has restriction, 2e^1, 2e; no redundant 2·e row.
* q-340056: easy blank; 6e^x+ln8; explicitly supplied f′(x)= followed on a new line by `{{field-1}}`. Expected fragment is 6e^x, not a whole equation. Two equivalent source answer spellings. Four derivative rows, double aligned wrapper.
* q-340067: easy inline blank; 9e^x+ln4; supplied slope at ln2. Expected scalar 18. Four derivative rows, then restriction, 9e^{ln2}, 9·2, 18.
* q-71053: easy full-equation radio; 10−2e^x; five whole equations. Constant-first distribution D(10)+D(−2e^x), reduction 0−2D(e^x), final −2e^x, double aligned wrapper.

No variable names, power, exponential base, x-dependent coefficient, number of x-dependent summands, or question type are broadened. Displayed variables remain x and f(x).

## 2. Generalized shared pattern and purpose

Given f(x)=ae^x+c or c+ae^x, find f′(x), optionally evaluate it at the supplied point to get a tangent slope. Recognize d(e^x)/dx=e^x, differentiate c to zero, keep coefficient a, and apply addition/constant multiple rules. A blank either supplies f′(x)= and expects just its RHS, or expects the slope scalar. Radio equations include their whole LHS; slope radios contain only scalars.

## 3. Component and complete-bank map

Here a is the signed exponential coefficient, b is the signed displayed integer constant or log argument slot, C=sign(b)ln|b| for log constants and C=b for integer constants; t is the supplied point. Each row below lists **every source option**, together with the parameterized recipe. These are complete profiles selected before sampling, never a first-valid subset of a pooled bank.

| Source/profile | Original options in capture order | Parameterized full values in that order | Correct |
|---|---|---|---|
| q-1927 / legacy_log_scale | ln7·e^x; 7e^x+ln7; 0; ln7; 7e^x | lnabs(b)·e^x; ae^x+C; 0; C; ae^x | Last, inferred |
| q-51208 / legacy_log_base | −4e^x+ln2; ln2; 0; 2−4e^x; −4e^x | ae^x+C; C; 0; abs(b)+ae^x; ae^x | Last, inferred |
| q-101587 / slope_zero | ln5; 1; 0; 5; −1 | lnabs(a); b; 0; ae^0; −b | Fourth |
| q-101590 / slope_one | 0; 1; 2e; e²; 2 | 0; 1; ae^1; e^a; a | Third |
| q-340056 / blank_alias | 6{e}^x; 6e^x | ae^x in both preserved spellings | First source canonical, second equivalent accepted alias |
| q-340067 / slope_blank | 18 | ae^{ln2}=2a | Sole choice |
| q-71053 / negative_unit | −e^x; −2e^x; 10−2e^x; 10−e^x; 0 | −e^x; ae^x; b+ae^x; b−e^x; 0 | Second |

Every equation-radio option retains f′(x)=. Scalar/fragment options have no math delimiters in stored values. Original comparison covers all 28 answer values (including both aliases), 20 wrong radio choices, seven complete banks, and five available designations. Two missing designations are derived independently, separately counted.

Interpretation limits: `ln|a|`, `b`, `−b` at (a,b)=(5,1), and `e^a` at a=2 are underdetermined scalar evidence. They are explicit replay formulas, not claims that the original author intended those wrong operations. The q-51208 `|b|+ae^x` option also does not recover the authoring intent. These profiles remain available through the public generate API and are exercised at changed parameters. Eligible source profile constraints keep t=0/b=1 for slope_zero, t=1 for slope_one, and negative a/nonlog constant for negative_unit; ambiguity rejects the whole instance.

Normal defaults for slope radios use a separately authored complete bank: correct ae^t; retained constant ae^t+C; omitted exponential evaluation a; omitted coefficient e^t; zero. Normal derivative radios use correct ae^x; retained C (ae^x+C); omitted coefficient e^x; retained constant only C; zero. The legacy log-scale bank has defensible same-method default operations: use constant as coefficient, retain constant, differentiate everything to zero, return the constant only. None adds learner-facing diagnosis. All profiles compute correct first, preserve one fixed solution, and reject any equal pair in a radio bank.

## 4. Reusable Markdown/value masks

Prompt components are built from complete mathematical slots: signed coefficient term, complete constant, ordered two-term function expression, complete point expression, and response layout. No short-number global replacement is used. Derivative expression masks preserve source e braces and f prime notation; signed terms avoid bare +- and --.

Fixed prose is the source's complete opening about the derivative of e^x and constant C, followed by “Using the addition rule, then, we have” or the slope version “First, using the addition rule, we get”. Derivative solution masks keep exactly four stages: D(f), distributed D(term1)+D(term2), extracted coefficient D(e^x) and explicit zero, final ae^x. Constant-first sources keep the same first/second order and signed coefficient reduction. Nested aligned wrappers are retained where observed. A legacy source has no solution to reproduce, so it uses the canonical prose and this four-stage sequence as an explicitly authored fill.

Slope solution additionally uses the exact source sentence “Therefore, the slope of the tangent at $x=t$ is” and the restriction/evaluation/final sequence. At t=1 it omits the redundant intermediate product; t=0 and logarithmic points retain the evaluated e-component and product before final collection. All displayed rows are parsed independently and checked against the derivative of the **actual printed prompt**. The solution never depends on a chosen error option.

Easy samplers use source-sized signed integers, source layouts and familiar exact points; moderate/hard bounds and rationale are recorded in classification. All explicit inputs receive the same level and profile guards as samplers. A rational is normalized before the guard, so a hidden common factor cannot defeat the noninteger workload condition. Incorrect explicit parameters fail; normal sampling rejects the entire invalid bank and resamples.

Identity is a stable UUID derived from generator version, actual prompt, full fixed solution, field type, sorted complete displayed bank and correct value. Seed and option order are excluded; changed aliases/banks change presentation identity. Mathematical fingerprints exclude the constant, formatting, unused point on a derivative-only task, and profile. Source parameters replay through the same formulas and renderers as varied instances, without returning literal source payloads or answer lookup tables.

Plot extraction/specification: **none**. There are no prompt, option, canonical or solution plot references in this KP. Steps 5 and 7 require no assets or rendering.
