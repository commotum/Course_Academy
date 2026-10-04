Import update (2026-10-04): saved content was committed at EDB basis 410 → 411. The normalized payload is `content-import.json`; `edb-import/verification.json` confirms completeness, a no-op reimport, and unchanged learner/engine facts. `content.json` and the original capture evidence remain preserved. Earlier statements below about no database writes describe the original capture.

# The Sum Rule for Indefinite Integrals — live capture

Math Academy task **13925458**, topic **3769**, completed October 3, 2026.
The lesson served five questions for each of three knowledge points. Actual
sequences were `W-C-W-C-C`, `C-W-C-W-C`, `C-W-C-W-C`. The policy for future
captures is 70% `C-W-C-W-C`, 30% `W-C-W-C-C`; this lesson used the closest
three-KP allocation after its first answer had already been submitted.

All fifteen practice questions have captured problems, source IDs, difficulty,
worked solutions, and one observed radio field with five source choices and the
correct choice identified. No practice choices were invented. The separate
attempt log records intentional answers used to reveal content; these attempts
must not become learner ability evidence.

Three canonical examples were captured live, including their problems and worked
solutions. All three match the previously imported canonical IDs and mathematical
content. Their live views contain no answer widgets or difficulty labels. Their
database records also lack answer fields and difficulty. Those attributes need
authorship if canonical examples are to be complete interactive questions.
Calculator requirements and option feedback were not exposed and remain unknown.

No database transaction or learner/engine update was performed.

## Saved evidence

- `live-capture.json`: DOM HTML and rendered math captured before submission,
  plus each practice solution and grading result after submission.
- `activity-capture.json`: expanded history HTML, KP titles, question IDs, and
  source difficulty labels. It includes source activity details as evidence;
  normalized content excludes timing and learner results.
- `content.json`: content-only import candidate with explicit correct choices.
- `capture-attempts.json`: intentional answer sequence audit.
- `database-before.edn`, `id-matches.edn`: read-only current database evidence.
- `matching-report.json`, `verification.json`: match and completeness checks.
- `prepare_capture.py`: repeatable join and verification of these saved sources.
- `lesson-completed.jpg`: completion screen, showing 7 of 12 XP awarded.

## Database matches

| KP | Existing canonical | Existing encountered practice | New encountered practice |
| --- | --- | --- | --- |
| Computing an Integral Using the Sum Rule | `e-371` | `q-29828` | `q-71168`, `q-113779`, `q-71172`, `q-113778` |
| Computing an Integral Using the Sum and Constant Factor Rules | `e-372` | `q-2166` | `q-113784`, `q-113788`, `q-2160`, `q-113789` |
| Integrating Sums of Power Functions | `e-373` | `q-2250` | `q-49174`, `q-49062`, `q-113845`, `q-113851` |

All three existing practice records have the same correct answer and choice set
as the live widgets, allowing for choice order, whitespace, and redundant TeX
braces. All three lack difficulty and worked-solution. Their existing answer
entities can be preserved when adding those attributes.

The twelve new questions can be created with captured fields and linked to the
KP UUIDs in `content.json`. The original practice questions not served in this
lesson (`q-2159`, `q-211`, `q-29830`) were not refreshed by this capture.

## Observed selectors and identifiers

| Purpose | Live lesson selector |
| --- | --- |
| Current step | `.stepButton.current` (`stepButton-q<ID>`, `stepButton-e<ID>`, or `stepButton-t<ID>`) |
| Practice container and source ID | `#step-q<ID>.questionWidget` |
| Practice problem | `#step-q<ID> .questionWidget-text` |
| Choice rows | `#step-q<ID> .questionWidget-choicesTable tr` |
| Choice value | `.questionWidget-choiceText` within a row |
| Choice label / clickable control | `#questionWidget-choiceLetterCircle-<ID>-<letter>` |
| Submit | `#step-q<ID> .questionWidget-submitButton` |
| Grading result | `#step-q<ID> .questionWidget-result` |
| Revealed solution | `#step-q<ID> .questionWidget-explanation` |
| Advance after grading | `#continueButton-q<ID>` |
| Canonical example | `#step-e<ID> .exampleQuestion`, `.exampleExplanation`, `.stepName` |
| Advance from example | `#continueButton-e<ID>` |
| Tutorial advance | `#continueButton-t<ID>` |
| Completion | `#finalScreen` and `#finalScreen-doneButton` |

These radio fields use clickable divs, with no native input elements. The DOM
choice letter is local to this question presentation; retain the choice value
and Math Academy question ID when matching database answers. Future lessons may
use other field types and require local inspection of their actual widgets.

| Purpose | Activity selector |
| --- | --- |
| Knowledge point | `.kp`, title `.kpTitle` |
| Question ID and problem | `#question-<ID>`, child `.questionText` |
| Difficulty | `.questionDifficulty`, labels `E`/`M`/`H` |
| Expand solution | `#question-<ID> .answerDetails` |
| Solution container | `#questionExplanation-<ID>` (a sibling of the question) |

Capture live widgets before submission, wait for the question's Continue button,
then capture the revealed explanation. Advance and inspect the newly rendered
item before choosing an answer. Visible progress slots alone are not evidence
that their question contents have been loaded.

For MathJax, read each SVG's own descendant `title` and local assistive MathML.
The live page reuses SVG title IDs; resolving `aria-labelledby` globally can
return a different formula. Raw HTML was retained to support reconstruction.
Example IDs use example content IDs (`e-371`), not the original lesson-step IDs.
