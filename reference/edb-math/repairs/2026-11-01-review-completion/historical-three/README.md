# Historical local review correction (speculative)

This bundle corrects three controller-owned five-question reviews that the old three-in-a-row implementation marked failed. The current user policy is: answer at least three; finish early when the latest two are correct; completion after all five is successful regardless of correctness.

The correction preserves every actual question observation, recorded accuracy evidence, XP award, and original finish time. In particular, the CICCI review retains all five observations and XP earned 0. The separately corrected dy/dx review is excluded.

Target local review tasks and original terminal transactions:

| Task | Outcome sequence | Original terminal T | Original finish (Unix milliseconds) |
| --- | --- | --- | --- |
| 17592186639386 | CCICC | 4994 | 1792470303033 |
| 17592186654853 | CCICC | 5010 | 1792470875797 |
| 17592186653076 | CICCI | 5047 | 1792473017885 |

The retention calculation starts from each historical db-before and replays the original terminal event as successful, then all later events affecting its complete retention closure. An unchanged control replay must reproduce every original recorded result and current retention. The October 20 failure baseline uses the controller's historical zero failed-review refresh; the corrected pass uses canonical credit without that failure refresh. Subsequent credits use original observed answers, original event times, historical factual snapshots, and canonical credit functions. No answers are regraded.

The five progress rows are disjoint between these three corrections. The final helper rechecks every captured factual progress field against a fresh captured value, adds CAS guards for all unchanged factual fields and task/item observations, changes failed status to completed, and stores the original finish time explicitly. Progress and task entity predicates execute in a native speculative preview with the application's real callback registry. The preview must equal canonical desired progress and may change only retention fields, the three outcomes and their explicit original finish attributes, plus the speculative transaction instant.

`transaction.edn` is exact intended logical data; `ready.json` contains its stable request key, explicit source, captured basis, original dates/XP, guards, and preview datoms. `native-preview.json` is speculative and is not a durable transaction receipt. `replay-report.json` and per-task replay traces contain source journal paths and verified control results. Parent must submit the exact saved EDN under the saved request key/source and compare the captured basis; a stale basis must not be silently recomputed under the same key.

No durable database writes are performed by the audit or final-batch helper.
