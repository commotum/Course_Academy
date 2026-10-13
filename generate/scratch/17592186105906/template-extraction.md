# Four-stage extraction

## 1. Specific sources

| Source | Source AB-factor, AD-factor, angle; quadrilateral | Response; solution sequence |
|---|---|---|
| q-18188 | 16,21,56°;90 in² | radio; formal formula, substitution, 168 sin56°,139.278…,139; difference139−90=49 |
| q-18192 | 12,9,117°;15 in² | radio; no difficulty, correct reference, or solution; calculate48.114…−15→33 independently |
| q-161104 | 9,7,46°;17 cm² | radio; formal formula, substitution, (1/2)63 sin46°,22.659…,23; difference23−17=6 |
| q-285740 | 6,4,75°;10 cm² | blank; same product stages,11.591…,12;12−10=2 |
| q-285754 | 4,7,45°;7 mm² | blank; same product stages,9.899…,10;10−7=3; wrong intermediate m² unit |
| q-285769 | 2.5,6,63°;5 km² | blank; same product stages,6.682…,7;7−5=2 |
| q-285786 | 5,6.5,90°;13 mi² | blank; formal/substituted/product stages, directly≈16; decimal row omitted;16−13=3 |
| q-72764 | 9,15,52°;34 cm² | radio; evaluated half67.5 sin52°,53.190…,53;53−34=19 |

Decoded TeX has single command backslashes and genuine two-backslash row separators; no escape repair is claimed. Exact raw prose and all captured attributes remain in source.json. Every source mask reproduces its prompt and present worked solution exactly. Source masks are parameterized by complete row components; no literal source-payload return branch exists.

## 2. Shared mathematical pattern

A concave quadrilateral ABCD sits inside enclosing ABD; missing BCD is its indentation. Compute outer area T=(1/2)AB·AD·sin A, round it to integer R, then subtract integer quadrilateral Q. Since Q is integral, round(T−Q)=round(T)−Q. The canonical uses enclosing ACD and missing ABC with the same relationship. Response is integer area, either complete unit-bearing scalar radio choice or delimiter-free integer blank.

## 3. Component and bank mapping

Every source bank is fully preserved under its own `raw_q-*` profile. Opaque scalar offsets below are an evidence replay coordinate system, **not inferred mistake operations**; they generate changed values from the correct difference but are ineligible for learner defaults. Profiles are selected whole before parameters.

| Source | Correct c | Complete values | Exact offset recipes relative to c |
|---|---|---|---|
| q-18188 |49|34,42,49,45,38|c−15,c−7,c,c−4,c−11|
| q-18192 |33 inferred, original designation absent|38,31,33,39,34|c+5,c−2,c,c+6,c+1|
| q-161104 |6|8,7,5,4,6|c+2,c+1,c−1,c−2,c|
| q-72764 |19|34,23,19,13,25|c+15,c+4,c,c−6,c+6|
| four blanks |2,3,2,3|one integer each|c|

All 24 options are one-to-one replayed; 16 are radio distractors. There are 7 original correct designations; q-18192 has none and cannot count as a matched observed key. Its old owning lesson JSON confirms the same five radio values, no answer key or worked solution. Supported normal inferred key: (1/2)(12)(9)sin117°≈48.114352; round48−15=33.

For normal five-choice method banks: easy `[S−Q,S,S+Q,Q,round((S−Q)/2)]` (correct difference, omit subtraction, add Q, answer given quadrilateral, halve difference). Moderate/right-angle hard `[R−Q,R,R+Q,round(2T)−Q,round(T−Q/2)]` (omit half-factor, incorrectly halve subtracted area). Nonright hard `[R−Q,R,R+Q,round(2T)−Q,round(ab/2)−Q]` (omit half-factor or sine). Blank uses c alone. Reject the entire selected bank on any repeated/nonpositive value; never replace individual choices. Wrong options can exceed the enclosing area because they implement concrete arithmetic mistakes; they never have negative area. Original option styling is retained raw; normal radios use text units consistently. No new learner-facing distractor diagnosis is added.

## 4. Reusable masks and constraints

Source prompt masks retain image-first placement, nearest-integer wording, calculator note only where observed, and exact blank key. Raw q-18192 omits difficulty/solution/correct ref. Repaired q-18192 fills them explicitly, with evidence-only opaque bank. Hard source solution masks preserve formal formula → factor substitution → half-product form → optional decimal → rounded outer area → difference formula → numeric difference → final unit-bearing result. Decimal truncation to 3 places follows source presentation. The right-angle family omits the decimal stage, as observed. Normal unit replacements are whole text-unit slots, protecting prose such as integer and TeX commands such as begin/sin.

Normal side-length ratio is at most 2.5, supported by the observed 6:2.5 geometry, to keep diagrams legible. Normal bounds are enforced on explicit parameters and samplers. Whole-bank validity uses rounded complete values. Sampler Q is 45–85% of outer area, retaining a readable indentation; explicit geometry additionally requires 0<Q<T and positive rounded answer. Orientations 0/90/180/270 and units are incidental; fingerprints exclude them and canonicalize commutative side order. Easy fingerprint excludes unassessed geometry-side data and includes only supplied enclosing area/Q. Content identity includes actual prompt, solution, complete sorted bank, presence of correct ref and difficulty; option shuffle/seed cannot change it.

## Errors and supported repairs

q-285754 displays mm lengths and mm² prompt/final area but an m² rounded intermediate; raw preserved, normal fixes to mm². q-285754, q-285769 and q-285786 reverse the displayed AB/AD factors relative to raster side labels; products/final answers remain correct by commutativity. Raw diagrams and rows retained, normal changed geometry follows each displayed substitution order so no label misstatement remains. Canonical prose lists the difference in opposite verbal order but its explicit outer-minus-quadrilateral equation is correct; canonical remains context evidence only. No source options are silently removed. Historical error intent remains unresolved and is never a learner-default bank.

Native rounding form: all integer blanks require a canonical rounded integer. Actual engine checks accept surrounding whitespace but reject equivalent unevaluated `2+0` and leading-zero `02`; these are recorded expected form rejections, not algebra mistakes or unresolved errors.
