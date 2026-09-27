# Math Academy progress attribution

Reconciled `progress.csv` against the complete history supplied on September 24,
2026. It contains 212 activities through September 20, 2026 at 21:34, sorted
newest first. No activity beyond that supplied history has been checked.

The reconciliation filled 71 previously blank course/course-code pairs and added
one missing activity: **Graphing Curves Defined Parametrically**, August 9,
2026 at 20:04, Precalculus, topic 803, 15/15 XP.

## Meaning of the course fields

- Explicit course labels in the supplied history are preserved. A lesson's
  course can differ from the course the student was enrolled in.
- An unlabeled lesson or review is assigned using the inferred enrollment at
  its completion time, checked against the local MA course catalog.
- Diagnostic activities use the course named in the exam title. An exam does
  not by itself establish a lasting enrollment change.
- Assessments and multistep activities use the inferred enrollment. These 21
  assignments are contextual: their titles are not ordinary catalog topics.
  Their topic IDs remain blank.

All 183 lesson/review activities match both the topic title and topic ID in
their assigned course's `vault/MA` catalog. For the duplicated title **Vertical
Asymptotes of Rational Functions**, the explicit Precalculus label resolves the
topic ID. Diagnostic XP denominators remain blank where none were supplied.

## Inferred enrollment timeline

End times below are exclusive; start times are inclusive. Switch boundaries
use diagnostic completion times as the best available markers, rather than
verified account enrollment timestamps.

| Start | End | Inferred enrollment | Evidence |
| --- | --- | --- | --- |
| 2025-02-27 11:13 | 2026-07-14 20:10 | Mathematical Foundations II (MF2) | Initial 3/3 unlabeled lesson/review events fit MF2. After the MF3 exam, 38/38 unlabeled events fit MF2 and none fit MF3. After the MVC exam, 5/5 fit MF2 and none fit MVC. MF2 supplemental exams support continued MF2 work. |
| 2026-07-14 20:10 | 2026-08-18 16:19 | Calculus II (CA2), probable | CA2 placement followed by 20 CA2 lesson/review events covering 10 topics, alongside prerequisite courses. Quiz 1/retake on August 5, Quiz 2 on August 8, Quiz 3 on August 10. |
| 2026-08-18 16:19 | 2026-09-17 17:05 | Calculus I (CA1), probable | CA1 placement followed by 31 CA1 lesson/review events covering 20 topics, plus two Precalculus lessons. Quiz numbering restarts: Quiz 1 on August 22, Quiz 2 on September 4, Quiz 3 on September 17. |
| 2026-09-17 17:05 | Latest supplied activity | Mathematical Foundations II (MF2) | MF2 placement followed by 22/22 unlabeled lesson/review events fitting MF2, representing 21 distinct topics. |

The complete paste explicitly labels CA2 and CA1 lessons even during their
probable enrollment periods. Therefore, label visibility alone does not prove
historical enrollment. The July/August switches and the contextual quiz and
multistep assignments remain inferences based on diagnostics, topic progression,
and quiz restarts. No sustained switch to MF3 or MVC is supported by the supplied
activity history; their diagnostic rows retain those exam course names.

## Diagnostic dates recovered from the full history

These dates already matched the CSV; none required a date correction.

| Completed at | Exam | XP earned |
| --- | --- | --- |
| 2025-02-27 11:13 | Mathematical Foundations II: Placement Exam | 44 |
| 2025-02-28 13:26 | Mathematical Foundations III: Placement Exam | 21 |
| 2025-07-29 12:28 | Mathematical Foundations II: Supplemental Diagnostic Exam | 3 |
| 2026-01-09 00:35 | Multivariable Calculus: Placement Exam | 0 |
| 2026-04-02 20:22 | Mathematical Foundations II: Supplemental Diagnostic Exam | 4 |
| 2026-07-14 20:10 | Calculus II: Placement Exam | 31 |
| 2026-08-18 16:19 | Calculus I: Placement Exam | 2 |
| 2026-09-17 17:05 | Mathematical Foundations II: Placement Exam | 60 |
