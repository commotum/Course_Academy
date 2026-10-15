# Parabolic cylinder generator

`../17592186175972.py` generates validated easy and moderate radio questions. The source snapshot is math basis 2275, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1; replenishment rechecks current source records, learner usage and inventory under the application lock.

```bash
.venv/bin/python generate/scratch/17592186175972/validate.py
.venv/bin/python generate/scratch/17592186175972.py --difficulty all --seed 12 --count 5 --format json
.venv/bin/python generate/scratch/17592186175972/replenish.py
```

`generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` supports easy/moderate; `hard` raises an explicit capability exception. Raw profiles ending `_raw` replay source evidence only and cannot enter the inventory. The CLI deduplicates assessed mathematical tasks within each output, including across levels, and fails explicitly on bounded exhaustion. Replenishment also excludes existing source/canonical/generated tasks and checks actual grading.

All six sources, seven banks and 35 choices replay exactly, with missing source keys preserved. Normal output documents repairs: a duplicate field is removed, missing metadata is completed, and the free-coordinate copy convention is explicit. The opaque q103986 half-linear member is retained in raw evidence; its normal complete bank is separately labeled authored. No source or learner record is repaired by this task.

Hard remains unsupported. Its uncalibrated normalization proposal is retained only as draft analysis and inaccessible through public generation. Nominal hard reserve remains five unfilled. Easy/moderate capacities overlap: 69 and 66 tasks, 69 globally; coefficient or bank changes do not multiply the three free-coordinate copy tasks.

`replenish.py` uses the configured EDB integration and contributor, retains exact requests/receipts under `reference/replenishment`, acquires `.local/learning/requests/math/api.lock`, checks the basis, previews native specs, and holds the lock through commit and exact-basis readback. Only additive content and this KP's generator registration are allowed. See the job result and verification for the final committed counts.
