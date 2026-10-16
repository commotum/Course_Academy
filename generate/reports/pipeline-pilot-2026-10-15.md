# Generator pipeline pilot — 2026-10-15

The inventory worker now runs the restartable generate → independent validation → prepare → push pipeline. The learning service was restarted after the previous worker drained, its handoff lock was released, and a new inventory job was observed launching `scripts/generator_pipeline.py`.

## Live publication

| Knowledge point | New questions | Commit basis | Archived runtime files | Independent review |
| --- | ---: | --- | ---: | --- |
| 17592186096841 — polynomial chain rule | 2 | 2776 → 2777 | 4 | All seven checks passed |
| 17592186096814 — unit vectors from diagrams | 2 | 2789 → 2790 | 5 | All seven checks passed after repair |

Both immutable packages are registered under `generators/<prefix>/<sha256>/generator.py` beneath `/media/jake/SSD/EDB/math`, beside the existing `images` store. The diagram batch references four canonical image files; all four filenames match the SHA-256 of their bytes. Author/reviewer evidence and generated output are excluded from the archived runtime files.

Native EDB previews, guarded commits, receipt validation and readback passed. Existing questions and unrelated learner/engine facts were preserved. Repeating each publication returned its original receipt. Both registered packages ran from fresh relocated copies without an authoring session or further publication.

Evidence:

- [Text pilot state and receipt](../../.local/generation/math/17592186096841-easy/job.json), [independent review](../../.local/generation/math/17592186096841-easy/review-2/result.json).
- [Diagram pilot state and receipt](../../.local/generation/math/17592186096814-easy/job.json), [independent review](../../.local/generation/math/17592186096814-easy/review-3/result.json).

## Reviewer controls and recovery

Actual separate reviewer sessions accepted the correct matrix-entry control, rejected a fixed-target generator for restricted variety, and rejected a diagonal-sum generator for instructional drift. All three had mathematically correct answers and source replay. The drift case also lacked satisfactory rendering evidence; that failure was retained. [Control results](../../.local/generation/reviewer-evaluation/evaluation.json).

The diagram reviewer demonstrated a nested-output-path defect. Automatic author repair fixed the generator guard; integration exposed and fixed the runner's matching output-location error. The final review included actual learning-UI screenshots, native grading, independent arithmetic, source replay, variation and relocation checks.

Forty generator tests and eight inventory tests pass, including injected lost replies, stale guards, failed readback, changed approved artifacts, bounded rejection and interrupted authoring. These failure-injection checks use simulated database responses; the two publications above used live EDB.

This is a small pilot, not a bulk migration of the 411 approved drafts. Normal inventory requests now use the pipeline. Content that cannot pass review stops after the configured attempt limit while other jobs continue. See the [operating guide](../README.md).
