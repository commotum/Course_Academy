# Validation report

Private draft at math basis2275. Validator passed under Python 3.13.5 and SymPy 1.14.0.

- Source fidelity: 6/6 original prompts, 5/5 present full worked solutions, 6/6 complete banks, 35/35 options, 15/15 existing correct designations, exact missing-attribute presence parity.
- Generated actual-display checks: 2160 sampled questions across all six families and all three levels, plus 469 exhaustive finite component instances covering obstruction locations, diagonal one/nonone masks and rectangular shapes.
- Native memory-only grading: 121 accepted correct choices, 142 rejected wrong choices, zero unresolved checks; every displayed option tested on original keyed banks and the selected variant banks.
- All seven corruption regressions rejected (missing operative stage, wrong witness, wrong key, control character, stale conclusion, displayed workload, equivalent bank choices). Explicit cross-level workload rejection: 72 checks. Default sampling covers all six families at each level.
- Source zero/identity/diagonal overlaps and 1×1 boundaries verified mathematically and through public generated fields; a changed witness at fixed entries changes content identity and leaves task identity unchanged.
- Meaningful sampled task counts easy/moderate/hard: {'easy': 621, 'moderate': 618, 'hard': 628}. Finite per-template capacities and actual slot coverage are in validation.json. These counts exclude seeds, labels, banks, nonzero magnitudes, irrelevant diagonal scalars and rectangular entries. Per-template capacities must not be summed as a deduplicated cross-template total.
- Registered numeric script and every numeric evidence file are unchanged, with exact file-set and SHA256 parity against baseline-hashes.json.

q-7829 remains raw evidence without its missing original grade, key or worked solution, and is ineligible for learning. The method profile infers D-only and provides a separately authored fixed solution. Inference does not count as original designation fidelity. Only easy difficulty is observed; authored moderate/hard workload calibration remains uncertain. No human/native UI raster review is claimed. Parent independent QA is pending.

Draft script SHA256: `b9352b1150e24fa8d59e0fc63c0295a118bdb90d3b661dc431352cbdfc0e6e91`.
Registered numeric script SHA256: `317b60b8bc389fd1ca7d64570c916e094e134c23bf41fc9c2695b895800b5939`.

Verification command:

```bash
.venv/bin/python generate/scratch/17592186087697-draft/validate.py
```
