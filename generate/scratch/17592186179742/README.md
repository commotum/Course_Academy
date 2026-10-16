# Qualitative vector-field work signs

Validated generator: `generate/scratch/17592186179742.py`.

Run from repository root with the existing environment:

```sh
MPLCONFIGDIR=/tmp/ca-kp79742-mpl .venv/bin/python generate/scratch/17592186179742.py --difficulty moderate --seed 804742 --output /tmp/work-sign.json
MPLCONFIGDIR=/tmp/ca-kp79742-mpl .venv/bin/python generate/scratch/17592186179742/validate.py
MPLCONFIGDIR=/tmp/ca-kp79742-mpl .venv/bin/python generate/scratch/17592186179742/replenish.py
```

The generator emits review JSON and programmatic PNG assets; it has no database writes. `--replay q-125500` emits an exact source replay marked evidence-only. Validation proves dot-product signs over all 320 bounded parameter cases, compares 13 complete source banks, exercises all supported field/profile combinations with the actual native grader, rejects stale keys/solutions, and retains a visual review. Source fidelity is separate from mathematical correctness of analytic variants.

Easy and moderate are supported. Hard remains a bounded capability exception with an explicit five-question shortage, never marked filled. The analytic sampler has eight easy and four moderate distinct task classes after conservative equivalence grouping; replay-only source families are documented separately. Rotations, aspect-ratio variants within noncircles, scaling and bank changes cannot inflate inventory.

The source capture, source/choice mapping, extraction and plot specification are adjacent files. `reference/generated-review.png` was visually checked for both geometries, signs, traversal directions, readable labels, unclipped bounds and consistent arrows; `reference/display-review.json` records those exact examples. All originals remain immutable.

Publication uses the existing EDB integration, configured `:application/ca-engine` contributor, native schema/spec preview, content-addressed image store, stable generator UUID and repository-relative registration. It holds application api.lock from fresh lineage/basis/inventory reads through submission and exact report-basis readback. Exact EDN requests, UUIDs, source attribution, previews, receipts, assets and verification remain under `reference/replenishment/basis-*/`. Outcome JSON is written to the requested inventory job result path. The receipt rejects unrelated attributes, non-new question entities, retractions or learner-history changes; readback preserves every original source question and canonical example.
