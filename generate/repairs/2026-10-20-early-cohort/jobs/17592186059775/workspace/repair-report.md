# Current repair result — author-260

The installed runner rejects unchanged runtime bytes before regressions or
sampling. Reproduced this exact failure first, then ran all retained checks.
Generator, source replay, independent math, counterfactual, delivery, shortcut,
native grading and inventory checks pass. Corrected evidence validates, but its
registered strict handoff test exits 1. UI binding and visual reinspection pass.

Commands and results: evidence/author260-regressions.json.
The source-supported runtime and completed repairs are unchanged.

The existing root-cause patch runner-fix/evidence-only-rejection.patch remains
staged, uninstalled. Applying it changes scripts/generator_pipeline.py, outside
the authorized workspace. No database, publication, runner or other-job writes
were performed. A fresh independent review is required after that fix.
