# Classification — KP17592186083278

Frozen source: math, basis1356, lineage01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. source.json is a byte-identical copy of the wrapper. Practice only: eight questions. Actual captured difficulty enum values are easy (5), moderate (2); q-21206 genuinely has no difficulty attribute. There are zero observed hard questions. Source analysis never substitutes canonical examples into practice counts.

| Template | Source | Captured difficulty | Field shape | Banks | Plots |
|---|---|---|---|---|---|
| line_quadratic | q-20853 | :question.difficulty/easy | 1 radio/math, 5 choices | 1 | none |
| line_cubic | q-21206 | absent | 1 radio/math, 5 choices; correct absent | 1 | none |
| circle_horizontal | q-21072 | :question.difficulty/easy | 1 radio/text, 5 choices | 1 | none |
| polynomial_two | q-350359 | :question.difficulty/easy | 2 ordered blanks/math | 0 distractor banks | none |
| spiral_cos | q-350368 | :question.difficulty/easy | 2 ordered blanks/math | 0 distractor banks | none |
| spiral_sin | q-357255 | :question.difficulty/easy | 2 ordered blanks/math; pull order field2 then field1 | 0 distractor banks | none |
| circle_vertical | q-21081 | :question.difficulty/moderate | duplicate selection fields, 5 text choices each, legacy correct absent | 2 historical bank layouts | none |
| power_line | q-122726 | :question.difficulty/moderate | 1 radio/math, 5 choices | 1 | none |
| paired_cubics | no source | authored hard | 2 ordered blanks/math | no distractors | none |

Eight observed Markdown/value families, six observed radio field-banks (including duplicate legacy); twelve total field-banks when six single-answer blank fields are included. All 36 captured answer values remain mapped. No prompt, choice, or solution plot is present in the assigned KP or its canonical example. Adjacent decoded ord92 audit finds zero doubled slashes in all prompts and answer values; aligned worked-solution double-slash line breaks are legitimate. JSON escaping is not a source anomaly.

## Repairs and historical evidence

The authoritative widget capture /home/jake/Developer/MA/DATA/Lessons/799/Source/799.json, question21081, contains ONE five-choice multiple-choice widget. The legacy field and the newer field represent the same bank with different spelling/order. Raw API profiles retain both fields, the missing legacy correct ref, and original values. Normal profiles retain the current correctly designated field only. q-21206's widget confirms one five-choice field; it does not supply a captured correct designation or worked solution. Its mathematical answer t=0 is independently inferred; normal easy is an authored assignment and its solution uses the common source method. Raw omits all absent attributes.

No mathematical source-key errors were found. Raw evidence remains ineligible. Opaque historical line/power scalar banks, including repaired opaque profiles, remain evidence-only. Native grading and mathematical correctness are separate.

## Scope and difficulty rationale

Owning topic799 is Calculating Tangent and Normal Lines with Parametric Equations. Preceding topic798 differentiates parametric curves; preceding topic987 covers normal lines. The actual activity route is reconstructed through first-step/next: Introduction -> Computing the Tangent Line -> Horizontal or Vertical Tangents tutorial -> THIS KP -> Computing the Normal Line -> Determining Normal Horizontal/Vertical. This generator stays at locating tangent parameter values; it never asks tangent equations, normals, polar curves, arc lengths or geometric singularity classification.

The canonical x=t²+3,y=-t+1 establishes differentiating both components, solving one derivative=0, and checking the other is nonzero. The tutorial explicitly disallows inferring a slope from 0/0. All supported normal parameters enforce regularity. In particular, hard excludes intersecting derivative root sets. No source or generated answer claims that 0/0 means both horizontal and vertical.

Easy preserves each of the five observed easy demands and adds a supported cubic/linear missing-record repair. Integer assessed shifts generalize one-factor roots without introducing another method. Moderate preserves full-period vertical trig and a single shifted odd-power root (n in3,5,7), with constant companion derivative. Hard has no observed label: its authored independent workload differentiates TWO cubics, factors the requested derivative, finds two small integer roots, and substitutes both roots into the other nonconstant quadratic derivative. Four distinct factor roots prevent degeneracy and maintain two genuine regularity checks. The prerequisite differentiation and observed easy polynomial factor solve support this extension, but the hard label is a design claim, not recovered calibration. There is no progression within any difficulty: families are unordered independent practice.

All level guards apply to explicit inputs and sampling. Nonzero integer scales have absolute value<=10; linear root shifts <=5; moderate n3,5,7; easy polynomial integer r with |r|1..5 and u/3 with |u|1..8, u not divisible by3, half-integer c,d with |c|,|d|<=3; spiral quarter-turn phase index0..3; hard four distinct nonzero integer roots of magnitude<=4 and scales ±1,±2. Ineligible whole banks reject rather than replace individual options.

Fingerprinting normalizes each derivative's nonzero scalar and discards constant translations: the assessed task is zero-set solving plus regularity within the actual domain. Circle translations, scalar magnitudes, exponentials' outer scales and answer-bank aliases do not inflate mathematical task counts. Full displayed content remains in presentation identity. Familiar quarter-turn phases intentionally form a finite spiral subfamily; polynomial/factor families provide broader repeated practice.

The eligible finite mathematical families (excluding option profiles/notation/scales/translations) are: line_quadratic 11 shifted linear-zero tasks; line_cubic 11 shifted double-zero tasks; circle_horizontal 7 domain tasks; polynomial_two 1,536 (r,u,c) derivative/factor/check tasks; spiral families jointly 2 after quarter-turn and scalar equivalence; circle_vertical 7 domain tasks; power_line 25 eligible (n,s) whole-bank tasks; paired_cubics 420 unordered requested/companion root-set pairs. The easy union therefore supports1,567, moderate32, and hard420 mathematical tasks. Displayed arithmetic scales add presentation variety without inflating these counts. Default sampling serves every supported source family.
