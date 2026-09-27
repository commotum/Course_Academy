# FIRe: findings from the authorized live account inspection

Inspected September 26, 2026, Pacific time (September 27 UTC), through the user's
existing Math Academy session. Only completed activities, course progress, and
the currently offered menu were read. No lesson was started, no answer was
submitted, and no account setting was changed.

The [captured observations](fire-live-observations-2026-09-26.json) contain
**162 question occurrences in nine completed tasks**, with question IDs,
topic/fragment links, E/M/H labels, outcomes, and displayed timing. They also
contain a **360-topic graph color snapshot** and the **five currently offered
lessons**. Each saved question row and graph topic/color pair was checked against
a checksum calculated from the corresponding browser capture. These checks
guard against transcription mistakes; they are not authenticity signatures.

This improves the evidence substantially, but does not expose numeric FIRe
memory, repetition progress, learning speed, encompassing weights, or due times.

After matching overlapping task/occurrence identities, the old and new sources
cover **39 observed tasks and 396 question occurrences**. Of these, 162 now have
direct question-to-topic links; 67 additional older occurrences have only their
task's topic as a scope assumption. The union of indexed task IDs is 218. All
74 overlapping question-feature records agree on correctness, difficulty, and
elapsed time. The capture contains 160 distinct question IDs across 128 topics.

## Completed activities recovered

| Task ID | Activity | Questions | Correct | Incorrect | Displayed elapsed sum |
| --- | --- | ---: | ---: | ---: | ---: |
| 11604423 | July 14 Calculus II diagnostic | 45 | 20 | 25 | 3,015 s |
| 12563189 | August 18 Calculus I diagnostic | 16 | 3 | 13 | 1,236 s |
| 13469233 | September 17 Foundations II diagnostic | 65 | 39 | 26 | 5,010 s |
| 13553418 | September 24 Quiz 4 | 10 | 7 | 3 | 900 s |
| 13675888 | Polynomial root multiplicities review | 3 | 2 | 1 | 610 s |
| 13675890 | Rules of sum and product review | 3 | 3 | 0 | 2,078 s |
| 13675889 | Transformed logarithmic functions review | 3 | 3 | 0 | 1,402 s |
| 13682227 | September 24 Quiz 4 retake | 8 | 8 | 0 | 857 s |
| 13682230 | Function arithmetic multistep | 9 | 9 | 0 | 651 s |

The last task is absent from the original 217-row progress CSV. It completed at
19:50 on September 24, after that CSV's final activity. The original CSV and
reduced XP observations remain intact; this is an additional source, not a
silent replacement of their provenance.

## The quiz errors identify the intervening review topics

Quiz 4 completed at 11:25 with incorrect answers on precisely three topics:

| Quiz topic | Question ID | Subsequent review | Completed | Review outcomes |
| --- | --- | --- | --- | --- |
| 88: Multiplicities of the Roots of Polynomials | 74234 | 13675888 | 11:39 | Incorrect, Correct, Correct |
| 161: The Rules of Sum and Product | 122144 | 13675890 | 16:11 | Correct, Correct, Correct |
| 1610: Properties of Transformed Logarithmic Functions | 81989 | 13675889 | 16:34 | Correct, Correct, Correct |

The 17:05 retake follows these reviews. This directly establishes the match
between incorrect quiz topics and subsequent review topics in this sequence.
Together with the published targeted-remediation rule, it supports a remediation
interpretation more strongly than the earlier title/XP-only observations did.
It does not expose assignment times, whether every review was mandatory, or
the internal cause code. These reviews must not be treated as ordinary due-time
observations when fitting a spaced-repetition schedule.

The polynomial review also shows that a completed three-question review need
not be a perfect early exit: it contains one incorrect answer followed by two
correct answers and earns the 4-XP base. The other two reviews contain three
correct answers and earn 6 XP. This sample does not recover the full stopping
algorithm or prove that five questions were preallocated.

The original quiz has ten questions; the retake has eight. The retake covers
eight of the same topic/fragment pairs, including two of the three originally
incorrect topics, using different question IDs. It omits topic 436 (originally
correct) and topic 161 (originally incorrect). Thus this retake is not simply a
test consisting of the three failed questions or the three failed topics.
Its selection/count rule remains unknown. Its eight correct results independently
confirm the previously hypothesized perfect-score award of 18 XP on a 15-XP
base; that is evidence about XP, not FIRe credit.

## The same question can be delivered again

Two exact question IDs recur across the captured diagnostics:

| Question ID | Topic / fragment | July 14 result | September 17 result |
| --- | --- | --- | --- |
| 79870 | 1643 / 4150 | Incorrect | Correct |
| 112044 | 660 / 4971 | Incorrect | Correct |

This is learner delivery evidence, beyond finding a question in multiple
reference lessons. It establishes that MA can repeat an item across diagnostics.
It does not establish a universal repetition policy for ordinary reviews.
Use `(task ID, occurrence index)` for the historical occurrence and retain the
question ID separately. A repeated item is neither a new content identity nor
a reason to overwrite the earlier answer.

## The question links identify example content, not lesson steps

All 162 live `(topic ID, fragment)` pairs uniquely match an **example content
ID** in the corresponding saved lesson JSON. They do not match the placement's
step ID. For example, `/topics/161#5085` refers to example content 5085, placed at
lesson step 18562; fragment 5086 refers to example content 5086 at step 18563.
This extends the earlier verified example-2993 case across every captured result.

Only six captured question IDs occur in the reference-question CSV. All six
agree with the live topic and with the resolved example placement's step ID.
That sparse overlap is consistent with the reference lessons containing question
samples, rather than the full assessment bank. The raw capture's provisional
`step_anchor` field means the URL fragment; it must not be imported as
`:lesson-step/math-academy-id`. Keep topic, example content, question, and step
identities distinct.

## Timing and outcome fields need careful interpretation

All ten original-quiz question timestamps display the same 11:25 completion
time; all eight retake timestamps display 17:05. Their elapsed durations differ.
Those timestamps therefore cannot establish the individual answer timeline.
Diagnostic and review timestamps vary, but still have only minute precision
and no displayed timezone. The raw strings are retained rather than converted
into invented UTC instants or start times.

For example, the counting-rules review displays 33:40 elapsed for its first
question. Such observations do not identify focused work time, expected solve
time, or MA's internal spacing clock. The original quiz's 900-second sum is
consistent with a 15-minute limit, but one total does not prove the stopping
rule; the retake's 857 seconds and eight correct answers do not resolve its
different length.

The older reduced observation for the Calculus I diagnostic uses `no_answer`
labels where the current completed UI says `Incorrect`. These can be compatible:
an unanswered item may be counted incorrect. Preserve the two source fields
instead of replacing an unknown submission subtype with a claimed wrong entry.

## What the live graph and menu establish

The course was Mathematical Foundations II, displayed at 62%. Its graph has
360 topic nodes: 136 gray and 224 blue, across the six legacy blue shades.
The colored proportion is about 62.2%, consistent with the displayed percentage.
This is an observation of agreement, not proof of the percentage formula or a
numeric retention estimate. No numeric FIRe attributes appeared on the inspected
SVG nodes or course-progress circles.

The offered menu contained five lessons: The Law of Cosines; The Shortest
Distance Between a Point and a Line; Factorials; Vertical Translations of
Exponential Growth Functions; and Calculating the Equation of a Tangent Line
Using Differentiation. The capture records task IDs and base XP. It establishes
availability at capture time, not when those tasks first became available or
why they were selected.

The page exposed the current learner identifier, allowing a focused attempt to
open the documented own-account course knowledge-graph GET resource. The browser
blocked navigation with `net::ERR_BLOCKED_BY_CLIENT`. No response was obtained,
and no workaround was attempted. The earlier permission issue is resolved;
this is now a browser-access limitation.

## Consequences for the implementation and schema

- Preserve question occurrence identity, exact question/topic links, source
  fragment namespace, displayed result, submission subtype when actually known,
  and time provenance. The existing optional ordered observation payload can
  carry these without changing question-bank ownership.
- Keep diagnostic placement separate from ordinary retention credit. These
  diagnostic results do not reveal the resulting placement balances or reset
  state, so they cannot initialize MA-equivalent repetition values.
- Separate remediation selection from memory-based review selection. A review
  that follows a failed quiz item is not reliable evidence of a due threshold.
- Keep prior exposure available for evaluation. Repeated diagnostic question IDs
  are observed; how MA accounts for that exposure remains unknown.
- Continue labeling numerical FIRe policies as reconstruction choices. Better
  outcome mappings help replay ability evidence and analyze task selection,
  but do not identify undisclosed retention functions.

The executable reconstruction remains described in
[fire-reconstruction.md](fire-reconstruction.md); the original snapshot's
sensitivity experiments remain in [fire-history-analysis.md](fire-history-analysis.md).

## Reproduce the audit

[The audit program](../engine/fire/live_history.py) verifies captured-row
checksums, compares both original sources, checks catalog namespaces, and
produces [resolved observations and traces](../engine/fire/fixtures/live-history-audit.json).
The output records the input and implementation SHA-256 hashes.

```bash
python3 -m engine.fire.live_history \
  --catalog-root /home/jake/Developer/MA/DATA
python3 -m unittest discover -s tests
```

The full suite passes 67 tests. The new checks cover transcription corruption,
source disagreements, ambiguous ID mappings, repeated item occurrences, and
separation of diagnostic evidence from ordinary answer accuracy.

The audit executes the chosen two-channel accuracy estimator on 18 assessment
answers and 18 practice answers. All 126 diagnostic answers remain separate;
they do not establish placement or retention credit. This is a sensitivity
replay with declared priors, not a recovered MA ability profile. It creates
zero retention events, because task-to-credit magnitudes and initial FIRe
states are still unknown.
