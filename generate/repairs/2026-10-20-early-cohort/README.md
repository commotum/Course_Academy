# Early generator review and repair campaign

Requested on 2026-10-20. The cutoff is **2026-10-16 14:51:26 America/Los_Angeles**, the earliest recorded introduction of decision-variation verification. Current registered generators are the authority; a historical `qa_passed` flag alone does not establish a current review.

The registration/course snapshot is EDB basis **5119**. There are 634 registered generators eligible by their earliest Git build evidence or conservatively included because their age is unknown. An initial certificate scan identified 197 possible current-policy skips and 437 candidates requiring verification, including 61 in Linear Algebra or Differential Equations. All 71 generators in those subjects are processed first; their 10 possible certificate skips are checked cheaply against fresh instructional source identity before launching any session. The rest of the cohort follows. Dates are never inferred from filesystem modification times.

`cohort.json` freezes membership and priority and retains each job's outcome. The worker rechecks current registration, package/source identity and complete policy-2 review evidence before skipping a generator. Changes in question-pool membership do not by themselves invalidate instructional evidence.

Execution uses the existing generator pipeline with three parallel workers and the normal per-KP exclusion locks. Workers claim distinct generators from the frozen priority order under a short shared-state lock; the slow author/review work runs outside that lock. Each slot retains its own lifetime lock and passes both slot and KP locks to its agent process, so recovery cannot duplicate still-running work. A supervisor restarts interrupted slots independently while healthy slots continue. Status includes every active generator in `active_jobs`. Existing archived packages go directly to sampling/review. Legacy scripts first receive a mechanical package preserving code, resources and local imports. A demonstrated packaging, sampling or independent-review failure starts the normal repair author, followed by independent verification. No generator is newly invented merely because it is absent from the registration snapshot. Publication retains the existing guarded request/receipt recovery and immutable packages.

Passing unchanged archived packages receive current review approval through verified unchanged registration, without publishing extra questions. Changed/repackaged runtimes receive their reviewed five-question initial batch. Reviewer evidence includes the required structural-shortcut checks by recognizable template and after delivery filtering, rather than relying on total output uniqueness.

If an independent review demonstrates defects in stored generated questions, the pool repair path requires exact question identities and reproduced generated-record evidence. It marks demonstrated unused, noncanonical, nonsource generated questions retired after a fresh guarded read and native transaction preview. Their KP memberships remain intact. Repair and inventory recapture happen before the final independent review. Question/answer entities and learner history remain. Source questions, previously served questions and unsupported claims are protected. Unresolved source/content/engine issues remain explicitly recorded as needing repair; they are never converted to successful certification.

The running scoped service is `course-academy-generator-cohort-20261020.service`, now backed by a persistent unit installed through `scripts/generator_services.py`. It restarts on unexpected worker-process failure and retains its definition after a clean boundary stop. Automatic inventory builders/refills remain disabled through `COURSE_ACADEMY_DISABLE_GENERATION=1`. The campaign stops if the provider reports a capacity limit instead of retrying that failure across the cohort.

After the 2026-10-21 power outage, the saved campaign had 25 verified generators and one interrupted review. It was resumed from that review. The unit now has `WantedBy=default.target` and is enabled for boot recovery; the existing user service manager already has lingering enabled. `start_cohort` retains this boot enablement on subsequent installs. The active review process was preserved while installing the boot setting.

The initial clean-reload helper failed because systemd unloaded the completed transient worker unit. This stopped the campaign after the first independent review; no campaign repairs had been published. The helper now recreates an unloaded transient unit. The scoped worker was recreated and observed active on 2026-10-20; the first slope-field generator is receiving one bounded additional author attempt for the demonstrated diagram-consensus shortcut, after its earlier three attempts addressed packaging. Previous failed reviews and session launch limits are retained in the job, including `resume-20261020.json`.

Current status:

```bash
.venv/bin/python scripts/generator_cohort.py status \
  --directory generate/repairs/2026-10-20-early-cohort
```

`jobs/<kp>/job.json` records the pipeline stage; `author-*` and `review-*` retain session evidence. `status.json` is updated at job boundaries and by the status command. A `stop-after-current` file requests a clean boundary stop. To resume, remove that file and start the persistent scoped service; `generator_services.start_cohort(directory)` installs its definition if necessary. Completed jobs, exact pending submissions and session launch limits are retained. Author and review budgets persist across restarts. Repeated unchanged failures, permission blockers, and exhausted budgets stop new campaign claims with a visible `campaign_error`; the service exits 78 and does not restart automatically. Report-format errors continue as report correction without reauthoring. Infrastructure interruption preserves the current job for service recovery.

Validation of the campaign machinery: seven cohort tests, three pool-repair tests and all 35 existing generator-pipeline tests passed. These tests establish scheduling, package adoption, publication/retirement guardrails and recovery behavior; individual generator correctness is established by each generator's actual independent review.

On 2026-10-21 the cohort service was upgraded to `--workers 3`. The previous single worker was drained at a saved pipeline boundary before enabling concurrent state writes. `stop-after-current` prevents new claims across all slots and lets current attempts reach a saved boundary. A provider capacity error is shared across workers: no further generators are claimed, while other in-flight work is retained. Clear `capacity_error` under the campaign state lock only when intentionally resuming after capacity becomes available. General creation/refill workers remain disabled.

After resolving a blocker, requeue that one job explicitly, then start the service:

```bash
.venv/bin/python scripts/generator_cohort.py resume \
  --directory generate/repairs/2026-10-20-early-cohort \
  --kp KNOWLEDGE_POINT_ID --resume-reason 'Describe the completed fix'
systemctl --user start course-academy-generator-cohort-20261020.service
```

Report corrections run in the full reviewer evidence root. They do not go through generator authoring or require an artificial runtime change. Historical inventory findings use the runner's guarded retirement path before recapture and fresh review. Database basis changes alone do not trigger another review.
