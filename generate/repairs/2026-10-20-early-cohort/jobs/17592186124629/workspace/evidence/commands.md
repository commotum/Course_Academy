# Reproduction and verification

Run in the supplied workspace. `PY` below means `/home/jake/Developer/Course_Academy/.venv/bin/python`; `REPO` means `/home/jake/Developer/Course_Academy`; `JOB` means `$REPO/generate/repairs/2026-10-20-early-cohort/jobs/17592186124629`. These are command abbreviations, not runtime dependencies.

1. Initial failure: copy the original entrypoint and its source.json into an isolated temporary directory, then run `PY -I <copy>/17592186124629.py --difficulty moderate --count 5 --seed 24629 --format json`. Fails with StopIteration while searching parents for scripts/generator_policy.py. Exact stderr is in initial-failure.json. Original entrypoint is preserved in pre-repair-generator.py.
2. Initial shortcut: enumerate the original `batch('moderate', 100, 24629)` domain. All 18 semantic records across nine source templates have a single correct-answer vector per template; initial-shortcut.json records them. The new test reconstructs visible answer vectors instead of accepting sampler metadata.
3. `PY check_relocation.py`: PASS. Checks every runtime import against standard library and declared local files, copies only manifest files, then runs the actual CLI in isolated Python with only the relocated package added to the import path. Five records, no undeclared imports, no runtime-file writes. Result: relocation.json. Registered in ../repair-regressions.json using the retained packaging event code (history has no named findings).
4. `PY validate_repair.py`: PASS. Replays every complete source profile and bank, checks all prior eligible premise cases, evaluates visible implications against compatible rank witnesses, rejects the empty explicit checkbox mask, verifies unsupported bands and determinism, and writes source-replay-report.json, test-records.json, counterfactuals.json, native-input.json and pedagogical-variation.json. Current results: 15 banks, 81 complete choices / 54 distractors, 316 decision records, 12 legacy premise records; 106 identical-hypothesis cue groups across 14 recognizable profiles. The script calls the following shared tools once per validation pass:

   `REPO/generate/runs/current/check-engine evidence/native-input.json evidence/native-report.json`

   PASS: 623 accepted responses, 1,232 rejected responses, zero unresolved; zero database writes.

   `PY REPO/generate/pipeline/check_delivery.py --input evidence/test-records.json --source JOB/source/source.json --inventory JOB/source/inventory.json --difficulty moderate --output evidence/delivery --math-root /media/jake/SSD/EDB/math`

   PASS: 316 accepted. Coverage/cue probes are computed before and after filtering. Unclassified resolves to the declared moderate default; the shared tool requires the effective band.
5. `PY REPO/generate/pipeline/check_delivery.py --input evidence/samples.json --source JOB/source/source.json --inventory JOB/source/inventory.json --difficulty moderate --output evidence/delivery-samples --math-root /media/jake/SSD/EDB/math`

   PASS: requested sample accepted 5/5, no duplicates.
6. `PY REPO/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --math-root /media/jake/SSD/EDB/math`

   PASS: five actual UI screenshots. Initial horizontal theorem clipping was found by visual inspection and repaired by stacking its equivalence. All five final screenshots inspected; see visual-review.json and render/rendering.json. No assets were generated or published.

Source fidelity, mathematics, grading, variation, delivery and visual layout are separate claims with the corresponding reports. Symbolic dimensions have representative rank witnesses at n=1,2,5,9; the lesson's universal theorem supplies the general justification. Inventory assessment inspected all 16 supplied IDs and verified equality with the original source IDs, and absence of generator provenance. No stored generated instance of the runtime/structural findings exists in this snapshot. Original errors are described separately in inventory-assessment.json; database content was not edited. Live learner history, later inventory, and configured policy draws are outside the offline evidence.
