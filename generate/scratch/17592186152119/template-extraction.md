# Four extraction stages

## 1. Specific source descriptions

| Source | Coefficients | Factors | Input power rows | Prompt/layout and fixed solution |
|---|---|---|---|---|
| q-218518 | 3,4,6 | (x + 1) | 3;2;5 | Three separate math spans, blank; no captured solution |
| q-218519 | 2,4,5 | u,(v - 2) | (2,3);(3,2);(1,4) | First span contains first two inputs; blank; no captured solution |
| q-112230 | 5,6,12 | (x-5),(y-2) | (5,3);(3,3);(3,2) | Find-polynomials radio; 24 ordered math spans in solution |
| q-222127 | 3,9,2 | (x+5) | 4;1;2 | Blank `is{{field-1}}`; 17 solution math spans |
| q-222129 | 8,2,10 | (y-7) | 3;5;2 | Same blank template, different multiples-list spacing; 17 spans |
| q-222132 | 3,8,2 | (x-7),(y+2) | (1,3);(3,1);(5,2) | First-two-input math span; blank; 24 solution math spans |
| q-76247 | 6,4,8 | (x-5) | 1;3;4 | Find-LCM radio; single-factor solution, ending period; 17 spans |
| q-76475 | 20,10,12 | x,(y+2) | (7,1);(6,3);(4,2) | Monomial braces in powered x, radio; 24 solution math spans |

Every coefficient is a positive integer, every factor is primitive and linear, and the factors are already shown. Exponents are positive and powers of one omit exponent notation. The source LCM keeps integer content (e.g. 60, not 1). Constants have a separate LCM demonstrated with multiples, then factors have maxima demonstrated, followed by a formal variable-part LCM and a final product. The single-factor solution describes its maximum in one sentence; the multi-factor version lists each factor's three powers, says to raise each factor to its maximum, and has a three-row final aligned expression.

## 2. Generalized family and purpose

Given exactly three positive-integer-content polynomials already expressed as products of distinct primitive factors, find their least common multiple over the integer polynomial ring. Compute the integer LCM of the three constants, then retain each displayed factor to its greatest input power. Blank entries contain the complete LCM polynomial without math delimiters; radios choose among five complete polynomial expressions. No polynomial expansion or factorization is required in the learner question.

## 3. Complete component and choice mapping

Let C be the LCM of coefficient triple c, M the column maxima, m the column minima, S the column sums, P the LCM of the first two coefficients, and e_2 the second input's single-factor exponent. Each value below maps one-to-one to its original field and correct designation. Choices are always generated as a complete eligible five-entry bank, never filled from a pool.

| Profile/source | Full source bank mapped to parameterized components | Interpretation limit |
|---|---|---|
| q-76247 | 24 F^4 correct=C F^M; 48 F^4=2C F^M; 24 F^6=C F^(2e_2); 48 F^6=2C F^(2e_2); 64 F^8=max(c)^2 F^S | Exponent6 and coefficient64 patterns are underdetermined; recorded expressions are replay patterns, not recovered author intent |
| q-112230 | 60 F^5 G^3 correct=C F^M0 G^M1; 30 F^5 G^3=P F^M0 G^M1; 90 F^5 G^3=(C+P)F^M0 G^M1; 60 F^11 G^7=C F^S0 G^(S1-1); 90 F^11 G^7=(C+P)F^S0 G^(S1-1) | Actual input G powers sum8, not7; S1-1 is an explicit observed value recipe with unresolved mistake interpretation. It is never the default learner bank |
| q-76475 | 60 x^7 G^3 correct=C maxima; 120 x^4 G=2C minima; 120 x^7 G^3=2C maxima; 60 x^17 G^6=C sums; 60 x^4 G=C minima | Whole bank supports ordinary wrong coefficient, minimum-power and multiply-input-power operations |
| q-222127 | 18(x+5)^4=C F^M | Blank; no wrong options |
| q-222129 | 40(y-7)^5=C F^M | Blank; no wrong options |
| q-222132 | 24(x-7)^5(y+2)^3=C F^M0 G^M1 | Blank; prose typo separately repaired |
| q-218518 | No source answer; derived12(x+1)^5 | Completion denominator, not bank match |
| q-218519 | No source answer; derived20u^3(v-2)^4 | Completion denominator, not bank match |

Every normal authored radio bank is C maxima, GCF(c) maxima, product(c) maxima, C minima, C sums. The content mistakes are the actual assessed-method operations of taking a GCF instead of an LCM and multiplying all constants instead of finding their least common multiple. Minimum and sum powers are actual wrong maximum-selection operations. Any coincident content value rejects the entire instance. All underdetermined scalar 2C source recipes stay in explicit observed replay profiles, marked evidence-only and ineligible for learning. No invented diagnosis is shown to learners. The fixed solution never depends on the selected answer.

All prompt math spans are complete polynomial components (or complete first-two-polynomial groups). `masks.json` separates unchanged prose from ordered math slots. `source_solution_math` fills each formal LCM input, coefficient heading/list, power list, maximum reference, variable LCM row, and final product row from current parameters. Multiples lists are recomputed from the coefficient and integer LCM; source ellipsis styles and original punctuation are preserved, while full-list lengths follow the changed LCM. The two missing solutions receive all common instructional stages rather than only a final CAS answer.

## 4. Reusable masks, domains and calculations

Easy: one nonzero-shift factor, coefficients2..12, powers1..5, integer LCM≤60, at least two distinct input powers. Moderate: two factors in two independent variables, coefficients2..20, powers1..7, integer LCM≤120, and each power column must require maximum selection. Both monomial/binomial and binomial/binomial layouts are supported. Hard: three nonzero-shift factors in x,y,x with first/third shifts distinct, coefficients2..20, powers1..5, integer LCM≤120, all factors substantive in all inputs, unique maxima distributed over the three input rows. Shift magnitude≤9. Explicit inputs receive every bound, as do observed bank profiles. All displayed factors are monic and primitive, so their distinctness test is already the reduced mathematical-object test; hidden GCFs cannot reduce factor workload.

A selected complete bank is constructed before acceptance. Any collision or equivalence rejects the whole instance. Source-only uncertain banks remain explicitly requestable for faithful replay and changed-parameter inspection; default generation uses defensible authored or observed-derived complete banks. Changing seed only reorders choices at fixed parameters/profile; identity hashes version, prompt, complete fixed solution, owned bank and field type. Mathematical fingerprint is the unordered set of three expanded integer-content input polynomials, excluding complete banks and profiles, and minimizing over consistent variable aliases. Thus input order and variable spelling cannot inflate task counts. Polynomial scalar multiples are not identified, because integer content is assessed.

The native grader verifies factored canonical and independently expanded forms, and rejects 2 times the answer: this substantiates the intended positive integer-content convention. Formatting, all numeric multiple lists, all printed LCM equalities and every maximum sentence are checked from the actual displayed text without using generation parameter math. Full source solution-string equality separately verifies stage sequence and prose. Plot extraction/generation are not applicable: none occur in any source or authored variation. The work stops after step7.


## Raw omission replay and completion separation

`raw-q-218518` and `raw-q-218519` are public parameterized evidence profiles. They preserve the original absent choices, correct ref, difficulty and worked-solution attributes, rather than filling them during source fidelity replay. `source-cases.json` uses these raw profiles. `completion-q-218518` and `completion-q-218519` are separately labeled normal authored completions, with independently verified answers and full shared-method solutions. Every raw omission or source-error profile sets evidence_only=True and eligible_for_learning=False. Observed radio replay profiles are also evidence-only because their exact scalar patterns have limited interpretation; normal generation selects the complete assessed-method operation bank. Changing valid explicit parameters in a raw omission profile changes its displayed input polynomials while retaining every source omission.
