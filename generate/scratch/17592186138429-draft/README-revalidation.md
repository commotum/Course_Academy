# Word Problems revalidation draft

Owned candidate: `../17592186138429-draft.py`. Numeric registered script and entire tree are immutable. `registered-baseline.json` captures all 390 registered files and directory names before imports. All generation, rendering and validation runs import only the draft.

The registered script changed from independently reviewed SHA `2e9ce23fc0d78f8a45d6d0a53a4b394edcb751736ee5992d1b9e66396376288a` to `25416a41c2ca43b74da65b311f5ab7eba34b55a8a433fd4cbba04a270c717058`. The retained prior baseline implements original trucks/pools/cars. Current registered code dispatches added `planes`/`tanks` templates into extensions.py, adds their renderer revision, and reports version5. Existing refreshed validation already matched those source prompts, banks, solutions and native blank equivalents. This draft preserves that work; only ownership isolation, blank Markdown presentation, fresh source handling and the newly uncovered two-blank walkers template are substantive changes.

Fresh source basis2275: five MA practice originals (18 canonical answer values,12 distractors,6 fields), one canonical example, thirteen generated inventory records. `source.json` is byte-exact refresh; `source-cases.json` lists only original MA IDs; `independent-inventory.json` contains only the thirteen nonMA records. Existing1356 validation is retained separately and rerun in this draft. Source errors and repairs remain distinct; raw originals are never relabeled generated inventory.

Run from repository root:

```
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186138429-draft/validate.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186138429-draft/revalidate.py
.venv/bin/python generate/scratch/17592186138429-draft.py --difficulty easy --template walkers --seed 3 --format markdown
```

The native grader binary is frozen at `check-engine-frozen`, copied from the supplied in-memory checker. No EDB access, database writes, registration, replenishment, or commits are part of this draft. `revalidation.json`, engine inputs/report, sampled JSON and rendered Markdown are concrete evidence for root review. Historical reports copied from the numeric tree are historical; final review status is awaiting independent root review.

Limits: exact source distractor intentions remain unknown; optional scalar profiles reproduce complete observed banks, default banks use a complete adjacent-grid profile. The original truck's narrow source window cannot support the authored adjacent-grid bank at the original t=6 (8h lies beyond7h); its observed bank remains valid and replayed, while bank-independent fingerprint comparison extends the window to9h. Original valid forms remain available. No normal valid form is pruned, no rating is inferred for historical unrated sources, and no infinite bank claim is made.

Parent integration activates all four supported easy contexts in ordinary sampling (trucks, planes, tanks and walkers), preserves explicit template replay, rejects non-integer seeds/counts, and deduplicates batches by mathematical/contextual task. Current source metadata is basis2275; original source capture bases remain in evidence. Default bounded M/H capacities are22/24; batch limit100 also applies.
