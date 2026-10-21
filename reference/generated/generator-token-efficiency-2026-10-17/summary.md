# Generator token and retry audit

Local session logs showed repeated failures from system Node 18 with Playwright
requiring Node 20+, broad repository searches, and large report dumps. The shared
renderer now checks and selects the existing compatible runtime automatically.
Two actual-UI cases passed with PATH restricted to the old system environment;
the saved screenshot was visually inspected.

Malformed reviewer reports previously entered author repair. They now receive one
bounded correction by the reviewer, preserving the generator and sampled batch.
A second invalid report stops the job with its workspace retained. Changed
candidate bytes still require repair and cannot bypass approval.

Revisions receive prior independent review paths only when source and policy
match. Prompts direct agents to reuse those scripts, verify the current candidate,
use bounded output and targeted reads, record brief resumption state at completed
milestones, and stop after required checks pass. Plot documents are conditional
on diagrams; document paths are explicit. All eight acceptance checks remain
required, and existing approvals retain their current policy version.

Completed structured agent results were already cached; a new regression verifies
that reuse launches no agent. Existing job/workspace recovery, bounded author
attempts, per-KP exclusion, and approval-based agent-free refills remain in place.

Validation: 32 pipeline, 4 renderer-runtime, and 9 review-validation tests passed
(45 total), plus two actual-UI rendering cases. Running pipelines were preserved;
the retry changes load when the next pipeline starts, while updated prompt files
and the renderer are used on their next invocation. No service restart was needed.

[Audit evidence](audit.json) · [Renderer verification](renderer-smoke.json)
