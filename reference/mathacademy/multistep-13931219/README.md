# Manual multistep capture: 13931219

Radical Functions and Polynomials in Geometrical Settings, multistep 1780,
Mathematical Foundations II. Completed October 3, 2026 at 9:36 PM: six of six
questions correct, 10 XP plus the 3 XP perfect-score bonus.

`content.json` contains six ordered questions, seven MathQuill answer fields,
correct field values verified by the site's grades, original worked solutions,
source difficulty ratings, topic/KP links, and resolved database KP UUIDs.
`assets/manifest.json` maps three original diagram URLs to permanent files and
SHA-256 hashes. The first question's explanation has its own triangle diagram;
the shared pool diagram and the four-option graph image are also saved.

Keep the shared pool context and preceding parts with these questions. Later
parts refer to the polynomial, earlier answers, or “part 5”; importing their
isolated stems would lose necessary information. Question 2 offers diagrams
A–D in one image but uses a typed blank, not radio inputs. Question 5 has two
blanks; its second field supplies only the coefficient after the printed
`x = -8 ± i`.

The live page used `#steps > .step`, `#question-N`, and
`.matheditor-wrapper-answer .mq-editable-field`. Within each question, locate
`.matheditor-wrapper-answer` by its zero-based field index; the wrappers have
no IDs. Submit and continue buttons are `#submitButton-STEP` and
`#continueButton-STEP`. After submission, the live explanation is in
`#question-N-explanationFrame`. Activity explanations are siblings of the
question nodes, selected as `#questionExplanation-N`, and expand through
`#question-N .helpButton`. Source KP links use `.questionKP`; difficulties
use `.questionDifficulty`. These selectors were observed on this activity.

Raw live, answered, and graded HTML/JSON/screenshots are saved for every part.
The initial/full live page includes the shared context; the activity record
omits that context. Activity HTML, separate solution records, and image bundles
are preserved too. `completion.png` proves the perfect result.

`knowledge-state-completed.json` holds the post-activity display bands for all
1,040 topics across courses 113, 111, and 136. No mid-activity snapshot was made.
These are displayed repetition bands, not continuous/internal learner state.

Read-only database matching at basis 323 found all six question IDs are new and
resolved all six KPs by topic and trimmed title. Nothing was transacted. The
manual capture did not modify the automator; multistep support was added
separately afterward. No canonical examples were presented.

To reproduce normalization from saved evidence, run `prepare_capture.py`, then
`read_database.py` for a fresh read-only database comparison. The latter needs
access to the local database socket. Neither script writes database records.
