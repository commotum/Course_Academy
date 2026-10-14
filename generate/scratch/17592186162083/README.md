# Validated arc-length invariance generator

Entry point: `generate/scratch/17592186162083.py`.

```sh
.venv/bin/python generate/scratch/17592186162083.py --difficulty moderate --count 2 --seed 13 --format json
.venv/bin/python generate/scratch/17592186162083/validate.py
.venv/bin/python generate/scratch/17592186162083/replenish.py
```

Moderate and hard are supported. Easy and legacy unrated entries remain explicit
capability exceptions. The bounded policy contains 113 moderate and 145 hard
geometries before existing-source exclusion. These are finite limits, not claims
of unlimited generation; current source and generated geometries are subtracted
at every replenishment. Different parameter speeds or supplied integral values
on an existing geometry cannot fill a reserve. Original identities are retained.

Validation is in `validation.json`: all five original prompt/solution replays
are exact, 15/15 complete banks and 30/30 values match; independent displayed
mathematics and actual application grading pass across every bounded case.
`review.md` places original and boundary variants next to each other. Reviewed
curve expressions, statement labels, solution claims and formatting agree;
there are no plots or asset publication steps. Source text retains the original
operator notation and mathematical layout. The frozen generator hash is recorded
in validation evidence and checked again before any preparation.

The replenisher reuses the existing EDB integration and configured application
contributor. It acquires `api.lock`, captures current inventory/basis, checks the
lineage and unchanged source evidence, validates supplied instances if present,
excludes existing geometries, checks UUID collisions and generator identities,
and requests installed native content specs in preview and commit. It retains
exact EDN, guarded requests, previews, receipts and exact-basis readback in
`reference/replenishment/`. Every datom must be additive and limited to the
requested KP and new content. Old question records, canonical example and
learner history are preserved. The stable generator UUID and repository-relative
path are registered through the existing generator schema. Saved unknown request
outcomes are recovered before another intent is prepared. Repeat preparation
must produce no content changes. Native inventory is rechecked after readback.
