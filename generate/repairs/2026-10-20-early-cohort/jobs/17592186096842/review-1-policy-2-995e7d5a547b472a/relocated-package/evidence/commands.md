# Reproduction and current-package checks

Run from this workspace. `PY=/home/jake/Developer/Course_Academy/.venv/bin/python`.

1. `"$PY" -B checks/shortcut_probe.py ../samples.json` — before repair, exit 1;
   1/1 applicable radio leaked the answer. Output: checks/shortcut-..-samples.json.
2. `"$PY" -B checks/regression.py > evidence/regression.log 2>&1` — exit 0.
   Invokes the current `generator.py --difficulty easy --seed 3173462200 --count 5
   --format json` with COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=evidence/assets;
   retains prospective-batch.json; tests exact a=7,b=37,t=-4,seed=3173462203;
   tests 20 seeds for each of eight affected radio layouts (160 records).
   Calls shared check_delivery.py with explicit current-batch inputs for all bands
   and the requested batch; writes logs and accepted records under evidence.
3. `"$PY" -B checks/validate.py > evidence/validation.log 2>&1` — exit 0;
   complete source replay, independent visible-prompt differentiation, controlled
   target/bank changes, relocated CLI determinism, dependencies; grader input.
4. `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine
   evidence/grader-input.json evidence/grader-results.json > evidence/grader.log 2>&1`
   — exit 0, 207 accepted and 709 rejected as expected.
5. `"$PY" -B checks/cues.py > evidence/cues.log 2>&1` — per-template cues and
   refreshed inventory eligibility. Output: cue-results.json, inventory-status.json.
6. `python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py
   --input evidence/render-records.json --output evidence/render
   --asset-root evidence/assets > evidence/render.log 2>&1` — exit 0, 3/3 passed;
   all three PNGs visually inspected (visual-inspection.json).

All shell commands above stay within the workspace for writes. No database,
publication, network service, or other-job mutation is involved. No assets are
required by this generator; evidence/assets is the explicit empty output directory.
7. `"$PY" -B checks/selection.py` — exit 0; five delivered candidates reachable
   in a disclosed positive-easy-weight scenario. Future entity ordering, policy
   weights and learner exposure are not available; see selection-results.json.
