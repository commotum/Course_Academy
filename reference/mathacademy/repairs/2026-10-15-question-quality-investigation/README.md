# Investigation of the 18 question records

Live snapshot: math database basis **2615**, after the separately authorized visual repair. This investigation made **no additional live repairs**.

## What affects studying

All 18 are attached to practice banks but fail the application’s actual question validation because at least one graded field has no canonical answer. The five duplicates additionally violate unique field-key requirements. Normal lesson/review candidate selection and inventory filtering call this validator, so these records are excluded from normal practice rather than being randomly served with incorrect grading. Developer previews can still show the captured bank.

There are no retained task-item/content assertions, withdrawals, or submitted-response links for these 18 questions or their field-owned answers in the checked history. This is a statement about retained database evidence, not a claim about everything ever displayed in the original Math Academy website.

The 13 affected KPs contain 147 question records in total: 129 currently validate and 18 are blocked. Each KP has 8–13 structurally usable records before learner-specific exposure and difficulty filtering. Completing the flagged records would increase that bank; it does not itself establish how many fresh questions a particular learner has left.

The native checks used `learning::validate_response_question`. Candidate filtering is in `engine/rust/learning.rs:571` and inventory filtering in `engine/rust/inventory.rs:226`. The proposed keys/field cleanup were simulated only in memory and checked through `learning::grade_field`: 18 accepted and 72 rejected options, no database writes.

## Five duplicate-field questions

The retained history shows an initial unkeyed `selection` field, then a later keyed `selection` field, with no withdrawal of the first ownership link. Both sets of assertions were attributed to `:org/Math-Academy`. These are two physical fields for the same logical response, not two separate parts of the question. The banks match mathematically, all five existing keyed answers check independently, and removing only the stale ownership link makes each question pass the real validator in memory.

| Question EID | Source ID | Old unkeyed field | Later keyed field | Verified existing key |
| --- | --- | --- | --- | --- |
| 17592186059961 | q-10248 | 17592186056125 | 17592186386021 | Final third row (0,5,21); rows 1 and 2 unchanged. |
| 17592186162553 | q-42531 | 17592186160610 | 17592186402822 | R1 := R1 - 2R3; R2 := R2 - 2R3. |
| 17592186162555 | q-42563 | 17592186160622 | 17592186402835 | C2 := C2 - 3C3; C4 := C4 - 2C3. |
| 17592186162556 | q-42917 | 17592186160628 | 17592186402848 | C1 := C1 - 3C3; C2 := C2 - 4C3. |
| 17592186162570 | q-91163 | 17592186160712 | 17592186404524 | R1 := R1 + 2R2; R3 := R3 - 3R2. |

Recommended repair: retract just the five obsolete `question/answer-fields` links. Preserve both field entities, their answers, question IDs and retained history. No answer value, correct key, or difficulty needs to change.

The current importer also does not clean these up automatically: `scripts/question_capture/math_content.py:140` makes a dictionary keyed by `answer-field/key`, collapsing the duplicate candidates. Replaying each keyed field through the actual import planner produced no stale-field retraction in all five cases. This reproduces why reimporting is not a reliable cleanup; it does not prove that this current implementation originally created the duplicates.

### One existing worked-solution error

Question **17592186059961 / q-10248** asks for `R3 := R3 + 3R1`. Its intermediate displayed matrix shows first row **(1,-2,-4)**, although row 1 must remain **(-1,2,4)**. The final displayed matrix and keyed answer are correct. Fix this intermediate row along with the duplicate link before returning the question to practice. Every matrix stage in the other four existing worked solutions was independently checked and passed.

## Thirteen incomplete imported questions

Each has a complete five-option bank but no correct-answer link, no worked solution, and no observed difficulty. Retained history contains no earlier solution or rating assertion for them; the retained key history is also empty for those fields. They were already incomplete, not damaged by the visual repair. Independent exact calculations found one correct existing option in every bank.

| Question EID | Source ID | Skill | Verified answer / required result |
| --- | --- | --- | --- |
| 17592186059963 | q-10252 | Applying Row Operations To an Augmented Matrix | Scale row 1: `[2,4,6]`; other rows unchanged. |
| 17592186059965 | q-10321 | Reducing a 2x2 Augmented Matrix to REF Using Gaussian Elimination | REF rows `[1,-3|-7]`, `[0,1|3]`. |
| 17592186059978 | q-1076 | Reducing a 2x2 Augmented Matrix to REF Using Gaussian Elimination | REF rows `[1,4|3]`, `[0,1|-1]`; x=7, y=-1. |
| 17592186060199 | q-20240 | Identifying the Appropriate Row Operation To Transform One Matrix Into Another | R2 := R2 - 3R1. |
| 17592186060203 | q-20389 | Identifying the Appropriate Row Operation To Transform One Matrix Into Another | Swap R1 and R3. |
| 17592186060204 | q-20392 | Identifying the Appropriate Row Operation To Transform a Given Entry to a Desired Value | R2 := R2 + R1. |
| 17592186096923 | q-10202 | Solving a System of Equations Given an Augmented Matrix Containing Non-Unit Leading Entries | Solution column (2, 0, -3). |
| 17592186097182 | q-20451 | Solving a System of Equations Using Back Substitution | Solution column (-11/2, -5/2, -4). |
| 17592186129774 | q-42026 | Identifying Augmented Matrices in Row Echelon Form | A only is not in row echelon form. |
| 17592186129776 | q-42362 | Identifying the Leading Entries of a Matrix | Leading-entry sum 3 + 1 + 2 = 6. |
| 17592186129777 | q-42363 | Identifying the Leading Entries of a Matrix | Leading-entry sum 4 + (-2) = 2. |
| 17592186129778 | q-42369 | Identifying Matrices in Row Echelon Form | B only is not in row echelon form. |
| 17592186162574 | q-91208 | Using Column Operations to Create a Row of Zeros in a 4x4 Matrix | C1 := C1 + 5C4 and C3 := C3 - 3C4. |

Recommended repair: reuse the existing correct answer entity and author a worked solution using the KP canonical example and matching nearby solutions. Keep source IDs, field IDs, option banks and learner history. Treat these new explanations/answer deductions as authored repairs, not recovered original-source solutions.

Keep their difficulty unrated unless genuine observed rating evidence is recovered. `schema/content/4-question.edn` defines difficulty as observed metadata. The selector permits structurally valid unrated questions only as a fallback when no eligible positively weighted rated band remains; completing a question does not justify inventing an Easy/Moderate/Hard label.

## Decision options

1. **Recommended first:** clean the five stale field links and correct the q-10248 intermediate row. This recovers five already rated questions with verified existing answers and solutions.

2. **Then, if more source-bank coverage is wanted:** complete the 13 imported questions with verified keys and authored worked solutions, retaining unrated status. These are mathematically recoverable; no new distractors are required.

3. **Leave them excluded:** no action is needed to prevent their normal selection, because current engine validation already blocks all 18. This retains the smaller usable question bank.

No corrective transaction for these 18 has been submitted. The only live write in this turn is the previously prepared, explicitly authorized 181-field visual repair at basis 2615.

## Evidence files

`questions.json` and per-EID EDN pulls; `field-history.edn`, `correct-history.edn`, `solution-history.edn`, `difficulty-history.edn`; `provenance.json`; retained presentation/response history; `answer-analysis.json`; `native-report.json`; `pool-inventory.json`; `import-reproduction.json`.
