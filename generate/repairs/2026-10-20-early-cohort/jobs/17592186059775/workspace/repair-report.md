# Current repair result — author-255

The exact latest failure is in the installed runner's unchanged-package gate,
before regression execution or sampling. The evidence-only finding requires
preserving the repaired runtime. No runtime change is justified.

Fresh evidence validation and negative controls pass. The exact shortcut batch
passes before and after shared delivery; all five answer roles and 25 native
grading responses pass. All runtime hashes remain unchanged. The strict handoff
regression still exits 1, so this is not a completed repair.

Commands and results: `evidence/author255-verification.json`.
The existing root-cause patch `runner-fix/evidence-only-rejection.patch` remains
staged and uninstalled: applying it changes `scripts/generator_pipeline.py`
outside the authorized workspace. No database, publication, runner, or other-job
files were changed.
