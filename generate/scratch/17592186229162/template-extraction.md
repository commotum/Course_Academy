# Template extraction

## 1. Specific sources

All ten prompts provide a constant-coefficient first-order ODE in x and y, a supplied complementary exponential Ae^(-b*x/a), and ask for the RHS fragment of y_p(x). All source coefficient/exponent forms are integers. Signed b, negative exponents and a negative second forcing coefficient occur. Every rated blank owns exactly one mathematical expected answer; no option pool, distractor, mixed field or plot exists.

| Source | Template | a | b | k (ordered) | c (ordered) | a*k+b | expected trial coefficients |
|---|---|---:|---:|---|---|---|---|
| q-332393 | legacy_single | 9 | 18 | [2] | [4] | [36] | ['1/9'] |
| q-332645 | legacy_single | 5 | 10 | [-3] | [15] | [-5] | ['-3'] |
| q-332644 | single | 3 | -6 | [4] | [9] | [6] | ['3/2'] |
| q-332655 | single | 5 | -20 | [-1] | [15] | [-25] | ['-3/5'] |
| q-332659 | single | 6 | -18 | [-2] | [24] | [-30] | ['-4/5'] |
| q-332664 | single | 7 | 14 | [-5] | [21] | [-21] | ['-1'] |
| q-332667 | two_hard | 4 | 8 | [2, 3] | [5, 3] | [16, 20] | ['5/16', '3/20'] |
| q-332668 | two_and | 3 | 9 | [1, 4] | [7, 4] | [12, 21] | ['7/12', '4/21'] |
| q-332669 | two_comma | 1 | 3 | [2, 5] | [2, 1] | [5, 8] | ['2/5', '1/8'] |
| q-332670 | two_doublecomma | 2 | -6 | [1, 2] | [3, -2] | [-4, -2] | ['-3/4', '1'] |

The q332393 legacy equation has a9,b18,c4,k2, yielding alpha=4/(18+18)=1/9. q332645 has a5,b10,c15,k-3, yielding alpha=15/(-15+10)=-3. These are independent derivations of missing values, not recovered source keys.

## 2. Shared pattern

For a*y'+b*y=sum(c_i*e^(k_i*x)), with distinct nonzero k_i, try y_p=sum(alpha_i*e^(k_i*x)). Differentiate, substitute, distribute a and b, collect coefficients, and solve alpha_i=c_i/(a*k_i+b). Every a*k_i+b must be nonzero, so no resonance adjustment is assessed.

## 3. Complete component and bank mapping

Every source field is field-1, blank, with answer fragment sum(c_i/(a*k_i+b)*e^(k_i*x)); the ordered coefficients in the table completely map all eight displayed bank members and their correct designations. The two legacy raw banks have zero displayed choices and no correct ref; the public generate API reproduces those absences with their original profile names. Blank fields have no distractor recipe. Exact replay compares all answer values one-to-one, not only a mathematical canonical simplification.

Prompt components: a multiplying dy/dx, signed b multiplying y, complete signed forcing sum, homogeneous exponent -b/a, and supplied y_p(x)= fragment. Worked-solution components retain the shared opening sentence, complete forcing prose, nonoverlap assertion, trial, derivative, substitute sentence, grouped substitution row, unevaluated distribution row, collected row, coefficient equations and solved coefficient equations for two terms, then the final particular solution. A one-term source solves alpha as the fourth aligned row and omits separate coefficient blocks. All eight source solution strings replay exactly, including spaces, punctuation, paragraph ordering and redundant arithmetic stages. Source-specific separator patterns are explicit presentation templates, not inferred authoring intent.

## 4. Reusable template, guards and extensions

Fixed wording/masks are in render(); the slots are complete coefficients, exponent arguments, exponential terms and ordered equation components. No global short-token replacement changes the mathematics. Coefficients are combined by signed helpers so negative a*k and b values do not create bare -- or +-. Intermediate rows preserve unevaluated distribution masks, then collection, rather than collapsing to a CAS final answer.

All levels: positive integer a, integer complementary exponent -b/a, nonzero b,c,k; distinct k; nonresonance a*k+b!=0; a1..9, |b|<=30, |k|<=5, |c|<=30. Easy uses one term and integer -b/a. Its observed coefficients may give rational final trial coefficients; the supported unrated repair may also have rational normalized forcing (4/9). Moderate uses two terms and a1..3. Hard uses two terms, displayed a4..7, primitive whole-ODE leading coefficient a/gcd(a,b,c1,c2)>=4, with both c/a noninteger, anchored to q332667. The GCF guard applies to the reduced mathematical object: a4,b8,c[2,6] is rejected because it reduces to a2,b4,c[1,3], a moderate task; a6,b12,c[-3,9] similarly reduces to leading coefficient2. Both explicit input checks and whole-instance sampling enforce this guard. The observed hard a4,b8,c[5,3] has GCF1 and remains valid. These authored bounds preserve parallel same-level tasks rather than introduce harder methods. The moderate/hard distinction is an authored arithmetic policy supported by sparse original labels, not a claim of recovered curriculum thresholds. All constraints are enforced on explicit normal inputs as well as sampling. Raw replay intentionally preserves observed presentation and field absence.

Normal output minimally clarifies: "Use a linear combination of the displayed forcing exponentials." The unrestricted original request also mathematically permits adding any homogeneous term to the expected particular solution. The native fixed-answer grader rejects such a valid alternative. The clarification fixes response-form eligibility without changing the ODE or answer. Raw original wording and its observed native rejection remain documented separately. The two legacy normal records additionally receive derived answers, source-style worked solutions, easy labels and paragraph separation. The added answers/solutions have no observed fidelity denominator.

Task fingerprints use normalized b/a and normalized forcing coefficient/exponent pairs sorted by exponent: scaling an entire ODE and swapping term order do not count as new tasks. IDs use actual prompt, fixed solution, complete bank, field type and version. Parameter seed/order aliases do not create different content IDs. No plots; steps5/7 need no renderer. No database preparation follows.
