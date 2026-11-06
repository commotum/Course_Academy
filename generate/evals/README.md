# Offline instructional checks

`intent-cases.json` freezes eight mechanisms from the repair research and three
held-out analogues. It records the required learner work, defective construction
and legitimate neighboring cases. These are evaluation controls, not database
records or published practice.

Run the bounded live semantic review:

```sh
.venv/bin/python generate/evals/run_semantic_controls.py /tmp/generator-semantic-eval
```

This uses the configured Codex login and the production principles/reviewer
instructions. A first, source-only turn establishes the learner work; a second
turn sees shuffled candidate designs and the graph images. Expected verdicts are
withheld. Inspect the actual reasoning and image-viewing evidence, not merely the
summary's matching count. This checks semantic judgment; it does not run a full
generator, native grading or the application player for each candidate.

Run the full production sequence on the synthetic matrix-entry source:

```sh
.venv/bin/python generate/evals/run_offline_pipeline.py \
  --directory /tmp/generator-live-pipeline --seed 60419
```

The adapter supplies fixed local source/inventory captures and refuses database
operations. Actual production agents must complete source accounts, exemplar
grading/rendering and independent acceptance, generator construction, and final
three-band verification. It stops at `prepare`, before package publication or
database preparation. It supplies no fake agent reports or grading evidence.

Keep the same directory and seed when resuming an interruption. If an external
implementation change legitimately consumes the saved retry allowance, use the
production `--resume-reason` mechanism and retain that reason. Do not reset saved
counters, replace failed samples, fabricate reports or hide failed runs. Freeze
production inputs before starting a new evaluation to avoid needless invalidation.

These bounded controls and the mechanical regression tests support specific
claims. They do not empirically calibrate difficulty or estimate a universal
generation success rate. The November 5 closure report records the actual runs,
corrections, results and limits.
