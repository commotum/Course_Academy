All commands run from the supplied workspace. Runtime files were unchanged after validation. No services or database were contacted.

Exact reviewer counterexample, before repair (failed with the reported assertion) and after repair (passed):
```
/home/jake/Developer/Course_Academy/.venv/bin/python evidence/shortcut_regression.py
```
Original failure: reproduction.log, before-minimal.json, before-minimal-results.json. Current result: minimal-failure.json, minimal-failure-results.json. The copied reviewer predictor is unchanged; audit.py retains its independent visible-record math helpers with paths redirected into this workspace.

Source replay, mathematical checks, controlled bank/target counterfactuals, fresh sampling, inventory inspection, dependency/relocation, and retained regression:
```
/home/jake/Developer/Course_Academy/.venv/bin/python evidence/check_repair.py
```
Result: 10 source questions, 11 banks, 182 math/solution checks, nine banks each supporting five different correct choices, 108 normal samples. Old five-question batch regenerated from its original seeds/profiles in repaired-batch.json. Native cases include every choice, not just declared keys.

```
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --asset-root evidence --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python evidence/check_repair.py evidence/delivery/accepted.json
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-input.json --output evidence/render --asset-root evidence --math-root /media/jake/SSD/EDB/math
```
Results: native grader 182 accepted/728 rejected; delivery 171/171 accepted, zero duplicates; all nine fixed-bank families retained; five UI renders passed and screenshots visually inspected. Full reports are alongside this file.

The repeated source banks are preserved for original source replay. Runtime banks keep the complete observed shapes while allowing all five operation pairs to be correct. Conditional on a bank, the normal sampler selects each role uniformly before matrix data. Controlled cases show that signs, magnitudes, frequencies, profile, or option order cannot determine the correct pair without relevant matrix evidence. In the natural sample the exact reviewer predictor is correct on 8 of 52 applicable cases (five-choice baseline 20%). No arbitrary balance quota was imposed.
