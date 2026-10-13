# Mathematical Foundations I progress discrepancy

Draft for Math Academy support. Not sent.

Student ID: **57975**. Course ID: **113**, Mathematical Foundations I.

The account's Learn page repeatedly alternated between its gradually increasing completion percentage and 98–99%, without a new placement test or enrollment change between those readings. Its most recent MF1 placement exam completed October 11, 2026, approximately 7:09 PM Pacific.

On October 12, 2026:

| Pacific time | Displayed completion | MF1 topic colors |
|---|---|---|
| 4:44 PM | 29% | 251 of 357 topics white |
| 4:53 PM | 98% | 356 of 357 topics in the darkest blue |
| 4:59 PM | 30% | Pending new lesson topics returned to white |

Two ordinary lessons completed between the first two readings. Both dashboards identify the same student and course. The high-percentage state also shows an MF2 sequence tab at 79%; its presence alone does not establish an error.

The available activity queue largely persists across these changes. For example, Interpreting Additive Opposites and Addition Using Absolute Value, Rational Numbers as Finite or Repeating Decimals, and Reasoning With Equivalent Ratios remain offered as new lessons with Start links and green prerequisite checks, while their corresponding course-progress circles alternate between white and the darkest blue. Remaining XP stayed at 5,982 in the compared snapshots.

Please clarify which progress/knowledge view is authoritative and investigate the inconsistent readings. In particular, check whether current diagnostic placement and earlier assumed prerequisite mastery are being mixed, or whether a course/placement context is missing from a cache key. These possible causes are hypotheses, not established findings. Preserve the student's enrollment, placement results, completed activities, and XP while investigating.

Evidence:

- [29% Learn snapshot](/home/jake/Developer/Course_Academy/reference/mathacademy/capture/linear/14152753/post-activity/1791848660706049314/dashboard-68131310f179214e12bb.html)
- [98% Learn snapshot](/home/jake/Developer/Course_Academy/reference/mathacademy/capture/linear/14153000/post-activity/1791849209777620520/dashboard-51b2a79e50bac1f065a1.html)
- [29% state, MF1 topic progress](/home/jake/Developer/Course_Academy/reference/mathacademy/capture/linear/14152753/post-activity/1791848660706049314/course-113-51c4808f9da9bf1d718e.html)
- [98% state, MF1 topic progress](/home/jake/Developer/Course_Academy/reference/mathacademy/capture/linear/14153000/post-activity/1791849209777620520/course-113-8e7e78877c8a7d831663.html)

Later instrumented reads retain original HTTP bodies independently of rendered DOM. The recent saved readings have been stable at 48–49%, with matching server and DOM percentages; this does not explain or invalidate the earlier oscillation. Raw bodies and allowlisted Date/ETag/cache headers are under `reference/mathacademy/capture/linear/browser-originals/`. Authentication headers are excluded.
