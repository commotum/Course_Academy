# Course-independent assessment eligibility

Implemented and deployed after the user accepted the timing findings and explicitly requested that assessments have no course restriction.

Ordinary assessment preparation now considers every explicitly learned topic in the learner's activity history, with a provisional 48-hour floor measured from recorded successful learning. A prior retrieval event is no longer required. Reviews do not restart the learning-age clock. The existing finalized-practice-XP cadence, previously-assessed preference, fresh-question checks, database difficulty weights, and provisional question-time budget remain in use. No course preference is applied.

Prepared assessments use the title “Practice assessment” and omit `activity/course`. Existing pending assessments remain available across course switches even if their definitions carry an old course reference. Assessment scheduling and availability also work in self-directed mode. Existing reserved routes are preserved rather than rewritten.

Assessment misses can prepare immediate reviews outside the selected course and in self-directed mode. Ordinary spaced-review timing remains independent of the assessment maturity check, with its existing course/mode scope. This change does not implement mandatory-remediation gating or retake scheduling. Those remain the separate planned lifecycle: required successful remediation followed immediately by an optional retake, without another two-day wait.

Changed code: `engine/rust/retrieval.rs`, `scripts/learning_api.rs`, engine documentation, and retrieval tests. No schema additions, weight updates, or historical backfill transactions were made for this change. The existing first-successful-learning age anchor remains; the report's uncertainty about resetting that clock after relearning is unresolved.

Validation: **108 engine unit tests passed; 47 native API tests passed; two optional live tests ignored.** New checks cover admission immediately below and at 48 hours, topics with no review history, identical selections across different course contexts, self-directed mode, recent reviews without age resets, ordinary reviews before 48 hours, immediate cross-course miss reviews, and starting the same legacy-course-linked assessment after course/mode changes without duplicate preparation or route changes.

The app service was restarted with the tested production binary. Both learner and home endpoints returned HTTP 200 at basis 1194; the new worker path and results are retained in [verification.json](verification.json). No capture runners were started or restarted. The evidence motivating the change is in [timed-delay-report.md](../../../timed-delay-report.md).
