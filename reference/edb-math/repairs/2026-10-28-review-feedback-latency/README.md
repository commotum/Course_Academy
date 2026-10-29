# Immediate review feedback and background persistence

Ordinary review Answer, Next, Skip, Pause, and Resume requests are acknowledged after an atomic, fsynced local outbox write. A dedicated read-only native peer supplies grading, question cards, and the engine's actual review stopping and XP decisions. A separate persistence peer replays acknowledged commands in order through the existing guarded learner transaction and exact-request receipt path. Another native peer handles the scheduler, so queue calculations do not hold the answer worker.

The learner can answer later questions and complete a review before any queued database save finishes. Reloads recover the locally acknowledged view. Replaying an uncertain save retains the exact database request identity; only a confirmed basis rejection receives a new write key. Permanent save errors retain all accepted work, stop further admission, and expose Retry saving. Transient outages automatically retry. A small Saving indicator clears when the queue drains and refreshes progress statistics.

Working intervals are captured when the server acknowledges learner interactions and are stored as task-item component records. Timing and daily statistics use these observed intervals rather than delayed commit timestamps. The four added attributes and exact schema receipt/readback are under `schema/`. Activity changes first pause and drain tracked reviews; native pause/resume also preserves existing interval clocks. Existing presentations, grades, and time history are retained.

Assessments and adaptive lessons retain their existing submission flow. The fast path is scoped to ordinary reserved five-question reviews, including their normal early stopping rules. Completed, fully saved history is read from the authoritative database. The generation pipeline remains enabled with its configured six build workers.

Verification:

- `tests/test_review_outbox.py`: blocked database writer permits feedback, Next, and a subsequent answer; restart/lost acknowledgement recovery; exact retry identity; confirmed conflict handling; pause/resume; activity switching; errors; assessment isolation.
- `tests/test_page_read_admission.py`: fast review feedback bypasses a held scheduler admission lock and never uses the slow answer/save workers on the request path.
- Native API tests: delayed actual in-memory EDB transactions preserve grading, the three-correct review stop, question order, 1.2 seconds of observed work despite much later commits, pause/resume, midnight statistics, and assessment answer secrecy. Full API suite: 98 passed, 7 existing ignored tests.
- `tests/review-async-browser.py`: actual renderer, controls, HTTP admission and outbox with native-generated multiple-choice fixtures. With both database persistence and scheduler admission blocked, all three answers and Next steps finish, the completion page survives reload, and six background operations subsequently save in order. See `browser-verification.json` and `review-before-background-save.png`. MathJax is stubbed in this latency test; native mathematics and grading are separately tested.
- `live-readonly-verification.json`: warmed native grading on a previously submitted live review question, without submitting another response or changing learner data. Study HTTP availability also checked.

The browser test records approximately 60–80 ms from click to feedback/next view while database persistence is deliberately blocked. The live read-only grading check records sub-millisecond warmed native requests. These are measured local checks, not a guarantee about remote network latency.
