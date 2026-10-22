# Proposed runner correction

`evidence-only-rejection.patch` targets `scripts/generator_pipeline.py`; it has
not been installed. The generator and manifest are unchanged.

The current runner rejects an unchanged package even when its latest independent
review requests only an evidence-path correction. Returning unsupported then
restarts authoring. The proposed patch allows that candidate through the sample
gate only if the complete previous review binding matches and a valid revise
report has exclusively evidence findings. Retained regressions and sampling still
run, followed by a fresh independent review. It never consumes the copied
historical acceptance as new approval. Other findings retain the existing gate.

From this workspace:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_runner_handoff.py
```

This reproduces the original rejection, applies the distributable patch in a
temporary checkout, and exercises the actual original/patched sample-stage
control flow against the captured job and independent report. It covers 23 cases,
including content and mixed findings, invalid reports, every binding component,
failed regressions, refill and post-publication exclusion. Sampling, persistence
and external-service boundaries are instrumented; actual generator, delivery and
native grading checks are run separately by the registered regressions.

The runner owner can review the patch and `patch.json` base hash, then apply the
patch from the repository root with `git apply <absolute-path-to-this-patch>`.
Resume the ready author result through sample and fresh independent review. No
historical evidence installation is needed for that route. Applying this patch
requires a write outside the authorized workspace and was not attempted here.

Evidence: `../evidence/runner-handoff-regression.json` and
`../evidence/author31-handoff.log`. The original gate remains reproduced in
`../evidence/author31-boundary.log`.
