# Closest-point generator package

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186073815.py --difficulty easy --count 2 --seed 1954 --format json
.venv/bin/python generate/scratch/17592186073815/validate.py
.venv/bin/python generate/scratch/17592186073815/replenish.py
```

The generator only writes its local plots. The replenisher selects validated questions against fresh inventory, checks stable identities and source preservation, publishes verified bytes through the existing image store, previews with deployed native specs, and submits through the existing EDB integration. It holds the application api.lock through inventory recheck, basis-guarded submission, exact-basis readback and final inventory. Requests and receipts are retained under reference/replenishment/basis-*/. Interrupted commits recover the same retained request key and exact EDN.

Source difficulty ratings are preserved for generated variants. The package has no validated hard capability; the hard reserve remains explicitly unfilled. Counts beyond finite source-profile translations require new evidence or another validated family. Source questions and learner history are never rewritten. Generated content uses :application/ca-engine, with separate question and field-owned answer UUIDs and no Math Academy content ID.

Read classification.md, extraction.json, template-extraction.md, plot-extraction.md, capabilities.json, source-replay.json, native-grading.json, validation.json and review.json for the evidence and bounded fidelity limits. Metadata records exact dependencies, source basis, parameters, profile and generator version. No scheduler or application changes are part of this package.
