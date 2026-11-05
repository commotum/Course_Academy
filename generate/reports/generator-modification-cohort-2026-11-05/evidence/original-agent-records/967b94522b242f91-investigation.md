# Exact values using the cosine double-angle identity

KP **17592186087671**, “Finding Exact Values of Trigonometric Expressions Using the Double-Angle Formula,” has sufficient complete imported examples. **No reconstruction is needed; exemplars_file is null.** The selected reference is this same KP, not an unrelated analogue. All observations use the supplied `math` snapshots at basis **7323**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. No database queries, publication, or import edits were performed.

The learner recognizes a cosine double-angle identity in a numerical expression, doubles the angle, evaluates the resulting standard-angle cosine with its correct quadrant sign, and supplies an exact value. Hard questions additionally require recognizing an expanded perfect square and squaring the evaluated cosine. Solving trigonometric equations, half-angle extraction, and sine/tangent double-angle identities are outside this evidence.

## Source context and components to retain

The supplied lesson “The Double-Angle Formula for Cosine” (activity **17592186087908**) derives the identity from the cosine sum formula in tutorial **2638**, then derives both alternatives using the Pythagorean identity in tutorial **2639**. Neighboring KPs **17592186087669** and **17592186087670**, canonical examples **e-3666** and **e-3667**, simplify to a single trigonometric ratio. This KP adds exact evaluation. Its canonical example **e-3668** (entity **17592186087479**, UUID `e617aaf2-1232-57cc-8644-2467effda030`) transforms the difference at 22.5° to cos 45° and then √2/2.

The explicit supplied prerequisites array is empty. The lesson itself supports the prerequisite context: cosine addition, Pythagorean identity, double-angle recognition, special-angle values and quadrant signs; hard practice also draws on binomial-square recognition. These are instructional dependencies, not newly asserted database prerequisite links.

Retain degree/radian notation, exact-value instructions, complete five-choice banks on radio questions, single keyed blanks where present, and the worked sequence identity → substitution → doubled angle → exact evaluation. Hard solutions first identify the perfect square and finish by squaring the intermediate value. No diagrams or image references occur in the supplied material; plot requirement is **none** for every template. The eligibility snapshot excludes no questions.

Crucially, the identity reminder, substitution, reference-angle explanation and perfect-square hint occur **in the worked solution after answering**. Prompts do not supply these steps or assess them in separate fields. Moving them before the response would lower the demand. Radio banks support recognition/elimination; blanks require producing the exact value without choices. Neither asks the learner to submit a derivation.

## Observed and intended progression

| Band | Existing demand and response | Complete source IDs and independently checked answers |
| --- | --- | --- |
| Easy (6) | Direct cos²x − sin²x → cos 2x; 4 radio, 2 blank | q-24514: √3/2; q-120367: −√2/2; q-120368: √3/2; q-332138: √2/2; q-332139: −√3/2; q-7470: −√3/2 |
| Moderate (5) | Mostly recognize 1 − 2sin²x → cos 2x before evaluation; 4 radio, 1 blank | q-26706: −√2/2; q-120369: −√3/2; q-120370: √2/2; q-332147: −√2/2; q-7473: √2/2 |
| Hard (4) | Recognize cos⁴x − 2cos²x sin²x + sin⁴x = (cos²x − sin²x)², evaluate, then square; all blank | q-275706: 3/4; q-332148: 1/2; q-332150: 3/4; q-332151: 0 |

The six supplied reference questions are **q-24514** (entity 17592186088096), **q-120367** (17592186256399), **q-26706** (17592186088111), **q-120369** (17592186256401), **q-275706** (17592186292878), and **q-332148** (17592186304988). Their full UUIDs, as well as all other source identities and answers, are indexed in [source-audit.json](evidence/source-audit.json). Their complete prompts, fields, choices and solutions remain available in the supplied snapshots and [source-records.json](evidence/source-records.json).

There is genuine overlap in the imported labels: moderate **q-120370** uses the same direct-difference method as easy questions, and easy **q-120368** already includes a quadrant reduction. Larger angles, decimal degrees, negative results, or radians alone do not establish a higher level. Preserve these imported labels; use alternative-form recognition as the intended moderate progression rather than pretending every imported moderate question adds a step. Although 2cos²x − 1 is taught, no target practice question uses it; it is a lesson-supported extension, not an observed practice template.

For classification, easy has direct-difference radio and direct-difference blank templates. Moderate has alternative-form radio, alternative-form blank, and the overlapping direct-difference radio template. Hard has one mathematical backbone with two prompt layouts: inline degree expressions and display radian expressions. Preserve these layouts and their field placement separately. All fields are mathematical; radio keys are `selection`, blank keys are `field-1`.

Choice banks are not interchangeable. Easy radio q-24514 includes −√3, q-120367 includes both signs of √2/2, while q-120368 and q-7470 share a bank up to order. Moderate q-120369 and q-120370 share a bank up to order; q-26706 instead includes positive 1/2, and q-7473 uniquely offers 0 and 1. Blank fields store one correct answer, not a distractor bank. Full banks are retained in the evidence copies rather than replaced by a common recipe.

Future same-method variation can change eligible angles while deriving doubled angles, signs, answers, banks and solutions together. Vary positive/negative direct and alternative-form outcomes; hard outcomes are necessarily nonnegative because of the square. Keep the useful zero case q-332151 even though it admits direct evaluation. Do not reject simplifications or make every hard answer 3/4. One-answer radio/blank structure and the coefficients of the identity have mathematical reasons to remain fixed; answer position and incidental angle format do not.

## Checks and result

Read the full target material, lesson, canonical example, all 15 banks and solutions, prerequisite context, eligibility and image lists, all six reference questions, `generate/principles.md`, `generate/docs/3-classify.md`, and the offline validation-tool instructions. Source, inventory and reference agree on coverage **easy/moderate/hard = 6/5/4**; all 15 are complete. Authored questions do not alter observed coverage; none were created.

[check_source.py](evidence/check_source.py) independently evaluates all expressions using exact SymPy trigonometry and compares both the reduced identity and stored key. It also verifies one mathematically correct choice per field, inventory membership, reference membership and labels. All pass. Snapshot hashes are saved in the audit. Evidence records preserve imported content; the sole structural adaptation is converting pulled correct-answer objects to UUID lookup references for the native harness. Legacy doubled command slashes remain in those copies and work in the actual grader and renderer.

The native `learning::grade_field` harness passes **67 checks: 21 accepted, 46 rejected, zero unresolved**, covering every radio choice and independently determined valid and wrong blank responses. See [grading-input.json](evidence/grading-input.json) and [grading-report.json](evidence/grading-report.json).

`generate/pipeline/render_preview.py` renders all **15** prompts, answer controls and worked solutions through the unmodified learning UI. [rendering.json](evidence/render/rendering.json) passes every case with no exposed TeX, math errors, broken images, dangling glyphs or JavaScript errors. All screenshots were visually inspected in contact sheets 1–5. No dropdown fields exist. Long hard-question display equations use the UI's existing horizontal scrolling; the additional [hard-scroll report](evidence/hard-scroll/rendering.json) and scrolled screenshots verify their right-hand sides. This is an offline completed-state UI preview, not a claim about database publication, live question selection, or learner history.

No shared code or native binary repair was needed. Existing examples supply the usable instructional result; proceed from their unchanged source identities and complete evidence copies.
