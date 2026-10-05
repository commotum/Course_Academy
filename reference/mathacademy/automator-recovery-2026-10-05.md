# Capture recovery, October 5, 2026

The last batch stopped at 00:24 PDT after the solver for task 13949542 reported
`Selected model is at capacity. Please try a different model.` No capture worker
or held capture lock remained. All five offered lessons were saved as deferred,
so normal queue selection correctly found no eligible activity. Explicit resume
is required for these saved attempts.

## Repairs

- Solver capacity errors receive at most two 30–60 second retries, reusing the
  confirmed activity session. Other CLI failures are not automatically retried.
  SIGTERM interrupts both the CLI process and retry wait.
- Displayed original images are attached to solver turns alongside screenshots.
  The screenshot of q-139719 had clipped stations C and D. The saved original
  diagram shows two A-to-D routes, one B-to-C route, and zero C-to-C loops:
  a+b+c=3. Its uncertain solver answer was resolved from that original image.
- Inequalities use the visible `lteIcon` / `gteIcon` buttons. Typed commands are
  completed before leaving their command input. An unfinished command now blocks
  Submit even if its LaTeX string matches the intended value.
- q-336130's explicit multiplication dot between named functions now compares
  equal to the equivalent implicit product. Grouping, signs and exponents remain
  guarded. q-336932's old typing sequence now supplies the outer grouping required
  by `(ln(9))^2`; the comparison was not weakened to accept `ln(9)^2`.
- Two exact, topic-scoped live-example/history KP title variants are recognized
  for topics 612 and 708. Canonical KP IDs and original captured text are retained.
- Lesson start navigation waits for DOM readiness; later content-readiness checks
  still require loaded questions before answering.
- Known failed lesson/review completion messages are terminal captured attempts,
  including their partial question pools. Negative penalties such as `penalty of
  -2 XP` are parsed. A failed attempt does not mark a lesson topic successfully
  captured and therefore does not exclude a subsequently offered retake.

## Recovered content

| Task | Recovery | Verified import basis |
|---|---|---:|
| 13942892 | Factorial answer q-124142 was mixed inline math stored as text; corrected to math using the captured solution | 571 → 572 |
| 13944892 | Trend-line q-133772 corrected from 2008 to 2010 using the original graph and explicit worked solution | 572 → 573 |
| 13945275 | Continuity KP title variant; captured remaining history | 573 → 574 |
| 13947355 | Rational-equations KP title typo; captured remaining history | 574 → 575 |
| 13945962 | Completed lesson whose exit event returned HTTP 502; recovered history and snapshot | 575 → 576 |
| 13948638 | Already-completed −2 XP attempt; unfinished inequality command input caused the wrong submission | 576 → 577 |

The two existing-answer corrections were committed together at basis 570 → 571.
All correction and import checks preserved the same 4,587 protected learner and
engine facts, SHA-256
`9ba4c0ed1f9e54c3472df2e274ff3c83796cdce9444294fbd192fec181af7ba8`.
Each recovered import verified that reimport is a no-op. The six receipts cover
119 practice-question/canonical-example records, including existing records
completed with additional content. Recovered knowledge snapshots are explicitly
marked as recovered; changes after an interrupted snapshot are not attributable
solely to that earlier activity.

The actual Incorrect grade for q-276257 is retained. Its content was finalized
from the official solution, which confirms x≤9 and y≥0. The completed activity
card independently confirmed task 13948638 earned −2/15 XP. No question was
resubmitted. A later all-correct retake, task 13949104, was already captured and
imported; its cleared retake obligation remains cleared.

For q-113533, two radio options are equivalent indefinite integrals because K
is arbitrary and positive. The saved decision uses the mathematically correct
K-multiplier option matching canonical example e-450. The source ambiguity and
original uncertain answer are preserved in its recovery audit. No website
submission was made during this recovery work.

Task 13947838 stopped before capturing any question and is no longer offered.
Its topic 207 was later successfully captured and imported under lesson task
13947864 (20 questions/examples). The old checkpoint is retained as evidence;
it does not need replay and does not prevent selection of other eligible tasks.

## Resume

Run from `/home/jake/Developer/Course_Academy`. These are the five currently offered
saved lessons, ordered by their latest queue capture priorities:

```bash
for task in 13948864 13948072 13949542 13947866 13948006; do
  /home/jake/Developer/MA/.venv/bin/python scripts/question_capture run --headless \
    --resume "reference/mathacademy/question-capture/$task" --limit 1 || break
done
```

Then continue normal queue processing:

```bash
/home/jake/Developer/MA/.venv/bin/python scripts/question_capture run --headless
```

No default activity limit is imposed. Capacity retries can still exhaust if the
selected model remains unavailable; that external condition requires a later
explicit resume. The heartbeat remains paused and no live-answering batch was
launched during this repair.

## Verification

The full offline suite ran 184 tests. Its only failure was an existing assertion
hard-coded to expect 44 normalizer regression tests; the expanded set now has 46.
That assertion now counts the actual policy and reconciliation tests, and its
targeted rerun passed. Eight focused runner/retake checks and the added native
failed-completion check also passed after the final completion-policy changes.
Native editor checks confirmed completed inequality commands, rejection of
unfinished commands, powered-log grouping, and existing fraction/symbol entry.
The five explicit resume arguments resolve to the intended saved directories.
