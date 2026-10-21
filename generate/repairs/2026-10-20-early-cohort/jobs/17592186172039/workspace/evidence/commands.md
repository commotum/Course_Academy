# Reproducible commands and final results

Run from the workspace with the supplied job interpreter. These commands are offline and write evidence only. `validate_repair.py` sets its plot output directory to `evidence/assets`. Runtime files are declared separately in package.json.

```sh
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
$PY checks/runtime_closure.py
$PY checks/validate_repair.py
$REPO/generate/runs/current/check-engine evidence/native-input.json evidence/native-report.json
for band in easy moderate hard; do
  $PY $REPO/generate/pipeline/check_delivery.py --input evidence/records-$band.json --source ../source/source.json --inventory ../source/inventory.json --difficulty $band --output evidence/delivery-$band --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
done
$PY checks/decision_variation.py
COURSE_ACADEMY_GENERATOR_OUTPUT_DIR="$PWD/evidence/assets" $PY 17592186172039.py --difficulty moderate --count 5 --seed 0 --format json > evidence/samples.json
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-samples --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

Results:

- Original feedback reproduced in isolation: relocated entrypoint failed with StopIteration searching for repository scripts/generator_policy.py. `before-relocation.json` saves the traceback. Final relocation uses only the four declared runtime files, produces five deterministic records in every supported band, cold-renders four sign maps, and changes no runtime files.
- Source fidelity: eight prompts and complete banks; 54/54 boolean values. Seven exact worked solutions, one wording/math-exact compact solution with source bare math corrected to inline TeX. Source difficulty metadata is retained in validation evidence, including unrated q-97483.
- Independent correctness: 218 records, 108 semantic instances. Signs follow the global quadrant substitution x=sx*u,y=sy*v for u,v>0. Visible expressions, statement labels, answer values, solution comparisons and diagram sign specifications agree. Invalid zero coefficients, out-of-range coefficients, unsupported powers, repeated quadrants and invalid claims are rejected.
- Native learner grading: 783 accepted and 783 rejected responses, zero unresolved. Includes every source boolean choice, coefficient sign counterfactuals, changed quadrant targets, and positive coefficient rescaling.
- Delivery: easy 28→28, moderate 66→32, hard 124→76. All 108 semantic instances and all eight truth subsets in each surviving visible family remain. Duplicated solution-layout variants do not constitute distinct pre-answer prompts. Five-item default runner sample: 5→5.
- Variation: each implementation template and supported exponent pair has all eight truth subsets before filtering. Visible fraction/exponent families retain all eight after filtering. Every position can be true or false, ordinary correct counts range 0..3, fixed equation/quadrant cues do not determine the subset, and exact claim-label reversals are witnessed. Constant subset strategy succeeds on 1/8 of distinct controlled cases; constant ordinary count on at most 3/8. Relevant sign/claim/target changes alter expected answers and grading; positive rescaling preserves them. Magnitude, UUIDs, order and seeds do not count as semantic instances.
- Actual UI: six representative screenshots passed MathJax, fonts, image decoding and JavaScript checks. All screenshots were visually inspected for legibility, sign maps, complete labels, and unobstructed options; the updated compact solution screenshot was inspected again after math delimiter repair.
- Captured inventory: all 16 equations and boolean keys checked, no mathematical key mismatch. One stored item has all ordinary fields false and no None. `checks/reproduce_inventory.py` executes the retained historical definition with seed 3504342439 and parameters c=-6,a=1,b=0,quadrants=[1,3,2],claims=[1,-1,-1]; its generation metadata and migrated storage question match exactly. The current generator's same-parameter case offers None keyed true. No stored item was modified.

Limits: this is a bounded, source-supported sign/parity skill. Tests cover representative semantic instances, not all 320 possible unordered tasks. Live learner history, configured difficulty weights, identity collisions, and future inventory changes are not simulated. No engine limitation was demonstrated. There were no finding IDs in the supplied repair history; the feedback and newly demonstrated inventory case have separate executable checks rather than invented history IDs.

Input binding: the job-context source/inventory hash strings differ from the current supplied files' byte and canonical-JSON digests. No source or inventory file was modified. `final-report.json` records the observed byte hashes and supplied binding values; validation and delivery use the actual basis-5384 files. Independent review must establish a fresh binding. The historical import failure remains reproduced in before-relocation.json and passes with the repaired current runtime.
