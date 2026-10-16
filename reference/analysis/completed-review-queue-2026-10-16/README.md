# Completed review left a queued topic blue

Topic 17592186048749 is Differentiating Exponential Functions (MA 1114). Queue history records its addition on 2026-10-13 UTC and no subsequent removal. Its lesson had already completed before that addition. Review task 17592186480004 completed at 2026-10-16T22:41:39.362Z, but queue cleanup existed only in lesson credit. Graph blue correctly reflected the retained learner/queue membership.

Successful review completion now retracts the reviewed topic from learner/queue in the same completion transaction. Failed reviews, partial answers, assessments, targets, and other queued topics are preserved. The lesson player broadcasts queue invalidation for successful review completion as well as lessons.

The data repair retracts only this topic's stale queue membership, guarded by the completed review status. Native preview and committed receipt each show one domain datom retraction. Readback verifies the other 35 queue topics, targets, and review task are unchanged. No XP, progress, mastery, or activity history attributes changed.

Credit tests cover lesson and review success/failure/partial completion, unrelated queued topics and targets, and assessment exclusion. UI tests cover completion notifications and graph queue/color handling.
